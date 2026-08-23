"""Transactional SQLite storage for local knowledge records."""

from datetime import datetime
from pathlib import Path
import sqlite3

from project_atlas.domain import KnowledgeRecord, KnowledgeRecordType


SCHEMA_VERSION = 1


class KnowledgeRecordConflictError(ValueError):
    """Raised when a record key exists and replacement was not requested."""


class KnowledgeSchemaError(RuntimeError):
    """Raised when a database schema version is not supported."""


class LocalKnowledgeStore:
    """An explicit-path, local-only SQLite knowledge record store."""

    def __init__(self, path: str | Path) -> None:
        if not isinstance(path, (str, Path)):
            raise TypeError("path must be a string or Path")
        if isinstance(path, str) and not path.strip():
            raise ValueError("path must not be empty")
        resolved_path = Path(path).expanduser().resolve()
        if resolved_path.exists() and resolved_path.is_dir():
            raise ValueError("knowledge store path must be a file")
        resolved_path.parent.mkdir(parents=True, exist_ok=True)
        self._path = resolved_path
        self._connection = sqlite3.connect(str(resolved_path))
        self._connection.row_factory = sqlite3.Row
        try:
            self._initialize_schema()
        except Exception:
            self._connection.close()
            raise

    @property
    def path(self) -> Path:
        """Return the resolved local database path."""

        return self._path

    def save(self, record: KnowledgeRecord, *, replace: bool = False) -> None:
        """Persist a record, requiring explicit permission to replace a key."""

        if not isinstance(record, KnowledgeRecord):
            raise TypeError("record must be a KnowledgeRecord")
        if not isinstance(replace, bool):
            raise TypeError("replace must be a boolean")
        values = (
            record.record_type.value,
            record.id,
            record.project_id,
            record.recorded_at.isoformat(),
            record.data_json,
        )
        statement = (
            "INSERT INTO knowledge_records "
            "(record_type, record_id, project_id, recorded_at, data_json) "
            "VALUES (?, ?, ?, ?, ?)"
        )
        if replace:
            statement += (
                " ON CONFLICT(record_type, record_id) DO UPDATE SET "
                "project_id=excluded.project_id, "
                "recorded_at=excluded.recorded_at, data_json=excluded.data_json"
            )
        try:
            with self._connection:
                self._connection.execute(statement, values)
        except sqlite3.IntegrityError as error:
            raise KnowledgeRecordConflictError(
                "knowledge record already exists; use replace=True explicitly"
            ) from error

    def get(
        self, record_type: KnowledgeRecordType, record_id: str
    ) -> KnowledgeRecord | None:
        """Return one record by typed key, or None when it does not exist."""

        self._require_record_type(record_type)
        self._require_non_empty(record_id, "record_id")
        row = self._connection.execute(
            "SELECT record_type, record_id, project_id, recorded_at, data_json "
            "FROM knowledge_records WHERE record_type = ? AND record_id = ?",
            (record_type.value, record_id),
        ).fetchone()
        return None if row is None else self._to_record(row)

    def list_records(
        self,
        *,
        record_type: KnowledgeRecordType | None = None,
        project_id: str | None = None,
    ) -> tuple[KnowledgeRecord, ...]:
        """List records using optional exact metadata filters."""

        clauses: list[str] = []
        parameters: list[str] = []
        if record_type is not None:
            self._require_record_type(record_type)
            clauses.append("record_type = ?")
            parameters.append(record_type.value)
        if project_id is not None:
            self._require_non_empty(project_id, "project_id")
            clauses.append("project_id = ?")
            parameters.append(project_id)
        statement = (
            "SELECT record_type, record_id, project_id, recorded_at, data_json "
            "FROM knowledge_records"
        )
        if clauses:
            statement += " WHERE " + " AND ".join(clauses)
        statement += " ORDER BY recorded_at, record_type, record_id"
        rows = self._connection.execute(statement, parameters).fetchall()
        return tuple(self._to_record(row) for row in rows)

    def close(self) -> None:
        """Close the local database connection."""

        self._connection.close()

    def __enter__(self) -> "LocalKnowledgeStore":
        return self

    def __exit__(self, exc_type: object, exc_value: object, traceback: object) -> None:
        self.close()

    def _initialize_schema(self) -> None:
        with self._connection:
            self._connection.execute(
                "CREATE TABLE IF NOT EXISTS schema_metadata ("
                "singleton INTEGER PRIMARY KEY CHECK (singleton = 1), "
                "version INTEGER NOT NULL)"
            )
            row = self._connection.execute(
                "SELECT version FROM schema_metadata WHERE singleton = 1"
            ).fetchone()
            if row is None:
                self._connection.execute(
                    "INSERT INTO schema_metadata (singleton, version) VALUES (1, ?)",
                    (SCHEMA_VERSION,),
                )
            elif row["version"] != SCHEMA_VERSION:
                raise KnowledgeSchemaError(
                    f"unsupported knowledge schema version: {row['version']}"
                )
            self._connection.execute(
                "CREATE TABLE IF NOT EXISTS knowledge_records ("
                "record_type TEXT NOT NULL, record_id TEXT NOT NULL, "
                "project_id TEXT, recorded_at TEXT NOT NULL, data_json TEXT NOT NULL, "
                "PRIMARY KEY (record_type, record_id))"
            )
            self._connection.execute(
                "CREATE INDEX IF NOT EXISTS idx_knowledge_project "
                "ON knowledge_records (project_id, recorded_at)"
            )

    @staticmethod
    def _to_record(row: sqlite3.Row) -> KnowledgeRecord:
        return KnowledgeRecord(
            id=row["record_id"],
            record_type=KnowledgeRecordType(row["record_type"]),
            project_id=row["project_id"],
            recorded_at=datetime.fromisoformat(row["recorded_at"]),
            data_json=row["data_json"],
        )

    @staticmethod
    def _require_record_type(record_type: KnowledgeRecordType) -> None:
        if not isinstance(record_type, KnowledgeRecordType):
            raise TypeError("record_type must be a KnowledgeRecordType")

    @staticmethod
    def _require_non_empty(value: object, name: str) -> None:
        if not isinstance(value, str):
            raise TypeError(f"{name} must be a string")
        if not value.strip():
            raise ValueError(f"{name} must not be empty")
