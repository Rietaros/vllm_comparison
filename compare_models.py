#!/usr/bin/env python3
"""Compare three model sizes, four weight formats and three contexts on Metal."""
from __future__ import annotations

import argparse
import csv
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

import compare_vllm as bench
from benchmark_config import DEFAULT_CONFIG, TIERS, load_models


def collect_results(output_dir, settings):
    """Keep every model/context cell separate; never use another model's FP32."""
    summaries, trials, models = [], [], []
    for tier, model in zip(TIERS, settings["models"]):
        path = output_dir / tier.lower() / "results.json"
        metadata = {"tier": tier, "model": model}
        if not path.exists():
            summaries.extend({**metadata, **item} for item in bench.summarize_rows(
                [], settings.get("precisions", list(bench.DEFAULT_PRECISIONS)), settings.get("repeats", 10)))
            continue
        data = json.loads(path.read_text())
        if data["settings"]["model"] != model:
            raise ValueError("Model identity mismatch in " + str(path))
        summaries.extend({**metadata, **item} for item in data["summary"])
        trials.extend({**metadata, **row} for row in data["results"])
        parameter_count = data["settings"].get("model_parameter_count")
        if parameter_count is None:
            parameter_count = next((sum(row["checkpoint_elements_by_dtype"].values()) for row in data["results"]
                                    if row["status"] == "ok" and row["precision"] in ("FP32", "BF16")
                                    and row.get("checkpoint_elements_by_dtype")), None)
        models.append({**metadata, "source_revision": data["settings"].get("source_revision"),
                       "model_parameter_count": parameter_count,
                       "source_weight_stats": data["settings"].get("source_weight_stats"),
                       "memory_plans": data["settings"].get("memory_plans"),
                       "enable_thinking": data["settings"].get("enable_thinking"),
                       "prompts": [{key: prompt.get(key) for key in ("context", "task_id", "task_description",
                                     "input_tokens", "record_count", "prompt_sha256", "expected", "reasoning_fields", "output_example")}
                                   for prompt in data.get("prompts", [])],
                       "report": str(path.parent / "comparison.md"),
                       "hardware": data["hardware"]})
    return summaries, trials, models


def suite_report(output_dir, hardware, settings):
    summaries, trials, models = collect_results(output_dir, settings)
    conditions_path = output_dir / "measurement_conditions.json"
    conditions = json.loads(conditions_path.read_text()) if conditions_path.exists() else []
    bench.write_json(output_dir / "suite_results.json", {"hardware": hardware, "settings": settings,
                     "models": models, "measurement_conditions": conditions,
                     "summary": summaries, "results": trials})
    for name, items in (("suite_summary.csv", summaries), ("suite_trials.csv", trials)):
        if not items:
            continue
        fields = list(dict.fromkeys(key for item in items for key in item))
        with (output_dir / name).open("w", newline="") as stream:
            writer = csv.DictWriter(stream, fieldnames=fields)
            writer.writeheader()
            writer.writerows({key: json.dumps(value, ensure_ascii=False) if isinstance(value, (dict, list)) else value
                             for key, value in item.items()} for item in items)
    def number(value, places=2):
        return f"{value:.{places}f}" if value is not None else "—"
    def percent(value):
        return number(value * 100, 0) + "%" if value is not None else "—"
    attempted = sum(row.get("generation_calls", 0) for row in trials)
    successful = sum(row["status"] == "ok" for row in trials)
    skipped = sum(row["status"] == "skipped" for row in trials)
    errors = sum(row["status"] == "error" for row in trials)
    requested = 3 * len(settings["precisions"]) * 3 * settings["repeats"]
    lines = ["# Model size and precision comparison", "",
             f"Hardware: **{hardware.get('chip', hardware['architecture'])}, {hardware.get('memory_bytes', 0) / 1024**3:.0f} GiB unified RAM**, "
             f"{hardware['cpu_cores']} CPU cores, {hardware.get('gpu_cores', 'unrecorded')} GPU cores, macOS {hardware['os_version']}. Backend: vLLM-Metal.", "",
             f"Requested {requested} generations; attempted {attempted}; completed {successful}; hardware-skipped {skipped}; error rows {errors}. "
             f"Each measured model/precision/context cell has {settings['repeats']} requested repetitions.", "",
             "The tiers describe relative parameter counts within this laptop experiment. A 4B model is the largest tier here, not a frontier model.", "",
             "## Models and hardware fit", "",
             "| Tier | Model | Model parameters | Precision | Estimated runtime GiB | Budget GiB | Hardware plan |",
             "|---|---|---:|---|---:|---:|---|"]
    if "memory_bytes" in hardware:
        budget = bench.laptop_memory_budget(hardware, settings.get("memory_fraction"), settings.get("memory_budget_gib"))
        lines[4:4] = [f"Requested laptop budget: {budget['requested_bytes'] / 1024**3:.2f} GiB; "
                      f"effective device budget: {budget['effective_bytes'] / 1024**3:.2f} GiB. "
                      f"Metal receives {budget['backend_memory_fraction']:.4f} of its recommended working set. "
                      "This is a planning budget rather than a measured or hard process-memory cap.", ""]
    for item in models:
        count = item.get("model_parameter_count")
        for precision, plan in (item.get("memory_plans") or {}).items():
            lines.append(f"| {item['tier']} | {item['model']} | {number(count / 1e9 if count else None, 3)}B | {precision} | "
                         f"{number(plan['estimated_runtime_bytes'] / 1024**3)} | {number(plan['runtime_budget_bytes'] / 1024**3)} | "
                         f"{'Fits configured budget' if plan['fits'] else 'Skipped'} |")
    lines += ["", "Runtime estimates include weights, group-scale allowance, a context-sized KV cache and 1 GiB workspace/engine reserve. "
              "The requested budget is capped to physical RAM and Apple's recommended GPU working set. Estimates are not measured peak usage. "
              "Each model result records a live memory/swap snapshot; other applications and swap can affect timing.", "",
              "## Tasks", "",
              "Short tests stock availability; Medium filters and ranks supplier quotes; Long reconciles a shipment dossier with correction notices and a superseding memo. "
              "Rows contain unique receipts, offers and movements instead of repeated filler. Each reference answer is computed from the same task data supplied to the model.", "",
              "Every context includes a valid JSON format example with illustrative values. Models must compute their own answer and return evaluated integer results.", "",
              "Length and task difficulty change together. Cross-context timing differences describe different workloads and cannot isolate context length as their cause.", ""]
    if models:
        for prompt in models[0].get("prompts", []):
            lines += [f"- **{prompt['context']}**: {prompt['task_description']} Input tokens: {prompt['input_tokens']}; "
                      f"records: {prompt['record_count']}; reference: `{json.dumps(prompt['expected'], ensure_ascii=False)}`."]
    lines += ["", "## Average results", "",
              "| Tier | Precision | Context | Status | Completed | Tokens in / mean out | Saved weights GiB | Mean seconds ± SD | Mean TTFT ms ± SD | TTFT measured / completed | Mean output tokens/s | JSON valid | Correct fields | Reasoning fields | Exact answer pass |",
              "|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|"]
    if conditions:
        start = lines.index("## Average results")
        lines[start:start] = ["## Measurement conditions", "", *["- " + note for note in conditions], ""]
    for item in summaries:
        seconds = item["generation_s_mean"]
        timing = number(seconds, 3) + " ± " + number(item["generation_s_stddev"], 3) if seconds is not None else "—"
        valid, passed = item["json_valid_rate"], item["answer_pass_rate"]
        ttft, ttft_coverage = bench.ttft_cells(item)
        lines.append(f"| {item['tier']} | {item['precision']} | {item['context']} | {item['status']} | "
                     f"{item['trials_successful']}/{item['trials_requested']} | {item['input_tokens'] or '—'} / {number(item['output_tokens_mean'], 1)} | "
                     f"{number(item['weight_payload_bytes'] / 1024**3 if item['weight_payload_bytes'] is not None else None)} | {timing} | {ttft} | {ttft_coverage} | "
                     f"{number(item['end_to_end_tokens_per_s_mean'], 1)} | {percent(valid)} | "
                     f"{percent(item['field_accuracy_mean'])} | {percent(item.get('reasoning_accuracy_mean'))} | {percent(passed)} |")
    lines += ["", "Tokens/s means generated output tokens divided by the full request time, including input prefill, decode and API overhead. "
              "It is not decode-only speed. Compare latency together with output length; longer or incorrect responses can distort output tokens/s.", "",
              "TTFT (time to first token) is engine request arrival to the first generated token reaching the engine frontend, "
              "including queueing and prefill. It excludes model setup, subsequent decoding and HTTP/network transport. "
              "The table shows arithmetic mean ± sample SD in milliseconds; JSON/CSV timings remain in seconds. "
              "TTFT measured / completed shows coverage. Missing metrics are unavailable and excluded from TTFT averages; "
              "total request latency cannot be used to reconstruct them.", "",
              f"Output limit: {settings['max_new_tokens']} tokens per request. "
              f"{sum(r.get('finish_reason') == 'length' for r in trials)} returned responses reached this limit. "
              "Truncated answers are retained and graded as returned; they are included in the reported answer pass rates.", "",
              "Thinking is disabled by default for Qwen3. Models use the same task builders and context budgets; exact prompts, token counts and per-model reference answers are saved. "
              "FP32 comparisons stay within each model. A skipped FP32 baseline leaves speedup empty.", "",
              "Accuracy is strict ground-truth JSON field matching on a distinct synthetic task per context. "
              "JSON fences are accepted; values and types must match exactly. Full-answer pass requires exactly the requested keys. "
              "Reasoning fields include each task's numerical calculations and rule-based decisions; names are scored separately in the raw field results. "
              "Invalid JSON prevents field scoring. Per-field rates use successful requests; full-answer/JSON rates count all generation attempts. "
              "Ten greedy repetitions measure timing variability, not ten independent examples or cross-validation. "
              "These tasks cannot establish general model quality or a monotonic relationship between model size and correctness.", "",
              "FP8 is MXFP8 weight storage with BF16 activations; INT4 uses affine weights with BF16 activations. "
              "FP32 is cast from the same BF16 source checkpoint; it cannot recover training precision. "
              "Unsupported or oversized cases have no fabricated timing or accuracy.", "",
              "## Outputs and evidence", ""]
    if "FP8_A8" in settings["precisions"]:
        index = lines.index("## Outputs and evidence")
        lines[index:index] = bench.write_comparison(output_dir, summaries, trials)
    for item in models:
        prompt_link = (f"[complete prompts]({item['tier'].lower()}/prompts.md), "
                       if any(p.get("input_tokens") for p in item.get("prompts", [])) else "")
        lines.append(f"- [{item['tier']} individual outputs, means and engine warnings]({item['tier'].lower()}/comparison.md), "
                     + prompt_link +
                     f"[model card](https://huggingface.co/{item['model']}). Resolved source: `{item['source_revision']}`.")
    lines += ["", "Raw trials: `suite_trials.csv` / `suite_results.json`. Aggregated cells: `suite_summary.csv`. "
              "Per-model folders retain checkpoint audits, prompts, job specifications, engine logs and all generated answers.", ""]
    warnings = sorted({row["tier"] + "/" + row["precision"] for row in trials if row.get("engine_teardown_warning")})
    if warnings:
        lines += ["The installed backend logged segmentation faults during engine teardown after saving completed results for: "
                  + ", ".join(warnings) + ". These timings exclude teardown; clean shutdown is not verified.", ""]
    (output_dir / "comparison.md").write_text("\n".join(lines))
    print(f"Suite: {successful}/{requested} completed, {skipped} skipped. Report: {output_dir / 'comparison.md'}", flush=True)


def parse_args(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, default=DEFAULT_CONFIG, help="Model configuration JSON (default: config.json beside this script)")
    parser.add_argument("--models", nargs=3, metavar=("LIGHT", "MEDIUM", "COMPLEX"),
                        help="Override the lightweight, medium and complex models from config")
    parser.add_argument("--model-order", nargs=3, choices=TIERS, default=list(TIERS),
                        help="Engine execution order; report rows keep the canonical tier order")
    bench.add_precision_arguments(parser)
    parser.add_argument("--context-tokens", nargs=3, type=int, default=[256, 1024, 4096])
    parser.add_argument("--repeats", type=int, default=10)
    parser.add_argument("--max-new-tokens", type=int, default=96)
    bench.add_memory_arguments(parser)
    parser.add_argument("--timeout", type=int, default=1200, help="Maximum seconds per precision, excluding conversion")
    parser.add_argument("--thinking", choices=["auto", "on", "off"], default="auto")
    parser.add_argument("--output-dir", type=Path)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--resume", action="store_true")
    args = parser.parse_args(argv)
    if args.activation_comparison:
        args.precisions = list(bench.ACTIVATION_PRECISIONS)
    if args.models is None:
        try:
            args.models = load_models(args.config)
        except (OSError, ValueError) as error:
            parser.error(str(error))
    bench.validate_memory_arguments(args, parser)
    if args.repeats <= 0 or args.max_new_tokens <= 0 or args.timeout <= 0:
        parser.error("Repeats, tokens and timeout must be positive")
    if not 0 < args.context_tokens[0] < args.context_tokens[1] < args.context_tokens[2]:
        parser.error("Context budgets must be positive and strictly increasing")
    if len(set(args.models)) != 3 or len(set(args.precisions)) != len(args.precisions):
        parser.error("Use three distinct models and unique precisions")
    if set(args.model_order) != set(TIERS):
        parser.error("Model order must contain each tier exactly once")
    if args.resume and (args.output_dir is None or args.dry_run):
        parser.error("Resume requires a real run and its existing output directory")
    return args


def main():
    args = parse_args()
    bench.local_environment()
    hardware = bench.hardware_info()
    output_dir = (args.output_dir or bench.ROOT / "results" / ("models_" + datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ"))).resolve()
    settings = {key: getattr(args, key) for key in ("models", "model_order", "precisions", "context_tokens", "repeats", "max_new_tokens", "memory_fraction", "memory_budget_gib", "thinking", "dry_run")}
    settings["cache_policy"] = "physical-budget-to-metal-with-block-override-v1"
    settings["prompt_suite"] = bench.PROMPT_SUITE
    settings["timing_policy"] = bench.TIMING_POLICY
    settings.update(bench.activation_settings(args.precisions))
    manifest = output_dir / "suite_manifest.json"
    if args.resume:
        previous = json.loads(manifest.read_text())
        if previous["settings"] != settings or previous["hardware"]["packages"] != hardware["packages"]:
            raise ValueError("Resume requires identical suite settings and package versions")
    elif manifest.exists():
        raise ValueError("Suite exists; use a new output directory or --resume")
    bench.write_json(manifest, {"settings": settings, "hardware": hardware})
    suite_report(output_dir, hardware, settings)
    failures = []
    for tier in args.model_order:
        model = args.models[TIERS.index(tier)]
        folder = output_dir / tier.lower()
        folder.mkdir(parents=True, exist_ok=True)
        command = [sys.executable, str(bench.ROOT / "compare_vllm.py"), "--model", model,
                   "--output-dir", str(folder), "--repeats", str(args.repeats),
                   "--max-new-tokens", str(args.max_new_tokens),
                   *(["--memory-budget-gib", str(args.memory_budget_gib)] if args.memory_budget_gib is not None
                     else ["--memory-fraction", str(args.memory_fraction)]),
                   "--timeout", str(args.timeout), "--thinking", args.thinking,
                   "--precisions", *args.precisions, "--context-tokens", *map(str, args.context_tokens)]
        if args.dry_run:
            command.append("--dry-run")
        if args.resume and (folder / "results.json").exists():
            command.append("--resume")
        print(f"Running {tier}: {model}", flush=True)
        with (folder / "benchmark.log").open("a" if args.resume else "w") as log:
            result = subprocess.run(command, stdout=log, stderr=subprocess.STDOUT)
        if result.returncode:
            failures.append(tier)
            print(f"{tier} returned {result.returncode}; see {folder / 'benchmark.log'}", flush=True)
        suite_report(output_dir, hardware, settings)
    if failures:
        print("Incomplete model runs: " + ", ".join(failures), file=sys.stderr)
    return 1 if failures else 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (OSError, ValueError) as error:
        print("Error: " + str(error), file=sys.stderr)
        sys.exit(2)
