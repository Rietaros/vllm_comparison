import contextlib
import importlib.util
import io
import json
import os
import subprocess
import sys
import tempfile
import types
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import activation_experiment as activation
import benchmark_backend as backend
import compare_models as suite
import compare_vllm as bench
import cuda_backend as cuda
from test_comparison import WordTokenizer

HAS_TORCH = importlib.util.find_spec("torch") is not None
HAS_CONVERTER = HAS_TORCH and all(importlib.util.find_spec(name) for name in ("transformers", "compressed_tensors", "safetensors"))


def tiny_fp8_model():
    import torch
    class Projection(torch.nn.Module):
        def __init__(self):
            super().__init__()
            weights = torch.sin(torch.arange(4096).reshape(64, 64) / 19).to(torch.float8_e4m3fn)
            self.weight = torch.nn.Parameter(weights, requires_grad=False)
            kernel = type("MarlinFP8ScaledMMLinearKernel", (), {})()
            self.scheme = type("CompressedTensorsW8A16Fp8", (), {} )()
            self.scheme.linear_kernel = kernel
            self.scheme.weight_quant = types.SimpleNamespace(num_bits=8)
            self.quant_method = type("CompressedTensorsLinearMethod", (), {})()
        def forward(self, input_):
            return torch.nn.functional.linear(input_, self.weight.bfloat16())
    model = torch.nn.Module()
    model.projection = Projection()
    model.embedding = torch.nn.Embedding(64, 64, dtype=torch.bfloat16)
    with torch.no_grad():
        model.embedding.weight.fill_(.5)
    return model


def contract():
    return dict(checkpoint="shared/FP8", source_revision="commit", dtype="bfloat16", kv_cache_dtype="bfloat16",
        kv_cache_bytes=256 * bench.MIB, cache_block_size=16, num_gpu_blocks=256, max_model_len=5000,
        max_new_tokens=96, memory_fraction=.35, memory_policy=cuda.MEMORY_POLICY,
        timing_policy=bench.TIMING_POLICY, seed=42, temperature=0.0)


class BackendPlanningTests(unittest.TestCase):
    def test_cuda_dry_run_propagates_backend_to_suite_children_and_reports(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for script, options in (("compare_vllm.py", []), ("compare_models.py", ["--activation-comparison"])):
                destination = root / script
                result = subprocess.run([sys.executable, str(bench.ROOT / script), "--backend", "cuda",
                    "--dry-run", "--repeats", "1", "--output-dir", str(destination), *options], capture_output=True, text=True)
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertIn("NVIDIA CUDA", (destination / "comparison.md").read_text())
                if script == "compare_models.py":
                    self.assertIn("CUDA allocated peak", (destination / "activation_comparison.md").read_text())
                    for tier in suite.TIERS:
                        data = json.loads((destination / tier.lower() / "results.json").read_text())
                        self.assertEqual(data["settings"]["backend"], "cuda")
                        self.assertEqual(len(data["results"]), 6)
                        self.assertTrue(all(row["status"] == "planned" for row in data["results"]))

    def test_selection_and_memory_flags_are_shared_by_runners(self):
        with patch.object(backend.platform, "system", return_value="Linux"):
            self.assertEqual(backend.resolve_backend(), "cuda")
        with patch.object(backend.platform, "system", return_value="Darwin"):
            self.assertEqual(backend.resolve_backend(), "metal")
        for parse in (bench.parse_args, suite.parse_args):
            args = parse(["--backend", "cuda", "--activation-comparison", "--memory-fraction", ".9"])
            self.assertEqual(args.precisions, ["FP8", "FP8_A8"])
            self.assertEqual(args.backend, "cuda")
            with contextlib.redirect_stderr(io.StringIO()), self.assertRaises(SystemExit):
                parse(["--backend", "metal", "--memory-fraction", ".9"])

    def test_cuda_budget_uses_vram_and_keeps_identical_activation_cache_plans(self):
        hardware = {"backend": "cuda", "memory_bytes": 512 * 1024**3, "gpu_memory_bytes": 24 * 1024**3}
        config = dict(hidden_size=2560, head_dim=128, num_attention_heads=32,
                      num_key_value_heads=8, num_hidden_layers=36, vocab_size=151936, tie_word_embeddings=True)
        budget = backend.device_memory_budget(hardware, fraction=.8)
        self.assertAlmostEqual(budget["effective_bytes"] / 1024**3, 19.2)
        self.assertEqual(budget["source"], "VRAM fraction")
        capped = backend.device_memory_budget(hardware, budget_gib=100)
        self.assertLess(capped["effective_bytes"], hardware["gpu_memory_bytes"])
        baseline = bench.memory_plan(config, 4_022_000_000, "FP8", 4192, hardware, budget_gib=10)
        rounded = bench.memory_plan(config, 4_022_000_000, "FP8_A8", 4192, hardware, budget_gib=10)
        self.assertEqual(baseline, rounded)
        self.assertTrue(baseline["fits"])
        self.assertGreater(baseline["estimated_weight_bytes"], 4_022_000_000 * 1.1)
        self.assertEqual(baseline["runtime_reserve_bytes"], 2 * 1024**3)

    def test_cuda_settings_disable_compile_and_pin_weight_only_kernel(self):
        for precision in bench.SPECS:
            args = cuda.engine_arguments(precision)
            self.assertEqual(args["compilation_config"]["mode"], 0)
            self.assertEqual(args["attention_config"]["backend"], "TRITON_ATTN")
            self.assertEqual(args["tensor_parallel_size"], 1)
            if precision in cuda.DESCRIPTIONS:
                self.assertEqual(args["kernel_config"]["linear_backend"], "marlin")
                self.assertEqual(args["quantization"], "compressed-tensors")
        self.assertEqual(bench.activation_settings(["FP8", "FP8_A8"], "cuda")["memory_policy"], cuda.MEMORY_POLICY)

    def test_cuda_memory_requires_a_valid_before_snapshot_for_peaks(self):
        fields = activation.memory_fields({"cuda_allocated_bytes": 100}, {
            "cuda_allocated_bytes": 105, "cuda_peak_allocated_bytes": 130, "cuda_peak_reserved_bytes": 180,
            "cuda_reserved_bytes": 150, "cuda_device_used_bytes": 200, "rss_bytes": 300})
        self.assertEqual(fields["cuda_peak_extra_bytes"], 30)
        self.assertEqual(fields["cuda_peak_allocated_bytes"], 130)
        self.assertIsNone(fields["mlx_peak_bytes"])
        missing = activation.memory_fields({}, {"cuda_peak_allocated_bytes": 130})
        self.assertIsNone(missing["cuda_peak_allocated_bytes"])

    def test_cuda_failed_and_skipped_trials_keep_cuda_metadata(self):
        prompts = bench.make_trials(bench.make_prompts(WordTokenizer(), [128, 512, 2048]), 1)
        rows = bench.blank_rows("FP8", prompts, "skipped", "VRAM budget", "cuda")
        rows += bench.blank_rows("FP8_A8", prompts, "error", "Worker stopped", "cuda")
        summaries = bench.summarize_rows(rows, list(activation.ACTIVATION_PRECISIONS), 1)
        self.assertTrue(all(row["backend"] == "cuda" and "MXFP8" not in row["description"] for row in rows))
        with tempfile.TemporaryDirectory() as directory:
            activation.write_comparison(Path(directory), summaries, rows, "cuda")
            self.assertIn("CUDA allocated peak", (Path(directory) / "activation_comparison.md").read_text())

    def test_cuda_report_refuses_changed_runtime_weight_hash(self):
        rows = [{"precision": precision, "backend": "cuda", "context": "Short", "trial_id": 1,
                 "status": "ok", "generation_calls": 1, "generation_s": 1, "output_tokens": 1,
                 "output": "{}", "input_tokens": 100, "prompt_sha256": "hash", "expected": {"x": 1},
                 "experiment_contract": {**contract(), "backend": "cuda", "weight_policy": cuda.WEIGHT_POLICY,
                                         "weight_sha256": "weights"}} for precision in activation.ACTIVATION_PRECISIONS]
        summaries = bench.summarize_rows(rows, list(activation.ACTIVATION_PRECISIONS), 1)
        self.assertEqual(activation.comparison_rows(summaries, rows)[0]["verified_trial_pairs"], 1)
        rows[1]["experiment_contract"]["weight_sha256"] = "changed"
        with self.assertRaisesRegex(ValueError, "mismatch"):
            activation.comparison_rows(summaries, rows)


@unittest.skipUnless(HAS_TORCH, "Requires Torch (CPU is sufficient)")
class TorchActivationTests(unittest.TestCase):
    def test_rounding_keeps_exact_parameters_and_embedding_lookups(self):
        import torch
        model = tiny_fp8_model()
        x = torch.cos(torch.arange(256).reshape(4, 64) / 13).bfloat16()
        tokens = torch.tensor([0, 1, 7])
        embedding = model.embedding(tokens).clone()
        baseline = model.projection(x)
        expected = model.projection(cuda.fp8_round_trip(x))
        weight = model.projection.weight
        before = cuda.audit_loaded_model(model)
        cuda.validate_audit(before, "FP8")
        cuda.round_fp8_activations(model)
        self.assertTrue(torch.equal(model.projection(input_=x), expected))
        self.assertFalse(torch.equal(expected, baseline))
        self.assertTrue(torch.equal(model.embedding(tokens), embedding))
        self.assertIs(model.projection.weight, weight)
        after = cuda.audit_loaded_model(model)
        self.assertEqual(before["weight_sha256"], after["weight_sha256"])
        cuda.validate_audit(after, "FP8_A8")
        zeros = torch.zeros(2, 64, dtype=torch.bfloat16)
        self.assertTrue(torch.equal(cuda.fp8_round_trip(zeros), zeros))
        with self.assertRaises(ValueError):
            cuda.fp8_round_trip(x.float())

    def test_unsupported_kernel_rejected_before_any_hook_installation(self):
        model = tiny_fp8_model()
        model.other = tiny_fp8_model().projection
        model.other.scheme.linear_kernel = type("NativeW8A8Kernel", (), {})()
        with self.assertRaisesRegex(ValueError, "weight-only"):
            cuda.round_fp8_activations(model)
        self.assertFalse(model.projection._forward_pre_hooks)

    def test_worker_uses_cuda_callbacks_and_preserves_full_pair_contract(self):
        import torch
        observed = []
        class FakeLLM:
            def __init__(self, **kwargs):
                observed.append(kwargs)
                self.model = tiny_fp8_model()
                self.llm_engine = types.SimpleNamespace(engine_core=types.SimpleNamespace(shutdown=lambda: None))
            def apply_model(self, callback):
                return [callback(self.model)]
            def generate(self, prompts, **kwargs):
                self.model.projection(torch.ones(4, 64, dtype=torch.bfloat16))
                expected = next(p["expected"] for p in job["prompts"] if p["prompt_token_ids"] == prompts[0]["prompt_token_ids"])
                completion = types.SimpleNamespace(text=json.dumps(expected), token_ids=[1, 2], finish_reason="stop")
                return [types.SimpleNamespace(outputs=[completion], metrics=types.SimpleNamespace(first_token_latency=.000001))]
        modules = {"vllm": types.SimpleNamespace(LLM=FakeLLM, SamplingParams=lambda **kw: kw),
                   "vllm.platforms": types.SimpleNamespace(current_platform=types.SimpleNamespace(is_cuda=lambda: True))}
        counters = dict(synchronize=lambda: None, reset_peak_memory_stats=lambda: None,
            memory_allocated=lambda: 100, memory_reserved=lambda: 150, max_memory_allocated=lambda: 125,
            max_memory_reserved=lambda: 180, mem_get_info=lambda: (1000, 2000))
        with tempfile.TemporaryDirectory() as directory, patch.dict(sys.modules, modules), \
                patch.multiple(torch.cuda, **counters), contextlib.redirect_stdout(io.StringIO()):
            rows = []
            for precision in activation.ACTIVATION_PRECISIONS:
                job = dict(backend="cuda", precision=precision, checkpoint="shared/FP8", source="source", max_model_len=5000,
                    max_new_tokens=96, memory_fraction=.35, kv_cache_dtype="bfloat16", memory_policy=cuda.MEMORY_POLICY,
                    experiment_contract=contract(), preparation={}, result_path=str(Path(directory) / (precision + ".json")),
                    prompts=bench.make_trials(bench.make_prompts(WordTokenizer(), [128, 512, 2048]), 1))
                result = bench.run_worker(job)
                self.assertTrue(all(row["status"] == "ok" and row["all_fields_correct"] for row in result))
                for row in result:
                    self.assertEqual(row["memory_before"]["pid"], row["runtime_audit"]["engine_pid"])
                    self.assertEqual(row["cuda_peak_allocated_bytes"], 125)
                    self.assertIsNone(row["mlx_peak_bytes"])
                    self.assertIsNotNone(row["ttft_s"])
                rows.extend(result)
            self.assertEqual(observed[0], observed[1])
            summaries = bench.summarize_rows(rows, list(activation.ACTIVATION_PRECISIONS), 1)
            comparisons = activation.comparison_rows(summaries, rows)
            self.assertEqual([item["verified_trial_pairs"] for item in comparisons], [1, 1, 1])
            activation.write_comparison(Path(directory), summaries, rows, "cuda")
            self.assertIn("CUDA allocated peak", (Path(directory) / "activation_comparison.md").read_text())
            self.assertEqual(json.loads((Path(directory) / "activation_comparison.json").read_text())["activation_policy"], cuda.ACTIVATION_POLICY)


@unittest.skipUnless(HAS_CONVERTER, "Requires Torch, transformers and compressed-tensors")
class CudaCheckpointTests(unittest.TestCase):
    def test_streamed_qwen_checkpoints_reuse_fp8_and_preserve_dense_embeddings(self):
        import torch
        from transformers import Qwen3Config, Qwen3ForCausalLM
        from safetensors.torch import load_file
        from compressed_tensors.quantization import QuantizationScheme
        from compressed_tensors.compressors.naive_quantized import FloatQuantizationCompressor
        from compressed_tensors.compressors.pack_quantized import PackedQuantizationCompressor
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "source"
            model = Qwen3ForCausalLM(Qwen3Config(vocab_size=256, hidden_size=256, intermediate_size=512,
                num_hidden_layers=1, num_attention_heads=2, num_key_value_heads=1, head_dim=128, tie_word_embeddings=True)).bfloat16()
            model.save_pretrained(source)
            original = model.state_dict()
            paths = {}
            for precision in ("FP8", "FP8_A8", "INT4"):
                destination, stats, cached = cuda.prepare_checkpoint(source, "commit", "tiny", precision,
                    root / "models", bench.safetensors_info, bench.write_json)
                paths[precision] = destination
                self.assertEqual(cached, precision == "FP8_A8")
                tensors = {}
                for path in destination.glob("*.safetensors"):
                    tensors.update(load_file(path))
                self.assertTrue(torch.equal(tensors["model.embed_tokens.weight"], original["model.embed_tokens.weight"]))
                prefix = "model.layers.0.self_attn.q_proj."
                state = {key.removeprefix(prefix): value for key, value in tensors.items() if key.startswith(prefix)}
                case = "FP8" if precision == "FP8_A8" else precision
                compressor = PackedQuantizationCompressor if case == "INT4" else FloatQuantizationCompressor
                restored = compressor.decompress(state, QuantizationScheme(**cuda.quantization_recipe(case)))["weight"]
                self.assertEqual(restored.shape, original[prefix + "weight"].shape)
                self.assertLess((restored.float() - original[prefix + "weight"].float()).abs().max().item(), .02)
                self.assertIn("I32" if case == "INT4" else "F8_E4M3", stats["elements_by_dtype"])
                config = json.loads((destination / "config.json").read_text())["quantization_config"]
                self.assertIsNone(config["config_groups"]["weights"]["input_activations"])
            self.assertEqual(paths["FP8"], paths["FP8_A8"])
            config_path = paths["FP8"] / "config.json"
            config = json.loads(config_path.read_text())
            config["quantization_config"]["config_groups"]["weights"]["input_activations"] = {"num_bits": 8}
            bench.write_json(config_path, config)
            with self.assertRaisesRegex(ValueError, "weight-only"):
                cuda.prepare_checkpoint(source, "commit", "tiny", "FP8", root / "models", bench.safetensors_info, bench.write_json)


if __name__ == "__main__":
    unittest.main()
