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

    def test_dashboard_covers_release_status_history_and_composition(self) -> None:
        page = (DASHBOARD / "app" / "page.tsx").read_text()
        translations = (DASHBOARD / "app" / "i18n.ts").read_text()
        for label in ("Release status", "Version history", "Project composition"):
            self.assertIn(label, translations)
        for section_id in ('id="health"', 'id="history"', 'id="composition"'):
            self.assertIn(section_id, page)

    def test_dashboard_declares_local_read_only_boundary(self) -> None:
        page = (DASHBOARD / "app" / "page.tsx").read_text()
        translations = (DASHBOARD / "app" / "i18n.ts").read_text()
        self.assertIn("Local only", translations)
        self.assertIn("Local operation", translations)
        self.assertIn("t.localOnly", page)
        self.assertIn("t.readOnly", page)
        self.assertNotIn("fetch(", page)
        self.assertNotIn("https://", page)

    def test_cloud_resources_are_not_configured(self) -> None:
        hosting = json.loads((DASHBOARD / ".openai" / "hosting.json").read_text())
        self.assertIsNone(hosting["d1"])
        self.assertIsNone(hosting["r2"])

    def test_composition_view_explains_nodes_and_connections(self) -> None:
        page = (DASHBOARD / "app" / "page.tsx").read_text()
        translations = (DASHBOARD / "app" / "i18n.ts").read_text()
        for label in ("Project Atlas 包含哪些部分", "源代码存放于", "包含", "项目资料保存在本机"):
            self.assertIn(label, translations)
        self.assertIn("t.compositionRelations[0]", page)
        self.assertIn("不是自动扫描或实时分析结果", translations)

    def test_static_release_record_is_not_presented_as_live_health(self) -> None:
        page = (DASHBOARD / "app" / "page.tsx").read_text()
        translations = (DASHBOARD / "app" / "i18n.ts").read_text()
        self.assertIn("不是实时监控结果", translations)
        self.assertIn("t.releaseRecordNote", page)
        self.assertNotIn('className="health-ring"', page)
        self.assertNotIn("<strong>100%</strong>", page)
        self.assertNotIn("一切运行稳定", translations)

    def test_dashboard_design_contract_matches_project_goal(self) -> None:
        design = (ROOT / "docs" / "DASHBOARD_DESIGN.md").read_text()
        self.assertIn("发布记录不等于实时状态", design)
        self.assertIn("项目组成不等于项目关系", design)
        self.assertIn("不得伪造实时分析结果", design)

    def test_workspace_manager_uses_only_the_loopback_service(self) -> None:
        manager = (DASHBOARD / "app" / "workspace-manager.tsx").read_text()
        self.assertIn("http://127.0.0.1:43821", manager)
        self.assertNotIn("https://", manager)
        self.assertIn("/api/workspaces", manager)
        self.assertIn("window.setInterval", manager)

    def test_workspace_manager_exposes_explicit_local_controls(self) -> None:
        manager = (DASHBOARD / "app" / "workspace-manager.tsx").read_text()
        translations = (DASHBOARD / "app" / "i18n.ts").read_text()
        for control in ("chooseDirectory", "scanNow", "automaticChecks", "interval", "confirmRemove"):
            self.assertIn(control, manager)
        self.assertIn("目录中的文件不会被删除", translations)
        self.assertIn("关闭本地服务后，自动检查将停止", translations)

    def test_workspace_manager_displays_the_latest_check_summary(self) -> None:
        manager = (DASHBOARD / "app" / "workspace-manager.tsx").read_text()
        for field in ("project_count", "added", "changed", "removed", "limited"):
            self.assertIn(f"last_summary.{field}", manager)
        self.assertIn("change_status", manager)


if __name__ == "__main__":
    unittest.main()
