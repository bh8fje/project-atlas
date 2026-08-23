"""Bounded AI context contract with traceable knowledge sources."""

from collections.abc import Mapping
from dataclasses import dataclass
from datetime import datetime
from typing import Any, Self

from ._validation import parse_datetime, require_aware_datetime, require_non_empty


@dataclass(frozen=True, slots=True)
class AIContext:
    """A local, prepared context payload suitable for an AI provider."""

    project_id: str
    generated_at: datetime
    content: str
    source_record_keys: tuple[str, ...]
    truncated: bool

    def __post_init__(self) -> None:
        require_non_empty(self.project_id, "project_id")
        require_aware_datetime(self.generated_at, "generated_at")
        require_non_empty(self.content, "content")
        if not isinstance(self.source_record_keys, tuple) or any(
            not isinstance(key, str) or not key.strip()
            for key in self.source_record_keys
        ):
            raise TypeError(
                "source_record_keys must be a tuple of non-empty strings"
            )
        if len(set(self.source_record_keys)) != len(self.source_record_keys):
            raise ValueError("source_record_keys must be unique")
        if not isinstance(self.truncated, bool):
            raise TypeError("truncated must be a boolean")

    @property
    def character_count(self) -> int:
        """Return the number of characters in the prepared context."""

        return len(self.content)

    def to_dict(self) -> dict[str, Any]:
        """Return a JSON-compatible context representation."""

        return {
            "project_id": self.project_id,
            "generated_at": self.generated_at.isoformat(),
            "content": self.content,
            "source_record_keys": list(self.source_record_keys),
            "truncated": self.truncated,
            "character_count": self.character_count,
        }

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> Self:
        """Create a validated context from serialized data."""

        raw_source_keys = data.get("source_record_keys")
        if not isinstance(raw_source_keys, list):
            raise TypeError("source_record_keys must be a list")
        raw_truncated = data.get("truncated")
        if not isinstance(raw_truncated, bool):
            raise TypeError("truncated must be a boolean")
        return cls(
            project_id=require_non_empty(data.get("project_id"), "project_id"),
            generated_at=parse_datetime(data.get("generated_at"), "generated_at"),
            content=require_non_empty(data.get("content"), "content"),
            source_record_keys=tuple(
                require_non_empty(key, "source_record_key")
                for key in raw_source_keys
            ),
            truncated=raw_truncated,
        )
