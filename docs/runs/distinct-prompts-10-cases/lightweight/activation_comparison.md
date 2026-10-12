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
