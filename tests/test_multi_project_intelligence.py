import unittest
from datetime import datetime, timezone

from project_atlas.domain import (
    MultiProjectIntelligence,
    Project,
    ProjectRelationship,
    ProjectRelationshipGraph,
    ProjectRelationshipType,
    ProjectStatus,
    ProjectUnderstanding,
)
from project_atlas.intelligence import MultiProjectIntelligenceService


NOW = datetime(2026, 8, 23, 10, 0, tzinfo=timezone.utc)


def project(project_id: str) -> Project:
    return Project(project_id, project_id.upper(), f"/projects/{project_id}", NOW, NOW, ProjectStatus.ACTIVE)


def understanding(project_id: str, risks: tuple[str, ...]) -> ProjectUnderstanding:
    return ProjectUnderstanding(project_id, f"Purpose {project_id}", ("Python",), risks, "steady", NOW, (f"PROJECT:{project_id}",), "fixture", "fixture-v1")


class MultiProjectIntelligenceTests(unittest.TestCase):
    def setUp(self) -> None:
        self.projects = (project("a"), project("b"), project("c"))
        self.understandings = (
            understanding("a", ("Dependency drift", "Missing docs")),
            understanding("b", ("dependency drift",)),
            understanding("c", ()),
        )
        self.graph = ProjectRelationshipGraph(
            NOW,
            self.projects,
            (ProjectRelationship("a", "b", ProjectRelationshipType.DEPENDS_ON),),
        )

    def test_aggregates_shared_risks_relationships_and_isolates(self) -> None:
        result = MultiProjectIntelligenceService().analyze(self.projects, self.understandings, self.graph, generated_at=NOW)
        self.assertEqual(result.project_count, 3)
        self.assertEqual(result.shared_risks, ("Dependency drift",))
        self.assertEqual(result.isolated_project_ids, ("c",))
        self.assertEqual([item.relationship_count for item in result.projects], [1, 1, 0])

    def test_output_is_deterministic_for_reordered_inputs(self) -> None:
        service = MultiProjectIntelligenceService()
        first = service.analyze(self.projects, self.understandings, self.graph, generated_at=NOW)
        second = service.analyze(tuple(reversed(self.projects)), tuple(reversed(self.understandings)), self.graph, generated_at=NOW)
        self.assertEqual(first, second)

    def test_result_round_trip_serialization(self) -> None:
        result = MultiProjectIntelligenceService().analyze(self.projects, self.understandings, self.graph, generated_at=NOW)
        self.assertEqual(MultiProjectIntelligence.from_dict(result.to_dict()), result)

    def test_requires_at_least_two_projects(self) -> None:
        single_graph = ProjectRelationshipGraph(NOW, (self.projects[0],), ())
        with self.assertRaises(ValueError):
            MultiProjectIntelligenceService().analyze((self.projects[0],), (self.understandings[0],), single_graph)

    def test_requires_exactly_one_understanding_per_project(self) -> None:
        with self.assertRaises(ValueError):
            MultiProjectIntelligenceService().analyze(self.projects, self.understandings[:2], self.graph)

    def test_requires_graph_to_match_project_set(self) -> None:
        partial_graph = ProjectRelationshipGraph(NOW, self.projects[:2], ())
        with self.assertRaises(ValueError):
            MultiProjectIntelligenceService().analyze(self.projects, self.understandings, partial_graph)

    def test_rejects_naive_generation_time(self) -> None:
        with self.assertRaises(ValueError):
            MultiProjectIntelligenceService().analyze(self.projects, self.understandings, self.graph, generated_at=datetime(2026, 8, 23))


if __name__ == "__main__":
    unittest.main()
