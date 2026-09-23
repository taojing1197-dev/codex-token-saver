---
name: codex-token-saver
description: Reduce Codex context and tool-output usage for repository work by estimating file cost, narrowing discovery, batching independent checks, and reusing verified results without weakening correctness. Use when the user asks to save tokens, work within a context budget, or make a large-repository task more efficient.
---

# Codex Token Saver

Save tokens by avoiding irrelevant context, not by skipping necessary verification. Never trade away safety, correctness, or user-requested detail.

## Start narrow

1. Restate the concrete deliverable in one sentence.
2. Search filenames and targeted symbols before reading files. Prefer `rg --files`, `rg -n`, Git status, and small schema summaries.
3. Use `scripts/context_budget.py` to estimate the largest context contributors before opening broad directories. Read [references/budgeting.md](references/budgeting.md) when a numeric budget or a very large repository is involved.
4. Read matched slices, headers, schemas, and callers first. Expand only when an unanswered decision requires it.

## Reuse and batch

- Reuse unchanged file contents, command results, and verified facts within the task.
- Batch independent read-only checks when doing so keeps outputs attributable.
- Summarize large logs and structured files by counts, errors, paths, and decisive fields.
- Prefer existing scripts and tests over re-deriving their behavior from every implementation file.
- Do not repeat a failed command unchanged. Inspect the failure and choose one targeted next step.

## Guardrails

- Do not invent a token count. The helper reports an estimate based on byte size, not the model's exact tokenizer.
- Do not omit required skill instructions, project rules, security checks, or production verification.
- Do not use a subagent for a small task merely to reduce visible context; delegation has its own cost and must be authorized when required.
- If a user requests exhaustive review, prioritize coverage and explain any budget tradeoff rather than silently narrowing scope.

## Finish compactly

Lead with the result. Report changed files, verification, and remaining risk. Include detailed logs only when the user asks or they are necessary to diagnose a failure.
