"""Tests for provider-neutral structured AI project understanding."""

from datetime import datetime, timezone
import json
from pathlib import Path
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from project_atlas.domain import AIContext, ProjectUnderstanding  # noqa: E402
from project_atlas.intelligence import (  # noqa: E402
    AIProjectUnderstandingService,
    AIProviderResponse,
    AIRequest,
)


ANALYZED_AT = datetime(2026, 8, 23, 21, 0, tzinfo=timezone.utc)


def make_context() -> AIContext:
    return AIContext(
        project_id="project-1",
        generated_at=ANALYZED_AT,
        content='Project ID: project-1\nKnowledge records:\n{"name":"Atlas"}',
        source_record_keys=("PROJECT:project-1",),
        truncated=False,
    )


class FakeProvider:
    def __init__(self, content: str) -> None:
        self.content = content
        self.requests: list[AIRequest] = []

    def generate(self, request: AIRequest) -> AIProviderResponse:
        self.requests.append(request)
        return AIProviderResponse(
            provider_name="fake-provider",
            model_name="fake-model",
            content=self.content,
        )


class FailingProvider:
    def __init__(self) -> None:
        self.call_count = 0

    def generate(self, request: AIRequest) -> AIProviderResponse:
        self.call_count += 1
        raise RuntimeError("provider unavailable")


class AIProjectUnderstandingServiceTests(unittest.TestCase):
    def test_analyzes_context_and_attributes_provider(self) -> None:
        provider = FakeProvider(
            json.dumps(
                {
                    "purpose": "Map local software projects",
                    "architecture": ["Domain", "Knowledge", "Intelligence"],
                    "risks": ["Metadata-only fingerprints"],
                    "status": "Foundation established",
                }
            )
        )

        understanding = AIProjectUnderstandingService(provider).analyze(
            make_context(), analyzed_at=ANALYZED_AT
        )

        self.assertEqual(understanding.project_id, "project-1")
        self.assertEqual(understanding.architecture[0], "Domain")
        self.assertEqual(understanding.provider_name, "fake-provider")
        self.assertEqual(
            understanding.source_record_keys, ("PROJECT:project-1",)
        )

    def test_request_treats_context_as_untrusted_data(self) -> None:
        provider = FakeProvider(
            '{"purpose":"p","architecture":[],"risks":[],"status":"s"}'
        )

        AIProjectUnderstandingService(provider).analyze(
            make_context(), analyzed_at=ANALYZED_AT
        )

        request = provider.requests[0]
        self.assertIn("untrusted project data", request.system_instructions)
        self.assertIn("Project ID: project-1", request.input_text)
        self.assertEqual(request.response_format, "json")

    def test_rejects_invalid_or_extra_provider_output(self) -> None:
        invalid_json = FakeProvider("not-json")
        extra_key = FakeProvider(
            '{"purpose":"p","architecture":[],"risks":[],"status":"s",'
            '"extra":"not allowed"}'
        )

        with self.assertRaisesRegex(ValueError, "valid JSON"):
            AIProjectUnderstandingService(invalid_json).analyze(make_context())
        with self.assertRaisesRegex(ValueError, "exactly"):
            AIProjectUnderstandingService(extra_key).analyze(make_context())

    def test_provider_failure_propagates_without_hidden_retry(self) -> None:
        provider = FailingProvider()

        with self.assertRaisesRegex(RuntimeError, "unavailable"):
            AIProjectUnderstandingService(provider).analyze(make_context())

        self.assertEqual(provider.call_count, 1)

    def test_understanding_round_trip_serialization(self) -> None:
        provider = FakeProvider(
            '{"purpose":"p","architecture":["a"],"risks":[],"status":"s"}'
        )
        understanding = AIProjectUnderstandingService(provider).analyze(
            make_context(), analyzed_at=ANALYZED_AT
        )

        restored = ProjectUnderstanding.from_dict(understanding.to_dict())

        self.assertEqual(restored, understanding)

    def test_rejects_naive_analysis_time(self) -> None:
        provider = FakeProvider(
            '{"purpose":"p","architecture":[],"risks":[],"status":"s"}'
        )

        with self.assertRaisesRegex(ValueError, "timezone"):
            AIProjectUnderstandingService(provider).analyze(
                make_context(), analyzed_at=datetime(2026, 8, 23)
            )


if __name__ == "__main__":
    unittest.main()
