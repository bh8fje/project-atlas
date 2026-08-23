"""Tests for bounded local project discovery."""

from datetime import datetime, timezone
from pathlib import Path
import sys
from tempfile import TemporaryDirectory
import unittest
from uuid import UUID


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from project_atlas.discovery import (  # noqa: E402
    DiscoveryScope,
    LocalProjectDiscoveryEngine,
)
from project_atlas.domain import ProjectStatus  # noqa: E402


OBSERVED_AT = datetime(2026, 8, 23, 12, 0, tzinfo=timezone.utc)


class DiscoveryScopeTests(unittest.TestCase):
    def test_scope_requires_explicit_roots(self) -> None:
        with self.assertRaisesRegex(ValueError, "roots"):
            DiscoveryScope(roots=())

    def test_scope_rejects_negative_depth(self) -> None:
        with self.assertRaisesRegex(ValueError, "max_depth"):
            DiscoveryScope(roots=("/tmp",), max_depth=-1)


class LocalProjectDiscoveryEngineTests(unittest.TestCase):
    def test_discovers_project_markers_and_creates_projects(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            python_project = root / "python-project"
            web_project = root / "web-project"
            ordinary_directory = root / "notes"
            python_project.mkdir()
            web_project.mkdir()
            ordinary_directory.mkdir()
            (python_project / "pyproject.toml").write_text("", encoding="utf-8")
            (web_project / "package.json").write_text("{}", encoding="utf-8")

            projects = LocalProjectDiscoveryEngine().discover(
                DiscoveryScope(roots=(root,)), observed_at=OBSERVED_AT
            )

        self.assertEqual(
            [project.name for project in projects],
            ["python-project", "web-project"],
        )
        for project in projects:
            UUID(project.id)
            self.assertIs(project.status, ProjectStatus.ACTIVE)
            self.assertEqual(project.created_at, OBSERVED_AT)
            self.assertEqual(project.updated_at, OBSERVED_AT)

    def test_honors_maximum_depth(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            nested_project = root / "level-one" / "level-two"
            nested_project.mkdir(parents=True)
            (nested_project / "go.mod").write_text("module example", encoding="utf-8")
            engine = LocalProjectDiscoveryEngine()

            shallow = engine.discover(DiscoveryScope(roots=(root,), max_depth=1))
            deep = engine.discover(DiscoveryScope(roots=(root,), max_depth=2))

        self.assertEqual(shallow, ())
        self.assertEqual(len(deep), 1)
        self.assertEqual(deep[0].name, "level-two")

    def test_prunes_excluded_directories(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            dependency_project = root / "node_modules" / "dependency"
            dependency_project.mkdir(parents=True)
            (dependency_project / "package.json").write_text("{}", encoding="utf-8")

            projects = LocalProjectDiscoveryEngine().discover(
                DiscoveryScope(roots=(root,))
            )

        self.assertEqual(projects, ())

    def test_does_not_follow_directory_symlinks(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            external = root / "external-project"
            scan_root = root / "scan-root"
            external.mkdir()
            scan_root.mkdir()
            (external / "Cargo.toml").write_text("", encoding="utf-8")
            (scan_root / "linked-project").symlink_to(external, target_is_directory=True)

            projects = LocalProjectDiscoveryEngine().discover(
                DiscoveryScope(roots=(scan_root,))
            )

        self.assertEqual(projects, ())

    def test_rejects_missing_or_file_roots(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            file_root = root / "file.txt"
            file_root.write_text("content", encoding="utf-8")
            engine = LocalProjectDiscoveryEngine()

            with self.assertRaisesRegex(ValueError, "does not exist"):
                engine.discover(DiscoveryScope(roots=(root / "missing",)))
            with self.assertRaisesRegex(ValueError, "must be a directory"):
                engine.discover(DiscoveryScope(roots=(file_root,)))

    def test_rejects_naive_observation_time(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)

            with self.assertRaisesRegex(ValueError, "timezone"):
                LocalProjectDiscoveryEngine().discover(
                    DiscoveryScope(roots=(root,)),
                    observed_at=datetime(2026, 8, 23, 12, 0),
                )

    def test_rejects_non_datetime_observation_time(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)

            with self.assertRaisesRegex(TypeError, "datetime"):
                LocalProjectDiscoveryEngine().discover(
                    DiscoveryScope(roots=(root,)),
                    observed_at="2026-08-23T12:00:00Z",  # type: ignore[arg-type]
                )


if __name__ == "__main__":
    unittest.main()
