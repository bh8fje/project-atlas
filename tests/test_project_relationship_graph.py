"""Tests for explicit cross-project relationship graphs."""

from datetime import datetime, timezone
from pathlib import Path
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from project_atlas.domain import (  # noqa: E402
    Project,
    ProjectRelationship,
    ProjectRelationshipGraph,
    ProjectRelationshipType,
    ProjectStatus,
)
from project_atlas.knowledge import ProjectRelationshipGraphBuilder  # noqa: E402


GENERATED_AT = datetime(2026, 8, 23, 17, 0, tzinfo=timezone.utc)


def make_project(project_id: str) -> Project:
    return Project(
        id=project_id,
        name=project_id,
        path=f"/projects/{project_id}",
        created_at=GENERATED_AT,
        updated_at=GENERATED_AT,
        status=ProjectStatus.ACTIVE,
    )


class ProjectRelationshipGraphTests(unittest.TestCase):
    def test_builds_sorted_graph_and_queries_adjacency(self) -> None:
        projects = (make_project("project-b"), make_project("project-a"))
        relationship = ProjectRelationship(
            source_project_id="project-a",
            target_project_id="project-b",
            relationship_type=ProjectRelationshipType.DEPENDS_ON,
        )

        graph = ProjectRelationshipGraphBuilder().build(
            projects,
            (relationship,),
            generated_at=GENERATED_AT,
        )

        self.assertEqual(
            [project.id for project in graph.projects],
            ["project-a", "project-b"],
        )
        self.assertEqual(graph.outgoing("project-a"), (relationship,))
        self.assertEqual(graph.incoming("project-b"), (relationship,))
        self.assertEqual(graph.project_count, 2)
        self.assertEqual(graph.relationship_count, 1)

    def test_graph_round_trip_serialization(self) -> None:
        graph = ProjectRelationshipGraphBuilder().build(
            (make_project("project-a"), make_project("project-b")),
            (
                ProjectRelationship(
                    source_project_id="project-a",
                    target_project_id="project-b",
                    relationship_type=ProjectRelationshipType.RELATED_TO,
                ),
            ),
            generated_at=GENERATED_AT,
        )

        restored = ProjectRelationshipGraph.from_dict(graph.to_dict())

        self.assertEqual(restored, graph)

    def test_rejects_relationship_to_unknown_project(self) -> None:
        relationship = ProjectRelationship(
            source_project_id="project-a",
            target_project_id="missing",
            relationship_type=ProjectRelationshipType.UNKNOWN,
        )

        with self.assertRaisesRegex(ValueError, "reference graph projects"):
            ProjectRelationshipGraphBuilder().build(
                (make_project("project-a"),),
                (relationship,),
                generated_at=GENERATED_AT,
            )

    def test_rejects_duplicate_project_and_relationship(self) -> None:
        project_a = make_project("project-a")
        project_b = make_project("project-b")
        relationship = ProjectRelationship(
            source_project_id="project-a",
            target_project_id="project-b",
            relationship_type=ProjectRelationshipType.GENERATED_FROM,
        )

        with self.assertRaisesRegex(ValueError, "project ids"):
            ProjectRelationshipGraphBuilder().build(
                (project_a, project_a), (), generated_at=GENERATED_AT
            )
        with self.assertRaisesRegex(ValueError, "relationships must be unique"):
            ProjectRelationshipGraphBuilder().build(
                (project_a, project_b),
                (relationship, relationship),
                generated_at=GENERATED_AT,
            )

    def test_relationship_rejects_self_reference(self) -> None:
        with self.assertRaisesRegex(ValueError, "cannot reference itself"):
            ProjectRelationship(
                source_project_id="project-a",
                target_project_id="project-a",
                relationship_type=ProjectRelationshipType.RELATED_TO,
            )

    def test_adjacency_rejects_unknown_project(self) -> None:
        graph = ProjectRelationshipGraphBuilder().build(
            (make_project("project-a"),), (), generated_at=GENERATED_AT
        )

        with self.assertRaisesRegex(ValueError, "graph project"):
            graph.outgoing("missing")


if __name__ == "__main__":
    unittest.main()
