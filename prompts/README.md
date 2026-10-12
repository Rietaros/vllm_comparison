# Editable prompt and answer cases

There are **10 Short, 10 Medium, and 10 Long cases**, each with a different topic. Each context contains **5 math cases** (`01`–`05`) and **5 understanding Q&A cases** (`06`–`10`). Topics also differ across contexts, for 30 distinct topics in total.

Math cases require calculations from supplied values. Understanding Q&A cases require reading the supplied passage, applying its rules, and answering questions without arithmetic. Short passages are compact; Medium passages add policy details and distractors; Long dossiers combine registers, corrections, or conflicting sources.

| Case | Type | Short topic | Medium topic | Long topic |
|---|---|---|---|---|
| 01 | Math | Inventory balance | Event catering budget | Community project funding |
| 02 | Math | Cafe bill | Water meter invoice | Time-of-use energy bill |
| 03 | Math | Train travel time | Courier route selection | Weighted course grade |
| 04 | Math | Garden planting area | Factory batch yield | Backup storage capacity |
| 05 | Math | Quiz points | Study time planning | Scholarship award allocation |
| 06 | Understanding Q&A | Gift return policy | IT incident escalation | Emergency drill routing |
| 07 | Understanding Q&A | Library visitor access | Accessible venue booking | Software release approval |
| 08 | Understanding Q&A | Fern care instructions | Confidential document routing | Heritage artifact provenance |
| 09 | Understanding Q&A | Suspicious login email | Wildlife briefing comprehension | Community moderation appeal |
| 10 | Understanding Q&A | Museum object location | Editorial correction workflow | Research consent withdrawal |

Every case is two files:

- `short/01.md` contains the question and its data.
- `short/01.json` contains the expected JSON answer and comparison rules.

The same pairing applies to `02` through `10`, and to the `medium/` and `long/` folders. Edit both files together when changing a question. Answers are literal values; the benchmark never regenerates or overrides your expected answer.

For example, a prompt asking for `6 * 7` and a JSON integer field `total` can use:

```json
{
  "mode": "static",
  "case_type": "math",
  "topic": "Multiplication",
  "expected": {"total": 42},
  "reasoning_fields": ["total"],
  "comparison": {"allow_extra_fields": false, "case_sensitive": true}
}
```

`cases.json` lists the case IDs and file paths in trial order. Trial 1 uses `01`, trial 2 uses `02`, and trial 10 uses `10`. All precision variants use the same case IDs and answers. To add an eleventh case, create another Markdown/JSON pair in each context and append its entry to each manifest list. The runner rejects missing cases and duplicate IDs or prompts.

`case_type` and `topic` identify the two case types and the subject in reports and per-trial CSV/JSON output. They are optional for custom datasets; when present, `case_type` must be `math` or `understanding_qna`, and `topic` must be a nonempty string. Keep them aligned with the passage when editing a case. The default bank's topic uniqueness and 5/5 split are checked by the test suite; custom banks can choose their own composition.

`system.md` supplies shared instructions. Markdown is used literally, including dollar signs. The default input budgets are 256, 1,024, and 4,096 tokens including system/chat formatting; keep edited prompts within the budget or raise `--context-tokens`. JSON types match exactly, so `42`, `"42"`, `42.0`, and `true` differ.

Use `--repeats 10` for the balanced 5 math / 5 Q&A cases in each context. `--repeats 1` selects only the first math pair; smaller prefixes do not preserve the full split. Use a fresh output folder after editing files; resume checks the questions, answers, labels, rules, and manifest order.

The optional `tools/create_prompt_bank.py` command validates and copies this bank, including user edits, instead of regenerating repeated scenarios. Supply `--output-dir PATH` to create a copy and `--tokenizer MODEL_OR_LOCAL_PATH` to check exact input lengths against the default budgets.

The old top-level `short.md`, `normal.md`, and `long.md` files are historical templates. Current runs use the files referenced by `cases.json`.
