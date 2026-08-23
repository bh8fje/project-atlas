"""Tests for user-approved workspace registration and monitoring."""

from datetime import datetime, timedelta, timezone
import json
from pathlib import Path
import sys
from tempfile import TemporaryDirectory
import unittest


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from project_atlas.application import (  # noqa: E402
    WorkspaceMonitor,
    WorkspaceRegistry,
    WorkspaceScanService,
    WorkspaceStateStore,
)
from project_atlas.domain import WorkspaceRoot  # noqa: E402
from project_atlas.local_service import WorkspaceController  # noqa: E402


ADDED_AT = datetime(2026, 8, 23, 10, 0, tzinfo=timezone.utc)


class FakePicker:
    def __init__(self, path: str | None) -> None:
        self.path = path
        self.last_language: str | None = None

    def choose(self, language: str = "zh") -> str | None:
        self.last_language = language
        return self.path


class WorkspaceRootTests(unittest.TestCase):
    def test_serializes_and_validates_monitoring_preferences(self) -> None:
        workspace = WorkspaceRoot(
            id="workspace-1",
            path="/projects",
            monitoring_enabled=True,
            scan_interval_minutes=15,
            added_at=ADDED_AT,
        )

        self.assertEqual(WorkspaceRoot.from_dict(workspace.to_dict()), workspace)
        with self.assertRaisesRegex(ValueError, "between 1 and 1440"):
            WorkspaceRoot(
                id="workspace-1",
                path="/projects",
                monitoring_enabled=True,
                scan_interval_minutes=0,
                added_at=ADDED_AT,
            )


class WorkspaceRegistryTests(unittest.TestCase):
    def test_adds_canonical_directory_once_and_persists_it(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            registry_path = root / "state" / "workspaces.json"
            registry = WorkspaceRegistry(registry_path)

            first = registry.add(root, added_at=ADDED_AT)
            second = registry.add(str(root), added_at=ADDED_AT + timedelta(minutes=1))
            reloaded = WorkspaceRegistry(registry_path).list()

        self.assertEqual(first, second)
        self.assertEqual(reloaded, (first,))

    def test_updates_monitoring_and_removes_workspace(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            registry = WorkspaceRegistry(root / "workspaces.json")
            workspace = registry.add(root, added_at=ADDED_AT)

            updated = registry.set_monitoring(
                workspace.id, enabled=True, scan_interval_minutes=30
            )
            registry.remove(workspace.id)

        self.assertTrue(updated.monitoring_enabled)
        self.assertEqual(updated.scan_interval_minutes, 30)
        self.assertEqual(registry.list(), ())

    def test_rejects_missing_or_non_directory_paths(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            file_path = root / "file.txt"
            file_path.write_text("content", encoding="utf-8")
            registry = WorkspaceRegistry(root / "workspaces.json")

            with self.assertRaisesRegex(ValueError, "does not exist"):
                registry.add(root / "missing")
            with self.assertRaisesRegex(ValueError, "must be a directory"):
                registry.add(file_path)


class WorkspaceScanServiceTests(unittest.TestCase):
    def _services(
        self, root: Path
    ) -> tuple[WorkspaceRegistry, WorkspaceScanService]:
        registry = WorkspaceRegistry(root / "atlas-data" / "workspaces.json")
        service = WorkspaceScanService(
            registry,
            WorkspaceStateStore(root / "atlas-data" / "workspace-state.json"),
        )
        return registry, service

    def test_discovers_projects_and_persists_lightweight_results(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            project = root / "sample"
            project.mkdir()
            (project / "pyproject.toml").write_text("[project]", encoding="utf-8")
            registry, service = self._services(root)
            workspace = registry.add(root, added_at=ADDED_AT)

            report = service.scan(
                workspace.id, scanned_at=ADDED_AT + timedelta(minutes=1)
            )
            persisted = service.latest_projects(workspace.id)
            summary = service.latest_summary(workspace.id)

        self.assertEqual(report.to_dict()["summary"]["project_count"], 1)
        self.assertEqual(report.projects[0]["name"], "sample")
        self.assertEqual(report.projects[0]["change_status"], "added")
        self.assertEqual(report.projects[0]["artifact_type_counts"]["configuration"], 1)
        self.assertEqual(persisted[0]["change_status"], "added")
        self.assertEqual(
            summary,
            {
                "project_count": 1,
                "added": 1,
                "changed": 0,
                "removed": 0,
                "limited": 0,
            },
        )

    def test_oversized_project_is_reported_without_stopping_workspace_scan(self) -> None:
        class OversizedAnalyzer:
            def analyze(self, project: object, *, analyzed_at: datetime) -> None:
                raise ValueError("project structure exceeds max_artifacts")

        with TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            project = root / "large-project"
            project.mkdir()
            (project / "package.json").write_text("{}", encoding="utf-8")
            registry, service = self._services(root)
            service._analyzer = OversizedAnalyzer()  # type: ignore[assignment]
            workspace = registry.add(root, added_at=ADDED_AT)

            report = service.scan(workspace.id, scanned_at=ADDED_AT)

        self.assertEqual(report.to_dict()["summary"]["limited"], 1)
        self.assertEqual(report.projects[0]["analysis_status"], "limited")
        self.assertIsNone(report.projects[0]["artifact_count"])
        self.assertEqual(report.projects[0]["artifact_type_counts"], {})
        self.assertEqual(len(report.limited_project_ids), 1)

    def test_reports_changed_and_removed_projects(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            project = root / "sample"
            project.mkdir()
            marker = project / "pyproject.toml"
            marker.write_text("[project]", encoding="utf-8")
            registry, service = self._services(root)
            workspace = registry.add(root, added_at=ADDED_AT)
            service.scan(workspace.id, scanned_at=ADDED_AT + timedelta(minutes=1))

            (project / "main.py").write_text("print('atlas')", encoding="utf-8")
            changed = service.scan(
                workspace.id, scanned_at=ADDED_AT + timedelta(minutes=2)
            )
            marker.unlink()
            removed = service.scan(
                workspace.id, scanned_at=ADDED_AT + timedelta(minutes=3)
            )

        self.assertEqual(changed.projects[0]["change_status"], "changed")
        self.assertEqual(len(removed.removed_project_ids), 1)

    def test_monitor_scans_only_enabled_due_workspaces(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            project = root / "sample"
            project.mkdir()
            (project / "package.json").write_text("{}", encoding="utf-8")
            registry, service = self._services(root)
            workspace = registry.add(
                root,
                monitoring_enabled=True,
                scan_interval_minutes=15,
                added_at=ADDED_AT,
            )
            monitor = WorkspaceMonitor(registry, service)

            first = monitor.scan_due(now=ADDED_AT)
            too_soon = monitor.scan_due(now=ADDED_AT + timedelta(minutes=14))
            due = monitor.scan_due(now=ADDED_AT + timedelta(minutes=15))

        self.assertEqual(len(first), 1)
        self.assertEqual(too_soon, ())
        self.assertEqual(len(due), 1)
        self.assertEqual(due[0].workspace.id, workspace.id)


class WorkspaceControllerTests(unittest.TestCase):
    def test_directory_picker_cancel_does_not_register_workspace(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            registry = WorkspaceRegistry(root / "workspaces.json")
            controller = WorkspaceController(
                registry,
                WorkspaceScanService(
                    registry, WorkspaceStateStore(root / "state.json")
                ),
                picker=FakePicker(None),
            )

            result = controller.select({"monitoring_enabled": True})

        self.assertEqual(result, {"cancelled": True})
        self.assertEqual(registry.list(), ())

    def test_directory_selection_runs_initial_scan(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            project = root / "sample"
            project.mkdir()
            (project / "go.mod").write_text("module sample", encoding="utf-8")
            registry = WorkspaceRegistry(root / "atlas-data" / "workspaces.json")
            picker = FakePicker(str(root))
            controller = WorkspaceController(
                registry,
                WorkspaceScanService(
                    registry,
                    WorkspaceStateStore(root / "atlas-data" / "state.json"),
                ),
                picker=picker,
            )

            result = controller.select(
                {
                    "language": "ko",
                    "monitoring_enabled": True,
                    "scan_interval_minutes": 20,
                }
            )
            registered = registry.list()[0]

        self.assertFalse(result["cancelled"])
        self.assertEqual(result["result"]["summary"]["project_count"], 1)
        self.assertTrue(registered.monitoring_enabled)
        self.assertEqual(picker.last_language, "ko")

    def test_registry_files_contain_only_local_workspace_state(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            registry_path = root / "workspaces.json"
            registry = WorkspaceRegistry(registry_path)
            registry.add(root, added_at=ADDED_AT)

            stored = json.loads(registry_path.read_text(encoding="utf-8"))

        self.assertEqual(stored["version"], 1)
        self.assertNotIn("password", json.dumps(stored).lower())

    def test_remove_forgets_workspace_without_deleting_project_files(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            project = root / "sample"
            project.mkdir()
            marker = project / "pyproject.toml"
            marker.write_text("[project]", encoding="utf-8")
            registry = WorkspaceRegistry(root / "atlas-data" / "workspaces.json")
            controller = WorkspaceController(
                registry,
                WorkspaceScanService(
                    registry,
                    WorkspaceStateStore(root / "atlas-data" / "state.json"),
                ),
                picker=FakePicker(str(root)),
            )
            controller.select({})
            workspace_id = registry.list()[0].id

            result = controller.remove(workspace_id)

            self.assertEqual(result, {"removed": True})
            self.assertEqual(registry.list(), ())
            self.assertTrue(marker.is_file())


if __name__ == "__main__":
    unittest.main()
