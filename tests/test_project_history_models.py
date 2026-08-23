"""Tests for project snapshot, change, and history event contracts."""

from datetime import datetime, timedelta, timezone
from pathlib import Path
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from project_atlas.domain import (  # noqa: E402
    ChangeType,
    HistoryEventType,
    ProjectChange,
    ProjectFingerprint,
    ProjectHistoryEvent,
    ProjectSnapshot,
)


RECORDED_AT = datetime(2026, 8, 23, 15, 0, tzinfo=timezone.utc)


def make_fingerprint(*, project_id: str = "project-1") -> ProjectFingerprint:
    return ProjectFingerprint(
        project_id=project_id,
        stable_project_id="12345678-1234-5678-1234-567812345678",
        algorithm="sha256-metadata-v1",
        digest="a" * 64,
        generated_at=RECORDED_AT,
        artifact_count=3,
    )


class ProjectSnapshotTests(unittest.TestCase):
    def test_creates_snapshot_and_exposes_artifact_count(self) -> None:
        snapshot = ProjectSnapshot(
            id="snapshot-1",
            project_id="project-1",
            fingerprint=make_fingerprint(),
            created_at=RECORDED_AT,
        )

        self.assertEqual(snapshot.artifact_count, 3)

    def test_snapshot_round_trip_serialization(self) -> None:
        snapshot = ProjectSnapshot(
            id="snapshot-1",
            project_id="project-1",
            fingerprint=make_fingerprint(),
            created_at=RECORDED_AT,
        )

        restored = ProjectSnapshot.from_dict(snapshot.to_dict())

        self.assertEqual(restored, snapshot)

    def test_snapshot_rejects_mismatched_project_and_future_fingerprint(self) -> None:
        with self.assertRaisesRegex(ValueError, "project_id"):
            ProjectSnapshot(
                id="snapshot-1",
                project_id="different-project",
                fingerprint=make_fingerprint(),
                created_at=RECORDED_AT,
            )
        with self.assertRaisesRegex(ValueError, "after the snapshot"):
            ProjectSnapshot(
                id="snapshot-1",
                project_id="project-1",
                fingerprint=make_fingerprint(),
                created_at=RECORDED_AT - timedelta(seconds=1),
            )


class ProjectChangeTests(unittest.TestCase):
    def test_change_round_trip_serialization(self) -> None:
        change = ProjectChange(
            id="change-1",
            project_id="project-1",
            from_snapshot_id="snapshot-1",
            to_snapshot_id="snapshot-2",
            artifact_path="src/main.py",
            change_type=ChangeType.MODIFIED,
            recorded_at=RECORDED_AT,
        )

        restored = ProjectChange.from_dict(change.to_dict())

        self.assertEqual(restored, change)

    def test_change_supports_initial_snapshot(self) -> None:
        change = ProjectChange(
            id="change-1",
            project_id="project-1",
            from_snapshot_id=None,
            to_snapshot_id="snapshot-1",
            artifact_path="README.md",
            change_type=ChangeType.ADDED,
            recorded_at=RECORDED_AT,
        )

        self.assertIsNone(change.from_snapshot_id)

    def test_change_rejects_same_snapshot_pair(self) -> None:
        with self.assertRaisesRegex(ValueError, "must differ"):
            ProjectChange(
                id="change-1",
                project_id="project-1",
                from_snapshot_id="snapshot-1",
                to_snapshot_id="snapshot-1",
                artifact_path="README.md",
                change_type=ChangeType.UNKNOWN,
                recorded_at=RECORDED_AT,
            )


class ProjectHistoryEventTests(unittest.TestCase):
    def test_event_round_trip_serialization(self) -> None:
        event = ProjectHistoryEvent(
            id="event-1",
            project_id="project-1",
            event_type=HistoryEventType.CHANGES_RECORDED,
            occurred_at=RECORDED_AT,
            snapshot_id="snapshot-2",
            change_ids=("change-1", "change-2"),
            description="Recorded declared changes",
        )

        restored = ProjectHistoryEvent.from_dict(event.to_dict())

        self.assertEqual(restored, event)

    def test_event_rejects_duplicate_change_references(self) -> None:
        with self.assertRaisesRegex(ValueError, "unique"):
            ProjectHistoryEvent(
                id="event-1",
                project_id="project-1",
                event_type=HistoryEventType.CHANGES_RECORDED,
                occurred_at=RECORDED_AT,
                change_ids=("change-1", "change-1"),
            )

    def test_history_enums_convert_from_serialized_values(self) -> None:
        self.assertIs(ChangeType("REMOVED"), ChangeType.REMOVED)
        self.assertIs(
            HistoryEventType("SNAPSHOT_CAPTURED"),
            HistoryEventType.SNAPSHOT_CAPTURED,
        )


if __name__ == "__main__":
    unittest.main()
