"""Tests for deterministic project structure change detection."""

from datetime import datetime, timedelta, timezone
from pathlib import Path
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from project_atlas.domain import (  # noqa: E402
    ArtifactType,
    ChangeType,
    ProjectArtifact,
    ProjectStructure,
)
from project_atlas.history import ChangeDetectionEngine  # noqa: E402


BEFORE_AT = datetime(2026, 8, 23, 15, 0, tzinfo=timezone.utc)
AFTER_AT = BEFORE_AT + timedelta(minutes=5)


def make_artifact(
    root: Path,
    relative_path: str,
    *,
    artifact_id: str | None = None,
    updated_at: datetime = BEFORE_AT,
    artifact_type: ArtifactType = ArtifactType.SOURCE_CODE,
) -> ProjectArtifact:
    path = root if relative_path == "." else root / relative_path
    return ProjectArtifact(
        id=artifact_id or f"artifact-{relative_path}-{updated_at.timestamp()}",
        name=path.name,
        path=str(path),
        artifact_type=artifact_type,
        created_at=BEFORE_AT,
        updated_at=updated_at,
    )


def make_structure(
    root: Path,
    artifacts: tuple[ProjectArtifact, ...],
    *,
    analyzed_at: datetime,
    project_id: str = "project-1",
) -> ProjectStructure:
    return ProjectStructure(
        project_id=project_id,
        root_path=str(root),
        analyzed_at=analyzed_at,
        artifacts=artifacts,
        relationships=(),
        technologies=(),
    )


class ChangeDetectionEngineTests(unittest.TestCase):
    def test_detects_added_removed_and_modified_artifacts(self) -> None:
        root = Path("/projects/sample")
        before = make_structure(
            root,
            (
                make_artifact(root, ".", artifact_type=ArtifactType.DIRECTORY),
                make_artifact(root, "removed.py"),
                make_artifact(root, "modified.py"),
                make_artifact(root, "unchanged.py"),
            ),
            analyzed_at=BEFORE_AT,
        )
        after = make_structure(
            root,
            (
                make_artifact(root, ".", artifact_type=ArtifactType.DIRECTORY),
                make_artifact(root, "added.py", updated_at=AFTER_AT),
                make_artifact(root, "modified.py", updated_at=AFTER_AT),
                make_artifact(root, "unchanged.py"),
            ),
            analyzed_at=AFTER_AT,
        )

        changes = ChangeDetectionEngine().detect(
            before,
            after,
            from_snapshot_id="snapshot-1",
            to_snapshot_id="snapshot-2",
            recorded_at=AFTER_AT,
        )

        self.assertEqual(
            [(change.artifact_path, change.change_type) for change in changes],
            [
                ("added.py", ChangeType.ADDED),
                ("modified.py", ChangeType.MODIFIED),
                ("removed.py", ChangeType.REMOVED),
            ],
        )

    def test_initial_structure_reports_all_artifacts_as_added(self) -> None:
        root = Path("/projects/sample")
        after = make_structure(
            root,
            (make_artifact(root, ".", artifact_type=ArtifactType.DIRECTORY),),
            analyzed_at=AFTER_AT,
        )

        changes = ChangeDetectionEngine().detect(
            None,
            after,
            from_snapshot_id=None,
            to_snapshot_id="snapshot-1",
            recorded_at=AFTER_AT,
        )

        self.assertEqual(len(changes), 1)
        self.assertEqual(changes[0].artifact_path, ".")
        self.assertIs(changes[0].change_type, ChangeType.ADDED)

    def test_ignores_ephemeral_artifact_ids(self) -> None:
        root = Path("/projects/sample")
        first = make_artifact(root, "main.py", artifact_id="first-analysis-id")
        second = make_artifact(root, "main.py", artifact_id="second-analysis-id")
        before = make_structure(root, (first,), analyzed_at=BEFORE_AT)
        after = make_structure(root, (second,), analyzed_at=AFTER_AT)

        changes = ChangeDetectionEngine().detect(
            before,
            after,
            from_snapshot_id="snapshot-1",
            to_snapshot_id="snapshot-2",
            recorded_at=AFTER_AT,
        )

        self.assertEqual(changes, ())

    def test_change_ids_are_deterministic(self) -> None:
        root = Path("/projects/sample")
        before = make_structure(
            root,
            (make_artifact(root, "main.py"),),
            analyzed_at=BEFORE_AT,
        )
        after = make_structure(root, (), analyzed_at=AFTER_AT)
        engine = ChangeDetectionEngine()

        first = engine.detect(
            before,
            after,
            from_snapshot_id="snapshot-1",
            to_snapshot_id="snapshot-2",
            recorded_at=AFTER_AT,
        )
        second = engine.detect(
            before,
            after,
            from_snapshot_id="snapshot-1",
            to_snapshot_id="snapshot-2",
            recorded_at=AFTER_AT + timedelta(minutes=1),
        )

        self.assertEqual(first[0].id, second[0].id)

    def test_rejects_mismatched_projects_and_reverse_time(self) -> None:
        root = Path("/projects/sample")
        before = make_structure(root, (), analyzed_at=AFTER_AT)
        different_project = make_structure(
            root, (), analyzed_at=AFTER_AT, project_id="project-2"
        )
        earlier = make_structure(root, (), analyzed_at=BEFORE_AT)
        engine = ChangeDetectionEngine()

        with self.assertRaisesRegex(ValueError, "same project"):
            engine.detect(
                before,
                different_project,
                from_snapshot_id="snapshot-1",
                to_snapshot_id="snapshot-2",
            )
        with self.assertRaisesRegex(ValueError, "must not be analyzed"):
            engine.detect(
                before,
                earlier,
                from_snapshot_id="snapshot-1",
                to_snapshot_id="snapshot-2",
            )

    def test_rejects_invalid_initial_snapshot_reference(self) -> None:
        root = Path("/projects/sample")
        after = make_structure(root, (), analyzed_at=AFTER_AT)

        with self.assertRaisesRegex(ValueError, "must be None"):
            ChangeDetectionEngine().detect(
                None,
                after,
                from_snapshot_id="snapshot-0",
                to_snapshot_id="snapshot-1",
            )


if __name__ == "__main__":
    unittest.main()
