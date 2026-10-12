"""Verify and export a completed three-model case comparison without model weights."""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import statistics
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import compare_vllm as bench
import activation_experiment as activation


def canonical(value):
    return json.dumps(value, sort_keys=True, ensure_ascii=True, allow_nan=False)


def verify_run(source):
    suite = json.loads((source / "suite_results.json").read_text())
    rows = suite["results"]
    repeats, precisions = suite["settings"]["repeats"], suite["settings"]["precisions"]
    expected_keys = {(tier, precision, context, index) for tier in ("Lightweight", "Medium", "Complex")
                     for precision in precisions for context in bench.LEVELS for index in range(1, repeats + 1)}
    keys = {(row["tier"], row["precision"], row["context"], row["trial_id"]) for row in rows}
    if len(rows) != len(keys) or keys != expected_keys or any(row["status"] not in ("ok", "skipped") for row in rows):
        raise ValueError("Export requires all requested cases completed or explicitly memory-skipped, with no duplicate or failed trials")
    models, case_signatures, pair_count = [], None, 0
    for tier in ("lightweight", "medium", "complex"):
        data = json.loads((source / tier / "results.json").read_text())
        if data["settings"]["task_suite_sha256"] != suite["settings"]["task_suite_sha256"]:
            raise ValueError("Dataset identity differs between models")
        prompts = {(p["context"], p["trial_id"]): p for p in data["prompts"]}
        if len(prompts) != len(bench.LEVELS) * repeats:
            raise ValueError("Saved prompts do not contain one case per context and trial")
        signatures = {}
        for key, prompt in prompts.items():
            digest = hashlib.sha256(json.dumps(prompt["prompt_token_ids"]).encode()).hexdigest()
            if digest != prompt["prompt_sha256"] or len(prompt["prompt_token_ids"]) != prompt["input_tokens"]:
                raise ValueError("Saved token hash/count mismatch: " + prompt["case_id"])
            if prompt["input_tokens"] > prompt["target_tokens"]:
                raise ValueError("Case exceeds its input budget: " + prompt["case_id"])
            expectation = {"expected": prompt["expected"], "reasoning_fields": prompt["reasoning_fields"], "comparison": prompt["comparison"]}
            if hashlib.sha256(json.dumps(expectation, sort_keys=True).encode()).hexdigest() != prompt["expectation_sha256"]:
                raise ValueError("Expectation hash mismatch: " + prompt["case_id"])
            signatures[key] = {"case_id": prompt["case_id"], "prompt_sha256": digest,
                               "expectation_sha256": prompt["expectation_sha256"], "expected": prompt["expected"]}
        for context in bench.LEVELS:
            cases = [p for p in prompts.values() if p["context"] == context]
            if len({p["prompt_text_sha256"] for p in cases}) != repeats:
                raise ValueError("Duplicate context prompts in saved trials")
        identical_to_first = case_signatures is None or canonical(signatures_as_list(signatures)) == canonical(signatures_as_list(case_signatures))
        if case_signatures is None:
            case_signatures = signatures
        for row in data["results"]:
            prompt = prompts[bench.trial_key(row)]
            for field in ("case_id", "prompt_sha256", "expectation_sha256", "expected", "reasoning_fields", "comparison"):
                if canonical(row[field]) != canonical(prompt[field]):
                    raise ValueError(f"Wrong case/answer on a trial: {tier}/{row['precision']}/{bench.trial_key(row)}: {field}")
            if row["status"] == "skipped":
                if row["generation_calls"] != 0 or row.get("generation_s") is not None:
                    raise ValueError("Skipped case contains a generation or timing")
                continue
            if row["generation_calls"] != 1 or not math.isfinite(row["generation_s"]) or row["generation_s"] <= 0:
                raise ValueError("Each completed case must have exactly one real generation")
            if row.get("ttft_s") is not None and not 0 < row["ttft_s"] <= row["generation_s"]:
                raise ValueError("Invalid TTFT")
            score = bench.score_answer(row["output"], prompt["expected"], prompt["reasoning_fields"], prompt["comparison"])
            if any(canonical(row[field]) != canonical(value) for field, value in score.items()):
                raise ValueError("Stored score differs from its configured answer comparison")
        for cell in data["summary"]:
            selected = [r for r in data["results"] if r["precision"] == cell["precision"] and r["context"] == cell["context"] and r["status"] == "ok"]
            if cell["trials_successful"] != len(selected):
                raise ValueError("Summary completion count mismatch")
            if selected:
                for field in ("generation_s", "ttft_s", "field_accuracy"):
                    values = [r[field] for r in selected if r.get(field) is not None]
                    if values and not math.isclose(cell[field + "_mean"], statistics.mean(values), rel_tol=1e-12):
                        raise ValueError("Summary mean mismatch: " + field)
                    if len(values) > 1 and not math.isclose(cell[field + "_stddev"], statistics.stdev(values), rel_tol=1e-12, abs_tol=1e-12):
                        raise ValueError("Summary sample deviation mismatch: " + field)
                if len(cell["expected_by_trial"]) != repeats or cell["unique_cases_successful"] != len(selected):
                    raise ValueError("Summary collapsed distinct cases or references")
        pairs = activation.comparison_rows(data["summary"], data["results"], suite["settings"]["backend"])
        pair_count += sum(pair["successful_trial_pairs"] for pair in pairs)
        source_model = Path(data["settings"]["model"])
        marker = source_model / "comparison_manifest.json"
        identity = json.loads(marker.read_text())["identity"] if marker.exists() else {}
        models.append({"tier": tier, "source": data["settings"]["model"],
            "model": identity.get("model", data["settings"]["model"]),
            "original_revision": identity.get("revision", data["settings"].get("source_revision")),
            "same_tokens_and_answers_as_first_model": identical_to_first,
            "cases": [{"context": p["context"], "trial_id": p["trial_id"], "case_id": p["case_id"],
                       "input_tokens": p["input_tokens"], "expected": p["expected"],
                       "prompt_sha256": p["prompt_sha256"], "expectation_sha256": p["expectation_sha256"]} for p in data["prompts"]]})
    verification = {"backend": suite["settings"]["backend"], "requested": len(rows),
        "completed": sum(r["status"] == "ok" for r in rows), "skipped": sum(r["status"] == "skipped" for r in rows),
        "failed": 0, "cases_per_context": repeats, "dataset_cases": len(bench.LEVELS) * repeats,
        "ttft_measured": sum(r["status"] == "ok" and r.get("ttft_s") is not None for r in rows),
        "verified_activation_pairs": pair_count, "task_suite_sha256": suite["settings"]["task_suite_sha256"],
        "models": models, "engine_teardown_warnings": sorted({r["tier"] + "/" + r["precision"] for r in rows if r.get("engine_teardown_warning")}),
        "checks": ["exact requested matrix and unique trial keys", "one distinct saved prompt per context/trial",
            "each format uses the correct case ID, tokens, expectation hash, and answer", "one generation per successful trial",
            "skipped cases have no generation or timing", "token hashes/counts and budgets", "typed expectation hashes",
            "configured accuracy scores recomputed", "means and sample deviations recomputed",
            "individual expectations retained in summaries", "fixed FP8 activation-pair contracts verified"]}
    return suite, verification


def signatures_as_list(signatures):
    return [{"context": key[0], "trial_id": key[1], **value} for key, value in sorted(signatures.items())]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input-dir", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--run-date", required=True, help="User-facing date, YYYY-MM-DD")
    args = parser.parse_args()
    source, output = args.input_dir.resolve(), args.output_dir.resolve()
    if source == output:
        raise ValueError("Export destination must differ from the original run")
    suite, verification = verify_run(source)
    output.mkdir(parents=True, exist_ok=True)

    def clean(text):
        text = text.replace(str(source) + "/", "").replace(str(ROOT) + "/", "")
        for model in verification["models"]:
            if model["source"] != model["model"]:
                text = text.replace("https://huggingface.co/" + model["source"], "https://huggingface.co/" + model["model"])
        return text

    for tier in ("", "lightweight", "medium", "complex"):
        destination = output / tier
        destination.mkdir(exist_ok=True)
        names = ["comparison.md", "activation_comparison.md", "activation_comparison.csv", "activation_comparison.json"]
        names += ["suite_summary.csv"] if not tier else ["prompts.md"]
        for name in names:
            path = source / tier / name
            if path.exists():
                text = clean(path.read_text())
                if name.endswith(".md"):
                    text = "\n".join(line.rstrip() for line in text.splitlines()) + "\n"
                (destination / name).write_text(text)
    fields = ["tier", "model", "precision", "context", "trial_id", "case_id", "status", "input_tokens", "output_tokens",
              "generation_calls", "generation_s", "ttft_s", "expected", "parsed_answer", "field_accuracy", "reasoning_accuracy",
              "all_fields_correct", "comparison", "prompt_sha256", "expectation_sha256", "finish_reason", "output", *bench.MEMORY_METRICS]
    with (output / "trials.csv").open("w", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows({key: json.dumps(row.get(key), ensure_ascii=False) if key == "output"
                         else clean(json.dumps(row.get(key), ensure_ascii=False)) if isinstance(row.get(key), (dict, list))
                         else row.get(key) for key in fields} for row in suite["results"])
    verification["run_date"] = args.run_date
    (output / "verification.json").write_text(clean(json.dumps(verification, indent=2)) + "\n")
    hardware = suite["hardware"]
    hardware_label = bench.hardware_description(hardware)
    model_table = "\n".join(f"| {m['tier']} | {m['model']} | `{m['original_revision']}` |" for m in verification["models"])
    warnings = ", ".join(verification["engine_teardown_warnings"])
    warning_text = ("The backend logged teardown segmentation faults after saving results for " + warnings + ". Warnings are retained in the reports; clean teardown is not verified.") if warnings else "No teardown warning was detected."
    settings = suite["settings"]
    budgets = " / ".join(f"{number:,}" for number in settings["context_tokens"])
    budget_label = (f"{settings['memory_fraction'] * 100:g}% of selected device memory" if settings.get("memory_fraction") is not None
                    else f"{settings.get('memory_budget_gib') or 10:g} GiB")
    platform_note = ("This run used NVIDIA CUDA." if verification["backend"] == "cuda"
                     else "This run used Apple Silicon; NVIDIA inference was not performed here.")
    source_note = ("The run used the existing local dense BF16 source copies recorded below, avoiding another model download."
                   if all(Path(model["source"]).is_dir() for model in verification["models"])
                   else "The source models and resolved revisions are recorded below.")
    (output / "README.md").write_text(f"""# Ten different cases per context: comparison output

Run date: **{args.run_date}**. Hardware: {hardware_label}.

**{verification['completed']} completed generations, {verification['skipped']} memory-skipped slots, {verification['failed']} failed cases.** Each precision/model evaluates {verification['cases_per_context']} different Short, Medium, and Long question/answer pairs: {verification['dataset_cases']} distinct dataset cases, answered once per format/model. Input budgets are {budgets} tokens; output limit is {settings['max_new_tokens']} tokens. The planning budget is {budget_label}.

- [Full comparison and individual model answers](comparison.md)
- [Fixed FP8 activation comparison](activation_comparison.md)
- [Summary CSV](suite_summary.csv) and [all individual trials](trials.csv)
- [Activation CSV](activation_comparison.csv) and [JSON](activation_comparison.json)
- [Verification, case IDs, and expected answers](verification.json)

{verification['ttft_measured']} successful requests have measured TTFT. All {verification['verified_activation_pairs']} FP8/FP8_A8 pairs have verified matching case IDs, token inputs, expected answers, comparison rules, and checkpoint/cache/settings contracts. References are retained per trial, and aggregate statistics were recomputed from the individual measurements.

The `output` column in `trials.csv` is a JSON-encoded string, preserving the exact response including newlines and trailing spaces. Decode it with `json.loads(row["output"])` in Python. Markdown reports show readable answers.

{source_note} New requests used the editable Markdown/JSON case bank; model choices in `config.json` were unchanged.

| Tier | Model | Source revision |
|---|---|---|
{model_table}

Accuracy covers this synthetic dataset. Timing deviations include case differences, output lengths, system load, and first-request initialization work. FP8_A8 applies FP8 rounding with BF16 buffers rather than native FP8 activation storage. GPU memory counters overlap and must not be added. {platform_note}

{warning_text}

Edit [the prompt and answer pairs](../../../prompts/README.md), then run all configured models on Apple Silicon:

```sh
.venv/bin/python compare_models.py --backend metal \\
  --precisions FP32 BF16 FP8 INT4 FP8_A8 --memory-budget-gib 10 \\
  --repeats 10 --timeout 3600 --output-dir results/my-distinct-cases
```

On NVIDIA, use `.venv-cuda/bin/python`, `--backend cuda`, and `--memory-fraction 0.8` instead of the absolute memory budget. See the [main README](../../../README.md) for setup.
""")
    print(json.dumps({key: verification[key] for key in ("completed", "skipped", "failed", "dataset_cases", "verified_activation_pairs")}))


if __name__ == "__main__":
    main()
