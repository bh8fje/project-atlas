"""Immutable cross-project relationship graph contracts."""

from collections.abc import Mapping
from dataclasses import dataclass
from datetime import datetime
from typing import Any, Self

from ._validation import parse_datetime, require_aware_datetime, require_non_empty
from .enums import ProjectRelationshipType
from .project import Project


@dataclass(frozen=True, slots=True)
class ProjectRelationship:
    """A directed, explicitly declared relationship between projects."""

    source_project_id: str
    target_project_id: str
    relationship_type: ProjectRelationshipType

    def __post_init__(self) -> None:
        require_non_empty(self.source_project_id, "source_project_id")
        require_non_empty(self.target_project_id, "target_project_id")
        if self.source_project_id == self.target_project_id:
            raise ValueError("project relationship cannot reference itself")
        if not isinstance(self.relationship_type, ProjectRelationshipType):
            raise TypeError(
                "relationship_type must be a ProjectRelationshipType"
            )

    def to_dict(self) -> dict[str, str]:
        """Return a JSON-compatible relationship representation."""

        return {
            "source_project_id": self.source_project_id,
            "target_project_id": self.target_project_id,
            "relationship_type": self.relationship_type.value,
        }

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> Self:
        """Create a validated relationship from serialized data."""

        return cls(
            source_project_id=require_non_empty(
                data.get("source_project_id"), "source_project_id"
            ),
            target_project_id=require_non_empty(
                data.get("target_project_id"), "target_project_id"
            ),
            relationship_type=ProjectRelationshipType(
                require_non_empty(
                    data.get("relationship_type"), "relationship_type"
                )
            ),
        )


@dataclass(frozen=True, slots=True)
class ProjectRelationshipGraph:
    """A deterministic in-memory graph of projects and directed edges."""

    generated_at: datetime
    projects: tuple[Project, ...]
    relationships: tuple[ProjectRelationship, ...]

    def __post_init__(self) -> None:
        require_aware_datetime(self.generated_at, "generated_at")
        if not isinstance(self.projects, tuple) or any(
            not isinstance(project, Project) for project in self.projects
        ):
            raise TypeError("projects must be a tuple of Project values")
        if not isinstance(self.relationships, tuple) or any(
            not isinstance(relationship, ProjectRelationship)
            for relationship in self.relationships
        ):
            raise TypeError(
                "relationships must be a tuple of ProjectRelationship values"
            )
        project_ids = [project.id for project in self.projects]
        if len(set(project_ids)) != len(project_ids):
            raise ValueError("project ids must be unique")
        ordered_projects = tuple(
            sorted(self.projects, key=lambda project: project.id)
        )
        if ordered_projects != self.projects:
            raise ValueError("projects must be ordered by id")
        relationship_keys = [
            self._relationship_key(item) for item in self.relationships
        ]
        if len(set(relationship_keys)) != len(relationship_keys):
            raise ValueError("project relationships must be unique")
        ordered_relationships = tuple(
            sorted(self.relationships, key=self._relationship_key)
        )
        if ordered_relationships != self.relationships:
            raise ValueError("project relationships must be deterministically ordered")
        known_project_ids = set(project_ids)
        if any(
            relationship.source_project_id not in known_project_ids
            or relationship.target_project_id not in known_project_ids
            for relationship in self.relationships
        ):
            raise ValueError("project relationships must reference graph projects")

    @property
    def project_count(self) -> int:
        """Return the number of project nodes."""

        return len(self.projects)

    @property
    def relationship_count(self) -> int:
        """Return the number of directed relationships."""

        return len(self.relationships)

    def outgoing(self, project_id: str) -> tuple[ProjectRelationship, ...]:
        """Return relationships originating from one graph project."""

        self._require_project(project_id)
        return tuple(
            relationship
            for relationship in self.relationships
            if relationship.source_project_id == project_id
        )

    def incoming(self, project_id: str) -> tuple[ProjectRelationship, ...]:
        """Return relationships targeting one graph project."""

        self._require_project(project_id)
        return tuple(
            relationship
            for relationship in self.relationships
            if relationship.target_project_id == project_id
        )

    def to_dict(self) -> dict[str, Any]:
        """Return a JSON-compatible graph representation."""

        return {
            "generated_at": self.generated_at.isoformat(),
            "projects": [project.to_dict() for project in self.projects],
            "relationships": [
                relationship.to_dict() for relationship in self.relationships
            ],
            "project_count": self.project_count,
            "relationship_count": self.relationship_count,
        }

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> Self:
        """Create a validated graph from serialized data."""

        raw_projects = data.get("projects")
        raw_relationships = data.get("relationships")
        if not isinstance(raw_projects, list):
            raise TypeError("projects must be a list")
        if not isinstance(raw_relationships, list):
            raise TypeError("relationships must be a list")
        return cls(
            generated_at=parse_datetime(data.get("generated_at"), "generated_at"),
            projects=tuple(Project.from_dict(item) for item in raw_projects),
            relationships=tuple(
                ProjectRelationship.from_dict(item) for item in raw_relationships
            ),
        )

    def _require_project(self, project_id: str) -> None:
        require_non_empty(project_id, "project_id")
        if all(project.id != project_id for project in self.projects):
            raise ValueError("project_id must reference a graph project")

    @staticmethod
    def _relationship_key(
        relationship: ProjectRelationship,
    ) -> tuple[str, str, str]:
        return (
            relationship.source_project_id,
            relationship.target_project_id,
            relationship.relationship_type.value,
        )
