"""Tests for local transactional knowledge storage."""

from datetime import datetime, timedelta, timezone
from pathlib import Path
import sqlite3
import sys
from tempfile import TemporaryDirectory
import unittest


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from project_atlas.domain import KnowledgeRecord, KnowledgeRecordType  # noqa: E402
from project_atlas.knowledge import (  # noqa: E402
    KnowledgeRecordConflictError,
    KnowledgeSchemaError,
    LocalKnowledgeStore,
)


RECORDED_AT = datetime(2026, 8, 23, 18, 0, tzinfo=timezone.utc)


def make_record(
    record_id: str,
    *,
    record_type: KnowledgeRecordType = KnowledgeRecordType.PROJECT,
    project_id: str | None = "project-1",
    minute: int = 0,
    name: str = "Atlas",
) -> KnowledgeRecord:
    return KnowledgeRecord.from_payload(
        id=record_id,
        record_type=record_type,
        project_id=project_id,
        recorded_at=RECORDED_AT + timedelta(minutes=minute),
        payload={"name": name, "nested": {"enabled": True}},
    )


class KnowledgeRecordTests(unittest.TestCase):
    def test_record_round_trip_and_detached_payload(self) -> None:
        record = make_record("record-1")

        restored = KnowledgeRecord.from_dict(record.to_dict())
        payload = record.payload
        payload["name"] = "changed outside"

        self.assertEqual(restored, record)
        self.assertEqual(record.payload["name"], "Atlas")

    def test_rejects_non_json_payload(self) -> None:
        with self.assertRaisesRegex(ValueError, "JSON-compatible"):
            KnowledgeRecord.from_payload(
                id="record-1",
                record_type=KnowledgeRecordType.UNKNOWN,
                recorded_at=RECORDED_AT,
                payload={"invalid": object()},
            )


class LocalKnowledgeStoreTests(unittest.TestCase):
    def test_persists_record_across_reopen(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            path = Path(temporary_directory) / "atlas.db"
            record = make_record("record-1")
            with LocalKnowledgeStore(path) as store:
                store.save(record)

            with LocalKnowledgeStore(path) as reopened:
                restored = reopened.get(record.record_type, record.id)

        self.assertEqual(restored, record)

    def test_requires_explicit_replace(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            path = Path(temporary_directory) / "atlas.db"
            original = make_record("record-1")
            replacement = make_record("record-1", name="Replacement")
            with LocalKnowledgeStore(path) as store:
                store.save(original)
                with self.assertRaises(KnowledgeRecordConflictError):
                    store.save(replacement)
                store.save(replacement, replace=True)

                restored = store.get(KnowledgeRecordType.PROJECT, "record-1")

        self.assertEqual(restored, replacement)

    def test_lists_records_with_exact_filters_and_stable_order(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            path = Path(temporary_directory) / "atlas.db"
            records = (
                make_record("later", minute=2),
                make_record(
                    "other-project",
                    project_id="project-2",
                    minute=1,
                ),
                make_record(
                    "change",
                    record_type=KnowledgeRecordType.PROJECT_CHANGE,
                    minute=1,
                ),
            )
            with LocalKnowledgeStore(path) as store:
                for record in records:
                    store.save(record)

                project_records = store.list_records(project_id="project-1")
                typed_records = store.list_records(
                    record_type=KnowledgeRecordType.PROJECT_CHANGE
                )

        self.assertEqual(
            [record.id for record in project_records], ["change", "later"]
        )
        self.assertEqual([record.id for record in typed_records], ["change"])

    def test_same_id_can_exist_for_different_record_types(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            path = Path(temporary_directory) / "atlas.db"
            project = make_record("shared-id")
            snapshot = make_record(
                "shared-id",
                record_type=KnowledgeRecordType.PROJECT_SNAPSHOT,
            )
            with LocalKnowledgeStore(path) as store:
                store.save(project)
                store.save(snapshot)

                records = store.list_records()

        self.assertEqual(len(records), 2)

    def test_rejects_unsupported_schema_version(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            path = Path(temporary_directory) / "atlas.db"
            connection = sqlite3.connect(path)
            connection.execute(
                "CREATE TABLE schema_metadata ("
                "singleton INTEGER PRIMARY KEY, version INTEGER NOT NULL)"
            )
            connection.execute(
                "INSERT INTO schema_metadata (singleton, version) VALUES (1, 999)"
            )
            connection.commit()
            connection.close()

            with self.assertRaises(KnowledgeSchemaError):
                LocalKnowledgeStore(path)

    def test_rejects_directory_as_store_path(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            with self.assertRaisesRegex(ValueError, "must be a file"):
                LocalKnowledgeStore(temporary_directory)


if __name__ == "__main__":
    unittest.main()
