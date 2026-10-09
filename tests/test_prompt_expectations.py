import contextlib
import copy
import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import activation_experiment as activation
import compare_models
import compare_vllm as bench
import prompt_tasks
from answer_comparison import score_answer
from test_comparison import WordTokenizer


class PromptExpectationTests(unittest.TestCase):
    @contextlib.contextmanager
    def editable_tasks(self):
        original = prompt_tasks.PROMPT_DIR
        with tempfile.TemporaryDirectory() as directory:
            folder = Path(directory)
            for path in original.iterdir():
                if path.suffix in (".md", ".json"):
                    shutil.copyfile(path, folder / path.name)
            with patch.object(prompt_tasks, "PROMPT_DIR", folder):
                yield folder

    def write_definition(self, folder, definition, name="short"):
        (folder / (name + ".json")).write_text(json.dumps(definition))

    def test_custom_prompt_and_expected_answer_need_no_python_changes(self):
        with self.editable_tasks() as folder:
            (folder / "short.md").write_text('There are 6 boxes with 7 items each. Return JSON {"total": integer}. Price is $5.')
            self.write_definition(folder, {"mode": "static", "expected": {"total": 42}, "reasoning_fields": ["total"]})
            prompts = bench.make_prompts(WordTokenizer(), [128, 512, 2048])
            short = prompts[0]
            self.assertEqual(short["expected"], {"total": 42})
            self.assertIn("Price is $5.", short["prompt"])
            self.assertEqual(short["record_count"], 0)
            self.assertTrue(score_answer('{"total":42}', short["expected"])["all_fields_correct"])
            self.assertFalse(score_answer('{"total":41}', short["expected"])["all_fields_correct"])
            self.assertLess(short["input_tokens"], short["target_tokens"])

    def test_static_prompts_are_not_padded_and_may_have_identical_lengths(self):
        with self.editable_tasks() as folder:
            for name in ("short", "normal", "long"):
                (folder / (name + ".md")).write_text('Return JSON {"answer": 42}.')
                self.write_definition(folder, {"mode": "static", "expected": {"answer": 42}}, name)
            prompts = bench.make_prompts(WordTokenizer(), [128, 512, 2048])
            self.assertEqual(len({p["input_tokens"] for p in prompts}), 1)
            self.assertTrue(all(p["record_count"] == 0 for p in prompts))
            with self.assertRaisesRegex(ValueError, "minimum prompt size"):
                bench.make_prompts(WordTokenizer(), [1, 2, 3])

    def test_generated_references_preserve_types_and_allow_renamed_fields(self):
        with self.editable_tasks() as folder:
            definition = prompt_tasks.load_expectation("short")
            definition["expected"] = {"stock": {"$ref": "available_units"}, "decision": {"$ref": "fulfillable"}, "label": "edited"}
            definition["reasoning_fields"] = ["stock", "decision"]
            definition["output_example"] = {"stock": 5, "decision": False, "label": "example"}
            self.write_definition(folder, definition)
            task = prompt_tasks.short_task(7)
            self.assertIs(type(task["expected"]["stock"]), int)
            self.assertIs(type(task["expected"]["decision"]), bool)
            self.assertEqual(task["expected"]["stock"], sum(r["units"] for r in task["task_data"]["receipts"]) - 9)
            self.assertEqual(task["expected"]["label"], "edited")
            self.assertIn(json.dumps(definition["output_example"]), task["prompt"])

    def test_invalid_expectations_fail_before_model_resolution(self):
        with self.editable_tasks() as folder:
            definition = {"mode": "static", "expected": {"answer": 42}}
            invalid = [[], {}, {**definition, "mode": "other"}, {**definition, "expected": {}},
                       {**definition, "expected": []}, {**definition, "expected": {"answer": float("nan")}},
                       {**definition, "reasoning_fields": ["missing"]},
                       {**definition, "reasoning_fields": ["answer", "answer"]},
                       {**definition, "comparison": {"case_sensitive": "false"}},
                       {**definition, "comparison": {"unknown": True}}, {**definition, "unexpected": 1},
                       {**definition, "expected": {"answer": {"$ref": "missing"}}},
                       {**definition, "output_example": {"answer": "wrong type"}}]
            for value in invalid:
                with self.subTest(value=value):
                    self.write_definition(folder, value)
                    with self.assertRaises(ValueError):
                        prompt_tasks.short_task()
            (folder / "short.json").write_text('not JSON')
            with self.assertRaisesRegex(ValueError, "Invalid JSON"):
                prompt_tasks.short_task()

    def test_comparison_options_change_scoring_but_keep_exact_types(self):
        expected = {"city": "Bandung", "count": 42, "approved": True, "details": {"name": "HELLO"}}
        answer = {"city": "BANDUNG", "count": 42, "approved": True, "details": {"name": "hello", "extra": 1}, "note": "extra"}
        self.assertFalse(score_answer(json.dumps(answer), expected)["all_fields_correct"])
        options = {"case_sensitive": False, "allow_extra_fields": True}
        self.assertTrue(score_answer(json.dumps(answer), expected, comparison=options)["all_fields_correct"])
        for value in (42.0, "42", True):
            self.assertFalse(score_answer(json.dumps({**answer, "count": value}), expected, comparison=options)["all_fields_correct"])

    def test_missing_null_and_nonfinite_answers_cannot_pass(self):
        self.assertFalse(score_answer('{}', {"value": None})["all_fields_correct"])
        self.assertTrue(score_answer('{"value":null}', {"value": None})["all_fields_correct"])
        for answer in ('{"value":NaN}', '{"value":Infinity}', '{"value":1e999}'):
            self.assertFalse(score_answer(answer, {"value": 1.0})["json_valid"])

    def test_empty_reasoning_fields_leave_reasoning_accuracy_unavailable(self):
        score = score_answer('{"name":"hello"}', {"name": "hello"}, reasoning_fields=[])
        self.assertTrue(score["all_fields_correct"])
        self.assertIsNone(score["reasoning_accuracy"])

    def test_answer_only_edit_changes_suite_identity_without_changing_tokens(self):
        with self.editable_tasks() as folder:
            (folder / "short.md").write_text('Return JSON {"answer": integer}.')
            definition = {"mode": "static", "expected": {"answer": 42}}
            self.write_definition(folder, definition)
            before_hash = prompt_tasks.task_suite_sha256()
            before = bench.make_prompts(WordTokenizer(), [128, 512, 2048])
            self.write_definition(folder, {**definition, "expected": {"answer": 43}})
            after = bench.make_prompts(WordTokenizer(), [128, 512, 2048])
            self.assertEqual(before[0]["prompt_sha256"], after[0]["prompt_sha256"])
            self.assertNotEqual(before_hash, prompt_tasks.task_suite_sha256())
            with self.assertRaisesRegex(ValueError, "expected"):
                bench.validate_resume_tasks(before, after)

    def test_rule_only_edit_is_rejected_on_resume(self):
        prompts = bench.make_prompts(WordTokenizer(), [128, 512, 2048])
        after = copy.deepcopy(prompts)
        after[0]["comparison"]["case_sensitive"] = False
        with self.assertRaisesRegex(ValueError, "comparison"):
            bench.validate_resume_tasks(prompts, after)
        after = copy.deepcopy(prompts)
        after[0]["reasoning_fields"] = []
        with self.assertRaisesRegex(ValueError, "reasoning_fields"):
            bench.validate_resume_tasks(prompts, after)

    def test_activation_pair_rejects_different_comparison_rules(self):
        from test_activation_experiment import contract
        rows = [{"precision": precision, "context": "Short", "trial_id": 1, "status": "ok", "generation_calls": 1,
                 "output": '{"answer":1}', "output_tokens": 1, "generation_s": 1.0,
                 "prompt_sha256": "same", "input_tokens": 10, "expected": {"answer": 1},
                 "comparison": {"case_sensitive": precision == "FP8"}, "experiment_contract": contract()}
                for precision in activation.ACTIVATION_PRECISIONS]
        summaries = bench.summarize_rows(rows, activation.ACTIVATION_PRECISIONS, 1)
        with self.assertRaisesRegex(ValueError, "comparison"):
            activation.comparison_rows(summaries, rows)

    def test_suite_rejects_answers_changed_between_models(self):
        with tempfile.TemporaryDirectory() as directory:
            folder = Path(directory)
            (folder / "lightweight").mkdir()
            bench.write_json(folder / "lightweight/results.json", {"settings": {"model": "small", "task_suite_sha256": "changed"}})
            with self.assertRaisesRegex(ValueError, "changed between model runs"):
                compare_models.collect_results(folder, {"models": ["small", "medium", "large"], "task_suite_sha256": "original"})


if __name__ == "__main__":
    unittest.main()
