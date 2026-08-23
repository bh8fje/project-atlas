"""Bounded local project discovery without project analysis."""

from collections.abc import Iterable
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path

from project_atlas.domain import Project, ProjectStatus
from project_atlas.fingerprint import ProjectIdentityGenerator


DEFAULT_PROJECT_MARKERS = frozenset(
    {".git", "Cargo.toml", "go.mod", "package.json", "pyproject.toml"}
)

DEFAULT_EXCLUDED_DIRECTORIES = frozenset(
    {
        ".git",
        ".venv",
        "__pycache__",
        "build",
        "dist",
        "node_modules",
        "venv",
    }
)


@dataclass(frozen=True, slots=True)
class DiscoveryScope:
    """Explicit boundaries for one local discovery operation."""

    roots: tuple[str | Path, ...]
    max_depth: int = 4
    excluded_directories: frozenset[str] = field(
        default_factory=lambda: DEFAULT_EXCLUDED_DIRECTORIES
    )

    def __post_init__(self) -> None:
        if not self.roots:
            raise ValueError("roots must contain at least one directory")
        if isinstance(self.max_depth, bool) or not isinstance(self.max_depth, int):
            raise TypeError("max_depth must be an integer")
        if self.max_depth < 0:
            raise ValueError("max_depth must not be negative")
        if not isinstance(self.excluded_directories, frozenset):
            raise TypeError("excluded_directories must be a frozenset")
        if any(not isinstance(name, str) or not name for name in self.excluded_directories):
            raise ValueError("excluded directory names must be non-empty strings")


class LocalProjectDiscoveryEngine:
    """Discover project roots from explicit local directory scopes."""

    def __init__(self, markers: Iterable[str] = DEFAULT_PROJECT_MARKERS) -> None:
        normalized_markers = frozenset(markers)
        if not normalized_markers:
            raise ValueError("markers must not be empty")
        if any(not isinstance(marker, str) or not marker for marker in normalized_markers):
            raise ValueError("markers must be non-empty strings")
        self._markers = normalized_markers

    @property
    def markers(self) -> frozenset[str]:
        """Return the immutable project marker set."""

        return self._markers

    def discover(
        self, scope: DiscoveryScope, *, observed_at: datetime | None = None
    ) -> tuple[Project, ...]:
        """Discover project roots without inspecting project contents."""

        if not isinstance(scope, DiscoveryScope):
            raise TypeError("scope must be a DiscoveryScope")
        timestamp = observed_at or datetime.now(timezone.utc)
        if not isinstance(timestamp, datetime):
            raise TypeError("observed_at must be a datetime")
        if timestamp.tzinfo is None or timestamp.utcoffset() is None:
            raise ValueError("observed_at must include timezone information")

        roots = tuple(self._resolve_root(root) for root in scope.roots)
        discovered_paths: set[Path] = set()
        visited_paths: set[Path] = set()

        for root in roots:
            self._discover_from_root(
                root,
                scope=scope,
                discovered_paths=discovered_paths,
                visited_paths=visited_paths,
            )

        return tuple(
            self._to_project(path, observed_at=timestamp)
            for path in sorted(discovered_paths, key=lambda item: str(item))
        )

    def _discover_from_root(
        self,
        root: Path,
        *,
        scope: DiscoveryScope,
        discovered_paths: set[Path],
        visited_paths: set[Path],
    ) -> None:
        pending: list[tuple[Path, int]] = [(root, 0)]

        while pending:
            current, depth = pending.pop()
            resolved = current.resolve()
            if resolved in visited_paths:
                continue
            visited_paths.add(resolved)

            if self._is_project_root(resolved):
                discovered_paths.add(resolved)
                continue
            if depth >= scope.max_depth:
                continue

            children = self._child_directories(
                resolved, excluded=scope.excluded_directories
            )
            pending.extend((child, depth + 1) for child in reversed(children))

    def _is_project_root(self, directory: Path) -> bool:
        try:
            child_names = {child.name for child in directory.iterdir()}
        except OSError:
            return False
        return not self._markers.isdisjoint(child_names)

    @staticmethod
    def _child_directories(
        directory: Path, *, excluded: frozenset[str]
    ) -> tuple[Path, ...]:
        try:
            children = (
                child
                for child in directory.iterdir()
                if child.name not in excluded
                and not child.is_symlink()
                and child.is_dir()
            )
            return tuple(sorted(children, key=lambda item: item.name))
        except OSError:
            return ()

    @staticmethod
    def _resolve_root(root: str | Path) -> Path:
        if not isinstance(root, (str, Path)):
            raise TypeError("each discovery root must be a string or Path")
        if isinstance(root, str) and not root.strip():
            raise ValueError("discovery roots must not be empty")

        path = Path(root).expanduser().resolve()
        if not path.exists():
            raise ValueError(f"discovery root does not exist: {path}")
        if not path.is_dir():
            raise ValueError(f"discovery root must be a directory: {path}")
        return path

    @staticmethod
    def _to_project(path: Path, *, observed_at: datetime) -> Project:
        return Project(
            id=ProjectIdentityGenerator.stable_id(path),
            name=path.name or path.anchor,
            path=str(path),
            created_at=observed_at,
            updated_at=observed_at,
            status=ProjectStatus.ACTIVE,
        )
