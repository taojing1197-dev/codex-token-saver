import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).parents[1] / "scripts" / "context_budget.py"


class ContextBudgetTests(unittest.TestCase):
    def test_skips_dependencies_and_counts_selected_extensions(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "main.py").write_text("x" * 40, encoding="utf-8")
            (root / "notes.md").write_text("y" * 20, encoding="utf-8")
            (root / "image.bin").write_bytes(b"z" * 100)
            modules = root / "node_modules"
            modules.mkdir()
            (modules / "large.js").write_text("z" * 1000, encoding="utf-8")
            result = subprocess.run([sys.executable, str(SCRIPT), str(root), "--json"], text=True, capture_output=True)
            report = json.loads(result.stdout)
            self.assertEqual(result.returncode, 0)
            self.assertEqual(report["files"], 2)
            self.assertEqual(report["estimated_tokens"], 15)

    def test_budget_exit_code(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "large.txt"
            path.write_text("x" * 100, encoding="utf-8")
            result = subprocess.run([sys.executable, str(SCRIPT), str(path), "--max-tokens", "10"], text=True, capture_output=True)
            self.assertEqual(result.returncode, 1)


if __name__ == "__main__":
    unittest.main()
