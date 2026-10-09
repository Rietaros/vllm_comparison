"""Fixed-weight MXFP8 activation rounding and engine memory measurements."""
from __future__ import annotations

import csv
import json
import os
import platform
import resource

ACTIVATION_PRECISIONS = ("FP8", "FP8_A8")
ACTIVATION_POLICY = "mxfp8-linear-input-qdq-v1"
MEMORY_POLICY = "engine-per-request-mlx-peak-rss-v1"
MEMORY_METRICS = ("mlx_active_bytes_before", "mlx_active_bytes_after", "mlx_peak_bytes",
                  "mlx_peak_extra_bytes", "mlx_cache_bytes_after", "engine_rss_bytes_after",
                  "cuda_allocated_bytes_before", "cuda_allocated_bytes_after", "cuda_reserved_bytes_after",
                  "cuda_peak_allocated_bytes", "cuda_peak_extra_bytes", "cuda_peak_reserved_bytes",
                  "cuda_device_used_bytes_after")
CONTRACT_FIELDS = ("checkpoint", "source_revision", "dtype", "kv_cache_dtype", "kv_cache_bytes",
                   "cache_block_size", "num_gpu_blocks", "max_model_len", "max_new_tokens",
                   "memory_fraction", "memory_policy", "timing_policy", "seed", "temperature")


def round_fp8_activations(model):
    """Engine RPC: replace projections while sharing their exact weight arrays."""
    import mlx.core as mx
    import mlx.nn as nn
    from mlx.utils import tree_unflatten

    if not hasattr(mx, "qqmm"):
        raise RuntimeError("FP8 activation rounding requires MLX with mx.qqmm (validated on 0.32.1)")

    class RoundedLinear(nn.QuantizedLinear):
        activation_quantization = ACTIVATION_POLICY

        def __init__(self, original):
            # Avoid allocating or requantizing weights in the layer constructor.
            nn.Module.__init__(self)
            self.group_size, self.bits, self.mode = original.group_size, original.bits, original.mode
            self.weight, self.scales = original.weight, original.scales
            self.biases = None
            if "bias" in original:
                self.bias = original.bias
            self.freeze()
            self.train(original.training)

        def __call__(self, x):
            result = mx.qqmm(x, self.weight, scales=self.scales, group_size=self.group_size,
                             bits=self.bits, mode=self.mode)
            return result + self.bias if "bias" in self else result

    class RoundedEmbedding(nn.QuantizedEmbedding):
        activation_quantization = ACTIVATION_POLICY

        def __init__(self, original):
            nn.Module.__init__(self)
            self.group_size, self.bits, self.mode = original.group_size, original.bits, original.mode
            self.weight, self.scales = original.weight, original.scales
            self.biases = None
            self.num_embeddings, self.dims = original.num_embeddings, original.dims
            self.freeze()
            self.train(original.training)

        def as_linear(self, x):
            # Integer token lookups retain the inherited embedding implementation.
            # Only the tied output projection receives activation rounding.
            return mx.qqmm(x, self.weight, scales=self.scales, group_size=self.group_size,
                           bits=self.bits, mode=self.mode)

    replacements = []
    for name, module in model.named_modules():
        if getattr(module, "bits", None) is None or getattr(module, "mode", None) is None:
            continue
        if module.mode != "mxfp8" or module.bits != 8 or module.group_size != 32:
            raise ValueError("Activation experiment requires fixed MXFP8/32 weights: " + name)
        if type(module) not in (nn.QuantizedLinear, nn.QuantizedEmbedding):
            raise ValueError("Unsupported quantized projection in activation experiment: " + name)
        if not name:
            raise ValueError("Activation experiment requires a model containing named projections")
        replacement = RoundedLinear(module) if type(module) is nn.QuantizedLinear else RoundedEmbedding(module)
        replacements.append((name, replacement))
    if not replacements:
        raise ValueError("No MXFP8 projections found for activation rounding")
    # Validate every module before changing the model. Packed weights and scales
    # are shared by object identity; embeddings, attention and KV buffers stay BF16.
    model.update_modules(tree_unflatten(replacements))
    return {"policy": ACTIVATION_POLICY, "projections": [name for name, _ in replacements]}


def engine_memory(model, reset_peak=False):
    """Engine RPC: synchronized MLX counters and process RSS, outside timing."""
    import mlx.core as mx
    mx.synchronize()
    if reset_peak:
        mx.reset_peak_memory()
    snapshot = {"pid": os.getpid(), "mlx_active_bytes": mx.get_active_memory(),
                "mlx_peak_bytes": mx.get_peak_memory(), "mlx_cache_bytes": mx.get_cache_memory(),
                "rss_high_water_bytes": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
                * (1 if platform.system() == "Darwin" else 1024)}
    try:
        import psutil
        snapshot["rss_bytes"] = psutil.Process().memory_info().rss
    except ImportError:
        snapshot["rss_bytes"] = None
        snapshot["rss_unavailable_reason"] = "psutil is not installed in the engine environment"
    return snapshot


def begin_request_memory(model):
    return engine_memory(model, reset_peak=True)


def sample_memory(llm, audit, before=False, backend="metal"):
    try:
        if backend == "cuda":
            from cuda_backend import begin_request_memory as begin, engine_memory as end
        else:
            begin, end = begin_request_memory, engine_memory
        snapshots = llm.apply_model(begin if before else end)
        if len(snapshots) != 1 or snapshots[0].get("pid") != audit.get("engine_pid"):
            raise ValueError("Memory snapshot must come from the audited engine process")
        return snapshots[0]
    except Exception as error:
        return {"unavailable_reason": str(error)}


def memory_fields(before, after):
    valid_peak = "mlx_peak_bytes" in after and "mlx_active_bytes" in before
    valid_cuda_peak = "cuda_peak_allocated_bytes" in after and "cuda_allocated_bytes" in before
    return {"memory_before": before, "memory_after": after,
            "mlx_active_bytes_before": before.get("mlx_active_bytes"),
            "mlx_active_bytes_after": after.get("mlx_active_bytes"),
            "mlx_peak_bytes": after["mlx_peak_bytes"] if valid_peak else None,
            "mlx_peak_extra_bytes": max(0, after["mlx_peak_bytes"] - before["mlx_active_bytes"]) if valid_peak else None,
            "mlx_cache_bytes_after": after.get("mlx_cache_bytes"),
            "cuda_allocated_bytes_before": before.get("cuda_allocated_bytes"),
            "cuda_allocated_bytes_after": after.get("cuda_allocated_bytes"),
            "cuda_reserved_bytes_after": after.get("cuda_reserved_bytes"),
            "cuda_peak_allocated_bytes": after["cuda_peak_allocated_bytes"] if valid_cuda_peak else None,
            "cuda_peak_extra_bytes": max(0, after["cuda_peak_allocated_bytes"] - before["cuda_allocated_bytes"]) if valid_cuda_peak else None,
            "cuda_peak_reserved_bytes": after.get("cuda_peak_reserved_bytes") if valid_cuda_peak else None,
            "cuda_device_used_bytes_after": after.get("cuda_device_used_bytes"),
            "engine_rss_bytes_after": after.get("rss_bytes"),
            "engine_rss_high_water_bytes": after.get("rss_high_water_bytes")}


def comparison_rows(summaries, trials, backend="metal"):
    """Keep each model/context separate and validate actual paired attempts."""
    groups = {}
    for item in summaries:
        if item["precision"] in ACTIVATION_PRECISIONS:
            key = item.get("tier"), item.get("model"), item["context"]
            groups.setdefault(key, {})[item["precision"]] = item
    comparisons = []
    for (tier, model, context), cells in groups.items():
        baseline, rounded = cells.get("FP8"), cells.get("FP8_A8")
        if rounded is None:
            continue
        matched = {precision: {row.get("trial_id", 1): row for row in trials
                   if row["precision"] == precision and row["context"] == context
                   and row.get("tier") == tier and row.get("model") == model
                   and row.get("generation_calls", 0) > 0} for precision in ACTIVATION_PRECISIONS}
        verified = 0
        for trial_id in matched["FP8"].keys() & matched["FP8_A8"].keys():
            a, b = matched["FP8"][trial_id], matched["FP8_A8"][trial_id]
            contract = a.get("experiment_contract")
            required = set(CONTRACT_FIELDS)
            if a.get("backend") == "cuda":
                required |= {"backend", "weight_policy", "weight_sha256"}
            if not isinstance(contract, dict) or set(contract) != required:
                raise ValueError("Activation comparison requires a complete checkpoint/cache/settings contract")
            for field in ("experiment_contract", "prompt_sha256", "input_tokens", "expected"):
                if a.get(field) is None or a.get(field) != b.get(field):
                    raise ValueError(f"Activation comparison mismatch: {model or tier or ''}/{context}/{trial_id}: {field}")
            verified += 1
        item = {"tier": tier, "model": model, "context": context, "verified_trial_pairs": verified,
                "bf16_completed": baseline["trials_successful"] if baseline else 0,
                "fp8_rounded_completed": rounded["trials_successful"],
                "trials_requested_per_case": rounded["trials_requested"]}
        backends = {row.get("backend", "metal") for row in trials if row["precision"] in ACTIVATION_PRECISIONS
                    and row["context"] == context and row.get("tier") == tier and row.get("model") == model}
        if len(backends) > 1:
            raise ValueError("Activation cases must use the same backend")
        item["backend"] = next(iter(backends), backend)
        successful_ids = {p: {i for i, row in matched[p].items() if row["status"] == "ok"}
                          for p in ACTIVATION_PRECISIONS}
        item["successful_trial_pairs"] = len(successful_ids["FP8"] & successful_ids["FP8_A8"])
        for prefix, cell in (("bf16", baseline), ("fp8_rounded", rounded)):
            for metric in ("generation_s_mean", "generation_s_stddev", "ttft_s_mean", "ttft_s_stddev",
                           "ttft_measured_trials", "field_accuracy_mean", "reasoning_accuracy_mean", "answer_pass_rate",
                           "mlx_peak_bytes_mean", "mlx_peak_bytes_maximum", "mlx_peak_extra_bytes_mean",
                           "engine_rss_bytes_after_mean", "mlx_peak_bytes_measured_trials", "engine_rss_bytes_after_measured_trials",
                           "cuda_peak_allocated_bytes_mean", "cuda_peak_allocated_bytes_maximum", "cuda_peak_extra_bytes_mean",
                           "cuda_peak_allocated_bytes_measured_trials", "cuda_peak_reserved_bytes_mean",
                           "cuda_reserved_bytes_after_mean", "cuda_device_used_bytes_after_mean"):
                item[prefix + "_" + metric] = cell.get(metric) if cell else None
        a, b = item["bf16_generation_s_mean"], item["fp8_rounded_generation_s_mean"]
        # Do not compare independently populated aggregates without a verified pair.
        item["speedup_vs_bf16_activations"] = (a / b if verified and a and b
            and successful_ids["FP8"] == successful_ids["FP8_A8"] else None)
        comparisons.append(item)
    return comparisons


def write_comparison(output_dir, summaries, trials, backend="metal"):
    """Write a dedicated comparison with honest coverage and memory scope."""
    comparisons = comparison_rows(summaries, trials, backend)
    if not comparisons:
        return []
    if backend == "cuda":
        from cuda_backend import ACTIVATION_POLICY as policy, MEMORY_POLICY as memory_policy
        peak, allocator = "cuda_peak_allocated_bytes", "CUDA allocated"
        rounding = "FP8_A8 rounds quantized projection inputs per token to FP8 E4M3, then returns BF16 buffers. The unquantized output head retains BF16 inputs."
    else:
        policy, memory_policy, peak, allocator = ACTIVATION_POLICY, MEMORY_POLICY, "mlx_peak_bytes", "MLX"
        rounding = "FP8_A8 rounds quantized projection inputs to MXFP8 with mx.qqmm, then computes with BF16 buffers. A quantized tied output head also receives rounding."
    if any(item["backend"] != backend for item in comparisons):
        raise ValueError("Activation report backend does not match its trials")
    (output_dir / "activation_comparison.json").write_text(json.dumps({"backend": backend, "activation_policy": policy,
        "memory_policy": memory_policy, "comparison": comparisons}, indent=2, allow_nan=False) + "\n")
    with (output_dir / "activation_comparison.csv").open("w", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(comparisons[0]))
        writer.writeheader()
        writer.writerows(comparisons)
    def number(value, scale=1):
        return f"{value / scale:.3f}" if value is not None else "—"
    def percent(value):
        return number(value, .01) + "%" if value is not None else "—"
    lines = ["## Fixed FP8 weights: activation comparison", "",
        "FP8 uses BF16 activations. " + rounding + " "
        "This is a quantize/dequantize experiment, not native FP8 arithmetic or persistent FP8 activation storage. "
        "Embedding lookups, attention and the KV cache retain BF16 behavior.", "",
        "Both cases reuse one FP8 checkpoint, the same prompt token IDs, BF16 KV dtype, cache block size/count, generation settings and rotating trial schedule. "
        "Verified pairs check checkpoint/cache/settings identity, prompt hashes, token counts and reference answers. "
        "Sequential engine runs can still differ due to system load and compilation; means include first-request work.", "",
        f"| Model/tier | Context | Case | Completed | Verified pairs | Mean latency s | Mean TTFT ms | TTFT coverage | Mean field accuracy | Answer pass | Mean {allocator} peak MiB | Peak coverage | Mean engine RSS after MiB | RSS coverage |",
        "|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|"]
    for item in comparisons:
        for prefix, label in (("bf16", "FP8 / BF16 activations"), ("fp8_rounded", "FP8_A8 / FP8-rounded activations")):
            completed = item[prefix + "_completed"]
            field = item[prefix + "_field_accuracy_mean"]
            passed = item[prefix + "_answer_pass_rate"]
            lines.append(f"| {item['tier'] or item['model'] or 'Single model'} | {item['context']} | {label} | "
                f"{completed}/{item['trials_requested_per_case']} | {item['verified_trial_pairs']} | "
                f"{number(item[prefix + '_generation_s_mean'])} | {number(item[prefix + '_ttft_s_mean'], .001)} | "
                f"{item[prefix + '_ttft_measured_trials'] or 0}/{completed} | "
                f"{percent(field)} | {percent(passed)} | {number(item[prefix + '_' + peak + '_mean'], 1024**2)} | "
                f"{item[prefix + '_' + peak + '_measured_trials'] or 0}/{completed} | "
                f"{number(item[prefix + '_engine_rss_bytes_after_mean'], 1024**2)} | "
                f"{item[prefix + '_engine_rss_bytes_after_measured_trials'] or 0}/{completed} |")
    memory_scope = ("CUDA peak is the engine's Torch allocator peak, reset before each request; weights and KV allocations are included. "
        "Reserved peak/after and device-wide used memory after the request are saved separately. Torch counters exclude allocations outside its allocator; "
        "device-wide usage includes other processes. Extra peak subtracts the pre-request allocated bytes. Loaded parameter SHA-256 must match across paired trials. "
        if backend == "cuda" else "MLX peak is the engine's tracked active allocation peak, reset before each request; it includes weights and KV allocations, "
        "and excludes allocator cache and allocations outside MLX. Extra peak above the pre-request active allocation is also saved. "
        )
    lines += ["", memory_scope +
        "Engine RSS is a post-request resident-memory snapshot, not a sampled request peak. Its saved high-water mark is cumulative. "
        "These scopes overlap and must not be added. Memory RPCs and counter reset are outside TTFT and latency timing; "
        "missing measurements stay unavailable with explicit coverage. No activation-memory saving is assumed.", "",
        "Detailed metrics, sample deviations, coverage and verified-pair counts: `activation_comparison.json` / `activation_comparison.csv`.", ""]
    (output_dir / "activation_comparison.md").write_text("\n".join(lines))
    return lines
