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
