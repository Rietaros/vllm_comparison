# Benchmark details

For setup and run commands, start with the [README](../README.md). This page explains quantization, activation rounding, timing, and scoring. Historical Apple Silicon measurements are in [previous_results.md](previous_results.md).

## CUDA weight formats and activation rounding

| Case | CUDA weights | CUDA projection inputs |
|---|---|---|
| `FP32` | Original checkpoint cast by vLLM to FP32 | FP32 |
| `BF16` | Original checkpoint cast by vLLM to BF16 | BF16 |
| `FP8` | Per-channel FP8 E4M3, weight-only Marlin | BF16 |
| `FP8_A8` | The same FP8 checkpoint and loaded parameter bytes | Dynamic per-token E4M3 rounding, returned to BF16 |
| `INT4` | Symmetric packed INT4, groups of 128, Marlin | BF16 |

[cuda_backend.py](../cuda_backend.py) prepares FP8 and INT4 with data-free round-to-nearest quantization. It discovers standard Linear modules using a model on the Torch meta device, then reads and converts source tensors individually on CPU and writes bounded shards using the official compressed-tensors quantization and packing routines. Token embeddings and the output head stay BF16. No calibration prompts or additional model downloads are used. CUDA checkpoints use a separate cache identity from MLX checkpoints; both activation cases reuse one cached FP8 directory. Dense FP32/BF16 cases reuse the source directory, so their saved payload size describes the original checkpoint; `runtime_audit.loaded_weight_bytes` describes the loaded parameters.

CUDA pins **TRITON_ATTN** for all formats, which supports FP32 and BF16, and disables Torch compilation and CUDA graphs for this controlled comparison. These settings favor comparability and working activation hooks over maximum serving throughput. FP8 projections must load the [weight-only Marlin kernel](https://github.com/vllm-project/vllm/blob/v0.30.0/vllm/model_executor/layers/quantization/compressed_tensors/schemes/compressed_tensors_w8a16_fp8.py); the runtime audit rejects a native W8A8 replacement. The CUDA activation experiment applies per-token FP8 quantize/dequantize rounding only to quantized Linear inputs. Embedding lookups, the unquantized output head, attention, normalization and the BF16 KV cache retain their existing precision. It measures rounding effects and overhead, without assuming activation-memory savings.

`--memory-fraction` means a fraction of **selected GPU VRAM** on CUDA and unified physical RAM on Metal. CUDA allows up to 0.95; Metal retains its 0.7 limit. The default absolute budget is still 10 GiB. CUDA plans account for dense embedding/head matrices, KV blocks and a 2 GiB runtime reserve; requests above the budget are skipped. Budgets are estimates, rather than hard process limits, and vLLM can still reject insufficient free VRAM at startup.

CUDA activation reports include engine-process Torch allocated/reserved memory, allocated/reserved peaks reset before each request, extra allocated peak above the starting allocation, device-wide used VRAM after the request, and engine RSS. Torch counters exclude allocations outside its allocator; device-wide memory includes other GPU users. These scopes overlap and must not be added. Measurements run in the audited engine process outside TTFT/latency timing. Missing counters remain unavailable with coverage counts. SHA-256 of loaded parameter bytes, including scales, must match across paired CUDA trials alongside the existing checkpoint/prompt/cache/settings contract.

Dense text models with standard Linear projections are supported; the configured Qwen3 tiers are the default. MoE and multimodal recipes require separate experiments and are rejected. CUDA and Metal use different quantization recipes, so backend results should be interpreted separately. Resume checks backend, GPU identity/visibility, policies and package versions; use a fresh output directory when changing platforms.

## Metal activation rounding and memory

The implementation is in [activation_experiment.py](../activation_experiment.py), validated with MLX 0.32.1 on an M1 Pro. `FP8_A8` is a **quantize/dequantize experiment**: projection inputs are rounded to FP8, then processed using BF16 buffers. It measures the accuracy effect and execution overhead; it does not claim native FP8 arithmetic or persistent FP8 activation storage. Rounding covers quantized linear projections and a tied embedding output projection. Token embedding lookups, attention operations, normalization, nonlinearities and the KV cache retain their existing behavior. Unsupported quantized module types fail explicitly.

Both cases resolve to the same cached `FP8` checkpoint without converting a second copy. Each runs in a separate engine process with identical prompt token IDs and reference answers, BF16 KV dtype, cache block size/count, input/output limits, seed, decoding settings and rotating context schedule. Requested cache/settings and checkpoint identity are saved per trial. Reports reject mismatched paired attempts; successful-pair counts accompany the results. Speedup is omitted when the successful trial IDs differ. Sequential engine execution still permits system-load drift; first-request compilation work is included in latency.

The experiment retains standard accuracy, TTFT and total-latency measurements, and adds **engine-process memory** outside the timed request:

- MLX active allocation before/after each request, allocator cache after it, and active allocation peak reset before each request.
- Extra MLX peak above the pre-request active allocation.
- Engine RSS after the request and its cumulative process RSS high-water mark.

MLX counters cover allocations tracked by MLX; RSS is a resident-memory snapshot rather than a sampled request peak. These measurements overlap and must not be added. The implementation does not assume FP8 rounding reduces activation memory. Missing metrics remain unavailable, with coverage counts and reasons in the raw snapshots.

Each experiment writes `activation_comparison.md`, `activation_comparison.json`, and `activation_comparison.csv` alongside the existing reports. They compare latency, TTFT, field/reasoning accuracy, full-answer pass, memory and coverage per model/context. JSON/CSV also retain sample deviations, maximum MLX peaks, successful-pair counts and latency ratios. Standard raw trial and summary files include the new memory fields. The suite produces the comparison both at its root and inside each model folder.

`--activation-comparison` is opt-in and mutually exclusive with `--precisions`; the standard four-format defaults remain available. For an explicit case list, `--precisions FP8 FP8_A8` selects the same experiment. Use a fresh output directory: resume also validates the activation and memory measurement policies.

## Metal weight formats

| Label | Weight representation | Activations | Local implementation |
|---|---|---|---|
| FP32 | 32-bit floating point | FP32 | Dense MLX checkpoint |
| BF16 | 16-bit bfloat16 | BF16 | Dense MLX checkpoint |
| FP8 | 8-bit E4M3 floating point, with one microscale per block of 32 weights | BF16 | **MXFP8, W8A16** |
| INT4 | Packed 4-bit integer values, with scales/biases per group of 64 weights | BF16 | **Affine INT4, W4A16** |

FP8 here is [MLX's MXFP8](https://ml-explore.github.io/mlx/build/html/python/_autosummary/mlx.core.quantized_matmul.html), not INT8. Packed MXFP8 and INT4 tensors appear as `uint32` containers in the saved files; their quantization metadata identifies the actual representation. Checkpoint headers and loaded engine modules are inspected to verify the requested format.

The M1 Pro runs Metal kernels for these formats. This comparison measures their local execution, including dequantization, and does **not** claim native FP8 tensor-core or pure INT4 arithmetic. Higher precision remains in scales, some unquantized parameters, and reductions. Native CUDA FP8 W8A8 is a different hardware/activation recipe. The CUDA section above describes this project's weight-only kernels and explicit activation rounding.

The default source model was published in BF16. Casting it to FP32 allows FP32 execution; it cannot recover precision absent from the original weights. The FP32 case is the baseline for this checkpoint, not an original FP32 training checkpoint.

## Prompts and comparison

Short, Medium, and Long use input budgets of **256, 1,024, and 4,096 tokens**, including the model's chat template. [prompt_tasks.py](../prompt_tasks.py) defines the data and reference calculations for three different tasks under the version `differentiated-json-examples-v3`, with prompt text loaded from [prompts/short.md](../prompts/short.md), [prompts/normal.md](../prompts/normal.md), and [prompts/long.md](../prompts/long.md). Complete, unique data records are added until the next record would exceed the budget; no repeated filler is used. All precisions receive exactly the same token IDs and reference answer for a given context. The token IDs, token counts, hashes, structured task data, JSON examples and references are saved.

| Context | Task | What the model must do | Input tokens / records in the Qwen3 rerun |
|---|---|---|---:|
| Short | Stock availability | Sum accepted receipts, subtract reservations and decide whether a new request can be fulfilled | 256 / 9 receipts |
| Medium | Supplier selection | Filter 20 offers by certification, capacity and delivery deadline; calculate costs; choose the best eligible offer and count eligible suppliers | 992 / 20 offers |
| Long | Shipment reconciliation | Read a site directory, stock policy, 77 movements, four correction notices and a superseding memo; calculate available stock, shortfall and action | 4,065 / 77 movements |

Every prompt now includes a valid example of its requested JSON schema. The examples are explicitly labeled as illustrative, and models must calculate the actual answer:

| Context | Example output format |
|---|---|
| Short | `{"item": "PENCIL", "available_units": 5, "fulfillable": false}` |
| Medium | `{"vendor": "EXAMPLE", "landed_cost": 1500, "eligible_vendors": 2, "delivery_days": 3}` |
| Long | `{"destination": "Example City", "available_units": 50, "shortfall_units": 25, "action": "REORDER"}` |

Integers must be evaluated numbers, rather than expressions such as `17 + 25`. The examples count toward the input budgets, so this version fits fewer records than the previous prompts. Budget, examples and record counts changed together; comparisons to earlier runs do not isolate the effect of any one change.

The reference answer is computed from the exact records included after tokenizer fitting. For the three Qwen3 models the token IDs and references were verified identical across all tiers. With other tokenizers, fitting may include different numbers of records, so check their saved prompts before drawing comparisons across models. Precision comparisons within a model always use the same input.

The tasks differ in both length and reasoning difficulty. Differences between Short, Medium and Long therefore describe different workloads; they do not isolate the effect of length. Ten repetitions of each fixed task measure timing variability, not general accuracy across a dataset. Historical measurements using the ORCHID/Bandung question and repeated archive sentences are summarized in [previous_results.md](previous_results.md); their generated files are not tracked in Git. Resume rejects a different prompt-suite version or different prompt hashes.

Greedy decoding (`temperature=0`, seed 42), batch size 1, a common output limit, and disabled prefix caching keep the comparison consistent. Output can stop early at EOS, so the results record output token counts and finish reasons. The default output limit of 96 tokens accommodates all three compact JSON schemas; any truncated answer is retained and graded as returned.

An otherwise valid JSON object inside a Markdown code fence is accepted. Field values and types must match exactly: a string, float or boolean cannot substitute for an integer, and integer `1` cannot substitute for boolean `true`. Full-answer pass also requires exactly the requested keys. Invalid JSON scores false on every field. Reports separate JSON validity, per-field accuracy, reasoning-field accuracy and full-answer pass rate.

Each precision loads its model once and runs ten rounds. Context order rotates between rounds (`Short → Medium → Long`, then `Medium → Long → Short`, then `Long → Short → Medium`) using the same schedule for every precision. All ten measurements enter the average, including the first request. No extra benchmark warm-up is added; vLLM's engine initialization and internal profiling happen outside the timed requests. Rotation spreads context measurements across the run; it does not eliminate drift between the sequential precision engines.

The result compares:

- **Average generation latency:** arithmetic mean of successful request times, including prompt prefill + decoding + API overhead. Sample standard deviation, median, minimum, and maximum are also saved. Download, conversion, and engine loading are excluded.
- **Average time to first token (TTFT):** engine request arrival to the first generated token reaching the engine frontend, including queueing and input prefill. Tables show mean ± sample SD in milliseconds and measured/completed coverage. Raw JSON/CSV and summary statistics use seconds (`ttft_s`, `ttft_s_mean`, etc.). Model setup, subsequent decoding and HTTP/network transport are excluded. Engine statistics are enabled to collect vLLM V1's `first_token_latency`; its wall-clock arrival and monotonic `first_token_ts` must not be subtracted. Missing metrics remain unavailable and never become zero or estimates from total latency. The timing policy is recorded, and resume requires an identical policy.
- **Average end-to-end output tokens/s:** arithmetic mean of each trial's output tokens divided by its generation latency. The summary also includes weighted throughput (`total output tokens / total elapsed generation time`). Both include prefill.
- **Actual saved weight size:** tensor payload bytes, including scales and remaining higher precision parameters. Theoretical bit ratios alone do not describe total runtime memory.
- **Average answer accuracy:** mean fraction of correct fields for the context's own schema (three fields for Short, four for Medium/Long). Reasoning-field accuracy averages the specified calculations and decisions, excluding the name field. Each individual field's correctness is also reported. Full-answer pass rate divides completely correct, schema-conforming answers by all generation attempts, counting generation errors as failures.
- **Average FP32 agreement:** exact-output-match rate, mean character similarity, and structured-answer agreement rate, pairing the same context and trial ID. Mean speedup is `FP32 mean latency / comparison mean latency`. Agreement with FP32 is distinct from accuracy.
- **Trial coverage and consistency:** requested, attempted, successful, failed, and missing counts; number of distinct outputs; and the share of successful requests matching the most common output.
- **Separate setup timing:** source download/resolution, checkpoint preparation, and engine initialization.

The engine uses at most one concurrent sequence, a 512-token scheduler prefill budget, and a KV cache estimated from the architecture, cache precision and longest request, with a minimum of 256 MiB. Both commands default to a 10 GiB planning budget; the NVIDIA examples in the README instead select 80% of GPU VRAM. The explicit KV allocation governs cache sizing; the budget is not a hard cap on total process memory. Process RSS is a cumulative driver high-water mark, not complete engine or unified GPU memory. Some first-request kernel work may remain inside the generation time even after engine initialization.

The sample standard deviation is undefined for fewer than two successful requests and is then left empty. Failed/planned/missing requests never become zero timings in an average. Always check the completed/requested count when comparing means. These three fixed tasks are not a general accuracy evaluation or a cross-validation estimate. Errors are retained; a failed run exits nonzero and preserves completed measurements.

## Validation

The automated checks cover CPU checkpoint conversion, activation rounding, mocked CUDA engine/memory routing, shared scoring and reporting, and Metal behavior. Actual CUDA inference, timing, and memory still need to be measured on an NVIDIA server.

Run the checks in the environment you installed:

```sh
# NVIDIA / Linux
.venv-cuda/bin/python -m unittest discover -s tests -v

# Apple Silicon
.venv/bin/python -m unittest discover -s tests -v
```

Metal-specific tests are skipped outside Apple Silicon. Generated results and downloaded checkpoints are excluded from Git.
