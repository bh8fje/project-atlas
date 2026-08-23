import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DASHBOARD = ROOT / "dashboard"


class LocalDashboardTests(unittest.TestCase):
    def test_sites_scaffold_has_required_files_and_commands(self) -> None:
        package = json.loads((DASHBOARD / "package.json").read_text())
        self.assertEqual(package["name"], "project-atlas-dashboard")
        self.assertIn("dev", package["scripts"])
        self.assertIn("build", package["scripts"])
        self.assertTrue((DASHBOARD / "vite.config.ts").is_file())

    def test_dashboard_covers_status_history_and_relationships(self) -> None:
        page = (DASHBOARD / "app" / "page.tsx").read_text()
        for label in ("Project health", "Project history", "Knowledge map"):
            self.assertIn(label, page)

    def test_dashboard_declares_local_read_only_boundary(self) -> None:
        page = (DASHBOARD / "app" / "page.tsx").read_text()
        self.assertIn("Local only", page)
        self.assertIn("Read only", page)
        self.assertNotIn("fetch(", page)
        self.assertNotIn("https://", page)

    def test_cloud_resources_are_not_configured(self) -> None:
        hosting = json.loads((DASHBOARD / ".openai" / "hosting.json").read_text())
        self.assertIsNone(hosting["d1"])
        self.assertIsNone(hosting["r2"])


if __name__ == "__main__":
    unittest.main()
