# vLLM precision comparison: case averages

Model: `models/7b50efe10ce32606/BF16`; source: `local:models/7b50efe10ce32606/BF16`.
Hardware: Apple M1 Pro, 16 GiB unified RAM, Darwin 15.5. Backend: vLLM-Metal.

10 measured generations per precision/context (150 requested in total). Batch size 1; temperature 0; seed 42; prefix caching disabled.
Each round rotates context order; all precisions use the same schedule and the same token IDs. The model is loaded once per precision.
Means include the first measured request. No extra benchmark warm-up is added. Engine initialization/profile/warm-up passes are outside generation timing.
Each round uses a different editable prompt and expected answer per context. Means and sample deviations summarize variation across these cases and their output lengths.
Elapsed time includes prompt prefill, decoding, and API overhead; tokens/s is end-to-end output throughput.
Output limit: 96 tokens. 2 returned responses reached the limit; truncated answers are retained and graded as returned.
Model download, conversion, and engine loading are timed separately. First requests can include lazy kernel initialization.
Metal FP8 uses MXFP8 E4M3 weights with BF16 inputs; INT4 uses affine weights. This measures local Metal inference.
FP8_A8 applies activation quantize/dequantize rounding with BF16 buffers. Some tensors and reductions retain higher precision.
Weight size is the saved tensor payload, including scales and unquantized tensors; it is not total runtime memory.
Prepared Metal files are audited against their requested storage format.
RSS is the cumulative driver-process high-water mark, not the complete engine/GPU memory usage.

| Precision | Context | Status | Completed / requested | Mean input tokens | Mean seconds ± SD | Mean TTFT ms ± SD | TTFT measured / completed | Mean tokens/s | Weight MiB | Mean correct fields | Answer pass rate | Speedup vs FP32 |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| FP32 | Short | complete | 10 / 10 | 251.7 | 0.567 ± 0.012 | 200.9 ± 12.6 | 10/10 | 39.3 | 2273.8 | 46.7% | 0.0% | 1.00 |
| FP32 | Medium | complete | 10 / 10 | 1017.4 | 2.346 ± 0.396 | 1567.2 ± 36.0 | 10/10 | 17.0 | 2273.8 | 20.0% | 0.0% | 1.00 |
| FP32 | Long | complete | 10 / 10 | 4090.5 | 20.600 ± 0.674 | 19428.5 ± 590.1 | 10/10 | 2.2 | 2273.8 | 12.5% | 0.0% | 1.00 |
| BF16 | Short | complete | 10 / 10 | 251.7 | 0.334 ± 0.008 | 107.3 ± 8.7 | 10/10 | 66.8 | 1136.9 | 46.7% | 0.0% | 1.70 |
| BF16 | Medium | complete | 10 / 10 | 1017.4 | 0.894 ± 0.233 | 412.1 ± 5.3 | 10/10 | 44.6 | 1136.9 | 20.0% | 0.0% | 2.63 |
| BF16 | Long | complete | 10 / 10 | 4090.5 | 3.450 ± 0.075 | 2690.5 ± 34.0 | 10/10 | 13.1 | 1136.9 | 10.0% | 0.0% | 5.97 |
| FP8 | Short | complete | 10 / 10 | 251.7 | 0.344 ± 0.073 | 123.8 ± 5.2 | 10/10 | 92.3 | 586.3 | 33.3% | 0.0% | 1.65 |
| FP8 | Medium | complete | 10 / 10 | 1017.4 | 0.838 ± 0.008 | 493.9 ± 6.7 | 10/10 | 50.1 | 586.3 | 10.0% | 0.0% | 2.80 |
| FP8 | Long | complete | 10 / 10 | 4090.5 | 3.518 ± 0.079 | 2985.8 ± 37.0 | 10/10 | 11.5 | 586.3 | 17.5% | 0.0% | 5.85 |
| INT4 | Short | complete | 10 / 10 | 251.7 | 0.302 ± 0.061 | 124.3 ± 10.2 | 10/10 | 96.6 | 319.8 | 40.0% | 0.0% | 1.88 |
| INT4 | Medium | complete | 10 / 10 | 1017.4 | 0.750 ± 0.020 | 468.2 ± 10.1 | 10/10 | 55.3 | 319.8 | 7.5% | 0.0% | 3.13 |
| INT4 | Long | complete | 10 / 10 | 4090.5 | 3.374 ± 0.036 | 2882.6 ± 31.9 | 10/10 | 12.5 | 319.8 | 12.5% | 0.0% | 6.11 |
| FP8_A8 | Short | complete | 10 / 10 | 251.7 | 0.465 ± 0.107 | 235.0 ± 12.2 | 10/10 | 67.1 | 586.3 | 30.0% | 0.0% | 1.22 |
| FP8_A8 | Medium | complete | 10 / 10 | 1017.4 | 1.344 ± 0.036 | 1039.9 ± 27.8 | 10/10 | 27.1 | 586.3 | 7.5% | 0.0% | 1.75 |
| FP8_A8 | Long | complete | 10 / 10 | 4090.5 | 5.760 ± 0.142 | 5180.7 ± 95.8 | 10/10 | 7.5 | 586.3 | 10.0% | 0.0% | 3.58 |

Observed runtime limitation: the installed vLLM/Metal stack logged a segmentation fault during engine shutdown for FP32, BF16, FP8, INT4, FP8_A8. Completed generation results were saved before shutdown. See the corresponding engine logs; a clean teardown is not verified.

## Fixed FP8 weights: activation comparison

FP8 uses BF16 activations. FP8_A8 rounds quantized projection inputs to MXFP8 with mx.qqmm, then computes with BF16 buffers. A quantized tied output head also receives rounding. This is a quantize/dequantize experiment, not native FP8 arithmetic or persistent FP8 activation storage. Embedding lookups, attention and the KV cache retain BF16 behavior.

Both cases reuse one FP8 checkpoint, the same prompt token IDs, BF16 KV dtype, cache block size/count, generation settings and rotating trial schedule. Verified pairs check checkpoint/cache/settings identity, prompt hashes, token counts and reference answers. Sequential engine runs can still differ due to system load and compilation; means include first-request work.

| Model/tier | Context | Case | Completed | Verified pairs | Mean latency s | Mean TTFT ms | TTFT coverage | Mean field accuracy | Answer pass | Mean MLX peak MiB | Peak coverage | Mean engine RSS after MiB | RSS coverage |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Single model | Short | FP8 / BF16 activations | 10/10 | 10 | 0.344 | 123.760 | 10/10 | 33.333% | 0.000% | 1470.894 | 10/10 | 1305.552 | 10/10 |
| Single model | Short | FP8_A8 / FP8-rounded activations | 10/10 | 10 | 0.465 | 234.983 | 10/10 | 30.000% | 0.000% | 1484.234 | 10/10 | 1269.380 | 10/10 |
| Single model | Medium | FP8 / BF16 activations | 10/10 | 10 | 0.838 | 493.933 | 10/10 | 10.000% | 0.000% | 1634.620 | 10/10 | 1292.284 | 10/10 |
| Single model | Medium | FP8_A8 / FP8-rounded activations | 10/10 | 10 | 1.344 | 1039.895 | 10/10 | 7.500% | 0.000% | 1649.550 | 10/10 | 1255.919 | 10/10 |
| Single model | Long | FP8 / BF16 activations | 10/10 | 10 | 3.518 | 2985.764 | 10/10 | 17.500% | 0.000% | 1633.621 | 10/10 | 1243.036 | 10/10 |
| Single model | Long | FP8_A8 / FP8-rounded activations | 10/10 | 10 | 5.760 | 5180.739 | 10/10 | 10.000% | 0.000% | 1637.255 | 10/10 | 1219.358 | 10/10 |

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

Trials 1:

```text
```json
{"item":"MONITOR","available_units":5,"fulfillable":false}
```
```

Trials 2:

```text
```json
{"item":"KEYBOARD","available_units":54,"fulfillable":true}
```
```

Trials 3:

```text
```json
{"item":"ROUTER","available_units":54,"fulfillable":true}
```
```

Trials 4:

```text
```json
{"item":"PRINTER","available_units":56, "fulfillable":false}
```
```

Trials 5:

```text
```json
{"item":"TABLET","available_units":54,"fulfillable":true}
```
```

Trials 6:

```text
```json
{"item":"SCANNER","available_units":54,"fulfillable":true}
```
```

Trials 7:

```text
```json
{"item":"WEBCAM","available_units":54,"fulfillable":true}
```
```

Trials 8:

```text
```json
{"item":"HEADSET","available_units":217,"fulfillable":true}
```
```

Trials 9:

```text
```json
{"item":"SPEAKER","available_units":5,"fulfillable":false}
```
```

Trials 10:

```text
```json
{"item":"PROJECTOR","available_units":545,"fulfillable":true}
```
```

### BF16

Trials 1:

```text
```json
{"item":"MONITOR","available_units":5,"fulfillable":false}
```
```

Trials 2:

```text
```json
{"item":"KEYBOARD","available_units":54,"fulfillable":true}
```
```

Trials 3:

```text
```json
{"item":"ROUTER","available_units":54,"fulfillable":true}
```
```

Trials 4:

```text
```json
{"item":"PRINTER","available_units":56, "fulfillable":false}
```
```

Trials 5:

```text
```json
{"item":"TABLET","available_units":54,"fulfillable":true}
```
```

Trials 6:

```text
```json
{"item":"SCANNER","available_units":54,"fulfillable":true}
```
```

Trials 7:

```text
```json
{"item":"WEBCAM","available_units":54,"fulfillable":true}
```
```

Trials 8:

```text
```json
{"item":"HEADSET","available_units":217,"fulfillable":true}
```
```

Trials 9:

```text
```json
{"item":"SPEAKER","available_units":5,"fulfillable":false}
```
```

Trials 10:

```text
```json
{"item":"PROJECTOR","available_units":230,"fulfillable":true}
```
```

### FP8

Trials 1:

```text
```json
{"item": "MONITOR", "available_units": 5, "fulfillable": false}
```
```

Trials 2:

```text
```json
{"item": "KEYBOARD", "available_units": 34 + 17 + 3 + 8 + 13 + 18 + 4 + 9 + 14 - 7, "fulfillable": true}
```
```

Trials 3:

```text
```json
{"item": "ROUTER", "available_units": 55, "fulfillable": true}
```
```

Trials 4:

```text
```json
{"item": "PRINTER", "available_units": 56 + 230 - 11, "fulfillable": true}
```
```

Trials 5:

```text
```json
{"item": "TABLET", "available_units": 57, "fulfillable": true}
```
```

Trials 6:

```text
```json
{"item": "SCANNER", "available_units": 78 + 260 - 15, "fulfillable": true}
```
```

Trials 7:

```text
```json
{"item": "WEBCAM", "available_units": 50, "fulfillable": true}
```
```

Trials 8:

```text
```json
{"item": "HEADSET", "available_units": 210, "fulfillable": true}
```
```

Trials 9:

```text
```json
{"item": "SPEAKER", "available_units": 111, "fulfillable": true}
```
```

Trials 10:

```text
```json
{"item": "PROJECTOR", "available_units": 122 + 320 - 23, "fulfillable": true}
```
```

### INT4

Trials 1:

```text
```json
{"item": "MONITOR", "available_units": 5, "fulfillable": false}
```
```

Trials 2:

```text
```json
{"item": "KEYBOARD", "available_units": 34 + 17 + 3 + 8 + 13 + 18 + 4 + 9 + 14 = 89, "fulfillable": true}
```
```

Trials 3:

```text
```json
{"item": "ROUTER", "available_units": 55, "fulfillable": true}
```
```

Trials 4:

```text
```json
{"item": "PRINTER", "available_units": 56, "fulfillable": true}
```
```

Trials 5:

```text
```json
{"item": "TABLET", "available_units": 52, "fulfillable": true}
```
```

Trials 6:

```text
```json
{"item": "SCANNER", "available_units": 100, "fulfillable": true}
```
```

Trials 7:

```text
```json
{"item": "WEBCAM", "available_units": 5, "fulfillable": false}
```
```

Trials 8:

```text
```json
{"item": "HEADSET", "available_units": 100, "fulfillable": true}
```
```

Trials 9:

```text
```json
{"item": "SPEAKER", "available_units": 111, "fulfillable": true}
```
```

Trials 10:

```text
```json
{"item": "PROJECTOR", "available_units": 320, "fulfillable": true}
```
```

### FP8_A8

Trials 1:

```text
```json
{"item":"MONITOR","available_units":50,"fulfillable":true}
```
```

Trials 2:

```text
```json
{"item": "KEYBOARD", "available_units": 34 + 17 + 3 + 8 + 13 + 18 + 4 + 9 + 14 - 7, "fulfillable": true}
```
```

Trials 3:

```text
```json
{"item": "ROUTER", "available_units": 45 + 47 - 9, "fulfillable": true}
```
```

Trials 4:

```text
```json
{"item":"PRINTER","available_units":56, "fulfillable":false}
```
```

Trials 5:

```text
```json
{"item": "TABLET", "available_units": 67 + 57 - 13, "fulfillable": true}
```
```

Trials 6:

```text
```json
{"item":"SCANNER","available_units":50,"fulfillable":true}
```
```

Trials 7:

```text
```json
{"item": "WEBCAM", "available_units": 50, "fulfillable": false}
```
```

Trials 8:

```text
```json
{"item": "HEADSET", "available_units": 100 + 21 + 7 + 12 + 17 + 3 + 8 + 13 + 18 - 19, "fulfillable": true}
```
```

Trials 9:

```text
```json
{"item":"SPEAKER","available_units":111,"fulfillable":true}
```
```

Trials 10:

```text
```json
{"item":"PROJECTOR","available_units":54,"fulfillable":true}
```
```

## Medium answers

### FP32

Trials 1:

```text
```json
{"vendor":"V01-01","landed_cost":1500,"eligible_vendors":1,"delivery_days":1}
```
```

Trials 2:

```text
```json
{"vendor":"V02-01","landed_cost":1500,"eligible_vendors":1,"delivery_days":1}
```
```

Trials 3:

```text
```json
{"vendor":"V03-01","landed_cost":1500,"eligible_vendors":1,"delivery_days":3}
```
```

Trials 4:

```text
```json
{"vendor":"V04-01","landed_cost":1500,"eligible_vendors":1,"delivery_days":1}
```
```

Trials 5:

```text
```json
{"vendor":"V05-01","landed_cost":1500,"eligible_vendors":1,"delivery_days":1}
```
```

Trials 6:

```text
```json
{"vendor":"V06-01","landed_cost":1500,"eligible_vendors":1,"delivery_days":3}
```
```

Trials 7:

```text
```json
{"vendor":"V07-01","landed_cost":1500,"eligible_vendors":1,"delivery_days":1}
```
```

Trials 8:

```text
```json
{"vendor":"V08-01","landed_cost":17*162 + 118 - 5 - 1*162 + 1*162 + 1*162 + 1*162 + 1*162 + 1*162 + 1*162 + 1*162 + 1*162 +
```

Trials 9:

```text
```json
{"vendor":"V09-01","landed_cost":1500,"eligible_vendors":1,"delivery_days":3}
```
```

Trials 10:

```text
```json
{"vendor":"V10-01","landed_cost":1500,"eligible_vendors":1,"delivery_days":1}
```
```

### BF16

Trials 1:

```text
```json
{"vendor":"V01-01","landed_cost":1500,"eligible_vendors":1,"delivery_days":1}
```
```

Trials 2:

```text
```json
{"vendor":"V02-01","landed_cost":1500,"eligible_vendors":1,"delivery_days":1}
```
```

Trials 3:

```text
```json
{"vendor":"V03-01","landed_cost":1500,"eligible_vendors":1,"delivery_days":3}
```
```

Trials 4:

```text
```json
{"vendor":"V04-01","landed_cost":1500,"eligible_vendors":1,"delivery_days":1}
```
```

Trials 5:

```text
```json
{"vendor":"V05-01","landed_cost":1500,"eligible_vendors":1,"delivery_days":1}
```
```

Trials 6:

```text
```json
{"vendor":"V06-01","landed_cost":1500,"eligible_vendors":1,"delivery_days":3}
```
```

Trials 7:

```text
```json
{"vendor":"V07-01","landed_cost":1500,"eligible_vendors":1,"delivery_days":1}
```
```

Trials 8:

```text
```json
{"vendor":"V08-01","landed_cost":17*162 + 118 - 5 - 1*162 + 1*162 + 1*162 + 1*162 + 1*162 + 1*162 + 1*162 + 1*162 + 1*162 +
```

Trials 9:

```text
```json
{"vendor":"V09-01","landed_cost":1500,"eligible_vendors":1,"delivery_days":3}
```
```

Trials 10:

```text
```json
{"vendor":"V10-01","landed_cost":1500,"eligible_vendors":1,"delivery_days":1}
```
```

### FP8

Trials 1:

```text
```json
{"vendor": "V01-01", "landed_cost": 1500, "eligible_vendors": 2, "delivery_days": 3}
```
```

Trials 2:

```text
```json
{"vendor": "V02-01", "landed_cost": 1500, "eligible_vendors": 2, "delivery_days": 3}
```
```

Trials 3:

```text
```json
{"vendor": "V03-01", "landed_cost": 1500, "eligible_vendors": 2, "delivery_days": 3}
```
```

Trials 4:

```text
```json
{"vendor": "V04-01", "landed_cost": 1500, "eligible_vendors": 2, "delivery_days": 4}
```
```

Trials 5:

```text
```json
{"vendor": "V05-01", "landed_cost": 1500, "eligible_vendors": 2, "delivery_days": 3}
```
```

Trials 6:

```text
```json
{"vendor": "V06-01", "landed_cost": 1500, "eligible_vendors": 2, "delivery_days": 3}
```
```

Trials 7:

```text
```json
{"vendor": "V07-01", "landed_cost": 1500, "eligible_vendors": 2, "delivery_days": 3}
```
```

Trials 8:

```text
```json
{"vendor": "V08-01", "landed_cost": 1700, "eligible_vendors": 1, "delivery_days": 1}
```
```

Trials 9:

```text
```json
{"vendor": "V09-01", "landed_cost": 1500, "eligible_vendors": 2, "delivery_days": 3}
```
```

Trials 10:

```text
```json
{"vendor": "V10-01", "landed_cost": 1500, "eligible_vendors": 2, "delivery_days": 1}
```
```

### INT4

Trials 1:

```text
```json
{"vendor": "V01-01", "landed_cost": 1500, "eligible_vendors": 2, "delivery_days": 3}
```
```

Trials 2:

```text
```json
{"vendor": "V02-01", "landed_cost": 1500, "eligible_vendors": 2, "delivery_days": 3}
```
```

Trials 3:

```text
```json
{"vendor": "V03-01", "landed_cost": 1500, "eligible_vendors": 2, "delivery_days": 3}
```
```

Trials 4:

```text
```json
{"vendor": "V04-01", "landed_cost": 1500, "eligible_vendors": 2, "delivery_days": 3}
```
```

Trials 5:

```text
```json
{"vendor": "V05-01", "landed_cost": 1500, "eligible_vendors": 2, "delivery_days": 3}
```
```

Trials 6:

```text
```json
{"vendor": "EXAMPLE", "landed_cost": 1500, "eligible_vendors": 2, "delivery_days": 3}
```
```

Trials 7:

```text
```json
{"vendor": "V07-01", "landed_cost": 1500, "eligible_vendors": 2, "delivery_days": 3}
```
```

Trials 8:

```text
```json
{"vendor": "V08-01", "landed_cost": 1500, "eligible_vendors": 2, "delivery_days": 3}
```
```

Trials 9:

```text
```json
{"vendor": "V09-01", "landed_cost": 1500, "eligible_vendors": 2, "delivery_days": 3}
```
```

Trials 10:

```text
```json
{"vendor": "V10-01", "landed_cost": 1500, "eligible_vendors": 2, "delivery_days": 3}
```
```

### FP8_A8

Trials 1:

```text
```json
{"vendor":"V01-01","landed_cost":1100,"eligible_vendors":1,"delivery_days":4}
```
```

Trials 2:

```text
```json
{"vendor":"V02-01","landed_cost":1500,"eligible_vendors":2,"delivery_days":3}
```
```

Trials 3:

```text
```json
{"vendor": "V03-01", "landed_cost": 1500, "eligible_vendors": 2, "delivery_days": 3}
```
```

Trials 4:

```text
```json
{"vendor":"V04-01","landed_cost":1500,"eligible_vendors":2,"delivery_days":3}
```
```

Trials 5:

```text
```json
{"vendor":"V05-01","landed_cost":1500,"eligible_vendors":2,"delivery_days":3}
```
```

Trials 6:

```text
```json
{"vendor": "V06-01", "landed_cost": 1500, "eligible_vendors": 2, "delivery_days": 3}
```
```

Trials 7:

```text
```json
{"vendor":"V07-01","landed_cost":1500,"eligible_vendors":2,"delivery_days":3}
```
```

Trials 8:

```text
```json
{"vendor":"V08-01","landed_cost":1700,"eligible_vendors":1,"delivery_days":5}
```
```

Trials 9:

```text
```json
{"vendor":"V09-01","landed_cost":1500,"eligible_vendors":2,"delivery_days":3}
```
```

Trials 10:

```text
```json
{"vendor":"V10-01","landed_cost":1500,"eligible_vendors":2,"delivery_days":3}
```
```

## Long answers

### FP32

Trials 1:

```text
```json
{
  "destination": "BDG",
  "available_units": 255,
  "shortfall_units": 909,
  "action": "REORDER"
}
```
```

Trials 2:

```text
```json
{
  "destination": "SYB",
  "available_units": 336,
  "shortfall_units": 0,
  "action": "RELEASE"
}
```
```

Trials 3:

```text
```json
{
  "destination": "SMG",
  "available_units": 371,
  "shortfall_units": 927 - 371 = 556,
  "action": "REORDER"
}
```
```

Trials 4:

```text
```json
{
  "destination": "BDG",
  "available_units": 360,
  "shortfall_units": 210,
  "action": "REORDER"
}
```
```

Trials 5:

```text
```json
{
  "destination": "SYB",
  "available_units": 441,
  "shortfall_units": 945 - 441 = 504,
  "action": "REORDER"
}
```
```

Trials 6:

```text
```json
{
  "destination": "SMG",
  "available_units": 476,
  "shortfall_units": 0,
  "action": "RELEASE"
}
```
```

Trials 7:

```text
```json
{
  "destination": "BDG",
  "available_units": 511,
  "shortfall_units": 963 - 511 = 452,
  "action": "REORDER"
}
```
```

Trials 8:

```text
```json
{
  "destination": "SYB",
  "available_units": 523,
  "shortfall_units": 230,
  "action": "REORDER"
}
```
```

Trials 9:

```text
```json
{
  "destination": "SMG",
  "available_units": 581,
  "shortfall_units": 0,
  "action": "RELEASE"
}
```
```

Trials 10:

```text
{
  "destination": "BDG",
  "available_units": 570,
  "shortfall_units": 240,
  "action": "REORDER"
}
```

### BF16

Trials 1:

```text
{
  "destination": "BDG",
  "available_units": 255,
  "shortfall_units": 909 - 255 = 654,
  "action": "REORDER"
}
```

Trials 2:

```text
{
  "destination": "SYB",
  "available_units": 336,
  "shortfall_units": 0,
  "action": "RELEASE"
}
```

Trials 3:

```text
{
  "destination": "SMG",
  "available_units": 371,
  "shortfall_units": 927 - 371 = 556,
  "action": "REORDER"
}
```

Trials 4:

```text
{
  "destination": "BDG",
  "available_units": 360,
  "shortfall_units": 210 - 360 = -150,
  "action": "RELEASE"
}
```

Trials 5:

```text
{
  "destination": "SYB",
  "available_units": 441,
  "shortfall_units": 945 - 441 = 504,
  "action": "REORDER"
}
```

Trials 6:

```text
```json
{
  "destination": "SMG",
  "available_units": 476,
  "shortfall_units": 0,
  "action": "RELEASE"
}
```
```

Trials 7:

```text
{
  "destination": "BDG",
  "available_units": 511,
  "shortfall_units": 963 - 511 = 452,
  "action": "REORDER"
}
```

Trials 8:

```text
```json
{
  "destination": "SYB",
  "available_units": 523,
  "shortfall_units": 230,
  "action": "REORDER"
}
```
```

Trials 9:

```text
```json
{
  "destination": "SMG",
  "available_units": 581,
  "shortfall_units": 0,
  "action": "RELEASE"
}
```
```

Trials 10:

```text
{
  "destination": "BDG",
  "available_units": 570,
  "shortfall_units": 240,
  "action": "REORDER"
}
```

### FP8

Trials 1:

```text
```json
{
  "destination": "BDG",
  "available_units": 255,
  "shortfall_units": 0,
  "action": "RELEASE"
}
```
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
  "destination": "SMG",
  "available_units": 371,
  "shortfall_units": 0,
  "action": "RELEASE"
}
```

Trials 4:

```text
{
  "destination": "BDG",
  "available_units": 360,
  "shortfall_units": 210 - 360 = -150,
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
  "destination": "SMG",
  "available_units": 476,
  "shortfall_units": 0,
  "action": "RELEASE"
}
```

Trials 7:

```text
{
  "destination": "BDG",
  "available_units": 465,
  "shortfall_units": 963 - 465 = 498,
  "action": "REORDER"
}
```

Trials 8:

```text
{
  "destination": "Surabaya",
  "available_units": 523,
  "shortfall_units": 230,
  "action": "REORDER"
}
```

Trials 9:

```text
{
  "destination": "SMG",
  "available_units": 581,
  "shortfall_units": 0,
  "action": "RELEASE"
}
```

Trials 10:

```text
{
  "destination": "BDG",
  "available_units": 50,
  "shortfall_units": 25,
  "action": "REORDER"
}
```

### INT4

Trials 1:

```text
```json
{
  "destination": "Example City",
  "available_units": 255,
  "shortfall_units": 25,
  "action": "REORDER"
}
```
```

Trials 2, 3, 4, 5, 6, 7, 9, 10:

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

Trials 8:

```text
```json
{
  "destination": "Example City",
  "available_units": 500,
  "shortfall_units": 25,
  "action": "REORDER"
}
```
```

### FP8_A8

Trials 1:

```text
{
  "destination": "BDG",
  "available_units": 255,
  "shortfall_units": 909 - 255 = 654,
  "action": "REORDER"
}
```

Trials 2:

```text
{
  "destination": "Surabaya",
  "available_units": 313,
  "shortfall_units": 200,
  "action": "REORDER"
}
```

Trials 3:

```text
{
  "destination": "SMG",
  "available_units": 371,
  "shortfall_units": 0,
  "action": "RELEASE"
}
```

Trials 4:

```text
{
  "destination": "BDG",
  "available_units": 360,
  "shortfall_units": 210 - 360 = -150,
  "action": "REORDER"
}
```

Trials 5:

```text
{
  "destination": "Surabaya",
  "available_units": 418,
  "shortfall_units": 945 - 418 = 527,
  "action": "REORDER"
}
```

Trials 6:

```text
{
  "destination": "SMG",
  "available_units": 476,
  "shortfall_units": 0,
  "action": "RELEASE"
}
```

Trials 7:

```text
```json
{
  "destination": "BDG",
  "available_units": 465,
  "shortfall_units": 963 - 465 = 498,
  "action": "REORDER"
}
```
```

Trials 8:

```text
{
  "destination": "Surabaya",
  "available_units": 523,
  "shortfall_units": 25,
  "action": "REORDER"
}
```

Trials 9:

```text
{
  "destination": "SMG",
  "available_units": 581,
  "shortfall_units": 0,
  "action": "RELEASE"
}
```

Trials 10:

```text
{
  "destination": "BDG",
  "available_units": 50,
  "shortfall_units": 25,
  "action": "REORDER"
}
```
