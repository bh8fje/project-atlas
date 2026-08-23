"""Version-neutral local knowledge record contract."""

from collections.abc import Mapping
from dataclasses import dataclass
from datetime import datetime
import json
from typing import Any, Self

from ._validation import parse_datetime, require_aware_datetime, require_non_empty
from .enums import KnowledgeRecordType


@dataclass(frozen=True, slots=True)
class KnowledgeRecord:
    """An immutable, typed envelope around canonical JSON knowledge data."""

    id: str
    record_type: KnowledgeRecordType
    data_json: str
    recorded_at: datetime
    project_id: str | None = None

    def __post_init__(self) -> None:
        require_non_empty(self.id, "id")
        if not isinstance(self.record_type, KnowledgeRecordType):
            raise TypeError("record_type must be a KnowledgeRecordType")
        require_non_empty(self.data_json, "data_json")
        require_aware_datetime(self.recorded_at, "recorded_at")
        if self.project_id is not None:
            require_non_empty(self.project_id, "project_id")
        payload = self._parse_payload(self.data_json)
        canonical = self._canonical_json(payload)
        if canonical != self.data_json:
            raise ValueError("data_json must use canonical JSON encoding")

    @property
    def payload(self) -> dict[str, Any]:
        """Return a detached JSON-compatible payload dictionary."""

        return self._parse_payload(self.data_json)

    def to_dict(self) -> dict[str, Any]:
        """Return a JSON-compatible record representation."""

        return {
            "id": self.id,
            "record_type": self.record_type.value,
            "project_id": self.project_id,
            "recorded_at": self.recorded_at.isoformat(),
            "payload": self.payload,
        }

    @classmethod
    def from_payload(
        cls,
        *,
        id: str,
        record_type: KnowledgeRecordType,
        payload: Mapping[str, Any],
        recorded_at: datetime,
        project_id: str | None = None,
    ) -> Self:
        """Create a record from a mapping using canonical JSON encoding."""

        if not isinstance(payload, Mapping):
            raise TypeError("payload must be a mapping")
        return cls(
            id=id,
            record_type=record_type,
            data_json=cls._canonical_json(dict(payload)),
            recorded_at=recorded_at,
            project_id=project_id,
        )

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> Self:
        """Create a validated record from serialized data."""

        raw_payload = data.get("payload")
        if not isinstance(raw_payload, Mapping):
            raise TypeError("payload must be a mapping")
        return cls.from_payload(
            id=require_non_empty(data.get("id"), "id"),
            record_type=KnowledgeRecordType(
                require_non_empty(data.get("record_type"), "record_type")
            ),
            project_id=(
                None
                if data.get("project_id") is None
                else require_non_empty(data.get("project_id"), "project_id")
            ),
            recorded_at=parse_datetime(data.get("recorded_at"), "recorded_at"),
            payload=raw_payload,
        )

    @staticmethod
    def _canonical_json(payload: dict[str, Any]) -> str:
        try:
            return json.dumps(
                payload,
                ensure_ascii=False,
                allow_nan=False,
                separators=(",", ":"),
                sort_keys=True,
            )
        except (TypeError, ValueError) as error:
            raise ValueError(
                "payload must contain only JSON-compatible values"
            ) from error

    @staticmethod
    def _parse_payload(data_json: str) -> dict[str, Any]:
        try:
            payload = json.loads(data_json)
        except (TypeError, json.JSONDecodeError) as error:
            raise ValueError("data_json must contain valid JSON") from error
        if not isinstance(payload, dict):
            raise ValueError("data_json must contain a JSON object")
        return payload
