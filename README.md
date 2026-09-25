# Codex Token Saver

A Codex skill and zero-dependency context estimator for efficient repository work.

It encourages targeted discovery, selective reading, batched checks, output summarization, and reuse of verified results while preserving correctness and safety.

## Estimate a repository

```bash
python3 scripts/context_budget.py . --top 20
python3 scripts/context_budget.py src docs --extensions .py,.ts,.md --max-tokens 30000
```

Extension filters accept either `.py,.md` or `py,md`. Missing input paths fail clearly instead of producing a misleading zero-file report.

The default estimate uses one token per four bytes and is intentionally approximate. Use `--bytes-per-token 2.5` for a more conservative estimate on multilingual prose or minified code. The tool does not inspect or upload file contents.

## Test

```bash
python3 -m unittest discover -s tests -v
```

Contributions should demonstrate measurable context reduction without removing necessary verification.

## License

MIT
