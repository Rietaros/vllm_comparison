## Fixed FP8 weights: activation comparison

FP8 uses BF16 activations. FP8_A8 rounds quantized projection inputs to MXFP8 with mx.qqmm, then computes with BF16 buffers. A quantized tied output head also receives rounding. This is a quantize/dequantize experiment, not native FP8 arithmetic or persistent FP8 activation storage. Embedding lookups, attention and the KV cache retain BF16 behavior.

Both cases reuse one FP8 checkpoint, the same prompt token IDs, BF16 KV dtype, cache block size/count, generation settings and rotating trial schedule. Verified pairs check checkpoint/cache/settings identity, prompt hashes, token counts and reference answers. Sequential engine runs can still differ due to system load and compilation; means include first-request work.

| Model/tier | Context | Case | Completed | Verified pairs | Mean latency s | Mean TTFT ms | TTFT coverage | Mean field accuracy | Answer pass | Mean MLX peak MiB | Peak coverage | Mean engine RSS after MiB | RSS coverage |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Single model | Short | FP8 / BF16 activations | 1/1 | 1 | 2.509 | 853.125 | 1/1 | 0.000% | 0.000% | 4930.785 | 1/1 | 4420.906 | 1/1 |
| Single model | Short | FP8_A8 / FP8-rounded activations | 1/1 | 1 | 3.791 | 2161.213 | 1/1 | 0.000% | 0.000% | 4958.285 | 1/1 | 4218.141 | 1/1 |
| Single model | Medium | FP8 / BF16 activations | 1/1 | 1 | 4.815 | 3132.084 | 1/1 | 0.000% | 0.000% | 5082.039 | 1/1 | 4411.625 | 1/1 |
| Single model | Medium | FP8_A8 / FP8-rounded activations | 1/1 | 1 | 9.834 | 8468.461 | 1/1 | 50.000% | 0.000% | 5115.289 | 1/1 | 4203.219 | 1/1 |
| Single model | Long | FP8 / BF16 activations | 1/1 | 1 | 17.911 | 16004.053 | 1/1 | 75.000% | 0.000% | 5084.899 | 1/1 | 4402.859 | 1/1 |
| Single model | Long | FP8_A8 / FP8-rounded activations | 1/1 | 1 | 42.821 | 40937.888 | 1/1 | 50.000% | 0.000% | 5115.290 | 1/1 | 4191.547 | 1/1 |

MLX peak is the engine's tracked active allocation peak, reset before each request; it includes weights and KV allocations, and excludes allocator cache and allocations outside MLX. Extra peak above the pre-request active allocation is also saved. Engine RSS is a post-request resident-memory snapshot, not a sampled request peak. Its saved high-water mark is cumulative. These scopes overlap and must not be added. Memory RPCs and counter reset are outside TTFT and latency timing; missing measurements stay unavailable with explicit coverage. No activation-memory saving is assumed.

Detailed metrics, sample deviations, coverage and verified-pair counts: `activation_comparison.json` / `activation_comparison.csv`.
