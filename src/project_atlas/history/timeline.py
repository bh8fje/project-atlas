"""Validated in-memory project timeline construction."""

from collections.abc import Iterable
from datetime import datetime, timezone

from project_atlas.domain import (
    ProjectChange,
    ProjectHistoryEvent,
    ProjectSnapshot,
    ProjectTimeline,
)


class ProjectTimelineBuilder:
    """Order project events after validating their history references."""

    def build(
        self,
        project_id: str,
        *,
        snapshots: Iterable[ProjectSnapshot],
        changes: Iterable[ProjectChange],
        events: Iterable[ProjectHistoryEvent],
        generated_at: datetime | None = None,
    ) -> ProjectTimeline:
        """Build a deterministic timeline from explicit in-memory history."""

        if not isinstance(project_id, str):
            raise TypeError("project_id must be a string")
        if not project_id.strip():
            raise ValueError("project_id must not be empty")
        snapshot_values = self._materialize(
            snapshots, ProjectSnapshot, "snapshots"
        )
        change_values = self._materialize(changes, ProjectChange, "changes")
        event_values = self._materialize(
            events, ProjectHistoryEvent, "events"
        )
        timestamp = generated_at or datetime.now(timezone.utc)
        if not isinstance(timestamp, datetime):
            raise TypeError("generated_at must be a datetime")
        if timestamp.tzinfo is None or timestamp.utcoffset() is None:
            raise ValueError("generated_at must include timezone information")

        self._require_project(project_id, snapshot_values, "snapshots")
        self._require_project(project_id, change_values, "changes")
        self._require_project(project_id, event_values, "events")
        snapshots_by_id = self._by_unique_id(snapshot_values, "snapshot")
        changes_by_id = self._by_unique_id(change_values, "change")
        self._validate_changes(change_values, snapshots_by_id)
        self._validate_events(event_values, snapshots_by_id, changes_by_id)

        ordered_events = tuple(
            sorted(event_values, key=lambda event: (event.occurred_at, event.id))
        )
        return ProjectTimeline(
            project_id=project_id,
            generated_at=timestamp,
            events=ordered_events,
        )

    @staticmethod
    def _materialize(values: Iterable[object], expected_type: type, name: str) -> tuple:
        if isinstance(values, (str, bytes)):
            raise TypeError(f"{name} must be an iterable of {expected_type.__name__}")
        try:
            materialized = tuple(values)
        except TypeError as error:
            raise TypeError(
                f"{name} must be an iterable of {expected_type.__name__}"
            ) from error
        if any(not isinstance(value, expected_type) for value in materialized):
            raise TypeError(f"{name} must contain only {expected_type.__name__}")
        return materialized

    @staticmethod
    def _require_project(project_id: str, values: tuple, name: str) -> None:
        if any(value.project_id != project_id for value in values):
            raise ValueError(f"{name} must belong to the requested project")

    @staticmethod
    def _by_unique_id(values: tuple, name: str) -> dict[str, object]:
        indexed: dict[str, object] = {}
        for value in values:
            if value.id in indexed:
                raise ValueError(f"{name} ids must be unique")
            indexed[value.id] = value
        return indexed

    @staticmethod
    def _validate_changes(
        changes: tuple[ProjectChange, ...],
        snapshots_by_id: dict[str, object],
    ) -> None:
        for change in changes:
            if change.to_snapshot_id not in snapshots_by_id:
                raise ValueError("change target snapshot must exist")
            if (
                change.from_snapshot_id is not None
                and change.from_snapshot_id not in snapshots_by_id
            ):
                raise ValueError("change source snapshot must exist")

    @staticmethod
    def _validate_events(
        events: tuple[ProjectHistoryEvent, ...],
        snapshots_by_id: dict[str, object],
        changes_by_id: dict[str, object],
    ) -> None:
        for event in events:
            if (
                event.snapshot_id is not None
                and event.snapshot_id not in snapshots_by_id
            ):
                raise ValueError("event snapshot must exist")
            if any(change_id not in changes_by_id for change_id in event.change_ids):
                raise ValueError("event changes must exist")
