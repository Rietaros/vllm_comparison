#!/usr/bin/env python3
"""Repeated precision/context benchmarks on Apple Metal or NVIDIA CUDA."""
from __future__ import annotations

import argparse
import csv
import hashlib
import importlib.metadata
import json
import math
import os
import platform
import re
import signal
import shutil
import struct
import statistics
import subprocess
import sys
import time
from datetime import datetime, timezone
from difflib import SequenceMatcher
from collections import Counter
from pathlib import Path

from prompt_tasks import PROMPT_SUITE, SYSTEM, TASK_BUILDERS, task_suite_sha256
from answer_comparison import SCORING_POLICY, score_answer
from benchmark_config import DEFAULT_CONFIG, MODEL_TIERS, load_models
from benchmark_backend import (resolve_backend, add_backend_arguments, device_memory_budget,
                               hardware_description, CACHE_POLICIES)
from activation_experiment import (ACTIVATION_PRECISIONS, ACTIVATION_POLICY, MEMORY_POLICY, MEMORY_METRICS,
    round_fp8_activations, sample_memory, memory_fields, write_comparison)

ROOT = Path(__file__).resolve().parent
MIB = 1024 ** 2
SPECS = {
    "FP32": {"bits": 32, "dtype": "float32", "mode": None,
             "description": "FP32 weights and activations; reductions may use backend-specific precision"},
    "BF16": {"bits": 16, "dtype": "bfloat16", "mode": None,
             "description": "BF16 weights and activations; reductions may use FP32"},
    "FP8": {"bits": 8, "dtype": "bfloat16", "mode": "mxfp8", "group_size": 32,
            "description": "MXFP8 E4M3 weights with block scales; BF16 activations (W8A16)"},
    "INT4": {"bits": 4, "dtype": "bfloat16", "mode": "affine", "group_size": 64,
             "description": "Affine INT4 weights with group scales/biases; BF16 activations (W4A16)"},
}
DEFAULT_PRECISIONS = tuple(SPECS)
SPECS["FP8_A8"] = {**SPECS["FP8"], "weight_format": "FP8",
                   "description": "Fixed MXFP8 weights; MXFP8-rounded projection inputs with BF16 buffers (A8 QDQ)"}
LEVELS = ("Short", "Medium", "Long")


def write_json(path, data):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(data, indent=2, ensure_ascii=False, allow_nan=False) + "\n")
    temporary.replace(path)


def local_environment():
    # Keep downloads and compiled caches inside the workspace.
    defaults = {"HF_HOME": str(ROOT / ".cache/huggingface"),
                "VLLM_CACHE_ROOT": str(ROOT / ".cache/vllm"),
                "XDG_CACHE_HOME": str(ROOT / ".cache"),
                "VLLM_WORKER_MULTIPROC_METHOD": "spawn", "TOKENIZERS_PARALLELISM": "false",
                # Required by the vLLM apply_model RPC for our trusted local audit
                # callback. The engine is local; no serving endpoint is opened.
                "VLLM_ALLOW_INSECURE_SERIALIZATION": "1"}
    for key, value in defaults.items():
        os.environ.setdefault(key, value)


def hardware_info(backend="auto"):
    backend = resolve_backend(backend)
    info = {"os": platform.system(), "os_version": platform.mac_ver()[0] or platform.release(),
            "architecture": platform.machine(), "python": platform.python_version(),
            "cpu_cores": os.cpu_count(), "backend": backend}
    if platform.system() == "Linux":
        info["memory_bytes"] = os.sysconf("SC_PAGE_SIZE") * os.sysconf("SC_PHYS_PAGES")
    if platform.system() == "Darwin":
        for key, command in (("chip", ["sysctl", "-n", "machdep.cpu.brand_string"]),
                             ("memory_bytes", ["sysctl", "-n", "hw.memsize"])):
            result = subprocess.run(command, capture_output=True, text=True)
            if result.returncode == 0:
                info[key] = int(result.stdout) if key == "memory_bytes" else result.stdout.strip()
        if "memory_bytes" not in info:
            result = subprocess.run(["system_profiler", "SPHardwareDataType", "-json"], capture_output=True, text=True)
            if result.returncode == 0:
                device = json.loads(result.stdout)["SPHardwareDataType"][0]
                info["chip"] = device.get("chip_type", "Apple Silicon")
                memory = device.get("physical_memory", "")
                if re.fullmatch(r"\d+ GB", memory):
                    info["memory_bytes"] = int(memory.split()[0]) * 1024 ** 3
    packages = {}
    if backend == "cuda":
        from cuda_backend import REQUIRED_PACKAGES
        names = REQUIRED_PACKAGES
    else:
        names = ("vllm", "vllm-metal", "mlx", "mlx-lm", "torch", "transformers")
    for package in names:
        try:
            packages[package] = importlib.metadata.version(package)
        except importlib.metadata.PackageNotFoundError:
            packages[package] = None
    info["packages"] = packages
    if backend == "cuda":
        import cuda_backend
        info.update(cuda_backend.hardware_info())
        return info
    info["compatible_os"] = (info["os"] == "Darwin" and info["architecture"] == "arm64"
                             and int((info["os_version"] or "0").split(".")[0]) >= 15)
    if info["compatible_os"] and packages.get("mlx"):
        import mlx.core as mx
        info["metal_device"] = mx.device_info()
        result = subprocess.run(["system_profiler", "SPDisplaysDataType", "-json"], capture_output=True, text=True)
        if result.returncode == 0:
            devices = json.loads(result.stdout).get("SPDisplaysDataType", [])
            cores = next((gpu.get("sppci_cores") for gpu in devices if gpu.get("sppci_cores")), None)
            if cores and str(cores).isdigit():
                info["gpu_cores"] = int(cores)
        result = subprocess.run(["vm_stat"], capture_output=True, text=True)
        info["memory_snapshot"] = result.stdout.strip()
        result = subprocess.run(["sysctl", "-n", "vm.swapusage"], capture_output=True, text=True)
        info["swap_snapshot"] = result.stdout.strip()
    return info


def laptop_memory_budget(hardware, fraction=None, budget_gib=None):
    """Compatibility alias for the shared Metal/CUDA budget planner."""
    return device_memory_budget(hardware, fraction, budget_gib)


def add_memory_arguments(parser):
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--memory-budget-gib", type=float,
                       help="Weight + KV + runtime planning budget in GiB (default: 10), capped to device limits")
    group.add_argument("--memory-fraction", type=float, help="Fraction of unified RAM (Metal) or selected GPU VRAM (CUDA)")


def validate_memory_arguments(args, parser):
    if args.memory_budget_gib is None and args.memory_fraction is None:
        args.memory_budget_gib = 10.0
    if args.memory_budget_gib is not None and (not math.isfinite(args.memory_budget_gib) or args.memory_budget_gib <= 0):
        parser.error("--memory-budget-gib must be finite and positive")
    backend = resolve_backend(getattr(args, "backend", "metal"))
    maximum = .95 if backend == "cuda" else .7
    if args.memory_fraction is not None and not 0 < args.memory_fraction <= maximum:
        parser.error(f"--memory-fraction must be > 0 and <= {maximum} for {backend}")


def add_precision_arguments(parser):
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--precisions", nargs="+", choices=list(SPECS), default=list(DEFAULT_PRECISIONS))
    group.add_argument("--activation-comparison", action="store_true",
                       help="Compare fixed FP8 weights with BF16 vs FP8-rounded activations and engine memory")


def activation_settings(precisions, backend="metal"):
    if backend == "cuda":
        import cuda_backend
        activation_policy, memory_policy = cuda_backend.ACTIVATION_POLICY, cuda_backend.MEMORY_POLICY
    else:
        activation_policy, memory_policy = ACTIVATION_POLICY, MEMORY_POLICY
    return ({"activation_policy": activation_policy, "memory_policy": memory_policy,
             "activation_baseline": "FP8", "kv_cache_dtype": "bfloat16"} if "FP8_A8" in precisions else {})


def precision_description(precision, backend="metal"):
    if backend == "cuda":
        from cuda_backend import DESCRIPTIONS
        return DESCRIPTIONS.get(precision, SPECS[precision]["description"])
    return SPECS[precision]["description"]


def memory_plan(config, parameter_count, precision, max_model_len, hardware, fraction=None, budget_gib=None):
    """Conservative runtime estimate for one dense GQA request; not measured RSS."""
    spec = SPECS[precision]
    weight_bytes = math.ceil(parameter_count * spec["bits"] / 8)
    if spec["mode"]:
        # Block scales, affine biases and remaining dense tensors need space too.
        weight_bytes = math.ceil(weight_bytes * 1.10)
        if hardware.get("backend") == "cuda":
            # CUDA keeps token embeddings and the output head in BF16. Their
            # large vocabulary matrices must not be budgeted as FP8/INT4.
            dense = config.get("vocab_size", 0) * config["hidden_size"] * (1 if config.get("tie_word_embeddings") else 2)
            weight_bytes += min(dense, parameter_count) * (2 - spec["bits"] / 8)
            weight_bytes = math.ceil(weight_bytes)
    head_dim = config.get("head_dim", config["hidden_size"] // config["num_attention_heads"])
    cache_per_token = (2 * config["num_hidden_layers"] * config.get("num_key_value_heads", config["num_attention_heads"])
                       * head_dim * (4 if precision == "FP32" else 2))
    cache_bytes = max(256 * MIB, math.ceil(cache_per_token * (max_model_len + 128) / (64 * MIB)) * 64 * MIB)
    cuda = hardware.get("backend") == "cuda"
    overhead = (2 if cuda else 1) * 1024 * MIB  # Workspace, activations and engine reserve.
    limits = device_memory_budget(hardware, fraction, budget_gib)
    budget = limits["effective_bytes"]
    block_size = 16
    # Metal 0.30 budgets against its recommended working set, and its paged
    # path ignores kv_cache_memory_bytes. Upstream's block override is honored.
    blocks = math.ceil(cache_bytes / (cache_per_token * block_size))
    allocated_cache = blocks * cache_per_token * block_size
    required = weight_bytes + allocated_cache + overhead
    return {"estimated_weight_bytes": weight_bytes, "kv_cache_bytes": cache_bytes,
            "allocated_kv_cache_bytes": allocated_cache, "cache_block_size": block_size,
            "num_gpu_blocks": blocks, "backend_memory_fraction": limits["backend_memory_fraction"],
            "requested_runtime_budget_bytes": limits["requested_bytes"], "budget_source": limits["source"],
            "runtime_reserve_bytes": overhead, "estimated_runtime_bytes": required,
            "runtime_budget_bytes": budget, "fits": required <= budget,
            "reason": f"Estimated weights + KV + runtime reserve = {required / 1024**3:.2f} GiB; "
                      f"configured {'GPU VRAM' if cuda else 'unified RAM'} budget = {budget / 1024**3:.2f} GiB"}


def stream_qwen3_checkpoint(source, destination, precision):
    """Convert Qwen3 one tensor at a time on CPU, bounding conversion RAM.

    Matches MLX-LM's default Qwen3 recipe: quantize embeddings and linear
    weights; preserve norms, remove a redundant tied lm_head. No model forward.
    """
    import numpy as np
    import mlx.core as mx
    config = json.loads((source / "config.json").read_text())
    if config["model_type"] != "qwen3":
        raise ValueError("Streaming conversion supports the dense Qwen3 architecture only")
    spec = SPECS[precision]
    destination.mkdir(parents=True)
    # Copy tokenizer and metadata; rebuild the tensor index below.
    for path in source.iterdir():
        if path.is_file() and path.suffix in (".json", ".jinja", ".txt", ".model") and not path.name.endswith(".index.json"):
            shutil.copyfile(path, destination / path.name)
    dtype_map = {"BF16": np.uint16, "F16": np.float16, "F32": np.float32}
    shard, shard_bytes, index, payload, shard_id = {}, 0, {}, 0, 0
    def flush():
        nonlocal shard, shard_bytes, shard_id, payload
        if not shard:
            return
        shard_id += 1
        filename = f"model-{shard_id:05d}.safetensors"
        mx.save_safetensors(str(destination / filename), shard, metadata={"format": "mlx"})
        index.update({name: filename for name in shard})
        payload += shard_bytes
        shard, shard_bytes = {}, 0
        mx.clear_cache()
    with mx.stream(mx.cpu):
        for path in sorted(source.glob("*.safetensors")):
            with path.open("rb") as stream:
                header_size = struct.unpack("<Q", stream.read(8))[0]
                header = json.loads(stream.read(header_size))
            for name, item in header.items():
                if name == "__metadata__" or (name == "lm_head.weight" and config.get("tie_word_embeddings")):
                    continue
                if item["dtype"] not in dtype_map:
                    raise ValueError("Unsupported Qwen3 source dtype " + item["dtype"])
                mapped = np.memmap(path, mode="r", dtype=dtype_map[item["dtype"]],
                                   offset=8 + header_size + item["data_offsets"][0], shape=tuple(item["shape"]))
                tensor = mx.array(mapped)
                if item["dtype"] == "BF16":
                    tensor = tensor.view(mx.bfloat16)
                tensor = tensor.astype(getattr(mx, spec["dtype"]))
                if spec["mode"] and len(item["shape"]) == 2 and name.endswith(".weight"):
                    if item["shape"][-1] % spec["group_size"]:
                        raise ValueError("Qwen3 matrix cannot use the requested group size: " + name)
                    quantized = mx.quantize(tensor, group_size=spec["group_size"], bits=spec["bits"], mode=spec["mode"])
                    suffixes = ("weight", "scales", "biases") if spec["mode"] == "affine" else ("weight", "scales")
                    values = {name.rsplit(".", 1)[0] + "." + suffix: value for suffix, value in zip(suffixes, quantized)}
                else:
                    values = {name: tensor}
                mx.eval(list(values.values()))
                size = sum(v.nbytes for v in values.values())
                if shard_bytes + size > 128 * MIB:
                    flush()
                shard.update(values)
                shard_bytes += size
                del tensor, mapped, values
                if spec["mode"] and len(item["shape"]) == 2:
                    del quantized
        flush()
    config.update(torch_dtype=spec["dtype"], dtype=spec["dtype"])
    if spec["mode"]:
        quant = {key: spec[key] for key in ("bits", "group_size", "mode")}
        config.update(quantization=quant, quantization_config=quant)
    write_json(destination / "config.json", config)
    write_json(destination / "model.safetensors.index.json", {"metadata": {"total_size": payload}, "weight_map": index})


def safetensors_info(directory, exclude_names=()):
    """Inspect actual saved tensor types/bytes without loading model weights."""
    tensors, total_bytes, total_elements, dtype_elements = {}, 0, 0, {}
    for path in sorted(Path(directory).glob("*.safetensors")):
        with path.open("rb") as stream:
            length = struct.unpack("<Q", stream.read(8))[0]
            if length > 100 * MIB:
                raise ValueError("Unexpected safetensors header size")
            header = json.loads(stream.read(length))
        for name, item in header.items():
            if name == "__metadata__" or name in exclude_names:
                continue
            if name in tensors:
                raise ValueError("Duplicate tensor: " + name)
            tensors[name] = item
            total_bytes += item["data_offsets"][1] - item["data_offsets"][0]
            count = math.prod(item["shape"])
            total_elements += count
            dtype_elements[item["dtype"]] = dtype_elements.get(item["dtype"], 0) + count
    if not tensors:
        raise ValueError("No safetensors weights in " + str(directory))
    return {"tensor_count": len(tensors), "stored_elements": total_elements,
            "weight_payload_bytes": total_bytes, "elements_by_dtype": dtype_elements}


def validate_checkpoint(directory, precision):
    spec = SPECS[precision]
    config = json.loads((Path(directory) / "config.json").read_text())
    stats = safetensors_info(directory)
    quant = config.get("quantization", {})
    if spec["mode"]:
        if quant.get("mode", "affine") != spec["mode"] or quant.get("bits") != spec["bits"]:
            raise ValueError("Checkpoint quantization does not match " + precision)
        if quant.get("group_size") != spec["group_size"]:
            raise ValueError("Checkpoint group size does not match " + precision)
        if not stats["elements_by_dtype"].get("U32"):
            raise ValueError("Quantized checkpoint has no packed uint32 weights")
    else:
        expected_dtype = "F32" if precision == "FP32" else "BF16"
        if quant or config.get("quantization_config"):
            raise ValueError("Dense checkpoint unexpectedly contains quantization metadata")
        if not stats["elements_by_dtype"].get(expected_dtype):
            raise ValueError("Checkpoint has no " + expected_dtype + " weights")
        wrong = {key for key in stats["elements_by_dtype"]
                 if key.startswith(("F", "BF")) and key != expected_dtype}
        if wrong:
            raise ValueError("Dense checkpoint contains unexpected floating types: " + str(wrong))
    return stats


def resolve_source(model, revision):
    from huggingface_hub import snapshot_download
    local = Path(model).expanduser()
    if local.is_dir():
        return local.resolve(), "local:" + str(local.resolve())
    path = Path(snapshot_download(model, revision=revision,
                                 allow_patterns=["*.json", "*.safetensors", "*.model", "*.txt", "*.jinja"], max_workers=2))
    return path, path.name  # The snapshot directory name is the resolved commit.


def prepare_checkpoint(source, source_revision, model, precision, model_dir):
    # Activation rounding must reuse the baseline's bytes and conversion identity.
    precision = SPECS[precision].get("weight_format", precision)
    from mlx_lm.convert import convert
    spec = SPECS[precision]
    config = json.loads((source / "config.json").read_text())
    identity = {"model": model, "revision": source_revision, "spec": spec,
                "mlx": importlib.metadata.version("mlx"), "mlx_lm": importlib.metadata.version("mlx-lm")}
    if config.get("model_type") == "qwen3":
        identity["conversion"] = "streaming-qwen3-v1"
    key = hashlib.sha256(json.dumps(identity, sort_keys=True).encode()).hexdigest()[:16]
    destination = Path(model_dir) / key / precision
    marker = destination / "comparison_manifest.json"
    if marker.exists():
        saved = json.loads(marker.read_text())
        if saved["identity"] != identity:
            raise ValueError("Prepared checkpoint identity mismatch")
        return destination, validate_checkpoint(destination, precision), True
    if destination.exists():
        raise ValueError("Incomplete conversion at " + str(destination) + "; move it aside and rerun")
    if config.get("quantization") or config.get("quantization_config"):
        raise ValueError("Use an unquantized base model so all four variants share the same source weights")
    kwargs = {"hf_path": str(source), "mlx_path": str(destination), "dtype": spec["dtype"]}
    if spec["mode"]:
        kwargs.update(quantize=True, q_bits=spec["bits"], q_group_size=spec["group_size"], q_mode=spec["mode"])
    if config.get("model_type") == "qwen3":
        stream_qwen3_checkpoint(source, destination, precision)
    else:
        convert(**kwargs)
    # Metal's MLX loader preserves checkpoint dtypes; prepare the actual weights
    # instead of assuming that vLLM's dtype flag casts the checkpoint for us.
    config_path = destination / "config.json"
    config = json.loads(config_path.read_text())
    config.update(torch_dtype=spec["dtype"], dtype=spec["dtype"])
    write_json(config_path, config)
    stats = validate_checkpoint(destination, precision)
    write_json(marker, {"identity": identity, "weight_stats": stats})
    return destination, stats, False


def make_prompts(tokenizer, budgets, enable_thinking=None):
    """Fit distinct complete tasks by adding unique records, never repeated filler."""
    prompts = []
    for level, budget in zip(LEVELS, budgets):
        def encode(count):
            task = TASK_BUILDERS[level](count)
            messages = [{"role": "system", "content": SYSTEM}, {"role": "user", "content": task["prompt"]}]
            extra = {} if enable_thinking is None else {"enable_thinking": enable_thinking}
            ids = tokenizer.apply_chat_template(messages, tokenize=True, add_generation_prompt=True,
                                                return_dict=False, **extra)
            return task, list(ids)
        task, ids = encode(0)
        if len(ids) > budget:
            raise ValueError(f"{level} budget {budget} is below the minimum prompt size {len(ids)}")
        if task["task_mode"] == "generated":
            low, high = 0, 1
            while len(encode(high)[1]) <= budget:
                low, high = high, high * 2
            high -= 1
            while low < high:
                middle = (low + high + 1) // 2
                if len(encode(middle)[1]) <= budget:
                    low = middle
                else:
                    high = middle - 1
            task, ids = encode(low)
        digest = hashlib.sha256(json.dumps(ids).encode()).hexdigest()
        prompts.append({**task, "context": level, "prompt_suite": PROMPT_SUITE,
                        "target_tokens": budget, "input_tokens": len(ids),
                        "prompt_token_ids": ids, "prompt_sha256": digest})
    if all(p["task_mode"] == "generated" for p in prompts) and len({p["input_tokens"] for p in prompts}) != 3:
        raise ValueError("Context budgets must produce three distinct token lengths")
    return prompts


def task_metadata(prompt):
    return {key: prompt[key] for key in ("prompt_suite", "task_id", "task_mode", "expected", "reasoning_fields", "comparison")
            if key in prompt}


def validate_resume_tasks(previous, current):
    for field in ("prompt_sha256", "expected", "reasoning_fields", "comparison", "task_mode"):
        if [p.get(field) for p in previous] != [p.get(field) for p in current]:
            raise ValueError(f"Resume tasks must match the original inputs and scoring: {field}")


def blank_rows(precision, prompts, status, error, backend="metal"):
    return [{"precision": precision, "backend": backend, "context": p["context"], "status": status, "error": error,
             **task_metadata(p),
             "trial_id": p.get("trial_id", 1),
             "description": precision_description(precision, backend), "input_tokens": p["input_tokens"],
             "prompt_sha256": p["prompt_sha256"], "generation_calls": 0,
             "generation_s": None, "ttft_s": None, "ttft_source": None,
             "ttft_unavailable_reason": "No completed generation", "output": None} for p in prompts]


def trial_key(row):
    return row["context"], row.get("trial_id", 1)


def make_trials(prompts, repeats):
    """Rotate context order each round, with the same schedule for all precisions."""
    trials = []
    for trial_id in range(1, repeats + 1):
        offset = (trial_id - 1) % len(prompts)
        ordered = prompts[offset:] + prompts[:offset]
        trials.extend({**prompt, "trial_id": trial_id} for prompt in ordered)
    return trials


def metric(output, name):
    metrics = getattr(output, "metrics", None)
    return getattr(metrics, name, None) if metrics is not None else None


TIMING_POLICY = "vllm-request-metrics-ttft-v1"


def first_token_timing(output, elapsed):
    """Read engine TTFT without mixing frontend and engine-core clocks.

    vLLM V1 supplies first_token_latency directly. Its arrival_time is wall
    clock, whereas first_token_ts is monotonic; subtracting those is invalid.
    Older engines expose a same-clock arrival_time/first_token_time pair.
    """
    latency = metric(output, "first_token_latency")
    source = "vllm.metrics.first_token_latency"
    if latency is None:
        arrival, first = metric(output, "arrival_time"), metric(output, "first_token_time")
        if arrival is not None and first is not None:
            latency = first - arrival
            source = "vllm.metrics.first_token_time-arrival_time"
    valid = (isinstance(latency, (int, float)) and not isinstance(latency, bool)
             and math.isfinite(latency) and 0 < latency <= elapsed)
    if not valid:
        reason = ("Engine did not expose TTFT metrics" if latency is None else
                  "Engine TTFT was non-finite, non-positive, or longer than the measured request")
        return {"ttft_s": None, "ttft_source": None, "ttft_unavailable_reason": reason}
    return {"ttft_s": latency, "ttft_source": source, "ttft_unavailable_reason": None}


def ttft_cells(summary):
    """Display milliseconds while keeping raw and summary timings in seconds."""
    count = summary.get("ttft_measured_trials", 0)
    completed = summary["trials_successful"]
    if not count:
        return ("unavailable", f"0/{completed}") if completed else ("—", "—")
    mean = summary["ttft_s_mean"] * 1000
    stddev = summary["ttft_s_stddev"]
    deviation = f"{stddev * 1000:.1f}" if stddev is not None else "—"
    return f"{mean:.1f} ± {deviation}", f"{count}/{completed}"


def audit_loaded_model(model):
    """Called inside the engine worker; inspect tensors without any forward pass."""
    from mlx.utils import tree_flatten
    histogram = {}
    weight_bytes = 0
    for _, tensor in tree_flatten(model.parameters()):
        dtype = str(tensor.dtype).split(".")[-1]
        histogram[dtype] = histogram.get(dtype, 0) + tensor.size
        weight_bytes += tensor.nbytes
    quantized = []
    for name, module in model.named_modules():
        if getattr(module, "bits", None) is not None and getattr(module, "mode", None) is not None:
            quantized.append({"name": name, "bits": module.bits, "mode": module.mode,
                              "activation_quantization": getattr(module, "activation_quantization", None)})
    return {"loaded_elements_by_dtype": histogram, "loaded_weight_bytes": weight_bytes,
            "quantized_modules": quantized, "engine_pid": os.getpid(),
            "audit_scope": "Visible MLX module parameters; backend wrapper/compiled state may be outside this tree"}


def run_worker(job):
    """Each precision runs in its own process to release all device/engine memory."""
    local_environment()
    backend = job.get("backend", "metal")
    if backend == "cuda":
        import torch
        import cuda_backend as runtime
        # generate returns CPU token IDs after engine execution. Device counters
        # synchronize inside the engine RPC, where the model actually resides.
        synchronize = lambda: None
    else:
        import mlx.core as mx
        runtime = sys.modules[__name__]
        synchronize = mx.synchronize
    from vllm import LLM, SamplingParams
    from vllm.platforms import current_platform
    if backend == "cuda" and not current_platform.is_cuda():
        raise RuntimeError("Expected NVIDIA CUDA, but vLLM selected " + str(type(current_platform)))
    if backend == "metal" and current_platform.__class__.__module__.split(".")[0] != "vllm_metal":
        raise RuntimeError("Expected the Metal plugin, but vLLM selected " + str(type(current_platform)))
    spec = SPECS[job["precision"]]
    measure_memory = bool(job.get("memory_policy"))
    started = time.perf_counter()
    llm = LLM(model=job["checkpoint"], tokenizer=job["source"], dtype=spec["dtype"],
              max_model_len=job["max_model_len"], max_num_seqs=1,
              max_num_batched_tokens=512, gpu_memory_utilization=job["memory_fraction"],
              kv_cache_memory_bytes=job.get("kv_cache_bytes", 256 * MIB), enable_prefix_caching=False,
              **({"kv_cache_dtype": job["kv_cache_dtype"]} if "kv_cache_dtype" in job else {}),
              **({"block_size": job["cache_block_size"], "num_gpu_blocks_override": job["num_gpu_blocks"]}
                 if "num_gpu_blocks" in job else {}),
              enforce_eager=True, seed=42, trust_remote_code=False,
              distributed_executor_backend="uni", disable_log_stats=False,
              **(runtime.engine_arguments(job["precision"]) if backend == "cuda" else {}))
    engine_load_s = time.perf_counter() - started
    if job["precision"] == "FP8_A8":
        llm.apply_model(runtime.round_fp8_activations)
    audits = llm.apply_model(runtime.audit_loaded_model)
    if len(audits) != 1:
        raise RuntimeError("Expected exactly one engine worker")
    audit = audits[0]
    if backend == "cuda":
        runtime.validate_audit(audit, job["precision"])
        if "experiment_contract" in job:
            job["experiment_contract"].update(backend=backend, weight_policy=runtime.WEIGHT_POLICY,
                                               weight_sha256=audit["weight_sha256"])
    elif spec["mode"]:
        if not audit["quantized_modules"] or any(m["bits"] != spec["bits"] or m["mode"] != spec["mode"]
                                                  for m in audit["quantized_modules"]):
            raise RuntimeError("Loaded quantization does not match the requested precision")
        rounded = [m.get("activation_quantization") == ACTIVATION_POLICY for m in audit["quantized_modules"]]
        if job["precision"] == "FP8_A8" and not all(rounded):
            raise RuntimeError("Loaded projections did not enable FP8 activation rounding")
        if job["precision"] == "FP8" and any(rounded):
            raise RuntimeError("BF16 activation baseline unexpectedly contains FP8 rounding")
    elif audit["loaded_elements_by_dtype"].get(spec["dtype"], 0) == 0 or audit["quantized_modules"]:
        raise RuntimeError("Loaded model does not match requested dense precision")
    params = SamplingParams(temperature=0.0, top_p=1.0, max_tokens=job["max_new_tokens"], seed=42)
    rows = []
    try:
        for prompt in job["prompts"]:
            row = {"precision": job["precision"], "context": prompt["context"],
                   **task_metadata(prompt),
                   "trial_id": prompt.get("trial_id", 1), "status": "running",
                   "backend": backend, "description": precision_description(job["precision"], backend), "input_tokens": prompt["input_tokens"],
                   "prompt_sha256": prompt["prompt_sha256"], "generation_calls": 0,
                   "engine_load_s": engine_load_s, "runtime_audit": audit,
                   **({"experiment_contract": job["experiment_contract"]} if "experiment_contract" in job else {}),
                   "ttft_s": None, "ttft_source": None,
                   "ttft_unavailable_reason": "No completed generation", **job["preparation"]}
            rows.append(row)
            before_memory = {}
            try:
                synchronize()
                if measure_memory:
                    before_memory = sample_memory(llm, audit, before=True, backend=backend)
                # Persist the attempt before generation so interrupted trials
                # cannot be silently repeated on resume. File I/O is not timed.
                row["generation_calls"] = 1
                write_json(job["result_path"], rows)
                start = time.perf_counter()
                generated = llm.generate([{"prompt_token_ids": prompt["prompt_token_ids"]}],
                                         sampling_params=params, use_tqdm=False)[0]
                synchronize()
                elapsed = time.perf_counter() - start
                completion = generated.outputs[0]
                count = len(completion.token_ids)
                row.update(status="ok", generation_s=elapsed, output_tokens=count,
                           end_to_end_tokens_per_s=count / elapsed,
                           output=completion.text, output_token_ids=list(completion.token_ids),
                           finish_reason=completion.finish_reason)
                row.update(first_token_timing(generated, elapsed))
                row.update(score_answer(completion.text, prompt["expected"], prompt.get("reasoning_fields"),
                                        prompt.get("comparison")))
                import resource
                row["driver_peak_rss_bytes"] = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss * (1 if platform.system() == "Darwin" else 1024)
                ttft = f"{row['ttft_s'] * 1000:.1f}ms" if row["ttft_s"] is not None else "unavailable"
                print(f"{job['precision']} {prompt['context']} trial {row['trial_id']}: {elapsed:.3f}s, "
                      f"TTFT {ttft}, {count} output tokens", flush=True)
            except Exception as error:
                row.update(status="error", error=str(error), generation_s=None, output=None)
            if measure_memory:
                row.update(memory_fields(before_memory, sample_memory(llm, audit, backend=backend)))
            write_json(job["result_path"], rows)  # Preserve previous cells if a later one fails.
    finally:
        shutdown = getattr(llm.llm_engine.engine_core, "shutdown", None)
        if shutdown is not None:
            shutdown()
    return rows


def compare_rows(rows):
    references = {trial_key(r): r for r in rows if r["precision"] == "FP32" and r["status"] == "ok"}
    for row in rows:
        reference = references.get(trial_key(row))
        if row["status"] != "ok" or reference is None:
            continue
        row["speedup_vs_fp32"] = reference["generation_s"] / row["generation_s"]
        row["output_exact_match_fp32"] = row["output"] == reference["output"]
        row["text_similarity_fp32"] = SequenceMatcher(None, reference["output"], row["output"], autojunk=False).ratio()
        row["answer_agreement_fp32"] = (row["json_valid"] and reference["json_valid"]
                                       and row["parsed_answer"] == reference["parsed_answer"])
        row["weight_payload_ratio_vs_fp32"] = (row["weight_payload_bytes"] / reference["weight_payload_bytes"])


def pending_prompts(rows, precision, prompts):
    attempted = {trial_key(r) for r in rows if r["precision"] == precision and r.get("generation_calls", 0) > 0}
    return [p for p in prompts if trial_key(p) not in attempted]


def metric_stats(values):
    values = [value for value in values if value is not None]
    if not values:
        return dict(mean=None, stddev=None, median=None, minimum=None, maximum=None)
    return {"mean": statistics.mean(values), "stddev": statistics.stdev(values) if len(values) > 1 else None,
            "median": statistics.median(values), "minimum": min(values), "maximum": max(values)}


def summarize_rows(rows, precisions, repeats):
    """Average successful timings; count every failed/missing trial explicitly."""
    seen = set()
    for row in rows:
        key = row["precision"], *trial_key(row)
        if key in seen:
            raise ValueError("Duplicate precision/context/trial measurement: " + str(key))
        if not 1 <= row.get("trial_id", 1) <= repeats:
            raise ValueError("Trial ID exceeds requested repeats")
        seen.add(key)
    summaries = []
    for precision in precisions:
        for context in LEVELS:
            trials = [r for r in rows if r["precision"] == precision and r["context"] == context]
            successful = [r for r in trials if r["status"] == "ok"]
            attempted = sum(r.get("generation_calls", 0) > 0 for r in trials)
            n = len(successful)
            item = {"precision": precision, "context": context, "trials_requested": repeats,
                    "trials_attempted": attempted, "trials_successful": n,
                    "trials_failed": sum(r["status"] == "error" for r in trials),
                    "trials_missing": repeats - len(trials),
                    "trials_skipped": sum(r["status"] == "skipped" for r in trials),
                    "status": ("complete" if n == repeats else "partial" if n else "skipped"
                               if trials and all(r["status"] == "skipped" for r in trials) else "error"
                               if any(r["status"] == "error" for r in trials) else "pending"),
                    "input_tokens": next((r.get("input_tokens") for r in trials), None),
                    "weight_payload_bytes": next((r["weight_payload_bytes"] for r in trials if "weight_payload_bytes" in r), None)}
            item["task_id"] = next((r.get("task_id") for r in trials), None)
            item["expected"] = next((r["expected"] for r in trials if "expected" in r), None)
            for name in ("generation_s", "end_to_end_tokens_per_s", "ttft_s", "output_tokens", "field_accuracy", "reasoning_accuracy", "text_similarity_fp32", *MEMORY_METRICS):
                for statistic, value in metric_stats([r.get(name) for r in successful]).items():
                    item[name + "_" + statistic] = value
            for name in MEMORY_METRICS:
                item[name + "_measured_trials"] = sum(r.get(name) is not None for r in successful)
            item["ttft_measured_trials"] = sum(r.get("ttft_s") is not None for r in successful)
            item["ttft_missing_trials"] = n - item["ttft_measured_trials"]
            passed = sum(bool(r.get("all_fields_correct")) for r in successful)
            item["answers_all_fields_correct"] = passed
            item["answer_pass_rate"] = passed / attempted if attempted else None
            item["json_valid_rate"] = sum(bool(r.get("json_valid")) for r in successful) / attempted if attempted else None
            fields = list(dict.fromkeys(key for r in trials for key in r.get("expected", r.get("field_correct", {}))))
            for field in fields:
                values = [r["field_correct"][field] for r in successful if field in r.get("field_correct", {})]
                item[field + "_correct_rate"] = statistics.mean(values) if values else None
            outputs = Counter(r["output"] for r in successful)
            item["unique_outputs"] = len(outputs)
            item["output_consistency_rate"] = max(outputs.values()) / n if n else None
            for name in ("output_exact_match_fp32", "answer_agreement_fp32"):
                values = [r[name] for r in successful if name in r]
                item[name + "_rate"] = statistics.mean(values) if values else None
            item["weighted_end_to_end_tokens_per_s"] = (sum(r["output_tokens"] for r in successful)
                / sum(r["generation_s"] for r in successful)) if n else None
            summaries.append(item)
    references = {s["context"]: s for s in summaries if s["precision"] == "FP32"}
    for item in summaries:
        reference = references.get(item["context"])
        baseline = reference["generation_s_mean"] if reference else None
        item["speedup_vs_fp32_mean"] = baseline / item["generation_s_mean"] if baseline and item["generation_s_mean"] else None
    return summaries


def execute_worker(job_path, log_path, timeout):
    with log_path.open("w") as log:
        process = subprocess.Popen([sys.executable, str(Path(__file__).resolve()), "--worker-job", str(job_path)],
                                   stdout=log, stderr=subprocess.STDOUT, start_new_session=True)
        try:
            return process.wait(timeout=timeout)
        except subprocess.TimeoutExpired:
            # Include the engine subprocess so a timeout cannot leave GPU memory
            # occupied while the next precision starts.
            try:
                os.killpg(process.pid, signal.SIGTERM)
                process.wait(timeout=10)
            except subprocess.TimeoutExpired:
                os.killpg(process.pid, signal.SIGKILL)
                process.wait()
            except ProcessLookupError:
                pass
            raise


def report(output_dir, hardware, settings, prompts, rows):
    rows.sort(key=lambda r: (list(SPECS).index(r["precision"]), LEVELS.index(r["context"]), r.get("trial_id", 1)))
    repeats = settings["measured_generations_per_cell"]
    warnings = []
    for precision in settings["precisions"]:
        log_path = output_dir / (precision + ".log")
        if log_path.exists():
            log_text = log_path.read_text(errors="replace")
            shutdown = log_text.find("Metal worker shutdown complete")
            crash = log_text.find("Segfault encountered", shutdown) if shutdown >= 0 else -1
            if crash >= 0:
                warning = "Engine logged a segmentation fault during shutdown after worker cleanup; see " + precision + ".log"
                warnings.append(precision)
                for row in rows:
                    if row["precision"] == precision:
                        row["engine_teardown_warning"] = warning
    compare_rows(rows)
    summaries = summarize_rows(rows, settings["precisions"], repeats)
    write_json(output_dir / "results.json", {"created_utc": datetime.now(timezone.utc).isoformat(),
               "hardware": hardware, "settings": settings,
               "expected_answers": {p["context"]: p.get("expected") for p in prompts},
               "prompts": prompts, "summary": summaries, "results": rows})
    write_json(output_dir / "summary.json", summaries)
    columns = ["precision", "backend", "context", "task_id", "task_mode", "comparison", "reasoning_fields", "trial_id", "status", "input_tokens", "output_tokens", "generation_calls",
               *MEMORY_METRICS, "engine_rss_high_water_bytes", "memory_before", "memory_after", "experiment_contract",
               "generation_s", "end_to_end_tokens_per_s", "ttft_s", "ttft_source", "ttft_unavailable_reason", "engine_load_s",
               "prepare_s", "weight_payload_bytes", "weight_payload_scope", "runtime_audit", "driver_peak_rss_bytes", "field_accuracy",
               "all_fields_correct", "reasoning_accuracy", "expected", "parsed_answer", "field_correct", "schema_valid",
               "speedup_vs_fp32", "output_exact_match_fp32",
               "text_similarity_fp32", "answer_agreement_fp32", "finish_reason", "description", "error", "engine_teardown_warning", "output"]
    with (output_dir / "results.csv").open("w", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=columns, extrasaction="ignore")
        writer.writeheader()
        writer.writerows({key: json.dumps(value, ensure_ascii=False) if isinstance(value, (dict, list)) else value
                         for key, value in row.items()} for row in rows)
    with (output_dir / "summary.csv").open("w", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(dict.fromkeys(key for item in summaries for key in item)))
        writer.writeheader()
        writer.writerows({key: json.dumps(value, ensure_ascii=False) if isinstance(value, (dict, list)) else value
                         for key, value in item.items()} for item in summaries)
    def number(value, places=3):
        return f"{value:.{places}f}" if value is not None else "—"
    lines = ["# vLLM precision comparison: repeated-run averages", "", f"Model: `{settings['model']}`; source: `{settings.get('source_revision', 'not loaded')}`.",
             "Hardware: " + hardware_description(hardware) + ".", "",
             f"{repeats} measured generations per precision/context ({len(settings['precisions']) * len(LEVELS) * repeats} requested in total). Batch size 1; temperature 0; seed 42; prefix caching disabled.",
             "Each round rotates context order; all precisions use the same schedule and the same token IDs. The model is loaded once per precision.",
             "Means include the first measured request. No extra benchmark warm-up is added. Engine initialization/profile/warm-up passes are outside generation timing.",
             "These are repeated measurements of fixed prompts, not cross-validation folds or independent accuracy examples. Greedy outputs may be identical across repeats.",
             "Elapsed time includes prompt prefill, decoding, and API overhead; tokens/s is end-to-end output throughput.",
             f"Output limit: {settings['max_new_tokens']} tokens. {sum(r.get('finish_reason') == 'length' for r in rows)} returned responses reached the limit; truncated answers are retained and graded as returned.",
             "Model download, conversion, and engine loading are timed separately. First requests can include lazy kernel initialization.",
             ("CUDA FP8 uses per-channel E4M3 weights and the weight-only Marlin kernel; INT4 uses symmetric groups of 128. "
              "Both use BF16 projection inputs. Quantization recipes differ from Metal; compare results within one backend."
              if hardware.get("backend") == "cuda" else
              "Metal FP8 uses MXFP8 E4M3 weights with BF16 inputs; INT4 uses affine weights. This measures local Metal inference."),
             "FP8_A8 applies activation quantize/dequantize rounding with BF16 buffers. Some tensors and reductions retain higher precision.",
             "Weight size is the saved tensor payload, including scales and unquantized tensors; it is not total runtime memory.",
             ("CUDA dense variants load and cast the original source directory; their payload size describes the source checkpoint. "
              "Loaded parameter bytes and dtypes are saved in runtime_audit; FP8/INT4 sizes describe prepared CUDA files."
              if hardware.get("backend") == "cuda" else "Prepared Metal files are audited against their requested storage format."),
             "RSS is the cumulative driver-process high-water mark, not the complete engine/GPU memory usage.", "",
             "| Precision | Context | Status | Completed / requested | Input tokens | Mean seconds ± SD | Mean TTFT ms ± SD | TTFT measured / completed | Mean tokens/s | Weight MiB | Mean correct fields | Answer pass rate | Speedup vs FP32 |",
             "|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|"]
    for item in summaries:
        size = item["weight_payload_bytes"]
        accuracy = item["field_accuracy_mean"]
        pass_rate = item["answer_pass_rate"]
        accuracy_text = number(accuracy * 100, 1) + "%" if accuracy is not None else "—"
        pass_text = number(pass_rate * 100, 1) + "%" if pass_rate is not None else "—"
        timing = number(item["generation_s_mean"]) + " ± " + number(item["generation_s_stddev"])
        ttft, ttft_coverage = ttft_cells(item)
        lines.append(f"| {item['precision']} | {item['context']} | {item['status']} | {item['trials_successful']} / {repeats} | {item['input_tokens'] or '—'} | "
                     f"{timing} | {ttft} | {ttft_coverage} | {number(item['end_to_end_tokens_per_s_mean'], 1)} | "
                     f"{number(size / MIB if size is not None else None, 1)} | {accuracy_text} | {pass_text} | "
                     f"{number(item['speedup_vs_fp32_mean'], 2)} |")
    if warnings:
        lines += ["", "Observed runtime limitation: the installed vLLM/Metal stack logged a segmentation fault during engine shutdown for "
                  + ", ".join(warnings) + ". Completed generation results were saved before shutdown. See the corresponding engine logs; a clean teardown is not verified."]
    if "FP8_A8" in settings["precisions"]:
        lines += ["", *write_comparison(output_dir, summaries, rows, settings.get("backend", "metal"))]
    lines += ["", "## Tasks and reference answers", "",
              "Each context reads its Markdown prompt and JSON expectation file. Generated tasks add complete records to fit their budgets and calculate references from those records. "
              "Static tasks use the Markdown literally with the configured expected answer; their actual token counts may be below the budgets. "
              "Context length and reasoning difficulty change together, so differences across contexts do not isolate length alone. "
              "Each precision receives the same token IDs, reference answer, and comparison rules at a given context.", ""]
    for prompt in prompts:
        lines += [f"- **{prompt['context']}**: {prompt.get('task_description', 'Task not tokenized in this plan')} "
                  f"Records: {prompt.get('record_count', 'pending')}; input tokens: {prompt.get('input_tokens') or 'pending'}. "
                  f"Reference: `{json.dumps(prompt.get('expected'), ensure_ascii=False)}`. "
                  f"Comparison: `{json.dumps(prompt.get('comparison', {}), ensure_ascii=False)}`."]
    prompt_link = ("[Read the complete prompts](prompts.md); `prompts.json` also contains task data, token IDs and hashes."
                   if any("prompt" in p for p in prompts) else "Prompts and reference answers are generated when a real run begins.")
    lines += ["", prompt_link, "",
              "Accuracy checks the configured JSON fields and their types. Expected fields must always be present; extra keys and string case follow each task's comparison options. Text similarity measures agreement with FP32, not correctness.",
              "SD is the sample standard deviation across successful requests (undefined for fewer than two). Failed/planned trials never contribute zero timings to the mean.",
              "TTFT (time to first token) measures engine request arrival to the first generated token reaching the engine frontend; "
              "it includes queueing and input prefill, and excludes model setup and subsequent decoding. This local measurement excludes HTTP/network transport. "
              "Tables show milliseconds; JSON/CSV fields use seconds. TTFT coverage counts measured versus completed requests. "
              "Only available, valid engine metrics enter TTFT averages; unavailable historical metrics are never reconstructed from total latency.",
              "Mean field accuracy uses successful requests. Answer pass rate uses every generation attempt as its denominator, with generation errors counted as failures.",
              "Summary files retain each task's per-field correctness and the mean accuracy of its reasoning fields among successful requests. Invalid JSON scores false for all fields; valid JSON fences are accepted.",
              "Mean tokens/s is the arithmetic mean of individual trial rates. Summary files also include weighted tokens/s, median, minimum, maximum, and trial counts.",
              "Speedup is the FP32 mean latency divided by the comparison mean for the same context; raw output comparisons pair the same trial ID.",
              "Repeated timing measures runtime variation. These three fixed tasks do not establish overall model quality.", ""]
    for level in LEVELS:
        lines += ["## " + level + " answers", ""]
        for precision in settings["precisions"]:
            trials = [r for r in rows if r["context"] == level and r["precision"] == precision]
            if not trials:
                continue
            lines += ["### " + precision, ""]
            grouped = {}
            for row in trials:
                text = row.get("output") if row["status"] == "ok" else row.get("error", "No generation")
                grouped.setdefault(text, []).append(str(row.get("trial_id", 1)))
            for text, trial_ids in grouped.items():
                lines += ["Trials " + ", ".join(trial_ids) + ":", "", "```text", text or "(empty output)", "```", ""]
    (output_dir / "comparison.md").write_text("\n".join(lines))
    table_start = next(i for i, line in enumerate(lines) if line.startswith("| Precision"))
    print("\n" + "\n".join(lines[table_start:table_start + len(summaries) + 2]))
    print("\nReport: " + str(output_dir / "comparison.md"))


def parse_args(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    add_backend_arguments(parser)
    parser.add_argument("--config", type=Path, default=DEFAULT_CONFIG, help="Model configuration JSON (default: config.json beside this script)")
    selection = parser.add_mutually_exclusive_group()
    selection.add_argument("--model", help="Explicit model ID or local directory; overrides config")
    selection.add_argument("--tier", choices=MODEL_TIERS, default="lightweight", help="Model tier from config (default: lightweight)")
    parser.add_argument("--revision", help="Optional Hugging Face commit/tag; resolved commit is recorded")
    add_precision_arguments(parser)
    parser.add_argument("--context-tokens", type=int, nargs=3, default=[256, 1024, 4096], metavar=("SHORT", "MEDIUM", "LONG"))
    parser.add_argument("--max-new-tokens", type=int, default=96)
    parser.add_argument("--repeats", type=int, default=10, help="Measured generations per precision/context (default: 10)")
    add_memory_arguments(parser)
    parser.add_argument("--thinking", choices=["auto", "on", "off"], default="auto",
                        help="Auto disables thinking for Qwen3 to compare concise final answers")
    parser.add_argument("--model-dir", type=Path, default=ROOT / "models")
    parser.add_argument("--output-dir", type=Path)
    parser.add_argument("--timeout", type=int, default=600, help="Maximum engine + generation seconds per precision")
    parser.add_argument("--hardware", action="store_true", help="Show hardware/dependencies without downloading models")
    parser.add_argument("--dry-run", action="store_true", help="Write a plan; no downloads or inference")
    parser.add_argument("--resume", action="store_true", help="Run only unattempted trials in an existing --output-dir")
    parser.add_argument("--worker-job", type=Path, help=argparse.SUPPRESS)
    args = parser.parse_args(argv)
    if args.activation_comparison:
        args.precisions = list(ACTIVATION_PRECISIONS)
    if args.model is None:
        try:
            args.model = load_models(args.config)[MODEL_TIERS.index(args.tier)]
        except (OSError, ValueError) as error:
            parser.error(str(error))
    validate_memory_arguments(args, parser)
    if args.max_new_tokens <= 0 or args.timeout <= 0 or args.repeats <= 0:
        parser.error("Token limit, timeout, and repeats must be positive")
    if not 0 < args.context_tokens[0] < args.context_tokens[1] < args.context_tokens[2]:
        parser.error("Short, Medium, Long token budgets must be positive and strictly increasing")
    if len(set(args.precisions)) != len(args.precisions):
        parser.error("Specify each precision once")
    if args.resume and (args.output_dir is None or args.dry_run or args.hardware):
        parser.error("--resume requires --output-dir and a real benchmark run")
    return args


def main():
    args = parse_args()
    local_environment()
    if args.worker_job:
        job = json.loads(args.worker_job.read_text())
        try:
            run_worker(job)
        except Exception as error:
            previous = json.loads(Path(job["result_path"]).read_text()) if Path(job["result_path"]).exists() else []
            finished = {trial_key(row) for row in previous}
            previous.extend(blank_rows(job["precision"], [p for p in job["prompts"] if trial_key(p) not in finished], "error", str(error), job.get("backend", "metal")))
            write_json(job["result_path"], previous)
            raise
        return 0
    hardware = hardware_info(args.backend)
    backend = hardware["backend"]
    if args.hardware:
        print(json.dumps(hardware, indent=2))
        return 0
    # Validate editable tasks before resolving or downloading any model.
    preview_tasks = {level: TASK_BUILDERS[level](0) for level in LEVELS}
    output_dir = (args.output_dir or ROOT / "results" / datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")).resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    settings = {"model": args.model, "backend": backend,
                "cuda_visible_devices": hardware.get("cuda_visible_devices"),
                "gpu_uuid": hardware.get("gpu_uuid"),
                "precisions": args.precisions, "context_token_budgets": args.context_tokens,
                "max_new_tokens": args.max_new_tokens, "memory_fraction": args.memory_fraction,
                "memory_budget_gib": args.memory_budget_gib,
                "measured_generations_per_cell": args.repeats, "benchmark_warmup_generations": 0,
                "seed": 42, "temperature": 0.0, "prefix_caching": False,
                "prompt_suite": PROMPT_SUITE, "task_suite_sha256": task_suite_sha256(),
                "scoring_policy": SCORING_POLICY, "timing_policy": TIMING_POLICY,
                "thinking_policy": args.thinking, "cache_policy": CACHE_POLICIES[backend]}
    settings.update(activation_settings(args.precisions, backend))
    previous = None
    if args.resume:
        previous = json.loads((output_dir / "results.json").read_text())
        if any(previous["settings"].get(key, "auto" if key == "thinking_policy" else "metal" if key == "backend" else None) != value
               for key, value in settings.items() if key != "cache_policy"):
            raise ValueError("Resume settings must match the original run")
        if previous["settings"].get("cache_policy") != settings["cache_policy"]:
            if any(row.get("generation_calls", 0) for row in previous["results"]):
                raise ValueError("Cache policy changed; preserve this run and use a new output directory for comparable measurements")
        if previous["hardware"]["packages"] != hardware["packages"]:
            raise ValueError("Resume requires the same package versions")
    elif any((output_dir / name).exists() for name in ("results.json", "prompts.json")):
        raise ValueError("Output directory already contains a run; use a new directory or --resume")
    if args.dry_run:
        prompts = [{"context": level, "input_tokens": None, "target_tokens": budget,
                    "prompt_suite": PROMPT_SUITE, "task_id": preview_tasks[level]["task_id"],
                    "task_mode": preview_tasks[level]["task_mode"], "comparison": preview_tasks[level]["comparison"],
                    "reasoning_fields": preview_tasks[level]["reasoning_fields"],
                    "task_description": preview_tasks[level]["task_description"]}
                   for level, budget in zip(LEVELS, args.context_tokens)]
        rows = [row for precision in args.precisions for row in blank_rows(
            precision, make_trials([{**p, "prompt_sha256": None} for p in prompts], args.repeats), "planned", "Dry run; no compute performed", backend)]
        report(output_dir, hardware, settings, prompts, rows)
        return 0
    if not hardware["compatible_os"]:
        raise RuntimeError("CUDA requires Linux; Metal requires native arm64 macOS 15+")
    missing = [name for name, version in hardware["packages"].items() if version is None]
    if missing:
        install = "pip install -r requirements-cuda.txt" if backend == "cuda" else "python3.13 setup_metal.py"
        raise RuntimeError("Missing packages: " + ", ".join(missing) + ". Run " + install)
    if backend == "cuda":
        if not hardware.get("cuda_available"):
            raise RuntimeError("NVIDIA CUDA is unavailable; check the driver, CUDA PyTorch and CUDA_VISIBLE_DEVICES")
        if hardware.get("gpu_compute_capability", [0])[0] < 8:
            raise RuntimeError("This BF16/CUDA comparison requires compute capability 8.0+ (Ampere or newer)")
    if "memory_bytes" not in hardware:
        raise RuntimeError("Cannot read physical memory; allow hardware access before running the benchmark")
    started = time.perf_counter()
    source, revision = resolve_source(args.model, previous["settings"].get("source_revision") if previous else args.revision)
    settings.update(source_revision=revision, source_resolution_s=time.perf_counter() - started)
    from transformers import AutoTokenizer
    tokenizer = AutoTokenizer.from_pretrained(str(source), trust_remote_code=False)
    source_config = json.loads((source / "config.json").read_text())
    enable_thinking = (False if source_config.get("model_type") == "qwen3" else None) if args.thinking == "auto" else args.thinking == "on"
    settings["enable_thinking"] = enable_thinking
    prompts = make_prompts(tokenizer, args.context_tokens, enable_thinking)
    trials = make_trials(prompts, args.repeats)
    settings["trial_schedule"] = [{"trial_id": p["trial_id"], "context": p["context"]} for p in trials]
    if previous:
        validate_resume_tasks(previous["prompts"], prompts)
    write_json(output_dir / "prompts.json", prompts)
    prompt_lines = ["# Complete benchmark prompts", "", "Suite: " + PROMPT_SUITE,
                    "", "System message: " + SYSTEM, ""]
    for prompt in prompts:
        prompt_lines += ["## " + prompt["context"], "", prompt["task_description"], "",
                         f"Input tokens including chat template: {prompt['input_tokens']}. Unique records: {prompt['record_count']}.",
                         "", "Reference answer: `" + json.dumps(prompt["expected"], ensure_ascii=False) + "`.",
                         "", "Comparison rules: `" + json.dumps(prompt["comparison"], ensure_ascii=False) + "`.",
                         "", "```text", prompt["prompt"], "```", ""]
    (output_dir / "prompts.md").write_text("\n".join(prompt_lines))
    source_stats = safetensors_info(source)
    settings["source_weight_stats"] = source_stats
    excluded = ("lm_head.weight",) if source_config.get("model_type") == "qwen3" and source_config.get("tie_word_embeddings") else ()
    settings["model_parameter_count"] = safetensors_info(source, excluded)["stored_elements"]
    if backend == "metal" and source_config.get("model_type") != "qwen3" and source_stats["weight_payload_bytes"] * 4 > laptop_memory_budget(
            hardware, args.memory_fraction, args.memory_budget_gib)["effective_bytes"]:
        raise RuntimeError("Base checkpoint is too large for the conservative conversion budget; choose a smaller model or raise the memory budget")
    if backend == "cuda":
        if source_config.get("quantization_config") or source_config.get("quantization"):
            raise ValueError("Use an unquantized source model for comparable CUDA variants")
        if any(source_config.get(key, 0) for key in ("num_local_experts", "num_experts")) or source_config.get("text_config"):
            raise ValueError("CUDA comparison currently supports dense text models; MoE/multimodal recipes require separate experiments")
    max_model_len = max(p["input_tokens"] for p in prompts) + args.max_new_tokens
    settings["memory_plans"] = {precision: memory_plan(source_config, settings["model_parameter_count"], precision,
                                                      max_model_len, hardware, args.memory_fraction, args.memory_budget_gib)
                                for precision in args.precisions}
    rows = previous["results"] if previous else []
    if previous:
        settings["source_resolution_s"] += previous["settings"].get("source_resolution_s", 0)
        settings["resumed_from_unmeasured_cells"] = True
    for precision in args.precisions:
        pending = pending_prompts(rows, precision, trials)
        if not pending:
            print("Preserving completed generation attempts for " + precision, flush=True)
            continue
        # Remove only zero-attempt rows. Successful or attempted measurements are
        # retained; resuming never generates another answer for those cells.
        pending_keys = {trial_key(p) for p in pending}
        rows = [r for r in rows if not (r["precision"] == precision and trial_key(r) in pending_keys)]
        plan = settings["memory_plans"][precision]
        if not plan["fits"]:
            print("Skipping " + precision + ": " + plan["reason"], flush=True)
            rows.extend(blank_rows(precision, pending, "skipped", plan["reason"], backend))
            report(output_dir, hardware, settings, prompts, rows)
            continue
        started = time.perf_counter()
        result_path = output_dir / (precision + "_worker_results.json")
        try:
            print("\nPreparing " + precision + ": " + precision_description(precision, backend), flush=True)
            if backend == "cuda":
                import cuda_backend
                checkpoint, stats, cached = cuda_backend.prepare_checkpoint(source, revision, args.model, precision,
                    args.model_dir, safetensors_info, write_json)
            else:
                checkpoint, stats, cached = prepare_checkpoint(source, revision, args.model, precision, args.model_dir)
            preparation = {"prepare_s": time.perf_counter() - started, "checkpoint_cached": cached,
                           "weight_payload_bytes": stats["weight_payload_bytes"],
                           "checkpoint_elements_by_dtype": stats["elements_by_dtype"],
                           "weight_payload_scope": stats.get("weight_payload_scope", "Prepared checkpoint tensor payload")}
            # Conversion tensors must be released before the engine starts.
            import gc
            gc.collect()
            if backend == "metal":
                import mlx.core as mx
                mx.clear_cache()
            job = {"backend": backend, "precision": precision, "checkpoint": str(checkpoint), "source": str(source),
                   "max_model_len": max_model_len, "kv_cache_bytes": plan["kv_cache_bytes"],
                   "max_new_tokens": args.max_new_tokens, "memory_fraction": plan["backend_memory_fraction"],
                   "cache_block_size": plan["cache_block_size"], "num_gpu_blocks": plan["num_gpu_blocks"],
                   "timing_policy": TIMING_POLICY,
                   "prompts": pending, "preparation": preparation, "result_path": str(result_path)}
            if "FP8_A8" in args.precisions:
                job.update(memory_policy=settings["memory_policy"])
                # Only the paired FP8 cases pin BF16 cache storage. Metal's
                # FP32 engine requires a cache matching its FP32 model dtype.
                if precision in ACTIVATION_PRECISIONS:
                    job.update(kv_cache_dtype="bfloat16")
                    job["experiment_contract"] = {"checkpoint": str(checkpoint.resolve()), "source_revision": revision,
                        "dtype": SPECS[precision]["dtype"], "kv_cache_dtype": job["kv_cache_dtype"],
                        "kv_cache_bytes": job["kv_cache_bytes"], "cache_block_size": job["cache_block_size"],
                        "num_gpu_blocks": job["num_gpu_blocks"], "max_model_len": job["max_model_len"],
                        "max_new_tokens": job["max_new_tokens"], "memory_fraction": job["memory_fraction"],
                        "memory_policy": settings["memory_policy"], "timing_policy": TIMING_POLICY, "seed": 42, "temperature": 0.0}
            job_path = output_dir / (precision + "_job.json")
            write_json(job_path, job)
            # Preserve prior failed initialization evidence when resuming.
            if previous:
                for existing in (result_path, output_dir / (precision + ".log")):
                    if existing.exists():
                        archive = existing.with_name(existing.name + ".before-resume-" + datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ"))
                        existing.rename(archive)
            returncode = execute_worker(job_path, output_dir / (precision + ".log"), args.timeout)
            if result_path.exists():
                mode_rows = json.loads(result_path.read_text())
            else:
                mode_rows = blank_rows(precision, pending, "error", f"Worker exited {returncode}; see {precision}.log", backend)
            rows.extend(mode_rows)
        except subprocess.TimeoutExpired:
            rows.extend(json.loads(result_path.read_text()) if result_path.exists() else [])
            finished = {trial_key(r) for r in rows if r["precision"] == precision}
            rows.extend(blank_rows(precision, [p for p in pending if trial_key(p) not in finished], "error", "Worker timed out", backend))
        except Exception as error:
            rows.extend(blank_rows(precision, pending, "error", str(error), backend))
        for row in rows:
            if row["status"] == "running":
                row.update(status="error", error="Worker stopped before this attempted trial returned a result",
                           generation_s=None, output=None)
        report(output_dir, hardware, settings, prompts, rows)
    if previous:
        report(output_dir, hardware, settings, prompts, rows)
    return 0 if all(row["status"] in ("ok", "skipped") for row in rows) else 1


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (OSError, RuntimeError, ValueError) as error:
        print("Error: " + str(error), file=sys.stderr)
        sys.exit(2)
