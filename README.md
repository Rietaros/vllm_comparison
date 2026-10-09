# vLLM precision comparison on Apple Silicon

Python benchmark for **FP32, BF16, FP8, and INT4** with **Short, Medium, and Long** context. By default it runs **10 generations per precision/context**: four precisions × three contexts × ten repeats = **120 measured requests**. The comparison reports **average time to first token (TTFT), total latency and accuracy**, plus sample standard deviation, median, minimum, and maximum. Individual measurements and answers are retained.

These are repeated benchmarks of the same prompts, rather than cross-validation: there is no training step, held-out dataset, or ten independent folds. Repetition measures runtime variation and output consistency. With greedy decoding, repeated outputs can be identical; ten copies of one prompt do not provide ten independent accuracy examples.

This project targets the inspected laptop: **Apple M1 Pro, 10 CPU cores, 16 GPU cores, 16 GB unified memory, macOS 15.5**. It uses the actual [vLLM-Metal plugin](https://docs.vllm.ai/projects/vllm-metal/en/stable/). The model suite compares **Qwen3-0.6B, Qwen3-1.7B, and Qwen3-4B**, configured in [config.json](config.json). The single-model runner defaults to the configured `lightweight` model, currently `Qwen/Qwen3-0.6B`; new runs use the differentiated prompts described below. Each model's precision variants share one resolved source checkpoint, with its revision saved in the results.

## Configuration and prompt files

Edit [config.json](config.json) to save the model ID or local checkpoint directory for each tier:

```json
{
  "models": {
    "lightweight": "Qwen/Qwen3-0.6B",
    "medium": "Qwen/Qwen3-1.7B",
    "complex": "Qwen/Qwen3-4B"
  }
}
```

Both runners use this file by default. Choose another config with `--config PATH`; `--models` (suite) and `--model` (single model) override its model choices. The three tiers must contain distinct models.

```sh
.venv/bin/python compare_models.py --config config.json --dry-run
.venv/bin/python compare_vllm.py --tier medium --dry-run
.venv/bin/python compare_vllm.py --tier complex --precisions INT4
```

Prompt instructions live in Markdown:

| File | Context |
|---|---|
| [prompts/system.md](prompts/system.md) | Shared system message |
| [prompts/short.md](prompts/short.md) | Short: stock availability |
| [prompts/normal.md](prompts/normal.md) | Normal, labeled **Medium** in reports: supplier selection |
| [prompts/long.md](prompts/long.md) | Long: shipment reconciliation |

[benchmark_config.py](benchmark_config.py) loads and validates model choices. [prompt_tasks.py](prompt_tasks.py) reads the Markdown as UTF-8 and fills `$variable` placeholders using Python's `string.Template`. It generates the records and computes reference answers; the benchmark still fits complete records within each token budget. Keep `$receipts`, `$quotes`, and `$events` in their respective templates so context fitting can add records. Other placeholders insert task values and the illustrative JSON example. Use `$$` for a literal dollar sign. Literal JSON braces need no escaping.

The default config and prompts are resolved relative to the scripts, so commands also work from another directory. Use a new output directory after changing prompt instructions or models; resume checks the actual models and prompt token hashes. Keep instructions consistent with the generated task data, reference calculations and output schemas in `prompt_tasks.py`.

Downloaded weights, environments, caches, installation metadata and generated results are excluded from Git by [.gitignore](.gitignore).

## Compare lightweight, medium and complex models

```sh
.venv/bin/python compare_models.py --repeats 10 --output-dir results/my-model-comparison
```

| Tier | Default model | Role in this experiment |
|---|---|---|
| Lightweight | [Qwen3-0.6B](https://huggingface.co/Qwen/Qwen3-0.6B) | Smallest Qwen3 model; compare all four formats |
| Medium | [Qwen3-1.7B](https://huggingface.co/Qwen/Qwen3-1.7B) | More parameters; compare formats within the RAM budget |
| Complex | [Qwen3-4B](https://huggingface.co/Qwen/Qwen3-4B) | Largest local tier; BF16/FP8/INT4 fit the 10 GiB planning budget |

These are relative size tiers for this laptop. They use the same Qwen3 architecture, supported by [vLLM-Metal](https://docs.vllm.ai/projects/vllm-metal/en/stable/supported_models/), to reduce differences between model families. Parameter count does not guarantee better answers on every prompt. Thinking is disabled using the model's chat template so the 96-token limit measures final JSON answers rather than truncating reasoning. `--thinking on` enables a separate reasoning experiment; allow more output tokens for it.

The full matrix requests **3 models × 4 precisions × 3 contexts × 10 repeats = 360 generations**. Before starting each engine, the runner estimates weights, quantization overhead, a KV cache large enough for Long context, and 1 GiB for runtime/workspace. Both commands now default to a **10 GiB laptop budget**, selectable with `--memory-budget-gib 10`. The effective budget is capped to physical RAM and Apple's recommended GPU working set (about **10.67 GiB** on this M1 Pro). Oversized cases are marked **skipped**, with no timing or accuracy values. Budget estimates are planning checks, not hard process limits or measured peak RAM; memory and swap snapshots are retained. `--memory-fraction 0.4` selects the previous 6.4 GiB budget on this 16 GiB laptop; it is mutually exclusive with `--memory-budget-gib`.

For the 4B tier, FP32 weights alone need about 15 GiB and still exceed the 10 GiB budget. BF16 weights need about 7.5 GiB and an estimated **9.12 GiB** including cache and runtime reserve, so BF16 is now eligible alongside FP8 and INT4. Medium FP32 also becomes eligible at an estimated **8.35 GiB**. The planned matrix therefore contains **330 measured slots and 30 Complex/FP32 skips** on this laptop. A machine with more RAM may allow additional formats; the script evaluates its actual hardware. This implementation targets native Apple Silicon Metal, so an NVIDIA PC needs a separate CUDA backend/quantization recipe.

Qwen3 checkpoints are converted **one tensor at a time on CPU**, with output shards targeting 128 MiB (a single larger tensor occupies its own shard). This avoids keeping a full dense 4B source and its converted model in memory together. The recipe is checked against MLX's Linear/Embedding conversions for all four formats, and the loaded engine is audited again. The three source downloads total roughly 14 GB; converted checkpoints require additional disk space. Redundant tied output-head tensors are excluded from the model parameter count and converted weights.

The suite writes `comparison.md`, `suite_summary.csv`, `suite_trials.csv`, and `suite_results.json`, plus a folder for each tier containing its exact answers, averages, prompt tokens, source revision and engine logs. FP32 speedups are calculated **within the same model**; if its FP32 case was skipped, the speedup stays empty.

For vLLM-Metal 0.30, the runner translates the laptop budget into the backend's fraction of Apple's recommended GPU working set (**10 GiB corresponds to about 0.9375** of that working set). Its paged path does not honor `kv_cache_memory_bytes`, so the runner also supplies an explicit 16-token block size and block-count override. This keeps cache capacity near the estimated size instead of silently consuming the entire remaining budget. The requested budget and actual engine/cache settings are saved. Resume refuses to mix different budgets, prompt suites, cache policies or timing policies; use a fresh output directory after changing them.

```sh
.venv/bin/python compare_models.py --dry-run
.venv/bin/python compare_models.py --resume --repeats 10 --output-dir results/my-model-comparison
.venv/bin/python compare_models.py --models Qwen/Qwen3-0.6B Qwen/Qwen3-1.7B Qwen/Qwen3-4B --precisions INT4
.venv/bin/python compare_models.py --model-order Complex Lightweight Medium --output-dir results/complex-first
.venv/bin/python compare_models.py --memory-budget-gib 10 --model-order Complex Lightweight Medium --repeats 10 --output-dir results/my-10gib-comparison
.venv/bin/python compare_models.py --memory-fraction 0.4 --output-dir results/my-6gib-comparison
```

The dry run plans 360 rows without downloading or computing. Resume preserves attempted measurements and validates the model list, settings, package versions and source revisions. Select a new directory to run a fresh experiment.

## Run

The official prebuilt Metal wheels need native **arm64 Python 3.12** and **macOS 15+**. The installer uses the official paired vLLM/Metal wheels and creates Python 3.12 inside this project. Start it with an existing Python that supports `venv`, for example the laptop's Homebrew Python 3.13:

```sh
python3.13 setup_metal.py
.venv/bin/python compare_vllm.py
```

The environment is already installed in `.venv` if this is the workspace in which the benchmark was created. No API key or paid service is needed. The first run downloads roughly 1 GB of source weights and saves several GB of converted checkpoints. Later runs reuse the cached conversions. Internet access is needed on the first run, and the executing process needs access to Metal.

Check hardware or write a plan without downloading models:

```sh
.venv/bin/python compare_vllm.py --hardware
.venv/bin/python compare_vllm.py --dry-run
```

Run the full comparison with an explicit destination:

```sh
.venv/bin/python compare_vllm.py --repeats 10 --output-dir results/my-run
```

Change the number of repeats, context budgets, or selected precisions:

```sh
.venv/bin/python compare_vllm.py --context-tokens 256 1024 4096 --max-new-tokens 96
.venv/bin/python compare_vllm.py --precisions FP32 INT4
.venv/bin/python compare_vllm.py --repeats 20
.venv/bin/python compare_vllm.py --repeats 1
```

If initialization fails or a run is interrupted, fix the cause and resume with matching options:

```sh
.venv/bin/python compare_vllm.py --resume --repeats 10 --output-dir results/my-run
```

Resume tracks each **precision/context/trial ID** independently. It preserves every trial that already attempted generation, including incorrect answers or generation failures. Only unattempted trials can run. The attempt is saved before inference, so an interrupted request is not silently repeated. Resume checks the source revision, prompts, settings, and package versions and archives earlier logs.

For a custom unquantized model, use `--model MODEL_ID_OR_LOCAL_DIRECTORY` and optionally `--revision COMMIT`. Dense Qwen3 uses streaming conversion and a per-format runtime check; other architectures retain the conservative full-model conversion check. Each precision's engine runs in a separate process so its memory is released before the next precision starts.

## What the four precisions mean here

| Label | Weight representation | Activations | Local implementation |
|---|---|---|---|
| FP32 | 32-bit floating point | FP32 | Dense MLX checkpoint |
| BF16 | 16-bit bfloat16 | BF16 | Dense MLX checkpoint |
| FP8 | 8-bit E4M3 floating point, with one microscale per block of 32 weights | BF16 | **MXFP8, W8A16** |
| INT4 | Packed 4-bit integer values, with scales/biases per group of 64 weights | BF16 | **Affine INT4, W4A16** |

FP8 here is [MLX's MXFP8](https://ml-explore.github.io/mlx/build/html/python/_autosummary/mlx.core.quantized_matmul.html), not INT8. Packed MXFP8 and INT4 tensors appear as `uint32` containers in the saved files; their quantization metadata identifies the actual representation. Checkpoint headers and loaded engine modules are inspected to verify the requested format.

The M1 Pro runs Metal kernels for these formats. This comparison measures their local execution, including dequantization, and does **not** claim native FP8 tensor-core or pure INT4 arithmetic. Higher precision remains in scales, some unquantized parameters, and reductions. CUDA [FP8 W8A8](https://docs.vllm.ai/en/stable/features/quantization/index.html) is a different hardware/activation recipe and would require a separate comparison.

The default source model was published in BF16. Casting it to FP32 allows FP32 execution; it cannot recover precision absent from the original weights. The FP32 case is the baseline for this checkpoint, not an original FP32 training checkpoint.

## Prompts and comparison

Short, Medium, and Long use input budgets of **256, 1,024, and 4,096 tokens**, including the model's chat template. [prompt_tasks.py](prompt_tasks.py) defines the data and reference calculations for three different tasks under the version `differentiated-json-examples-v3`, with prompt text loaded from [prompts/short.md](prompts/short.md), [prompts/normal.md](prompts/normal.md), and [prompts/long.md](prompts/long.md). Complete, unique data records are added until the next record would exceed the budget; no repeated filler is used. All precisions receive exactly the same token IDs and reference answer for a given context. The token IDs, token counts, hashes, structured task data, JSON examples and references are saved.

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

The tasks differ in both length and reasoning difficulty. Differences between Short, Medium and Long therefore describe different workloads; they do not isolate the effect of length. Ten repetitions of each fixed task measure timing variability, not general accuracy across a dataset. Historical runs using the ORCHID/Bandung question and repeated archive sentences remain unchanged in their original folders. Resume rejects a different prompt-suite version or different prompt hashes.

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

The engine uses at most one concurrent sequence, a 512-token scheduler prefill budget, and a KV cache estimated from the architecture, cache precision and longest request, with a minimum of 256 MiB. Both commands default to a 10 GiB laptop budget. The explicit KV allocation governs cache sizing; the budget is not a hard cap on total process memory. Process RSS is a cumulative driver high-water mark, not complete engine or unified GPU memory. Some first-request kernel work may remain inside the generation time even after engine initialization.

The sample standard deviation is undefined for fewer than two successful requests and is then left empty. Failed/planned/missing requests never become zero timings in an average. Always check the completed/requested count when comparing means. These three fixed tasks are not a general accuracy evaluation or a cross-validation estimate. Errors are retained; a failed run exits nonzero and preserves completed measurements.

## Output

Each run creates:

```text
results/<timestamp>/
  comparison.md                 average comparison and answers grouped by matching output
  summary.csv / summary.json    12 precision/context summaries with averages and variation
  results.csv                   all 120 individual trial measurements
  results.json                  summaries, raw trials, hardware, versions, prompts, and audits
  prompts.json                  exact shared inputs
  prompts.md                    readable full prompts and their reference answers
  FP32.log / BF16.log / ...      engine logs
  FP32_job.json / ...            worker configurations
  FP32_worker_results.json / ... per-precision measurements
```

Default run folders have unique UTC timestamps. Prefer a new `--output-dir` for each run so previous measurements remain available.

Run the benchmark's correctness checks without model downloads or model inference (the conversion checks use MLX on CPU):

```sh
.venv/bin/python -m unittest discover -s tests -v
```

The 32 tests check configuration loading and tier selection, CLI overrides and errors, Markdown prompt loading and invalid templates, valid illustrative JSON examples on every task, absolute 10 GiB planning and CLI selection, distinct tasks without repeated lines, independent calculations from rendered records, last-notice-wins corrections, task-specific schemas and boolean/numeric types, worker scoring against each prompt's reference, context consistency, checkpoint dtype validation, per-trial FP32 comparisons, ten requests per context, rotating schedules, correct means/sample deviation, failed-trial accounting, duplicate rejection, resume behavior, hardware planning, streaming conversion equivalence, skipped metrics, and model identity in suite aggregation. TTFT checks cover V1 latency extraction without mixing clock domains, legacy same-clock timestamps, missing/invalid metrics, measured coverage, milliseconds formatting, and statistics enabled in the worker.

## Time to first token results (10 GiB)

The latest [full comparison with TTFT](results/json_examples_10gib_ttft_10_runs/comparison.md) reran all **330 feasible requests**, with **10 repeats per model/precision/context** and the same **10 GiB** budget, differentiated prompts and illustrative JSON examples. TTFT was measured for **330/330 completed requests**. The 30 Complex/FP32 slots remain hardware-budget skips.

**TTFT** is the wait from engine request arrival to the first generated token, including queueing and input prefill. It excludes model setup and subsequent decoding. Reports now show **mean TTFT ± sample SD in milliseconds** and **measured/completed coverage** next to total request latency and end-to-end tokens/s. Raw JSON/CSV timings and summary statistics use seconds.

INT4 provides a measured format across all three tiers. TTFT in **milliseconds**, mean ± sample SD over ten requests:

| Tier | Short | Medium | Long |
|---|---:|---:|---:|
| Lightweight | 120.5 ± 10.8 | 452.8 ± 13.9 | 2855.5 ± 19.2 |
| Medium | 348.8 ± 95.3 | 1281.0 ± 297.0 | 5877.6 ± 420.8 |
| Complex | 794.0 ± 39.2 | 3168.3 ± 200.0 | 15555.9 ± 802.6 |

For example, Complex INT4/Long averaged **15,555.9 ms TTFT** and **16.842 s total latency**. Most of that request elapsed before the first token, which explains why its end-to-end output tokens/s is low even with a short answer.

All **25 tests passed**, and [independent verification](results/json_examples_10gib_ttft_10_runs/verification.txt) checked every TTFT value, timing bound, aggregate, coverage count and table unit, alongside the existing task, precision and memory checks. Details are in [validation.json](results/json_examples_10gib_ttft_10_runs/validation.json); the verification script is retained in that folder.

Full-answer pass remains **0%** in all 33 measured cells on these three fixed tasks. The backend again logged teardown segmentation faults in nine cases after saving completed results; warnings remain in the reports and engine logs. TTFT and total request timing exclude teardown.

This is a fresh cohort with engine statistics enabled. Historical timings and answers are retained separately, and unavailable historical TTFT is never estimated from total latency. To repeat this measurement policy, use a fresh directory:

```sh
.venv/bin/python compare_models.py --memory-budget-gib 10 --model-order Complex Lightweight Medium --repeats 10 --output-dir results/ttft-next-run
```

## Earlier JSON examples and 10 GiB results (without TTFT)

This earlier [full comparison](results/json_examples_10gib_10_runs/comparison.md) contains **330 completed generations**, **30 Complex/FP32 budget skips**, and **36 model/precision/context summaries**. Every feasible cell ran **10 times**. All three prompt levels include valid, illustrative JSON examples. The requested and effective budget are both **10 GiB**, with an engine fraction of approximately **0.9375** of Apple's recommended working set. The [complete prompts](results/json_examples_10gib_10_runs/lightweight/prompts.md) show the examples and reference answers. Engine statistics were disabled for this historical run, so its added TTFT columns correctly show **unavailable, 0/10**. Historical total latency and answer measurements are retained.

The larger budget enabled two additional formats. Mean generation latency in seconds, with sample standard deviation:

| Newly measured case | Short | Medium | Long |
|---|---:|---:|---:|
| Medium Qwen3-1.7B, FP32 | 2.417 ± 1.830 | 7.638 ± 1.911 | 24.536 ± 2.161 |
| Complex Qwen3-4B, BF16 | 6.604 ± 2.659 | 7.444 ± 2.092 | 19.338 ± 3.706 |

INT4 remained available for all three tiers:

| Tier | Short | Medium | Long |
|---|---:|---:|---:|
| Lightweight Qwen3-0.6B | 0.259 ± 0.009 | 0.706 ± 0.008 | 3.291 ± 0.009 |
| Medium Qwen3-1.7B | 0.505 ± 0.017 | 1.933 ± 0.049 | 6.383 ± 0.064 |
| Complex Qwen3-4B | 1.738 ± 0.011 | 3.782 ± 0.009 | 15.959 ± 0.017 |

None of the 33 measured cells matched every reference field. The best field score was **75% for Complex FP8/Long**: destination, available stock and action were correct, but shortfall was wrong. Several answers still contain unevaluated expressions or incorrect values despite the examples. **20 Medium FP32/BF16 responses reached the 96-token output limit**, and are graded as returned. Each measured cell produced one identical output across its ten repeats. These results describe the current tasks, decoding settings and limit; they do not establish general model accuracy.

All **22 tests passed**. Independent verification checked trial counts, exact 10 GiB budgets, Metal fraction mapping, prompt examples and references, means/SDs, field scores, checkpoint reuse, cache overrides, CSV schemas and FP32 baselines within both Lightweight and Medium. See [validation.json](results/json_examples_10gib_10_runs/validation.json) and [verification.txt](results/json_examples_10gib_10_runs/verification.txt). The backend still logged teardown segmentation faults in nine measured cases after saving their results; the report and logs preserve these warnings. The dense cases showed greater timing variation on this working laptop, with memory/swap snapshots retained.

Budget, examples and fitted record counts changed together. Compare precisions within this run, and keep the earlier measurements separate. To repeat the current configuration, choose a fresh destination:

```sh
.venv/bin/python compare_models.py --memory-budget-gib 10 --model-order Complex Lightweight Medium --repeats 10 --output-dir results/json-examples-10gib-next
```

## Earlier differentiated prompt results (6.4 GiB, without JSON examples)

The new [full comparison](results/differentiated_prompts_10_runs/comparison.md) contains **270 completed generations**, **90 RAM-budget-skipped slots**, and **36 summaries** across Qwen3-0.6B, Qwen3-1.7B and Qwen3-4B. Every feasible precision/context ran **10 times**. All checkpoints were reused from cache, and the sources match the previous three-model run. Read the [complete prompts and reference answers](results/differentiated_prompts_10_runs/lightweight/prompts.md).

INT4 provides one measured format across all three model tiers. Mean request latency in seconds, with sample standard deviation:

| Tier | Short: stock check | Medium: supplier selection | Long: shipment reconciliation | Full answer pass at Short / Medium / Long |
|---|---:|---:|---:|---|
| Lightweight, Qwen3-0.6B | 0.310 ± 0.010 | 0.776 ± 0.010 | 3.363 ± 0.076 | 0% / 0% / 0% |
| Medium, Qwen3-1.7B | 0.547 ± 0.005 | 1.594 ± 0.005 | 6.212 ± 0.014 | 0% / 0% / 0% |
| Complex, Qwen3-4B | 1.254 ± 0.018 | 3.922 ± 0.012 | 16.006 ± 0.013 | 0% / 0% / 0% |

None of the 27 measured model/precision/context cells passed every required field. This does not mean every field was wrong: Short generally matched the item and fulfillment decision but miscalculated the available stock; Complex FP8/Long matched Surabaya and REORDER for **50% field accuracy** while missing both numbers. Complex FP8/Short returned an unevaluated arithmetic expression inside its JSON, making the whole object invalid. The full report shows every format's means, output lengths, JSON validity, reasoning scores and exact answers. All cells produced one identical answer across their ten greedy repeats, so these repetitions do not provide independent accuracy examples.

The new tasks differ in content, length and difficulty; compare the formats on the same task. The old repeated-context results below remain unchanged and should not be pooled with these measurements. All **19 tests passed**, and an independent check verified the actual trial counts, task references, field scores, means/SDs, checkpoint reuse, cache overrides, CSV schemas and identical inputs across the three models. Validation details are in [validation.json](results/differentiated_prompts_10_runs/validation.json). The installed backend continued to log teardown segmentation faults after saving results; these warnings remain in the reports and raw data.

To run these models with the current JSON examples and 10 GiB budget, use a fresh output directory:

```sh
.venv/bin/python compare_models.py --model-order Complex Lightweight Medium --repeats 10 --output-dir results/differentiated-next-run
```

## Earlier single-model results (repeated context)

The original one-run comparison is preserved in [results/laptop/comparison.md](results/laptop/comparison.md). The earlier ten-run average comparison is saved in [results/laptop_10_runs/comparison.md](results/laptop_10_runs/comparison.md), with individual trials in `results.csv` and averages in `summary.csv`. These used the original repeated-context task. Several answers can fail the requested JSON/calculation task, so timing alone should not select a precision.

All 120 requests in the ten-run benchmark completed. Mean latency in seconds (sample standard deviation after ±):

| Precision | Short | Medium | Long |
|---|---:|---:|---:|
| FP32 | 0.572 ± 0.013 | 1.093 ± 0.020 | 6.705 ± 0.046 |
| BF16 | 0.400 ± 0.014 | 0.619 ± 0.064 | 1.755 ± 0.079 |
| FP8 (MXFP8) | 0.371 ± 0.018 | 0.635 ± 0.022 | 2.076 ± 0.195 |
| INT4 | 0.388 ± 0.016 | 0.590 ± 0.015 | 1.899 ± 0.020 |

BF16 had the lowest Long-context mean, while INT4 had the lowest Medium-context mean and smallest weight payload. Only INT4/Medium passed all three answer fields, in all ten trials. Every precision/context produced the same output on its ten repeats. These are observations from this laptop and fixed task, rather than general model-quality rankings.

The installed official vLLM 0.30.0 / vLLM-Metal 0.30.0 stack has logged segmentation faults during engine teardown after saving completed generation results. These are retained in the logs and flagged in the report/CSV/JSON; a clean teardown is not verified. Each precision runs in an isolated process.

## Earlier three-model results (repeated context)

The previous comparison is preserved in [results/qwen3_model_comparison_final/comparison.md](results/qwen3_model_comparison_final/comparison.md). It contains **270 successful measured requests**, **90 hardware-skipped slots**, **36 model/precision/context summaries**, every generated answer, and averages with sample standard deviation. It used the original repeated-context task. All checkpoints were cached before this run, and all nine measured model/precision engines used the corrected RAM-to-Metal budget mapping and explicit cache block limits.

Run these models with the current JSON examples, 10 GiB budget and a fresh output directory:

```sh
.venv/bin/python compare_models.py --model-order Complex Lightweight Medium --repeats 10
```

INT4 gives one common format across all three tiers. Its mean request times in seconds are:

| Tier | Model | Short | Medium | Long | Full answer pass at Short / Medium / Long |
|---|---|---:|---:|---:|---|
| Lightweight | Qwen3-0.6B | 0.387 | 0.735 | 3.254 | 0% / 0% / 0% |
| Medium | Qwen3-1.7B | 0.529 | 1.534 | 6.283 | 0% / 0% / 0% |
| Complex | Qwen3-4B | 1.278 | 3.770 | 15.859 | 100% / 100% / 100% |

The medium INT4 model calculated `42` correctly but used `"Project ORCHID"`, so it received **66.7% field accuracy** and **0% full-answer pass**. Medium BF16 passed Long context in all ten repeats. Complex FP8 computed the total correctly but also included the project-name prefix, while Complex INT4 passed every field at every context. The report separates JSON validity, per-field scores, and complete-answer matching so these differences are visible.

The tested formats were all four for Lightweight, BF16/FP8/INT4 for Medium, and FP8/INT4 for Complex. Medium FP32 and Complex FP32/BF16 were skipped under the **6.4 GiB configured budget**. This is a budget decision rather than a claim that every skipped format is unsupported by Metal. All models received identical prompt token IDs at each context: **248, 1,018 and 4,084 input tokens**.

The earlier [diagnostic run](results/qwen3_model_comparison/comparison.md) is preserved separately. It includes an FP8 startup failure caused by the earlier budget mapping and some download-overlapped timings. Use the final report for comparisons. The final raw data were independently checked for unique trial keys, 270 real generation calls, skipped-case accounting, means/SDs, per-field scores, shared prompt hashes, and actual cache overrides. All 15 automated checks passed.

Every cell produced the same answer across its ten greedy repetitions. These results cover a small fixed task; they are not cross-validation or a general model-quality ranking. The installed backend still logged teardown segmentation faults after saving completed results; logs and report warnings retain that limitation.
