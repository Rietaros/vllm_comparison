"""Editable ordered prompt/answer pairs, one distinct case per trial."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

from answer_comparison import comparison_options, validate_expected

CONTEXTS = ("Short", "Medium", "Long")
DEFAULT_MANIFEST = Path(__file__).resolve().parent / "prompts" / "cases.json"
PROMPT_SUITE = "diverse-math-qna-cases-v6"
CASE_TYPES = ("math", "understanding_qna")


def read_text(path):
    text = path.read_text(encoding="utf-8").rstrip("\r\n")
    if not text.strip():
        raise ValueError(f"Empty prompt file: {path}")
    return text


def load_bank(manifest=DEFAULT_MANIFEST, count=10):
    manifest = Path(manifest).resolve()
    definition = json.loads(manifest.read_text(encoding="utf-8"))
    if (not isinstance(definition, dict) or set(definition) != {"version", "system", "contexts"}
            or type(definition["version"]) is not int or definition["version"] != 1):
        raise ValueError("Prompt manifest requires version 1, system, and contexts")
    if not isinstance(definition["contexts"], dict) or set(definition["contexts"]) != set(CONTEXTS):
        raise ValueError("Prompt manifest must define Short, Medium, and Long")
    if type(count) is not int or count <= 0:
        raise ValueError("Number of prompt cases must be positive")

    def asset(name, suffix):
        if not isinstance(name, str) or not name.strip():
            raise ValueError("Manifest file paths must be nonempty strings")
        path = (manifest.parent / name).resolve()
        if path.suffix != suffix:
            raise ValueError(f"Expected a {suffix} file: {path}")
        return path

    system_path = asset(definition["system"], ".md")
    system = read_text(system_path)
    files = {manifest, system_path}
    cases, seen_ids = [], set()
    for context in CONTEXTS:
        entries = definition["contexts"][context]
        if not isinstance(entries, list) or len(entries) < count:
            available = len(entries) if isinstance(entries, list) else 0
            raise ValueError(f"{context} has {available} cases; --repeats {count} requires {count} distinct cases. Add cases to the manifest.")
        seen_text = set()
        for index, entry in enumerate(entries, 1):
            if not isinstance(entry, dict) or set(entry) != {"id", "prompt", "expected"}:
                raise ValueError(f"{context} case {index} requires id, prompt, and expected")
            case_id = entry["id"]
            if not isinstance(case_id, str) or not case_id.strip() or case_id in seen_ids:
                raise ValueError(f"Case IDs must be nonempty and unique: {case_id!r}")
            seen_ids.add(case_id)
            prompt_path, expected_path = asset(entry["prompt"], ".md"), asset(entry["expected"], ".json")
            files.update((prompt_path, expected_path))
            text = read_text(prompt_path)
            if text in seen_text:
                raise ValueError(f"Duplicate {context} prompt: {prompt_path}")
            seen_text.add(text)
            answer = json.loads(expected_path.read_text(encoding="utf-8"))
            allowed = {"mode", "task_id", "description", "case_type", "topic", "expected", "reasoning_fields", "comparison"}
            if not isinstance(answer, dict) or set(answer) - allowed or answer.get("mode", "static") != "static":
                raise ValueError(f"Case expectations must use static mode and literal expected values: {expected_path}")
            reasoning = validate_expected(answer.get("expected"), answer.get("reasoning_fields"))
            options = comparison_options(answer.get("comparison"))
            for key in ("task_id", "description", "topic"):
                if key in answer and (not isinstance(answer[key], str) or not answer[key].strip()):
                    raise ValueError(f"{expected_path}: {key} must be a nonempty string")
            if "case_type" in answer and answer["case_type"] not in CASE_TYPES:
                raise ValueError(f"{expected_path}: case_type must be math or understanding_qna")
            if index <= count:
                cases.append({"context": context, "trial_id": index, "case_id": case_id,
                    "task_id": answer.get("task_id", case_id), "task_description": answer.get("description", case_id),
                    "case_type": answer.get("case_type"), "topic": answer.get("topic"),
                    "task_mode": "static", "prompt": text, "record_count": 0, "task_data": {},
                    "expected": answer["expected"], "reasoning_fields": reasoning, "comparison": options,
                    "expectation_sha256": hashlib.sha256(json.dumps({"expected": answer["expected"],
                        "reasoning_fields": reasoning, "comparison": options}, sort_keys=True).encode()).hexdigest(),
                    "prompt_file": str(prompt_path), "expected_file": str(expected_path),
                    "prompt_text_sha256": hashlib.sha256(text.encode()).hexdigest()})
    digest = hashlib.sha256()
    for path in sorted(files):
        content = path.read_bytes()
        # Include referenced path names as well as file contents; file swaps
        # and expected-answer-only edits must invalidate resume.
        digest.update(str(path).encode() + b"\0" + len(content).to_bytes(8, "big") + content)
    return {"system": system, "cases": cases, "sha256": digest.hexdigest(), "manifest": str(manifest)}


def encode_cases(bank, tokenizer, budgets, enable_thinking=None):
    prompts = []
    for case in bank["cases"]:
        budget = budgets[CONTEXTS.index(case["context"])]
        ids = None
        if tokenizer is not None:
            extra = {} if enable_thinking is None else {"enable_thinking": enable_thinking}
            ids = list(tokenizer.apply_chat_template([
                {"role": "system", "content": bank["system"]}, {"role": "user", "content": case["prompt"]}],
                tokenize=True, add_generation_prompt=True, return_dict=False, **extra))
            if len(ids) > budget:
                raise ValueError(f"{case['case_id']} has {len(ids)} input tokens, exceeding the {case['context']} budget {budget}. Edit the prompt or raise --context-tokens.")
        prompts.append({**case, "prompt_suite": PROMPT_SUITE, "target_tokens": budget,
                        "input_tokens": len(ids) if ids is not None else None,
                        "prompt_token_ids": ids,
                        "prompt_sha256": hashlib.sha256(json.dumps(ids).encode()).hexdigest() if ids is not None else None})
    return prompts
