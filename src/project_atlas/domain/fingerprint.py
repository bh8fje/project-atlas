"""Stable project identity and structure fingerprint contract."""

from collections.abc import Mapping
from dataclasses import dataclass
from datetime import datetime
from string import hexdigits
from typing import Any, Self
from uuid import UUID

from ._validation import (
    parse_datetime,
    require_aware_datetime,
    require_non_empty,
    require_non_negative_int,
)


@dataclass(frozen=True, slots=True)
class ProjectFingerprint:
    """A versioned metadata digest for one stable local project identity."""

    project_id: str
    stable_project_id: str
    algorithm: str
    digest: str
    generated_at: datetime
    artifact_count: int

    def __post_init__(self) -> None:
        require_non_empty(self.project_id, "project_id")
        require_non_empty(self.stable_project_id, "stable_project_id")
        try:
            UUID(self.stable_project_id)
        except ValueError as error:
            raise ValueError("stable_project_id must be a UUID") from error
        require_non_empty(self.algorithm, "algorithm")
        require_non_empty(self.digest, "digest")
        if len(self.digest) != 64 or any(character not in hexdigits for character in self.digest):
            raise ValueError("digest must be a 64-character hexadecimal value")
        require_aware_datetime(self.generated_at, "generated_at")
        require_non_negative_int(self.artifact_count, "artifact_count")

    def matches(self, other: object) -> bool:
        """Return whether another fingerprint represents the same project state."""

        return (
            isinstance(other, ProjectFingerprint)
            and self.stable_project_id == other.stable_project_id
            and self.algorithm == other.algorithm
            and self.digest == other.digest
        )

    def to_dict(self) -> dict[str, str | int]:
        """Return a JSON-compatible fingerprint representation."""

        return {
            "project_id": self.project_id,
            "stable_project_id": self.stable_project_id,
            "algorithm": self.algorithm,
            "digest": self.digest,
            "generated_at": self.generated_at.isoformat(),
            "artifact_count": self.artifact_count,
        }

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> Self:
        """Create a validated fingerprint from serialized data."""

        return cls(
            project_id=require_non_empty(data.get("project_id"), "project_id"),
            stable_project_id=require_non_empty(
                data.get("stable_project_id"), "stable_project_id"
            ),
            algorithm=require_non_empty(data.get("algorithm"), "algorithm"),
            digest=require_non_empty(data.get("digest"), "digest"),
            generated_at=parse_datetime(data.get("generated_at"), "generated_at"),
            artifact_count=require_non_negative_int(
                data.get("artifact_count"), "artifact_count"
            ),
        )
