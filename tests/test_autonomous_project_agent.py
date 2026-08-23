import unittest
from dataclasses import replace
from datetime import datetime, timedelta, timezone

from project_atlas.domain import (
    AgentObservationCycle,
    AgentSignalSeverity,
    AgentSignalType,
    ChangeType,
    Project,
    ProjectChange,
    ProjectRelationship,
    ProjectRelationshipGraph,
    ProjectRelationshipType,
    ProjectStatus,
    ProjectUnderstanding,
)
from project_atlas.intelligence import AutonomousProjectAgent, MultiProjectIntelligenceService


NOW = datetime(2026, 8, 23, 11, 0, tzinfo=timezone.utc)


def make_project(project_id: str) -> Project:
    return Project(project_id, project_id.upper(), f"/projects/{project_id}", NOW, NOW, ProjectStatus.ACTIVE)


def make_understanding(project_id: str, risks: tuple[str, ...]) -> ProjectUnderstanding:
    return ProjectUnderstanding(project_id, "Purpose", ("Python",), risks, "steady", NOW, (f"PROJECT:{project_id}",), "fixture", "v1")


class AutonomousProjectAgentTests(unittest.TestCase):
    def setUp(self) -> None:
        projects = (make_project("a"), make_project("b"), make_project("c"))
        understandings = (
            make_understanding("a", ("Dependency drift",)),
            make_understanding("b", ("dependency drift",)),
            make_understanding("c", ()),
        )
        graph = ProjectRelationshipGraph(NOW, projects, (ProjectRelationship("a", "b", ProjectRelationshipType.DEPENDS_ON),))
        self.portfolio = MultiProjectIntelligenceService().analyze(projects, understandings, graph, generated_at=NOW)
        self.changes = (
            ProjectChange("change-1", "a", "snap-1", "snap-2", "src/a.py", ChangeType.MODIFIED, NOW),
            ProjectChange("change-2", "a", "snap-1", "snap-2", "old.txt", ChangeType.REMOVED, NOW),
        )

    def test_observes_changes_risks_and_isolated_projects(self) -> None:
        cycle = AutonomousProjectAgent().observe(self.changes, self.portfolio, observed_at=NOW)
        self.assertEqual({signal.signal_type for signal in cycle.signals}, {AgentSignalType.CHANGE_DETECTED, AgentSignalType.SHARED_RISK, AgentSignalType.ISOLATED_PROJECT})
        change_signal = next(item for item in cycle.signals if item.signal_type is AgentSignalType.CHANGE_DETECTED)
        self.assertEqual(change_signal.severity, AgentSignalSeverity.WARNING)
        self.assertEqual(cycle.observed_change_ids, ("change-1", "change-2"))

    def test_cycle_never_executes_actions(self) -> None:
        cycle = AutonomousProjectAgent().observe(self.changes, self.portfolio, observed_at=NOW)
        self.assertEqual(cycle.actions_executed, 0)
        with self.assertRaises(ValueError):
            replace(cycle, actions_executed=1)

    def test_cycle_is_deterministic_for_reordered_changes(self) -> None:
        agent = AutonomousProjectAgent()
        first = agent.observe(self.changes, self.portfolio, observed_at=NOW)
        second = agent.observe(tuple(reversed(self.changes)), self.portfolio, observed_at=NOW)
        self.assertEqual(first, second)

    def test_cycle_round_trip_serialization(self) -> None:
        cycle = AutonomousProjectAgent().observe(self.changes, self.portfolio, observed_at=NOW)
        self.assertEqual(AgentObservationCycle.from_dict(cycle.to_dict()), cycle)

    def test_rejects_unknown_project_changes(self) -> None:
        unknown = ProjectChange("change-x", "x", "snap-1", "snap-2", "x.py", ChangeType.ADDED, NOW)
        with self.assertRaises(ValueError):
            AutonomousProjectAgent().observe((unknown,), self.portfolio, observed_at=NOW)

    def test_rejects_future_and_duplicate_changes(self) -> None:
        future = ProjectChange("future", "a", "snap-1", "snap-2", "x.py", ChangeType.ADDED, NOW + timedelta(seconds=1))
        with self.assertRaises(ValueError):
            AutonomousProjectAgent().observe((future,), self.portfolio, observed_at=NOW)
        with self.assertRaises(ValueError):
            AutonomousProjectAgent().observe((self.changes[0], self.changes[0]), self.portfolio, observed_at=NOW)
        with self.assertRaises(ValueError):
            AutonomousProjectAgent().observe((), replace(self.portfolio, generated_at=NOW + timedelta(seconds=1)), observed_at=NOW)

    def test_empty_change_set_still_reports_portfolio_risks(self) -> None:
        cycle = AutonomousProjectAgent().observe((), self.portfolio, observed_at=NOW)
        self.assertNotIn(AgentSignalType.CHANGE_DETECTED, {item.signal_type for item in cycle.signals})
        self.assertIn(AgentSignalType.SHARED_RISK, {item.signal_type for item in cycle.signals})

    def test_agent_has_no_background_scheduler(self) -> None:
        agent = AutonomousProjectAgent()
        self.assertFalse(hasattr(agent, "start"))
        self.assertFalse(hasattr(agent, "run_forever"))


if __name__ == "__main__":
    unittest.main()
