import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import compare_vllm as bench
import compare_models as suite
from benchmark_config import load_models

DEFAULT_MODELS = load_models()


class ModelSuiteTests(unittest.TestCase):
    def test_hardware_plan_includes_context_cache_and_format_overhead(self):
        config = {"hidden_size": 2560, "head_dim": 128, "num_attention_heads": 32,
                  "num_key_value_heads": 8, "num_hidden_layers": 36}
        hardware = {"memory_bytes": 16 * 1024**3,
                    "metal_device": {"max_recommended_working_set_size": int(10.67 * 1024**3)}}
        plans = {p: bench.memory_plan(config, 4_022_000_000, p, 4192, hardware, .4) for p in bench.SPECS}
        self.assertFalse(plans["FP32"]["fits"])
        self.assertFalse(plans["BF16"]["fits"])
        self.assertTrue(plans["FP8"]["fits"])
        self.assertTrue(plans["INT4"]["fits"])
        self.assertAlmostEqual(plans["FP8"]["backend_memory_fraction"], 6.4 / 10.67, places=6)
        self.assertGreaterEqual(plans["FP8"]["allocated_kv_cache_bytes"], plans["FP8"]["kv_cache_bytes"])
        self.assertEqual(plans["FP8"]["allocated_kv_cache_bytes"], plans["FP8"]["num_gpu_blocks"] * 16 * 2 * 36 * 8 * 128 * 2)
        self.assertGreater(plans["FP8"]["estimated_weight_bytes"], 4_022_000_000)
        cache_minimum = 2 * 36 * 8 * 128 * 2 * 4192
        self.assertGreaterEqual(plans["BF16"]["kv_cache_bytes"], cache_minimum)
        self.assertLessEqual(abs(plans["FP32"]["kv_cache_bytes"] - 2 * plans["BF16"]["kv_cache_bytes"]), 64 * bench.MIB)
        low_gpu_budget = {**hardware, "metal_device": {"max_recommended_working_set_size": 2 * 1024**3}}
        self.assertFalse(bench.memory_plan(config, 4_022_000_000, "INT4", 4192, low_gpu_budget, .4)["fits"])

    def test_streaming_matches_mlx_layers_and_preserves_bfloat16_source(self):
        import mlx.core as mx
        import mlx.nn as nn
        with tempfile.TemporaryDirectory() as directory, mx.stream(mx.cpu):
            root = Path(directory)
            source = root / "source"
            source.mkdir()
            config = {"model_type": "qwen3", "tie_word_embeddings": True}
            (source / "config.json").write_text(json.dumps(config))
            # Signed non-constant values exercise scale, bias and packing.
            weights = (mx.arange(4096, dtype=mx.float32).reshape(64, 64) / 1024 - 2).astype(mx.bfloat16)
            norm = mx.ones((64,), dtype=mx.bfloat16)
            mx.save_safetensors(str(source / "model.safetensors"), {
                "model.layers.0.self_attn.q_proj.weight": weights,
                "model.embed_tokens.weight": weights,
                "model.norm.weight": norm,
                "lm_head.weight": weights})
            self.assertEqual(bench.safetensors_info(source, ("lm_head.weight",))["stored_elements"], 2 * 4096 + 64)
            for precision, spec in bench.SPECS.items():
                destination = root / precision
                bench.stream_qwen3_checkpoint(source, destination, precision)
                bench.validate_checkpoint(destination, precision)
                actual = {}
                for path in destination.glob("*.safetensors"):
                    actual.update(mx.load(str(path)))
                self.assertNotIn("lm_head.weight", actual)
                self.assertEqual(actual["model.norm.weight"].dtype, getattr(mx, spec["dtype"]))
                linear = nn.Linear(64, 64, bias=False)
                embedding = nn.Embedding(64, 64)
                linear.weight = embedding.weight = weights.astype(getattr(mx, spec["dtype"]))
                expected_layers = (("model.layers.0.self_attn.q_proj", linear), ("model.embed_tokens", embedding))
                for prefix, module in expected_layers:
                    if spec["mode"]:
                        module = module.to_quantized(group_size=spec["group_size"], bits=spec["bits"], mode=spec["mode"])
                    for suffix, tensor in module.parameters().items():
                        self.assertTrue(mx.array_equal(actual[prefix + "." + suffix], tensor).item())
                index = json.loads((destination / "model.safetensors.index.json").read_text())
                self.assertEqual(set(index["weight_map"]), set(actual))

    def test_absolute_ten_gib_budget_unblocks_dense_formats_and_respects_device_limits(self):
        config = {"hidden_size": 2560, "head_dim": 128, "num_attention_heads": 32,
                  "num_key_value_heads": 8, "num_hidden_layers": 36}
        hardware = {"memory_bytes": 16 * 1024**3,
                    "metal_device": {"max_recommended_working_set_size": int(10.67 * 1024**3)}}
        plans = {p: bench.memory_plan(config, 4_022_000_000, p, 4192, hardware, budget_gib=10) for p in bench.SPECS}
        self.assertFalse(plans["FP32"]["fits"])
        self.assertTrue(plans["BF16"]["fits"])
        self.assertEqual(plans["BF16"]["runtime_budget_bytes"], 10 * 1024**3)
        self.assertAlmostEqual(plans["BF16"]["backend_memory_fraction"], 10 / 10.67, places=6)
        medium = bench.memory_plan(config, 1_720_574_976, "FP32", 4192, hardware, budget_gib=10)
        self.assertTrue(medium["fits"])
        larger_ram = {**hardware, "memory_bytes": 32 * 1024**3}
        self.assertEqual(bench.laptop_memory_budget(larger_ram, budget_gib=10)["effective_bytes"], 10 * 1024**3)
        small_gpu = {**hardware, "metal_device": {"max_recommended_working_set_size": 5 * 1024**3}}
        capped = bench.laptop_memory_budget(small_gpu, budget_gib=10)
        self.assertEqual(capped["requested_bytes"], 10 * 1024**3)
        self.assertEqual(capped["effective_bytes"], 5 * 1024**3)
        self.assertEqual(capped["backend_memory_fraction"], 1)

    def test_memory_budget_cli_uses_ten_gib_default_or_explicit_fraction(self):
        import argparse
        parser = argparse.ArgumentParser()
        bench.add_memory_arguments(parser)
        defaults = parser.parse_args([])
        bench.validate_memory_arguments(defaults, parser)
        self.assertEqual(defaults.memory_budget_gib, 10)
        self.assertIsNone(defaults.memory_fraction)
        fraction = parser.parse_args(["--memory-fraction", "0.4"])
        bench.validate_memory_arguments(fraction, parser)
        self.assertEqual(fraction.memory_fraction, .4)
        self.assertIsNone(fraction.memory_budget_gib)

    def test_collection_keeps_model_identity_and_trial_baselines_separate(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for tier, model, seconds in zip(suite.TIERS, DEFAULT_MODELS, [1, 4, 9]):
                bench.write_json(root / tier.lower() / "results.json", {
                    "settings": {"model": model, "source_revision": "commit"}, "hardware": {},
                    "summary": [{"precision": "BF16", "context": "Long", "generation_s_mean": seconds}],
                    "results": [{"precision": "BF16", "context": "Long", "trial_id": 1, "status": "ok", "generation_s": seconds}]})
            summaries, rows, metadata = suite.collect_results(root, {"models": DEFAULT_MODELS})
            self.assertEqual([r["generation_s_mean"] for r in summaries], [1, 4, 9])
            self.assertEqual([r["model"] for r in rows], DEFAULT_MODELS)
            self.assertEqual(len(metadata), 3)
            with self.assertRaises(ValueError):
                suite.collect_results(root, {"models": ["incorrect", *DEFAULT_MODELS[1:]]})

    def test_missing_models_remain_visible_without_fabricated_trials(self):
        with tempfile.TemporaryDirectory() as directory:
            summary, rows, models = suite.collect_results(Path(directory), {
                "models": DEFAULT_MODELS, "precisions": ["INT4"], "repeats": 10})
        self.assertEqual(len(summary), 9)
        self.assertEqual(rows, [])
        self.assertEqual(models, [])
        self.assertEqual({cell["tier"] for cell in summary}, set(suite.TIERS))
        for cell in summary:
            self.assertEqual(cell["status"], "pending")
            self.assertEqual(cell["trials_missing"], 10)
            self.assertIsNone(cell["generation_s_mean"])

    def test_skipped_cases_have_no_latency_or_accuracy(self):
        prompts = [{"context": context, "input_tokens": 100, "prompt_sha256": "hash"} for context in bench.LEVELS]
        rows = bench.blank_rows("FP32", bench.make_trials(prompts, 10), "skipped", "Hardware budget")
        summary = bench.summarize_rows(rows, ["FP32"], 10)
        self.assertEqual(len(summary), 3)
        for cell in summary:
            self.assertEqual(cell["status"], "skipped")
            self.assertEqual(cell["trials_skipped"], 10)
            self.assertEqual(cell["trials_attempted"], 0)
            self.assertIsNone(cell["generation_s_mean"])
            self.assertIsNone(cell["answer_pass_rate"])

    def test_field_rates_distinguish_naming_from_math(self):
        answer = '{"project":"Project ORCHID","city":"Bandung","total_units":42}'
        row = {"precision": "INT4", "context": "Short", "trial_id": 1, "status": "ok",
               "generation_calls": 1, "generation_s": 1, "output_tokens": 10,
               "end_to_end_tokens_per_s": 10, "output": answer, **bench.score_answer(answer)}
        summary = bench.summarize_rows([row], ["INT4"], 1)[0]
        self.assertEqual(summary["project_correct_rate"], 0)
        self.assertEqual(summary["city_correct_rate"], 1)
        self.assertEqual(summary["total_units_correct_rate"], 1)
        self.assertEqual(summary["answer_pass_rate"], 0)

    def test_summaries_use_each_context_reference_and_reasoning_fields(self):
        rows = []
        for context in bench.LEVELS:
            prompt = bench.TASK_BUILDERS[context](0)
            answer = json.dumps(prompt["expected"])
            rows.append({"precision": "INT4", "context": context, "trial_id": 1, "status": "ok",
                         "generation_calls": 1, "generation_s": 1, "output_tokens": 10,
                         "end_to_end_tokens_per_s": 10, "output": answer, **bench.task_metadata(prompt),
                         **bench.score_answer(answer, prompt["expected"], prompt["reasoning_fields"])})
        summaries = bench.summarize_rows(rows, ["INT4"], 1)
        for item in summaries:
            self.assertEqual(item["answer_pass_rate"], 1)
            self.assertEqual(item["reasoning_accuracy_mean"], 1)
            for field in item["expected"]:
                self.assertEqual(item[field + "_correct_rate"], 1)
        self.assertNotIn("vendor_correct_rate", summaries[0])
        self.assertNotIn("fulfillable_correct_rate", summaries[2])


if __name__ == "__main__":
    unittest.main()
