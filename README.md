# Codex Token Saver

[![Tests](https://github.com/taojing1197-dev/codex-token-saver/actions/workflows/test.yml/badge.svg)](https://github.com/taojing1197-dev/codex-token-saver/actions/workflows/test.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

A Codex skill and zero-dependency context estimator for efficient repository work.

It encourages targeted discovery, selective reading, batched checks, output summarization, and reuse of verified results while preserving correctness and safety.

## Install

Install the CLI directly from the public repository:

```bash
python3 -m pip install "git+https://github.com/taojing1197-dev/codex-token-saver.git"
codex-context-budget --version
```

The repository can also be copied into a Codex skills directory. The installed CLI and the bundled script run the same implementation.

## Estimate a repository

```bash
codex-context-budget . --top 20
codex-context-budget src docs --extensions .py,.ts,.md --max-tokens 30000
codex-context-budget . --exclude-dir generated-cache --exclude-dir vendor

# Without installation
python3 scripts/context_budget.py . --top 20
```

Extension filters accept either `.py,.md` or `py,md`. Missing input paths fail clearly instead of producing a misleading zero-file report.
Negative limits are rejected so configuration mistakes cannot masquerade as an exceeded budget.

The default estimate uses one token per four bytes and is intentionally approximate. Use `--bytes-per-token 2.5` for a more conservative estimate on multilingual prose or minified code. The tool does not inspect or upload file contents.
The estimation ratio must be a positive finite number; `NaN` and infinite values are rejected.
Use repeatable `--exclude-dir` options for project-specific generated or vendor directory names without changing the built-in safe defaults.

## Test

```bash
python3 -m unittest discover -s tests -v
```

Contributions should demonstrate measurable context reduction without removing necessary verification.
Bug reports and reproducible examples are welcome in [GitHub Issues](https://github.com/taojing1197-dev/codex-token-saver/issues).

## License

MIT
