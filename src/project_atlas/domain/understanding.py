"""Structured AI project-understanding result contract."""

from collections.abc import Mapping
from dataclasses import dataclass
from datetime import datetime
from typing import Any, Self

from ._validation import parse_datetime, require_aware_datetime, require_non_empty


@dataclass(frozen=True, slots=True)
class ProjectUnderstanding:
    """A provider-attributed, source-traceable project analysis."""

    project_id: str
    purpose: str
    architecture: tuple[str, ...]
    risks: tuple[str, ...]
    status: str
    analyzed_at: datetime
    source_record_keys: tuple[str, ...]
    provider_name: str
    model_name: str

    def __post_init__(self) -> None:
        require_non_empty(self.project_id, "project_id")
        require_non_empty(self.purpose, "purpose")
        self._require_string_tuple(self.architecture, "architecture")
        self._require_string_tuple(self.risks, "risks")
        require_non_empty(self.status, "status")
        require_aware_datetime(self.analyzed_at, "analyzed_at")
        self._require_string_tuple(self.source_record_keys, "source_record_keys")
        if len(set(self.source_record_keys)) != len(self.source_record_keys):
            raise ValueError("source_record_keys must be unique")
        require_non_empty(self.provider_name, "provider_name")
        require_non_empty(self.model_name, "model_name")

    def to_dict(self) -> dict[str, Any]:
        """Return a JSON-compatible understanding representation."""

        return {
            "project_id": self.project_id,
            "purpose": self.purpose,
            "architecture": list(self.architecture),
            "risks": list(self.risks),
            "status": self.status,
            "analyzed_at": self.analyzed_at.isoformat(),
            "source_record_keys": list(self.source_record_keys),
            "provider_name": self.provider_name,
            "model_name": self.model_name,
        }

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> Self:
        """Create a validated understanding from serialized data."""

        architecture = cls._string_list(data.get("architecture"), "architecture")
        risks = cls._string_list(data.get("risks"), "risks")
        source_keys = cls._string_list(
            data.get("source_record_keys"), "source_record_keys"
        )
        return cls(
            project_id=require_non_empty(data.get("project_id"), "project_id"),
            purpose=require_non_empty(data.get("purpose"), "purpose"),
            architecture=architecture,
            risks=risks,
            status=require_non_empty(data.get("status"), "status"),
            analyzed_at=parse_datetime(data.get("analyzed_at"), "analyzed_at"),
            source_record_keys=source_keys,
            provider_name=require_non_empty(
                data.get("provider_name"), "provider_name"
            ),
            model_name=require_non_empty(data.get("model_name"), "model_name"),
        )

    @staticmethod
    def _require_string_tuple(value: object, field_name: str) -> None:
        if not isinstance(value, tuple) or any(
            not isinstance(item, str) or not item.strip() for item in value
        ):
            raise TypeError(f"{field_name} must be a tuple of non-empty strings")

    @staticmethod
    def _string_list(value: object, field_name: str) -> tuple[str, ...]:
        if not isinstance(value, list):
            raise TypeError(f"{field_name} must be a list")
        if any(not isinstance(item, str) or not item.strip() for item in value):
            raise TypeError(f"{field_name} must contain non-empty strings")
        return tuple(value)
