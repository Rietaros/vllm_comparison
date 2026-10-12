# Ten different cases per context: comparison output

Run date: **2026-10-12**. Hardware: Apple M1 Pro, 16 GiB unified RAM, Darwin 15.5. Backend: vLLM-Metal.

**420 completed generations, 30 memory-skipped slots, 0 failed cases.** Each precision/model evaluates 10 different Short, Medium, and Long question/answer pairs: 30 distinct dataset cases, answered once per format/model. Input budgets are 256 / 1,024 / 4,096 tokens; output limit is 96 tokens. The planning budget is 10 GiB.

- [Full comparison and individual model answers](comparison.md)
- [Fixed FP8 activation comparison](activation_comparison.md)
- [Summary CSV](suite_summary.csv) and [all individual trials](trials.csv)
- [Activation CSV](activation_comparison.csv) and [JSON](activation_comparison.json)
- [Verification, case IDs, and expected answers](verification.json)

420 successful requests have measured TTFT. All 90 FP8/FP8_A8 pairs have verified matching case IDs, token inputs, expected answers, comparison rules, and checkpoint/cache/settings contracts. References are retained per trial, and aggregate statistics were recomputed from the individual measurements.

The `output` column in `trials.csv` is a JSON-encoded string, preserving the exact response including newlines and trailing spaces. Decode it with `json.loads(row["output"])` in Python. Markdown reports show readable answers.

The run used the existing local dense BF16 source copies recorded below, avoiding another model download. New requests used the editable Markdown/JSON case bank; model choices in `config.json` were unchanged.

| Tier | Model | Source revision |
|---|---|---|
| lightweight | Qwen/Qwen3-0.6B | `c1899de289a04d12100db370d81485cdf75e47ca` |
| medium | Qwen/Qwen3-1.7B | `70d244cc86ccca08cf5af4e1e306ecf908b1ad5e` |
| complex | Qwen/Qwen3-4B | `1cfa9a7208912126459214e8b04321603b3df60c` |

Accuracy covers this synthetic dataset. Timing deviations include case differences, output lengths, system load, and first-request initialization work. FP8_A8 applies FP8 rounding with BF16 buffers rather than native FP8 activation storage. GPU memory counters overlap and must not be added. This run used Apple Silicon; NVIDIA inference was not performed here.

The backend logged teardown segmentation faults after saving results for Complex/BF16, Complex/FP8, Complex/FP8_A8, Complex/INT4, Lightweight/BF16, Lightweight/FP32, Lightweight/FP8, Lightweight/FP8_A8, Lightweight/INT4, Medium/BF16, Medium/FP8, Medium/FP8_A8, Medium/INT4. Warnings are retained in the reports; clean teardown is not verified.

Edit [the prompt and answer pairs](../../../prompts/README.md), then run all configured models on Apple Silicon:

```sh
.venv/bin/python compare_models.py --backend metal \
  --precisions FP32 BF16 FP8 INT4 FP8_A8 --memory-budget-gib 10 \
  --repeats 10 --timeout 3600 --output-dir results/my-distinct-cases
```

On NVIDIA, use `.venv-cuda/bin/python`, `--backend cuda`, and `--memory-fraction 0.8` instead of the absolute memory budget. See the [main README](../../../README.md) for setup.
