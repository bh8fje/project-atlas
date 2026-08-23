"""Project asset domain model."""

from collections.abc import Mapping
from dataclasses import dataclass
from datetime import datetime
from typing import Any, Self

from ._validation import parse_datetime, require_aware_datetime, require_non_empty
from .enums import ProjectStatus


@dataclass(frozen=True, slots=True)
class Project:
    """A locally addressable software project asset."""

    id: str
    name: str
    path: str
    created_at: datetime
    updated_at: datetime
    status: ProjectStatus

    def __post_init__(self) -> None:
        require_non_empty(self.id, "id")
        require_non_empty(self.name, "name")
        require_non_empty(self.path, "path")
        require_aware_datetime(self.created_at, "created_at")
        require_aware_datetime(self.updated_at, "updated_at")
        if not isinstance(self.status, ProjectStatus):
            raise TypeError("status must be a ProjectStatus")
        if self.updated_at < self.created_at:
            raise ValueError("updated_at must not be earlier than created_at")

    def to_dict(self) -> dict[str, str]:
        """Return a JSON-compatible representation of the project."""

        return {
            "id": self.id,
            "name": self.name,
            "path": self.path,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "status": self.status.value,
        }

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> Self:
        """Create a validated project from its serialized representation."""

        return cls(
            id=require_non_empty(data.get("id"), "id"),
            name=require_non_empty(data.get("name"), "name"),
            path=require_non_empty(data.get("path"), "path"),
            created_at=parse_datetime(data.get("created_at"), "created_at"),
            updated_at=parse_datetime(data.get("updated_at"), "updated_at"),
            status=ProjectStatus(require_non_empty(data.get("status"), "status")),
        )
