"""Tests for structured and local text knowledge queries."""

from datetime import datetime, timedelta, timezone
from pathlib import Path
import sys
from tempfile import TemporaryDirectory
import unittest


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from project_atlas.domain import (  # noqa: E402
    KnowledgeQuery,
    KnowledgeQueryResult,
    KnowledgeRecord,
    KnowledgeRecordType,
)
from project_atlas.knowledge import (  # noqa: E402
    KnowledgeQueryEngine,
    LocalKnowledgeStore,
)


BASE_AT = datetime(2026, 8, 23, 19, 0, tzinfo=timezone.utc)


def make_record(
    record_id: str,
    record_type: KnowledgeRecordType,
    project_id: str,
    minute: int,
    **payload: object,
) -> KnowledgeRecord:
    return KnowledgeRecord.from_payload(
        id=record_id,
        record_type=record_type,
        project_id=project_id,
        recorded_at=BASE_AT + timedelta(minutes=minute),
        payload=payload,
    )


class KnowledgeQueryEngineTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary_directory = TemporaryDirectory()
        path = Path(self.temporary_directory.name) / "atlas.db"
        self.store = LocalKnowledgeStore(path)
        self.records = (
            make_record(
                "project-atlas",
                KnowledgeRecordType.PROJECT,
                "project-1",
                0,
                name="Project Atlas",
                language="Python",
            ),
            make_record(
                "atlas-structure",
                KnowledgeRecordType.PROJECT_STRUCTURE,
                "project-1",
                1,
                technologies=["Python", "SQLite"],
            ),
            make_record(
                "other-project",
                KnowledgeRecordType.PROJECT,
                "project-2",
                2,
                name="Other Service",
                language="Go",
            ),
        )
        for record in self.records:
            self.store.save(record)
        self.engine = KnowledgeQueryEngine(self.store)

    def tearDown(self) -> None:
        self.store.close()
        self.temporary_directory.cleanup()

    def test_structured_query_filters_type_project_and_time(self) -> None:
        query = KnowledgeQuery(
            record_types=(KnowledgeRecordType.PROJECT_STRUCTURE,),
            project_id="project-1",
            recorded_from=BASE_AT + timedelta(seconds=1),
            recorded_to=BASE_AT + timedelta(minutes=1),
        )

        result = self.engine.query(query, executed_at=BASE_AT + timedelta(minutes=3))

        self.assertEqual([record.id for record in result.records], ["atlas-structure"])

    def test_text_search_is_case_insensitive_and_requires_all_terms(self) -> None:
        result = self.engine.search(
            "ATLAS language python",
            project_id="project-1",
            executed_at=BASE_AT + timedelta(minutes=3),
        )

        self.assertEqual([record.id for record in result.records], ["project-atlas"])

    def test_query_reports_total_before_limit(self) -> None:
        result = self.engine.search(
            "project",
            record_types=(KnowledgeRecordType.PROJECT,),
            limit=1,
            executed_at=BASE_AT + timedelta(minutes=3),
        )

        self.assertEqual(len(result.records), 1)
        self.assertEqual(result.total_matches, 2)

    def test_query_result_round_trip_serialization(self) -> None:
        result = self.engine.query(
            KnowledgeQuery(project_id="project-1"),
            executed_at=BASE_AT + timedelta(minutes=3),
        )

        restored = KnowledgeQueryResult.from_dict(result.to_dict())

        self.assertEqual(restored, result)

    def test_query_is_read_only(self) -> None:
        before = self.store.list_records()

        self.engine.search("Atlas", executed_at=BASE_AT + timedelta(minutes=3))

        self.assertEqual(self.store.list_records(), before)

    def test_rejects_punctuation_only_search_and_invalid_limit(self) -> None:
        with self.assertRaisesRegex(ValueError, "searchable term"):
            self.engine.search("!!!", executed_at=BASE_AT)
        with self.assertRaisesRegex(ValueError, "between 1 and 1000"):
            KnowledgeQuery(limit=0)


if __name__ == "__main__":
    unittest.main()
