"""Tests for stable project identity and metadata fingerprints."""

from datetime import datetime, timezone
from pathlib import Path
import sys
from tempfile import TemporaryDirectory
import unittest


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from project_atlas.analysis import ProjectStructureAnalyzer  # noqa: E402
from project_atlas.discovery import DiscoveryScope, LocalProjectDiscoveryEngine  # noqa: E402
from project_atlas.domain import (  # noqa: E402
    Project,
    ProjectFingerprint,
    ProjectStatus,
)
from project_atlas.fingerprint import (  # noqa: E402
    FINGERPRINT_ALGORITHM,
    ProjectFingerprintGenerator,
    ProjectIdentityGenerator,
)


OBSERVED_AT = datetime(2026, 8, 23, 14, 0, tzinfo=timezone.utc)


def make_project(path: Path) -> Project:
    return Project(
        id=ProjectIdentityGenerator.stable_id(path),
        name=path.name,
        path=str(path),
        created_at=OBSERVED_AT,
        updated_at=OBSERVED_AT,
        status=ProjectStatus.ACTIVE,
    )


class ProjectIdentityGeneratorTests(unittest.TestCase):
    def test_identity_is_stable_for_same_canonical_path(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory) / "project"
            root.mkdir()

            first = ProjectIdentityGenerator.stable_id(root)
            second = ProjectIdentityGenerator.stable_id(root / ".")

        self.assertEqual(first, second)

    def test_different_paths_have_different_identities(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            first_root = Path(temporary_directory) / "first"
            second_root = Path(temporary_directory) / "second"
            first_root.mkdir()
            second_root.mkdir()

            first = ProjectIdentityGenerator.stable_id(first_root)
            second = ProjectIdentityGenerator.stable_id(second_root)

        self.assertNotEqual(first, second)

    def test_discovery_reuses_stable_project_identity(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory) / "project"
            root.mkdir()
            (root / "pyproject.toml").write_text("", encoding="utf-8")
            engine = LocalProjectDiscoveryEngine()
            scope = DiscoveryScope(roots=(root,))

            first = engine.discover(scope, observed_at=OBSERVED_AT)
            second = engine.discover(scope, observed_at=OBSERVED_AT)

        self.assertEqual(first[0].id, second[0].id)

    def test_rejects_missing_and_file_paths(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            file_path = root / "file.txt"
            file_path.write_text("data", encoding="utf-8")

            with self.assertRaisesRegex(ValueError, "does not exist"):
                ProjectIdentityGenerator.stable_id(root / "missing")
            with self.assertRaisesRegex(ValueError, "must be a directory"):
                ProjectIdentityGenerator.stable_id(file_path)


class ProjectFingerprintGeneratorTests(unittest.TestCase):
    def test_fingerprint_is_repeatable_across_structure_analyses(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory) / "project"
            root.mkdir()
            (root / "main.py").write_text("pass\n", encoding="utf-8")
            project = make_project(root)
            analyzer = ProjectStructureAnalyzer()
            generator = ProjectFingerprintGenerator()

            first = generator.generate(
                analyzer.analyze(project, analyzed_at=OBSERVED_AT),
                generated_at=OBSERVED_AT,
            )
            second = generator.generate(
                analyzer.analyze(project, analyzed_at=OBSERVED_AT),
                generated_at=OBSERVED_AT,
            )

        self.assertTrue(first.matches(second))
        self.assertEqual(first.algorithm, FINGERPRINT_ALGORITHM)
        self.assertEqual(first.artifact_count, 2)

    def test_metadata_change_changes_fingerprint(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory) / "project"
            root.mkdir()
            source = root / "main.py"
            source.write_text("pass\n", encoding="utf-8")
            project = make_project(root)
            analyzer = ProjectStructureAnalyzer()
            generator = ProjectFingerprintGenerator()

            before = generator.generate(analyzer.analyze(project))
            source.write_text("print('changed')\n", encoding="utf-8")
            after = generator.generate(analyzer.analyze(project))

        self.assertFalse(before.matches(after))
        self.assertNotEqual(before.digest, after.digest)

    def test_fingerprint_round_trip_serialization(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory) / "project"
            root.mkdir()
            fingerprint = ProjectFingerprintGenerator().generate(
                ProjectStructureAnalyzer().analyze(make_project(root)),
                generated_at=OBSERVED_AT,
            )

            restored = ProjectFingerprint.from_dict(fingerprint.to_dict())

        self.assertEqual(restored, fingerprint)

    def test_model_rejects_invalid_digest(self) -> None:
        with self.assertRaisesRegex(ValueError, "64-character"):
            ProjectFingerprint(
                project_id="project",
                stable_project_id="12345678-1234-5678-1234-567812345678",
                algorithm=FINGERPRINT_ALGORITHM,
                digest="not-a-digest",
                generated_at=OBSERVED_AT,
                artifact_count=0,
            )

    def test_generator_rejects_naive_timestamp(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory) / "project"
            root.mkdir()
            structure = ProjectStructureAnalyzer().analyze(make_project(root))

            with self.assertRaisesRegex(ValueError, "timezone"):
                ProjectFingerprintGenerator().generate(
                    structure, generated_at=datetime(2026, 8, 23)
                )


if __name__ == "__main__":
    unittest.main()
