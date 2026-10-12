# vLLM precision comparison: case averages

Model: `models/7ec86880db931fb2/BF16`; source: `local:models/7ec86880db931fb2/BF16`.
Hardware: Apple M1 Pro, 16 GiB unified RAM, Darwin 15.5. Backend: vLLM-Metal.

10 measured generations per precision/context (150 requested in total). Batch size 1; temperature 0; seed 42; prefix caching disabled.
Each round rotates context order; all precisions use the same schedule and the same token IDs. The model is loaded once per precision.
Means include the first measured request. No extra benchmark warm-up is added. Engine initialization/profile/warm-up passes are outside generation timing.
Each round uses a different editable prompt and expected answer per context. Means and sample deviations summarize variation across these cases and their output lengths.
Elapsed time includes prompt prefill, decoding, and API overhead; tokens/s is end-to-end output throughput.
Output limit: 96 tokens. 50 returned responses reached the limit; truncated answers are retained and graded as returned.
Model download, conversion, and engine loading are timed separately. First requests can include lazy kernel initialization.
Metal FP8 uses MXFP8 E4M3 weights with BF16 inputs; INT4 uses affine weights. This measures local Metal inference.
FP8_A8 applies activation quantize/dequantize rounding with BF16 buffers. Some tensors and reductions retain higher precision.
Weight size is the saved tensor payload, including scales and unquantized tensors; it is not total runtime memory.
Prepared Metal files are audited against their requested storage format.
RSS is the cumulative driver-process high-water mark, not the complete engine/GPU memory usage.

| Precision | Context | Status | Completed / requested | Mean input tokens | Mean seconds ± SD | Mean TTFT ms ± SD | TTFT measured / completed | Mean tokens/s | Weight MiB | Mean correct fields | Answer pass rate | Speedup vs FP32 |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| FP32 | Short | complete | 10 / 10 | 251.7 | 5.105 ± 2.801 | 1452.5 ± 1727.4 | 10/10 | 11.8 | 6563.5 | 0.0% | 0.0% | 1.00 |
| FP32 | Medium | complete | 10 / 10 | 1017.4 | 9.092 ± 2.180 | 3118.0 ± 1244.1 | 10/10 | 11.1 | 6563.5 | 0.0% | 0.0% | 1.00 |
| FP32 | Long | complete | 10 / 10 | 4090.5 | 26.967 ± 3.802 | 22715.9 ± 880.9 | 10/10 | 2.2 | 6563.5 | 20.0% | 0.0% | 1.00 |
| BF16 | Short | complete | 10 / 10 | 251.7 | 1.509 ± 0.221 | 268.5 ± 21.4 | 10/10 | 34.4 | 3281.7 | 0.0% | 0.0% | 3.38 |
| BF16 | Medium | complete | 10 / 10 | 1017.4 | 3.402 ± 0.066 | 970.4 ± 42.0 | 10/10 | 28.2 | 3281.7 | 0.0% | 0.0% | 2.67 |
| BF16 | Long | complete | 10 / 10 | 4090.5 | 7.294 ± 0.801 | 5590.9 ± 281.0 | 10/10 | 7.5 | 3281.7 | 25.0% | 0.0% | 3.70 |
| FP8 | Short | complete | 10 / 10 | 251.7 | 0.884 ± 0.027 | 319.3 ± 12.4 | 10/10 | 46.8 | 1692.3 | 0.0% | 0.0% | 5.78 |
| FP8 | Medium | complete | 10 / 10 | 1017.4 | 2.004 ± 0.471 | 1254.0 ± 5.9 | 10/10 | 23.4 | 1692.3 | 15.0% | 0.0% | 4.54 |
| FP8 | Long | complete | 10 / 10 | 4090.5 | 7.584 ± 0.614 | 6145.3 ± 308.8 | 10/10 | 9.4 | 1692.3 | 10.0% | 0.0% | 3.56 |
| INT4 | Short | complete | 10 / 10 | 251.7 | 0.901 ± 0.066 | 298.7 ± 8.7 | 10/10 | 70.8 | 923.2 | 0.0% | 0.0% | 5.66 |
| INT4 | Medium | complete | 10 / 10 | 1017.4 | 2.195 ± 0.013 | 1176.4 ± 4.5 | 10/10 | 43.7 | 923.2 | 0.0% | 0.0% | 4.14 |
| INT4 | Long | complete | 10 / 10 | 4090.5 | 6.725 ± 0.473 | 5684.9 ± 9.2 | 10/10 | 9.8 | 923.2 | 7.5% | 0.0% | 4.01 |
| FP8_A8 | Short | complete | 10 / 10 | 251.7 | 1.303 ± 0.200 | 776.8 ± 50.4 | 10/10 | 27.3 | 1692.3 | 20.0% | 0.0% | 3.92 |
| FP8_A8 | Medium | complete | 10 / 10 | 1017.4 | 4.136 ± 0.209 | 3473.9 ± 136.6 | 10/10 | 10.2 | 1692.3 | 20.0% | 0.0% | 2.20 |
| FP8_A8 | Long | complete | 10 / 10 | 4090.5 | 16.590 ± 0.623 | 15433.5 ± 306.2 | 10/10 | 3.4 | 1692.3 | 12.5% | 0.0% | 1.63 |

Observed runtime limitation: the installed vLLM/Metal stack logged a segmentation fault during engine shutdown for BF16, FP8, INT4, FP8_A8. Completed generation results were saved before shutdown. See the corresponding engine logs; a clean teardown is not verified.

## Fixed FP8 weights: activation comparison

FP8 uses BF16 activations. FP8_A8 rounds quantized projection inputs to MXFP8 with mx.qqmm, then computes with BF16 buffers. A quantized tied output head also receives rounding. This is a quantize/dequantize experiment, not native FP8 arithmetic or persistent FP8 activation storage. Embedding lookups, attention and the KV cache retain BF16 behavior.

Both cases reuse one FP8 checkpoint, the same prompt token IDs, BF16 KV dtype, cache block size/count, generation settings and rotating trial schedule. Verified pairs check checkpoint/cache/settings identity, prompt hashes, token counts and reference answers. Sequential engine runs can still differ due to system load and compilation; means include first-request work.

| Model/tier | Context | Case | Completed | Verified pairs | Mean latency s | Mean TTFT ms | TTFT coverage | Mean field accuracy | Answer pass | Mean MLX peak MiB | Peak coverage | Mean engine RSS after MiB | RSS coverage |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Single model | Short | FP8 / BF16 activations | 10/10 | 10 | 0.884 | 319.349 | 10/10 | 0.000% | 0.000% | 2553.813 | 10/10 | 2367.911 | 10/10 |
| Single model | Short | FP8_A8 / FP8-rounded activations | 10/10 | 10 | 1.303 | 776.819 | 10/10 | 20.000% | 0.000% | 2582.089 | 10/10 | 2318.342 | 10/10 |
| Single model | Medium | FP8 / BF16 activations | 10/10 | 10 | 2.004 | 1253.979 | 10/10 | 15.000% | 0.000% | 2644.834 | 10/10 | 2329.372 | 10/10 |
| Single model | Medium | FP8_A8 / FP8-rounded activations | 10/10 | 10 | 4.136 | 3473.915 | 10/10 | 20.000% | 0.000% | 2689.563 | 10/10 | 2286.625 | 10/10 |
| Single model | Long | FP8 / BF16 activations | 10/10 | 10 | 7.584 | 6145.328 | 10/10 | 10.000% | 0.000% | 2629.055 | 10/10 | 2311.561 | 10/10 |
| Single model | Long | FP8_A8 / FP8-rounded activations | 10/10 | 10 | 16.590 | 15433.483 | 10/10 | 12.500% | 0.000% | 2674.058 | 10/10 | 2270.667 | 10/10 |

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
{"item":"MONITOR","available_units":23+10+15+20+6+11+16+21+7-5,"fulfillable":available_units >= 37}
```

Trials 2:

```text
{"item":"KEYBOARD","available_units":34+17+3+8+13+18+4+9+14-7,"fulfillable":available_units >= 200}
```

Trials 3:

```text
{"item":"ROUTER","available_units":45+5+10+15+20+6+11+16+21-9,"fulfillable":available_units >= 47}
```

Trials 4:

```text
{"item":"PRINTER","available_units":56+12+17+3+8+13+18+4+9-11,"fulfillable":false}
```

Trials 5:

```text
{"item":"TABLET","available_units":67+19+5+10+15+20+6+11+16-13,"fulfillable":(67+19+5+10+15+20+6+11+16-13)>=57}
```

Trials 6:

```text
{"item":"SCANNER","available_units":78+7+12+17+3+8+13+18+4-15,"fulfillable":available_units >= 260}
```

Trials 7:

```text
{"item":"WEBCAM","available_units":89+14+19+5+10+15+20+6+11-17,"fulfillable":available_units >= 67}
```

Trials 8:

```text
{"item":"HEADSET","available_units":100+21+7+12+17+3+8+13+18-19,"fulfillable":available_units >= 290}
```

Trials 9:

```text
{"item":"SPEAKER","available_units":111+9+14+19+5+10+15+20+6-21,"fulfillable":available_units >= 77}
```

Trials 10:

```text
{"item":"PROJECTOR","available_units":122+16+21+7+12+17+3+8+13-23,"fulfillable":available_units >= 320}
```

### BF16

Trials 1:

```text
{"item":"MONITOR","available_units":23+10+15+20+6+11+16+21+7-5,"fulfillable":available_units >= 37}
```

Trials 2:

```text
{"item":"KEYBOARD","available_units":34+17+3+8+13+18+4+9+14-7,"fulfillable":available_units >= 200}
```

Trials 3:

```text
{"item":"ROUTER","available_units":45+5+10+15+20+6+11+16+21-9,"fulfillable":available_units >= 47}
```

Trials 4:

```text
{"item":"PRINTER","available_units":56+12+17+3+8+13+18+4+9-11,"fulfillable":available_units >= 230}
```

Trials 5:

```text
{"item":"TABLET","available_units":67+19+5+10+15+20+6+11+16-13,"fulfillable":(67+19+5+10+15+20+6+11+16-13)>=57}
```

Trials 6:

```text
{"item":"SCANNER","available_units":78+7+12+17+3+8+13+18+4-15,"fulfillable":available_units >= 260}
```

Trials 7:

```text
{"item":"WEBCAM","available_units":89+14+19+5+10+15+20+6+11-17,"fulfillable":available_units >= 67}
```

Trials 8:

```text
{
  "item": "HEADSET",
  "available_units": 100 + 21 + 7 + 12 + 17 + 3 + 8 + 13 + 18 - 19,
  "fulfillable": available_units >= 290
}
```

Trials 9:

```text
{"item":"SPEAKER","available_units":111+9+14+19+5+10+15+20+6-21,"fulfillable":available_units >= 77}
```

Trials 10:

```text
{"item":"PROJECTOR","available_units":122+16+21+7+12+17+3+8+13-23,"fulfillable":available_units >= 320}
```

### FP8

Trials 1:

```text
{"item":"MONITOR","available_units":23+10+15+20+6+11+21+7-5,"fulfillable":false}
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
{"item":"PRINTER","available_units":56+12+17+3+8+13+4+9-11,"fulfillable":false}
```

Trials 5:

```text
{"item":"TABLET","available_units":67+19+5+10+15+20+6+11+16-13,"fulfillable":false}
```

Trials 6:

```text
{"item":"SCANNER","available_units":78+7+12+17+3+8+13+18+4-15,"fulfillable":false}
```

Trials 7:

```text
{"item":"WEBCAM","available_units":89+14+19+5+10+15+6+11-17,"fulfillable":false}
```

Trials 8:

```text
{"item":"HEADSET","available_units":100+21+7+12+17+3+8+13+18-19,"fulfillable":false}
```

Trials 9:

```text
{"item":"SPEAKER","available_units":111+9+14+19+5+10+15+20+6-21,"fulfillable":false}
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
  "fulfillable": available_units >= 37
}
```

Trials 2:

```text
{"item":"KEYBOARD","available_units":34+17+3+8+13+18+4+9+14-7,"fulfillable":available_units >= 200}
```

Trials 3:

```text
{
  "item": "ROUTER",
  "available_units": 45 + 5 + 10 + 15 + 20 + 6 + 11 + 16 + 21 - 9,
  "fulfillable": available_units >= 47
}
```

Trials 4:

```text
{
  "item": "PRINTER",
  "available_units": 56 + 12 + 17 + 3 + 8 + 13 + 18 + 4 + 9 - 11,
  "fulfillable": available_units >= 230
}
```

Trials 5:

```text
{
  "item": "TABLET",
  "available_units": 67 + 19 + 5 + 10 + 15 + 20 + 6 + 11 + 16 - 13,
  "fulfillable": available_units >= 57
}
```

Trials 6:

```text
{
  "item": "SCANNER",
  "available_units": 78 + 7 + 12 + 17 + 3 + 8 + 13 + 18 + 4 - 15,
  "fulfillable": available_units >= 260
}
```

Trials 7:

```text
{
  "item": "WEBCAM",
  "available_units": 89 + 14 + 19 + 5 + 10 + 15 + 20 + 6 + 11 - 17,
  "fulfillable": available_units >= 67
}
```

Trials 8:

```text
{
  "item": "HEADSET",
  "available_units": 100 + 21 + 7 + 12 + 17 + 3 + 8 + 13 + 18 - 19,
  "fulfillable": available_units >= 290
}
```

Trials 9:

```text
{
  "item": "SPEAKER",
  "available_units": 111 + 9 + 14 + 19 + 5 + 10 + 15 + 20 + 6 - 21,
  "fulfillable": available_units >= 77
}
```

Trials 10:

```text
{
  "item": "PROJECTOR",
  "available_units": 122 + 16 + 21 + 7 + 12 + 17 + 3 + 8 + 13 - 23,
  "fulfillable": available_units >= 320
}
```

### FP8_A8

Trials 1:

```text
{"item":"MONITOR","available_units":47,"fulfillable":true}
```

Trials 2:

```text
{"item":"KEYBOARD","available_units":34+17+3+8+13+18+4+9+14-7, "fulfillable":false}
```

Trials 3:

```text
{"item":"ROUTER","available_units":45 + 5 + 10 + 15 + 20 + 6 + 11 + 16 + 21 - 9, "fulfillable":false}
```

Trials 4:

```text
{"item":"PRINTER","available_units":56+12+17+3+8+13+18+4+9-11,"fulfillable":false}
```

Trials 5:

```text
{"item":"TABLET","available_units":105,"fulfillable":true}
```

Trials 6:

```text
{"item":"SCANNER","available_units":144,"fulfillable":false}
```

Trials 7:

```text
{"item":"WEBCAM","available_units":89+14+19+5+10+15+20+6+11-17, "fulfillable":false}
```

Trials 8:

```text
{"item":"HEADSET","available_units":100+21+7+12+17+3+8+13+18-19, "fulfillable":false}
```

Trials 9:

```text
{"item":"SPEAKER","available_units":111+9+14+19+5+10+15+20+6-21, "fulfillable":false}
```

Trials 10:

```text
{"item":"PROJECTOR","available_units":122+16+21+7+12+17+3+8+13-23,"fulfillable":false}
```

## Medium answers

### FP32

Trials 1:

```text
To determine the lowest eligible cost, we need to evaluate each quote that meets the criteria:

1. **Certified**.
2. **Capacity for the entire order** (99 units).
3. **Delivery within 4 days**.

Let's filter the quotes that meet these criteria:

- **V01-01**: Certified, capacity 124 units (not enough), delivery 1 day → **not eligible**.
- **V01-
```

Trials 2:

```text
To determine the lowest eligible cost, we need to evaluate each quote that meets the criteria:

1. **Certified**.
2. **Capacity for the entire order** (108 units).
3. **Delivery within 5 days**.
4. **No tax** (so no additional cost).

Let's filter the quotes that meet these criteria:

- **V02-01**: Certified, capacity 133 units (not enough), delivery 1
```

Trials 3:

```text
To determine the lowest eligible cost, we need to evaluate each quote that meets the criteria:

- Certified
- Capacity for the entire order (117 units)
- Delivery within 3 days

Let's filter the quotes:

**Eligible quotes**:
- V03-01: certified, capacity 142 units (≥117), delivery 1 day
- V03-02: certified, capacity 142 units
```

Trials 4:

```text
To determine the lowest eligible cost, we need to evaluate each quote that meets the criteria:

1. **Certified**.
2. **Capacity for the entire order** (126 units).
3. **Delivery within 4 days**.

Let's filter the quotes that meet these criteria:

- **V04-01**: Certified, capacity 151 units (sufficient), delivery 1 day (within 4 days).
- **V04
```

Trials 5:

```text
To determine the lowest eligible cost, we need to evaluate each quote that meets the criteria:

1. **Certified**.
2. **Capacity for the entire order** (135 units).
3. **Delivery within 5 days**.

Let's filter the quotes that meet these criteria:

- **V05-01**: Certified, capacity 160 units (≥135), delivery 1 day.
- **V05-02
```

Trials 6:

```text
To determine the lowest eligible cost, we need to evaluate each quote that meets the criteria:

1. **Certified**.
2. **Capacity for the entire order** (144 units).
3. **Delivery within 3 days**.

Let's filter the quotes that meet these criteria:

- **V06-01**: Certified, capacity 169 units (insufficient), delivery 1 day (valid).
- **V06-02
```

Trials 7:

```text
To determine the lowest eligible cost, we need to evaluate each quote that meets the criteria:

1. **Certified**.
2. **Capacity for the entire order** (153 units).
3. **Delivery within 4 days**.

Let's filter the quotes that meet these criteria:

- **V07-01**: Certified, capacity 178 units (insufficient), delivery 1 day (within 4 days) → **Not eligible**
```

Trials 8:

```text
To determine the lowest eligible cost, we need to evaluate each quote that meets the criteria:

1. **Certified**.
2. **Capacity for the entire order (162 units)**.
3. **Delivery within 5 days**.

Let's filter the quotes that meet these criteria:

- **V08-01**: Certified, capacity 187 units (≥162), delivery 1 day.
- **V08-02
```

Trials 9:

```text
To determine the lowest eligible cost, we need to evaluate each quote that meets the criteria:

1. **Certified**.
2. **Capacity for the entire order** (171 units).
3. **Delivery within 3 days**.

Let's filter the quotes that meet these criteria:

- **V09-01**: Certified, capacity 196 units (≥171), delivery 1 day.
- **V09-06
```

Trials 10:

```text
To determine the lowest eligible cost, we need to evaluate each quote that meets the criteria:

1. **Certified**.
2. **Capacity for the entire order (180 units)**.
3. **Delivery within 4 days**.

Let's filter the quotes that meet these criteria:

- **V10-01**: Certified, capacity 205 units (≥ 180), delivery 1 day (≤ 4).
- **V
```

### BF16

Trials 1:

```text
To determine the lowest eligible cost, we need to filter the quotes based on the following criteria:

1. **Certified**: Only eligible quotes have "certified yes".
2. **Capacity**: The order quantity must be at least 99 units.
3. **Delivery days**: Must be 4 days or less.
4. **Unit price**: Must be such that the total cost (including shipping and discount) is minimized.

Let's evaluate the eligible quotes:

- **
```

Trials 2:

```text
To determine the lowest eligible cost, we need to evaluate each quote that meets the criteria:

1. **Certified**.
2. **Capacity for the entire order** (108 units).
3. **Delivery within 5 days**.
4. **No tax** (so no additional cost).

Let's filter the quotes that meet these criteria:

- **V02-01**: Certified, capacity 133 units (not enough), delivery 1
```

Trials 3:

```text
To determine the lowest eligible cost, we need to evaluate each quote that is eligible based on the given criteria:

### Eligibility Criteria:
- **Certified**: Yes
- **Capacity for the entire order**: Must be ≥ 117 units
- **Delivery within 3 days**: Must be ≤ 3 days
- **Unit price, shipping, and fixed discount must be valid**

### Eligible Quotes:
- **V03-01**: Unit price
```

Trials 4:

```text
To determine the lowest eligible cost, we need to evaluate each quote that meets the criteria:

1. **Certified**.
2. **Capacity for the entire order** (126 units).
3. **Delivery within 4 days**.

Let's filter the quotes that meet these criteria:

- **V04-01**: Certified, capacity 151 units (sufficient), delivery 1 day (within 4 days).
- **V04
```

Trials 5:

```text
To determine the lowest eligible cost, we need to evaluate each quote that meets the criteria:

1. **Certified**.
2. **Capacity for the entire order** (135 units).
3. **Delivery within 5 days**.

Let's filter the quotes that meet these criteria:

- **V05-01**: Certified, capacity 160 units (≥135), delivery 1 day.
- **V05-02
```

Trials 6:

```text
To determine the lowest eligible cost, we need to evaluate each quote that meets the criteria:

- Certified
- Capacity for the entire order (144 units)
- Delivery within 3 days

Let's filter the quotes:

**Eligible quotes:**
- V06-01: certified, capacity 169 units, delivery 1 day (144 units ≤ 169)
- V06-02: certified, capacity
```

Trials 7:

```text
To determine the lowest eligible cost, we need to evaluate each quote that meets the criteria:

1. **Certified**.
2. **Capacity for the entire order** (153 units).
3. **Delivery within 4 days**.

Let's filter the quotes that meet these criteria:

- **V07-01**: Certified, capacity 178 units (sufficient), delivery 1 day.
- **V07-02**: Certified
```

Trials 8:

```text
To determine the lowest eligible cost, we need to evaluate each quote that meets the criteria:

1. **Certified**.
2. **Capacity for the entire order (162 units)**.
3. **Delivery within 5 days**.

Let's filter the quotes that meet these criteria:

- **V08-01**: Certified, capacity 187 units (≥162), delivery 1 day.
- **V08-02
```

Trials 9:

```text
To determine the lowest eligible cost, we need to evaluate each quote based on the following criteria:

1. **Certified**: Only eligible quotes with "certified yes".
2. **Capacity for the entire order**: The quote must have a capacity equal to or greater than 171 units.
3. **Delivery within 3 days**: The delivery days must be ≤ 3.
4. **Landed cost calculation**:
   - Landed cost = (Order quantity
```

Trials 10:

```text
To determine the lowest eligible cost, we need to evaluate each quote that meets the criteria:

1. **Certified**.
2. **Capacity for the entire order (180 units)**.
3. **Delivery within 4 days**.

Let's filter the quotes that meet these criteria:

- **V10-01**: Certified, capacity 205 units (≥ 180), delivery 1 day (≤ 4).
- **V
```

### FP8

Trials 1:

```text
{"vendor":"V01-01","landed_cost":1500,"eligible_vendors":2,"delivery_days":1}
```

Trials 2:

```text
{"vendor":"V02-01","landed_cost":1500,"eligible_vendors":2,"delivery_days":1}
```

Trials 3:

```text
{"vendor":"V03-01","landed_cost":1500,"eligible_vendors":2,"delivery_days":1}
```

Trials 4:

```text
{"vendor":"V04-01","landed_cost":1500,"eligible_vendors":2,"delivery_days":1}
```

Trials 5:

```text
{"vendor":"V05-01","landed_cost":1500,"eligible_vendors":2,"delivery_days":1}
```

Trials 6:

```text
To determine the lowest eligible cost, we need to filter the quotes based on the criteria:

1. **Certified**: Yes
2. **Capacity for the entire order (144 units)**: Yes
3. **Delivery within 3 days**: Yes
4. **No tax**: Already accounted for

We will filter the quotes to include only those that meet these criteria and then calculate the landed cost for each eligible vendor.

### Eligible Quotes:
- V0
```

Trials 7:

```text
{"vendor":"V07-01","landed_cost":1500,"eligible_vendors":2,"delivery_days":1}
```

Trials 8:

```text
{"vendor":"V08-01","landed_cost":1500,"eligible_vendors":2,"delivery_days":1}
```

Trials 9:

```text
To determine the lowest eligible cost for purchasing 171 speaker units, we need to evaluate the quotes that meet the following criteria:

1. **Certified**: Yes
2. **Capacity for the entire order**: 171 units
3. **Delivery within 3 days**: Yes
4. **No tax**: Yes

We will filter the quotes to find those that meet these criteria and then compute the landed cost for each eligible vendor.

### Eligible Quotes
```

Trials 10:

```text
To determine the lowest eligible cost for purchasing 180 projector units in one order, we need to evaluate the quotes that meet the following criteria:

1. **Certified**: Yes
2. **Capacity for the entire order**: 180 units
3. **Delivery within 4 days**

We will filter the quotes to find those that meet these criteria and then compute the landed cost for each eligible vendor.

### Eligible Quotes:
- V10-0
```

### INT4

Trials 1:

```text
To determine the lowest eligible cost, we must evaluate each vendor's quote based on the following criteria:

1. **Certified**: Only eligible quotes.
2. **Capacity for the entire order**: Must match the total order quantity (99 units).
3. **Delivery days**: Lower is better.
4. **Landed cost** = (order quantity × unit price) + shipping fee - fixed discount.

Let’s evaluate each eligible vendor:

---

**V01-0
```

Trials 2:

```text
To determine the lowest eligible cost, we must evaluate each vendor's eligibility and calculate the landed cost.

### Eligibility Criteria:
- Certified
- Capacity for the entire order (108 units)
- Delivery within 5 days

### Valid Vendors:
- V02-01: Certified, capacity 133, delivery 1
- V02-02: Certified, capacity 133, delivery 2
- V02
```

Trials 3:

```text
To determine the lowest eligible cost, we must evaluate each vendor's eligibility and calculate the landed cost.

### Eligibility Criteria:
- Certified
- Capacity for the entire order
- Delivery within the deadline

### Step-by-Step Evaluation:

#### V03-01:
- Certified: Yes
- Capacity: 142 units
- Delivery: 1 day
- Landed cost: 142 * 17 - 15 + (
```

Trials 4:

```text
To determine the lowest eligible cost, we must evaluate each eligible vendor based on the following criteria:

1. **Eligibility**:
   - Certified
   - Capacity for the entire order (126 units)
   - Delivery within 4 days

2. **Cost Calculation**:
   - Landed cost = (order quantity × unit price) + shipping fee - fixed discount
   - No tax

3. **Break ties** by:
   - Fewer
```

Trials 5:

```text
To determine the lowest eligible cost, we must evaluate each vendor's quote based on the following criteria:

1. **Eligibility**:
   - Certified
   - Capacity for the entire order
   - Delivery within the deadline

2. **Cost Calculation**:
   - Landed cost = (order quantity × unit price) + shipping fee - fixed discount

3. **Break ties** by:
   - Fewer delivery days
   - Alphabetically smallest vendor name
```

Trials 6:

```text
To determine the lowest eligible cost, we must evaluate each vendor's eligibility and calculate the landed cost.

### Eligibility Criteria:
- Certified
- Capacity for the entire order (144 units)
- Delivery within 3 days

### Valid Vendors:
- V06-01: Certified, capacity 169, delivery 1 day
- V06-02: Certified, capacity 169, delivery 2 days
- V
```

Trials 7:

```text
To determine the lowest eligible cost, we must evaluate each vendor's eligibility and calculate the landed cost.

### Eligibility Criteria:
- Certified
- Capacity for the entire order (153 units)
- Delivery within 4 days

### Valid Vendors:
- V07-01: Certified, capacity 178, delivery 1 day
- V07-02: Certified, capacity 178, delivery 2 days
- V
```

Trials 8:

```text
To determine the lowest eligible cost, we must evaluate each vendor's eligibility and calculate the landed cost.

### Eligibility Criteria:
- Certified
- Capacity for the entire order (162 units)
- Delivery within 5 days

### Valid Vendors:
- V08-01: Certified, capacity 187, delivery 1
- V08-02: Certified, capacity 187, delivery 2
- V08
```

Trials 9:

```text
To determine the lowest eligible cost, we must evaluate each vendor's eligibility and calculate the landed cost.

### Eligibility Criteria:
- Certified
- Delivery within 3 days
- Capacity for the entire order (171 units)

### Valid Vendors:
- V09-01: Certified, delivery 1 day, capacity 196 units
- V09-05: Certified, delivery 7 days, capacity 143 units

```

Trials 10:

```text
To determine the lowest eligible cost, we must evaluate each vendor based on the following criteria:

1. **Certified**: Only eligible vendors.
2. **Capacity for the entire order**: Must match the total quantity.
3. **Delivery days**: Lower is better.
4. **Landed cost**: Calculated as `order quantity * unit price + shipping fee - fixed discount`.

We will only consider eligible vendors (certified, capacity matches, and delivery days are valid).

###
```

### FP8_A8

Trials 1:

```text
{
  "vendor": "V01-01",
  "landed_cost": 1500,
  "eligible_vendors": 2,
  "delivery_days": 1
}
```

Trials 2:

```text
{"vendor":"V02-01","landed_cost":1500,"eligible_vendors":2,"delivery_days":3}
```

Trials 3:

```text
{
  "vendor": "V03-01",
  "landed_cost": 1500,
  "eligible_vendors": 2,
  "delivery_days": 1
}
```

Trials 4:

```text
{
  "vendor": "V04-01",
  "landed_cost": 1500,
  "eligible_vendors": 2,
  "delivery_days": 1
}
```

Trials 5:

```text
{
  "vendor": "V05-01",
  "landed_cost": 1500,
  "eligible_vendors": 2,
  "delivery_days": 1
}
```

Trials 6:

```text
{
  "vendor": "V06-01",
  "landed_cost": 1500,
  "eligible_vendors": 2,
  "delivery_days": 3
}
```

Trials 7:

```text
{
  "vendor": "V07-01",
  "landed_cost": 153 * 14 + 107 - 0,
  "eligible_vendors": 2,
  "delivery_days": 1
}
```

Trials 8:

```text
{"vendor":"V08-01","landed_cost":1500,"eligible_vendors":2,"delivery_days":1}
```

Trials 9:

```text
{
  "vendor": "V09-01",
  "landed_cost": 1500,
  "eligible_vendors": 2,
  "delivery_days": 1
}
```

Trials 10:

```text
{
  "vendor": "V10-01",
  "landed_cost": 1500,
  "eligible_vendors": 2,
  "delivery_days": 1
}
```

## Long answers

### FP32

Trials 1:

```text
{
  "destination": "Bandung",
  "available_units": 255 + 301 + 255 + 301 + 255 + 301 + 255 + 301 + 255 + 301 + 255 + 301 + 255 + 301 + 255 + 301 + 2
```

Trials 2:

```text
{
  "destination": "Surabaya",
  "available_units": 120,
  "shortfall_units": 80,
  "action": "REORDER"
}
```

Trials 3:

```text
{
  "destination": "Semarang",
  "available_units": 371 + 18 + 21 + 6 + 25 + 13 + 18 + 21 + 6 + 25 + 13 + 18 + 21 + 6 + 25 + 13 + 18 + 21 + 6 + 25 + 13 +
```

Trials 4:

```text
{
  "destination": "Bandung",
  "available_units": 123,
  "shortfall_units": 27,
  "action": "REORDER"
}
```

Trials 5:

```text
{
  "destination": "Surabaya",
  "available_units": 125,
  "shortfall_units": 80,
  "action": "REORDER"
}
```

Trials 6:

```text
{
  "destination": "SMG",
  "available_units": 120,
  "shortfall_units": 10,
  "action": "REORDER"
}
```

Trials 7:

```text
{
  "destination": "Bandung",
  "available_units": 465 + 26 + 26 + 14 + 17 + 14 + 17 + 14 + 17 + 14 + 17 + 14 + 17 + 14 + 17 + 14 + 17 + 14 + 17 + 14 +
```

Trials 8:

```text
{
  "destination": "Surabaya",
  "available_units": 120,
  "shortfall_units": 10,
  "action": "REORDER"
}
```

Trials 9:

```text
{
  "destination": "Semarang",
  "available_units": 581 - 16 - 24 - 27 - 10 - 24 - 27 - 10 - 24 - 27 - 10 - 24 - 27 - 10 - 24 - 27 - 10 - 24 - 27 - 10 -
```

Trials 10:

```text
{
  "destination": "Bandung",
  "available_units": 240,
  "shortfall_units": 0,
  "action": "RELEASE"
}
```

### BF16

Trials 1:

```text
{
  "destination": "Bandung",
  "available_units": 104,
  "shortfall_units": 14,
  "action": "REORDER"
}
```

Trials 2:

```text
{
  "destination": "Surabaya",
  "available_units": 120,
  "shortfall_units": 80,
  "action": "REORDER"
}
```

Trials 3:

```text
{
  "destination": "Semarang",
  "available_units": 371 + 18 + 21 + 6 + 25 + 13 + 18 + 21 + 6 + 25 + 13 + 18 + 21 + 6 + 25 + 13 + 18 + 21 + 6 + 25 + 13 +
```

Trials 4:

```text
{
  "destination": "Bandung",
  "available_units": 123,
  "shortfall_units": 27,
  "action": "REORDER"
}
```

Trials 5:

```text
{
  "destination": "Surabaya",
  "available_units": 125,
  "shortfall_units": 80,
  "action": "REORDER"
}
```

Trials 6:

```text
{
  "destination": "SMG",
  "available_units": 120,
  "shortfall_units": 100,
  "action": "REORDER"
}
```

Trials 7:

```text
{
  "destination": "Bandung",
  "available_units": 465 + 26 + 26 + 14 + 17 + 14 + 17 + 14 + 17 + 14 + 17 + 14 + 17 + 14 + 17 + 14 + 17 + 14 + 17 + 14 +
```

Trials 8:

```text
{
  "destination": "Surabaya",
  "available_units": 120,
  "shortfall_units": 10,
  "action": "REORDER"
}
```

Trials 9:

```text
{
  "destination": "Semarang",
  "available_units": 581 - 47 + 10 + 18 + 21 + 25 + 6 + 18 + 21 + 25 + 6 + 21 + 25 + 6 + 21 + 25 + 6 + 21 + 25 + 6 + 21 +
```

Trials 10:

```text
{
  "destination": "Bandung",
  "available_units": 240,
  "shortfall_units": 0,
  "action": "RELEASE"
}
```

### FP8

Trials 1:

```text
{
  "destination": "Bandung",
  "available_units": 255 + 278 + 301 - 23 - 20 - 27 - 8 - 15 - 24 - 7 - 14 - 21 - 4 - 11 - 18 - 25 - 22 - 5 - 26 - 9 - 26 -
```

Trials 2:

```text
{
  "destination": "Surabaya",
  "available_units": 100,
  "shortfall_units": 25,
  "action": "REORDER"
}
```

Trials 3:

```text
{
  "destination": "Semarang",
  "available_units": 325 + 348 + 371 - 29,
  "shortfall_units": 927 - (325 + 348 + 371 - 29),
  "action": "REORDER"
}
```

Trials 4:

```text
{
  "destination": "Bandung",
  "available_units": 360 + 11 + 8 + 23 + 20 + 11 + 16 + 23 + 8 + 20 + 23 + 16 + 23 + 16 + 23 + 16 + 23 + 16 + 23 + 16 + 23
```

Trials 5:

```text
{
  "destination": "Surabaya",
  "available_units": 104,
  "shortfall_units": 81,
  "action": "REORDER"
}
```

Trials 6:

```text
{
  "destination": "Semarang",
  "available_units": 430 + 453 + 476 - 38,
  "shortfall_units": 220 - (430 + 453 + 476 - 38),
  "action": "REORDER"
}
```

Trials 7:

```text
{
  "destination": "Bandung",
  "available_units": 465 + 26 + 26 + 14 + 17 + 14 + 26 + 14 + 26 + 14 + 26 + 14 + 26 + 14 + 26 + 14 + 26 + 14 + 26 + 14 +
```

Trials 8:

```text
{
  "destination": "Surabaya",
  "available_units": 120,
  "shortfall_units": 10,
  "action": "REORDER"
}
```

Trials 9:

```text
{
  "destination": "Semarang",
  "available_units": 535 + 558 + 581 - 47,
  "shortfall_units": 981 - (535 + 558 + 581 - 47),
  "action": "REORDER"
}
```

Trials 10:

```text
{
  "destination": "Bandung",
  "available_units": 570 + 20 + 17 + 14 + 5 + 17 + 20 + 27 + 11 + 8 + 15 + 12 + 19 + 23 + 20 + 27 + 15 + 12 + 19 + 23 + 20
```

### INT4

Trials 1:

```text
{
  "destination": "BDG",
  "available_units": 255 + 278 + 301 + 9 + 13 + 20 + 10 + 8 + 14 + 21 + 25 + 22 + 5 + 17 + 26 + 9 + 14 + 22 + 5 + 17 + 26 +
```

Trials 2:

```text
{
  "destination": "SBY",
  "available_units": 200,
  "shortfall_units": 0,
  "action": "RELEASE"
}
```

Trials 3:

```text
{
  "destination": "SMG",
  "available_units": 120,
  "shortfall_units": 127,
  "action": "REORDER"
}
```

Trials 4:

```text
{
  "destination": "BDG",
  "available_units": 360 + 11 + 8 + 11 + 23 + 20 + 19 + 23 + 20 + 11 + 20 + 19 + 11 + 20 + 16 + 19 + 16 + 10 + 15 + 12 + 1
```

Trials 5:

```text
{
  "destination": "SBY",
  "available_units": 945,
  "shortfall_units": 0,
  "action": "RELEASE"
}
```

Trials 6:

```text
{
  "destination": "SMG",
  "available_units": 120,
  "shortfall_units": 100,
  "action": "REORDER"
}
```

Trials 7:

```text
{
  "destination": "BDG",
  "available_units": 465 + 26 + 17 + 14 + 26 + 5 + 10 + 17 + 22 + 25 + 22 + 14 + 17 + 26 + 5 + 10 + 17 + 26 + 5 + 10 + 17 +
```

Trials 8:

```text
{
  "destination": "SBY",
  "available_units": 100,
  "shortfall_units": 30,
  "action": "REORDER"
}
```

Trials 9:

```text
{
  "destination": "SMG",
  "available_units": 581 + 22 + 9 + 18 + 21 + 6 + 10 + 17 + 25 + 14 + 21 + 18 + 21 + 10 + 17 + 25 + 14 + 21 + 18 + 21 + 10
```

Trials 10:

```text
{
  "destination": "BDG",
  "available_units": 570 + 20 + 11 + 8 + 11 + 23 + 20 + 19 + 20 + 15 + 12 + 19 + 23 + 20 + 15 + 12 + 19 + 20 + 15 + 12 + 1
```

### FP8_A8

Trials 1:

```text
{
  "destination": "Bandung",
  "available_units": 255 + 278 + 301 - 23 - 20 - 27 - 24 - 24 - 8 - 15 - 20 - 23 - 20 - 23 - 20 - 23 - 20 - 23 - 20 - 23 -
```

Trials 2:

```text
{
  "destination": "Surabaya",
  "available_units": 100,
  "shortfall_units": 25,
  "action": "REORDER"
}
```

Trials 3:

```text
{
  "destination": "Semarang",
  "available_units": 325 + 348 + 371 - 29,
  "shortfall_units": 927 - (325 + 348 + 371 - 29),
  "action": "REORDER"
}
```

Trials 4:

```text
{
  "destination": "Bandung",
  "available_units": 360 + 383 + 406 - 32,
  "shortfall_units": 210 - (360 + 383 + 406 - 32),
  "action": "REORDER"
}
```

Trials 5:

```text
{
  "destination": "Surabaya",
  "available_units": 1045,
  "shortfall_units": 49,
  "action": "REORDER"
}
```

Trials 6:

```text
{
  "destination": "Semarang",
  "available_units": 165,
  "shortfall_units": 15,
  "action": "REORDER"
}
```

Trials 7:

```text
{
  "destination": "Bandung",
  "available_units": 465,
  "shortfall_units": 963 - 465,
  "action": "REORDER"
}
```

Trials 8:

```text
{
  "destination": "Surabaya",
  "available_units": 106,
  "shortfall_units": 24,
  "action": "REORDER"
}
```

Trials 9:

```text
{
  "destination": "Semarang",
  "available_units": 581,
  "shortfall_units": 981 - 581 = 400,
  "action": "REORDER"
}
```

Trials 10:

```text
{
  "destination": "Bandung",
  "available_units": 570 + 593 + 616 - 50,
  "shortfall_units": 240 - (570 + 593 + 616 - 50),
  "action": "REORDER"
}
```
