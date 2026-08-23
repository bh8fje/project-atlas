"""Tests for the Project Atlas engineering baseline."""

from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]


class ProjectBaselineTests(unittest.TestCase):
    def test_required_project_files_exist(self) -> None:
        required_paths = (
            "README.md",
            "AGENTS.md",
            "ROADMAP.md",
            "PROJECT_STATUS.md",
            "pyproject.toml",
            "config",
            "docs",
            "src/project_atlas",
            "tests",
        )

        for relative_path in required_paths:
            with self.subTest(path=relative_path):
                self.assertTrue((ROOT / relative_path).exists())

    def test_package_declares_version_without_business_api(self) -> None:
        package_init = ROOT / "src" / "project_atlas" / "__init__.py"
        content = package_init.read_text(encoding="utf-8")

        self.assertIn('__version__ = "0.1.0"', content)


if __name__ == "__main__":
    unittest.main()
