"""Structured AI project-assistant answer contract."""

from collections.abc import Mapping
from dataclasses import dataclass
from datetime import datetime
from typing import Any, Self

from ._validation import parse_datetime, require_aware_datetime, require_non_empty


@dataclass(frozen=True, slots=True)
class ProjectAssistantAnswer:
    """A provider-attributed, source-traceable answer about one project."""

    project_id: str
    question: str
    answer: str
    recommendations: tuple[str, ...]
    cautions: tuple[str, ...]
    answered_at: datetime
    source_record_keys: tuple[str, ...]
    provider_name: str
    model_name: str

    def __post_init__(self) -> None:
        require_non_empty(self.project_id, "project_id")
        require_non_empty(self.question, "question")
        require_non_empty(self.answer, "answer")
        self._require_string_tuple(self.recommendations, "recommendations")
        self._require_string_tuple(self.cautions, "cautions")
        require_aware_datetime(self.answered_at, "answered_at")
        self._require_string_tuple(self.source_record_keys, "source_record_keys")
        if len(set(self.source_record_keys)) != len(self.source_record_keys):
            raise ValueError("source_record_keys must be unique")
        require_non_empty(self.provider_name, "provider_name")
        require_non_empty(self.model_name, "model_name")

    def to_dict(self) -> dict[str, Any]:
        """Return a JSON-compatible answer representation."""

        return {
            "project_id": self.project_id,
            "question": self.question,
            "answer": self.answer,
            "recommendations": list(self.recommendations),
            "cautions": list(self.cautions),
            "answered_at": self.answered_at.isoformat(),
            "source_record_keys": list(self.source_record_keys),
            "provider_name": self.provider_name,
            "model_name": self.model_name,
        }

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> Self:
        """Create a validated answer from serialized data."""

        return cls(
            project_id=require_non_empty(data.get("project_id"), "project_id"),
            question=require_non_empty(data.get("question"), "question"),
            answer=require_non_empty(data.get("answer"), "answer"),
            recommendations=cls._string_list(
                data.get("recommendations"), "recommendations"
            ),
            cautions=cls._string_list(data.get("cautions"), "cautions"),
            answered_at=parse_datetime(data.get("answered_at"), "answered_at"),
            source_record_keys=cls._string_list(
                data.get("source_record_keys"), "source_record_keys"
            ),
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
