"""NVIDIA vLLM checkpoint preparation, activation QDQ and engine auditing.

Imports of torch, transformers and compressed-tensors are lazy so plans and reports
also work on machines without a CUDA installation.
"""
from __future__ import annotations

import gc
import hashlib
import importlib.metadata
import json
import os
import platform
import resource
from pathlib import Path

ACTIVATION_POLICY = "cuda-e4m3-per-token-input-qdq-v1"
MEMORY_POLICY = "engine-per-request-cuda-allocator-peak-rss-v1"
WEIGHT_POLICY = "compressed-tensors-streaming-rtn-weight-only-v1"
REQUIRED_PACKAGES = ("vllm", "torch", "transformers", "compressed-tensors", "psutil")
DESCRIPTIONS = {
    "FP8": "FP8 E4M3 per-channel weights; Marlin BF16 projection inputs (W8A16)",
    "FP8_A8": "Fixed FP8 E4M3 weights; per-token FP8-rounded projection inputs with BF16 buffers (A8 QDQ)",
    "INT4": "Symmetric INT4 weights, groups of 128; BF16 activations (W4A16)",
}


def hardware_info():
    info = {"compatible_os": platform.system() == "Linux", "cuda_available": False,
            "cuda_visible_devices": os.environ.get("CUDA_VISIBLE_DEVICES")}
    try:
        import torch
        info["cuda_runtime"] = torch.version.cuda
        info["cuda_available"] = torch.cuda.is_available() and torch.version.cuda is not None
        if info["cuda_available"]:
            # Single-GPU experiments use logical device zero. CUDA_VISIBLE_DEVICES
            # selects the physical GPU before any CUDA or vLLM import.
            gpu = torch.cuda.get_device_properties(0)
            info.update(gpu_name=gpu.name, gpu_memory_bytes=gpu.total_memory,
                        gpu_compute_capability=[gpu.major, gpu.minor],
                        visible_gpu_count=torch.cuda.device_count(), gpu_uuid=str(getattr(gpu, "uuid", "")))
    except (ImportError, RuntimeError, OSError) as error:
        info["cuda_unavailable_reason"] = str(error)
    return info


def engine_arguments(precision):
    kwargs = {"tensor_parallel_size": 1, "compilation_config": {"mode": 0},
              "enable_chunked_prefill": True, "attention_config": {"backend": "TRITON_ATTN"}}
    if precision in DESCRIPTIONS:
        kwargs.update(quantization="compressed-tensors", kernel_config={"linear_backend": "marlin"})
    return kwargs


def quantization_recipe(precision):
    weights = {"num_bits": 8, "type": "float", "strategy": "channel", "symmetric": True}
    if precision == "INT4":
        weights = {"num_bits": 4, "type": "int", "strategy": "group", "group_size": 128, "symmetric": True}
    return {"targets": ["Linear"], "weights": weights,
            "input_activations": None, "output_activations": None}


def validate_checkpoint(directory, precision, stats):
    config = json.loads((Path(directory) / "config.json").read_text())
    quant = config.get("quantization_config") or {}
    if quant.get("quant_method") != "compressed-tensors":
        raise ValueError("CUDA quantization requires a compressed-tensors checkpoint")
    groups = list((quant.get("config_groups") or {}).values())
    wanted = quantization_recipe(precision)["weights"]
    if not groups or any(any(group.get("weights", {}).get(key) != value for key, value in wanted.items())
                         or group.get("input_activations") or group.get("output_activations") for group in groups):
        raise ValueError("CUDA checkpoint must contain the requested weight-only recipe")
    if precision == "INT4":
        if not stats["elements_by_dtype"].get("I32"):
            raise ValueError("INT4 checkpoint does not contain packed integer tensors")
    elif not stats["elements_by_dtype"].get("F8_E4M3"):
        raise ValueError("FP8 checkpoint does not contain E4M3 tensors")
    return stats


def prepare_checkpoint(source, source_revision, model, precision, model_dir, read_stats, write_json):
    source = Path(source)
    config = json.loads((source / "config.json").read_text())
    if config.get("quantization") or config.get("quantization_config"):
        raise ValueError("Use an unquantized source model for comparable CUDA variants")
    if precision in ("FP32", "BF16"):
        # vLLM's CUDA loader casts the original tensors to the requested dtype.
        stats = {**read_stats(source), "weight_payload_scope": "Original source checkpoint; CUDA loaded dtype is audited separately"}
        return source, stats, True
    precision = "FP8" if precision == "FP8_A8" else precision
    identity = {"model": model, "revision": source_revision, "backend": "cuda", "policy": WEIGHT_POLICY,
                "recipe": quantization_recipe(precision),
                "packages": {name: importlib.metadata.version(name) for name in ("torch", "transformers", "compressed-tensors")}}
    key = hashlib.sha256(json.dumps(identity, sort_keys=True).encode()).hexdigest()[:16]
    destination = Path(model_dir) / ("cuda-" + key) / precision
    marker = destination / "comparison_manifest.json"
    if marker.exists():
        if json.loads(marker.read_text())["identity"] != identity:
            raise ValueError("CUDA checkpoint identity mismatch")
        return destination, validate_checkpoint(destination, precision, read_stats(destination)), True
    if destination.exists():
        raise ValueError("Incomplete CUDA conversion at " + str(destination) + "; move it aside and rerun")
    stream_checkpoint(source, destination, precision, write_json)
    stats = validate_checkpoint(destination, precision, read_stats(destination))
    write_json(marker, {"identity": identity, "weight_stats": stats})
    return destination, stats, False


def compress_weight(weight, precision):
    """Use official compressed-tensors quantization/packing on one CPU tensor."""
    from compressed_tensors.quantization import QuantizationScheme
    from compressed_tensors.quantization.utils import calculate_qparams
    from compressed_tensors.compressors.naive_quantized import FloatQuantizationCompressor
    from compressed_tensors.compressors.pack_quantized import PackedQuantizationCompressor

    scheme = QuantizationScheme(**quantization_recipe(precision))
    values = weight.float()
    if precision == "INT4":
        if values.shape[-1] % 128:
            raise ValueError("CUDA INT4 requires projection input dimensions divisible by 128")
        values = values.reshape(values.shape[0], -1, 128)
        low, high = values.amin(dim=-1), values.amax(dim=-1)
        compressor = PackedQuantizationCompressor
    else:
        low, high = values.amin(dim=-1, keepdim=True), values.amax(dim=-1, keepdim=True)
        compressor = FloatQuantizationCompressor
    scales, zero_points = calculate_qparams(low, high, scheme.weights)
    state = {"weight": weight, "weight_scale": scales, "weight_zero_point": zero_points}
    return compressor.compress(state, scheme)


def stream_checkpoint(source, destination, precision, write_json):
    """Discover Linear targets on meta, then convert one tensor at a time on CPU."""
    import torch
    from transformers import AutoConfig, AutoModelForCausalLM
    from safetensors import safe_open
    from safetensors.torch import save_file
    from compressed_tensors.quantization import QuantizationConfig, QuantizationScheme

    config = AutoConfig.from_pretrained(str(source), trust_remote_code=False)
    with torch.device("meta"):
        architecture = AutoModelForCausalLM.from_config(config, dtype=torch.bfloat16, trust_remote_code=False)
    head = architecture.get_output_embeddings()
    targets = {name for name, module in architecture.named_modules()
               if isinstance(module, torch.nn.Linear) and module is not head}
    if not targets:
        raise ValueError("CUDA conversion requires standard dense Linear projections")
    del architecture, head
    gc.collect()
    destination.mkdir(parents=True)
    shard, shard_bytes, index, shard_id, converted = {}, 0, {}, 0, set()
    total_size = 0
    def flush():
        nonlocal shard, shard_bytes, shard_id
        if shard:
            shard_id += 1
            filename = f"model-{shard_id:05d}.safetensors"
            save_file(shard, str(destination / filename), metadata={"format": "pt"})
            index.update({key: filename for key in shard})
            shard, shard_bytes = {}, 0
    for filename in sorted(source.glob("*.safetensors")):
        with safe_open(str(filename), framework="pt", device="cpu") as tensors:
            for name in tensors.keys():
                tensor = tensors.get_tensor(name)
                if tensor.is_floating_point():
                    tensor = tensor.to(torch.bfloat16)
                prefix = name.removesuffix(".weight")
                if name.endswith(".weight") and prefix in targets:
                    converted.add(prefix)
                    outputs = {prefix + "." + key: value for key, value in compress_weight(tensor, precision).items()}
                else:
                    outputs = {name: tensor}
                for key, value in outputs.items():
                    size = value.numel() * value.element_size()
                    if shard_bytes + size > 128 * 1024**2:
                        flush()
                    shard[key] = value.contiguous()
                    shard_bytes += size
                    total_size += size
    flush()
    if converted != targets:
        raise ValueError("CUDA checkpoint is missing Linear weights: " + ", ".join(sorted(targets - converted)))
    quant = QuantizationConfig(config_groups={"weights": QuantizationScheme(**quantization_recipe(precision))},
        format="pack-quantized" if precision == "INT4" else "float-quantized",
        quantization_status="compressed", ignore=["lm_head"])
    saved_config = json.loads((source / "config.json").read_text())
    saved_config.update(dtype="bfloat16", torch_dtype="bfloat16", quantization_config=quant.model_dump(mode="json"))
    write_json(destination / "config.json", saved_config)
    write_json(destination / "model.safetensors.index.json", {"metadata": {"total_size": total_size}, "weight_map": index})


def fp8_round_trip(x):
    """Dynamic E4M3 per-token QDQ. Return BF16 buffers; never modify x."""
    import torch
    if x.dtype != torch.bfloat16:
        raise ValueError("CUDA FP8 rounding requires BF16 projection inputs")
    values = x.float()
    maximum = torch.finfo(torch.float8_e4m3fn).max
    scale = (values.abs().amax(dim=-1, keepdim=True) / maximum).clamp_min(torch.finfo(torch.float32).tiny)
    quantized = (values / scale).clamp(-maximum, maximum).to(torch.float8_e4m3fn)
    return (quantized.float() * scale).to(x.dtype)


def _fp8_projections(model):
    projections = []
    for name, module in model.named_modules():
        method = getattr(module, "quant_method", None)
        scheme = getattr(module, "scheme", None)
        if type(scheme).__name__ == "CompressedTensorsW8A16Fp8":
            if type(getattr(scheme, "linear_kernel", None)).__name__ != "MarlinFP8ScaledMMLinearKernel":
                raise ValueError("CUDA FP8 baseline requires the weight-only Marlin kernel")
            projections.append((name, module))
        elif scheme is not None or (method is not None and "Unquantized" not in type(method).__name__
                                   and type(method).__name__ != "CompressedTensorsKVCacheMethod"):
            raise ValueError("Unsupported CUDA quantized module: " + name + "/" + type(method).__name__)
    if not projections:
        raise ValueError("CUDA model has no FP8 weight-only projections")
    return projections


def round_fp8_activations(model):
    projections = _fp8_projections(model)  # Validate everything before mutating.
    if any(getattr(module, "activation_quantization", None) for _, module in projections):
        raise ValueError("CUDA activation rounding was already installed")
    def pre_hook(module, args, kwargs):
        if args:
            return (fp8_round_trip(args[0]), *args[1:]), kwargs
        key = next((key for key in ("input_", "x") if key in kwargs), None)
        if key is None:
            raise ValueError("CUDA projection did not receive its input tensor")
        return args, {**kwargs, key: fp8_round_trip(kwargs[key])}
    for _, module in projections:
        module.register_forward_pre_hook(pre_hook, with_kwargs=True)
        module.activation_quantization = ACTIVATION_POLICY
    return {"activation_policy": ACTIVATION_POLICY, "rounded_projections": [name for name, _ in projections]}


def audit_loaded_model(model):
    """Fingerprint parameters in bounded CPU chunks, outside inference timing."""
    import torch
    histogram, weight_bytes, quantized = {}, 0, []
    digest = hashlib.sha256()
    for name, tensor in sorted(model.named_parameters()):
        dtype = str(tensor.dtype).split(".")[-1]
        histogram[dtype] = histogram.get(dtype, 0) + tensor.numel()
        weight_bytes += tensor.numel() * tensor.element_size()
        digest.update(json.dumps([name, dtype, list(tensor.shape)]).encode())
        flattened = tensor.detach().reshape(-1)
        for offset in range(0, flattened.numel(), 1024**2):
            digest.update(flattened[offset:offset + 1024**2].contiguous().view(torch.uint8).cpu().numpy().tobytes())
    for name, module in model.named_modules():
        scheme = getattr(module, "scheme", None)
        if scheme is not None:
            quantized.append({"name": name, "scheme": type(scheme).__name__,
                "kernel": type(getattr(scheme, "linear_kernel", None) or getattr(scheme, "kernel", None)).__name__,
                "bits": getattr(getattr(scheme, "weight_quant", None), "num_bits", getattr(scheme, "num_bits", None)),
                "group_size": getattr(scheme, "group_size", None),
                "activation_quantization": getattr(module, "activation_quantization", None)})
    return {"engine_pid": os.getpid(), "loaded_elements_by_dtype": histogram, "loaded_weight_bytes": weight_bytes,
            "weight_sha256": digest.hexdigest(), "quantized_modules": quantized,
            "audit_scope": "Torch model parameters, including quantization scales; CUDA workspaces/KV excluded"}


def validate_audit(audit, precision):
    quantized = audit["quantized_modules"]
    if precision in ("FP8", "FP8_A8"):
        if not quantized or any(m["scheme"] != "CompressedTensorsW8A16Fp8"
                               or m["bits"] != 8 or m["kernel"] != "MarlinFP8ScaledMMLinearKernel" for m in quantized):
            raise ValueError("CUDA FP8 model did not load weight-only Marlin projections")
        wanted = ACTIVATION_POLICY if precision == "FP8_A8" else None
        if any(m["activation_quantization"] != wanted for m in quantized):
            raise ValueError("CUDA FP8 activation policy mismatch")
    elif precision == "INT4":
        if not quantized or any(m["scheme"] != "CompressedTensorsWNA16" or m["bits"] != 4
                               or m["group_size"] != 128 or m["kernel"] != "MarlinLinearKernel" for m in quantized):
            raise ValueError("CUDA INT4 model did not load W4A16 projections")
    else:
        dtype = "float32" if precision == "FP32" else "bfloat16"
        if quantized or not audit["loaded_elements_by_dtype"].get(dtype):
            raise ValueError("CUDA model dtype does not match the requested dense precision")


def engine_memory(model, reset_peak=False):
    import torch
    import psutil
    torch.cuda.synchronize()
    if reset_peak:
        torch.cuda.reset_peak_memory_stats()
    free, total = torch.cuda.mem_get_info()
    return {"pid": os.getpid(), "cuda_allocated_bytes": torch.cuda.memory_allocated(),
            "cuda_reserved_bytes": torch.cuda.memory_reserved(),
            "cuda_peak_allocated_bytes": torch.cuda.max_memory_allocated(),
            "cuda_peak_reserved_bytes": torch.cuda.max_memory_reserved(),
            "cuda_device_used_bytes": total - free, "rss_bytes": psutil.Process().memory_info().rss,
            "rss_high_water_bytes": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
            * (1 if platform.system() == "Darwin" else 1024)}


def begin_request_memory(model):
    return engine_memory(model, reset_peak=True)
