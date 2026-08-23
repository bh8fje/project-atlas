"""Engineering task domain model and lifecycle rules."""

from collections.abc import Mapping
from dataclasses import dataclass, replace
from datetime import datetime, timezone
from typing import Any, ClassVar, Self

from ._validation import parse_datetime, require_aware_datetime, require_non_empty
from .enums import TaskStatus


@dataclass(frozen=True, slots=True)
class Task:
    """A single, validated unit of engineering work."""

    id: str
    name: str
    description: str
    status: TaskStatus
    created_at: datetime
    completed_at: datetime | None = None

    _ALLOWED_TRANSITIONS: ClassVar[dict[TaskStatus, frozenset[TaskStatus]]] = {
        TaskStatus.PLANNED: frozenset(
            {TaskStatus.IN_PROGRESS, TaskStatus.BLOCKED, TaskStatus.CANCELLED}
        ),
        TaskStatus.IN_PROGRESS: frozenset(
            {TaskStatus.COMPLETED, TaskStatus.BLOCKED, TaskStatus.CANCELLED}
        ),
        TaskStatus.BLOCKED: frozenset(
            {TaskStatus.IN_PROGRESS, TaskStatus.CANCELLED}
        ),
        TaskStatus.COMPLETED: frozenset(),
        TaskStatus.CANCELLED: frozenset(),
    }

    def __post_init__(self) -> None:
        require_non_empty(self.id, "id")
        require_non_empty(self.name, "name")
        require_non_empty(self.description, "description")
        if not isinstance(self.status, TaskStatus):
            raise TypeError("status must be a TaskStatus")
        require_aware_datetime(self.created_at, "created_at")

        if self.completed_at is not None:
            require_aware_datetime(self.completed_at, "completed_at")
            if self.completed_at < self.created_at:
                raise ValueError("completed_at must not be earlier than created_at")

        if self.status is TaskStatus.COMPLETED and self.completed_at is None:
            raise ValueError("a completed task must define completed_at")
        if self.status is not TaskStatus.COMPLETED and self.completed_at is not None:
            raise ValueError("completed_at is only valid for a completed task")

    def transition_to(
        self, new_status: TaskStatus, *, at: datetime | None = None
    ) -> Self:
        """Return a new task after applying a valid lifecycle transition."""

        if not isinstance(new_status, TaskStatus):
            raise TypeError("new_status must be a TaskStatus")
        if new_status not in self._ALLOWED_TRANSITIONS[self.status]:
            raise ValueError(
                f"invalid task transition: {self.status.value} -> {new_status.value}"
            )

        completed_at = None
        if new_status is TaskStatus.COMPLETED:
            completed_at = at or datetime.now(timezone.utc)
            require_aware_datetime(completed_at, "at")

        return replace(self, status=new_status, completed_at=completed_at)

    def to_dict(self) -> dict[str, str | None]:
        """Return a JSON-compatible representation of the task."""

        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "status": self.status.value,
            "created_at": self.created_at.isoformat(),
            "completed_at": (
                self.completed_at.isoformat() if self.completed_at is not None else None
            ),
        }

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> Self:
        """Create a validated task from its serialized representation."""

        raw_completed_at = data.get("completed_at")
        completed_at = (
            None
            if raw_completed_at is None
            else parse_datetime(raw_completed_at, "completed_at")
        )
        return cls(
            id=require_non_empty(data.get("id"), "id"),
            name=require_non_empty(data.get("name"), "name"),
            description=require_non_empty(data.get("description"), "description"),
            status=TaskStatus(require_non_empty(data.get("status"), "status")),
            created_at=parse_datetime(data.get("created_at"), "created_at"),
            completed_at=completed_at,
        )
