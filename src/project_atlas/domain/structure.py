"""Project structure analysis result contract."""

from collections.abc import Mapping
from dataclasses import dataclass
from datetime import datetime
from typing import Any, Self

from ._validation import parse_datetime, require_aware_datetime, require_non_empty
from .asset import AssetRelationship, ProjectArtifact
from .enums import ArtifactType


@dataclass(frozen=True, slots=True)
class ProjectStructure:
    """A point-in-time, in-memory description of project composition."""

    project_id: str
    root_path: str
    analyzed_at: datetime
    artifacts: tuple[ProjectArtifact, ...]
    relationships: tuple[AssetRelationship, ...]
    technologies: tuple[str, ...]

    def __post_init__(self) -> None:
        require_non_empty(self.project_id, "project_id")
        require_non_empty(self.root_path, "root_path")
        require_aware_datetime(self.analyzed_at, "analyzed_at")
        if not isinstance(self.artifacts, tuple) or any(
            not isinstance(artifact, ProjectArtifact) for artifact in self.artifacts
        ):
            raise TypeError("artifacts must be a tuple of ProjectArtifact values")
        if not isinstance(self.relationships, tuple) or any(
            not isinstance(relationship, AssetRelationship)
            for relationship in self.relationships
        ):
            raise TypeError(
                "relationships must be a tuple of AssetRelationship values"
            )
        if not isinstance(self.technologies, tuple) or any(
            not isinstance(technology, str) or not technology
            for technology in self.technologies
        ):
            raise TypeError("technologies must be a tuple of non-empty strings")
        if tuple(sorted(set(self.technologies))) != self.technologies:
            raise ValueError("technologies must be sorted and unique")

        artifact_ids = [artifact.id for artifact in self.artifacts]
        if len(set(artifact_ids)) != len(artifact_ids):
            raise ValueError("artifact ids must be unique")
        known_source_ids = {self.project_id, *artifact_ids}
        known_target_ids = set(artifact_ids)
        for relationship in self.relationships:
            if relationship.source_id not in known_source_ids:
                raise ValueError("relationship source must reference this structure")
            if relationship.target_id not in known_target_ids:
                raise ValueError("relationship target must reference an artifact")

    @property
    def artifact_count(self) -> int:
        """Return the number of described artifacts."""

        return len(self.artifacts)

    def artifact_type_counts(self) -> dict[str, int]:
        """Return JSON-compatible artifact counts grouped by type."""

        counts = {artifact_type.value: 0 for artifact_type in ArtifactType}
        for artifact in self.artifacts:
            counts[artifact.artifact_type.value] += 1
        return counts

    def to_dict(self) -> dict[str, Any]:
        """Return a JSON-compatible representation of the structure."""

        return {
            "project_id": self.project_id,
            "root_path": self.root_path,
            "analyzed_at": self.analyzed_at.isoformat(),
            "artifacts": [artifact.to_dict() for artifact in self.artifacts],
            "relationships": [
                relationship.to_dict() for relationship in self.relationships
            ],
            "technologies": list(self.technologies),
            "artifact_type_counts": self.artifact_type_counts(),
        }

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> Self:
        """Create a validated structure from serialized data."""

        raw_artifacts = data.get("artifacts")
        raw_relationships = data.get("relationships")
        raw_technologies = data.get("technologies")
        if not isinstance(raw_artifacts, list):
            raise TypeError("artifacts must be a list")
        if not isinstance(raw_relationships, list):
            raise TypeError("relationships must be a list")
        if not isinstance(raw_technologies, list):
            raise TypeError("technologies must be a list")

        return cls(
            project_id=require_non_empty(data.get("project_id"), "project_id"),
            root_path=require_non_empty(data.get("root_path"), "root_path"),
            analyzed_at=parse_datetime(data.get("analyzed_at"), "analyzed_at"),
            artifacts=tuple(ProjectArtifact.from_dict(item) for item in raw_artifacts),
            relationships=tuple(
                AssetRelationship.from_dict(item) for item in raw_relationships
            ),
            technologies=tuple(
                require_non_empty(item, "technology") for item in raw_technologies
            ),
        )
