"""Local workspace root domain contracts."""

from collections.abc import Mapping
from dataclasses import dataclass
from datetime import datetime
from typing import Any, Self

from ._validation import parse_datetime, require_aware_datetime, require_non_empty


@dataclass(frozen=True, slots=True)
class WorkspaceRoot:
    """A user-approved local directory and its monitoring preference."""

    id: str
    path: str
    monitoring_enabled: bool
    scan_interval_minutes: int
    added_at: datetime
    last_scanned_at: datetime | None = None

    def __post_init__(self) -> None:
        require_non_empty(self.id, "id")
        require_non_empty(self.path, "path")
        if not isinstance(self.monitoring_enabled, bool):
            raise TypeError("monitoring_enabled must be a boolean")
        if isinstance(self.scan_interval_minutes, bool) or not isinstance(
            self.scan_interval_minutes, int
        ):
            raise TypeError("scan_interval_minutes must be an integer")
        if not 1 <= self.scan_interval_minutes <= 1_440:
            raise ValueError("scan_interval_minutes must be between 1 and 1440")
        require_aware_datetime(self.added_at, "added_at")
        if self.last_scanned_at is not None:
            require_aware_datetime(self.last_scanned_at, "last_scanned_at")
            if self.last_scanned_at < self.added_at:
                raise ValueError("last_scanned_at must not be earlier than added_at")

    def to_dict(self) -> dict[str, str | bool | int | None]:
        """Return a JSON-compatible representation."""

        return {
            "id": self.id,
            "path": self.path,
            "monitoring_enabled": self.monitoring_enabled,
            "scan_interval_minutes": self.scan_interval_minutes,
            "added_at": self.added_at.isoformat(),
            "last_scanned_at": (
                self.last_scanned_at.isoformat()
                if self.last_scanned_at is not None
                else None
            ),
        }

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> Self:
        """Create a validated workspace root from serialized data."""

        last_scanned_at = data.get("last_scanned_at")
        if last_scanned_at is not None:
            last_scanned_at = parse_datetime(last_scanned_at, "last_scanned_at")
        return cls(
            id=require_non_empty(data.get("id"), "id"),
            path=require_non_empty(data.get("path"), "path"),
            monitoring_enabled=data.get("monitoring_enabled"),
            scan_interval_minutes=data.get("scan_interval_minutes"),
            added_at=parse_datetime(data.get("added_at"), "added_at"),
            last_scanned_at=last_scanned_at,
        )
