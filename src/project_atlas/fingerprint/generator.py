"""Stable local identity and metadata fingerprint generation."""

from datetime import datetime, timezone
from hashlib import sha256
import json
from pathlib import Path
from uuid import NAMESPACE_URL, uuid5

from project_atlas.domain import (
    ArtifactType,
    ProjectArtifact,
    ProjectFingerprint,
    ProjectStructure,
)


FINGERPRINT_ALGORITHM = "sha256-metadata-v1"


class ProjectIdentityGenerator:
    """Generate a stable local UUID from a canonical project path."""

    @staticmethod
    def stable_id(path: str | Path) -> str:
        """Return a deterministic UUID for an existing project directory."""

        if not isinstance(path, (str, Path)):
            raise TypeError("path must be a string or Path")
        if isinstance(path, str) and not path.strip():
            raise ValueError("path must not be empty")
        canonical_path = Path(path).expanduser().resolve()
        if not canonical_path.exists():
            raise ValueError(f"project path does not exist: {canonical_path}")
        if not canonical_path.is_dir():
            raise ValueError(f"project path must be a directory: {canonical_path}")
        return str(uuid5(NAMESPACE_URL, canonical_path.as_uri()))


class ProjectFingerprintGenerator:
    """Generate versioned fingerprints from project structure metadata."""

    def generate(
        self,
        structure: ProjectStructure,
        *,
        generated_at: datetime | None = None,
    ) -> ProjectFingerprint:
        """Generate a fingerprint without reading file contents."""

        if not isinstance(structure, ProjectStructure):
            raise TypeError("structure must be a ProjectStructure")
        timestamp = generated_at or datetime.now(timezone.utc)
        if not isinstance(timestamp, datetime):
            raise TypeError("generated_at must be a datetime")
        if timestamp.tzinfo is None or timestamp.utcoffset() is None:
            raise ValueError("generated_at must include timezone information")

        root = Path(structure.root_path).expanduser().resolve()
        stable_project_id = ProjectIdentityGenerator.stable_id(root)
        descriptors = [
            self._artifact_descriptor(artifact, root=root)
            for artifact in structure.artifacts
        ]
        descriptors.sort(key=lambda item: item["path"])
        canonical_data = json.dumps(
            descriptors,
            ensure_ascii=False,
            separators=(",", ":"),
            sort_keys=True,
        ).encode("utf-8")

        return ProjectFingerprint(
            project_id=structure.project_id,
            stable_project_id=stable_project_id,
            algorithm=FINGERPRINT_ALGORITHM,
            digest=sha256(canonical_data).hexdigest(),
            generated_at=timestamp,
            artifact_count=structure.artifact_count,
        )

    @staticmethod
    def _artifact_descriptor(artifact: object, *, root: Path) -> dict[str, object]:
        if not isinstance(artifact, ProjectArtifact):
            raise TypeError("structure artifacts must be ProjectArtifact values")
        path = Path(artifact.path).expanduser().resolve()
        try:
            relative_path = path.relative_to(root)
        except ValueError as error:
            raise ValueError("artifact path must be contained by the project root") from error
        try:
            metadata = path.stat()
        except OSError as error:
            raise ValueError(f"unable to read artifact metadata: {path}") from error

        return {
            "path": relative_path.as_posix() or ".",
            "type": artifact.artifact_type.value,
            "size": 0 if artifact.artifact_type is ArtifactType.DIRECTORY else metadata.st_size,
            "mtime_ns": metadata.st_mtime_ns,
        }
