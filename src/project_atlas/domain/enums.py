"""Lifecycle states used by the Project Atlas domain model."""

from enum import Enum


class ProjectStatus(str, Enum):
    """Lifecycle state of a software project asset."""

    INITIALIZING = "INITIALIZING"
    ACTIVE = "ACTIVE"
    PAUSED = "PAUSED"
    ARCHIVED = "ARCHIVED"
    UNKNOWN = "UNKNOWN"


class TaskStatus(str, Enum):
    """Lifecycle state of an engineering task."""

    PLANNED = "PLANNED"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    BLOCKED = "BLOCKED"
    CANCELLED = "CANCELLED"
