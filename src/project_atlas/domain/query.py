"""Knowledge query and result contracts."""

from collections.abc import Mapping
from dataclasses import dataclass
from datetime import datetime
from typing import Any, Self

from ._validation import (
    parse_datetime,
    require_aware_datetime,
    require_non_empty,
    require_non_negative_int,
)
from .enums import KnowledgeRecordType
from .knowledge import KnowledgeRecord


@dataclass(frozen=True, slots=True)
class KnowledgeQuery:
    """Structured filters with optional local text-search input."""

    record_types: tuple[KnowledgeRecordType, ...] = ()
    project_id: str | None = None
    text: str | None = None
    recorded_from: datetime | None = None
    recorded_to: datetime | None = None
    limit: int = 100

    def __post_init__(self) -> None:
        if not isinstance(self.record_types, tuple) or any(
            not isinstance(record_type, KnowledgeRecordType)
            for record_type in self.record_types
        ):
            raise TypeError(
                "record_types must be a tuple of KnowledgeRecordType values"
            )
        if len(set(self.record_types)) != len(self.record_types):
            raise ValueError("record_types must be unique")
        if self.project_id is not None:
            require_non_empty(self.project_id, "project_id")
        if self.text is not None:
            require_non_empty(self.text, "text")
        if self.recorded_from is not None:
            require_aware_datetime(self.recorded_from, "recorded_from")
        if self.recorded_to is not None:
            require_aware_datetime(self.recorded_to, "recorded_to")
        if (
            self.recorded_from is not None
            and self.recorded_to is not None
            and self.recorded_from > self.recorded_to
        ):
            raise ValueError("recorded_from must not be after recorded_to")
        require_non_negative_int(self.limit, "limit")
        if self.limit < 1 or self.limit > 1_000:
            raise ValueError("limit must be between 1 and 1000")

    def to_dict(self) -> dict[str, Any]:
        """Return a JSON-compatible query representation."""

        return {
            "record_types": [record_type.value for record_type in self.record_types],
            "project_id": self.project_id,
            "text": self.text,
            "recorded_from": (
                None
                if self.recorded_from is None
                else self.recorded_from.isoformat()
            ),
            "recorded_to": (
                None if self.recorded_to is None else self.recorded_to.isoformat()
            ),
            "limit": self.limit,
        }

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> Self:
        """Create a validated query from serialized data."""

        raw_record_types = data.get("record_types")
        if not isinstance(raw_record_types, list):
            raise TypeError("record_types must be a list")
        return cls(
            record_types=tuple(
                KnowledgeRecordType(require_non_empty(item, "record_type"))
                for item in raw_record_types
            ),
            project_id=(
                None
                if data.get("project_id") is None
                else require_non_empty(data.get("project_id"), "project_id")
            ),
            text=(
                None
                if data.get("text") is None
                else require_non_empty(data.get("text"), "text")
            ),
            recorded_from=cls._optional_datetime(
                data.get("recorded_from"), "recorded_from"
            ),
            recorded_to=cls._optional_datetime(
                data.get("recorded_to"), "recorded_to"
            ),
            limit=require_non_negative_int(data.get("limit"), "limit"),
        )

    @staticmethod
    def _optional_datetime(value: object, field_name: str) -> datetime | None:
        return None if value is None else parse_datetime(value, field_name)


@dataclass(frozen=True, slots=True)
class KnowledgeQueryResult:
    """An immutable page of matching knowledge records."""

    query: KnowledgeQuery
    records: tuple[KnowledgeRecord, ...]
    total_matches: int
    executed_at: datetime

    def __post_init__(self) -> None:
        if not isinstance(self.query, KnowledgeQuery):
            raise TypeError("query must be a KnowledgeQuery")
        if not isinstance(self.records, tuple) or any(
            not isinstance(record, KnowledgeRecord) for record in self.records
        ):
            raise TypeError("records must be a tuple of KnowledgeRecord values")
        require_non_negative_int(self.total_matches, "total_matches")
        if len(self.records) > self.total_matches:
            raise ValueError("records must not exceed total_matches")
        if len(self.records) > self.query.limit:
            raise ValueError("records must not exceed the query limit")
        require_aware_datetime(self.executed_at, "executed_at")

    def to_dict(self) -> dict[str, Any]:
        """Return a JSON-compatible query result representation."""

        return {
            "query": self.query.to_dict(),
            "records": [record.to_dict() for record in self.records],
            "total_matches": self.total_matches,
            "executed_at": self.executed_at.isoformat(),
        }

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> Self:
        """Create a validated result from serialized data."""

        raw_query = data.get("query")
        raw_records = data.get("records")
        if not isinstance(raw_query, Mapping):
            raise TypeError("query must be a mapping")
        if not isinstance(raw_records, list):
            raise TypeError("records must be a list")
        return cls(
            query=KnowledgeQuery.from_dict(raw_query),
            records=tuple(KnowledgeRecord.from_dict(item) for item in raw_records),
            total_matches=require_non_negative_int(
                data.get("total_matches"), "total_matches"
            ),
            executed_at=parse_datetime(data.get("executed_at"), "executed_at"),
        )
