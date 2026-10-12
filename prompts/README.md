# Editable prompt and answer cases

There are **10 Short, 10 Medium, and 10 Long cases**. Every case is two files:

- `short/01.md` contains the question and its data.
- `short/01.json` contains the expected JSON answer and comparison rules.

The same pairing applies to `02` through `10`, and to the `medium/` and `long/` folders. Edit both files together when changing a question. Answers are literal values; the benchmark never regenerates or overrides your expected answer.

For example, a prompt asking for `6 * 7` and a JSON integer field `total` can use:

```json
{
  "mode": "static",
  "expected": {"total": 42},
  "reasoning_fields": ["total"],
  "comparison": {"allow_extra_fields": false, "case_sensitive": true}
}
```

`cases.json` lists the case IDs and file paths in trial order. Trial 1 uses `01`, trial 2 uses `02`, and trial 10 uses `10`. All precision variants use the same case IDs and answers. To add an eleventh case, create another Markdown/JSON pair in each context and append its entry to each manifest list. The runner rejects missing cases and duplicate IDs or prompts.

`system.md` supplies shared instructions. Markdown is used literally, including dollar signs. The default input budgets are 256, 1,024, and 4,096 tokens including system/chat formatting; keep edited prompts within the budget or raise `--context-tokens`. JSON types match exactly, so `42`, `"42"`, `42.0`, and `true` differ.

Use `--repeats 10` for all ten cases, or `--repeats 1` for only the first pair in each context. Use a fresh output folder after editing files; resume checks the questions, answers, rules, and manifest order.

The old top-level `short.md`, `normal.md`, and `long.md` files are historical templates. Current runs use the files referenced by `cases.json`.
