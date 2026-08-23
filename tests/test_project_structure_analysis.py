"""Tests for bounded project structure analysis."""

from datetime import datetime, timezone
from pathlib import Path
import sys
from tempfile import TemporaryDirectory
import unittest


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from project_atlas.analysis import (  # noqa: E402
    ProjectStructureAnalyzer,
    StructureAnalysisScope,
)
from project_atlas.domain import (  # noqa: E402
    ArtifactType,
    Project,
    ProjectStatus,
    ProjectStructure,
    RelationshipType,
)


ANALYZED_AT = datetime(2026, 8, 23, 13, 0, tzinfo=timezone.utc)


def make_project(path: Path) -> Project:
    return Project(
        id="project-under-test",
        name=path.name,
        path=str(path),
        created_at=ANALYZED_AT,
        updated_at=ANALYZED_AT,
        status=ProjectStatus.ACTIVE,
    )


class StructureAnalysisScopeTests(unittest.TestCase):
    def test_scope_validates_limits(self) -> None:
        with self.assertRaisesRegex(ValueError, "max_depth"):
            StructureAnalysisScope(max_depth=-1)
        with self.assertRaisesRegex(ValueError, "max_artifacts"):
            StructureAnalysisScope(max_artifacts=0)


class ProjectStructureAnalyzerTests(unittest.TestCase):
    def test_analyzes_structure_classification_and_technologies(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory) / "sample-project"
            source = root / "src"
            source.mkdir(parents=True)
            (root / "pyproject.toml").write_text("", encoding="utf-8")
            (root / "package.json").write_text("{}", encoding="utf-8")
            (root / "README.md").write_text("# Sample", encoding="utf-8")
            (source / "main.py").write_text("pass", encoding="utf-8")
            (root / "image.bin").write_bytes(b"binary")

            structure = ProjectStructureAnalyzer().analyze(
                make_project(root), analyzed_at=ANALYZED_AT
            )

        artifacts_by_name = {artifact.name: artifact for artifact in structure.artifacts}
        self.assertIs(
            artifacts_by_name["pyproject.toml"].artifact_type,
            ArtifactType.CONFIGURATION,
        )
        self.assertIs(
            artifacts_by_name["README.md"].artifact_type,
            ArtifactType.DOCUMENT,
        )
        self.assertIs(
            artifacts_by_name["main.py"].artifact_type,
            ArtifactType.SOURCE_CODE,
        )
        self.assertIs(
            artifacts_by_name["image.bin"].artifact_type,
            ArtifactType.FILE,
        )
        self.assertEqual(structure.technologies, ("Node.js", "Python"))
        self.assertEqual(structure.analyzed_at, ANALYZED_AT)

    def test_builds_contains_relationships_for_every_artifact(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory) / "sample-project"
            source = root / "src"
            source.mkdir(parents=True)
            (source / "main.go").write_text("package main", encoding="utf-8")
            project = make_project(root)

            structure = ProjectStructureAnalyzer().analyze(project)

        self.assertEqual(len(structure.relationships), structure.artifact_count)
        self.assertTrue(
            any(
                relationship.source_id == project.id
                and relationship.relationship_type is RelationshipType.CONTAINS
                for relationship in structure.relationships
            )
        )

    def test_structure_round_trip_serialization(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory) / "sample-project"
            root.mkdir()
            (root / "Cargo.toml").write_text("", encoding="utf-8")
            structure = ProjectStructureAnalyzer().analyze(
                make_project(root), analyzed_at=ANALYZED_AT
            )

            serialized = structure.to_dict()
            restored = ProjectStructure.from_dict(serialized)

        self.assertEqual(restored, structure)
        self.assertEqual(serialized["artifact_type_counts"]["CONFIGURATION"], 1)

    def test_honors_depth_and_excluded_directories(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory) / "sample-project"
            deep = root / "src" / "nested"
            dependency = root / "node_modules" / "dependency"
            deep.mkdir(parents=True)
            dependency.mkdir(parents=True)
            (deep / "hidden.py").write_text("pass", encoding="utf-8")
            (dependency / "package.json").write_text("{}", encoding="utf-8")

            structure = ProjectStructureAnalyzer().analyze(
                make_project(root), scope=StructureAnalysisScope(max_depth=1)
            )

        names = {artifact.name for artifact in structure.artifacts}
        self.assertIn("src", names)
        self.assertNotIn("nested", names)
        self.assertNotIn("node_modules", names)
        self.assertNotIn("dependency", names)

    def test_enforces_artifact_limit(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory) / "sample-project"
            root.mkdir()
            (root / "one.txt").write_text("one", encoding="utf-8")

            with self.assertRaisesRegex(ValueError, "max_artifacts"):
                ProjectStructureAnalyzer().analyze(
                    make_project(root),
                    scope=StructureAnalysisScope(max_artifacts=1),
                )

    def test_does_not_follow_symlinks(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory) / "sample-project"
            external = Path(temporary_directory) / "external"
            root.mkdir()
            external.mkdir()
            (external / "secret.py").write_text("pass", encoding="utf-8")
            (root / "external-link").symlink_to(external, target_is_directory=True)

            structure = ProjectStructureAnalyzer().analyze(make_project(root))

        self.assertNotIn(
            "external-link", {artifact.name for artifact in structure.artifacts}
        )
        self.assertNotIn("secret.py", {artifact.name for artifact in structure.artifacts})

    def test_rejects_invalid_project_path(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            missing = root / "missing"

            with self.assertRaisesRegex(ValueError, "does not exist"):
                ProjectStructureAnalyzer().analyze(make_project(missing))


if __name__ == "__main__":
    unittest.main()
