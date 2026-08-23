"""Read-only structured and local text queries over knowledge records."""

from collections.abc import Iterable
from datetime import datetime, timezone
import re

from project_atlas.domain import (
    KnowledgeQuery,
    KnowledgeQueryResult,
    KnowledgeRecord,
    KnowledgeRecordType,
)

from .storage import LocalKnowledgeStore


class KnowledgeQueryEngine:
    """Execute deterministic read-only queries against a local store."""

    def __init__(self, store: LocalKnowledgeStore) -> None:
        if not isinstance(store, LocalKnowledgeStore):
            raise TypeError("store must be a LocalKnowledgeStore")
        self._store = store

    def query(
        self,
        query: KnowledgeQuery,
        *,
        executed_at: datetime | None = None,
    ) -> KnowledgeQueryResult:
        """Apply structured filters and optional all-term text matching."""

        if not isinstance(query, KnowledgeQuery):
            raise TypeError("query must be a KnowledgeQuery")
        timestamp = executed_at or datetime.now(timezone.utc)
        if not isinstance(timestamp, datetime):
            raise TypeError("executed_at must be a datetime")
        if timestamp.tzinfo is None or timestamp.utcoffset() is None:
            raise ValueError("executed_at must include timezone information")
        terms = self._terms(query.text)
        records = self._store.list_records(project_id=query.project_id)
        matches = tuple(
            record
            for record in records
            if self._matches(record, query=query, terms=terms)
        )
        return KnowledgeQueryResult(
            query=query,
            records=matches[: query.limit],
            total_matches=len(matches),
            executed_at=timestamp,
        )

    def search(
        self,
        text: str,
        *,
        record_types: Iterable[KnowledgeRecordType] = (),
        project_id: str | None = None,
        limit: int = 100,
        executed_at: datetime | None = None,
    ) -> KnowledgeQueryResult:
        """Run a convenient local keyword query without semantic inference."""

        if isinstance(record_types, (str, bytes)):
            raise TypeError("record_types must contain KnowledgeRecordType values")
        try:
            type_values = tuple(record_types)
        except TypeError as error:
            raise TypeError(
                "record_types must contain KnowledgeRecordType values"
            ) from error
        query = KnowledgeQuery(
            record_types=type_values,
            project_id=project_id,
            text=text,
            limit=limit,
        )
        return self.query(query, executed_at=executed_at)

    @staticmethod
    def _terms(text: str | None) -> tuple[str, ...]:
        if text is None:
            return ()
        terms = tuple(re.findall(r"\w+", text.casefold(), flags=re.UNICODE))
        if not terms:
            raise ValueError("text must contain at least one searchable term")
        return terms

    @staticmethod
    def _matches(
        record: KnowledgeRecord,
        *,
        query: KnowledgeQuery,
        terms: tuple[str, ...],
    ) -> bool:
        if query.record_types and record.record_type not in query.record_types:
            return False
        if (
            query.recorded_from is not None
            and record.recorded_at < query.recorded_from
        ):
            return False
        if query.recorded_to is not None and record.recorded_at > query.recorded_to:
            return False
        haystack = "\n".join(
            (
                record.id,
                record.record_type.value,
                record.project_id or "",
                record.data_json,
            )
        ).casefold()
        return all(term in haystack for term in terms)
