import contextlib
import io
import json
import os
import sys
import tempfile
import types
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import activation_experiment as activation
import compare_models as suite
import compare_vllm as bench
from test_comparison import WordTokenizer


def contract():
    return dict(checkpoint="shared/FP8", source_revision="commit", dtype="bfloat16", kv_cache_dtype="bfloat16",
                kv_cache_bytes=256 * bench.MIB, cache_block_size=16, num_gpu_blocks=256, max_model_len=5000,
                max_new_tokens=96, memory_fraction=.35, memory_policy=activation.MEMORY_POLICY,
                timing_policy=bench.TIMING_POLICY, seed=42, temperature=0.0)


class ActivationExperimentTests(unittest.TestCase):
    def make_model(self):
        import mlx.core as mx
        import mlx.nn as nn
        class TinyModel(nn.Module):
            def __init__(self):
                super().__init__()
                self.projection = nn.Linear(64, 64, bias=True)
                self.embedding = nn.Embedding(64, 64)
        model = TinyModel()
        w = mx.sin(mx.arange(4096, dtype=mx.float32).reshape(64, 64) / 17).astype(mx.bfloat16)
        model.projection.weight = model.embedding.weight = w
        model.projection.bias = mx.ones(64, dtype=mx.bfloat16)
        nn.quantize(model, mode="mxfp8", bits=8, group_size=32)
        return model

    def test_activation_rounding_reuses_weights_matches_qdq_and_preserves_lookups(self):
        import mlx.core as mx
        model = self.make_model()
        x = mx.cos(mx.arange(256, dtype=mx.float32).reshape(4, 64) / 13).astype(mx.bfloat16)
        token_ids = mx.array([0, 1, 7])
        original = {name: layer for name, layer in model.named_modules() if name}
        embeddings = model.embedding(token_ids)
        baseline = model.projection(x)
        xq, scales = mx.quantize(x, mode="mxfp8", bits=8, group_size=32)
        rounded_x = mx.dequantize(xq, scales=scales, mode="mxfp8", bits=8, group_size=32).astype(x.dtype)
        expected = model.projection(rounded_x)
        expected_head = model.embedding.as_linear(rounded_x)
        before_audit = bench.audit_loaded_model(model)
        activation.round_fp8_activations(model)
        output = model.projection(x)
        mx.eval(output, expected, embeddings, expected_head)
        self.assertTrue(mx.array_equal(output, expected).item())
        self.assertFalse(mx.array_equal(output, baseline).item())
        self.assertTrue(mx.array_equal(model.embedding(token_ids), embeddings).item())
        self.assertTrue(mx.array_equal(model.embedding.as_linear(x), expected_head).item())
        self.assertEqual(output.dtype, mx.bfloat16)
        for name, layer in original.items():
            new = dict(model.named_modules())[name]
            self.assertIs(new.weight, layer.weight)
            self.assertIs(new.scales, layer.scales)
        after_audit = bench.audit_loaded_model(model)
        self.assertEqual(before_audit["loaded_elements_by_dtype"], after_audit["loaded_elements_by_dtype"])
        self.assertEqual(before_audit["loaded_weight_bytes"], after_audit["loaded_weight_bytes"])
        self.assertTrue(all(m["activation_quantization"] == activation.ACTIVATION_POLICY for m in after_audit["quantized_modules"]))

    def test_invalid_model_is_rejected_before_any_projection_changes(self):
        import mlx.nn as nn
        model = self.make_model()
        original = model.projection
        model.embedding = nn.Embedding(64, 64).to_quantized(mode="affine", bits=4, group_size=64)
        with self.assertRaisesRegex(ValueError, "fixed MXFP8"):
            activation.round_fp8_activations(model)
        self.assertIs(model.projection, original)

    def test_both_activation_cases_reuse_the_exact_checkpoint_and_cache_plan(self):
        import mlx.core as mx
        # Keep NumPy's native extension loaded across the sys.modules mock.
        import numpy
        modules = {"mlx_lm": types.ModuleType("mlx_lm"), "mlx_lm.convert": types.SimpleNamespace(convert=None)}
        with tempfile.TemporaryDirectory() as directory, patch.dict(sys.modules, modules), \
                patch.object(bench.importlib.metadata, "version", return_value="test-version"):
            root = Path(directory)
            source = root / "source"
            source.mkdir()
            config = {"model_type": "qwen3", "hidden_size": 64, "num_attention_heads": 1,
                      "num_hidden_layers": 1, "num_key_value_heads": 1}
            (source / "config.json").write_text(json.dumps(config))
            mx.save_safetensors(str(source / "model.safetensors"), {
                "model.layers.0.self_attn.q_proj.weight": mx.ones((64, 64), dtype=mx.bfloat16)})
            a, stats_a, _ = bench.prepare_checkpoint(source, "commit", "model", "FP8", root / "models")
            contents = {p.name: p.read_bytes() for p in a.iterdir()}
            b, stats_b, reused = bench.prepare_checkpoint(source, "commit", "model", "FP8_A8", root / "models")
            self.assertEqual(a, b)
            self.assertEqual(stats_a, stats_b)
            self.assertTrue(reused)
            self.assertEqual(contents, {p.name: p.read_bytes() for p in b.iterdir()})
            hardware = {"memory_bytes": 16 * 1024**3}
            self.assertEqual(bench.memory_plan(config, 4096, "FP8", 4192, hardware),
                             bench.memory_plan(config, 4096, "FP8_A8", 4192, hardware))

    def test_cli_experiment_is_opt_in_and_shared_by_both_runners(self):
        for parse in (bench.parse_args, suite.parse_args):
            self.assertEqual(parse([]).precisions, list(bench.DEFAULT_PRECISIONS))
            self.assertEqual(parse(["--activation-comparison"]).precisions, list(activation.ACTIVATION_PRECISIONS))
            with contextlib.redirect_stderr(io.StringIO()), self.assertRaises(SystemExit):
                parse(["--activation-comparison", "--precisions", "INT4"])

    def test_worker_routes_rounding_and_memory_to_engine_and_reports_real_mlx_counters(self):
        import mlx.core as mx
        observed = []
        testcase = self
        class FakeLLM:
            def __init__(self, **kwargs):
                observed.append(kwargs)
                self.model = testcase.make_model()
                self.llm_engine = types.SimpleNamespace(engine_core=types.SimpleNamespace(shutdown=lambda: None))
            def apply_model(self, callback):
                return [callback(self.model)]
            def generate(self, prompts, **kwargs):
                x = mx.ones((4, 64), dtype=mx.bfloat16)
                y = self.model.projection(x)
                mx.eval(y)
                expected = next(p["expected"] for p in job["prompts"] if p["prompt_token_ids"] == prompts[0]["prompt_token_ids"])
                completion = types.SimpleNamespace(text=json.dumps(expected), token_ids=[1, 2], finish_reason="stop")
                return [types.SimpleNamespace(outputs=[completion], metrics=types.SimpleNamespace(first_token_latency=.000001))]
        platform_type = type("MetalPlatform", (), {"__module__": "vllm_metal.platform"})
        modules = {"vllm": types.SimpleNamespace(LLM=FakeLLM, SamplingParams=lambda **kwargs: kwargs),
                   "vllm.platforms": types.SimpleNamespace(current_platform=platform_type())}
        with tempfile.TemporaryDirectory() as directory, patch.dict(sys.modules, modules), contextlib.redirect_stdout(io.StringIO()):
            rows = []
            for precision in activation.ACTIVATION_PRECISIONS:
                job = {"precision": precision, "checkpoint": "shared/FP8", "source": "source", "max_model_len": 5000,
                       "max_new_tokens": 96, "memory_fraction": .35, "kv_cache_dtype": "bfloat16",
                       "memory_policy": activation.MEMORY_POLICY, "experiment_contract": contract(), "preparation": {},
                       "result_path": str(Path(directory) / (precision + ".json")),
                       "prompts": bench.make_trials(bench.make_prompts(WordTokenizer(), [128, 512, 2048]), 1)}
                result = bench.run_worker(job)
                self.assertTrue(all(r["status"] == "ok" and r["all_fields_correct"] for r in result))
                for row in result:
                    self.assertEqual(row["memory_before"]["pid"], row["runtime_audit"]["engine_pid"])
                    self.assertGreater(row["mlx_peak_bytes"], 0)
                    self.assertIsNotNone(row["ttft_s"])
                rows.extend(result)
            self.assertEqual(observed[0], observed[1])
            summaries = bench.summarize_rows(rows, list(activation.ACTIVATION_PRECISIONS), 1)
            comparisons = activation.comparison_rows(summaries, rows)
            self.assertEqual([item["verified_trial_pairs"] for item in comparisons], [1, 1, 1])
            self.assertTrue(all(s["mlx_peak_bytes_measured_trials"] == 1 for s in summaries))
            self.assertTrue(activation.write_comparison(Path(directory), summaries, rows))
            self.assertIn("quantize/dequantize", (Path(directory) / "activation_comparison.md").read_text())

    def test_comparison_refuses_changed_weights_cache_prompts_or_reference_answers(self):
        rows = [{"precision": p, "context": "Short", "trial_id": 1, "status": "ok", "generation_calls": 1,
                 "generation_s": 1, "output_tokens": 1, "output": "{}", "prompt_sha256": "hash", "input_tokens": 100,
                 "expected": {"answer": 1}, "experiment_contract": contract()} for p in activation.ACTIVATION_PRECISIONS]
        summaries = bench.summarize_rows(rows, list(activation.ACTIVATION_PRECISIONS), 1)
        for field, value in (("checkpoint", "other/FP8"), ("num_gpu_blocks", 512), ("kv_cache_dtype", "float16")):
            modified = [{**row, "experiment_contract": {**row["experiment_contract"]}} for row in rows]
            modified[1]["experiment_contract"][field] = value
            with self.subTest(field=field), self.assertRaisesRegex(ValueError, "mismatch"):
                activation.comparison_rows(summaries, modified)
        for field, value in (("prompt_sha256", "other"), ("input_tokens", 99), ("expected", {"answer": 2})):
            modified = [dict(row) for row in rows]
            modified[1][field] = value
            with self.subTest(field=field), self.assertRaisesRegex(ValueError, "mismatch"):
                activation.comparison_rows(summaries, modified)

    def test_missing_memory_and_incomplete_pairs_never_become_zero_or_speedups(self):
        fields = activation.memory_fields({}, {"mlx_peak_bytes": 123})
        self.assertIsNone(fields["mlx_peak_bytes"])
        llm = types.SimpleNamespace(apply_model=lambda callback: [{"pid": os.getpid() + 1}])
        self.assertIn("unavailable_reason", activation.sample_memory(llm, {"engine_pid": os.getpid()}))
        rows = [{"precision": p, "context": "Short", "trial_id": 1, "status": "ok", "generation_calls": 1,
                 "generation_s": 1, "output_tokens": 1, "output": "{}"} for p in activation.ACTIVATION_PRECISIONS]
        rows[1].update(status="error", generation_calls=0)
        summaries = bench.summarize_rows(rows, list(activation.ACTIVATION_PRECISIONS), 1)
        item = activation.comparison_rows(summaries, rows)[0]
        self.assertEqual(item["verified_trial_pairs"], 0)
        self.assertIsNone(item["speedup_vs_bf16_activations"])
        self.assertIsNone(item["bf16_mlx_peak_bytes_mean"])


if __name__ == "__main__":
    unittest.main()
