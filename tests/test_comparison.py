import json
import math
import re
import struct
import sys
import tempfile
import types
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import compare_vllm as benchmark
from prompt_tasks import long_task, medium_task, short_task


class WordTokenizer:
    def apply_chat_template(self, messages, **kwargs):
        words = " ".join(message["content"] for message in messages).split()
        return [sum(word.encode()) for word in words]


class ComparisonTests(unittest.TestCase):
    def test_contexts_have_distinct_tasks_complete_unique_records_and_references(self):
        prompts = benchmark.make_prompts(WordTokenizer(), [128, 512, 2048])
        counts = [p["input_tokens"] for p in prompts]
        self.assertLess(counts[0], counts[1])
        self.assertLess(counts[1], counts[2])
        for prompt in prompts:
            self.assertLessEqual(prompt["input_tokens"], prompt["target_tokens"])
            lines = prompt["prompt"].splitlines()
            self.assertEqual(len(lines), len(set(lines)))
            self.assertTrue(lines[-1].startswith("Return JSON only"))
            self.assertNotIn("Unrelated archive", prompt["prompt"])
            self.assertEqual(prompt["prompt_suite"], benchmark.PROMPT_SUITE)
            self.assertTrue(benchmark.score_answer(json.dumps(prompt["expected"]), prompt["expected"])["all_fields_correct"])
        self.assertEqual(len({p["task_id"] for p in prompts}), 3)
        self.assertEqual(len({json.dumps(p["expected"]) for p in prompts}), 3)
        self.assertEqual(prompts, benchmark.make_prompts(WordTokenizer(), [128, 512, 2048]))

    def test_accuracy_is_ground_truth_not_text_similarity(self):
        expected = {"city": "Bandung", "total_units": 42, "project": "ORCHID"}
        correct = benchmark.score_answer('{"city":"Bandung","total_units":42,"project":"ORCHID"}', expected)
        self.assertTrue(correct["all_fields_correct"])
        for value in ("true", '"42"', "42.0", "41"):
            score = benchmark.score_answer('{"city":"Bandung","total_units":' + value + ',"project":"ORCHID"}', expected)
            self.assertFalse(score["all_fields_correct"])
            self.assertAlmostEqual(score["field_accuracy"], 2 / 3)
        self.assertEqual(benchmark.score_answer("invalid", expected)['field_accuracy'], 0)

    def test_task_specific_scoring_enforces_boolean_types_and_exact_schema(self):
        expected = short_task()["expected"]
        self.assertFalse(expected["fulfillable"])
        for value in (0, "false", None):
            answer = {**expected, "fulfillable": value}
            self.assertFalse(benchmark.score_answer(json.dumps(answer), expected)["all_fields_correct"])
        wrong_schema = {**expected, "explanation": "extra"}
        score = benchmark.score_answer(json.dumps(wrong_schema), expected)
        self.assertEqual(score["field_accuracy"], 1)
        self.assertFalse(score["all_fields_correct"])
        self.assertFalse(benchmark.score_answer(json.dumps(expected), medium_task()["expected"])["all_fields_correct"])
        nested = {"counts": [1, 2], "decision": {"accepted": True}}
        self.assertFalse(benchmark.score_answer('{"counts":[true,2],"decision":{"accepted":true}}', nested)["all_fields_correct"])

    def test_every_task_has_valid_schema_examples_without_reference_answers(self):
        for builder in (short_task, medium_task, long_task):
            task = builder(7)
            lines = task["prompt"].splitlines()
            example_line = lines.index("Example JSON format only (illustrative values, not the answer):") + 1
            example = json.loads(lines[example_line])
            self.assertEqual(example, task["output_example"])
            self.assertEqual(example.keys(), task["expected"].keys())
            self.assertNotEqual(example, task["expected"])
            for key, value in example.items():
                self.assertIs(type(value), type(task["expected"][key]))
            self.assertIn("Return integer results, not arithmetic expressions.", task["prompt"])

    def test_reference_answers_follow_the_rendered_receipts_and_quotes(self):
        for extra in (0, 7, 19):
            short = short_task(extra)
            receipts = [int(x) for x in re.findall(r"Receipt R\d+: (\d+) units", short["prompt"])]
            reserved, requested = map(int, re.search(r"Already reserved: (\d+) units. A new customer requests (\d+)", short["prompt"]).groups())
            self.assertEqual(short["expected"]["available_units"], sum(receipts) - reserved)
            self.assertEqual(short["expected"]["fulfillable"], sum(receipts) - reserved >= requested)
            medium = medium_task(extra)
            offers = re.findall(r"([\w-]+): unit price (\d+); shipping (\d+); fixed discount (\d+); delivery (\d+) days; capacity (\d+) units; certified (yes|no)", medium["prompt"])
            eligible = [(120 * int(price) + int(shipping) - int(discount), int(days), name)
                        for name, price, shipping, discount, days, capacity, certified in offers
                        if int(capacity) >= 120 and int(days) <= 4 and certified == "yes"]
            cost, days, name = min(eligible)
            self.assertEqual(medium["expected"], {"vendor": name, "landed_cost": cost,
                                                 "delivery_days": days, "eligible_vendors": len(eligible)})

    def test_long_oracle_applies_rendered_corrections_and_latest_memo(self):
        for extra in (0, 7, 31):
            task = long_task(extra)
            text = task["prompt"]
            matches = re.findall(r"(E\d+) \| day \d+, slot \d+ \| site (\w+) \| (IN|OUT) (\d+) units \| status=(\w+) \| quality=(\w+)", text)
            rows = {eid: {"site": site, "operation": operation, "units": int(units), "status": status, "quality": quality}
                    for eid, site, operation, units, status, quality in matches}
            self.assertEqual(len(rows), task["record_count"])
            for field, value, eid in re.findall(r"Notice \d+: replace (\w+)=(\w+) on (E\d+)", text):
                rows[eid][field] = int(value) if field == "units" else value
            site, demand, reserved = re.search(r"Final memo, version 2: destination (\w+); demand (\d+) units; reservations (\d+)", text).groups()
            opening = int(re.search(rf"{site}=(\d+)", text).group(1))
            available = opening - int(reserved)
            for row in rows.values():
                if row["site"] == site and row["status"] == "posted" and row["quality"] == "usable":
                    available += row["units"] if row["operation"] == "IN" else -row["units"]
            shortfall = max(0, int(demand) - available)
            self.assertEqual(rows["E001"]["units"], 11)
            self.assertEqual(rows["E003"]["status"], "void")
            self.assertEqual(task["expected"], {"destination": "Surabaya", "available_units": available,
                                             "shortfall_units": shortfall, "action": "REORDER" if shortfall else "RELEASE"})

    def test_speedup_uses_matching_context_and_missing_baseline_is_empty(self):
        rows = [dict(precision="FP32", context="Short", status="ok", generation_s=2, output="a",
                     json_valid=False, weight_payload_bytes=100),
                dict(precision="BF16", context="Short", status="ok", generation_s=1, output="b",
                     json_valid=False, weight_payload_bytes=50),
                dict(precision="BF16", context="Long", status="ok", generation_s=3, output="b")]
        benchmark.compare_rows(rows)
        self.assertEqual(rows[1]["speedup_vs_fp32"], 2)
        self.assertEqual(rows[1]["weight_payload_ratio_vs_fp32"], 0.5)
        self.assertFalse(rows[1]["output_exact_match_fp32"])
        self.assertNotIn("speedup_vs_fp32", rows[2])

    def test_checkpoint_validation_reads_saved_dtype(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            header = json.dumps({"weight": {"dtype": "BF16", "shape": [2], "data_offsets": [0, 4]}}).encode()
            (root / "model.safetensors").write_bytes(struct.pack("<Q", len(header)) + header + b"\0" * 4)
            (root / "config.json").write_text("{}")
            self.assertEqual(benchmark.validate_checkpoint(root, "BF16")["weight_payload_bytes"], 4)
            with self.assertRaises(ValueError):
                benchmark.validate_checkpoint(root, "FP32")

    def test_resume_never_repeats_attempted_generation(self):
        prompts = [{"context": level} for level in benchmark.LEVELS]
        rows = [{"precision": "FP32", "context": "Short", "status": "ok", "generation_calls": 1},
                {"precision": "FP32", "context": "Medium", "status": "error", "generation_calls": 1},
                {"precision": "FP32", "context": "Long", "status": "error", "generation_calls": 0}]
        self.assertEqual(benchmark.pending_prompts(rows, "FP32", prompts), [{"context": "Long"}])
        self.assertEqual(benchmark.pending_prompts(rows, "BF16", prompts), prompts)

    def test_ten_round_schedule_is_shared_and_context_order_rotates(self):
        prompts = benchmark.make_prompts(WordTokenizer(), [128, 512, 2048])
        trials = benchmark.make_trials(prompts, 10)
        self.assertEqual(len(trials), 30)
        self.assertEqual(len({benchmark.trial_key(trial) for trial in trials}), 30)
        self.assertEqual([p["context"] for p in trials[:6]], ["Short", "Medium", "Long", "Medium", "Long", "Short"])
        for prompt in prompts:
            matched = [p for p in trials if p["context"] == prompt["context"]]
            self.assertEqual(len(matched), 10)
            self.assertTrue(all(p["prompt_token_ids"] == prompt["prompt_token_ids"] for p in matched))
        rows = [{"precision": "FP32", "context": "Short", "trial_id": 1, "generation_calls": 1},
                {"precision": "FP32", "context": "Short", "trial_id": 2, "generation_calls": 0}]
        pending = benchmark.pending_prompts(rows, "FP32", trials)
        self.assertEqual(len(pending), 29)
        self.assertNotIn(("Short", 1), [benchmark.trial_key(p) for p in pending])
        self.assertIn(("Short", 2), [benchmark.trial_key(p) for p in pending])

    def test_averages_count_failures_without_zero_timings(self):
        rows = []
        for trial_id, seconds, correct in ((1, 1.0, True), (2, 3.0, False)):
            rows.append(dict(precision="BF16", context="Short", trial_id=trial_id, status="ok", generation_calls=1,
                             generation_s=seconds, output_tokens=10, end_to_end_tokens_per_s=10 / seconds,
                             output=str(trial_id), field_accuracy=float(correct), all_fields_correct=correct,
                             json_valid=True))
        rows.append(dict(precision="BF16", context="Short", trial_id=3, status="error", generation_calls=1,
                         generation_s=None))
        summary = benchmark.summarize_rows(rows, ["BF16"], 4)[0]
        self.assertEqual(summary["generation_s_mean"], 2)
        self.assertAlmostEqual(summary["generation_s_stddev"], math.sqrt(2))
        self.assertEqual(summary["generation_s_median"], 2)
        self.assertEqual(summary["trials_successful"], 2)
        self.assertEqual(summary["trials_failed"], 1)
        self.assertEqual(summary["trials_missing"], 1)
        self.assertEqual(summary["field_accuracy_mean"], 0.5)
        self.assertEqual(summary["answer_pass_rate"], 1 / 3)
        self.assertEqual(summary["weighted_end_to_end_tokens_per_s"], 5)
        self.assertAlmostEqual(summary["end_to_end_tokens_per_s_mean"], (10 + 10 / 3) / 2)
        self.assertIsNone(benchmark.summarize_rows([], ["BF16"], 10)[0]["generation_s_mean"])
        self.assertIsNone(benchmark.metric_stats([1.0])["stddev"])
        with self.assertRaises(ValueError):
            benchmark.summarize_rows(rows + [rows[0]], ["BF16"], 4)

    def test_ttft_reads_v1_latency_without_subtracting_different_clocks(self):
        output = types.SimpleNamespace(metrics=types.SimpleNamespace(
            first_token_latency=0.125, arrival_time=1_800_000_000.0, first_token_ts=12345.0))
        timing = benchmark.first_token_timing(output, 0.5)
        self.assertEqual(timing["ttft_s"], 0.125)
        self.assertEqual(timing["ttft_source"], "vllm.metrics.first_token_latency")
        self.assertIsNone(timing["ttft_unavailable_reason"])
        output.metrics = types.SimpleNamespace(arrival_time=1_800_000_000.0, first_token_ts=12345.0)
        self.assertIsNone(benchmark.first_token_timing(output, 0.5)["ttft_s"])
        output.metrics = types.SimpleNamespace(arrival_time=100.0, first_token_time=100.25)
        self.assertEqual(benchmark.first_token_timing(output, 0.5)["ttft_s"], 0.25)

    def test_ttft_unavailable_and_invalid_metrics_are_not_estimated(self):
        output = types.SimpleNamespace(metrics=None)
        self.assertIsNone(benchmark.first_token_timing(output, 2)["ttft_s"])
        for latency in (0.0, -0.1, float("nan"), float("inf"), 3.0, True, "0.5"):
            output.metrics = types.SimpleNamespace(first_token_latency=latency)
            timing = benchmark.first_token_timing(output, 2)
            self.assertIsNone(timing["ttft_s"])
            self.assertIsNone(timing["ttft_source"])
            self.assertTrue(timing["ttft_unavailable_reason"])

    def test_ttft_averages_use_measured_coverage_and_display_milliseconds(self):
        rows = [dict(precision="BF16", context="Short", trial_id=i, status="ok", generation_calls=1,
                     generation_s=1.0, output_tokens=10, output="{}", ttft_s=ttft)
                for i, ttft in enumerate((0.1, None, 0.3), 1)]
        rows.append(dict(precision="BF16", context="Short", trial_id=4, status="error",
                         generation_calls=1, ttft_s=None))
        summary = benchmark.summarize_rows(rows, ["BF16"], 5)[0]
        self.assertEqual(summary["ttft_s_mean"], 0.2)
        self.assertAlmostEqual(summary["ttft_s_stddev"], math.sqrt(0.02))
        self.assertEqual(summary["ttft_measured_trials"], 2)
        self.assertEqual(summary["ttft_missing_trials"], 1)
        self.assertEqual(benchmark.ttft_cells(summary), ("200.0 ± 141.4", "2/3"))
        for row in rows:
            row["ttft_s"] = None
        missing = benchmark.summarize_rows(rows, ["BF16"], 5)[0]
        self.assertIsNone(missing["ttft_s_mean"])
        self.assertEqual(benchmark.ttft_cells(missing), ("unavailable", "0/3"))
        empty = benchmark.summarize_rows([], ["BF16"], 5)[0]
        self.assertEqual(benchmark.ttft_cells(empty), ("—", "—"))

    def test_baseline_pairing_and_speedup_of_means(self):
        rows = []
        for precision, times in (("FP32", [2.0, 8.0]), ("BF16", [1.0, 3.0])):
            for trial_id, seconds in enumerate(times, 1):
                rows.append(dict(precision=precision, context="Short", trial_id=trial_id, status="ok", generation_calls=1,
                                 generation_s=seconds, output="same", output_tokens=10, json_valid=False, weight_payload_bytes=100))
        benchmark.compare_rows(rows)
        self.assertEqual(rows[2]["speedup_vs_fp32"], 2.0)
        self.assertAlmostEqual(rows[3]["speedup_vs_fp32"], 8 / 3)
        summary = benchmark.summarize_rows(rows, ["FP32", "BF16"], 2)
        bf16 = next(item for item in summary if item["precision"] == "BF16" and item["context"] == "Short")
        self.assertEqual(bf16["speedup_vs_fp32_mean"], 2.5)

    def test_ten_generations_per_context_even_after_error(self):
        calls = []
        class FakeLLM:
            def __init__(self, **kwargs):
                if kwargs["disable_log_stats"]:
                    raise AssertionError("TTFT collection requires engine statistics")
                self.llm_engine = types.SimpleNamespace(engine_core=types.SimpleNamespace(shutdown=lambda: None))
            def apply_model(self, callback):
                return [{"loaded_elements_by_dtype": {"float32": 1}, "quantized_modules": []}]
            def generate(self, prompts, **kwargs):
                self_prompts = prompts
                calls.append(self_prompts)
                if len(calls) == 2:
                    raise RuntimeError("controlled generation failure")
                expected = next(p["expected"] for p in job["prompts"]
                                if p["prompt_token_ids"] == prompts[0]["prompt_token_ids"])
                completion = types.SimpleNamespace(text=json.dumps({**expected, "extra_note": "accepted by configuration"}),
                                                   token_ids=[1, 2], finish_reason="stop")
                return [types.SimpleNamespace(outputs=[completion], metrics=None)]
        metal = types.SimpleNamespace(synchronize=lambda: None)
        platform_type = type("MetalPlatform", (), {"__module__": "vllm_metal.platform"})
        modules = {"mlx": types.ModuleType("mlx"), "mlx.core": metal,
                   "vllm": types.SimpleNamespace(LLM=FakeLLM, SamplingParams=lambda **kwargs: kwargs),
                   "vllm.platforms": types.SimpleNamespace(current_platform=platform_type())}
        with tempfile.TemporaryDirectory() as directory, patch.dict(sys.modules, modules):
            job = {"precision": "FP32", "checkpoint": "unused", "source": "unused", "max_model_len": 5000,
                   "max_new_tokens": 96, "memory_fraction": 0.35, "preparation": {},
                   "result_path": str(Path(directory) / "worker.json"),
                   "prompts": benchmark.make_trials(benchmark.make_prompts(WordTokenizer(), [128, 512, 2048]), 10)}
            for prompt in job["prompts"]:
                prompt["comparison"]["allow_extra_fields"] = True
            rows = benchmark.run_worker(job)
            self.assertEqual(len(calls), 30)
            self.assertTrue(all(len(requests) == 1 for requests in calls))
            self.assertTrue(all(r["generation_calls"] == 1 for r in rows))
            self.assertEqual(sum(r["status"] == "ok" for r in rows), 29)
            self.assertTrue(all(r["all_fields_correct"] for r in rows if r["status"] == "ok"))
            self.assertTrue(all(r["ttft_s"] is None for r in rows))
            self.assertTrue(all(r["ttft_unavailable_reason"] for r in rows))
            self.assertEqual(len({r["task_id"] for r in rows}), 3)
            self.assertEqual(rows[1]["status"], "error")
            self.assertEqual(len({benchmark.trial_key(row) for row in rows}), 30)
            for level in benchmark.LEVELS:
                self.assertEqual(sum(r["context"] == level for r in rows), 10)
            self.assertEqual(json.loads(Path(job["result_path"]).read_text()), rows)


if __name__ == "__main__":
    unittest.main()
