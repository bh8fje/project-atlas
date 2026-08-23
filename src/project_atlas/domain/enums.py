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


class ArtifactType(str, Enum):
    """Classification of an artifact within a software project."""

    FILE = "FILE"
    DIRECTORY = "DIRECTORY"
    DOCUMENT = "DOCUMENT"
    SOURCE_CODE = "SOURCE_CODE"
    CONFIGURATION = "CONFIGURATION"
    UNKNOWN = "UNKNOWN"


class RelationshipType(str, Enum):
    """Semantic relationship between two project assets."""

    CONTAINS = "CONTAINS"
    DEPENDS_ON = "DEPENDS_ON"
    GENERATED_FROM = "GENERATED_FROM"
    UNKNOWN = "UNKNOWN"
