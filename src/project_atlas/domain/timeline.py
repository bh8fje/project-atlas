"""Immutable project timeline contract."""

from collections.abc import Mapping
from dataclasses import dataclass
from datetime import datetime
from typing import Any, Self

from ._validation import parse_datetime, require_aware_datetime, require_non_empty
from .history import ProjectHistoryEvent


@dataclass(frozen=True, slots=True)
class ProjectTimeline:
    """A chronologically ordered sequence of validated project events."""

    project_id: str
    generated_at: datetime
    events: tuple[ProjectHistoryEvent, ...]

    def __post_init__(self) -> None:
        require_non_empty(self.project_id, "project_id")
        require_aware_datetime(self.generated_at, "generated_at")
        if not isinstance(self.events, tuple) or any(
            not isinstance(event, ProjectHistoryEvent) for event in self.events
        ):
            raise TypeError("events must be a tuple of ProjectHistoryEvent values")
        if any(event.project_id != self.project_id for event in self.events):
            raise ValueError("events must belong to the timeline project")
        event_ids = [event.id for event in self.events]
        if len(set(event_ids)) != len(event_ids):
            raise ValueError("event ids must be unique")
        ordered_events = tuple(
            sorted(self.events, key=lambda event: (event.occurred_at, event.id))
        )
        if ordered_events != self.events:
            raise ValueError("events must be ordered by occurred_at and id")
        if self.events and self.events[-1].occurred_at > self.generated_at:
            raise ValueError("generated_at must not precede timeline events")

    @property
    def event_count(self) -> int:
        """Return the number of events in the timeline."""

        return len(self.events)

    def to_dict(self) -> dict[str, Any]:
        """Return a JSON-compatible timeline representation."""

        return {
            "project_id": self.project_id,
            "generated_at": self.generated_at.isoformat(),
            "events": [event.to_dict() for event in self.events],
            "event_count": self.event_count,
        }

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> Self:
        """Create a validated timeline from serialized data."""

        raw_events = data.get("events")
        if not isinstance(raw_events, list):
            raise TypeError("events must be a list")
        return cls(
            project_id=require_non_empty(data.get("project_id"), "project_id"),
            generated_at=parse_datetime(data.get("generated_at"), "generated_at"),
            events=tuple(ProjectHistoryEvent.from_dict(item) for item in raw_events),
        )
