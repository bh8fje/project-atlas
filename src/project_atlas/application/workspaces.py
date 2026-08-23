"""Local workspace registration, scanning, and scheduled checks."""

from collections.abc import Iterable
from dataclasses import dataclass, replace
from datetime import datetime, timedelta, timezone
import json
from pathlib import Path
from threading import RLock
from typing import Any
from uuid import NAMESPACE_URL, uuid5

from project_atlas.analysis import ProjectStructureAnalyzer
from project_atlas.discovery import DiscoveryScope, LocalProjectDiscoveryEngine
from project_atlas.domain import WorkspaceRoot
from project_atlas.fingerprint import ProjectFingerprintGenerator


DEFAULT_SCAN_INTERVAL_MINUTES = 15


def _atomic_json_write(path: Path, data: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(f"{path.suffix}.tmp")
    temporary.write_text(
        json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True),
        encoding="utf-8",
    )
    temporary.replace(path)


class WorkspaceRegistry:
    """Persist user-approved roots in one explicit local JSON file."""

    def __init__(self, path: str | Path) -> None:
        self._path = Path(path).expanduser().resolve()
        self._lock = RLock()

    @property
    def path(self) -> Path:
        return self._path

    def list(self) -> tuple[WorkspaceRoot, ...]:
        with self._lock:
            return tuple(sorted(self._load(), key=lambda item: item.path))

    def get(self, workspace_id: str) -> WorkspaceRoot:
        for workspace in self.list():
            if workspace.id == workspace_id:
                return workspace
        raise KeyError(f"unknown workspace: {workspace_id}")

    def add(
        self,
        path: str | Path,
        *,
        monitoring_enabled: bool = False,
        scan_interval_minutes: int = DEFAULT_SCAN_INTERVAL_MINUTES,
        added_at: datetime | None = None,
    ) -> WorkspaceRoot:
        canonical = self._canonical_directory(path)
        timestamp = added_at or datetime.now(timezone.utc)
        workspace = WorkspaceRoot(
            id=str(uuid5(NAMESPACE_URL, canonical.as_uri())),
            path=str(canonical),
            monitoring_enabled=monitoring_enabled,
            scan_interval_minutes=scan_interval_minutes,
            added_at=timestamp,
        )
        with self._lock:
            workspaces = {item.id: item for item in self._load()}
            existing = workspaces.get(workspace.id)
            if existing is not None:
                return existing
            workspaces[workspace.id] = workspace
            self._save(workspaces.values())
        return workspace

    def set_monitoring(
        self,
        workspace_id: str,
        *,
        enabled: bool,
        scan_interval_minutes: int | None = None,
    ) -> WorkspaceRoot:
        with self._lock:
            workspaces = {item.id: item for item in self._load()}
            try:
                current = workspaces[workspace_id]
            except KeyError as error:
                raise KeyError(f"unknown workspace: {workspace_id}") from error
            updated = replace(
                current,
                monitoring_enabled=enabled,
                scan_interval_minutes=(
                    scan_interval_minutes
                    if scan_interval_minutes is not None
                    else current.scan_interval_minutes
                ),
            )
            workspaces[workspace_id] = updated
            self._save(workspaces.values())
            return updated

    def mark_scanned(self, workspace_id: str, scanned_at: datetime) -> WorkspaceRoot:
        with self._lock:
            workspaces = {item.id: item for item in self._load()}
            try:
                current = workspaces[workspace_id]
            except KeyError as error:
                raise KeyError(f"unknown workspace: {workspace_id}") from error
            updated = replace(current, last_scanned_at=scanned_at)
            workspaces[workspace_id] = updated
            self._save(workspaces.values())
            return updated

    def remove(self, workspace_id: str) -> None:
        with self._lock:
            workspaces = {item.id: item for item in self._load()}
            if workspace_id not in workspaces:
                raise KeyError(f"unknown workspace: {workspace_id}")
            del workspaces[workspace_id]
            self._save(workspaces.values())

    def _load(self) -> tuple[WorkspaceRoot, ...]:
        if not self._path.exists():
            return ()
        raw = json.loads(self._path.read_text(encoding="utf-8"))
        if not isinstance(raw, dict) or not isinstance(raw.get("workspaces"), list):
            raise ValueError("workspace registry must contain a workspaces list")
        return tuple(WorkspaceRoot.from_dict(item) for item in raw["workspaces"])

    def _save(self, workspaces: Iterable[WorkspaceRoot]) -> None:
        ordered = sorted(workspaces, key=lambda item: item.path)
        _atomic_json_write(
            self._path,
            {"version": 1, "workspaces": [item.to_dict() for item in ordered]},
        )

    @staticmethod
    def _canonical_directory(path: str | Path) -> Path:
        if not isinstance(path, (str, Path)):
            raise TypeError("workspace path must be a string or Path")
        if isinstance(path, str) and not path.strip():
            raise ValueError("workspace path must not be empty")
        canonical = Path(path).expanduser().resolve()
        if not canonical.exists():
            raise ValueError(f"workspace path does not exist: {canonical}")
        if not canonical.is_dir():
            raise ValueError(f"workspace path must be a directory: {canonical}")
        return canonical


class WorkspaceStateStore:
    """Persist lightweight project fingerprints for change checks."""

    def __init__(self, path: str | Path) -> None:
        self._path = Path(path).expanduser().resolve()
        self._lock = RLock()

    def get(self, workspace_id: str) -> dict[str, dict[str, Any]]:
        with self._lock:
            workspace_state = self._load().get(workspace_id, {})
            projects = workspace_state.get("projects", workspace_state)
            return dict(projects) if isinstance(projects, dict) else {}

    def get_summary(self, workspace_id: str) -> dict[str, int]:
        with self._lock:
            workspace_state = self._load().get(workspace_id, {})
            summary = workspace_state.get("last_summary", {})
            return dict(summary) if isinstance(summary, dict) else {}

    def put(
        self,
        workspace_id: str,
        projects: dict[str, dict[str, Any]],
        *,
        summary: dict[str, int],
    ) -> None:
        with self._lock:
            state = self._load()
            state[workspace_id] = {"projects": projects, "last_summary": summary}
            _atomic_json_write(self._path, {"version": 1, "workspaces": state})

    def remove(self, workspace_id: str) -> None:
        with self._lock:
            state = self._load()
            state.pop(workspace_id, None)
            _atomic_json_write(self._path, {"version": 1, "workspaces": state})

    def _load(self) -> dict[str, dict[str, Any]]:
        if not self._path.exists():
            return {}
        raw = json.loads(self._path.read_text(encoding="utf-8"))
        if not isinstance(raw, dict) or not isinstance(raw.get("workspaces"), dict):
            raise ValueError("workspace state must contain a workspaces object")
        return raw["workspaces"]


@dataclass(frozen=True, slots=True)
class WorkspaceScanReport:
    workspace: WorkspaceRoot
    projects: tuple[dict[str, Any], ...]
    added_project_ids: tuple[str, ...]
    changed_project_ids: tuple[str, ...]
    removed_project_ids: tuple[str, ...]

    def to_dict(self) -> dict[str, Any]:
        return {
            "workspace": self.workspace.to_dict(),
            "projects": list(self.projects),
            "summary": {
                "project_count": len(self.projects),
                "added": len(self.added_project_ids),
                "changed": len(self.changed_project_ids),
                "removed": len(self.removed_project_ids),
            },
        }


class WorkspaceScanService:
    """Reuse discovery and fingerprints to check one approved directory."""

    def __init__(
        self,
        registry: WorkspaceRegistry,
        state_store: WorkspaceStateStore,
    ) -> None:
        self._registry = registry
        self._state_store = state_store
        self._discovery = LocalProjectDiscoveryEngine()
        self._analyzer = ProjectStructureAnalyzer()
        self._fingerprints = ProjectFingerprintGenerator()
        self._lock = RLock()

    def scan(
        self, workspace_id: str, *, scanned_at: datetime | None = None
    ) -> WorkspaceScanReport:
        timestamp = scanned_at or datetime.now(timezone.utc)
        with self._lock:
            workspace = self._registry.get(workspace_id)
            projects = self._discovery.discover(
                DiscoveryScope(roots=(workspace.path,)), observed_at=timestamp
            )
            previous = self._state_store.get(workspace_id)
            current: dict[str, dict[str, Any]] = {}
            project_rows: list[dict[str, Any]] = []
            added: list[str] = []
            changed: list[str] = []

            for project in projects:
                structure = self._analyzer.analyze(project, analyzed_at=timestamp)
                fingerprint = self._fingerprints.generate(
                    structure, generated_at=timestamp
                )
                row = {
                    "id": project.id,
                    "name": project.name,
                    "path": project.path,
                    "artifact_count": structure.artifact_count,
                    "technologies": list(structure.technologies),
                    "fingerprint": fingerprint.digest,
                }
                old = previous.get(project.id)
                if old is None:
                    status = "added"
                    added.append(project.id)
                elif old.get("fingerprint") != fingerprint.digest:
                    status = "changed"
                    changed.append(project.id)
                else:
                    status = "unchanged"
                project_rows.append({**row, "change_status": status})
                current[project.id] = {**row, "change_status": status}

            removed = sorted(set(previous) - set(current))
            project_rows.sort(key=lambda item: (item["name"], item["path"]))
            summary = {
                "project_count": len(project_rows),
                "added": len(added),
                "changed": len(changed),
                "removed": len(removed),
            }
            self._state_store.put(workspace_id, current, summary=summary)
            updated_workspace = self._registry.mark_scanned(workspace_id, timestamp)
            return WorkspaceScanReport(
                workspace=updated_workspace,
                projects=tuple(project_rows),
                added_project_ids=tuple(sorted(added)),
                changed_project_ids=tuple(sorted(changed)),
                removed_project_ids=tuple(removed),
            )

    def latest_projects(self, workspace_id: str) -> tuple[dict[str, Any], ...]:
        rows = self._state_store.get(workspace_id).values()
        return tuple(
            sorted(
                (dict(row) for row in rows),
                key=lambda item: (item["name"], item["path"]),
            )
        )

    def latest_summary(self, workspace_id: str) -> dict[str, int]:
        return {
            "project_count": 0,
            "added": 0,
            "changed": 0,
            "removed": 0,
            **self._state_store.get_summary(workspace_id),
        }

    def remove(self, workspace_id: str) -> None:
        with self._lock:
            self._registry.remove(workspace_id)
            self._state_store.remove(workspace_id)


class WorkspaceMonitor:
    """Run due checks only while the explicit local service is active."""

    def __init__(
        self, registry: WorkspaceRegistry, scan_service: WorkspaceScanService
    ) -> None:
        self._registry = registry
        self._scan_service = scan_service

    def scan_due(self, *, now: datetime | None = None) -> tuple[WorkspaceScanReport, ...]:
        timestamp = now or datetime.now(timezone.utc)
        reports: list[WorkspaceScanReport] = []
        for workspace in self._registry.list():
            if not workspace.monitoring_enabled:
                continue
            due_at = (
                workspace.last_scanned_at
                + timedelta(minutes=workspace.scan_interval_minutes)
                if workspace.last_scanned_at is not None
                else timestamp
            )
            if due_at <= timestamp:
                reports.append(self._scan_service.scan(workspace.id, scanned_at=timestamp))
        return tuple(reports)
