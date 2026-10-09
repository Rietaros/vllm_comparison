# One-repeat validation run: editable prompts and expected answers

Run on 2026-10-09 using **Apple M1 Pro, 16 GB unified memory, macOS 15.5**, and vLLM-Metal. NVIDIA inference was not run here.

**42 completed requests, 3 Complex/FP32 memory skips, 0 failed cases.** One generation per model/precision/context, with 256 / 1,024 / 4,096-token input budgets and a 96-token output limit. Selected formats: FP32, BF16, FP8, INT4, and FP8_A8. The planning budget was 10 GiB.

- [Full comparison and answers](comparison.md)
- [FP8 activation comparison](activation_comparison.md)
- [All-model summary CSV](suite_summary.csv)
- [Activation CSV](activation_comparison.csv) and [JSON](activation_comparison.json)
- [Verification and resolved expected answers](verification.json)

This run uses the default generated Markdown prompts and their new JSON expectation files. References were independently recalculated from the fitted task data. All 42 requests have valid TTFT; all nine activation pairs share prompts, expected answers, scoring rules, and fixed FP8 checkpoint/cache/settings contracts.

The Hugging Face download stalled, so this run used existing **local unquantized BF16 conversions** of the configured Qwen3 models. The default `config.json` was unchanged. Original model IDs and source revisions recorded by those conversions:

| Tier | Model | Original source revision |
|---|---|---|
| lightweight | Qwen/Qwen3-0.6B | `c1899de289a04d12100db370d81485cdf75e47ca` |
| medium | Qwen/Qwen3-1.7B | `70d244cc86ccca08cf5af4e1e306ecf908b1ad5e` |
| complex | Qwen/Qwen3-4B | `1cfa9a7208912126459214e8b04321603b3df60c` |

The local source folders are recorded in `verification.json`; weights are excluded from Git. Newly prepared precision variants were derived from those local BF16 sources. The initial lightweight FP32 engine failed before generation because the combined run pinned BF16 cache on FP32. After fixing the cache selection, resume generated only its three unattempted answers; all existing answers were preserved.

This is an execution check with one sample per case. Standard deviation is unavailable, and these timings are insufficient for a stable performance ranking. The first request and any lazy kernel work are included. FP8_A8 applies rounding with BF16 buffers, without native FP8 activation storage.

The Metal backend logged teardown segmentation faults after saving outputs for Complex/FP8, Complex/FP8_A8, Complex/INT4, Lightweight/BF16, Lightweight/FP32, Lightweight/FP8, Lightweight/FP8_A8, Lightweight/INT4, Medium/BF16, Medium/FP8, Medium/FP8_A8, Medium/INT4. The reports retain these warnings; clean teardown is not verified.

To run the same matrix from downloaded configured models:

```sh
.venv/bin/python compare_models.py --backend metal \
  --precisions FP32 BF16 FP8 INT4 FP8_A8 --memory-budget-gib 10 \
  --repeats 1 --timeout 1200 --output-dir results/my-modular-run
```

On NVIDIA, use `.venv-cuda/bin/python`, `--backend cuda`, and `--memory-fraction 0.8` instead of the absolute memory budget. Follow the [main README](../../../README.md) for installation and custom prompt/answer editing.
