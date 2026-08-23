"""Deterministic multi-project intelligence contracts."""

from collections.abc import Mapping
from dataclasses import dataclass
from datetime import datetime
from typing import Any, Self

from ._validation import parse_datetime, require_aware_datetime, require_non_empty, require_non_negative_int
from .enums import ProjectStatus


@dataclass(frozen=True, slots=True)
class ProjectIntelligenceSummary:
    project_id: str
    name: str
    project_status: ProjectStatus
    understanding_status: str
    risk_count: int
    relationship_count: int
    analyzed_at: datetime

    def __post_init__(self) -> None:
        require_non_empty(self.project_id, "project_id")
        require_non_empty(self.name, "name")
        if not isinstance(self.project_status, ProjectStatus):
            raise TypeError("project_status must be a ProjectStatus")
        require_non_empty(self.understanding_status, "understanding_status")
        require_non_negative_int(self.risk_count, "risk_count")
        require_non_negative_int(self.relationship_count, "relationship_count")
        require_aware_datetime(self.analyzed_at, "analyzed_at")

    def to_dict(self) -> dict[str, Any]:
        return {"project_id": self.project_id, "name": self.name, "project_status": self.project_status.value, "understanding_status": self.understanding_status, "risk_count": self.risk_count, "relationship_count": self.relationship_count, "analyzed_at": self.analyzed_at.isoformat()}

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> Self:
        return cls(
            project_id=require_non_empty(data.get("project_id"), "project_id"),
            name=require_non_empty(data.get("name"), "name"),
            project_status=ProjectStatus(require_non_empty(data.get("project_status"), "project_status")),
            understanding_status=require_non_empty(data.get("understanding_status"), "understanding_status"),
            risk_count=require_non_negative_int(data.get("risk_count"), "risk_count"),
            relationship_count=require_non_negative_int(data.get("relationship_count"), "relationship_count"),
            analyzed_at=parse_datetime(data.get("analyzed_at"), "analyzed_at"),
        )


@dataclass(frozen=True, slots=True)
class MultiProjectIntelligence:
    generated_at: datetime
    projects: tuple[ProjectIntelligenceSummary, ...]
    shared_risks: tuple[str, ...]
    isolated_project_ids: tuple[str, ...]
    relationship_count: int
    source_record_keys: tuple[str, ...]

    def __post_init__(self) -> None:
        require_aware_datetime(self.generated_at, "generated_at")
        if len(self.projects) < 2 or any(not isinstance(item, ProjectIntelligenceSummary) for item in self.projects):
            raise ValueError("projects must contain at least two summaries")
        project_ids = tuple(item.project_id for item in self.projects)
        if project_ids != tuple(sorted(project_ids)) or len(project_ids) != len(set(project_ids)):
            raise ValueError("projects must have unique ids ordered by project_id")
        self._ordered_unique_strings(self.shared_risks, "shared_risks")
        self._ordered_unique_strings(self.isolated_project_ids, "isolated_project_ids")
        if not set(self.isolated_project_ids).issubset(project_ids):
            raise ValueError("isolated_project_ids must reference projects")
        require_non_negative_int(self.relationship_count, "relationship_count")
        self._ordered_unique_strings(self.source_record_keys, "source_record_keys")

    @property
    def project_count(self) -> int:
        return len(self.projects)

    def to_dict(self) -> dict[str, Any]:
        return {"generated_at": self.generated_at.isoformat(), "projects": [item.to_dict() for item in self.projects], "project_count": self.project_count, "shared_risks": list(self.shared_risks), "isolated_project_ids": list(self.isolated_project_ids), "relationship_count": self.relationship_count, "source_record_keys": list(self.source_record_keys)}

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> Self:
        raw_projects = data.get("projects")
        if not isinstance(raw_projects, list):
            raise TypeError("projects must be a list")
        return cls(
            generated_at=parse_datetime(data.get("generated_at"), "generated_at"),
            projects=tuple(ProjectIntelligenceSummary.from_dict(item) for item in raw_projects),
            shared_risks=cls._string_list(data.get("shared_risks"), "shared_risks"),
            isolated_project_ids=cls._string_list(data.get("isolated_project_ids"), "isolated_project_ids"),
            relationship_count=require_non_negative_int(data.get("relationship_count"), "relationship_count"),
            source_record_keys=cls._string_list(data.get("source_record_keys"), "source_record_keys"),
        )

    @staticmethod
    def _ordered_unique_strings(value: object, field_name: str) -> None:
        if not isinstance(value, tuple) or any(not isinstance(item, str) or not item.strip() for item in value):
            raise TypeError(f"{field_name} must be a tuple of non-empty strings")
        if value != tuple(sorted(set(value))):
            raise ValueError(f"{field_name} must be unique and ordered")

    @staticmethod
    def _string_list(value: object, field_name: str) -> tuple[str, ...]:
        if not isinstance(value, list):
            raise TypeError(f"{field_name} must be a list")
        return tuple(value)
