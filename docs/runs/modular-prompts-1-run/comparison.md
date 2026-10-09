# Model size and precision comparison

Hardware: Apple M1 Pro, 16 GiB unified RAM, Darwin 15.5. Backend: vLLM-Metal.

Requested memory budget: 10.00 GiB; effective device budget: 10.00 GiB. Backend memory fraction: 0.9375. This is a planning budget rather than a measured or hard process-memory cap.

Requested 45 generations; attempted 42; completed 42; hardware-skipped 3; error rows 0. Each measured model/precision/context cell has 1 requested repetitions.

The tiers describe relative parameter counts within this experiment. A 4B model is the largest default tier.

## Models and hardware fit

| Tier | Model | Model parameters | Precision | Estimated runtime GiB | Budget GiB | Hardware plan |
|---|---|---:|---|---:|---:|---|
| Lightweight | models/7b50efe10ce32606/BF16 | 0.596B | FP32 | 4.16 | 10.00 | Fits configured budget |
| Lightweight | models/7b50efe10ce32606/BF16 | 0.596B | BF16 | 2.61 | 10.00 | Fits configured budget |
| Lightweight | models/7b50efe10ce32606/BF16 | 0.596B | FP8 | 2.11 | 10.00 | Fits configured budget |
| Lightweight | models/7b50efe10ce32606/BF16 | 0.596B | INT4 | 1.81 | 10.00 | Fits configured budget |
| Lightweight | models/7b50efe10ce32606/BF16 | 0.596B | FP8_A8 | 2.11 | 10.00 | Fits configured budget |
| Medium | models/7ec86880db931fb2/BF16 | 1.721B | FP32 | 8.35 | 10.00 | Fits configured budget |
| Medium | models/7ec86880db931fb2/BF16 | 1.721B | BF16 | 4.71 | 10.00 | Fits configured budget |
| Medium | models/7ec86880db931fb2/BF16 | 1.721B | FP8 | 3.26 | 10.00 | Fits configured budget |
| Medium | models/7ec86880db931fb2/BF16 | 1.721B | INT4 | 2.38 | 10.00 | Fits configured budget |
| Medium | models/7ec86880db931fb2/BF16 | 1.721B | FP8_A8 | 3.26 | 10.00 | Fits configured budget |
| Complex | models/e15b00bc84c6b5ee/BF16 | 4.022B | FP32 | 17.18 | 10.00 | Skipped |
| Complex | models/e15b00bc84c6b5ee/BF16 | 4.022B | BF16 | 9.12 | 10.00 | Fits configured budget |
| Complex | models/e15b00bc84c6b5ee/BF16 | 4.022B | FP8 | 5.75 | 10.00 | Fits configured budget |
| Complex | models/e15b00bc84c6b5ee/BF16 | 4.022B | INT4 | 3.69 | 10.00 | Fits configured budget |
| Complex | models/e15b00bc84c6b5ee/BF16 | 4.022B | FP8_A8 | 5.75 | 10.00 | Fits configured budget |

Runtime estimates include weights, quantization overhead, a context-sized KV cache and a backend-specific engine reserve. The requested budget is capped to the selected GPU's limits. Estimates are not measured peak usage. Each model result records its hardware and backend. Concurrent system load can affect timing.

## Tasks

Each context reads a Markdown prompt and its JSON expectation file. Generated tasks fit unique records and compute references from the fitted data. Static tasks use the literal Markdown and configured expected answer without padding.

Length and task difficulty change together. Cross-context timing differences describe different workloads and cannot isolate context length as their cause.

- **Short**: Single-item stock arithmetic and a fulfillment decision. Input tokens: 256; records: 9; reference: `{"item": "MONITOR", "available_units": 68, "fulfillable": true}`; comparison: `{"allow_extra_fields": false, "case_sensitive": true}`.
- **Medium**: Filter competing quotes, calculate landed costs and rank eligible suppliers. Input tokens: 992; records: 20; reference: `{"vendor": "TAMBORA", "landed_cost": 1365, "eligible_vendors": 7, "delivery_days": 4}`; comparison: `{"allow_extra_fields": false, "case_sensitive": true}`.
- **Long**: Reconcile a multi-document ledger, apply corrections and the latest policy, then calculate a dispatch decision. Input tokens: 4065; records: 77; reference: `{"destination": "Surabaya", "available_units": 215, "shortfall_units": 205, "action": "REORDER"}`; comparison: `{"allow_extra_fields": false, "case_sensitive": true}`.

## Average results

| Tier | Precision | Context | Status | Completed | Tokens in / mean out | Saved weights GiB | Mean seconds ± SD | Mean TTFT ms ± SD | TTFT measured / completed | Mean output tokens/s | JSON valid | Correct fields | Reasoning fields | Exact answer pass |
|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Lightweight | FP32 | Short | complete | 1/1 | 256 / 25.0 | 2.22 | 0.632 ± — | 214.8 ± — | 1/1 | 39.6 | 100% | 33% | 0% | 0% |
| Lightweight | FP32 | Medium | complete | 1/1 | 992 / 40.0 | 2.22 | 2.244 ± — | 1494.6 ± — | 1/1 | 17.8 | 100% | 0% | 0% | 0% |
| Lightweight | FP32 | Long | complete | 1/1 | 4065 / 42.0 | 2.22 | 20.740 ± — | 19634.2 ± — | 1/1 | 2.0 | 100% | 25% | 33% | 0% |
| Lightweight | BF16 | Short | complete | 1/1 | 256 / 25.0 | 1.11 | 0.406 ± — | 140.4 ± — | 1/1 | 61.6 | 100% | 33% | 0% | 0% |
| Lightweight | BF16 | Medium | complete | 1/1 | 992 / 40.0 | 1.11 | 0.847 ± — | 397.6 ± — | 1/1 | 47.3 | 100% | 0% | 0% | 0% |
| Lightweight | BF16 | Long | complete | 1/1 | 4065 / 42.0 | 1.11 | 3.312 ± — | 2636.3 ± — | 1/1 | 12.7 | 100% | 25% | 33% | 0% |
| Lightweight | FP8 | Short | complete | 1/1 | 256 / 25.0 | 0.57 | 0.309 ± — | 141.4 ± — | 1/1 | 80.9 | 100% | 33% | 0% | 0% |
| Lightweight | FP8 | Medium | complete | 1/1 | 992 / 61.0 | 0.57 | 0.966 ± — | 474.4 ± — | 1/1 | 63.2 | 0% | 0% | 0% | 0% |
| Lightweight | FP8 | Long | complete | 1/1 | 4065 / 37.0 | 0.57 | 3.435 ± — | 2959.8 ± — | 1/1 | 10.8 | 100% | 0% | 0% | 0% |
| Lightweight | INT4 | Short | complete | 1/1 | 256 / 25.0 | 0.31 | 0.297 ± — | 137.2 ± — | 1/1 | 84.2 | 100% | 33% | 0% | 0% |
| Lightweight | INT4 | Medium | complete | 1/1 | 992 / 41.0 | 0.31 | 0.750 ± — | 462.1 ± — | 1/1 | 54.7 | 100% | 0% | 0% | 0% |
| Lightweight | INT4 | Long | complete | 1/1 | 4065 / 42.0 | 0.31 | 3.346 ± — | 2864.6 ± — | 1/1 | 12.6 | 100% | 25% | 33% | 0% |
| Lightweight | FP8_A8 | Short | complete | 1/1 | 256 / 25.0 | 0.57 | 0.673 ± — | 500.5 ± — | 1/1 | 37.2 | 100% | 33% | 0% | 0% |
| Lightweight | FP8_A8 | Medium | complete | 1/1 | 992 / 96.0 | 0.57 | 1.818 ± — | 1013.1 ± — | 1/1 | 52.8 | 0% | 0% | 0% | 0% |
| Lightweight | FP8_A8 | Long | complete | 1/1 | 4065 / 44.0 | 0.57 | 5.692 ± — | 5116.7 ± — | 1/1 | 7.7 | 0% | 0% | 0% | 0% |
| Medium | FP32 | Short | complete | 1/1 | 256 / 22.0 | 6.41 | 5.113 ± — | 2593.0 ± — | 1/1 | 4.3 | 100% | 33% | 0% | 0% |
| Medium | FP32 | Medium | complete | 1/1 | 992 / 96.0 | 6.41 | 7.792 ± — | 2572.6 ± — | 1/1 | 12.3 | 0% | 0% | 0% | 0% |
| Medium | FP32 | Long | complete | 1/1 | 4065 / 37.0 | 6.41 | 25.248 ± — | 22345.7 ± — | 1/1 | 1.5 | 100% | 0% | 0% | 0% |
| Medium | BF16 | Short | complete | 1/1 | 256 / 22.0 | 3.20 | 0.859 ± — | 332.7 ± — | 1/1 | 25.6 | 100% | 33% | 0% | 0% |
| Medium | BF16 | Medium | complete | 1/1 | 992 / 96.0 | 3.20 | 3.366 ± — | 920.3 ± — | 1/1 | 28.5 | 0% | 0% | 0% | 0% |
| Medium | BF16 | Long | complete | 1/1 | 4065 / 37.0 | 3.20 | 5.835 ± — | 4712.8 ± — | 1/1 | 6.3 | 100% | 0% | 0% | 0% |
| Medium | FP8 | Short | complete | 1/1 | 256 / 22.0 | 1.65 | 0.670 ± — | 358.3 ± — | 1/1 | 32.9 | 100% | 67% | 50% | 0% |
| Medium | FP8 | Medium | complete | 1/1 | 992 / 42.0 | 1.65 | 1.863 ± — | 1238.1 ± — | 1/1 | 22.5 | 100% | 0% | 0% | 0% |
| Medium | FP8 | Long | complete | 1/1 | 4065 / 38.0 | 1.65 | 6.921 ± — | 6162.5 ± — | 1/1 | 5.5 | 100% | 0% | 0% | 0% |
| Medium | INT4 | Short | complete | 1/1 | 256 / 22.0 | 0.90 | 0.575 ± — | 356.9 ± — | 1/1 | 38.3 | 100% | 67% | 50% | 0% |
| Medium | INT4 | Medium | complete | 1/1 | 992 / 70.0 | 0.90 | 1.910 ± — | 1167.3 ± — | 1/1 | 36.6 | 0% | 0% | 0% | 0% |
| Medium | INT4 | Long | complete | 1/1 | 4065 / 38.0 | 0.90 | 6.455 ± — | 5835.9 ± — | 1/1 | 5.9 | 100% | 0% | 0% | 0% |
| Medium | FP8_A8 | Short | complete | 1/1 | 256 / 22.0 | 1.65 | 1.197 ± — | 880.2 ± — | 1/1 | 18.4 | 100% | 67% | 50% | 0% |
| Medium | FP8_A8 | Medium | complete | 1/1 | 992 / 40.0 | 1.65 | 4.588 ± — | 3903.0 ± — | 1/1 | 8.7 | 100% | 0% | 0% | 0% |
| Medium | FP8_A8 | Long | complete | 1/1 | 4065 / 39.0 | 1.65 | 18.000 ± — | 17120.4 ± — | 1/1 | 2.2 | 100% | 25% | 0% | 0% |
| Complex | FP32 | Short | skipped | 0/1 | 256 / — | — | — | — | — | — | — | — | — | — |
| Complex | FP32 | Medium | skipped | 0/1 | 992 / — | — | — | — | — | — | — | — | — | — |
| Complex | FP32 | Long | skipped | 0/1 | 4065 / — | — | — | — | — | — | — | — | — | — |
| Complex | BF16 | Short | complete | 1/1 | 256 / 55.0 | 7.49 | 23.364 ± — | 6423.4 ± — | 1/1 | 2.4 | 0% | 0% | 0% | 0% |
| Complex | BF16 | Medium | complete | 1/1 | 992 / 41.0 | 7.49 | 9.341 ± — | 4027.6 ± — | 1/1 | 4.4 | 100% | 50% | 33% | 0% |
| Complex | BF16 | Long | complete | 1/1 | 4065 / 40.0 | 7.49 | 33.159 ± — | 18704.0 ± — | 1/1 | 1.2 | 100% | 50% | 33% | 0% |
| Complex | FP8 | Short | complete | 1/1 | 256 / 55.0 | 3.86 | 2.509 ± — | 853.1 ± — | 1/1 | 21.9 | 0% | 0% | 0% | 0% |
| Complex | FP8 | Medium | complete | 1/1 | 992 / 51.0 | 3.86 | 4.815 ± — | 3132.1 ± — | 1/1 | 10.6 | 0% | 0% | 0% | 0% |
| Complex | FP8 | Long | complete | 1/1 | 4065 / 41.0 | 3.86 | 17.911 ± — | 16004.1 ± — | 1/1 | 2.3 | 100% | 75% | 67% | 0% |
| Complex | INT4 | Short | complete | 1/1 | 256 / 55.0 | 2.11 | 1.885 ± — | 822.8 ± — | 1/1 | 29.2 | 0% | 0% | 0% | 0% |
| Complex | INT4 | Medium | complete | 1/1 | 992 / 40.0 | 2.11 | 3.868 ± — | 2978.2 ± — | 1/1 | 10.3 | 100% | 0% | 0% | 0% |
| Complex | INT4 | Long | complete | 1/1 | 4065 / 38.0 | 2.11 | 16.031 ± — | 14747.8 ± — | 1/1 | 2.4 | 100% | 25% | 0% | 0% |
| Complex | FP8_A8 | Short | complete | 1/1 | 256 / 55.0 | 3.86 | 3.791 ± — | 2161.2 ± — | 1/1 | 14.5 | 0% | 0% | 0% | 0% |
| Complex | FP8_A8 | Medium | complete | 1/1 | 992 / 41.0 | 3.86 | 9.834 ± — | 8468.5 ± — | 1/1 | 4.2 | 100% | 50% | 33% | 0% |
| Complex | FP8_A8 | Long | complete | 1/1 | 4065 / 40.0 | 3.86 | 42.821 ± — | 40937.9 ± — | 1/1 | 0.9 | 100% | 50% | 33% | 0% |

Tokens/s means generated output tokens divided by the full request time, including input prefill, decode and API overhead. It is not decode-only speed. Compare latency together with output length; longer or incorrect responses can distort output tokens/s.

TTFT (time to first token) is engine request arrival to the first generated token reaching the engine frontend, including queueing and prefill. It excludes model setup, subsequent decoding and HTTP/network transport. The table shows arithmetic mean ± sample SD in milliseconds; JSON/CSV timings remain in seconds. TTFT measured / completed shows coverage. Missing metrics are unavailable and excluded from TTFT averages; total request latency cannot be used to reconstruct them.

Output limit: 96 tokens per request. 3 returned responses reached this limit. Truncated answers are retained and graded as returned; they are included in the reported answer pass rates.

Thinking is disabled by default for Qwen3. Models use the same task builders and context budgets; exact prompts, token counts and per-model reference answers are saved. FP32 comparisons stay within each model. A skipped FP32 baseline leaves speedup empty.

Accuracy compares JSON fields with each task's configured reference. JSON fences are accepted; JSON types must match exactly. Extra keys and string case follow each task's comparison options. Expected fields must always be present. Reasoning fields are selected in the task's expectation file and are also scored separately in the raw field results. Invalid JSON prevents field scoring. Per-field rates use successful requests; full-answer/JSON rates count all generation attempts. Greedy repetitions measure timing variability, not independent examples or cross-validation. These tasks cannot establish general model quality or a monotonic relationship between model size and correctness.

Metal FP8 is MXFP8 weight storage with BF16 inputs; INT4 uses affine weights with BF16 inputs. FP32 is cast from the same BF16 source checkpoint; it cannot recover training precision. Unsupported or oversized cases have no fabricated timing or accuracy.

## Fixed FP8 weights: activation comparison

FP8 uses BF16 activations. FP8_A8 rounds quantized projection inputs to MXFP8 with mx.qqmm, then computes with BF16 buffers. A quantized tied output head also receives rounding. This is a quantize/dequantize experiment, not native FP8 arithmetic or persistent FP8 activation storage. Embedding lookups, attention and the KV cache retain BF16 behavior.

Both cases reuse one FP8 checkpoint, the same prompt token IDs, BF16 KV dtype, cache block size/count, generation settings and rotating trial schedule. Verified pairs check checkpoint/cache/settings identity, prompt hashes, token counts and reference answers. Sequential engine runs can still differ due to system load and compilation; means include first-request work.

| Model/tier | Context | Case | Completed | Verified pairs | Mean latency s | Mean TTFT ms | TTFT coverage | Mean field accuracy | Answer pass | Mean MLX peak MiB | Peak coverage | Mean engine RSS after MiB | RSS coverage |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Lightweight | Short | FP8 / BF16 activations | 1/1 | 1 | 0.309 | 141.371 | 1/1 | 33.333% | 0.000% | 1477.320 | 1/1 | 1757.312 | 1/1 |
| Lightweight | Short | FP8_A8 / FP8-rounded activations | 1/1 | 1 | 0.673 | 500.488 | 1/1 | 33.333% | 0.000% | 1485.521 | 1/1 | 1733.047 | 1/1 |
| Lightweight | Medium | FP8 / BF16 activations | 1/1 | 1 | 0.966 | 474.430 | 1/1 | 0.000% | 0.000% | 1627.023 | 1/1 | 1680.625 | 1/1 |
| Lightweight | Medium | FP8_A8 / FP8-rounded activations | 1/1 | 1 | 1.818 | 1013.068 | 1/1 | 0.000% | 0.000% | 1636.023 | 1/1 | 1485.562 | 1/1 |
| Lightweight | Long | FP8 / BF16 activations | 1/1 | 1 | 3.435 | 2959.794 | 1/1 | 0.000% | 0.000% | 1627.795 | 1/1 | 1330.484 | 1/1 |
| Lightweight | Long | FP8_A8 / FP8-rounded activations | 1/1 | 1 | 5.692 | 5116.683 | 1/1 | 0.000% | 0.000% | 1636.023 | 1/1 | 1243.891 | 1/1 |
| Medium | Short | FP8 / BF16 activations | 1/1 | 1 | 0.670 | 358.281 | 1/1 | 66.667% | 0.000% | 2552.522 | 1/1 | 2404.625 | 1/1 |
| Medium | Short | FP8_A8 / FP8-rounded activations | 1/1 | 1 | 1.197 | 880.151 | 1/1 | 66.667% | 0.000% | 2581.522 | 1/1 | 2527.281 | 1/1 |
| Medium | Medium | FP8 / BF16 activations | 1/1 | 1 | 1.863 | 1238.148 | 1/1 | 0.000% | 0.000% | 2630.056 | 1/1 | 2109.594 | 1/1 |
| Medium | Medium | FP8_A8 / FP8-rounded activations | 1/1 | 1 | 4.588 | 3902.985 | 1/1 | 0.000% | 0.000% | 2674.056 | 1/1 | 2253.328 | 1/1 |
| Medium | Long | FP8 / BF16 activations | 1/1 | 1 | 6.921 | 6162.531 | 1/1 | 0.000% | 0.000% | 2630.056 | 1/1 | 2021.188 | 1/1 |
| Medium | Long | FP8_A8 / FP8-rounded activations | 1/1 | 1 | 18.000 | 17120.437 | 1/1 | 25.000% | 0.000% | 2674.057 | 1/1 | 2250.656 | 1/1 |
| Complex | Short | FP8 / BF16 activations | 1/1 | 1 | 2.509 | 853.125 | 1/1 | 0.000% | 0.000% | 4930.785 | 1/1 | 4420.906 | 1/1 |
| Complex | Short | FP8_A8 / FP8-rounded activations | 1/1 | 1 | 3.791 | 2161.213 | 1/1 | 0.000% | 0.000% | 4958.285 | 1/1 | 4218.141 | 1/1 |
| Complex | Medium | FP8 / BF16 activations | 1/1 | 1 | 4.815 | 3132.084 | 1/1 | 0.000% | 0.000% | 5082.039 | 1/1 | 4411.625 | 1/1 |
| Complex | Medium | FP8_A8 / FP8-rounded activations | 1/1 | 1 | 9.834 | 8468.461 | 1/1 | 50.000% | 0.000% | 5115.289 | 1/1 | 4203.219 | 1/1 |
| Complex | Long | FP8 / BF16 activations | 1/1 | 1 | 17.911 | 16004.053 | 1/1 | 75.000% | 0.000% | 5084.899 | 1/1 | 4402.859 | 1/1 |
| Complex | Long | FP8_A8 / FP8-rounded activations | 1/1 | 1 | 42.821 | 40937.888 | 1/1 | 50.000% | 0.000% | 5115.290 | 1/1 | 4191.547 | 1/1 |

MLX peak is the engine's tracked active allocation peak, reset before each request; it includes weights and KV allocations, and excludes allocator cache and allocations outside MLX. Extra peak above the pre-request active allocation is also saved. Engine RSS is a post-request resident-memory snapshot, not a sampled request peak. Its saved high-water mark is cumulative. These scopes overlap and must not be added. Memory RPCs and counter reset are outside TTFT and latency timing; missing measurements stay unavailable with explicit coverage. No activation-memory saving is assumed.

Detailed metrics, sample deviations, coverage and verified-pair counts: `activation_comparison.json` / `activation_comparison.csv`.

## Outputs and evidence

- [Lightweight individual outputs, means and engine warnings](lightweight/comparison.md), [complete prompts](lightweight/prompts.md), [model card](https://huggingface.co/models/7b50efe10ce32606/BF16). Resolved source: `local:models/7b50efe10ce32606/BF16`.
- [Medium individual outputs, means and engine warnings](medium/comparison.md), [complete prompts](medium/prompts.md), [model card](https://huggingface.co/models/7ec86880db931fb2/BF16). Resolved source: `local:models/7ec86880db931fb2/BF16`.
- [Complex individual outputs, means and engine warnings](complex/comparison.md), [complete prompts](complex/prompts.md), [model card](https://huggingface.co/models/e15b00bc84c6b5ee/BF16). Resolved source: `local:models/e15b00bc84c6b5ee/BF16`.

Raw trials: `suite_trials.csv` / `suite_results.json`. Aggregated cells: `suite_summary.csv`. Per-model folders retain checkpoint audits, prompts, job specifications, engine logs and all generated answers.

The installed backend logged segmentation faults during engine teardown after saving completed results for: Complex/FP8, Complex/FP8_A8, Complex/INT4, Lightweight/BF16, Lightweight/FP32, Lightweight/FP8, Lightweight/FP8_A8, Lightweight/INT4, Medium/BF16, Medium/FP8, Medium/FP8_A8, Medium/INT4. These timings exclude teardown; clean shutdown is not verified.
