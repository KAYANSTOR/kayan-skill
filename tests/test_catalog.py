from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class CatalogTests(unittest.TestCase):
    def test_validator_passes_without_executing_skill_code(self) -> None:
        result = subprocess.run(
            [sys.executable, str(ROOT / "scripts" / "validate_catalog.py"), "--root", str(ROOT)],
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_registry_matches_skill_count(self) -> None:
        registry = json.loads((ROOT / "registry" / "SKILLS_REGISTRY.json").read_text(encoding="utf-8"))
        actual = list(ROOT.glob("[0-9][0-9]-*/**/SKILL.md"))
        self.assertEqual(registry["skill_count"], len(actual))
        self.assertEqual(len(registry["skills"]), len(actual))

    def test_all_governance_files_exist(self) -> None:
        for name in ("SECURITY_POLICY.md", "AGENT_COMPATIBILITY.md", "WORKFLOW_POLICY.md"):
            self.assertTrue((ROOT / "00-MASTER" / name).is_file(), name)
        for name in ("SOURCES_MANIFEST.json", "COMPATIBILITY_MATRIX.json"):
            self.assertTrue((ROOT / "registry" / name).is_file(), name)


if __name__ == "__main__":
    unittest.main()
