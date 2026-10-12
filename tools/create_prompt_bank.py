"""Validate and copy the editable topic-diverse bank; never run during inference."""
from __future__ import annotations

import argparse
import json
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from prompt_bank import load_bank, encode_cases


def copy_bank(source_dir, output_dir, tokenizer=None):
    """Use the Markdown/JSON files as the source of truth, including user edits."""
    source_dir, output_dir = Path(source_dir).resolve(), Path(output_dir).resolve()
    manifest = source_dir / "cases.json"
    bank = load_bank(manifest)
    prompts = encode_cases(bank, tokenizer, [256, 1024, 4096], enable_thinking=False)
    definition = json.loads(manifest.read_text(encoding="utf-8"))
    names = {"cases.json", definition["system"]}
    for entries in definition["contexts"].values():
        for entry in entries:
            names.update((entry["prompt"], entry["expected"]))
    # A portable copy must keep every referenced asset inside the new folder.
    for name in names:
        if Path(name).is_absolute() or ".." in Path(name).parts:
            raise ValueError(f"Copy requires paths relative to the source folder: {name}")
    if source_dir != output_dir:
        for name in sorted(names):
            destination = output_dir / name
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(source_dir / name, destination)
    return prompts


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-dir", type=Path, default=ROOT / "prompts")
    parser.add_argument("--output-dir", type=Path, default=ROOT / "prompts")
    parser.add_argument("--tokenizer", help="Optional model ID or local folder for exact token-budget validation")
    args = parser.parse_args()
    tokenizer = None
    if args.tokenizer:
        from transformers import AutoTokenizer
        tokenizer = AutoTokenizer.from_pretrained(args.tokenizer, trust_remote_code=False)
    for prompt in copy_bank(args.source_dir, args.output_dir, tokenizer):
        print(prompt["case_id"], prompt["case_type"], prompt["topic"], prompt["input_tokens"], "tokens")


if __name__ == "__main__":
    main()
