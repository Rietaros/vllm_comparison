# Model size and precision comparison

Hardware: Apple M1 Pro, 16 GiB unified RAM, Darwin 15.5. Backend: vLLM-Metal.

Requested memory budget: 10.00 GiB; effective device budget: 10.00 GiB. Backend memory fraction: 0.9375. This is a planning budget rather than a measured or hard process-memory cap.

Requested 450 generations; attempted 420; completed 420; hardware-skipped 30; error rows 0. Each model/precision/context cell requests 10 different prompt/answer cases.

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

- **Short / short-01**: Short case 01: monitor decision. Input tokens: 251; records: 0; reference: `{"item": "MONITOR", "available_units": 124, "fulfillable": true}`; comparison: `{"allow_extra_fields": false, "case_sensitive": true}`.
- **Short / short-02**: Short case 02: keyboard decision. Input tokens: 250; records: 0; reference: `{"item": "KEYBOARD", "available_units": 113, "fulfillable": false}`; comparison: `{"allow_extra_fields": false, "case_sensitive": true}`.
- **Short / short-03**: Short case 03: router decision. Input tokens: 251; records: 0; reference: `{"item": "ROUTER", "available_units": 140, "fulfillable": true}`; comparison: `{"allow_extra_fields": false, "case_sensitive": true}`.
- **Short / short-04**: Short case 04: printer decision. Input tokens: 251; records: 0; reference: `{"item": "PRINTER", "available_units": 129, "fulfillable": false}`; comparison: `{"allow_extra_fields": false, "case_sensitive": true}`.
- **Short / short-05**: Short case 05: tablet decision. Input tokens: 252; records: 0; reference: `{"item": "TABLET", "available_units": 156, "fulfillable": true}`; comparison: `{"allow_extra_fields": false, "case_sensitive": true}`.
- **Short / short-06**: Short case 06: scanner decision. Input tokens: 251; records: 0; reference: `{"item": "SCANNER", "available_units": 145, "fulfillable": false}`; comparison: `{"allow_extra_fields": false, "case_sensitive": true}`.
- **Short / short-07**: Short case 07: webcam decision. Input tokens: 253; records: 0; reference: `{"item": "WEBCAM", "available_units": 172, "fulfillable": true}`; comparison: `{"allow_extra_fields": false, "case_sensitive": true}`.
- **Short / short-08**: Short case 08: headset decision. Input tokens: 253; records: 0; reference: `{"item": "HEADSET", "available_units": 180, "fulfillable": false}`; comparison: `{"allow_extra_fields": false, "case_sensitive": true}`.
- **Short / short-09**: Short case 09: speaker decision. Input tokens: 252; records: 0; reference: `{"item": "SPEAKER", "available_units": 188, "fulfillable": true}`; comparison: `{"allow_extra_fields": false, "case_sensitive": true}`.
- **Short / short-10**: Short case 10: projector decision. Input tokens: 253; records: 0; reference: `{"item": "PROJECTOR", "available_units": 196, "fulfillable": false}`; comparison: `{"allow_extra_fields": false, "case_sensitive": true}`.
- **Medium / medium-01**: Medium case 01: monitor decision. Input tokens: 1015; records: 0; reference: `{"vendor": "V01-07", "landed_cost": 832, "eligible_vendors": 8, "delivery_days": 1}`; comparison: `{"allow_extra_fields": false, "case_sensitive": true}`.
- **Medium / medium-02**: Medium case 02: keyboard decision. Input tokens: 1019; records: 0; reference: `{"vendor": "V02-13", "landed_cost": 914, "eligible_vendors": 8, "delivery_days": 1}`; comparison: `{"allow_extra_fields": false, "case_sensitive": true}`.
- **Medium / medium-03**: Medium case 03: router decision. Input tokens: 1017; records: 0; reference: `{"vendor": "V03-19", "landed_cost": 1031, "eligible_vendors": 8, "delivery_days": 1}`; comparison: `{"allow_extra_fields": false, "case_sensitive": true}`.
- **Medium / medium-04**: Medium case 04: printer decision. Input tokens: 1018; records: 0; reference: `{"vendor": "V04-04", "landed_cost": 1397, "eligible_vendors": 8, "delivery_days": 1}`; comparison: `{"allow_extra_fields": false, "case_sensitive": true}`.
- **Medium / medium-05**: Medium case 05: tablet decision. Input tokens: 1017; records: 0; reference: `{"vendor": "V05-01", "landed_cost": 1140, "eligible_vendors": 8, "delivery_days": 1}`; comparison: `{"allow_extra_fields": false, "case_sensitive": true}`.
- **Medium / medium-06**: Medium case 06: scanner decision. Input tokens: 1016; records: 0; reference: `{"vendor": "V06-18", "landed_cost": 1549, "eligible_vendors": 7, "delivery_days": 3}`; comparison: `{"allow_extra_fields": false, "case_sensitive": true}`.
- **Medium / medium-07**: Medium case 07: webcam decision. Input tokens: 1018; records: 0; reference: `{"vendor": "V07-09", "landed_cost": 1559, "eligible_vendors": 8, "delivery_days": 2}`; comparison: `{"allow_extra_fields": false, "case_sensitive": true}`.
- **Medium / medium-08**: Medium case 08: headset decision. Input tokens: 1015; records: 0; reference: `{"vendor": "V08-02", "landed_cost": 1485, "eligible_vendors": 7, "delivery_days": 2}`; comparison: `{"allow_extra_fields": false, "case_sensitive": true}`.
- **Medium / medium-09**: Medium case 09: speaker decision. Input tokens: 1020; records: 0; reference: `{"vendor": "V09-02", "landed_cost": 2085, "eligible_vendors": 4, "delivery_days": 2}`; comparison: `{"allow_extra_fields": false, "case_sensitive": true}`.
- **Medium / medium-10**: Medium case 10: projector decision. Input tokens: 1019; records: 0; reference: `{"vendor": "V10-01", "landed_cost": 1475, "eligible_vendors": 5, "delivery_days": 1}`; comparison: `{"allow_extra_fields": false, "case_sensitive": true}`.
- **Long / long-01**: Long case 01: monitor decision. Input tokens: 4093; records: 0; reference: `{"destination": "Bandung", "available_units": 226, "shortfall_units": 683, "action": "REORDER"}`; comparison: `{"allow_extra_fields": false, "case_sensitive": true}`.
- **Long / long-02**: Long case 02: keyboard decision. Input tokens: 4094; records: 0; reference: `{"destination": "Surabaya", "available_units": 227, "shortfall_units": 0, "action": "RELEASE"}`; comparison: `{"allow_extra_fields": false, "case_sensitive": true}`.
- **Long / long-03**: Long case 03: router decision. Input tokens: 4094; records: 0; reference: `{"destination": "Semarang", "available_units": 273, "shortfall_units": 654, "action": "REORDER"}`; comparison: `{"allow_extra_fields": false, "case_sensitive": true}`.
- **Long / long-04**: Long case 04: printer decision. Input tokens: 4096; records: 0; reference: `{"destination": "Bandung", "available_units": 371, "shortfall_units": 0, "action": "RELEASE"}`; comparison: `{"allow_extra_fields": false, "case_sensitive": true}`.
- **Long / long-05**: Long case 05: tablet decision. Input tokens: 4095; records: 0; reference: `{"destination": "Surabaya", "available_units": 427, "shortfall_units": 518, "action": "REORDER"}`; comparison: `{"allow_extra_fields": false, "case_sensitive": true}`.
- **Long / long-06**: Long case 06: scanner decision. Input tokens: 4094; records: 0; reference: `{"destination": "Semarang", "available_units": 489, "shortfall_units": 0, "action": "RELEASE"}`; comparison: `{"allow_extra_fields": false, "case_sensitive": true}`.
- **Long / long-07**: Long case 07: webcam decision. Input tokens: 4094; records: 0; reference: `{"destination": "Bandung", "available_units": 450, "shortfall_units": 513, "action": "REORDER"}`; comparison: `{"allow_extra_fields": false, "case_sensitive": true}`.
- **Long / long-08**: Long case 08: headset decision. Input tokens: 4095; records: 0; reference: `{"destination": "Surabaya", "available_units": 426, "shortfall_units": 0, "action": "RELEASE"}`; comparison: `{"allow_extra_fields": false, "case_sensitive": true}`.
- **Long / long-09**: Long case 09: speaker decision. Input tokens: 4068; records: 0; reference: `{"destination": "Semarang", "available_units": 450, "shortfall_units": 531, "action": "REORDER"}`; comparison: `{"allow_extra_fields": false, "case_sensitive": true}`.
- **Long / long-10**: Long case 10: projector decision. Input tokens: 4082; records: 0; reference: `{"destination": "Bandung", "available_units": 479, "shortfall_units": 0, "action": "RELEASE"}`; comparison: `{"allow_extra_fields": false, "case_sensitive": true}`.

## Average results

| Tier | Precision | Context | Status | Completed | Mean tokens in / out | Saved weights GiB | Mean seconds ± SD | Mean TTFT ms ± SD | TTFT measured / completed | Mean output tokens/s | JSON valid | Correct fields | Reasoning fields | Exact answer pass |
|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Lightweight | FP32 | Short | complete | 10/10 | 251.7 / 22.3 | 2.22 | 0.567 ± 0.012 | 200.9 ± 12.6 | 10/10 | 39.3 | 100% | 47% | 20% | 0% |
| Lightweight | FP32 | Medium | complete | 10/10 | 1017.4 / 41.1 | 2.22 | 2.346 ± 0.396 | 1567.2 ± 36.0 | 10/10 | 17.0 | 90% | 20% | 20% | 0% |
| Lightweight | FP32 | Long | complete | 10/10 | 4090.5 / 45.7 | 2.22 | 20.600 ± 0.674 | 19428.5 ± 590.1 | 10/10 | 2.2 | 70% | 12% | 17% | 0% |
| Lightweight | BF16 | Short | complete | 10/10 | 251.7 / 22.3 | 1.11 | 0.334 ± 0.008 | 107.3 ± 8.7 | 10/10 | 66.8 | 100% | 47% | 20% | 0% |
| Lightweight | BF16 | Medium | complete | 10/10 | 1017.4 / 41.1 | 1.11 | 0.894 ± 0.233 | 412.1 ± 5.3 | 10/10 | 44.6 | 90% | 20% | 20% | 0% |
| Lightweight | BF16 | Long | complete | 10/10 | 4090.5 / 45.2 | 1.11 | 3.450 ± 0.075 | 2690.5 ± 34.0 | 10/10 | 13.1 | 50% | 10% | 13% | 0% |
| Lightweight | FP8 | Short | complete | 10/10 | 251.7 / 32.2 | 0.57 | 0.344 ± 0.073 | 123.8 ± 5.2 | 10/10 | 92.3 | 60% | 33% | 20% | 0% |
| Lightweight | FP8 | Medium | complete | 10/10 | 1017.4 / 42.0 | 0.57 | 0.838 ± 0.008 | 493.9 ± 6.7 | 10/10 | 50.1 | 100% | 10% | 7% | 0% |
| Lightweight | FP8 | Long | complete | 10/10 | 4090.5 / 40.6 | 0.57 | 3.518 ± 0.079 | 2985.8 ± 37.0 | 10/10 | 11.5 | 80% | 18% | 13% | 0% |
| Lightweight | INT4 | Short | complete | 10/10 | 251.7 / 29.6 | 0.31 | 0.302 ± 0.061 | 124.3 ± 10.2 | 10/10 | 96.6 | 90% | 40% | 15% | 0% |
| Lightweight | INT4 | Medium | complete | 10/10 | 1017.4 / 41.5 | 0.31 | 0.750 ± 0.020 | 468.2 ± 10.1 | 10/10 | 55.3 | 100% | 8% | 3% | 0% |
| Lightweight | INT4 | Long | complete | 10/10 | 4090.5 / 42.2 | 0.31 | 3.374 ± 0.036 | 2882.6 ± 31.9 | 10/10 | 12.5 | 100% | 12% | 17% | 0% |
| Lightweight | FP8_A8 | Short | complete | 10/10 | 251.7 / 32.4 | 0.57 | 0.465 ± 0.107 | 235.0 ± 12.2 | 10/10 | 67.1 | 60% | 30% | 15% | 0% |
| Lightweight | FP8_A8 | Medium | complete | 10/10 | 1017.4 / 36.4 | 0.57 | 1.344 ± 0.036 | 1039.9 ± 27.8 | 10/10 | 27.1 | 100% | 8% | 3% | 0% |
| Lightweight | FP8_A8 | Long | complete | 10/10 | 4090.5 / 43.5 | 0.57 | 5.760 ± 0.142 | 5180.7 ± 95.8 | 10/10 | 7.5 | 60% | 10% | 7% | 0% |
| Medium | FP32 | Short | complete | 10/10 | 251.7 / 49.7 | 6.41 | 5.105 ± 2.801 | 1452.5 ± 1727.4 | 10/10 | 11.8 | 0% | 0% | 0% | 0% |
| Medium | FP32 | Medium | complete | 10/10 | 1017.4 / 96.0 | 6.41 | 9.092 ± 2.180 | 3118.0 ± 1244.1 | 10/10 | 11.1 | 0% | 0% | 0% | 0% |
| Medium | FP32 | Long | complete | 10/10 | 4090.5 / 61.9 | 6.41 | 26.967 ± 3.802 | 22715.9 ± 880.9 | 10/10 | 2.2 | 60% | 20% | 10% | 0% |
| Medium | BF16 | Short | complete | 10/10 | 251.7 / 52.1 | 3.20 | 1.509 ± 0.221 | 268.5 ± 21.4 | 10/10 | 34.4 | 0% | 0% | 0% | 0% |
| Medium | BF16 | Medium | complete | 10/10 | 1017.4 / 96.0 | 3.20 | 3.402 ± 0.066 | 970.4 ± 42.0 | 10/10 | 28.2 | 0% | 0% | 0% | 0% |
| Medium | BF16 | Long | complete | 10/10 | 4090.5 / 56.3 | 3.20 | 7.294 ± 0.801 | 5590.9 ± 281.0 | 10/10 | 7.5 | 70% | 25% | 13% | 0% |
| Medium | FP8 | Short | complete | 10/10 | 251.7 / 41.4 | 1.65 | 0.884 ± 0.027 | 319.3 ± 12.4 | 10/10 | 46.8 | 0% | 0% | 0% | 0% |
| Medium | FP8 | Medium | complete | 10/10 | 1017.4 / 50.5 | 1.65 | 2.004 ± 0.471 | 1254.0 ± 5.9 | 10/10 | 23.4 | 70% | 15% | 17% | 0% |
| Medium | FP8 | Long | complete | 10/10 | 4090.5 / 72.6 | 1.65 | 7.584 ± 0.614 | 6145.3 ± 308.8 | 10/10 | 9.4 | 30% | 10% | 3% | 0% |
| Medium | INT4 | Short | complete | 10/10 | 251.7 / 64.0 | 0.90 | 0.901 ± 0.066 | 298.7 ± 8.7 | 10/10 | 70.8 | 0% | 0% | 0% | 0% |
| Medium | INT4 | Medium | complete | 10/10 | 1017.4 / 96.0 | 0.90 | 2.195 ± 0.013 | 1176.4 ± 4.5 | 10/10 | 43.7 | 0% | 0% | 0% | 0% |
| Medium | INT4 | Long | complete | 10/10 | 4090.5 / 67.3 | 0.90 | 6.725 ± 0.473 | 5684.9 ± 9.2 | 10/10 | 9.8 | 50% | 8% | 10% | 0% |
| Medium | FP8_A8 | Short | complete | 10/10 | 251.7 / 36.7 | 1.65 | 1.303 ± 0.200 | 776.8 ± 50.4 | 10/10 | 27.3 | 30% | 20% | 15% | 0% |
| Medium | FP8_A8 | Medium | complete | 10/10 | 1017.4 / 42.5 | 1.65 | 4.136 ± 0.209 | 3473.9 ± 136.6 | 10/10 | 10.2 | 90% | 20% | 20% | 0% |
| Medium | FP8_A8 | Long | complete | 10/10 | 4090.5 / 57.3 | 1.65 | 16.590 ± 0.623 | 15433.5 ± 306.2 | 10/10 | 3.4 | 40% | 12% | 3% | 0% |
| Complex | FP32 | Short | skipped | 0/10 | 251.7 / — | — | — | — | — | — | — | — | — | — |
| Complex | FP32 | Medium | skipped | 0/10 | 1017.4 / — | — | — | — | — | — | — | — | — | — |
| Complex | FP32 | Long | skipped | 0/10 | 4090.5 / — | — | — | — | — | — | — | — | — | — |
| Complex | BF16 | Short | complete | 10/10 | 251.7 / 41.9 | 7.49 | 4.161 ± 1.402 | 1131.6 ± 836.2 | 10/10 | 10.9 | 10% | 10% | 10% | 10% |
| Complex | BF16 | Medium | complete | 10/10 | 1017.4 / 44.1 | 7.49 | 7.829 ± 2.925 | 3682.6 ± 1224.1 | 10/10 | 6.1 | 100% | 25% | 20% | 0% |
| Complex | BF16 | Long | complete | 10/10 | 4090.5 / 66.9 | 7.49 | 20.076 ± 3.824 | 13611.2 ± 1346.0 | 10/10 | 3.2 | 50% | 22% | 13% | 0% |
| Complex | FP8 | Short | complete | 10/10 | 251.7 / 43.6 | 3.86 | 2.066 ± 0.920 | 803.3 ± 10.6 | 10/10 | 19.0 | 50% | 33% | 25% | 0% |
| Complex | FP8 | Medium | complete | 10/10 | 1017.4 / 44.8 | 3.86 | 4.693 ± 0.029 | 3223.1 ± 3.5 | 10/10 | 9.5 | 100% | 25% | 23% | 0% |
| Complex | FP8 | Long | complete | 10/10 | 4090.5 / 90.1 | 3.86 | 19.523 ± 0.848 | 15487.2 ± 41.7 | 10/10 | 4.6 | 10% | 8% | 7% | 0% |
| Complex | INT4 | Short | complete | 10/10 | 251.7 / 55.8 | 2.11 | 1.769 ± 0.140 | 747.0 ± 8.9 | 10/10 | 31.4 | 0% | 0% | 0% | 0% |
| Complex | INT4 | Medium | complete | 10/10 | 1017.4 / 33.5 | 2.11 | 3.753 ± 0.124 | 3022.5 ± 6.4 | 10/10 | 8.9 | 100% | 20% | 17% | 0% |
| Complex | INT4 | Long | complete | 10/10 | 4090.5 / 49.4 | 2.11 | 16.370 ± 0.850 | 14696.7 ± 16.5 | 10/10 | 3.0 | 80% | 40% | 27% | 0% |
| Complex | FP8_A8 | Short | complete | 10/10 | 251.7 / 33.5 | 3.86 | 3.067 ± 0.431 | 2067.6 ± 67.6 | 10/10 | 10.6 | 40% | 27% | 20% | 0% |
| Complex | FP8_A8 | Medium | complete | 10/10 | 1017.4 / 44.4 | 3.86 | 10.436 ± 0.219 | 8950.7 ± 190.6 | 10/10 | 4.3 | 100% | 22% | 20% | 0% |
| Complex | FP8_A8 | Long | complete | 10/10 | 4090.5 / 43.5 | 3.86 | 40.792 ± 0.914 | 38848.0 ± 564.0 | 10/10 | 1.1 | 90% | 48% | 33% | 0% |

Tokens/s means generated output tokens divided by the full request time, including input prefill, decode and API overhead. It is not decode-only speed. Compare latency together with output length; longer or incorrect responses can distort output tokens/s.

TTFT (time to first token) is engine request arrival to the first generated token reaching the engine frontend, including queueing and prefill. It excludes model setup, subsequent decoding and HTTP/network transport. The table shows arithmetic mean ± sample SD in milliseconds; JSON/CSV timings remain in seconds. TTFT measured / completed shows coverage. Missing metrics are unavailable and excluded from TTFT averages; total request latency cannot be used to reconstruct them.

Output limit: 96 tokens per request. 70 returned responses reached this limit. Truncated answers are retained and graded as returned; they are included in the reported answer pass rates.

Thinking is disabled by default for Qwen3. Models use the same task builders and context budgets; exact prompts, token counts and per-model reference answers are saved. FP32 comparisons stay within each model. A skipped FP32 baseline leaves speedup empty.

Accuracy compares JSON fields with each task's configured reference. JSON fences are accepted; JSON types must match exactly. Extra keys and string case follow each task's comparison options. Expected fields must always be present. Reasoning fields are selected in the task's expectation file and are also scored separately in the raw field results. Invalid JSON prevents field scoring. Per-field rates use successful requests; full-answer/JSON rates count all generation attempts. Each round evaluates a different editable case. Deviations include variation in workloads and returned answer lengths. These tasks cannot establish general model quality or a monotonic relationship between model size and correctness.

Metal FP8 is MXFP8 weight storage with BF16 inputs; INT4 uses affine weights with BF16 inputs. FP32 is cast from the same BF16 source checkpoint; it cannot recover training precision. Unsupported or oversized cases have no fabricated timing or accuracy.

## Fixed FP8 weights: activation comparison

FP8 uses BF16 activations. FP8_A8 rounds quantized projection inputs to MXFP8 with mx.qqmm, then computes with BF16 buffers. A quantized tied output head also receives rounding. This is a quantize/dequantize experiment, not native FP8 arithmetic or persistent FP8 activation storage. Embedding lookups, attention and the KV cache retain BF16 behavior.

Both cases reuse one FP8 checkpoint, the same prompt token IDs, BF16 KV dtype, cache block size/count, generation settings and rotating trial schedule. Verified pairs check checkpoint/cache/settings identity, prompt hashes, token counts and reference answers. Sequential engine runs can still differ due to system load and compilation; means include first-request work.

| Model/tier | Context | Case | Completed | Verified pairs | Mean latency s | Mean TTFT ms | TTFT coverage | Mean field accuracy | Answer pass | Mean MLX peak MiB | Peak coverage | Mean engine RSS after MiB | RSS coverage |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Lightweight | Short | FP8 / BF16 activations | 10/10 | 10 | 0.344 | 123.760 | 10/10 | 33.333% | 0.000% | 1470.894 | 10/10 | 1305.552 | 10/10 |
| Lightweight | Short | FP8_A8 / FP8-rounded activations | 10/10 | 10 | 0.465 | 234.983 | 10/10 | 30.000% | 0.000% | 1484.234 | 10/10 | 1269.380 | 10/10 |
| Lightweight | Medium | FP8 / BF16 activations | 10/10 | 10 | 0.838 | 493.933 | 10/10 | 10.000% | 0.000% | 1634.620 | 10/10 | 1292.284 | 10/10 |
| Lightweight | Medium | FP8_A8 / FP8-rounded activations | 10/10 | 10 | 1.344 | 1039.895 | 10/10 | 7.500% | 0.000% | 1649.550 | 10/10 | 1255.919 | 10/10 |
| Lightweight | Long | FP8 / BF16 activations | 10/10 | 10 | 3.518 | 2985.764 | 10/10 | 17.500% | 0.000% | 1633.621 | 10/10 | 1243.036 | 10/10 |
| Lightweight | Long | FP8_A8 / FP8-rounded activations | 10/10 | 10 | 5.760 | 5180.739 | 10/10 | 10.000% | 0.000% | 1637.255 | 10/10 | 1219.358 | 10/10 |
| Medium | Short | FP8 / BF16 activations | 10/10 | 10 | 0.884 | 319.349 | 10/10 | 0.000% | 0.000% | 2553.813 | 10/10 | 2367.911 | 10/10 |
| Medium | Short | FP8_A8 / FP8-rounded activations | 10/10 | 10 | 1.303 | 776.819 | 10/10 | 20.000% | 0.000% | 2582.089 | 10/10 | 2318.342 | 10/10 |
| Medium | Medium | FP8 / BF16 activations | 10/10 | 10 | 2.004 | 1253.979 | 10/10 | 15.000% | 0.000% | 2644.834 | 10/10 | 2329.372 | 10/10 |
| Medium | Medium | FP8_A8 / FP8-rounded activations | 10/10 | 10 | 4.136 | 3473.915 | 10/10 | 20.000% | 0.000% | 2689.563 | 10/10 | 2286.625 | 10/10 |
| Medium | Long | FP8 / BF16 activations | 10/10 | 10 | 7.584 | 6145.328 | 10/10 | 10.000% | 0.000% | 2629.055 | 10/10 | 2311.561 | 10/10 |
| Medium | Long | FP8_A8 / FP8-rounded activations | 10/10 | 10 | 16.590 | 15433.483 | 10/10 | 12.500% | 0.000% | 2674.058 | 10/10 | 2270.667 | 10/10 |
| Complex | Short | FP8 / BF16 activations | 10/10 | 10 | 2.066 | 803.290 | 10/10 | 33.333% | 0.000% | 4928.497 | 10/10 | 4460.286 | 10/10 |
| Complex | Short | FP8_A8 / FP8-rounded activations | 10/10 | 10 | 3.067 | 2067.580 | 10/10 | 26.667% | 0.000% | 4955.097 | 10/10 | 4678.786 | 10/10 |
| Complex | Medium | FP8 / BF16 activations | 10/10 | 10 | 4.693 | 3223.105 | 10/10 | 25.000% | 0.000% | 5085.372 | 10/10 | 4416.173 | 10/10 |
| Complex | Medium | FP8_A8 / FP8-rounded activations | 10/10 | 10 | 10.436 | 8950.660 | 10/10 | 22.500% | 0.000% | 5127.056 | 10/10 | 4653.605 | 10/10 |
| Complex | Long | FP8 / BF16 activations | 10/10 | 10 | 19.523 | 15487.195 | 10/10 | 7.500% | 0.000% | 5072.790 | 10/10 | 4413.773 | 10/10 |
| Complex | Long | FP8_A8 / FP8-rounded activations | 10/10 | 10 | 40.792 | 38847.968 | 10/10 | 47.500% | 0.000% | 5115.290 | 10/10 | 4653.778 | 10/10 |

MLX peak is the engine's tracked active allocation peak, reset before each request; it includes weights and KV allocations, and excludes allocator cache and allocations outside MLX. Extra peak above the pre-request active allocation is also saved. Engine RSS is a post-request resident-memory snapshot, not a sampled request peak. Its saved high-water mark is cumulative. These scopes overlap and must not be added. Memory RPCs and counter reset are outside TTFT and latency timing; missing measurements stay unavailable with explicit coverage. No activation-memory saving is assumed.

Detailed metrics, sample deviations, coverage and verified-pair counts: `activation_comparison.json` / `activation_comparison.csv`.

## Outputs and evidence

- [Lightweight individual outputs, means and engine warnings](lightweight/comparison.md), [complete prompts](lightweight/prompts.md), [model card](https://huggingface.co/Qwen/Qwen3-0.6B). Resolved source: `local:models/7b50efe10ce32606/BF16`.
- [Medium individual outputs, means and engine warnings](medium/comparison.md), [complete prompts](medium/prompts.md), [model card](https://huggingface.co/Qwen/Qwen3-1.7B). Resolved source: `local:models/7ec86880db931fb2/BF16`.
- [Complex individual outputs, means and engine warnings](complex/comparison.md), [complete prompts](complex/prompts.md), [model card](https://huggingface.co/Qwen/Qwen3-4B). Resolved source: `local:models/e15b00bc84c6b5ee/BF16`.

Raw trials: `suite_trials.csv` / `suite_results.json`. Aggregated cells: `suite_summary.csv`. Per-model folders retain checkpoint audits, prompts, job specifications, engine logs and all generated answers.

The installed backend logged segmentation faults during engine teardown after saving completed results for: Complex/BF16, Complex/FP8, Complex/FP8_A8, Complex/INT4, Lightweight/BF16, Lightweight/FP32, Lightweight/FP8, Lightweight/FP8_A8, Lightweight/INT4, Medium/BF16, Medium/FP8, Medium/FP8_A8, Medium/INT4. These timings exclude teardown; clean shutdown is not verified.
