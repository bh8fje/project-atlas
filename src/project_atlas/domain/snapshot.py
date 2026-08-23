"""Point-in-time repository snapshot domain model."""

from collections.abc import Mapping
from dataclasses import dataclass
from datetime import datetime
from typing import Any, Self

from ._validation import (
    parse_datetime,
    require_aware_datetime,
    require_non_empty,
    require_non_negative_int,
)


@dataclass(frozen=True, slots=True)
class RepositorySnapshot:
    """A repository summary recorded at one point in time."""

    id: str
    repository_id: str
    created_at: datetime
    artifact_count: int

    def __post_init__(self) -> None:
        require_non_empty(self.id, "id")
        require_non_empty(self.repository_id, "repository_id")
        require_aware_datetime(self.created_at, "created_at")
        require_non_negative_int(self.artifact_count, "artifact_count")

    def to_dict(self) -> dict[str, str | int]:
        """Return a JSON-compatible representation of the snapshot."""

        return {
            "id": self.id,
            "repository_id": self.repository_id,
            "created_at": self.created_at.isoformat(),
            "artifact_count": self.artifact_count,
        }

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> Self:
        """Create a validated snapshot from serialized data."""

        return cls(
            id=require_non_empty(data.get("id"), "id"),
            repository_id=require_non_empty(
                data.get("repository_id"), "repository_id"
            ),
            created_at=parse_datetime(data.get("created_at"), "created_at"),
            artifact_count=require_non_negative_int(
                data.get("artifact_count"), "artifact_count"
            ),
        )
