"""Tests for the core Project Atlas domain contracts."""

from datetime import datetime, timedelta, timezone
from pathlib import Path
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from project_atlas.domain import Project, ProjectStatus, Task, TaskStatus  # noqa: E402


CREATED_AT = datetime(2026, 8, 23, 9, 0, tzinfo=timezone.utc)
UPDATED_AT = CREATED_AT + timedelta(hours=1)


class ProjectModelTests(unittest.TestCase):
    def test_project_creation(self) -> None:
        project = Project(
            id="project-atlas",
            name="Project Atlas",
            path="/projects/project-atlas",
            created_at=CREATED_AT,
            updated_at=UPDATED_AT,
            status=ProjectStatus.ACTIVE,
        )

        self.assertEqual(project.name, "Project Atlas")
        self.assertIs(project.status, ProjectStatus.ACTIVE)

    def test_project_round_trip_serialization(self) -> None:
        project = Project(
            id="project-atlas",
            name="Project Atlas",
            path="/projects/project-atlas",
            created_at=CREATED_AT,
            updated_at=UPDATED_AT,
            status=ProjectStatus.INITIALIZING,
        )

        serialized = project.to_dict()

        self.assertEqual(serialized["status"], "INITIALIZING")
        self.assertEqual(Project.from_dict(serialized), project)

    def test_project_rejects_invalid_time_order(self) -> None:
        with self.assertRaisesRegex(ValueError, "updated_at"):
            Project(
                id="project-atlas",
                name="Project Atlas",
                path="/projects/project-atlas",
                created_at=UPDATED_AT,
                updated_at=CREATED_AT,
                status=ProjectStatus.UNKNOWN,
            )

    def test_project_rejects_naive_datetime(self) -> None:
        with self.assertRaisesRegex(ValueError, "timezone"):
            Project(
                id="project-atlas",
                name="Project Atlas",
                path="/projects/project-atlas",
                created_at=datetime(2026, 8, 23, 9, 0),
                updated_at=UPDATED_AT,
                status=ProjectStatus.UNKNOWN,
            )


class TaskModelTests(unittest.TestCase):
    def test_task_creation(self) -> None:
        task = Task(
            id="TASK-002",
            name="Core Domain Foundation",
            description="Define stable domain contracts.",
            status=TaskStatus.PLANNED,
            created_at=CREATED_AT,
        )

        self.assertIs(task.status, TaskStatus.PLANNED)
        self.assertIsNone(task.completed_at)

    def test_task_status_transitions(self) -> None:
        planned = Task(
            id="TASK-002",
            name="Core Domain Foundation",
            description="Define stable domain contracts.",
            status=TaskStatus.PLANNED,
            created_at=CREATED_AT,
        )

        in_progress = planned.transition_to(TaskStatus.IN_PROGRESS)
        completed = in_progress.transition_to(TaskStatus.COMPLETED, at=UPDATED_AT)

        self.assertIs(planned.status, TaskStatus.PLANNED)
        self.assertIs(in_progress.status, TaskStatus.IN_PROGRESS)
        self.assertIs(completed.status, TaskStatus.COMPLETED)
        self.assertEqual(completed.completed_at, UPDATED_AT)

    def test_task_rejects_invalid_transition(self) -> None:
        task = Task(
            id="TASK-002",
            name="Core Domain Foundation",
            description="Define stable domain contracts.",
            status=TaskStatus.COMPLETED,
            created_at=CREATED_AT,
            completed_at=UPDATED_AT,
        )

        with self.assertRaisesRegex(ValueError, "invalid task transition"):
            task.transition_to(TaskStatus.IN_PROGRESS)

    def test_task_round_trip_serialization(self) -> None:
        task = Task(
            id="TASK-002",
            name="Core Domain Foundation",
            description="Define stable domain contracts.",
            status=TaskStatus.COMPLETED,
            created_at=CREATED_AT,
            completed_at=UPDATED_AT,
        )

        serialized = task.to_dict()

        self.assertEqual(serialized["status"], "COMPLETED")
        self.assertEqual(Task.from_dict(serialized), task)


class EnumTests(unittest.TestCase):
    def test_status_enums_convert_from_serialized_values(self) -> None:
        self.assertIs(ProjectStatus("ARCHIVED"), ProjectStatus.ARCHIVED)
        self.assertIs(TaskStatus("BLOCKED"), TaskStatus.BLOCKED)

    def test_status_enums_reject_unknown_values(self) -> None:
        with self.assertRaises(ValueError):
            ProjectStatus("DELETED")
        with self.assertRaises(ValueError):
            TaskStatus("RETRYING")


if __name__ == "__main__":
    unittest.main()
