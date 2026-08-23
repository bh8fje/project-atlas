"""Local construction of bounded and key-redacted AI context."""

from collections.abc import Iterable, Mapping
from datetime import datetime, timezone
import json
import re
from typing import Any

from project_atlas.domain import AIContext, KnowledgeRecord


REDACTION_MARKER = "[REDACTED]"
TRUNCATION_MARKER = "\n[TRUNCATED]"
SENSITIVE_KEY_SUFFIXES = frozenset(
    {
        "apikey",
        "authorization",
        "credential",
        "password",
        "privatekey",
        "secret",
        "token",
    }
)


class AIContextBuilder:
    """Prepare local knowledge for AI use without invoking a provider."""

    def build(
        self,
        project_id: str,
        records: Iterable[KnowledgeRecord],
        *,
        max_characters: int = 20_000,
        generated_at: datetime | None = None,
    ) -> AIContext:
        """Build deterministic context with key-based secret redaction."""

        if not isinstance(project_id, str):
            raise TypeError("project_id must be a string")
        if not project_id.strip():
            raise ValueError("project_id must not be empty")
        if isinstance(max_characters, bool) or not isinstance(max_characters, int):
            raise TypeError("max_characters must be an integer")
        if max_characters < 256 or max_characters > 1_000_000:
            raise ValueError("max_characters must be between 256 and 1000000")
        timestamp = generated_at or datetime.now(timezone.utc)
        if not isinstance(timestamp, datetime):
            raise TypeError("generated_at must be a datetime")
        if timestamp.tzinfo is None or timestamp.utcoffset() is None:
            raise ValueError("generated_at must include timezone information")
        record_values = self._materialize(records)
        if any(
            record.project_id not in (None, project_id) for record in record_values
        ):
            raise ValueError("records must be global or belong to the context project")
        ordered_records = tuple(
            sorted(
                record_values,
                key=lambda record: (
                    record.recorded_at,
                    record.record_type.value,
                    record.id,
                ),
            )
        )

        content = f"Project ID: {project_id}\nKnowledge records:"
        source_keys: list[str] = []
        truncated = False
        for record in ordered_records:
            line = "\n" + self._record_line(record)
            if len(content) + len(line) <= max_characters:
                content += line
                source_keys.append(f"{record.record_type.value}:{record.id}")
                continue
            available = max_characters - len(content) - len(TRUNCATION_MARKER)
            if available > 0:
                content += line[:available]
                source_keys.append(f"{record.record_type.value}:{record.id}")
            content += TRUNCATION_MARKER
            truncated = True
            break

        return AIContext(
            project_id=project_id,
            generated_at=timestamp,
            content=content,
            source_record_keys=tuple(source_keys),
            truncated=truncated,
        )

    @staticmethod
    def _materialize(records: Iterable[KnowledgeRecord]) -> tuple[KnowledgeRecord, ...]:
        if isinstance(records, (str, bytes)):
            raise TypeError("records must be an iterable of KnowledgeRecord values")
        try:
            record_values = tuple(records)
        except TypeError as error:
            raise TypeError(
                "records must be an iterable of KnowledgeRecord values"
            ) from error
        if any(not isinstance(record, KnowledgeRecord) for record in record_values):
            raise TypeError("records must contain only KnowledgeRecord values")
        return record_values

    @classmethod
    def _record_line(cls, record: KnowledgeRecord) -> str:
        prepared = {
            "id": record.id,
            "record_type": record.record_type.value,
            "project_id": record.project_id,
            "recorded_at": record.recorded_at.isoformat(),
            "payload": cls._redact(record.payload),
        }
        return json.dumps(
            prepared,
            ensure_ascii=False,
            allow_nan=False,
            separators=(",", ":"),
            sort_keys=True,
        )

    @classmethod
    def _redact(cls, value: Any) -> Any:
        if isinstance(value, Mapping):
            return {
                key: (
                    REDACTION_MARKER
                    if cls._is_sensitive_key(key)
                    else cls._redact(item)
                )
                for key, item in value.items()
            }
        if isinstance(value, list):
            return [cls._redact(item) for item in value]
        return value

    @staticmethod
    def _is_sensitive_key(key: object) -> bool:
        if not isinstance(key, str):
            return False
        normalized = re.sub(r"[^a-z0-9]", "", key.casefold())
        return any(
            normalized == suffix or normalized.endswith(suffix)
            for suffix in SENSITIVE_KEY_SUFFIXES
        )
