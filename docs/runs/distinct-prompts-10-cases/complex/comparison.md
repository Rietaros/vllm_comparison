# vLLM precision comparison: case averages

Model: `models/e15b00bc84c6b5ee/BF16`; source: `local:models/e15b00bc84c6b5ee/BF16`.
Hardware: Apple M1 Pro, 16 GiB unified RAM, Darwin 15.5. Backend: vLLM-Metal.

10 measured generations per precision/context (150 requested in total). Batch size 1; temperature 0; seed 42; prefix caching disabled.
Each round rotates context order; all precisions use the same schedule and the same token IDs. The model is loaded once per precision.
Means include the first measured request. No extra benchmark warm-up is added. Engine initialization/profile/warm-up passes are outside generation timing.
Each round uses a different editable prompt and expected answer per context. Means and sample deviations summarize variation across these cases and their output lengths.
Elapsed time includes prompt prefill, decoding, and API overhead; tokens/s is end-to-end output throughput.
Output limit: 96 tokens. 18 returned responses reached the limit; truncated answers are retained and graded as returned.
Model download, conversion, and engine loading are timed separately. First requests can include lazy kernel initialization.
Metal FP8 uses MXFP8 E4M3 weights with BF16 inputs; INT4 uses affine weights. This measures local Metal inference.
FP8_A8 applies activation quantize/dequantize rounding with BF16 buffers. Some tensors and reductions retain higher precision.
Weight size is the saved tensor payload, including scales and unquantized tensors; it is not total runtime memory.
Prepared Metal files are audited against their requested storage format.
RSS is the cumulative driver-process high-water mark, not the complete engine/GPU memory usage.

| Precision | Context | Status | Completed / requested | Mean input tokens | Mean seconds ± SD | Mean TTFT ms ± SD | TTFT measured / completed | Mean tokens/s | Weight MiB | Mean correct fields | Answer pass rate | Speedup vs FP32 |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| FP32 | Short | skipped | 0 / 10 | 251.7 | — ± — | — | — | — | — | — | — | — |
| FP32 | Medium | skipped | 0 / 10 | 1017.4 | — ± — | — | — | — | — | — | — | — |
| FP32 | Long | skipped | 0 / 10 | 4090.5 | — ± — | — | — | — | — | — | — | — |
| BF16 | Short | complete | 10 / 10 | 251.7 | 4.161 ± 1.402 | 1131.6 ± 836.2 | 10/10 | 10.9 | 7672.2 | 10.0% | 10.0% | — |
| BF16 | Medium | complete | 10 / 10 | 1017.4 | 7.829 ± 2.925 | 3682.6 ± 1224.1 | 10/10 | 6.1 | 7672.2 | 25.0% | 0.0% | — |
| BF16 | Long | complete | 10 / 10 | 4090.5 | 20.076 ± 3.824 | 13611.2 ± 1346.0 | 10/10 | 3.2 | 7672.2 | 22.5% | 0.0% | — |
| FP8 | Short | complete | 10 / 10 | 251.7 | 2.066 ± 0.920 | 803.3 ± 10.6 | 10/10 | 19.0 | 3956.2 | 33.3% | 0.0% | — |
| FP8 | Medium | complete | 10 / 10 | 1017.4 | 4.693 ± 0.029 | 3223.1 ± 3.5 | 10/10 | 9.5 | 3956.2 | 25.0% | 0.0% | — |
| FP8 | Long | complete | 10 / 10 | 4090.5 | 19.523 ± 0.848 | 15487.2 ± 41.7 | 10/10 | 4.6 | 3956.2 | 7.5% | 0.0% | — |
| INT4 | Short | complete | 10 / 10 | 251.7 | 1.769 ± 0.140 | 747.0 ± 8.9 | 10/10 | 31.4 | 2158.1 | 0.0% | 0.0% | — |
| INT4 | Medium | complete | 10 / 10 | 1017.4 | 3.753 ± 0.124 | 3022.5 ± 6.4 | 10/10 | 8.9 | 2158.1 | 20.0% | 0.0% | — |
| INT4 | Long | complete | 10 / 10 | 4090.5 | 16.370 ± 0.850 | 14696.7 ± 16.5 | 10/10 | 3.0 | 2158.1 | 40.0% | 0.0% | — |
| FP8_A8 | Short | complete | 10 / 10 | 251.7 | 3.067 ± 0.431 | 2067.6 ± 67.6 | 10/10 | 10.6 | 3956.2 | 26.7% | 0.0% | — |
| FP8_A8 | Medium | complete | 10 / 10 | 1017.4 | 10.436 ± 0.219 | 8950.7 ± 190.6 | 10/10 | 4.3 | 3956.2 | 22.5% | 0.0% | — |
| FP8_A8 | Long | complete | 10 / 10 | 4090.5 | 40.792 ± 0.914 | 38848.0 ± 564.0 | 10/10 | 1.1 | 3956.2 | 47.5% | 0.0% | — |

Observed runtime limitation: the installed vLLM/Metal stack logged a segmentation fault during engine shutdown for BF16, FP8, INT4, FP8_A8. Completed generation results were saved before shutdown. See the corresponding engine logs; a clean teardown is not verified.

## Fixed FP8 weights: activation comparison

FP8 uses BF16 activations. FP8_A8 rounds quantized projection inputs to MXFP8 with mx.qqmm, then computes with BF16 buffers. A quantized tied output head also receives rounding. This is a quantize/dequantize experiment, not native FP8 arithmetic or persistent FP8 activation storage. Embedding lookups, attention and the KV cache retain BF16 behavior.

Both cases reuse one FP8 checkpoint, the same prompt token IDs, BF16 KV dtype, cache block size/count, generation settings and rotating trial schedule. Verified pairs check checkpoint/cache/settings identity, prompt hashes, token counts and reference answers. Sequential engine runs can still differ due to system load and compilation; means include first-request work.

| Model/tier | Context | Case | Completed | Verified pairs | Mean latency s | Mean TTFT ms | TTFT coverage | Mean field accuracy | Answer pass | Mean MLX peak MiB | Peak coverage | Mean engine RSS after MiB | RSS coverage |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Single model | Short | FP8 / BF16 activations | 10/10 | 10 | 2.066 | 803.290 | 10/10 | 33.333% | 0.000% | 4928.497 | 10/10 | 4460.286 | 10/10 |
| Single model | Short | FP8_A8 / FP8-rounded activations | 10/10 | 10 | 3.067 | 2067.580 | 10/10 | 26.667% | 0.000% | 4955.097 | 10/10 | 4678.786 | 10/10 |
| Single model | Medium | FP8 / BF16 activations | 10/10 | 10 | 4.693 | 3223.105 | 10/10 | 25.000% | 0.000% | 5085.372 | 10/10 | 4416.173 | 10/10 |
| Single model | Medium | FP8_A8 / FP8-rounded activations | 10/10 | 10 | 10.436 | 8950.660 | 10/10 | 22.500% | 0.000% | 5127.056 | 10/10 | 4653.605 | 10/10 |
| Single model | Long | FP8 / BF16 activations | 10/10 | 10 | 19.523 | 15487.195 | 10/10 | 7.500% | 0.000% | 5072.790 | 10/10 | 4413.773 | 10/10 |
| Single model | Long | FP8_A8 / FP8-rounded activations | 10/10 | 10 | 40.792 | 38847.968 | 10/10 | 47.500% | 0.000% | 5115.290 | 10/10 | 4653.778 | 10/10 |

MLX peak is the engine's tracked active allocation peak, reset before each request; it includes weights and KV allocations, and excludes allocator cache and allocations outside MLX. Extra peak above the pre-request active allocation is also saved. Engine RSS is a post-request resident-memory snapshot, not a sampled request peak. Its saved high-water mark is cumulative. These scopes overlap and must not be added. Memory RPCs and counter reset are outside TTFT and latency timing; missing measurements stay unavailable with explicit coverage. No activation-memory saving is assumed.

Detailed metrics, sample deviations, coverage and verified-pair counts: `activation_comparison.json` / `activation_comparison.csv`.


## Tasks and reference answers

Each context reads its Markdown prompt and JSON expectation file. Generated tasks add complete records to fit their budgets and calculate references from those records. Static tasks use the Markdown literally with the configured expected answer; their actual token counts may be below the budgets. Context length and reasoning difficulty change together, so differences across contexts do not isolate length alone. Each precision receives the same token IDs, reference answer, and comparison rules for a given context and trial ID.

- **Short / short-01**: Short case 01: monitor decision. Records: 0; input tokens: 251. Reference: `{"item": "MONITOR", "available_units": 124, "fulfillable": true}`. Comparison: `{"allow_extra_fields": false, "case_sensitive": true}`.
- **Short / short-02**: Short case 02: keyboard decision. Records: 0; input tokens: 250. Reference: `{"item": "KEYBOARD", "available_units": 113, "fulfillable": false}`. Comparison: `{"allow_extra_fields": false, "case_sensitive": true}`.
- **Short / short-03**: Short case 03: router decision. Records: 0; input tokens: 251. Reference: `{"item": "ROUTER", "available_units": 140, "fulfillable": true}`. Comparison: `{"allow_extra_fields": false, "case_sensitive": true}`.
- **Short / short-04**: Short case 04: printer decision. Records: 0; input tokens: 251. Reference: `{"item": "PRINTER", "available_units": 129, "fulfillable": false}`. Comparison: `{"allow_extra_fields": false, "case_sensitive": true}`.
- **Short / short-05**: Short case 05: tablet decision. Records: 0; input tokens: 252. Reference: `{"item": "TABLET", "available_units": 156, "fulfillable": true}`. Comparison: `{"allow_extra_fields": false, "case_sensitive": true}`.
- **Short / short-06**: Short case 06: scanner decision. Records: 0; input tokens: 251. Reference: `{"item": "SCANNER", "available_units": 145, "fulfillable": false}`. Comparison: `{"allow_extra_fields": false, "case_sensitive": true}`.
- **Short / short-07**: Short case 07: webcam decision. Records: 0; input tokens: 253. Reference: `{"item": "WEBCAM", "available_units": 172, "fulfillable": true}`. Comparison: `{"allow_extra_fields": false, "case_sensitive": true}`.
- **Short / short-08**: Short case 08: headset decision. Records: 0; input tokens: 253. Reference: `{"item": "HEADSET", "available_units": 180, "fulfillable": false}`. Comparison: `{"allow_extra_fields": false, "case_sensitive": true}`.
- **Short / short-09**: Short case 09: speaker decision. Records: 0; input tokens: 252. Reference: `{"item": "SPEAKER", "available_units": 188, "fulfillable": true}`. Comparison: `{"allow_extra_fields": false, "case_sensitive": true}`.
- **Short / short-10**: Short case 10: projector decision. Records: 0; input tokens: 253. Reference: `{"item": "PROJECTOR", "available_units": 196, "fulfillable": false}`. Comparison: `{"allow_extra_fields": false, "case_sensitive": true}`.
- **Medium / medium-01**: Medium case 01: monitor decision. Records: 0; input tokens: 1015. Reference: `{"vendor": "V01-07", "landed_cost": 832, "eligible_vendors": 8, "delivery_days": 1}`. Comparison: `{"allow_extra_fields": false, "case_sensitive": true}`.
- **Medium / medium-02**: Medium case 02: keyboard decision. Records: 0; input tokens: 1019. Reference: `{"vendor": "V02-13", "landed_cost": 914, "eligible_vendors": 8, "delivery_days": 1}`. Comparison: `{"allow_extra_fields": false, "case_sensitive": true}`.
- **Medium / medium-03**: Medium case 03: router decision. Records: 0; input tokens: 1017. Reference: `{"vendor": "V03-19", "landed_cost": 1031, "eligible_vendors": 8, "delivery_days": 1}`. Comparison: `{"allow_extra_fields": false, "case_sensitive": true}`.
- **Medium / medium-04**: Medium case 04: printer decision. Records: 0; input tokens: 1018. Reference: `{"vendor": "V04-04", "landed_cost": 1397, "eligible_vendors": 8, "delivery_days": 1}`. Comparison: `{"allow_extra_fields": false, "case_sensitive": true}`.
- **Medium / medium-05**: Medium case 05: tablet decision. Records: 0; input tokens: 1017. Reference: `{"vendor": "V05-01", "landed_cost": 1140, "eligible_vendors": 8, "delivery_days": 1}`. Comparison: `{"allow_extra_fields": false, "case_sensitive": true}`.
- **Medium / medium-06**: Medium case 06: scanner decision. Records: 0; input tokens: 1016. Reference: `{"vendor": "V06-18", "landed_cost": 1549, "eligible_vendors": 7, "delivery_days": 3}`. Comparison: `{"allow_extra_fields": false, "case_sensitive": true}`.
- **Medium / medium-07**: Medium case 07: webcam decision. Records: 0; input tokens: 1018. Reference: `{"vendor": "V07-09", "landed_cost": 1559, "eligible_vendors": 8, "delivery_days": 2}`. Comparison: `{"allow_extra_fields": false, "case_sensitive": true}`.
- **Medium / medium-08**: Medium case 08: headset decision. Records: 0; input tokens: 1015. Reference: `{"vendor": "V08-02", "landed_cost": 1485, "eligible_vendors": 7, "delivery_days": 2}`. Comparison: `{"allow_extra_fields": false, "case_sensitive": true}`.
- **Medium / medium-09**: Medium case 09: speaker decision. Records: 0; input tokens: 1020. Reference: `{"vendor": "V09-02", "landed_cost": 2085, "eligible_vendors": 4, "delivery_days": 2}`. Comparison: `{"allow_extra_fields": false, "case_sensitive": true}`.
- **Medium / medium-10**: Medium case 10: projector decision. Records: 0; input tokens: 1019. Reference: `{"vendor": "V10-01", "landed_cost": 1475, "eligible_vendors": 5, "delivery_days": 1}`. Comparison: `{"allow_extra_fields": false, "case_sensitive": true}`.
- **Long / long-01**: Long case 01: monitor decision. Records: 0; input tokens: 4093. Reference: `{"destination": "Bandung", "available_units": 226, "shortfall_units": 683, "action": "REORDER"}`. Comparison: `{"allow_extra_fields": false, "case_sensitive": true}`.
- **Long / long-02**: Long case 02: keyboard decision. Records: 0; input tokens: 4094. Reference: `{"destination": "Surabaya", "available_units": 227, "shortfall_units": 0, "action": "RELEASE"}`. Comparison: `{"allow_extra_fields": false, "case_sensitive": true}`.
- **Long / long-03**: Long case 03: router decision. Records: 0; input tokens: 4094. Reference: `{"destination": "Semarang", "available_units": 273, "shortfall_units": 654, "action": "REORDER"}`. Comparison: `{"allow_extra_fields": false, "case_sensitive": true}`.
- **Long / long-04**: Long case 04: printer decision. Records: 0; input tokens: 4096. Reference: `{"destination": "Bandung", "available_units": 371, "shortfall_units": 0, "action": "RELEASE"}`. Comparison: `{"allow_extra_fields": false, "case_sensitive": true}`.
- **Long / long-05**: Long case 05: tablet decision. Records: 0; input tokens: 4095. Reference: `{"destination": "Surabaya", "available_units": 427, "shortfall_units": 518, "action": "REORDER"}`. Comparison: `{"allow_extra_fields": false, "case_sensitive": true}`.
- **Long / long-06**: Long case 06: scanner decision. Records: 0; input tokens: 4094. Reference: `{"destination": "Semarang", "available_units": 489, "shortfall_units": 0, "action": "RELEASE"}`. Comparison: `{"allow_extra_fields": false, "case_sensitive": true}`.
- **Long / long-07**: Long case 07: webcam decision. Records: 0; input tokens: 4094. Reference: `{"destination": "Bandung", "available_units": 450, "shortfall_units": 513, "action": "REORDER"}`. Comparison: `{"allow_extra_fields": false, "case_sensitive": true}`.
- **Long / long-08**: Long case 08: headset decision. Records: 0; input tokens: 4095. Reference: `{"destination": "Surabaya", "available_units": 426, "shortfall_units": 0, "action": "RELEASE"}`. Comparison: `{"allow_extra_fields": false, "case_sensitive": true}`.
- **Long / long-09**: Long case 09: speaker decision. Records: 0; input tokens: 4068. Reference: `{"destination": "Semarang", "available_units": 450, "shortfall_units": 531, "action": "REORDER"}`. Comparison: `{"allow_extra_fields": false, "case_sensitive": true}`.
- **Long / long-10**: Long case 10: projector decision. Records: 0; input tokens: 4082. Reference: `{"destination": "Bandung", "available_units": 479, "shortfall_units": 0, "action": "RELEASE"}`. Comparison: `{"allow_extra_fields": false, "case_sensitive": true}`.

[Read the complete prompts](prompts.md); `prompts.json` also contains task data, token IDs and hashes.

Accuracy checks the configured JSON fields and their types. Expected fields must always be present; extra keys and string case follow each task's comparison options. Text similarity measures agreement with FP32, not correctness.
SD is the sample standard deviation across successful requests (undefined for fewer than two). Failed/planned trials never contribute zero timings to the mean.
TTFT (time to first token) measures engine request arrival to the first generated token reaching the engine frontend; it includes queueing and input prefill, and excludes model setup and subsequent decoding. This local measurement excludes HTTP/network transport. Tables show milliseconds; JSON/CSV fields use seconds. TTFT coverage counts measured versus completed requests. Only available, valid engine metrics enter TTFT averages; unavailable historical metrics are never reconstructed from total latency.
Mean field accuracy uses successful requests. Answer pass rate uses every generation attempt as its denominator, with generation errors counted as failures.
Summary files retain each task's per-field correctness and the mean accuracy of its reasoning fields among successful requests. Invalid JSON scores false for all fields; valid JSON fences are accepted.
Mean tokens/s is the arithmetic mean of individual trial rates. Summary files also include weighted tokens/s, median, minimum, maximum, and trial counts.
Speedup is the FP32 mean latency divided by the comparison mean for the same context; raw output comparisons pair the same trial ID.
The dataset contains synthetic examples of three task families. Its accuracy does not establish overall model quality.

## Short answers

### FP32

Trials 1, 2, 3, 4, 5, 6, 7, 8, 9, 10:

```text
Estimated weights + KV + runtime reserve = 17.18 GiB; configured unified RAM budget = 10.00 GiB
```

### BF16

Trials 1:

```text
{
  "item": "MONITOR",
  "available_units": 23 + 10 + 15 + 20 + 6 + 11 + 16 + 21 + 7 - 5,
  "fulfillable": true
}
```

Trials 2:

```text
{"item":"KEYBOARD","available_units":34+17+3+8+13+18+4+9+14-7,"fulfillable":false}
```

Trials 3:

```text
{"item":"ROUTER","available_units":45+5+10+15+20+6+11+16+21-9,"fulfillable":false}
```

Trials 4:

```text
{"item":"PRINTER","available_units":56+12+17+3+8+13+18+4+9-11,"fulfillable":false}
```

Trials 5:

```text
{"item":"TABLET","available_units":67+19+5+10+15+20+6+11+16-13,"fulfillable":true}
```

Trials 6:

```text
{"item":"SCANNER","available_units":145,"fulfillable":false}
```

Trials 7:

```text
{"item":"WEBCAM","available_units":89+14+19+5+10+15+20+6+11-17,"fulfillable":true}
```

Trials 8:

```text
{"item":"HEADSET","available_units":100+21+7+12+17+3+8+13+18-19,"fulfillable":false}
```

Trials 9:

```text
{"item":"SPEAKER","available_units":111+9+14+19+5+10+15+20+6-21","fulfillable":true}
```

Trials 10:

```text
{"item":"PROJECTOR","available_units":122+16+21+7+12+17+3+8+13-23,"fulfillable":false}
```

### FP8

Trials 1:

```text
{"item":"MONITOR","available_units":102,"fulfillable":true}
```

Trials 2:

```text
{
  "item": "KEYBOARD",
  "available_units": 34 + 17 + 3 + 8 + 13 + 18 + 4 + 9 + 14 - 7,
  "fulfillable": 34 + 17 + 3 + 8 + 13 + 18 + 4 + 9 + 14 - 7 >= 200
}
```

Trials 3:

```text
{"item":"ROUTER","available_units":112,"fulfillable":true}
```

Trials 4:

```text
{
  "item": "PRINTER",
  "available_units": 56 + 12 + 17 + 3 + 8 + 13 + 18 + 4 + 9 - 11,
  "fulfillable": 56 + 12 + 17 + 3 + 8 + 13 + 18 + 4 + 9 - 11 >= 230

```

Trials 5:

```text
{"item":"TABLET","available_units":134,"fulfillable":true}
```

Trials 6:

```text
{"item":"SCANNER","available_units":143,"fulfillable":false}
```

Trials 7:

```text
{"item":"WEBCAM","available_units":162,"fulfillable":true}
```

Trials 8:

```text
{
  "item": "HEADSET",
  "available_units": 100 + 21 + 7 + 12 + 17 + 3 + 8 + 13 + 18 - 19,
  "fulfillable": false
}
```

Trials 9:

```text
{"item":"SPEAKER","available_units":111+9+14+19+5+10+15+20+6-21,"fulfillable":true}
```

Trials 10:

```text
{"item":"PROJECTOR","available_units":122+16+21+7+12+17+3+8+13-23,"fulfillable":false}
```

### INT4

Trials 1:

```text
{
  "item": "MONITOR",
  "available_units": 23 + 10 + 15 + 20 + 6 + 11 + 16 + 21 + 7 - 5,
  "fulfillable": true
}
```

Trials 2:

```text
{"item":"KEYBOARD","available_units":34 + 17 + 3 + 8 + 13 + 18 + 4 + 9 + 14 - 7","fulfillable":false}
```

Trials 3:

```text
{"item":"ROUTER","available_units":45 + 5 + 10 + 15 + 20 + 6 + 11 + 16 + 21 - 9,"fulfillable":false}
```

Trials 4:

```text
{
  "item": "PRINTER",
  "available_units": 56 + 12 + 17 + 3 + 8 + 13 + 18 + 4 + 9 - 11,
  "fulfillable": true
}
```

Trials 5:

```text
{
  "item": "TABLET",
  "available_units": 67 + 19 + 5 + 10 + 15 + 20 + 6 + 11 + 16 - 13,
  "fulfillable": true
}
```

Trials 6:

```text
{"item":"SCANNER","available_units":78+7+12+17+3+8+13+18+4-15","fulfillable":false}
```

Trials 7:

```text
{
  "item": "WEBCAM",
  "available_units": 89 + 14 + 19 + 5 + 10 + 15 + 20 + 6 + 11 - 17,
  "fulfillable": true
}
```

Trials 8:

```text
{
  "item": "HEADSET",
  "available_units": 100 + 21 + 7 + 12 + 17 + 3 + 8 + 13 + 18 - 19,
  "fulfillable": true
}
```

Trials 9:

```text
{"item":"SPEAKER","available_units":111 + 9 + 14 + 19 + 5 + 10 + 15 + 20 + 6 - 21","fulfillable":true}
```

Trials 10:

```text
{
  "item": "PROJECTOR",
  "available_units": 122 + 16 + 21 + 7 + 12 + 17 + 3 + 8 + 13 - 23,
  "fulfillable": true
}
```

### FP8_A8

Trials 1:

```text
{"item":"MONITOR","available_units":102,"fulfillable":true}
```

Trials 2:

```text
{"item":"KEYBOARD","available_units":34+17+3+8+13+18+4+9+14-7","fulfillable":false}
```

Trials 3:

```text
{"item":"ROUTER","available_units":126,"fulfillable":true}
```

Trials 4:

```text
{"item":"PRINTER","available_units":56+12+17+3+8+13+18+4+9-11,"fulfillable":false}
```

Trials 5:

```text
{"item":"TABLET","available_units":112,"fulfillable":true}
```

Trials 6:

```text
{"item":"SCANNER","available_units":132,"fulfillable":false}
```

Trials 7:

```text
{"item":"WEBCAM","available_units":89+14+19+5+10+15+20+6+11-17=164,"fulfillable":true}
```

Trials 8:

```text
{"item":"HEADSET","available_units":100+21+7+12+17+3+8+13+18-19","fulfillable":false}
```

Trials 9:

```text
{"item":"SPEAKER","available_units":111+9+14+19+5+10+15+20+6-21","fulfillable":true}
```

Trials 10:

```text
{"item":"PROJECTOR","available_units":122+16+21+7+12+17+3+8+13-23","fulfillable":false}
```

## Medium answers

### FP32

Trials 1, 2, 3, 4, 5, 6, 7, 8, 9, 10:

```text
Estimated weights + KV + runtime reserve = 17.18 GiB; configured unified RAM budget = 10.00 GiB
```

### BF16

Trials 1:

```text
{
  "vendor": "V01-03",
  "landed_cost": 990,
  "eligible_vendors": 5,
  "delivery_days": 4
}
```

Trials 2:

```text
{
  "vendor": "V02-01",
  "landed_cost": 1422,
  "eligible_vendors": 6,
  "delivery_days": 1
}
```

Trials 3:

```text
{
  "vendor": "V03-01",
  "landed_cost": 1842,
  "eligible_vendors": 6,
  "delivery_days": 1
}
```

Trials 4:

```text
{
  "vendor": "V04-04",
  "landed_cost": 132,
  "eligible_vendors": 10,
  "delivery_days": 1
}
```

Trials 5:

```text
{
  "vendor": "V05-01",
  "landed_cost": 1125,
  "eligible_vendors": 6,
  "delivery_days": 1
}
```

Trials 6:

```text
{
  "vendor": "V06-01",
  "landed_cost": 1584,
  "eligible_vendors": 4,
  "delivery_days": 1
}
```

Trials 7:

```text
{
  "vendor": "V07-09",
  "landed_cost": 1530,
  "eligible_vendors": 11,
  "delivery_days": 2
}
```

Trials 8:

```text
{
  "vendor": "V08-02",
  "landed_cost": 144,
  "eligible_vendors": 10,
  "delivery_days": 2
}
```

Trials 9:

```text
{
  "vendor": "V09-06",
  "landed_cost": 1710,
  "eligible_vendors": 6,
  "delivery_days": 1
}
```

Trials 10:

```text
{
  "vendor": "V10-08",
  "landed_cost": 2160,
  "eligible_vendors": 12,
  "delivery_days": 4
}
```

### FP8

Trials 1:

```text
{
  "vendor": "V01-07",
  "landed_cost": 1872,
  "eligible_vendors": 12,
  "delivery_days": 1
}
```

Trials 2:

```text
{
  "vendor": "V02-01",
  "landed_cost": 1458,
  "eligible_vendors": 12,
  "delivery_days": 1
}
```

Trials 3:

```text
{
  "vendor": "V03-05",
  "landed_cost": 153,
  "eligible_vendors": 11,
  "delivery_days": 1
}
```

Trials 4:

```text
{
  "vendor": "V04-04",
  "landed_cost": 1260,
  "eligible_vendors": 12,
  "delivery_days": 1
}
```

Trials 5:

```text
{
  "vendor": "V05-10",
  "landed_cost": 1430,
  "eligible_vendors": 12,
  "delivery_days": 1
}
```

Trials 6:

```text
{
  "vendor": "V06-01",
  "landed_cost": 1584,
  "eligible_vendors": 5,
  "delivery_days": 1
}
```

Trials 7:

```text
{
  "vendor": "V07-03",
  "landed_cost": 1866,
  "eligible_vendors": 12,
  "delivery_days": 3
}
```

Trials 8:

```text
{
  "vendor": "V08-02",
  "landed_cost": 1440,
  "eligible_vendors": 12,
  "delivery_days": 2
}
```

Trials 9:

```text
{
  "vendor": "V09-06",
  "landed_cost": 1710,
  "eligible_vendors": 12,
  "delivery_days": 1
}
```

Trials 10:

```text
{
  "vendor": "V10-12",
  "landed_cost": 1800,
  "eligible_vendors": 12,
  "delivery_days": 1
}
```

### INT4

Trials 1:

```text
{"vendor":"V01-03","landed_cost":990,"eligible_vendors":4,"delivery_days":4}
```

Trials 2:

```text
{"vendor":"V02-01","landed_cost":1452,"eligible_vendors":6,"delivery_days":1}
```

Trials 3:

```text
{"vendor":"V03-02","landed_cost":1170,"eligible_vendors":5,"delivery_days":2}
```

Trials 4:

```text
{"vendor":"V04-02","landed_cost":1260,"eligible_vendors":4,"delivery_days":2}
```

Trials 5:

```text
{"vendor":"V05-01","landed_cost":1350,"eligible_vendors":6,"delivery_days":1}
```

Trials 6:

```text
{
  "vendor": "V06-01",
  "landed_cost": 1584,
  "eligible_vendors": 4,
  "delivery_days": 1
}
```

Trials 7:

```text
{"vendor":"V07-03","landed_cost":2023,"eligible_vendors":4,"delivery_days":3}
```

Trials 8:

```text
{"vendor":"V08-02","landed_cost":1620,"eligible_vendors":4,"delivery_days":2}
```

Trials 9:

```text
{
  "vendor": "V09-02",
  "landed_cost": 2049,
  "eligible_vendors": 5,
  "delivery_days": 2
}
```

Trials 10:

```text
{"vendor":"V10-08","landed_cost":2142,"eligible_vendors":5,"delivery_days":4}
```

### FP8_A8

Trials 1:

```text
{
  "vendor": "V01-03",
  "landed_cost": 990,
  "eligible_vendors": 5,
  "delivery_days": 4
}
```

Trials 2:

```text
{
  "vendor": "V02-01",
  "landed_cost": 1438,
  "eligible_vendors": 12,
  "delivery_days": 1
}
```

Trials 3:

```text
{
  "vendor": "V03-05",
  "landed_cost": 153,
  "eligible_vendors": 11,
  "delivery_days": 1
}
```

Trials 4:

```text
{
  "vendor": "V04-04",
  "landed_cost": 1260,
  "eligible_vendors": 4,
  "delivery_days": 1
}
```

Trials 5:

```text
{
  "vendor": "V05-01",
  "landed_cost": 1125,
  "eligible_vendors": 12,
  "delivery_days": 1
}
```

Trials 6:

```text
{
  "vendor": "V06-01",
  "landed_cost": 1440,
  "eligible_vendors": 2,
  "delivery_days": 1
}
```

Trials 7:

```text
{
  "vendor": "V07-03",
  "landed_cost": 1962,
  "eligible_vendors": 12,
  "delivery_days": 3
}
```

Trials 8:

```text
{
  "vendor": "V08-02",
  "landed_cost": 1362,
  "eligible_vendors": 12,
  "delivery_days": 2
}
```

Trials 9:

```text
{
  "vendor": "V09-06",
  "landed_cost": 1710,
  "eligible_vendors": 6,
  "delivery_days": 1
}
```

Trials 10:

```text
{
  "vendor": "V10-12",
  "landed_cost": 1800,
  "eligible_vendors": 10,
  "delivery_days": 1
}
```

## Long answers

### FP32

Trials 1, 2, 3, 4, 5, 6, 7, 8, 9, 10:

```text
Estimated weights + KV + runtime reserve = 17.18 GiB; configured unified RAM budget = 10.00 GiB
```

### BF16

Trials 1:

```text
{
  "destination": "Bandung",
  "available_units": 255 + 9 + 17 + 5 + 26 + 14 + 25 + 17 + 14 + 26 + 5 + 26 + 14 + 25 + 17 + 26 + 5 + 26 + 14 + 25 + 17 +
```

Trials 2:

```text
{
  "destination": "Surabaya",
  "available_units": 313 + 4 + 19 + 16 + 19 + 7 + 10 + 16 + 12 + 19 + 16 + 19 + 12 + 19 + 16 + 19 + 16 + 19 + 16 + 19 + 1
```

Trials 3:

```text
{
  "destination": "Semarang",
  "available_units": 371,
  "shortfall_units": 0,
  "action": "RELEASE"
}
```

Trials 4:

```text
{
  "destination": "Bandung",
  "available_units": 360 + (24 + 7 + 11 + 8 + 15 + 20 + 27 + 11 + 23 + 20 + 17 + 14 + 26 + 11 + 23 + 20 + 17 + 20 + 11 + 8 +
```

Trials 5:

```text
{
  "destination": "Surabaya",
  "available_units": 418,
  "shortfall_units": 0,
  "action": "RELEASE"
}
```

Trials 6:

```text
{
  "destination": "Semarang",
  "available_units": 476,
  "shortfall_units": 0,
  "action": "RELEASE"
}
```

Trials 7:

```text
{
  "destination": "Bandung",
  "available_units": 465 + (22 + 5 + 26 + 9 + 13 + 17 + 14 + 21 + 26 + 9 + 17 + 25 + 26 + 14 + 21 + 26 + 14 + 21 + 26 + 17 +
```

Trials 8:

```text
{
  "destination": "Surabaya",
  "available_units": 523 + (20 + 27 + 24 + 7 + 11 + 15 + 20 + 27 + 12 + 19 + 23 + 20 + 24 + 7 + 16 + 23 + 20 + 27 + 12 + 1
```

Trials 9:

```text
{
  "destination": "Semarang",
  "available_units": 581,
  "shortfall_units": 0,
  "action": "RELEASE"
}
```

Trials 10:

```text
{
  "destination": "Bandung",
  "available_units": 570,
  "shortfall_units": 0,
  "action": "RELEASE"
}
```

### FP8

Trials 1:

```text
{
  "destination": "Bandung",
  "available_units": 255 + 9 + 17 + 14 + 26 + 5 + 26 + 14 + 26 + 5 + 26 + 14 + 26 + 5 + 26 + 14 + 26 + 5 + 26 + 14 + 26 + 5
```

Trials 2:

```text
{
  "destination": "Surabaya",
  "available_units": 313 + 4 + 19 + 16 + 23 + 19 + 16 + 20 + 12 + 15 + 19 + 16 + 23 + 12 + 19 + 23 + 12 + 15 + 16 + 27 +
```

Trials 3:

```text
{
  "destination": "Semarang",
  "available_units": 371 + 26 + 9 + 13 + 10 + 17 + 18 + 25 + 22 + 18 + 21 + 16 + 10 + 17 + 21 + 25 + 13 + 10 + 17 + 22 +
```

Trials 4:

```text
{
  "destination": "Bandung",
  "available_units": 360 + 24 + 7 + 14 + 11 + 8 + 15 + 20 + 23 + 17 + 26 + 14 + 22 + 26 + 5 + 14 + 21 + 11 + 20 + 27 + 10 +
```

Trials 5:

```text
{
  "destination": "Surabaya",
  "available_units": 418 + 26 + 9 + 13 + 17 + 10 + 14 + 21 + 18 + 25 + 26 + 17 + 14 + 10 + 13 + 17 + 14 + 21 + 18 + 25 +
```

Trials 6:

```text
{
  "destination": "Semarang",
  "available_units": 476 + 24 + 7 + 4 + 15 + 12 + 19 + 16 + 23 + 24 + 15 + 12 + 19 + 16 + 23 + 24 + 15 + 12 + 19 + 16 + 2
```

Trials 7:

```text
{
  "destination": "Bandung",
  "available_units": 465 + 26 + 5 + 17 + 14 + 26 + 5 + 17 + 26 + 5 + 14 + 26 + 5 + 14 + 26 + 5 + 14 + 26 + 5 + 14 + 26 + 5 +
```

Trials 8:

```text
{
  "destination": "Surabaya",
  "available_units": 523 + 20 + 27 + 11 + 15 + 4 + 19 + 7 + 16 + 23 + 20 + 12 + 15 + 11 + 12 + 19 + 4 + 11 + 12 + 19 + 16
```

Trials 9:

```text
{
  "destination": "Semarang",
  "available_units": 581 + 25 + 22 + 13 + 10 + 25 + 22 + 13 + 10 + 25 + 22 + 13 + 10 + 25 + 22 + 13 + 10 + 25 + 22 + 13 +
```

Trials 10:

```text
{
  "destination": "Bandung",
  "available_units": 570,
  "shortfall_units": 0,
  "action": "RELEASE"
}
```

### INT4

Trials 1:

```text
{
  "destination": "Bandung",
  "available_units": 255 + 9 + 17 + 14 + 26 + 5 + 23 + 20 + 14 + 26 + 5 + 20 + 17 + 14 + 26 + 5 + 20 + 17 + 14 + 26 + 5 + 2
```

Trials 2:

```text
{
  "destination": "Surabaya",
  "available_units": 313,
  "shortfall_units": 0,
  "action": "RELEASE"
}
```

Trials 3:

```text
{
  "destination": "Semarang",
  "available_units": 371,
  "shortfall_units": 0,
  "action": "RELEASE"
}
```

Trials 4:

```text
{
  "destination": "Bandung",
  "available_units": 360 + 24 + 7 + 14 + 11 + 8 + 20 + 23 + 17 + 20 + 14 + 8 + 26 + 5 + 20 + 11 + 26 + 5 + 23 + 17 + 20 + 1
```

Trials 5:

```text
{
  "destination": "Surabaya",
  "available_units": 418,
  "shortfall_units": 0,
  "action": "RELEASE"
}
```

Trials 6:

```text
{
  "destination": "Semarang",
  "available_units": 476,
  "shortfall_units": 0,
  "action": "RELEASE"
}
```

Trials 7:

```text
{
  "destination": "Bandung",
  "available_units": 465,
  "shortfall_units": 0,
  "action": "RELEASE"
}
```

Trials 8:

```text
{
  "destination": "Surabaya",
  "available_units": 523,
  "shortfall_units": 0,
  "action": "RELEASE"
}
```

Trials 9:

```text
{
  "destination": "Semarang",
  "available_units": 581,
  "shortfall_units": 0,
  "action": "RELEASE"
}
```

Trials 10:

```text
{
  "destination": "Bandung",
  "available_units": 570,
  "shortfall_units": 0,
  "action": "RELEASE"
}
```

### FP8_A8

Trials 1:

```text
{
  "destination": "Bandung",
  "available_units": 255 + 23 - 20 - 23 - 17 - 14 - 11 - 14 - 26 - 5 - 23 - 20 - 23 - 20 - 23 - 20 - 23 - 20 - 23 - 20 - 2
```

Trials 2:

```text
{
  "destination": "Surabaya",
  "available_units": 313,
  "shortfall_units": 0,
  "action": "RELEASE"
}
```

Trials 3:

```text
{
  "destination": "Semarang",
  "available_units": 371,
  "shortfall_units": 0,
  "action": "RELEASE"
}
```

Trials 4:

```text
{
  "destination": "Bandung",
  "available_units": 210,
  "shortfall_units": 0,
  "action": "RELEASE"
}
```

Trials 5:

```text
{
  "destination": "Surabaya",
  "available_units": 418,
  "shortfall_units": 0,
  "action": "RELEASE"
}
```

Trials 6:

```text
{
  "destination": "Semarang",
  "available_units": 476,
  "shortfall_units": 0,
  "action": "RELEASE"
}
```

Trials 7:

```text
{
  "destination": "Bandung",
  "available_units": 465,
  "shortfall_units": 0,
  "action": "RELEASE"
}
```

Trials 8:

```text
{
  "destination": "Surabaya",
  "available_units": 523,
  "shortfall_units": 0,
  "action": "RELEASE"
}
```

Trials 9:

```text
{
  "destination": "Semarang",
  "available_units": 612,
  "shortfall_units": 0,
  "action": "RELEASE"
}
```

Trials 10:

```text
{
  "destination": "Bandung",
  "available_units": 570,
  "shortfall_units": 0,
  "action": "RELEASE"
}
```
