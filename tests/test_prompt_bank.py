import copy
import json
import re
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import compare_vllm as bench
from prompt_bank import DEFAULT_MANIFEST, load_bank, encode_cases
from test_comparison import WordTokenizer


class PromptBankTests(unittest.TestCase):
    def copy_bank(self, directory):
        destination = Path(directory) / "prompts"
        shutil.copytree(DEFAULT_MANIFEST.parent, destination)
        return destination / "cases.json"

    def test_thirty_distinct_editable_prompts_and_answers(self):
        bank = load_bank()
        self.assertEqual(len(bank["cases"]), 30)
        for context in bench.LEVELS:
            cases = [case for case in bank["cases"] if case["context"] == context]
            self.assertEqual([case["trial_id"] for case in cases], list(range(1, 11)))
            self.assertEqual(len({case["prompt"] for case in cases}), 10)
            self.assertEqual(len({json.dumps(case["expected"], sort_keys=True) for case in cases}), 10)
            self.assertEqual(len({json.dumps({key: case["expected"][key] for key in case["reasoning_fields"]}, sort_keys=True) for case in cases}), 10)
            self.assertEqual(len({case["topic"] for case in cases}), 10)
            self.assertEqual([case["case_type"] for case in cases], ["math"] * 5 + ["understanding_qna"] * 5)
            self.assertTrue(all(Path(case["prompt_file"]).exists() and Path(case["expected_file"]).exists() for case in cases))
        self.assertEqual(len({case["topic"] for case in bank["cases"]}), 30)

    def test_expected_answers_independently_match_all_rendered_records(self):
        from diverse_case_oracles import math_answer, QNA_ANSWERS
        for case in load_bank()["cases"]:
            with self.subTest(case=case["case_id"]):
                expected = (math_answer(case["case_id"], case["prompt"]) if case["case_type"] == "math"
                            else QNA_ANSWERS[case["case_id"]])
                self.assertEqual(case["expected"], expected)
                self.assertTrue(all(type(case["expected"][key]) is type(value) for key, value in expected.items()))
                if case["case_type"] == "understanding_qna":
                    passage = case["prompt"].split("Return JSON only")[0]
                    self.assertTrue(all(value in passage for value in expected.values() if isinstance(value, str)))

    def test_trial_round_selects_new_case_without_cloning(self):
        prompts = encode_cases(load_bank(), WordTokenizer(), [512, 2048, 8192])
        trials = bench.make_trials(prompts, 10)
        self.assertEqual(len(trials), 30)
        self.assertEqual(len({case["case_id"] for case in trials}), 30)
        self.assertEqual([(p["context"], p["trial_id"]) for p in trials[:6]],
                         [("Short", 1), ("Medium", 1), ("Long", 1), ("Medium", 2), ("Long", 2), ("Short", 2)])
        for index in range(1, 11):
            self.assertTrue(all(case["case_id"].endswith(f"-{index:02d}") for case in trials if case["trial_id"] == index))
        self.assertEqual(trials, bench.make_trials(prompts, 10))
        with self.assertRaisesRegex(ValueError, "Each trial requires"):
            bench.make_trials(prompts[:-1], 10)

    def test_prefix_selection_never_wraps_when_cases_are_missing(self):
        bank = load_bank(count=3)
        self.assertEqual(len(bank["cases"]), 9)
        self.assertTrue(all(case["trial_id"] <= 3 for case in bank["cases"]))
        with self.assertRaisesRegex(ValueError, "requires 11 distinct cases"):
            load_bank(count=11)

    def test_user_can_replace_prompt_and_answer_without_python_changes(self):
        with tempfile.TemporaryDirectory() as directory:
            manifest = self.copy_bank(directory)
            prompt = manifest.parent / "short/02.md"
            answer = manifest.parent / "short/02.json"
            prompt.write_text('Compute 7 * 8. Return JSON {"total":integer}. Currency is $5.')
            answer.write_text(json.dumps({"expected": {"total": 56}, "comparison": {"allow_extra_fields": True}}))
            case = encode_cases(load_bank(manifest), WordTokenizer(), [512, 2048, 8192])[1]
            self.assertIn("$5", case["prompt"])
            self.assertEqual(case["expected"], {"total": 56})
            self.assertTrue(bench.score_answer('{"total":56,"note":"ok"}', case["expected"], comparison=case["comparison"])["all_fields_correct"])

    def test_expected_only_change_invalidates_resume_with_identical_tokens(self):
        with tempfile.TemporaryDirectory() as directory:
            manifest = self.copy_bank(directory)
            before_bank = load_bank(manifest)
            before = encode_cases(before_bank, WordTokenizer(), [512, 2048, 8192])
            path = manifest.parent / "short/01.json"
            answer = json.loads(path.read_text())
            answer["expected"]["available_units"] += 1
            path.write_text(json.dumps(answer))
            after_bank = load_bank(manifest)
            after = encode_cases(after_bank, WordTokenizer(), [512, 2048, 8192])
            self.assertEqual(before[0]["prompt_sha256"], after[0]["prompt_sha256"])
            self.assertNotEqual(before_bank["sha256"], after_bank["sha256"])
            with self.assertRaisesRegex(ValueError, "expected"):
                bench.validate_resume_tasks(before, after)

    def test_duplicate_cases_and_invalid_expectations_fail_early(self):
        with tempfile.TemporaryDirectory() as directory:
            manifest = self.copy_bank(directory)
            original = json.loads(manifest.read_text())
            invalid = copy.deepcopy(original)
            invalid["contexts"]["Short"][1]["id"] = invalid["contexts"]["Short"][0]["id"]
            manifest.write_text(json.dumps(invalid))
            with self.assertRaisesRegex(ValueError, "Case IDs"):
                load_bank(manifest)
            manifest.write_text(json.dumps(original))
            (manifest.parent / "short/02.md").write_text((manifest.parent / "short/01.md").read_text())
            with self.assertRaisesRegex(ValueError, "Duplicate Short prompt"):
                load_bank(manifest)

    def test_oversized_case_names_the_case_before_inference(self):
        with self.assertRaisesRegex(ValueError, "short-01.*exceeding"):
            encode_cases(load_bank(), WordTokenizer(), [1, 2, 3])

    def test_summaries_keep_all_expected_answers_and_case_length_statistics(self):
        prompts = encode_cases(load_bank(), WordTokenizer(), [512, 2048, 8192])
        rows = [{"precision": "BF16", "status": "ok", "generation_calls": 1, "generation_s": 1,
                 "output_tokens": 2, "output": json.dumps(p["expected"]), "context": p["context"],
                 "trial_id": p["trial_id"], "input_tokens": p["input_tokens"], **bench.task_metadata(p),
                 **bench.score_answer(json.dumps(p["expected"]), p["expected"], p["reasoning_fields"], p["comparison"])} for p in prompts]
        for summary in bench.summarize_rows(rows, ["BF16"], 10):
            self.assertIsNone(summary["expected"])
            self.assertEqual(len(summary["expected_by_trial"]), 10)
            self.assertEqual(summary["unique_cases_successful"], 10)
            self.assertEqual(summary["answer_pass_rate"], 1)
            self.assertIsNone(summary["output_consistency_rate"])
            self.assertGreater(summary["input_tokens_mean"], 0)

    def test_fp32_speedup_requires_the_same_successful_case_ids(self):
        rows = [{"precision": "FP32", "context": "Short", "trial_id": 1, "status": "ok", "generation_calls": 1,
                 "generation_s": 2, "output_tokens": 1, "output": "a"},
                {"precision": "BF16", "context": "Short", "trial_id": 2, "status": "ok", "generation_calls": 1,
                 "generation_s": 1, "output_tokens": 1, "output": "b"}]
        summary = bench.summarize_rows(rows, ["FP32", "BF16"], 2)[3]
        self.assertIsNone(summary["speedup_vs_fp32_mean"])

    def test_fp32_comparison_rejects_different_case_for_same_trial(self):
        base = {"context": "Short", "trial_id": 1, "status": "ok", "generation_s": 1, "output": "{}",
                "case_id": "short-01", "prompt_sha256": "same", "expected": {"total": 1}, "comparison": {},
                "json_valid": True, "parsed_answer": {}, "weight_payload_bytes": 100}
        with self.assertRaisesRegex(ValueError, "case_id"):
            bench.compare_rows([{**base, "precision": "FP32"}, {**base, "precision": "BF16", "case_id": "short-02"}])

    def test_expected_boolean_to_integer_edit_changes_comparison_identity(self):
        with tempfile.TemporaryDirectory() as directory:
            manifest = self.copy_bank(directory)
            before = encode_cases(load_bank(manifest), WordTokenizer(), [512, 2048, 8192])
            path = manifest.parent / "short/01.json"
            answer = json.loads(path.read_text())
            answer["expected"]["fulfillable"] = int(answer["expected"]["fulfillable"])
            path.write_text(json.dumps(answer))
            after = encode_cases(load_bank(manifest), WordTokenizer(), [512, 2048, 8192])
            self.assertNotEqual(before[0]["expectation_sha256"], after[0]["expectation_sha256"])
            with self.assertRaisesRegex(ValueError, "expectation_sha256"):
                bench.validate_resume_tasks(before, after)

    def test_case_classification_is_validated_and_preserved_in_reports(self):
        with tempfile.TemporaryDirectory() as directory:
            manifest = self.copy_bank(directory)
            path = manifest.parent / "short/01.json"
            original = json.loads(path.read_text())
            for updates in ({"case_type": "other"}, {"case_type": []}, {"topic": ""}, {"topic": 1}):
                path.write_text(json.dumps({**original, **updates}))
                with self.assertRaises(ValueError):
                    load_bank(manifest)
            path.write_text(json.dumps(original))
            prompts = encode_cases(load_bank(manifest), WordTokenizer(), [256, 1024, 4096])
            rows = bench.blank_rows("BF16", prompts, "planned", "test")
            for row, prompt in zip(rows, prompts):
                self.assertEqual(row["case_type"], prompt["case_type"])
                self.assertEqual(row["topic"], prompt["topic"])
            bench.write_prompt_files(Path(directory), prompts, "Test instructions")
            markdown = (Path(directory) / "prompts.md").read_text()
            self.assertIn("Case type: math. Topic: Inventory balance.", markdown)
            self.assertIn("Case type: understanding_qna. Topic: Gift return policy.", markdown)
            changed = copy.deepcopy(prompts)
            changed[0]["case_type"] = "understanding_qna"
            with self.assertRaisesRegex(ValueError, "case_type"):
                bench.validate_resume_tasks(prompts, changed)

    def test_copy_tool_preserves_diverse_topics_and_user_edits(self):
        from tools.create_prompt_bank import copy_bank
        with tempfile.TemporaryDirectory() as directory:
            source = self.copy_bank(directory).parent
            edited = source / "medium/06.md"
            edited.write_text(edited.read_text() + "\nUser's additional context.\n")
            destination = Path(directory) / "copy"
            copied = copy_bank(source, destination, WordTokenizer())
            self.assertEqual(len(copied), 30)
            self.assertEqual((destination / "medium/06.md").read_bytes(), edited.read_bytes())
            self.assertEqual(load_bank(source / "cases.json")["cases"][15]["expected"],
                             load_bank(destination / "cases.json")["cases"][15]["expected"])


if __name__ == "__main__":
    unittest.main()
