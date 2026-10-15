# Comparison results: diverse math and understanding Q&A prompts

Run date: **2026-10-15**, Asia/Jakarta. Summary generated: 2026-10-15 05:22 WIB.

**420 completed generations, 30 memory skips, and 0 failed trials out of 450 requested slots.** This is a fresh measurement of the 30-topic dataset, with five math and five understanding Q&A cases in each of Short, Medium, and Long.

## Main findings

- **Qwen/Qwen3-0.6B:** highest full-answer pass rate was 16.7% (5/30), achieved by FP32, BF16. INT4 had the lowest mean request latency at 0.446 s across the same 30 cases.
- **Qwen/Qwen3-1.7B:** highest full-answer pass rate was 33.3% (10/30), achieved by FP8. INT4 had the lowest mean request latency at 0.959 s across the same 30 cases.
- **Qwen/Qwen3-4B:** highest full-answer pass rate was 43.3% (13/30), achieved by FP8, FP8_A8. INT4 had the lowest mean request latency at 2.409 s across the same 30 cases.
- **Qwen/Qwen3-4B / FP32 was skipped:** Estimated weights + KV + runtime reserve = 16.49 GiB; configured unified RAM budget = 10.00 GiB. No latency or accuracy was assigned to these slots.

These are observations on this small synthetic dataset. Lowest latency and highest answer accuracy may come from different formats; request latency also reflects the length of the generated answer.

## Models and measurement settings

Apple M1 Pro, 16 GiB unified RAM, Darwin 15.5. Backend: vLLM-Metal.

| Tier | Model | Cached source revision |
|---|---|---|
| Lightweight | Qwen/Qwen3-0.6B | `c1899de289a04d12100db370d81485cdf75e47ca` |
| Medium | Qwen/Qwen3-1.7B | `70d244cc86ccca08cf5af4e1e306ecf908b1ad5e` |
| Complex | Qwen/Qwen3-4B | `1cfa9a7208912126459214e8b04321603b3df60c` |

- Formats: FP32, BF16, FP8, INT4, and FP8_A8. The FP8_A8 case holds FP8 weights fixed and rounds projection inputs to FP8.
- Metal FP32 uses an FP32 model and matching FP32 KV cache. BF16 uses BF16 weights; FP8 uses MXFP8 weights and INT4 uses affine INT4 weights. The latter three use BF16 activations and KV cache; FP8_A8 adds activation rounding with BF16 buffers.
- Input budgets: 256 / 1,024 / 4,096 tokens; actual ranges: 134–167 / 376–425 / 997–1,416 tokens, including chat formatting.
- Ten distinct cases per context and format; one generation per case. Math cases are `01`–`05`; understanding Q&A cases are `06`–`10`. The [topic table](prompts/README.md) lists all 30 use cases.
- Batch size 1, temperature 0, seed 42, thinking disabled, prefix caching disabled, output limit 96 tokens, planning budget 10 GiB.
- Each precision loads its engine separately. Context order rotates between trial rounds, and every format/model receives identical prompt token IDs and typed references.
- Timings exclude model download, checkpoint conversion, engine loading, and engine teardown. They include the first measured request; no additional benchmark warm-up is used.

## Overall results and math versus Q&A accuracy

All means below pool the 30 cases equally. Math and Q&A each have 15 cases across the three lengths. Full-answer pass requires all expected fields, exact JSON types, and the configured schema. Field accuracy is the mean fraction of correct fields per answer. Skipped formats have no accuracy or timing result.

| Model | Format | Completed | Full-answer pass | Math pass | Q&A pass | Field accuracy | JSON valid | Mean latency (s) | Mean TTFT (ms) | Mean TPS (tokens/s) | Mean output tokens | Saved weights (GiB) |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Qwen3-0.6B | FP32 | 30/30 | 5/30 (16.7%) | 0/15 (0.0%) | 5/15 (33.3%) | 34.7% | 73.3% | 1.370 | 781.1 | 34.2 | 34.6 | 2.220 |
| Qwen3-0.6B | BF16 | 30/30 | 5/30 (16.7%) | 0/15 (0.0%) | 5/15 (33.3%) | 34.7% | 73.3% | 0.604 | 237.7 | 62.7 | 35.0 | 1.110 |
| Qwen3-0.6B | FP8 | 30/30 | 3/30 (10.0%) | 0/15 (0.0%) | 3/15 (20.0%) | 29.2% | 73.3% | 0.565 | 288.3 | 77.8 | 38.1 | 0.573 |
| Qwen3-0.6B | INT4 | 30/30 | 2/30 (6.7%) | 0/15 (0.0%) | 2/15 (13.3%) | 29.4% | 90.0% | 0.446 | 268.0 | 78.2 | 29.3 | 0.312 |
| Qwen3-0.6B | FP8_A8 | 30/30 | 4/30 (13.3%) | 0/15 (0.0%) | 4/15 (26.7%) | 30.6% | 66.7% | 0.890 | 583.7 | 54.5 | 39.3 | 0.573 |
| Qwen3-1.7B | FP32 | 30/30 | 9/30 (30.0%) | 0/15 (0.0%) | 9/15 (60.0%) | 51.4% | 76.7% | 2.488 | 1209.5 | 12.9 | 28.4 | 6.410 |
| Qwen3-1.7B | BF16 | 30/30 | 9/30 (30.0%) | 0/15 (0.0%) | 9/15 (60.0%) | 48.6% | 70.0% | 1.276 | 566.7 | 23.9 | 29.2 | 3.205 |
| Qwen3-1.7B | FP8 | 30/30 | 10/30 (33.3%) | 0/15 (0.0%) | 10/15 (66.7%) | 47.2% | 70.0% | 1.179 | 721.5 | 30.8 | 32.9 | 1.653 |
| Qwen3-1.7B | INT4 | 30/30 | 7/30 (23.3%) | 0/15 (0.0%) | 7/15 (46.7%) | 49.7% | 80.0% | 0.959 | 678.6 | 35.8 | 29.2 | 0.902 |
| Qwen3-1.7B | FP8_A8 | 30/30 | 8/30 (26.7%) | 0/15 (0.0%) | 8/15 (53.3%) | 47.2% | 73.3% | 2.332 | 1879.1 | 17.8 | 31.9 | 1.653 |
| Qwen3-4B | FP32 | 0/30 | — | — | — | — | — | — | — | — | — | — |
| Qwen3-4B | BF16 | 30/30 | 11/30 (36.7%) | 1/15 (6.7%) | 10/15 (66.7%) | 57.2% | 83.3% | 3.154 | 1431.9 | 10.5 | 32.1 | 7.492 |
| Qwen3-4B | FP8 | 30/30 | 13/30 (43.3%) | 3/15 (20.0%) | 10/15 (66.7%) | 59.4% | 83.3% | 3.338 | 2265.0 | 11.7 | 33.0 | 3.863 |
| Qwen3-4B | INT4 | 30/30 | 10/30 (33.3%) | 1/15 (6.7%) | 9/15 (60.0%) | 54.4% | 80.0% | 2.409 | 1787.5 | 15.7 | 31.4 | 2.108 |
| Qwen3-4B | FP8_A8 | 30/30 | 13/30 (43.3%) | 2/15 (13.3%) | 11/15 (73.3%) | 59.4% | 86.7% | 5.976 | 5044.2 | 6.5 | 30.1 | 3.863 |

TTFT is engine request arrival to the first generated token, including queueing and prefill. Latency covers the complete request, including decoding. Saved weights describe tensor payload, not total engine memory.

TPS (tokens per second) measures generated output tokens divided by the full request latency, including prompt prefill, decoding, and API overhead. The tables report the arithmetic mean of per-request TPS (`mean(output_tokens / generation_s)`); this gives each case equal weight. Input tokens are excluded from the numerator. Model loading, conversion, and teardown are excluded from the timed request. Higher TPS means higher measured output throughput; compare it with accuracy and output length.

Representative arithmetic failures show why full-answer pass is stricter than recognizing the intended calculation:

**Qwen/Qwen3-0.6B / FP32 / `short-04` (garden area).** Expected: `{"garden_area": 84, "planted_area": 78}`. Returned:

````text
```json
{"garden_area": 12 * 7, "planted_area": 12 * 7 - 3 * 2}
```
````

**Qwen/Qwen3-1.7B / FP32 / `short-04` (garden area).** Expected: `{"garden_area": 84, "planted_area": 78}`. Returned:

````text
{"garden_area": 84, "planted_area": 60}
````

Unevaluated arithmetic expressions are invalid JSON and cannot receive field credit. A valid JSON object with a wrong numerical result can receive partial field credit while failing the complete answer. The benchmark records both outcomes without repairing the response.

## Results by prompt length

Each length has ten cases: five math and five understanding Q&A. Values after ± are sample standard deviations across different cases, including different answer lengths; they do not estimate repeatability for one fixed prompt.

| Model | Format | Short pass | Short latency (s) | Short TPS | Medium pass | Medium latency (s) | Medium TPS | Long pass | Long latency (s) | Long TPS |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Qwen3-0.6B | FP32 | 2/10 | 0.491 ± 0.147 | 49.0 ± 3.4 | 2/10 | 0.851 ± 0.259 | 37.0 ± 3.7 | 1/10 | 2.769 ± 0.851 | 16.4 ± 3.5 |
| Qwen3-0.6B | BF16 | 2/10 | 0.302 ± 0.079 | 78.4 ± 7.5 | 2/10 | 0.509 ± 0.195 | 64.6 ± 5.4 | 1/10 | 1.001 ± 0.324 | 45.2 ± 7.4 |
| Qwen3-0.6B | FP8 | 1/10 | 0.243 ± 0.055 | 104.2 ± 9.6 | 1/10 | 0.500 ± 0.165 | 82.2 ± 11.9 | 1/10 | 0.952 ± 0.201 | 47.0 ± 9.7 |
| Qwen3-0.6B | INT4 | 1/10 | 0.211 ± 0.036 | 107.0 ± 9.8 | 0/10 | 0.340 ± 0.028 | 80.0 ± 5.6 | 1/10 | 0.788 ± 0.137 | 47.6 ± 8.2 |
| Qwen3-0.6B | FP8_A8 | 2/10 | 0.318 ± 0.057 | 78.0 ± 12.3 | 1/10 | 0.719 ± 0.159 | 54.9 ± 15.1 | 1/10 | 1.632 ± 0.308 | 30.5 ± 7.3 |
| Qwen3-1.7B | FP32 | 2/10 | 0.977 ± 0.210 | 16.3 ± 1.9 | 4/10 | 1.989 ± 0.724 | 14.3 ± 1.9 | 3/10 | 4.497 ± 1.652 | 8.1 ± 2.8 |
| Qwen3-1.7B | BF16 | 2/10 | 0.625 ± 0.243 | 28.9 ± 3.2 | 4/10 | 1.101 ± 0.403 | 25.7 ± 3.5 | 3/10 | 2.103 ± 0.826 | 17.2 ± 5.2 |
| Qwen3-1.7B | FP8 | 2/10 | 0.445 ± 0.129 | 39.7 ± 6.2 | 4/10 | 1.083 ± 0.404 | 35.0 ± 10.9 | 4/10 | 2.010 ± 0.524 | 17.7 ± 7.4 |
| Qwen3-1.7B | INT4 | 2/10 | 0.340 ± 0.061 | 47.5 ± 9.5 | 2/10 | 0.758 ± 0.172 | 38.5 ± 10.4 | 3/10 | 1.781 ± 0.397 | 21.4 ± 7.5 |
| Qwen3-1.7B | FP8_A8 | 2/10 | 0.660 ± 0.058 | 25.2 ± 4.2 | 3/10 | 1.860 ± 0.425 | 19.9 ± 8.7 | 3/10 | 4.476 ± 0.807 | 8.2 ± 3.8 |
| Qwen3-4B | FP32 | — | — | — | — | — | — | — | — | — |
| Qwen3-4B | BF16 | 4/10 | 1.293 ± 0.338 | 12.1 ± 1.5 | 3/10 | 2.570 ± 1.041 | 11.1 ± 1.9 | 4/10 | 5.600 ± 2.085 | 8.3 ± 2.1 |
| Qwen3-4B | FP8 | 4/10 | 1.153 ± 0.371 | 15.3 ± 2.9 | 5/10 | 2.689 ± 1.005 | 13.0 ± 5.5 | 4/10 | 6.171 ± 1.950 | 6.8 ± 1.9 |
| Qwen3-4B | INT4 | 3/10 | 0.781 ± 0.160 | 21.1 ± 4.7 | 3/10 | 1.756 ± 0.417 | 17.0 ± 6.3 | 4/10 | 4.690 ± 1.264 | 9.0 ± 3.0 |
| Qwen3-4B | FP8_A8 | 4/10 | 1.570 ± 0.228 | 9.2 ± 1.8 | 5/10 | 4.352 ± 0.630 | 6.6 ± 2.7 | 4/10 | 12.005 ± 1.933 | 3.6 ± 1.4 |

Different lengths also use different topics and difficulty levels. Differences across these columns cannot isolate context length as the cause.

## Fixed FP8 weights: effect of activation rounding

Each row pools 30 verified paired cases for a model. TPS columns use the same mean per-request definition as the overall table. FP8 uses BF16 projection inputs; FP8_A8 rounds those inputs through MXFP8 while retaining BF16 buffers. Both formats reuse the same FP8 checkpoint and BF16 KV-cache settings. This experiment measures rounding effects and overhead; it does not provide persistent FP8 activation storage or native FP8 arithmetic.

| Model | Verified pairs | FP8 pass | FP8_A8 pass | Pass-rate change (pp) | FP8 latency (s) | FP8_A8 latency (s) | FP8 TPS | FP8_A8 TPS | Latency change | FP8 mean MLX peak (MiB) | FP8_A8 mean MLX peak (MiB) |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Qwen3-0.6B | 30 | 3/30 (10.0%) | 4/30 (13.3%) | +3.3 | 0.565 | 0.890 | 77.8 | 54.5 | +57.4% | 1301.6 | 1335.7 |
| Qwen3-1.7B | 30 | 10/30 (33.3%) | 8/30 (26.7%) | -6.7 | 1.179 | 2.332 | 30.8 | 17.8 | +97.7% | 2382.6 | 2425.4 |
| Qwen3-4B | 30 | 13/30 (43.3%) | 13/30 (43.3%) | +0.0 | 3.338 | 5.976 | 11.7 | 6.5 | +79.0% | 4636.3 | 4666.2 |

MLX peak is a per-request engine allocator peak and includes persistent allocations; it is not additional activation storage or total system RAM. Memory counters overlap and must not be added. Sequential runs can differ due to compilation, first-request work, and concurrent system load.

## Validation and limits

- Verified all 450 unique model/format/context/trial slots, with 420 actual single-generation completions, 30 explicit skips, and no failed trials.
- TTFT coverage: 420/420 completed requests. FP8 activation contracts: 90/90 successful pairs verified.
- Recomputed TPS from output token counts and full request latency for all 420 completed requests, and checked the reported mean TPS and per-context sample deviations.
- Recomputed every configured answer score and checked stored token counts/hashes, typed expectation hashes, context budgets, per-context means, sample deviations, case identities, and consistent prompts/answers across models.
- Independently checked all 15 arithmetic references against the rendered inputs and all 15 comprehension references against the reviewed passages. Every format/model retains the 5/5 split in each length.
- 14 completed responses reached the 96-token output limit. Responses are graded exactly as returned, including truncation.
- Strict string case and JSON schema affect full-answer pass: a mathematically correct value can still fail if the answer uses the wrong key, extra fields, an incorrect type, or a different required phrase.
- FP32 was cast from the same cached BF16 source as the other formats; this cannot restore precision absent from the source checkpoint.
- These are local Apple Metal results. NVIDIA performance and native CUDA FP8 behavior were not measured.
- The installed backend reported segmentation faults during teardown **after completed results were saved** for: Complex/BF16, Complex/FP8, Complex/FP8_A8, Complex/INT4, Lightweight/BF16, Lightweight/FP32, Lightweight/FP8, Lightweight/FP8_A8, Lightweight/INT4, Medium/BF16, Medium/FP32, Medium/FP8, Medium/FP8_A8, Medium/INT4. These warnings remain in the raw logs; clean shutdown is not verified. Request timings exclude teardown.

## Reproduce and inspect

Run from this repository on the same Apple Metal environment with the existing local BF16 sources:

```sh
.venv/bin/python compare_models.py --backend metal \
  --models models/7b50efe10ce32606/BF16 models/7ec86880db931fb2/BF16 models/e15b00bc84c6b5ee/BF16 \
  --precisions FP32 BF16 FP8 INT4 FP8_A8 --memory-budget-gib 10 \
  --repeats 10 --thinking off --timeout 1200 \
  --output-dir results/diverse-topics-comparison-20261015
```

Use a fresh output directory for a new measurement. On a fresh clone, omit `--models` to use the same Qwen3 model IDs from [config.json](config.json); the local source folders above are cached weights and are not tracked in Git.

Raw artifacts are retained locally in `results/diverse-topics-comparison-20261015/`: `suite_results.json`, `suite_trials.csv`, `suite_summary.csv`, `activation_comparison.json`, and per-model prompts, reports, checkpoint audits, and engine logs. The `results/` folder is ignored by Git; this commit publishes the requested summary in `output.md`.

Software versions: `{"mlx": "0.32.1", "mlx-lm": "0.32.0", "torch": "2.13.0", "transformers": "5.19.0", "vllm": "0.30.0+cpu", "vllm-metal": "0.30.0"}`.

Code/dataset revision: `eb1652d` (`diverse-math-qna-cases-v6`). Local dataset identity SHA-256: `b71495790f54ffc84a0bf7df324ea3f22e6e3384a4b1b9f1eb3264c30859ed5b`. This run hash includes absolute asset paths and will differ in another checkout.
