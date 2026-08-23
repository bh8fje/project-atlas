"""Tests for validated project timeline generation."""

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
    ProjectTimeline,
)
from project_atlas.history import ProjectTimelineBuilder  # noqa: E402


BASE_AT = datetime(2026, 8, 23, 16, 0, tzinfo=timezone.utc)


def make_snapshot(snapshot_id: str, minute: int) -> ProjectSnapshot:
    created_at = BASE_AT + timedelta(minutes=minute)
    fingerprint = ProjectFingerprint(
        project_id="project-1",
        stable_project_id="12345678-1234-5678-1234-567812345678",
        algorithm="sha256-metadata-v1",
        digest=f"{minute:x}".rjust(64, "0"),
        generated_at=created_at,
        artifact_count=minute + 1,
    )
    return ProjectSnapshot(
        id=snapshot_id,
        project_id="project-1",
        fingerprint=fingerprint,
        created_at=created_at,
    )


def make_change() -> ProjectChange:
    return ProjectChange(
        id="change-1",
        project_id="project-1",
        from_snapshot_id="snapshot-1",
        to_snapshot_id="snapshot-2",
        artifact_path="src/main.py",
        change_type=ChangeType.MODIFIED,
        recorded_at=BASE_AT + timedelta(minutes=2),
    )


def make_event(
    event_id: str,
    minute: int,
    *,
    snapshot_id: str | None = None,
    change_ids: tuple[str, ...] = (),
) -> ProjectHistoryEvent:
    return ProjectHistoryEvent(
        id=event_id,
        project_id="project-1",
        event_type=(
            HistoryEventType.CHANGES_RECORDED
            if change_ids
            else HistoryEventType.SNAPSHOT_CAPTURED
        ),
        occurred_at=BASE_AT + timedelta(minutes=minute),
        snapshot_id=snapshot_id,
        change_ids=change_ids,
    )


class ProjectTimelineBuilderTests(unittest.TestCase):
    def test_builds_chronological_timeline_with_stable_tie_break(self) -> None:
        snapshots = (make_snapshot("snapshot-1", 0), make_snapshot("snapshot-2", 2))
        events = (
            make_event("event-z", 2, snapshot_id="snapshot-2"),
            make_event("event-a", 2, change_ids=("change-1",)),
            make_event("event-first", 0, snapshot_id="snapshot-1"),
        )

        timeline = ProjectTimelineBuilder().build(
            "project-1",
            snapshots=snapshots,
            changes=(make_change(),),
            events=events,
            generated_at=BASE_AT + timedelta(minutes=3),
        )

        self.assertEqual(
            [event.id for event in timeline.events],
            ["event-first", "event-a", "event-z"],
        )
        self.assertEqual(timeline.event_count, 3)

    def test_timeline_round_trip_serialization(self) -> None:
        timeline = ProjectTimelineBuilder().build(
            "project-1",
            snapshots=(make_snapshot("snapshot-1", 0),),
            changes=(),
            events=(make_event("event-1", 0, snapshot_id="snapshot-1"),),
            generated_at=BASE_AT,
        )

        restored = ProjectTimeline.from_dict(timeline.to_dict())

        self.assertEqual(restored, timeline)

    def test_rejects_missing_event_references(self) -> None:
        builder = ProjectTimelineBuilder()

        with self.assertRaisesRegex(ValueError, "event snapshot"):
            builder.build(
                "project-1",
                snapshots=(),
                changes=(),
                events=(make_event("event-1", 0, snapshot_id="missing"),),
                generated_at=BASE_AT,
            )
        with self.assertRaisesRegex(ValueError, "event changes"):
            builder.build(
                "project-1",
                snapshots=(),
                changes=(),
                events=(make_event("event-1", 0, change_ids=("missing",)),),
                generated_at=BASE_AT,
            )

    def test_rejects_change_with_missing_snapshot(self) -> None:
        with self.assertRaisesRegex(ValueError, "target snapshot"):
            ProjectTimelineBuilder().build(
                "project-1",
                snapshots=(make_snapshot("snapshot-1", 0),),
                changes=(make_change(),),
                events=(),
                generated_at=BASE_AT + timedelta(minutes=3),
            )

    def test_rejects_duplicate_history_ids(self) -> None:
        snapshot = make_snapshot("snapshot-1", 0)

        with self.assertRaisesRegex(ValueError, "snapshot ids"):
            ProjectTimelineBuilder().build(
                "project-1",
                snapshots=(snapshot, snapshot),
                changes=(),
                events=(),
                generated_at=BASE_AT,
            )

    def test_rejects_generation_before_latest_event(self) -> None:
        with self.assertRaisesRegex(ValueError, "must not precede"):
            ProjectTimelineBuilder().build(
                "project-1",
                snapshots=(),
                changes=(),
                events=(make_event("event-1", 2),),
                generated_at=BASE_AT,
            )


if __name__ == "__main__":
    unittest.main()
