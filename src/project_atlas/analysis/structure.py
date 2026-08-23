"""Bounded project structure and technology analysis."""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4

from project_atlas.discovery import DEFAULT_EXCLUDED_DIRECTORIES
from project_atlas.domain import (
    ArtifactType,
    AssetRelationship,
    Project,
    ProjectArtifact,
    ProjectStructure,
    RelationshipType,
)


SOURCE_CODE_EXTENSIONS = frozenset(
    {
        ".c",
        ".cc",
        ".cpp",
        ".cs",
        ".dart",
        ".go",
        ".h",
        ".hpp",
        ".java",
        ".js",
        ".jsx",
        ".kt",
        ".kts",
        ".php",
        ".py",
        ".rb",
        ".rs",
        ".sh",
        ".swift",
        ".ts",
        ".tsx",
    }
)

DOCUMENT_EXTENSIONS = frozenset({".md", ".rst", ".txt"})

CONFIGURATION_NAMES = frozenset(
    {
        ".env",
        "build.gradle",
        "cargo.toml",
        "gemfile",
        "go.mod",
        "package.json",
        "pom.xml",
        "pubspec.yaml",
        "pyproject.toml",
        "requirements.txt",
        "setup.cfg",
        "tox.ini",
        "tsconfig.json",
    }
)

TECHNOLOGY_MARKERS: dict[str, frozenset[str]] = {
    "Dart": frozenset({"pubspec.yaml"}),
    "Go": frozenset({"go.mod"}),
    "Java": frozenset({"build.gradle", "pom.xml"}),
    "Node.js": frozenset({"package.json"}),
    "Python": frozenset(
        {"pyproject.toml", "requirements.txt", "setup.cfg", "tox.ini"}
    ),
    "Ruby": frozenset({"gemfile"}),
    "Rust": frozenset({"cargo.toml"}),
    "TypeScript": frozenset({"tsconfig.json"}),
}

TECHNOLOGY_EXTENSIONS: dict[str, frozenset[str]] = {
    "C/C++": frozenset({".c", ".cc", ".cpp", ".h", ".hpp"}),
    "C#": frozenset({".cs"}),
    "Dart": frozenset({".dart"}),
    "Go": frozenset({".go"}),
    "Java": frozenset({".java"}),
    "JavaScript": frozenset({".js", ".jsx"}),
    "Kotlin": frozenset({".kt", ".kts"}),
    "PHP": frozenset({".php"}),
    "Python": frozenset({".py"}),
    "Ruby": frozenset({".rb"}),
    "Rust": frozenset({".rs"}),
    "Shell": frozenset({".sh"}),
    "Swift": frozenset({".swift"}),
    "TypeScript": frozenset({".ts", ".tsx"}),
}


@dataclass(frozen=True, slots=True)
class StructureAnalysisScope:
    """Limits for one project structure analysis."""

    max_depth: int = 8
    max_artifacts: int = 10_000
    excluded_directories: frozenset[str] = field(
        default_factory=lambda: DEFAULT_EXCLUDED_DIRECTORIES
    )

    def __post_init__(self) -> None:
        for value, field_name in (
            (self.max_depth, "max_depth"),
            (self.max_artifacts, "max_artifacts"),
        ):
            if isinstance(value, bool) or not isinstance(value, int):
                raise TypeError(f"{field_name} must be an integer")
        if self.max_depth < 0:
            raise ValueError("max_depth must not be negative")
        if self.max_artifacts < 1:
            raise ValueError("max_artifacts must be positive")


class ProjectStructureAnalyzer:
    """Describe project composition without reading file contents."""

    def analyze(
        self,
        project: Project,
        *,
        scope: StructureAnalysisScope | None = None,
        analyzed_at: datetime | None = None,
    ) -> ProjectStructure:
        """Analyze one declared project directory within explicit limits."""

        if not isinstance(project, Project):
            raise TypeError("project must be a Project")
        active_scope = scope or StructureAnalysisScope()
        if not isinstance(active_scope, StructureAnalysisScope):
            raise TypeError("scope must be a StructureAnalysisScope")
        timestamp = analyzed_at or datetime.now(timezone.utc)
        if not isinstance(timestamp, datetime):
            raise TypeError("analyzed_at must be a datetime")
        if timestamp.tzinfo is None or timestamp.utcoffset() is None:
            raise ValueError("analyzed_at must include timezone information")

        root = Path(project.path).expanduser().resolve()
        if not root.exists():
            raise ValueError(f"project path does not exist: {root}")
        if not root.is_dir():
            raise ValueError(f"project path must be a directory: {root}")

        artifacts: list[ProjectArtifact] = []
        relationships: list[AssetRelationship] = []
        technologies: set[str] = set()
        pending: list[tuple[Path, int, str]] = [(root, 0, project.id)]

        while pending:
            path, depth, parent_id = pending.pop()
            if path.is_symlink():
                continue
            artifact = self._to_artifact(path)
            artifacts.append(artifact)
            if len(artifacts) > active_scope.max_artifacts:
                raise ValueError("project structure exceeds max_artifacts")
            relationships.append(
                AssetRelationship(
                    source_id=parent_id,
                    target_id=artifact.id,
                    relationship_type=RelationshipType.CONTAINS,
                )
            )
            self._detect_technologies(path, technologies)

            if not path.is_dir() or depth >= active_scope.max_depth:
                continue
            children = self._children(
                path, excluded=active_scope.excluded_directories
            )
            pending.extend(
                (child, depth + 1, artifact.id) for child in reversed(children)
            )

        artifacts.sort(key=lambda item: item.path)
        relationships.sort(key=lambda item: (item.source_id, item.target_id))
        return ProjectStructure(
            project_id=project.id,
            root_path=str(root),
            analyzed_at=timestamp,
            artifacts=tuple(artifacts),
            relationships=tuple(relationships),
            technologies=tuple(sorted(technologies)),
        )

    @staticmethod
    def _children(
        directory: Path, *, excluded: frozenset[str]
    ) -> tuple[Path, ...]:
        try:
            children = (
                child
                for child in directory.iterdir()
                if child.name not in excluded and not child.is_symlink()
            )
            return tuple(sorted(children, key=lambda item: item.name))
        except OSError:
            return ()

    @staticmethod
    def _to_artifact(path: Path) -> ProjectArtifact:
        try:
            metadata = path.stat()
        except OSError as error:
            raise ValueError(f"unable to read project artifact metadata: {path}") from error

        updated_at = datetime.fromtimestamp(metadata.st_mtime, tz=timezone.utc)
        created_timestamp = getattr(metadata, "st_birthtime", metadata.st_ctime)
        created_at = datetime.fromtimestamp(
            min(created_timestamp, metadata.st_mtime), tz=timezone.utc
        )
        return ProjectArtifact(
            id=str(uuid4()),
            name=path.name or path.anchor,
            path=str(path),
            artifact_type=ProjectStructureAnalyzer._classify(path),
            created_at=created_at,
            updated_at=updated_at,
        )

    @staticmethod
    def _classify(path: Path) -> ArtifactType:
        if path.is_dir():
            return ArtifactType.DIRECTORY
        lowered_name = path.name.lower()
        if lowered_name in CONFIGURATION_NAMES:
            return ArtifactType.CONFIGURATION
        if path.suffix.lower() in SOURCE_CODE_EXTENSIONS:
            return ArtifactType.SOURCE_CODE
        if path.suffix.lower() in DOCUMENT_EXTENSIONS:
            return ArtifactType.DOCUMENT
        if path.is_file():
            return ArtifactType.FILE
        return ArtifactType.UNKNOWN

    @staticmethod
    def _detect_technologies(path: Path, technologies: set[str]) -> None:
        if not path.is_file():
            return
        lowered_name = path.name.lower()
        for technology, markers in TECHNOLOGY_MARKERS.items():
            if lowered_name in markers:
                technologies.add(technology)
        extension = path.suffix.lower()
        for technology, extensions in TECHNOLOGY_EXTENSIONS.items():
            if extension in extensions:
                technologies.add(technology)
