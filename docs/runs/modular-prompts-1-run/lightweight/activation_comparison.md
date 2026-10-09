## Fixed FP8 weights: activation comparison

FP8 uses BF16 activations. FP8_A8 rounds quantized projection inputs to MXFP8 with mx.qqmm, then computes with BF16 buffers. A quantized tied output head also receives rounding. This is a quantize/dequantize experiment, not native FP8 arithmetic or persistent FP8 activation storage. Embedding lookups, attention and the KV cache retain BF16 behavior.

Both cases reuse one FP8 checkpoint, the same prompt token IDs, BF16 KV dtype, cache block size/count, generation settings and rotating trial schedule. Verified pairs check checkpoint/cache/settings identity, prompt hashes, token counts and reference answers. Sequential engine runs can still differ due to system load and compilation; means include first-request work.

| Model/tier | Context | Case | Completed | Verified pairs | Mean latency s | Mean TTFT ms | TTFT coverage | Mean field accuracy | Answer pass | Mean MLX peak MiB | Peak coverage | Mean engine RSS after MiB | RSS coverage |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Single model | Short | FP8 / BF16 activations | 1/1 | 1 | 0.309 | 141.371 | 1/1 | 33.333% | 0.000% | 1477.320 | 1/1 | 1757.312 | 1/1 |
| Single model | Short | FP8_A8 / FP8-rounded activations | 1/1 | 1 | 0.673 | 500.488 | 1/1 | 33.333% | 0.000% | 1485.521 | 1/1 | 1733.047 | 1/1 |
| Single model | Medium | FP8 / BF16 activations | 1/1 | 1 | 0.966 | 474.430 | 1/1 | 0.000% | 0.000% | 1627.023 | 1/1 | 1680.625 | 1/1 |
| Single model | Medium | FP8_A8 / FP8-rounded activations | 1/1 | 1 | 1.818 | 1013.068 | 1/1 | 0.000% | 0.000% | 1636.023 | 1/1 | 1485.562 | 1/1 |
| Single model | Long | FP8 / BF16 activations | 1/1 | 1 | 3.435 | 2959.794 | 1/1 | 0.000% | 0.000% | 1627.795 | 1/1 | 1330.484 | 1/1 |
| Single model | Long | FP8_A8 / FP8-rounded activations | 1/1 | 1 | 5.692 | 5116.683 | 1/1 | 0.000% | 0.000% | 1636.023 | 1/1 | 1243.891 | 1/1 |

MLX peak is the engine's tracked active allocation peak, reset before each request; it includes weights and KV allocations, and excludes allocator cache and allocations outside MLX. Extra peak above the pre-request active allocation is also saved. Engine RSS is a post-request resident-memory snapshot, not a sampled request peak. Its saved high-water mark is cumulative. These scopes overlap and must not be added. Memory RPCs and counter reset are outside TTFT and latency timing; missing measurements stay unavailable with explicit coverage. No activation-memory saving is assumed.

Detailed metrics, sample deviations, coverage and verified-pair counts: `activation_comparison.json` / `activation_comparison.csv`.
