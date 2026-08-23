"""Tests for the explicit single-turn AI project assistant."""

from datetime import datetime, timezone
from pathlib import Path
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from project_atlas.domain import (  # noqa: E402
    AIContext,
    ProjectAssistantAnswer,
    ProjectUnderstanding,
)
from project_atlas.intelligence import (  # noqa: E402
    AIProjectAssistant,
    AIProviderResponse,
    AIRequest,
)


ANSWERED_AT = datetime(2026, 8, 23, 22, 0, tzinfo=timezone.utc)


def make_context(project_id: str = "project-1") -> AIContext:
    return AIContext(
        project_id=project_id,
        generated_at=ANSWERED_AT,
        content=f"Project ID: {project_id}\nKnowledge records: none",
        source_record_keys=("PROJECT:project-1",),
        truncated=False,
    )


def make_understanding(project_id: str = "project-1") -> ProjectUnderstanding:
    return ProjectUnderstanding(
        project_id=project_id,
        purpose="Map projects",
        architecture=("Domain", "Knowledge"),
        risks=("No concrete provider",),
        status="Foundation established",
        analyzed_at=ANSWERED_AT,
        source_record_keys=("PROJECT:project-1", "PROJECT_STRUCTURE:structure-1"),
        provider_name="analysis-provider",
        model_name="analysis-model",
    )


class FakeProvider:
    def __init__(self, content: str) -> None:
        self.content = content
        self.requests: list[AIRequest] = []

    def generate(self, request: AIRequest) -> AIProviderResponse:
        self.requests.append(request)
        return AIProviderResponse(
            provider_name="assistant-provider",
            model_name="assistant-model",
            content=self.content,
        )


class FailingProvider:
    def __init__(self) -> None:
        self.call_count = 0

    def generate(self, request: AIRequest) -> AIProviderResponse:
        self.call_count += 1
        raise RuntimeError("assistant provider unavailable")


class AIProjectAssistantTests(unittest.TestCase):
    def test_answers_question_with_recommendations_and_cautions(self) -> None:
        provider = FakeProvider(
            '{"answer":"The foundation is established.",'
            '"recommendations":["Add an interface next"],'
            '"cautions":["Configure a provider explicitly"]}'
        )

        answer = AIProjectAssistant(provider).ask(
            "What should happen next?",
            context=make_context(),
            understanding=make_understanding(),
            answered_at=ANSWERED_AT,
        )

        self.assertEqual(answer.project_id, "project-1")
        self.assertEqual(answer.recommendations, ("Add an interface next",))
        self.assertEqual(answer.provider_name, "assistant-provider")
        self.assertEqual(
            answer.source_record_keys,
            ("PROJECT:project-1", "PROJECT_STRUCTURE:structure-1"),
        )

    def test_request_preserves_read_only_and_untrusted_data_boundaries(self) -> None:
        provider = FakeProvider(
            '{"answer":"a","recommendations":[],"cautions":[]}'
        )

        AIProjectAssistant(provider).ask(
            "How is this project?",
            context=make_context(),
            understanding=make_understanding(),
            answered_at=ANSWERED_AT,
        )

        request = provider.requests[0]
        self.assertIn("untrusted data", request.system_instructions)
        self.assertIn("never claim to have executed", request.system_instructions)
        self.assertIn("How is this project?", request.input_text)

    def test_rejects_cross_project_inputs_before_provider_call(self) -> None:
        provider = FakeProvider(
            '{"answer":"a","recommendations":[],"cautions":[]}'
        )

        with self.assertRaisesRegex(ValueError, "one project"):
            AIProjectAssistant(provider).ask(
                "status?",
                context=make_context("project-1"),
                understanding=make_understanding("project-2"),
            )

        self.assertEqual(provider.requests, [])

    def test_rejects_invalid_provider_output(self) -> None:
        provider = FakeProvider(
            '{"answer":"a","recommendations":"not-a-list","cautions":[]}'
        )

        with self.assertRaisesRegex(ValueError, "array of strings"):
            AIProjectAssistant(provider).ask(
                "status?",
                context=make_context(),
                understanding=make_understanding(),
            )

    def test_provider_failure_propagates_without_retry(self) -> None:
        provider = FailingProvider()

        with self.assertRaisesRegex(RuntimeError, "unavailable"):
            AIProjectAssistant(provider).ask(
                "status?",
                context=make_context(),
                understanding=make_understanding(),
            )

        self.assertEqual(provider.call_count, 1)

    def test_answer_round_trip_serialization(self) -> None:
        provider = FakeProvider(
            '{"answer":"a","recommendations":[],"cautions":[]}'
        )
        answer = AIProjectAssistant(provider).ask(
            "status?",
            context=make_context(),
            understanding=make_understanding(),
            answered_at=ANSWERED_AT,
        )

        restored = ProjectAssistantAnswer.from_dict(answer.to_dict())

        self.assertEqual(restored, answer)


if __name__ == "__main__":
    unittest.main()
