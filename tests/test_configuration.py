import contextlib
import io
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import compare_models
import compare_vllm
import prompt_tasks
from benchmark_config import MODEL_TIERS, load_models


class ConfigurationTests(unittest.TestCase):
    def test_config_order_does_not_change_tier_assignment(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "config.json"
            path.write_text(json.dumps({"models": {
                "complex": "custom/large", "lightweight": "custom/small", "medium": "custom/middle"}}))
            self.assertEqual(load_models(path), ["custom/small", "custom/middle", "custom/large"])

    def test_invalid_model_configuration_is_rejected(self):
        defaults = dict(zip(MODEL_TIERS, ("custom/small", "custom/middle", "custom/large")))
        invalid = [[], {}, {"models": []}, {"models": {"lightweight": "custom/small"}}]
        invalid += [{"models": {**defaults, "complex": value}} for value in (None, 42, "", " ", " custom/large", "custom/small")]
        invalid.append({"models": {**defaults, "unexpected": "custom/extra"}})
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "config.json"
            for config in invalid:
                with self.subTest(config=config):
                    path.write_text(json.dumps(config))
                    with self.assertRaises(ValueError):
                        load_models(path)

    def test_both_runners_select_models_from_the_requested_config(self):
        models = ["custom/small", "custom/middle", "custom/large"]
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "config.json"
            path.write_text(json.dumps({"models": dict(zip(MODEL_TIERS, models))}))
            self.assertEqual(compare_models.parse_args(["--config", str(path)]).models, models)
            self.assertEqual(compare_vllm.parse_args(["--config", str(path)]).model, models[0])
            for tier, model in zip(MODEL_TIERS, models):
                self.assertEqual(compare_vllm.parse_args(["--config", str(path), "--tier", tier]).model, model)

    def test_explicit_models_override_config_without_loading_it(self):
        with tempfile.TemporaryDirectory() as directory:
            missing = str(Path(directory) / "missing.json")
            self.assertEqual(compare_models.parse_args([
                "--config", missing, "--models", "override/small", "override/middle", "override/large"]).models,
                ["override/small", "override/middle", "override/large"])
            self.assertEqual(compare_vllm.parse_args(["--config", missing, "--model", "override/model"]).model,
                             "override/model")

    def test_config_errors_are_reported_as_cli_errors(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "bad.json"
            path.write_text("invalid JSON")
            for parse in (compare_models.parse_args, compare_vllm.parse_args):
                stderr = io.StringIO()
                with contextlib.redirect_stderr(stderr), self.assertRaises(SystemExit) as error:
                    parse(["--config", str(path)])
                self.assertEqual(error.exception.code, 2)
                self.assertIn("error:", stderr.getvalue())

    def test_task_builders_read_the_markdown_templates(self):
        original_dir = prompt_tasks.PROMPT_DIR
        builders = {"short": prompt_tasks.short_task, "normal": prompt_tasks.medium_task, "long": prompt_tasks.long_task}
        with tempfile.TemporaryDirectory() as directory:
            for name in builders:
                text = (original_dir / (name + ".md")).read_text(encoding="utf-8")
                (Path(directory) / (name + ".md")).write_text(text + f"Custom {name} instructions.\n", encoding="utf-8")
                (Path(directory) / (name + ".json")).write_text((original_dir / (name + ".json")).read_text())
            with patch.object(prompt_tasks, "PROMPT_DIR", Path(directory)):
                for name, builder in builders.items():
                    task = builder(7)
                    self.assertTrue(task["prompt"].endswith(f"Custom {name} instructions."))
                    self.assertIn(json.dumps(task["output_example"], ensure_ascii=False), task["prompt"])
                    self.assertNotIn("$output_example", task["prompt"])

    def test_invalid_templates_fail_before_context_fitting(self):
        with tempfile.TemporaryDirectory() as directory, patch.object(prompt_tasks, "PROMPT_DIR", Path(directory)):
            (Path(directory) / "short.json").write_text((Path(prompt_tasks.__file__).parent / "prompts/short.json").read_text())
            path = Path(directory) / "short.md"
            for text, message in (("", "empty"), ("No records", "must include"),
                                  ("$receipts $unknown", "Invalid placeholder"), ("$receipts $", "Invalid placeholder")):
                with self.subTest(text=text):
                    path.write_text(text)
                    with self.assertRaisesRegex(ValueError, message):
                        prompt_tasks.short_task()
            path.unlink()
            with self.assertRaises(FileNotFoundError):
                prompt_tasks.short_task()


if __name__ == "__main__":
    unittest.main()
