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
