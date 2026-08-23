"""Project history contracts without capture, detection, or persistence behavior."""

from collections.abc import Mapping
from dataclasses import dataclass
from datetime import datetime
from typing import Any, Self

from ._validation import parse_datetime, require_aware_datetime, require_non_empty
from .enums import ChangeType, HistoryEventType
from .fingerprint import ProjectFingerprint


@dataclass(frozen=True, slots=True)
class ProjectSnapshot:
    """An immutable project fingerprint recorded at one point in time."""

    id: str
    project_id: str
    fingerprint: ProjectFingerprint
    created_at: datetime

    def __post_init__(self) -> None:
        require_non_empty(self.id, "id")
        require_non_empty(self.project_id, "project_id")
        if not isinstance(self.fingerprint, ProjectFingerprint):
            raise TypeError("fingerprint must be a ProjectFingerprint")
        require_aware_datetime(self.created_at, "created_at")
        if self.fingerprint.project_id != self.project_id:
            raise ValueError("fingerprint project_id must match snapshot project_id")
        if self.fingerprint.generated_at > self.created_at:
            raise ValueError("fingerprint must not be generated after the snapshot")

    @property
    def artifact_count(self) -> int:
        """Return the artifact count captured by the fingerprint."""

        return self.fingerprint.artifact_count

    def to_dict(self) -> dict[str, Any]:
        """Return a JSON-compatible snapshot representation."""

        return {
            "id": self.id,
            "project_id": self.project_id,
            "fingerprint": self.fingerprint.to_dict(),
            "created_at": self.created_at.isoformat(),
            "artifact_count": self.artifact_count,
        }

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> Self:
        """Create a validated snapshot from serialized data."""

        raw_fingerprint = data.get("fingerprint")
        if not isinstance(raw_fingerprint, Mapping):
            raise TypeError("fingerprint must be a mapping")
        return cls(
            id=require_non_empty(data.get("id"), "id"),
            project_id=require_non_empty(data.get("project_id"), "project_id"),
            fingerprint=ProjectFingerprint.from_dict(raw_fingerprint),
            created_at=parse_datetime(data.get("created_at"), "created_at"),
        )


@dataclass(frozen=True, slots=True)
class ProjectChange:
    """A declared artifact change between two project snapshots."""

    id: str
    project_id: str
    from_snapshot_id: str | None
    to_snapshot_id: str
    artifact_path: str
    change_type: ChangeType
    recorded_at: datetime

    def __post_init__(self) -> None:
        require_non_empty(self.id, "id")
        require_non_empty(self.project_id, "project_id")
        if self.from_snapshot_id is not None:
            require_non_empty(self.from_snapshot_id, "from_snapshot_id")
        require_non_empty(self.to_snapshot_id, "to_snapshot_id")
        require_non_empty(self.artifact_path, "artifact_path")
        if not isinstance(self.change_type, ChangeType):
            raise TypeError("change_type must be a ChangeType")
        require_aware_datetime(self.recorded_at, "recorded_at")
        if self.from_snapshot_id == self.to_snapshot_id:
            raise ValueError("from_snapshot_id and to_snapshot_id must differ")

    def to_dict(self) -> dict[str, str | None]:
        """Return a JSON-compatible change representation."""

        return {
            "id": self.id,
            "project_id": self.project_id,
            "from_snapshot_id": self.from_snapshot_id,
            "to_snapshot_id": self.to_snapshot_id,
            "artifact_path": self.artifact_path,
            "change_type": self.change_type.value,
            "recorded_at": self.recorded_at.isoformat(),
        }

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> Self:
        """Create a validated change from serialized data."""

        raw_from_snapshot_id = data.get("from_snapshot_id")
        if raw_from_snapshot_id is not None:
            raw_from_snapshot_id = require_non_empty(
                raw_from_snapshot_id, "from_snapshot_id"
            )
        try:
            change_type = ChangeType(data.get("change_type"))
        except ValueError as error:
            raise ValueError("change_type must be a valid ChangeType") from error
        return cls(
            id=require_non_empty(data.get("id"), "id"),
            project_id=require_non_empty(data.get("project_id"), "project_id"),
            from_snapshot_id=raw_from_snapshot_id,
            to_snapshot_id=require_non_empty(
                data.get("to_snapshot_id"), "to_snapshot_id"
            ),
            artifact_path=require_non_empty(
                data.get("artifact_path"), "artifact_path"
            ),
            change_type=change_type,
            recorded_at=parse_datetime(data.get("recorded_at"), "recorded_at"),
        )


@dataclass(frozen=True, slots=True)
class ProjectHistoryEvent:
    """A timestamped fact referencing snapshots or declared changes."""

    id: str
    project_id: str
    event_type: HistoryEventType
    occurred_at: datetime
    snapshot_id: str | None = None
    change_ids: tuple[str, ...] = ()
    description: str | None = None

    def __post_init__(self) -> None:
        require_non_empty(self.id, "id")
        require_non_empty(self.project_id, "project_id")
        if not isinstance(self.event_type, HistoryEventType):
            raise TypeError("event_type must be a HistoryEventType")
        require_aware_datetime(self.occurred_at, "occurred_at")
        if self.snapshot_id is not None:
            require_non_empty(self.snapshot_id, "snapshot_id")
        if not isinstance(self.change_ids, tuple) or any(
            not isinstance(change_id, str) or not change_id.strip()
            for change_id in self.change_ids
        ):
            raise TypeError("change_ids must be a tuple of non-empty strings")
        if len(set(self.change_ids)) != len(self.change_ids):
            raise ValueError("change_ids must be unique")
        if self.description is not None:
            require_non_empty(self.description, "description")

    def to_dict(self) -> dict[str, Any]:
        """Return a JSON-compatible event representation."""

        return {
            "id": self.id,
            "project_id": self.project_id,
            "event_type": self.event_type.value,
            "occurred_at": self.occurred_at.isoformat(),
            "snapshot_id": self.snapshot_id,
            "change_ids": list(self.change_ids),
            "description": self.description,
        }

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> Self:
        """Create a validated event from serialized data."""

        raw_change_ids = data.get("change_ids")
        if not isinstance(raw_change_ids, list):
            raise TypeError("change_ids must be a list")
        raw_snapshot_id = data.get("snapshot_id")
        if raw_snapshot_id is not None:
            raw_snapshot_id = require_non_empty(raw_snapshot_id, "snapshot_id")
        raw_description = data.get("description")
        if raw_description is not None:
            raw_description = require_non_empty(raw_description, "description")
        try:
            event_type = HistoryEventType(data.get("event_type"))
        except ValueError as error:
            raise ValueError("event_type must be a valid HistoryEventType") from error
        return cls(
            id=require_non_empty(data.get("id"), "id"),
            project_id=require_non_empty(data.get("project_id"), "project_id"),
            event_type=event_type,
            occurred_at=parse_datetime(data.get("occurred_at"), "occurred_at"),
            snapshot_id=raw_snapshot_id,
            change_ids=tuple(
                require_non_empty(change_id, "change_id")
                for change_id in raw_change_ids
            ),
            description=raw_description,
        )
