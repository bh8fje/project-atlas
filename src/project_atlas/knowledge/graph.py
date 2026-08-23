"""Construction of deterministic explicit project relationship graphs."""

from collections.abc import Iterable
from datetime import datetime, timezone

from project_atlas.domain import (
    Project,
    ProjectRelationship,
    ProjectRelationshipGraph,
)


class ProjectRelationshipGraphBuilder:
    """Build an in-memory graph from explicitly supplied nodes and edges."""

    def build(
        self,
        projects: Iterable[Project],
        relationships: Iterable[ProjectRelationship],
        *,
        generated_at: datetime | None = None,
    ) -> ProjectRelationshipGraph:
        """Validate, sort, and return an immutable relationship graph."""

        project_values = self._materialize(projects, Project, "projects")
        relationship_values = self._materialize(
            relationships, ProjectRelationship, "relationships"
        )
        timestamp = generated_at or datetime.now(timezone.utc)
        if not isinstance(timestamp, datetime):
            raise TypeError("generated_at must be a datetime")
        if timestamp.tzinfo is None or timestamp.utcoffset() is None:
            raise ValueError("generated_at must include timezone information")
        return ProjectRelationshipGraph(
            generated_at=timestamp,
            projects=tuple(sorted(project_values, key=lambda project: project.id)),
            relationships=tuple(
                sorted(
                    relationship_values,
                    key=lambda relationship: (
                        relationship.source_project_id,
                        relationship.target_project_id,
                        relationship.relationship_type.value,
                    ),
                )
            ),
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
