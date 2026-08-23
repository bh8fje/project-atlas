"""Loopback-only service for approved directory selection and monitoring."""

import argparse
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
from pathlib import Path
import shutil
import subprocess
import sys
from threading import Event, Thread
from typing import Any, Callable, Protocol
from urllib.parse import urlparse

from project_atlas.application import (
    DEFAULT_SCAN_INTERVAL_MINUTES,
    WorkspaceMonitor,
    WorkspaceRegistry,
    WorkspaceScanService,
    WorkspaceStateStore,
)


DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT = 43821
DEFAULT_ALLOWED_ORIGINS = frozenset(
    {"http://localhost:3000", "http://127.0.0.1:3000"}
)


class DirectoryPicker(Protocol):
    def choose(self, language: str = "zh") -> str | None: ...


class NativeDirectoryPicker:
    """Open the operating system directory chooser without reading files."""

    _PROMPTS = {
        "zh": "选择 Project Atlas 扫描目录",
        "en": "Choose a Project Atlas scan folder",
        "ru": "Выберите папку для сканирования Project Atlas",
        "ko": "Project Atlas 스캔 폴더 선택",
    }

    def choose(self, language: str = "zh") -> str | None:
        prompt = self._PROMPTS.get(language, self._PROMPTS["zh"])
        if sys.platform == "darwin":
            return self._choose_macos(prompt)
        if sys.platform == "win32":
            return self._choose_windows(prompt)
        return self._choose_linux(prompt)

    @staticmethod
    def _choose_macos(prompt: str) -> str | None:
        escaped_prompt = prompt.replace("\\", "\\\\").replace('"', '\\"')
        result = subprocess.run(
            [
                "osascript",
                "-e",
                f'POSIX path of (choose folder with prompt "{escaped_prompt}")',
            ],
            check=False,
            capture_output=True,
            text=True,
        )
        if result.returncode != 0:
            return None
        return result.stdout.strip() or None

    @staticmethod
    def _choose_windows(prompt: str) -> str | None:
        escaped_prompt = prompt.replace("'", "''")
        script = (
            "Add-Type -AssemblyName System.Windows.Forms; "
            "$dialog = New-Object System.Windows.Forms.FolderBrowserDialog; "
            f"$dialog.Description = '{escaped_prompt}'; "
            "if ($dialog.ShowDialog() -eq 'OK') { $dialog.SelectedPath }"
        )
        result = subprocess.run(
            ["powershell", "-NoProfile", "-Command", script],
            check=False,
            capture_output=True,
            text=True,
        )
        if result.returncode != 0:
            return None
        return result.stdout.strip() or None

    @staticmethod
    def _choose_linux(prompt: str) -> str | None:
        executable = shutil.which("zenity")
        if executable is None:
            raise RuntimeError("directory picker requires zenity on this system")
        result = subprocess.run(
            [executable, "--file-selection", "--directory", "--title", prompt],
            check=False,
            capture_output=True,
            text=True,
        )
        if result.returncode != 0:
            return None
        return result.stdout.strip() or None


class WorkspaceController:
    """Translate local UI actions into explicit workspace operations."""

    def __init__(
        self,
        registry: WorkspaceRegistry,
        scan_service: WorkspaceScanService,
        picker: DirectoryPicker | None = None,
    ) -> None:
        self._registry = registry
        self._scan_service = scan_service
        self._picker = picker or NativeDirectoryPicker()

    def list(self) -> dict[str, Any]:
        return {
            "workspaces": [
                {
                    **workspace.to_dict(),
                    "projects": list(self._scan_service.latest_projects(workspace.id)),
                    "last_summary": self._scan_service.latest_summary(workspace.id),
                }
                for workspace in self._registry.list()
            ]
        }

    def select(self, data: dict[str, Any]) -> dict[str, Any]:
        language = data.get("language", "zh")
        if language not in {"zh", "en", "ru", "ko"}:
            raise ValueError("language must be zh, en, ru, or ko")
        selected = self._picker.choose(language)
        if selected is None:
            return {"cancelled": True}
        enabled = data.get("monitoring_enabled", False)
        interval = data.get(
            "scan_interval_minutes", DEFAULT_SCAN_INTERVAL_MINUTES
        )
        workspace = self._registry.add(
            selected,
            monitoring_enabled=enabled,
            scan_interval_minutes=interval,
        )
        workspace = self._registry.set_monitoring(
            workspace.id,
            enabled=enabled,
            scan_interval_minutes=interval,
        )
        report = self._scan_service.scan(workspace.id)
        return {"cancelled": False, "result": report.to_dict()}

    def scan(self, workspace_id: str) -> dict[str, Any]:
        return {"result": self._scan_service.scan(workspace_id).to_dict()}

    def set_monitoring(self, workspace_id: str, data: dict[str, Any]) -> dict[str, Any]:
        enabled = data.get("enabled")
        if not isinstance(enabled, bool):
            raise TypeError("enabled must be a boolean")
        interval = data.get("scan_interval_minutes")
        workspace = self._registry.set_monitoring(
            workspace_id,
            enabled=enabled,
            scan_interval_minutes=interval,
        )
        return {"workspace": workspace.to_dict()}

    def remove(self, workspace_id: str) -> dict[str, bool]:
        self._scan_service.remove(workspace_id)
        return {"removed": True}


def create_handler(
    controller: WorkspaceController,
    *,
    allowed_origins: frozenset[str] = DEFAULT_ALLOWED_ORIGINS,
) -> type[BaseHTTPRequestHandler]:
    """Create a loopback API handler bound to one controller."""

    class WorkspaceRequestHandler(BaseHTTPRequestHandler):
        server_version = "ProjectAtlasLocal/1"

        def do_OPTIONS(self) -> None:  # noqa: N802
            if not self._origin_allowed():
                self._send_error(HTTPStatus.FORBIDDEN, "origin is not allowed")
                return
            self.send_response(HTTPStatus.NO_CONTENT)
            self._cors_headers()
            self.send_header("Access-Control-Allow-Methods", "GET, POST, DELETE, OPTIONS")
            self.send_header("Access-Control-Allow-Headers", "Content-Type")
            self.send_header("Access-Control-Max-Age", "600")
            self.end_headers()

        def do_GET(self) -> None:  # noqa: N802
            if not self._origin_allowed():
                self._send_error(HTTPStatus.FORBIDDEN, "origin is not allowed")
                return
            if urlparse(self.path).path == "/api/workspaces":
                self._run(controller.list)
                return
            self._send_error(HTTPStatus.NOT_FOUND, "endpoint not found")

        def do_POST(self) -> None:  # noqa: N802
            if not self._origin_allowed():
                self._send_error(HTTPStatus.FORBIDDEN, "origin is not allowed")
                return
            path = urlparse(self.path).path
            data = self._read_json()
            if data is None:
                return
            if path == "/api/workspaces/select":
                self._run(lambda: controller.select(data))
                return
            parts = path.strip("/").split("/")
            if len(parts) == 4 and parts[:2] == ["api", "workspaces"]:
                workspace_id, action = parts[2], parts[3]
                if action == "scan":
                    self._run(lambda: controller.scan(workspace_id))
                    return
                if action == "monitoring":
                    self._run(lambda: controller.set_monitoring(workspace_id, data))
                    return
            self._send_error(HTTPStatus.NOT_FOUND, "endpoint not found")

        def do_DELETE(self) -> None:  # noqa: N802
            if not self._origin_allowed():
                self._send_error(HTTPStatus.FORBIDDEN, "origin is not allowed")
                return
            parts = urlparse(self.path).path.strip("/").split("/")
            if len(parts) == 3 and parts[:2] == ["api", "workspaces"]:
                self._run(lambda: controller.remove(parts[2]))
                return
            self._send_error(HTTPStatus.NOT_FOUND, "endpoint not found")

        def log_message(self, format: str, *args: object) -> None:
            return

        def _origin_allowed(self) -> bool:
            origin = self.headers.get("Origin")
            return origin is None or origin in allowed_origins

        def _cors_headers(self) -> None:
            origin = self.headers.get("Origin")
            if origin in allowed_origins:
                self.send_header("Access-Control-Allow-Origin", origin)
                self.send_header("Vary", "Origin")

        def _read_json(self) -> dict[str, Any] | None:
            raw_length = self.headers.get("Content-Length", "0")
            try:
                length = int(raw_length)
            except ValueError:
                self._send_error(HTTPStatus.BAD_REQUEST, "invalid content length")
                return None
            if length > 32_768:
                self._send_error(HTTPStatus.REQUEST_ENTITY_TOO_LARGE, "request is too large")
                return None
            raw = self.rfile.read(length) if length else b"{}"
            try:
                data = json.loads(raw)
            except (UnicodeDecodeError, json.JSONDecodeError):
                self._send_error(HTTPStatus.BAD_REQUEST, "request body must be JSON")
                return None
            if not isinstance(data, dict):
                self._send_error(HTTPStatus.BAD_REQUEST, "request body must be an object")
                return None
            return data

        def _run(self, operation: Callable[[], object]) -> None:
            try:
                result = operation()
            except KeyError as error:
                self._send_error(HTTPStatus.NOT_FOUND, str(error))
            except (TypeError, ValueError, RuntimeError) as error:
                self._send_error(HTTPStatus.BAD_REQUEST, str(error))
            else:
                self._send_json(HTTPStatus.OK, result)

        def _send_json(self, status: HTTPStatus, data: object) -> None:
            payload = json.dumps(data, ensure_ascii=False).encode("utf-8")
            self.send_response(status)
            self._cors_headers()
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(payload)))
            self.send_header("Cache-Control", "no-store")
            self.end_headers()
            self.wfile.write(payload)

        def _send_error(self, status: HTTPStatus, message: str) -> None:
            self._send_json(status, {"error": message})

    return WorkspaceRequestHandler


def _monitor_loop(monitor: WorkspaceMonitor, stop: Event) -> None:
    while not stop.wait(5):
        try:
            monitor.scan_due()
        except (KeyError, OSError, TypeError, ValueError):
            continue


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run the Project Atlas local service")
    parser.add_argument("--host", default=DEFAULT_HOST)
    parser.add_argument("--port", type=int, default=DEFAULT_PORT)
    parser.add_argument(
        "--data-directory",
        type=Path,
        default=Path.home() / ".project-atlas",
    )
    args = parser.parse_args(argv)
    if args.host not in {"127.0.0.1", "localhost"}:
        parser.error("host must be a loopback address")

    data_directory = args.data_directory.expanduser().resolve()
    registry = WorkspaceRegistry(data_directory / "workspaces.json")
    state_store = WorkspaceStateStore(data_directory / "workspace-state.json")
    scan_service = WorkspaceScanService(registry, state_store)
    controller = WorkspaceController(registry, scan_service)
    monitor = WorkspaceMonitor(registry, scan_service)
    stop = Event()
    monitor_thread = Thread(
        target=_monitor_loop, args=(monitor, stop), name="atlas-monitor", daemon=True
    )
    server = ThreadingHTTPServer(
        (args.host, args.port), create_handler(controller)
    )
    monitor_thread.start()
    print(f"Project Atlas local service: http://{args.host}:{args.port}")
    try:
        server.serve_forever(poll_interval=0.5)
    except KeyboardInterrupt:
        pass
    finally:
        stop.set()
        server.server_close()
        monitor_thread.join(timeout=2)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
