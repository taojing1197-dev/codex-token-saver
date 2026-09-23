# Context budgeting

The helper estimates roughly one token per four bytes. This is intentionally approximate: language, code, minification, and model tokenization change the real count.

```bash
python3 scripts/context_budget.py . --top 20
python3 scripts/context_budget.py src docs --extensions .py,.ts,.md --max-tokens 30000
python3 scripts/context_budget.py . --json
```

Recommended sequence:

1. Exclude generated output, dependencies, caches, coverage, and VCS data.
2. Inspect the largest relevant files by headings or targeted matches.
3. Read callers and schemas before full implementations.
4. Reserve context for verification output and the final explanation.

Exit code 1 means the estimate exceeds `--max-tokens`. It is a planning signal, not proof that the task cannot be completed.
