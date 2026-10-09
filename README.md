# vLLM precision comparison

Compare **FP32, BF16, FP8, and INT4 weights**, or keep **FP8 weights fixed** and compare **BF16 versus FP8-rounded activations**. Runs support Linux NVIDIA GPUs and Apple Silicon.

Reports show accuracy, time to first token (TTFT), total request latency, and weight size. The activation experiment also measures engine memory. Every run uses Short, Medium, and Long prompts with default input budgets of **256, 1,024, and 4,096 tokens**.

## Run on an NVIDIA GPU: step by step

You need Linux, Git, Python 3.12 with `venv`, and an NVIDIA GPU with **compute capability 8.0+** for BF16, such as A100, L4, RTX 3090/4090, or H100. The pinned packages use **CUDA 12.9**; install a compatible NVIDIA driver using the [official vLLM installation guide](https://docs.vllm.ai/en/v0.30.0/getting_started/installation/gpu/).

This benchmark uses **one GPU at a time**. Internet access and free disk space are needed for the first model download and converted checkpoints; later runs reuse them.

### 1. Download the repository

```sh
git clone https://github.com/Rietaros/vllm_comparison.git
cd vllm_comparison
```

If you already cloned it, run the remaining commands from that folder.

### 2. Check the server and install dependencies

```sh
nvidia-smi
python3.12 --version
python3.12 -m venv .venv-cuda
.venv-cuda/bin/python -m pip install --upgrade pip
.venv-cuda/bin/python -m pip install -r requirements-cuda.txt
```

`nvidia-smi` should list your GPU. The requirements install the pinned vLLM, PyTorch, and quantization packages in a separate environment.

### 3. Select the GPU and check the backend

```sh
export CUDA_VISIBLE_DEVICES=0
.venv-cuda/bin/python compare_vllm.py --backend cuda --hardware
```

Change `0` to another GPU number if needed. The hardware report should show `cuda_available: true`, the GPU name, compute capability, and VRAM. Keep this GPU selection for the remaining commands.

### 4. Preview the experiment

```sh
.venv-cuda/bin/python compare_vllm.py \
  --backend cuda --tier lightweight --activation-comparison \
  --memory-fraction 0.8 --repeats 10 --timeout 1200 \
  --dry-run --output-dir results/nvidia-plan
```

This only writes a plan; it does not download models, run inference, or verify GPU execution. Use a different output folder for the real run.

### 5. Run the activation comparison

```sh
.venv-cuda/bin/python compare_vllm.py \
  --backend cuda --tier lightweight --activation-comparison \
  --memory-fraction 0.8 --repeats 10 --timeout 1200 \
  --output-dir results/nvidia-activation
```

This runs the configured lightweight model, initially **Qwen3-0.6B**, for **60 requests**: two activation cases × three contexts × ten repeats.

| Report case | Weights | Inputs to quantized linear layers |
|---|---|---|
| `FP8` | Fixed FP8 checkpoint | BF16 |
| `FP8_A8` | The same FP8 checkpoint | Rounded to FP8, then returned to BF16 |

Both cases use identical prompts, decoding settings, and BF16 KV cache settings. **FP8 rounding measures accuracy effects and execution overhead; it does not use native FP8 activation storage or guarantee lower memory use.**

`--memory-fraction 0.8` sets a planning budget of 80% of the selected GPU's VRAM. Cases estimated to exceed it are marked **skipped**. The estimate is not a hard memory limit; other GPU workloads can still cause startup failures.

### 6. Read the comparison output

Reports are saved automatically; no export command is needed.

```sh
cat results/nvidia-activation/activation_comparison.md
head -n 10 results/nvidia-activation/activation_comparison.csv
```

Open `results/nvidia-activation/comparison.md` for the full report and generated answers. Open the CSV in a spreadsheet, or use the JSON for further analysis. Files are saved on the server where you ran the benchmark.

To copy the results to your computer, run this there, replacing the SSH user, server, and repository path:

```sh
scp -r user@server:/path/to/vllm_comparison/results/nvidia-activation ./
```

## Compare all three models

After NVIDIA setup above, run **FP32, BF16, FP8, and INT4** across every configured tier:

```sh
.venv-cuda/bin/python compare_models.py \
  --backend cuda --memory-fraction 0.8 --repeats 10 \
  --output-dir results/nvidia-models

cat results/nvidia-models/comparison.md
```

This requests **360 generations**, subject to memory skips. Here FP8 and INT4 describe the **weights**; their quantized linear layers receive BF16 activations.

For the **activation experiment across all three tiers** instead, run:

```sh
.venv-cuda/bin/python compare_models.py \
  --backend cuda --activation-comparison --memory-fraction 0.8 --repeats 10 \
  --output-dir results/nvidia-activation-models

cat results/nvidia-activation-models/activation_comparison.md
```

This requests **180 generations**. Each suite also creates `lightweight/`, `medium/`, and `complex/` folders with individual model reports and logs.

## Choose models and edit prompts

Edit [config.json](config.json) to change the model saved for each tier. Use unquantized source checkpoints; the runner creates the precision variants.

| Tier | Default model |
|---|---|
| `lightweight` | `Qwen/Qwen3-0.6B` |
| `medium` | `Qwen/Qwen3-1.7B` |
| `complex` | `Qwen/Qwen3-4B` |

`compare_vllm.py --tier medium` selects one tier. `compare_models.py` runs all three, which must have distinct model IDs. NVIDIA support currently targets dense text models such as these Qwen3 models.

The code reads prompt instructions from these Markdown files:

| File | Purpose |
|---|---|
| [prompts/system.md](prompts/system.md) | Shared system instructions |
| [prompts/short.md](prompts/short.md) | Short: stock availability |
| [prompts/normal.md](prompts/normal.md) | Medium: supplier selection |
| [prompts/long.md](prompts/long.md) | Long: shipment reconciliation |

Keep the template variables, including `$receipts`, `$quotes`, and `$events`, and the expected JSON fields when editing instructions. Task data and reference answers are generated by [prompt_tasks.py](prompt_tasks.py). Use a fresh output directory after changing models or prompts.

## Understand the output

| File | Contents |
|---|---|
| `comparison.md` | Main comparison tables and generated answers |
| `activation_comparison.md`, `.csv`, `.json` | Paired accuracy, timing, and memory results; activation experiment only |
| `summary.csv`, `summary.json` | Averages and variation for a single model |
| `results.csv`, `results.json` | Individual trials and run metadata for a single model |
| `suite_summary.csv`, `suite_trials.csv`, `suite_results.json` | All-model averages, trials, and metadata |
| `prompts.md`, `prompts.json` | Exact inputs and reference answers; inside each model folder for suites |
| `*.log` | Engine logs; inside each model folder for suites |

How to compare rows for the **same model and context**:

| Metric | Meaning | Preferred direction |
|---|---|---|
| TTFT, milliseconds | Wait until the first generated token | Lower |
| Latency, seconds | Prompt processing plus the complete generated answer | Lower |
| Field accuracy | Fraction of reference fields answered correctly | Higher |
| Answer pass rate | Fraction of attempts with a completely correct answer | Higher |
| Engine memory, MiB | Allocator peaks and engine RSS in the activation experiment | Lower, comparing the same counter |

Check completed/requested counts, TTFT coverage, and memory coverage before comparing averages. Memory counters overlap; do not add them together. Download, conversion, and engine loading are excluded from request timings; the first request is included.

Markdown tables show TTFT in milliseconds; CSV/JSON TTFT values use seconds. Raw memory fields ending in `_bytes` use bytes.

These are three fixed tasks repeated to measure timing variation. They do not establish general model accuracy. CUDA and Metal use different quantization recipes, so compare precisions within the same backend. Actual NVIDIA timing and memory must be measured on your server.

## Useful options

| Option | Use |
|---|---|
| `--repeats 1` | Quick trial before a ten-repeat measurement; use a separate output folder |
| `--precisions BF16 INT4` | Select weight formats; use separately from `--activation-comparison` |
| `--context-tokens 256 1024 4096` | Set Short, Medium, and Long input budgets |
| `--memory-budget-gib 10` | Choose an absolute planning budget instead of `--memory-fraction` |
| `--dry-run` | Write a plan without downloads or inference |
| `--resume` | Continue an existing run with the same command, GPU, settings, and output folder; only unattempted trials run |

Use a new `--output-dir` for each experiment. To resume, repeat its original command and add `--resume`. Attempted trials, including failed ones, are preserved. For all options, run `python3 compare_vllm.py --help` or `python3 compare_models.py --help`.

## Run on Apple Silicon

On native Apple Silicon with **macOS 15+**, run from the cloned repository using an existing Python with `venv` support:

```sh
python3.13 setup_metal.py
.venv/bin/python compare_vllm.py --backend metal --hardware
.venv/bin/python compare_vllm.py --backend metal --activation-comparison \
  --repeats 10 --output-dir results/metal-activation
cat results/metal-activation/activation_comparison.md
```

The installer creates a Python 3.12 environment in `.venv`. Use `.venv/bin/python compare_models.py --backend metal` for the standard three-model comparison. Metal defaults to a 10 GiB planning budget, subject to device limits.

See [benchmark details](docs/benchmark_details.md) for quantization recipes, scoring, timing, memory scopes, and tests. [Previous Apple Silicon results](docs/previous_results.md) are kept separately. Downloaded weights, environments, and generated results are excluded from Git.
