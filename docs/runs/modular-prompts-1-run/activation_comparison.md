## Fixed FP8 weights: activation comparison

FP8 uses BF16 activations. FP8_A8 rounds quantized projection inputs to MXFP8 with mx.qqmm, then computes with BF16 buffers. A quantized tied output head also receives rounding. This is a quantize/dequantize experiment, not native FP8 arithmetic or persistent FP8 activation storage. Embedding lookups, attention and the KV cache retain BF16 behavior.

Both cases reuse one FP8 checkpoint, the same prompt token IDs, BF16 KV dtype, cache block size/count, generation settings and rotating trial schedule. Verified pairs check checkpoint/cache/settings identity, prompt hashes, token counts and reference answers. Sequential engine runs can still differ due to system load and compilation; means include first-request work.

| Model/tier | Context | Case | Completed | Verified pairs | Mean latency s | Mean TTFT ms | TTFT coverage | Mean field accuracy | Answer pass | Mean MLX peak MiB | Peak coverage | Mean engine RSS after MiB | RSS coverage |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Lightweight | Short | FP8 / BF16 activations | 1/1 | 1 | 0.309 | 141.371 | 1/1 | 33.333% | 0.000% | 1477.320 | 1/1 | 1757.312 | 1/1 |
| Lightweight | Short | FP8_A8 / FP8-rounded activations | 1/1 | 1 | 0.673 | 500.488 | 1/1 | 33.333% | 0.000% | 1485.521 | 1/1 | 1733.047 | 1/1 |
| Lightweight | Medium | FP8 / BF16 activations | 1/1 | 1 | 0.966 | 474.430 | 1/1 | 0.000% | 0.000% | 1627.023 | 1/1 | 1680.625 | 1/1 |
| Lightweight | Medium | FP8_A8 / FP8-rounded activations | 1/1 | 1 | 1.818 | 1013.068 | 1/1 | 0.000% | 0.000% | 1636.023 | 1/1 | 1485.562 | 1/1 |
| Lightweight | Long | FP8 / BF16 activations | 1/1 | 1 | 3.435 | 2959.794 | 1/1 | 0.000% | 0.000% | 1627.795 | 1/1 | 1330.484 | 1/1 |
| Lightweight | Long | FP8_A8 / FP8-rounded activations | 1/1 | 1 | 5.692 | 5116.683 | 1/1 | 0.000% | 0.000% | 1636.023 | 1/1 | 1243.891 | 1/1 |
| Medium | Short | FP8 / BF16 activations | 1/1 | 1 | 0.670 | 358.281 | 1/1 | 66.667% | 0.000% | 2552.522 | 1/1 | 2404.625 | 1/1 |
| Medium | Short | FP8_A8 / FP8-rounded activations | 1/1 | 1 | 1.197 | 880.151 | 1/1 | 66.667% | 0.000% | 2581.522 | 1/1 | 2527.281 | 1/1 |
| Medium | Medium | FP8 / BF16 activations | 1/1 | 1 | 1.863 | 1238.148 | 1/1 | 0.000% | 0.000% | 2630.056 | 1/1 | 2109.594 | 1/1 |
| Medium | Medium | FP8_A8 / FP8-rounded activations | 1/1 | 1 | 4.588 | 3902.985 | 1/1 | 0.000% | 0.000% | 2674.056 | 1/1 | 2253.328 | 1/1 |
| Medium | Long | FP8 / BF16 activations | 1/1 | 1 | 6.921 | 6162.531 | 1/1 | 0.000% | 0.000% | 2630.056 | 1/1 | 2021.188 | 1/1 |
| Medium | Long | FP8_A8 / FP8-rounded activations | 1/1 | 1 | 18.000 | 17120.437 | 1/1 | 25.000% | 0.000% | 2674.057 | 1/1 | 2250.656 | 1/1 |
| Complex | Short | FP8 / BF16 activations | 1/1 | 1 | 2.509 | 853.125 | 1/1 | 0.000% | 0.000% | 4930.785 | 1/1 | 4420.906 | 1/1 |
| Complex | Short | FP8_A8 / FP8-rounded activations | 1/1 | 1 | 3.791 | 2161.213 | 1/1 | 0.000% | 0.000% | 4958.285 | 1/1 | 4218.141 | 1/1 |
| Complex | Medium | FP8 / BF16 activations | 1/1 | 1 | 4.815 | 3132.084 | 1/1 | 0.000% | 0.000% | 5082.039 | 1/1 | 4411.625 | 1/1 |
| Complex | Medium | FP8_A8 / FP8-rounded activations | 1/1 | 1 | 9.834 | 8468.461 | 1/1 | 50.000% | 0.000% | 5115.289 | 1/1 | 4203.219 | 1/1 |
| Complex | Long | FP8 / BF16 activations | 1/1 | 1 | 17.911 | 16004.053 | 1/1 | 75.000% | 0.000% | 5084.899 | 1/1 | 4402.859 | 1/1 |
| Complex | Long | FP8_A8 / FP8-rounded activations | 1/1 | 1 | 42.821 | 40937.888 | 1/1 | 50.000% | 0.000% | 5115.290 | 1/1 | 4191.547 | 1/1 |

MLX peak is the engine's tracked active allocation peak, reset before each request; it includes weights and KV allocations, and excludes allocator cache and allocations outside MLX. Extra peak above the pre-request active allocation is also saved. Engine RSS is a post-request resident-memory snapshot, not a sampled request peak. Its saved high-water mark is cumulative. These scopes overlap and must not be added. Memory RPCs and counter reset are outside TTFT and latency timing; missing measurements stay unavailable with explicit coverage. No activation-memory saving is assumed.

Detailed metrics, sample deviations, coverage and verified-pair counts: `activation_comparison.json` / `activation_comparison.csv`.
