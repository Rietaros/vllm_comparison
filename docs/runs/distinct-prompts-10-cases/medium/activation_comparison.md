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
