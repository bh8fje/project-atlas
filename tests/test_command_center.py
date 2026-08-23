import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path

from project_atlas.application import CommandCenter
from project_atlas.domain import (
    CommandDefinition,
    CommandEffect,
    CommandRequest,
    CommandResult,
    CommandStatus,
)


NOW = datetime(2026, 8, 23, 9, 0, tzinfo=timezone.utc)


class CommandContractTests(unittest.TestCase):
    def test_request_and_result_round_trip(self) -> None:
        request = CommandRequest("req-1", "project.status", {"project_id": "p1"}, NOW)
        self.assertEqual(CommandRequest.from_dict(request.to_dict()), request)
        result = CommandResult("req-1", "project.status", CommandStatus.SUCCEEDED, NOW, "done", {"status": "ACTIVE"})
        self.assertEqual(CommandResult.from_dict(result.to_dict()), result)

    def test_parameters_are_json_compatible_and_detached(self) -> None:
        parameters = {"filters": ["active"]}
        request = CommandRequest("req-1", "project.list", parameters, NOW)
        parameters["filters"].append("archived")
        self.assertEqual(request.parameters["filters"], ["active"])
        with self.assertRaises(ValueError):
            CommandRequest("req-2", "bad", {"value": object()}, NOW)


class CommandCenterTests(unittest.TestCase):
    def test_dashboard_exposes_non_executing_command_center_summary(self) -> None:
        app = Path(__file__).resolve().parents[1] / "dashboard" / "app"
        page = (app / "page.tsx").read_text()
        translations = (app / "i18n.ts").read_text()
        self.assertIn('id="command-center"', page)
        self.assertIn("t.noHandlers", page)
        self.assertIn("No handlers registered", translations)

    def test_executes_registered_read_only_command(self) -> None:
        center = CommandCenter()
        center.register(CommandDefinition("project.status", "Read project status"), lambda params: {"project_id": params["project_id"], "status": "ACTIVE"})
        result = center.execute(CommandRequest("req-1", "project.status", {"project_id": "p1"}, NOW), completed_at=NOW)
        self.assertEqual(result.status, CommandStatus.SUCCEEDED)
        self.assertEqual(result.output["status"], "ACTIVE")

    def test_rejects_unconfirmed_mutation_without_calling_handler(self) -> None:
        calls = []
        center = CommandCenter()
        center.register(CommandDefinition("project.archive", "Archive project", CommandEffect.MUTATING), lambda params: calls.append(params) or {})
        result = center.execute(CommandRequest("req-1", "project.archive", {}, NOW), completed_at=NOW)
        self.assertEqual(result.status, CommandStatus.REJECTED)
        self.assertEqual(calls, [])

    def test_executes_confirmed_mutation(self) -> None:
        center = CommandCenter()
        center.register(CommandDefinition("project.archive", "Archive project", CommandEffect.MUTATING), lambda params: {"archived": True})
        request = CommandRequest("req-1", "project.archive", {}, NOW, confirmed=True)
        self.assertTrue(center.execute(request, completed_at=NOW).output["archived"])

    def test_lists_commands_deterministically_and_rejects_duplicates(self) -> None:
        center = CommandCenter()
        center.register(CommandDefinition("z.last", "Last"), lambda params: {})
        center.register(CommandDefinition("a.first", "First"), lambda params: {})
        self.assertEqual([item.name for item in center.list_commands()], ["a.first", "z.last"])
        with self.assertRaises(ValueError):
            center.register(CommandDefinition("a.first", "Duplicate"), lambda params: {})

    def test_unknown_commands_and_handler_failures_are_transparent(self) -> None:
        center = CommandCenter()
        with self.assertRaises(KeyError):
            center.execute(CommandRequest("req-1", "missing", {}, NOW))
        center.register(CommandDefinition("broken", "Fails"), lambda params: (_ for _ in ()).throw(RuntimeError("boom")))
        with self.assertRaisesRegex(RuntimeError, "boom"):
            center.execute(CommandRequest("req-2", "broken", {}, NOW))

    def test_rejects_completion_before_request(self) -> None:
        center = CommandCenter()
        center.register(CommandDefinition("status", "Status"), lambda params: {})
        with self.assertRaises(ValueError):
            center.execute(CommandRequest("req-1", "status", {}, NOW), completed_at=NOW - timedelta(seconds=1))


if __name__ == "__main__":
    unittest.main()
