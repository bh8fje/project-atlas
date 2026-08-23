"""Project artifact and asset relationship domain models."""

from collections.abc import Mapping
from dataclasses import dataclass
from datetime import datetime
from typing import Any, Self

from ._validation import parse_datetime, require_aware_datetime, require_non_empty
from .enums import ArtifactType, RelationshipType


@dataclass(frozen=True, slots=True)
class ProjectArtifact:
    """A typed asset located within a software project."""

    id: str
    name: str
    path: str
    artifact_type: ArtifactType
    created_at: datetime
    updated_at: datetime

    def __post_init__(self) -> None:
        require_non_empty(self.id, "id")
        require_non_empty(self.name, "name")
        require_non_empty(self.path, "path")
        if not isinstance(self.artifact_type, ArtifactType):
            raise TypeError("artifact_type must be an ArtifactType")
        require_aware_datetime(self.created_at, "created_at")
        require_aware_datetime(self.updated_at, "updated_at")
        if self.updated_at < self.created_at:
            raise ValueError("updated_at must not be earlier than created_at")

    def to_dict(self) -> dict[str, str]:
        """Return a JSON-compatible representation of the artifact."""

        return {
            "id": self.id,
            "name": self.name,
            "path": self.path,
            "artifact_type": self.artifact_type.value,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> Self:
        """Create a validated artifact from serialized data."""

        return cls(
            id=require_non_empty(data.get("id"), "id"),
            name=require_non_empty(data.get("name"), "name"),
            path=require_non_empty(data.get("path"), "path"),
            artifact_type=ArtifactType(
                require_non_empty(data.get("artifact_type"), "artifact_type")
            ),
            created_at=parse_datetime(data.get("created_at"), "created_at"),
            updated_at=parse_datetime(data.get("updated_at"), "updated_at"),
        )


@dataclass(frozen=True, slots=True)
class AssetRelationship:
    """A directed semantic relationship between two project assets."""

    source_id: str
    target_id: str
    relationship_type: RelationshipType

    def __post_init__(self) -> None:
        require_non_empty(self.source_id, "source_id")
        require_non_empty(self.target_id, "target_id")
        if self.source_id == self.target_id:
            raise ValueError("source_id and target_id must be different")
        if not isinstance(self.relationship_type, RelationshipType):
            raise TypeError("relationship_type must be a RelationshipType")

    def to_dict(self) -> dict[str, str]:
        """Return a JSON-compatible representation of the relationship."""

        return {
            "source_id": self.source_id,
            "target_id": self.target_id,
            "relationship_type": self.relationship_type.value,
        }

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> Self:
        """Create a validated relationship from serialized data."""

        return cls(
            source_id=require_non_empty(data.get("source_id"), "source_id"),
            target_id=require_non_empty(data.get("target_id"), "target_id"),
            relationship_type=RelationshipType(
                require_non_empty(
                    data.get("relationship_type"), "relationship_type"
                )
            ),
        )
