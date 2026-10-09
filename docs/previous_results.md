# Previous Apple Silicon results

These measurements used an Apple M1 Pro with 10 CPU cores, 16 GPU cores, 16 GB unified memory, and macOS 15.5. They are historical Metal measurements; NVIDIA results must be generated on your own server.

The `results/...` paths below refer to local generated artifacts, which are excluded from Git and are not included in a fresh clone. Follow the [README](../README.md) to generate a new comparison. Test counts below describe the checks performed at the time of each historical run.

## Time to first token results (10 GiB)

The latest full comparison with TTFT (`results/json_examples_10gib_ttft_10_runs/comparison.md`) reran all **330 feasible requests**, with **10 repeats per model/precision/context** and the same **10 GiB** budget, differentiated prompts and illustrative JSON examples. TTFT was measured for **330/330 completed requests**. The 30 Complex/FP32 slots remain hardware-budget skips.

**TTFT** is the wait from engine request arrival to the first generated token, including queueing and input prefill. It excludes model setup and subsequent decoding. Reports now show **mean TTFT ± sample SD in milliseconds** and **measured/completed coverage** next to total request latency and end-to-end tokens/s. Raw JSON/CSV timings and summary statistics use seconds.

INT4 provides a measured format across all three tiers. TTFT in **milliseconds**, mean ± sample SD over ten requests:

| Tier | Short | Medium | Long |
|---|---:|---:|---:|
| Lightweight | 120.5 ± 10.8 | 452.8 ± 13.9 | 2855.5 ± 19.2 |
| Medium | 348.8 ± 95.3 | 1281.0 ± 297.0 | 5877.6 ± 420.8 |
| Complex | 794.0 ± 39.2 | 3168.3 ± 200.0 | 15555.9 ± 802.6 |

For example, Complex INT4/Long averaged **15,555.9 ms TTFT** and **16.842 s total latency**. Most of that request elapsed before the first token, which explains why its end-to-end output tokens/s is low even with a short answer.

All **25 tests passed**, and independent verification (`results/json_examples_10gib_ttft_10_runs/verification.txt`) checked every TTFT value, timing bound, aggregate, coverage count and table unit, alongside the existing task, precision and memory checks. Details are in validation.json (`results/json_examples_10gib_ttft_10_runs/validation.json`); the verification script is retained in that folder.

Full-answer pass remains **0%** in all 33 measured cells on these three fixed tasks. The backend again logged teardown segmentation faults in nine cases after saving completed results; warnings remain in the reports and engine logs. TTFT and total request timing exclude teardown.

This is a fresh cohort with engine statistics enabled. Historical timings and answers are retained separately, and unavailable historical TTFT is never estimated from total latency. To repeat this measurement policy, use a fresh directory:

```sh
.venv/bin/python compare_models.py --memory-budget-gib 10 --model-order Complex Lightweight Medium --repeats 10 --output-dir results/ttft-next-run
```

## Earlier JSON examples and 10 GiB results (without TTFT)

This earlier full comparison (`results/json_examples_10gib_10_runs/comparison.md`) contains **330 completed generations**, **30 Complex/FP32 budget skips**, and **36 model/precision/context summaries**. Every feasible cell ran **10 times**. All three prompt levels include valid, illustrative JSON examples. The requested and effective budget are both **10 GiB**, with an engine fraction of approximately **0.9375** of Apple's recommended working set. The complete prompts (`results/json_examples_10gib_10_runs/lightweight/prompts.md`) show the examples and reference answers. Engine statistics were disabled for this historical run, so its added TTFT columns correctly show **unavailable, 0/10**. Historical total latency and answer measurements are retained.

The larger budget enabled two additional formats. Mean generation latency in seconds, with sample standard deviation:

| Newly measured case | Short | Medium | Long |
|---|---:|---:|---:|
| Medium Qwen3-1.7B, FP32 | 2.417 ± 1.830 | 7.638 ± 1.911 | 24.536 ± 2.161 |
| Complex Qwen3-4B, BF16 | 6.604 ± 2.659 | 7.444 ± 2.092 | 19.338 ± 3.706 |

INT4 remained available for all three tiers:

| Tier | Short | Medium | Long |
|---|---:|---:|---:|
| Lightweight Qwen3-0.6B | 0.259 ± 0.009 | 0.706 ± 0.008 | 3.291 ± 0.009 |
| Medium Qwen3-1.7B | 0.505 ± 0.017 | 1.933 ± 0.049 | 6.383 ± 0.064 |
| Complex Qwen3-4B | 1.738 ± 0.011 | 3.782 ± 0.009 | 15.959 ± 0.017 |

None of the 33 measured cells matched every reference field. The best field score was **75% for Complex FP8/Long**: destination, available stock and action were correct, but shortfall was wrong. Several answers still contain unevaluated expressions or incorrect values despite the examples. **20 Medium FP32/BF16 responses reached the 96-token output limit**, and are graded as returned. Each measured cell produced one identical output across its ten repeats. These results describe the current tasks, decoding settings and limit; they do not establish general model accuracy.

All **22 tests passed**. Independent verification checked trial counts, exact 10 GiB budgets, Metal fraction mapping, prompt examples and references, means/SDs, field scores, checkpoint reuse, cache overrides, CSV schemas and FP32 baselines within both Lightweight and Medium. See validation.json (`results/json_examples_10gib_10_runs/validation.json`) and verification.txt (`results/json_examples_10gib_10_runs/verification.txt`). The backend still logged teardown segmentation faults in nine measured cases after saving their results; the report and logs preserve these warnings. The dense cases showed greater timing variation on this working laptop, with memory/swap snapshots retained.

Budget, examples and fitted record counts changed together. Compare precisions within this run, and keep the earlier measurements separate. To repeat the current configuration, choose a fresh destination:

```sh
.venv/bin/python compare_models.py --memory-budget-gib 10 --model-order Complex Lightweight Medium --repeats 10 --output-dir results/json-examples-10gib-next
```

## Earlier differentiated prompt results (6.4 GiB, without JSON examples)

The new full comparison (`results/differentiated_prompts_10_runs/comparison.md`) contains **270 completed generations**, **90 RAM-budget-skipped slots**, and **36 summaries** across Qwen3-0.6B, Qwen3-1.7B and Qwen3-4B. Every feasible precision/context ran **10 times**. All checkpoints were reused from cache, and the sources match the previous three-model run. Read the complete prompts and reference answers (`results/differentiated_prompts_10_runs/lightweight/prompts.md`).

INT4 provides one measured format across all three model tiers. Mean request latency in seconds, with sample standard deviation:

| Tier | Short: stock check | Medium: supplier selection | Long: shipment reconciliation | Full answer pass at Short / Medium / Long |
|---|---:|---:|---:|---|
| Lightweight, Qwen3-0.6B | 0.310 ± 0.010 | 0.776 ± 0.010 | 3.363 ± 0.076 | 0% / 0% / 0% |
| Medium, Qwen3-1.7B | 0.547 ± 0.005 | 1.594 ± 0.005 | 6.212 ± 0.014 | 0% / 0% / 0% |
| Complex, Qwen3-4B | 1.254 ± 0.018 | 3.922 ± 0.012 | 16.006 ± 0.013 | 0% / 0% / 0% |

None of the 27 measured model/precision/context cells passed every required field. This does not mean every field was wrong: Short generally matched the item and fulfillment decision but miscalculated the available stock; Complex FP8/Long matched Surabaya and REORDER for **50% field accuracy** while missing both numbers. Complex FP8/Short returned an unevaluated arithmetic expression inside its JSON, making the whole object invalid. The full report shows every format's means, output lengths, JSON validity, reasoning scores and exact answers. All cells produced one identical answer across their ten greedy repeats, so these repetitions do not provide independent accuracy examples.

The new tasks differ in content, length and difficulty; compare the formats on the same task. The old repeated-context results below remain unchanged and should not be pooled with these measurements. All **19 tests passed**, and an independent check verified the actual trial counts, task references, field scores, means/SDs, checkpoint reuse, cache overrides, CSV schemas and identical inputs across the three models. Validation details are in validation.json (`results/differentiated_prompts_10_runs/validation.json`). The installed backend continued to log teardown segmentation faults after saving results; these warnings remain in the reports and raw data.

To run these models with the current JSON examples and 10 GiB budget, use a fresh output directory:

```sh
.venv/bin/python compare_models.py --model-order Complex Lightweight Medium --repeats 10 --output-dir results/differentiated-next-run
```

## Earlier single-model results (repeated context)

The original one-run comparison is preserved in results/laptop/comparison.md (`results/laptop/comparison.md`). The earlier ten-run average comparison is saved in results/laptop_10_runs/comparison.md (`results/laptop_10_runs/comparison.md`), with individual trials in `results.csv` and averages in `summary.csv`. These used the original repeated-context task. Several answers can fail the requested JSON/calculation task, so timing alone should not select a precision.

All 120 requests in the ten-run benchmark completed. Mean latency in seconds (sample standard deviation after ±):

| Precision | Short | Medium | Long |
|---|---:|---:|---:|
| FP32 | 0.572 ± 0.013 | 1.093 ± 0.020 | 6.705 ± 0.046 |
| BF16 | 0.400 ± 0.014 | 0.619 ± 0.064 | 1.755 ± 0.079 |
| FP8 (MXFP8) | 0.371 ± 0.018 | 0.635 ± 0.022 | 2.076 ± 0.195 |
| INT4 | 0.388 ± 0.016 | 0.590 ± 0.015 | 1.899 ± 0.020 |

BF16 had the lowest Long-context mean, while INT4 had the lowest Medium-context mean and smallest weight payload. Only INT4/Medium passed all three answer fields, in all ten trials. Every precision/context produced the same output on its ten repeats. These are observations from this laptop and fixed task, rather than general model-quality rankings.

The installed official vLLM 0.30.0 / vLLM-Metal 0.30.0 stack has logged segmentation faults during engine teardown after saving completed generation results. These are retained in the logs and flagged in the report/CSV/JSON; a clean teardown is not verified. Each precision runs in an isolated process.

## Earlier three-model results (repeated context)

The previous comparison is preserved in results/qwen3_model_comparison_final/comparison.md (`results/qwen3_model_comparison_final/comparison.md`). It contains **270 successful measured requests**, **90 hardware-skipped slots**, **36 model/precision/context summaries**, every generated answer, and averages with sample standard deviation. It used the original repeated-context task. All checkpoints were cached before this run, and all nine measured model/precision engines used the corrected RAM-to-Metal budget mapping and explicit cache block limits.

Run these models with the current JSON examples, 10 GiB budget and a fresh output directory:

```sh
.venv/bin/python compare_models.py --model-order Complex Lightweight Medium --repeats 10
```

INT4 gives one common format across all three tiers. Its mean request times in seconds are:

| Tier | Model | Short | Medium | Long | Full answer pass at Short / Medium / Long |
|---|---|---:|---:|---:|---|
| Lightweight | Qwen3-0.6B | 0.387 | 0.735 | 3.254 | 0% / 0% / 0% |
| Medium | Qwen3-1.7B | 0.529 | 1.534 | 6.283 | 0% / 0% / 0% |
| Complex | Qwen3-4B | 1.278 | 3.770 | 15.859 | 100% / 100% / 100% |

The medium INT4 model calculated `42` correctly but used `"Project ORCHID"`, so it received **66.7% field accuracy** and **0% full-answer pass**. Medium BF16 passed Long context in all ten repeats. Complex FP8 computed the total correctly but also included the project-name prefix, while Complex INT4 passed every field at every context. The report separates JSON validity, per-field scores, and complete-answer matching so these differences are visible.

The tested formats were all four for Lightweight, BF16/FP8/INT4 for Medium, and FP8/INT4 for Complex. Medium FP32 and Complex FP32/BF16 were skipped under the **6.4 GiB configured budget**. This is a budget decision rather than a claim that every skipped format is unsupported by Metal. All models received identical prompt token IDs at each context: **248, 1,018 and 4,084 input tokens**.

The earlier diagnostic run (`results/qwen3_model_comparison/comparison.md`) is preserved separately. It includes an FP8 startup failure caused by the earlier budget mapping and some download-overlapped timings. Use the final report for comparisons. The final raw data were independently checked for unique trial keys, 270 real generation calls, skipped-case accounting, means/SDs, per-field scores, shared prompt hashes, and actual cache overrides. All 15 automated checks passed.

Every cell produced the same answer across its ten greedy repetitions. These results cover a small fixed task; they are not cross-validation or a general model-quality ranking. The installed backend still logged teardown segmentation faults after saving completed results; logs and report warnings retain that limitation.
