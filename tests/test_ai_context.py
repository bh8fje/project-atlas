"""Tests for bounded, redacted, traceable AI context construction."""

from datetime import datetime, timedelta, timezone
from pathlib import Path
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from project_atlas.domain import (  # noqa: E402
    AIContext,
    KnowledgeRecord,
    KnowledgeRecordType,
)
from project_atlas.intelligence import AIContextBuilder  # noqa: E402


BASE_AT = datetime(2026, 8, 23, 20, 0, tzinfo=timezone.utc)


def make_record(
    record_id: str,
    minute: int,
    *,
    project_id: str | None = "project-1",
    payload: dict[str, object] | None = None,
) -> KnowledgeRecord:
    return KnowledgeRecord.from_payload(
        id=record_id,
        record_type=KnowledgeRecordType.PROJECT,
        project_id=project_id,
        recorded_at=BASE_AT + timedelta(minutes=minute),
        payload=payload or {"name": record_id},
    )


class AIContextBuilderTests(unittest.TestCase):
    def test_builds_deterministic_context_with_traceable_sources(self) -> None:
        later = make_record("later", 2)
        earlier = make_record("earlier", 1)

        context = AIContextBuilder().build(
            "project-1",
            (later, earlier),
            generated_at=BASE_AT + timedelta(minutes=3),
        )

        self.assertLess(
            context.content.index("earlier"), context.content.index("later")
        )
        self.assertEqual(
            context.source_record_keys,
            ("PROJECT:earlier", "PROJECT:later"),
        )
        self.assertFalse(context.truncated)

    def test_redacts_nested_sensitive_keys(self) -> None:
        record = make_record(
            "sensitive",
            0,
            payload={
                "name": "safe",
                "password": "do-not-expose",
                "nested": {
                    "api_key": "also-secret",
                    "accessToken": "token-value",
                },
            },
        )

        context = AIContextBuilder().build(
            "project-1", (record,), generated_at=BASE_AT
        )

        self.assertNotIn("do-not-expose", context.content)
        self.assertNotIn("also-secret", context.content)
        self.assertNotIn("token-value", context.content)
        self.assertIn("[REDACTED]", context.content)
        self.assertIn("safe", context.content)

    def test_enforces_character_limit_and_marks_truncation(self) -> None:
        record = make_record(
            "large",
            0,
            payload={"description": "x" * 1_000},
        )

        context = AIContextBuilder().build(
            "project-1",
            (record,),
            max_characters=256,
            generated_at=BASE_AT,
        )

        self.assertEqual(context.character_count, 256)
        self.assertTrue(context.truncated)
        self.assertTrue(context.content.endswith("[TRUNCATED]"))

    def test_accepts_global_record_but_rejects_other_project(self) -> None:
        global_record = make_record("global", 0, project_id=None)
        other_project = make_record("other", 0, project_id="project-2")
        builder = AIContextBuilder()

        context = builder.build("project-1", (global_record,), generated_at=BASE_AT)
        self.assertIn("global", context.content)
        with self.assertRaisesRegex(ValueError, "context project"):
            builder.build("project-1", (other_project,), generated_at=BASE_AT)

    def test_context_round_trip_serialization(self) -> None:
        context = AIContextBuilder().build(
            "project-1", (make_record("record-1", 0),), generated_at=BASE_AT
        )

        restored = AIContext.from_dict(context.to_dict())

        self.assertEqual(restored, context)

    def test_rejects_invalid_limit_and_naive_timestamp(self) -> None:
        builder = AIContextBuilder()

        with self.assertRaisesRegex(ValueError, "between 256"):
            builder.build("project-1", (), max_characters=255)
        with self.assertRaisesRegex(ValueError, "timezone"):
            builder.build(
                "project-1",
                (),
                generated_at=datetime(2026, 8, 23),
            )


if __name__ == "__main__":
    unittest.main()
