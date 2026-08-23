"""Tests for repository asset domain contracts."""

from datetime import datetime, timedelta, timezone
from pathlib import Path
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from project_atlas.domain import (  # noqa: E402
    ArtifactType,
    AssetRelationship,
    ProjectArtifact,
    RelationshipType,
    Repository,
    RepositorySnapshot,
)


CREATED_AT = datetime(2026, 8, 23, 10, 0, tzinfo=timezone.utc)
UPDATED_AT = CREATED_AT + timedelta(minutes=30)


class ProjectArtifactTests(unittest.TestCase):
    def test_artifact_creation(self) -> None:
        artifact = ProjectArtifact(
            id="artifact-readme",
            name="README.md",
            path="/projects/atlas/README.md",
            artifact_type=ArtifactType.DOCUMENT,
            created_at=CREATED_AT,
            updated_at=UPDATED_AT,
        )

        self.assertIs(artifact.artifact_type, ArtifactType.DOCUMENT)
        self.assertEqual(artifact.name, "README.md")

    def test_artifact_type_validation(self) -> None:
        with self.assertRaisesRegex(TypeError, "ArtifactType"):
            ProjectArtifact(
                id="artifact-readme",
                name="README.md",
                path="/projects/atlas/README.md",
                artifact_type="DOCUMENT",  # type: ignore[arg-type]
                created_at=CREATED_AT,
                updated_at=UPDATED_AT,
            )

    def test_artifact_round_trip_serialization(self) -> None:
        artifact = ProjectArtifact(
            id="artifact-config",
            name="pyproject.toml",
            path="/projects/atlas/pyproject.toml",
            artifact_type=ArtifactType.CONFIGURATION,
            created_at=CREATED_AT,
            updated_at=UPDATED_AT,
        )

        serialized = artifact.to_dict()

        self.assertEqual(serialized["artifact_type"], "CONFIGURATION")
        self.assertEqual(ProjectArtifact.from_dict(serialized), artifact)


class RepositoryTests(unittest.TestCase):
    def test_repository_creation_and_serialization(self) -> None:
        repository = Repository(
            id="repo-atlas",
            name="project-atlas",
            root_path="/projects/project-atlas",
            branch="main",
        )

        self.assertEqual(repository.branch, "main")
        self.assertEqual(Repository.from_dict(repository.to_dict()), repository)

    def test_repository_rejects_empty_branch(self) -> None:
        with self.assertRaisesRegex(ValueError, "branch"):
            Repository(
                id="repo-atlas",
                name="project-atlas",
                root_path="/projects/project-atlas",
                branch=" ",
            )


class RepositorySnapshotTests(unittest.TestCase):
    def test_snapshot_creation_and_serialization(self) -> None:
        snapshot = RepositorySnapshot(
            id="snapshot-001",
            repository_id="repo-atlas",
            created_at=CREATED_AT,
            artifact_count=12,
        )

        self.assertEqual(snapshot.artifact_count, 12)
        self.assertEqual(RepositorySnapshot.from_dict(snapshot.to_dict()), snapshot)

    def test_snapshot_rejects_negative_artifact_count(self) -> None:
        with self.assertRaisesRegex(ValueError, "artifact_count"):
            RepositorySnapshot(
                id="snapshot-001",
                repository_id="repo-atlas",
                created_at=CREATED_AT,
                artifact_count=-1,
            )


class AssetRelationshipTests(unittest.TestCase):
    def test_relationship_creation_and_serialization(self) -> None:
        relationship = AssetRelationship(
            source_id="repo-atlas",
            target_id="artifact-readme",
            relationship_type=RelationshipType.CONTAINS,
        )

        self.assertIs(relationship.relationship_type, RelationshipType.CONTAINS)
        self.assertEqual(
            AssetRelationship.from_dict(relationship.to_dict()), relationship
        )

    def test_relationship_rejects_self_reference(self) -> None:
        with self.assertRaisesRegex(ValueError, "different"):
            AssetRelationship(
                source_id="artifact-readme",
                target_id="artifact-readme",
                relationship_type=RelationshipType.DEPENDS_ON,
            )


if __name__ == "__main__":
    unittest.main()
