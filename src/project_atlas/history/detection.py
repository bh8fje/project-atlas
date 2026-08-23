"""Deterministic change detection between explicit project structures."""

from datetime import datetime, timezone
from pathlib import Path
from uuid import NAMESPACE_URL, uuid5

from project_atlas.domain import (
    ChangeType,
    ProjectArtifact,
    ProjectChange,
    ProjectStructure,
)


class ChangeDetectionEngine:
    """Compare two in-memory structures without scanning or persistence."""

    def detect(
        self,
        before: ProjectStructure | None,
        after: ProjectStructure,
        *,
        from_snapshot_id: str | None,
        to_snapshot_id: str,
        recorded_at: datetime | None = None,
    ) -> tuple[ProjectChange, ...]:
        """Return path-sorted additions, removals, and modifications."""

        if before is not None and not isinstance(before, ProjectStructure):
            raise TypeError("before must be a ProjectStructure or None")
        if not isinstance(after, ProjectStructure):
            raise TypeError("after must be a ProjectStructure")
        if before is None and from_snapshot_id is not None:
            raise ValueError("from_snapshot_id must be None for an initial structure")
        if before is not None and (
            not isinstance(from_snapshot_id, str) or not from_snapshot_id.strip()
        ):
            raise ValueError("from_snapshot_id is required when before is provided")
        if not isinstance(to_snapshot_id, str):
            raise TypeError("to_snapshot_id must be a string")
        if not to_snapshot_id.strip():
            raise ValueError("to_snapshot_id must not be empty")
        timestamp = recorded_at or datetime.now(timezone.utc)
        if not isinstance(timestamp, datetime):
            raise TypeError("recorded_at must be a datetime")
        if timestamp.tzinfo is None or timestamp.utcoffset() is None:
            raise ValueError("recorded_at must include timezone information")
        if before is not None:
            if before.project_id != after.project_id:
                raise ValueError("structures must belong to the same project")
            if before.analyzed_at > after.analyzed_at:
                raise ValueError("before must not be analyzed after after")

        before_by_path = self._artifacts_by_relative_path(before)
        after_by_path = self._artifacts_by_relative_path(after)
        changes: list[ProjectChange] = []

        for path in sorted(before_by_path.keys() | after_by_path.keys()):
            previous = before_by_path.get(path)
            current = after_by_path.get(path)
            change_type = self._change_type(previous, current)
            if change_type is None:
                continue
            changes.append(
                ProjectChange(
                    id=self._change_id(
                        project_id=after.project_id,
                        from_snapshot_id=from_snapshot_id,
                        to_snapshot_id=to_snapshot_id,
                        artifact_path=path,
                        change_type=change_type,
                    ),
                    project_id=after.project_id,
                    from_snapshot_id=from_snapshot_id,
                    to_snapshot_id=to_snapshot_id,
                    artifact_path=path,
                    change_type=change_type,
                    recorded_at=timestamp,
                )
            )

        return tuple(changes)

    @staticmethod
    def _artifacts_by_relative_path(
        structure: ProjectStructure | None,
    ) -> dict[str, ProjectArtifact]:
        if structure is None:
            return {}
        root = Path(structure.root_path)
        artifacts: dict[str, ProjectArtifact] = {}
        for artifact in structure.artifacts:
            path = Path(artifact.path)
            try:
                relative = path.relative_to(root)
            except ValueError as error:
                raise ValueError(
                    "artifact path must be contained by its structure root"
                ) from error
            if ".." in relative.parts:
                raise ValueError(
                    "artifact path must be contained by its structure root"
                )
            relative_path = relative.as_posix() or "."
            if relative_path in artifacts:
                raise ValueError("artifact paths must be unique within a structure")
            artifacts[relative_path] = artifact
        return artifacts

    @staticmethod
    def _change_type(
        before: ProjectArtifact | None,
        after: ProjectArtifact | None,
    ) -> ChangeType | None:
        if before is None:
            return ChangeType.ADDED
        if after is None:
            return ChangeType.REMOVED
        before_state = (
            before.name,
            before.artifact_type,
            before.created_at,
            before.updated_at,
        )
        after_state = (
            after.name,
            after.artifact_type,
            after.created_at,
            after.updated_at,
        )
        if before_state != after_state:
            return ChangeType.MODIFIED
        return None

    @staticmethod
    def _change_id(
        *,
        project_id: str,
        from_snapshot_id: str | None,
        to_snapshot_id: str,
        artifact_path: str,
        change_type: ChangeType,
    ) -> str:
        identity = "\n".join(
            (
                project_id,
                from_snapshot_id or "",
                to_snapshot_id,
                artifact_path,
                change_type.value,
            )
        )
        return str(uuid5(NAMESPACE_URL, identity))
