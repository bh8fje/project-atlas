"""Public domain contracts for Project Atlas."""

from .asset import AssetRelationship, ProjectArtifact
from .ai_context import AIContext
from .enums import (
    ArtifactType,
    ChangeType,
    HistoryEventType,
    KnowledgeRecordType,
    ProjectRelationshipType,
    ProjectStatus,
    RelationshipType,
    TaskStatus,
)
from .fingerprint import ProjectFingerprint
from .graph import ProjectRelationship, ProjectRelationshipGraph
from .history import ProjectChange, ProjectHistoryEvent, ProjectSnapshot
from .knowledge import KnowledgeRecord
from .project import Project
from .query import KnowledgeQuery, KnowledgeQueryResult
from .repository import Repository
from .snapshot import RepositorySnapshot
from .structure import ProjectStructure
from .task import Task
from .timeline import ProjectTimeline

__all__ = [
    "AIContext",
    "ArtifactType",
    "AssetRelationship",
    "ChangeType",
    "HistoryEventType",
    "KnowledgeRecord",
    "KnowledgeRecordType",
    "KnowledgeQuery",
    "KnowledgeQueryResult",
    "Project",
    "ProjectArtifact",
    "ProjectChange",
    "ProjectFingerprint",
    "ProjectHistoryEvent",
    "ProjectRelationship",
    "ProjectRelationshipGraph",
    "ProjectRelationshipType",
    "ProjectSnapshot",
    "ProjectStatus",
    "ProjectStructure",
    "ProjectTimeline",
    "RelationshipType",
    "Repository",
    "RepositorySnapshot",
    "Task",
    "TaskStatus",
]
