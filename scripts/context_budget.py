#!/usr/bin/env python3
"""Estimate repository context cost without reading file contents."""

from __future__ import annotations

import argparse
import json
import math
import os
import sys
from pathlib import Path


SKIP_DIRS = {
    ".git", ".hg", ".svn", ".next", ".nuxt", ".venv", "venv", "node_modules",
    "dist", "build", "coverage", "__pycache__", ".cache", ".pytest_cache",
}
DEFAULT_EXTENSIONS = {
    ".c", ".cc", ".cpp", ".css", ".go", ".h", ".hpp", ".html", ".java",
    ".js", ".json", ".jsx", ".kt", ".md", ".mjs", ".php", ".py", ".rb",
    ".rs", ".scss", ".sh", ".sql", ".svelte", ".swift", ".toml", ".ts",
    ".tsx", ".txt", ".vue", ".xml", ".yaml", ".yml",
}


def iter_files(paths: list[Path], extensions: set[str]):
    for entry in paths:
        entry = entry.expanduser().resolve()
        if entry.is_file():
            if not extensions or entry.suffix.lower() in extensions:
                yield entry
            continue
        if not entry.is_dir():
            continue
        for root, dirs, files in os.walk(entry, followlinks=False):
            dirs[:] = sorted(name for name in dirs if name not in SKIP_DIRS and not (Path(root) / name).is_symlink())
            for name in sorted(files):
                path = Path(root) / name
                if path.is_symlink():
                    continue
                if extensions and path.suffix.lower() not in extensions:
                    continue
                yield path


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("paths", nargs="*", default=["."], type=Path)
    parser.add_argument("--extensions", help="comma-separated extensions such as .py,.md")
    parser.add_argument("--top", type=int, default=20)
    parser.add_argument("--max-tokens", type=int)
    parser.add_argument("--json", action="store_true", dest="as_json")
    args = parser.parse_args()
    extensions = DEFAULT_EXTENSIONS
    if args.extensions is not None:
        extensions = {value.strip().lower() for value in args.extensions.split(",") if value.strip()}

    seen: set[Path] = set()
    rows = []
    for path in iter_files(args.paths, extensions):
        if path in seen:
            continue
        seen.add(path)
        try:
            size = path.stat().st_size
        except OSError:
            continue
        rows.append({"path": str(path), "bytes": size, "estimated_tokens": math.ceil(size / 4)})
    rows.sort(key=lambda item: (-item["estimated_tokens"], item["path"]))
    total_bytes = sum(item["bytes"] for item in rows)
    total_tokens = sum(item["estimated_tokens"] for item in rows)
    report = {
        "files": len(rows),
        "bytes": total_bytes,
        "estimated_tokens": total_tokens,
        "top": rows[: max(args.top, 0)],
        "estimate_note": "Approximation only: one token per four bytes.",
    }
    if args.as_json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print(f"files={report['files']} bytes={total_bytes} estimated_tokens={total_tokens}")
        for item in report["top"]:
            print(f"{item['estimated_tokens']:>10}  {item['bytes']:>12}  {item['path']}")
    return 1 if args.max_tokens is not None and total_tokens > args.max_tokens else 0


if __name__ == "__main__":
    raise SystemExit(main())
