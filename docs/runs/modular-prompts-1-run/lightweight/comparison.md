# vLLM precision comparison: repeated-run averages

Model: `models/7b50efe10ce32606/BF16`; source: `local:models/7b50efe10ce32606/BF16`.
Hardware: Apple M1 Pro, 16 GiB unified RAM, Darwin 15.5. Backend: vLLM-Metal.

1 measured generations per precision/context (15 requested in total). Batch size 1; temperature 0; seed 42; prefix caching disabled.
Each round rotates context order; all precisions use the same schedule and the same token IDs. The model is loaded once per precision.
Means include the first measured request. No extra benchmark warm-up is added. Engine initialization/profile/warm-up passes are outside generation timing.
These are repeated measurements of fixed prompts, not cross-validation folds or independent accuracy examples. Greedy outputs may be identical across repeats.
Elapsed time includes prompt prefill, decoding, and API overhead; tokens/s is end-to-end output throughput.
Output limit: 96 tokens. 1 returned responses reached the limit; truncated answers are retained and graded as returned.
Model download, conversion, and engine loading are timed separately. First requests can include lazy kernel initialization.
Metal FP8 uses MXFP8 E4M3 weights with BF16 inputs; INT4 uses affine weights. This measures local Metal inference.
FP8_A8 applies activation quantize/dequantize rounding with BF16 buffers. Some tensors and reductions retain higher precision.
Weight size is the saved tensor payload, including scales and unquantized tensors; it is not total runtime memory.
Prepared Metal files are audited against their requested storage format.
RSS is the cumulative driver-process high-water mark, not the complete engine/GPU memory usage.

| Precision | Context | Status | Completed / requested | Input tokens | Mean seconds ± SD | Mean TTFT ms ± SD | TTFT measured / completed | Mean tokens/s | Weight MiB | Mean correct fields | Answer pass rate | Speedup vs FP32 |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| FP32 | Short | complete | 1 / 1 | 256 | 0.632 ± — | 214.8 ± — | 1/1 | 39.6 | 2273.8 | 33.3% | 0.0% | 1.00 |
| FP32 | Medium | complete | 1 / 1 | 992 | 2.244 ± — | 1494.6 ± — | 1/1 | 17.8 | 2273.8 | 0.0% | 0.0% | 1.00 |
| FP32 | Long | complete | 1 / 1 | 4065 | 20.740 ± — | 19634.2 ± — | 1/1 | 2.0 | 2273.8 | 25.0% | 0.0% | 1.00 |
| BF16 | Short | complete | 1 / 1 | 256 | 0.406 ± — | 140.4 ± — | 1/1 | 61.6 | 1136.9 | 33.3% | 0.0% | 1.56 |
| BF16 | Medium | complete | 1 / 1 | 992 | 0.847 ± — | 397.6 ± — | 1/1 | 47.3 | 1136.9 | 0.0% | 0.0% | 2.65 |
| BF16 | Long | complete | 1 / 1 | 4065 | 3.312 ± — | 2636.3 ± — | 1/1 | 12.7 | 1136.9 | 25.0% | 0.0% | 6.26 |
| FP8 | Short | complete | 1 / 1 | 256 | 0.309 ± — | 141.4 ± — | 1/1 | 80.9 | 586.3 | 33.3% | 0.0% | 2.04 |
| FP8 | Medium | complete | 1 / 1 | 992 | 0.966 ± — | 474.4 ± — | 1/1 | 63.2 | 586.3 | 0.0% | 0.0% | 2.32 |
| FP8 | Long | complete | 1 / 1 | 4065 | 3.435 ± — | 2959.8 ± — | 1/1 | 10.8 | 586.3 | 0.0% | 0.0% | 6.04 |
| INT4 | Short | complete | 1 / 1 | 256 | 0.297 ± — | 137.2 ± — | 1/1 | 84.2 | 319.8 | 33.3% | 0.0% | 2.13 |
| INT4 | Medium | complete | 1 / 1 | 992 | 0.750 ± — | 462.1 ± — | 1/1 | 54.7 | 319.8 | 0.0% | 0.0% | 2.99 |
| INT4 | Long | complete | 1 / 1 | 4065 | 3.346 ± — | 2864.6 ± — | 1/1 | 12.6 | 319.8 | 25.0% | 0.0% | 6.20 |
| FP8_A8 | Short | complete | 1 / 1 | 256 | 0.673 ± — | 500.5 ± — | 1/1 | 37.2 | 586.3 | 33.3% | 0.0% | 0.94 |
| FP8_A8 | Medium | complete | 1 / 1 | 992 | 1.818 ± — | 1013.1 ± — | 1/1 | 52.8 | 586.3 | 0.0% | 0.0% | 1.23 |
| FP8_A8 | Long | complete | 1 / 1 | 4065 | 5.692 ± — | 5116.7 ± — | 1/1 | 7.7 | 586.3 | 0.0% | 0.0% | 3.64 |

Observed runtime limitation: the installed vLLM/Metal stack logged a segmentation fault during engine shutdown for FP32, BF16, FP8, INT4, FP8_A8. Completed generation results were saved before shutdown. See the corresponding engine logs; a clean teardown is not verified.

## Fixed FP8 weights: activation comparison

FP8 uses BF16 activations. FP8_A8 rounds quantized projection inputs to MXFP8 with mx.qqmm, then computes with BF16 buffers. A quantized tied output head also receives rounding. This is a quantize/dequantize experiment, not native FP8 arithmetic or persistent FP8 activation storage. Embedding lookups, attention and the KV cache retain BF16 behavior.

Both cases reuse one FP8 checkpoint, the same prompt token IDs, BF16 KV dtype, cache block size/count, generation settings and rotating trial schedule. Verified pairs check checkpoint/cache/settings identity, prompt hashes, token counts and reference answers. Sequential engine runs can still differ due to system load and compilation; means include first-request work.

| Model/tier | Context | Case | Completed | Verified pairs | Mean latency s | Mean TTFT ms | TTFT coverage | Mean field accuracy | Answer pass | Mean MLX peak MiB | Peak coverage | Mean engine RSS after MiB | RSS coverage |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Single model | Short | FP8 / BF16 activations | 1/1 | 1 | 0.309 | 141.371 | 1/1 | 33.333% | 0.000% | 1477.320 | 1/1 | 1757.312 | 1/1 |
| Single model | Short | FP8_A8 / FP8-rounded activations | 1/1 | 1 | 0.673 | 500.488 | 1/1 | 33.333% | 0.000% | 1485.521 | 1/1 | 1733.047 | 1/1 |
| Single model | Medium | FP8 / BF16 activations | 1/1 | 1 | 0.966 | 474.430 | 1/1 | 0.000% | 0.000% | 1627.023 | 1/1 | 1680.625 | 1/1 |
| Single model | Medium | FP8_A8 / FP8-rounded activations | 1/1 | 1 | 1.818 | 1013.068 | 1/1 | 0.000% | 0.000% | 1636.023 | 1/1 | 1485.562 | 1/1 |
| Single model | Long | FP8 / BF16 activations | 1/1 | 1 | 3.435 | 2959.794 | 1/1 | 0.000% | 0.000% | 1627.795 | 1/1 | 1330.484 | 1/1 |
| Single model | Long | FP8_A8 / FP8-rounded activations | 1/1 | 1 | 5.692 | 5116.683 | 1/1 | 0.000% | 0.000% | 1636.023 | 1/1 | 1243.891 | 1/1 |

MLX peak is the engine's tracked active allocation peak, reset before each request; it includes weights and KV allocations, and excludes allocator cache and allocations outside MLX. Extra peak above the pre-request active allocation is also saved. Engine RSS is a post-request resident-memory snapshot, not a sampled request peak. Its saved high-water mark is cumulative. These scopes overlap and must not be added. Memory RPCs and counter reset are outside TTFT and latency timing; missing measurements stay unavailable with explicit coverage. No activation-memory saving is assumed.

Detailed metrics, sample deviations, coverage and verified-pair counts: `activation_comparison.json` / `activation_comparison.csv`.


## Tasks and reference answers

Each context reads its Markdown prompt and JSON expectation file. Generated tasks add complete records to fit their budgets and calculate references from those records. Static tasks use the Markdown literally with the configured expected answer; their actual token counts may be below the budgets. Context length and reasoning difficulty change together, so differences across contexts do not isolate length alone. Each precision receives the same token IDs, reference answer, and comparison rules at a given context.

- **Short**: Single-item stock arithmetic and a fulfillment decision. Records: 9; input tokens: 256. Reference: `{"item": "MONITOR", "available_units": 68, "fulfillable": true}`. Comparison: `{"allow_extra_fields": false, "case_sensitive": true}`.
- **Medium**: Filter competing quotes, calculate landed costs and rank eligible suppliers. Records: 20; input tokens: 992. Reference: `{"vendor": "TAMBORA", "landed_cost": 1365, "eligible_vendors": 7, "delivery_days": 4}`. Comparison: `{"allow_extra_fields": false, "case_sensitive": true}`.
- **Long**: Reconcile a multi-document ledger, apply corrections and the latest policy, then calculate a dispatch decision. Records: 77; input tokens: 4065. Reference: `{"destination": "Surabaya", "available_units": 215, "shortfall_units": 205, "action": "REORDER"}`. Comparison: `{"allow_extra_fields": false, "case_sensitive": true}`.

[Read the complete prompts](prompts.md); `prompts.json` also contains task data, token IDs and hashes.

Accuracy checks the configured JSON fields and their types. Expected fields must always be present; extra keys and string case follow each task's comparison options. Text similarity measures agreement with FP32, not correctness.
SD is the sample standard deviation across successful requests (undefined for fewer than two). Failed/planned trials never contribute zero timings to the mean.
TTFT (time to first token) measures engine request arrival to the first generated token reaching the engine frontend; it includes queueing and input prefill, and excludes model setup and subsequent decoding. This local measurement excludes HTTP/network transport. Tables show milliseconds; JSON/CSV fields use seconds. TTFT coverage counts measured versus completed requests. Only available, valid engine metrics enter TTFT averages; unavailable historical metrics are never reconstructed from total latency.
Mean field accuracy uses successful requests. Answer pass rate uses every generation attempt as its denominator, with generation errors counted as failures.
Summary files retain each task's per-field correctness and the mean accuracy of its reasoning fields among successful requests. Invalid JSON scores false for all fields; valid JSON fences are accepted.
Mean tokens/s is the arithmetic mean of individual trial rates. Summary files also include weighted tokens/s, median, minimum, maximum, and trial counts.
Speedup is the FP32 mean latency divided by the comparison mean for the same context; raw output comparisons pair the same trial ID.
Repeated timing measures runtime variation. These three fixed tasks do not establish overall model quality.

## Short answers

### FP32

Trials 1:

```text
```json
{"item": "MONITOR", "available_units": 0, "fulfillable": false}
```
```

### BF16

Trials 1:

```text
```json
{"item": "MONITOR", "available_units": 0, "fulfillable": false}
```
```

### FP8

Trials 1:

```text
```json
{"item": "MONITOR", "available_units": 0, "fulfillable": false}
```
```

### INT4

Trials 1:

```text
```json
{"item": "MONITOR", "available_units": 0, "fulfillable": false}
```
```

### FP8_A8

Trials 1:

```text
```json
{"item": "MONITOR", "available_units": 5, "fulfillable": false}
```
```

## Medium answers

### FP32

Trials 1:

```text
```json
{"vendor": "RINJANI", "landed_cost": 1500, "eligible_vendors": 1, "delivery_days": 2}
```
```

### BF16

Trials 1:

```text
```json
{"vendor": "RINJANI", "landed_cost": 1500, "eligible_vendors": 1, "delivery_days": 2}
```
```

### FP8

Trials 1:

```text
```json
{
  "vendor": "BROMO",
  "landed_cost": 120 * 10 + 70 - 0 = 1200,
  "eligible_vendors": 1,
  "delivery_days": 3
}
```
```

### INT4

Trials 1:

```text
```json
{"vendor": "SUPPLIER-13", "landed_cost": 1500, "eligible_vendors": 1, "delivery_days": 2}
```
```

### FP8_A8

Trials 1:

```text
```json
{
  "vendor": "RINJANI",
  "landed_cost": 120 * 9 + 90 - 10 = 120 * 9 + 90 - 10 = 1080 + 90 - 10 = 1080 + 80 = 1160,
  "eligible_vendors": 3,
  "delivery_days":
```

## Long answers

### FP32

Trials 1:

```text
```json
{
  "destination": "BDG",
  "available_units": 50,
  "shortfall_units": 25,
  "action": "REORDER"
}
```
```

### BF16

Trials 1:

```text
```json
{
  "destination": "BDG",
  "available_units": 50,
  "shortfall_units": 25,
  "action": "REORDER"
}
```
```

### FP8

Trials 1:

```text
{
  "destination": "BDG",
  "available_units": 100,
  "shortfall_units": 0,
  "action": "RELEASE"
}
```

### INT4

Trials 1:

```text
```json
{
  "destination": "Example City",
  "available_units": 50,
  "shortfall_units": 25,
  "action": "REORDER"
}
```
```

### FP8_A8

Trials 1:

```text
{"destination": "Sembilan", "available_units": 210, "shortfall_units": 420 - 37 = 383, "action": "REORDER"}
```
