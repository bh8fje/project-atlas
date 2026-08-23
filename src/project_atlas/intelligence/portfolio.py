"""Local aggregation of explicitly supplied project intelligence."""

from datetime import datetime, timezone

from project_atlas.domain import Project, ProjectRelationshipGraph, ProjectUnderstanding
from project_atlas.domain.portfolio import MultiProjectIntelligence, ProjectIntelligenceSummary


class MultiProjectIntelligenceService:
    """Build a deterministic portfolio view without discovery or AI calls."""

    def analyze(
        self,
        projects: tuple[Project, ...],
        understandings: tuple[ProjectUnderstanding, ...],
        graph: ProjectRelationshipGraph,
        *,
        generated_at: datetime | None = None,
    ) -> MultiProjectIntelligence:
        if not isinstance(projects, tuple) or any(not isinstance(item, Project) for item in projects):
            raise TypeError("projects must be a tuple of Project values")
        if len(projects) < 2:
            raise ValueError("projects must contain at least two projects")
        if not isinstance(understandings, tuple) or any(not isinstance(item, ProjectUnderstanding) for item in understandings):
            raise TypeError("understandings must be a tuple of ProjectUnderstanding values")
        if not isinstance(graph, ProjectRelationshipGraph):
            raise TypeError("graph must be a ProjectRelationshipGraph")
        project_by_id = {item.id: item for item in projects}
        understanding_by_id = {item.project_id: item for item in understandings}
        if len(project_by_id) != len(projects):
            raise ValueError("project ids must be unique")
        if len(understanding_by_id) != len(understandings):
            raise ValueError("understandings must have unique project ids")
        project_ids = set(project_by_id)
        if set(understanding_by_id) != project_ids:
            raise ValueError("every project must have exactly one understanding")
        if {item.id for item in graph.projects} != project_ids:
            raise ValueError("graph projects must exactly match projects")
        timestamp = generated_at or datetime.now(timezone.utc)
        if not isinstance(timestamp, datetime):
            raise TypeError("generated_at must be a datetime")
        if timestamp.tzinfo is None or timestamp.utcoffset() is None:
            raise ValueError("generated_at must include timezone information")

        relationship_counts = {project_id: 0 for project_id in project_ids}
        for relationship in graph.relationships:
            relationship_counts[relationship.source_project_id] += 1
            relationship_counts[relationship.target_project_id] += 1
        summaries = tuple(
            ProjectIntelligenceSummary(
                project_id=project_id,
                name=project_by_id[project_id].name,
                project_status=project_by_id[project_id].status,
                understanding_status=understanding_by_id[project_id].status,
                risk_count=len(understanding_by_id[project_id].risks),
                relationship_count=relationship_counts[project_id],
                analyzed_at=understanding_by_id[project_id].analyzed_at,
            )
            for project_id in sorted(project_ids)
        )
        return MultiProjectIntelligence(
            generated_at=timestamp,
            projects=summaries,
            shared_risks=self._shared_risks(understandings),
            isolated_project_ids=tuple(sorted(key for key, count in relationship_counts.items() if count == 0)),
            relationship_count=graph.relationship_count,
            source_record_keys=tuple(sorted({key for item in understandings for key in item.source_record_keys})),
        )

    @staticmethod
    def _shared_risks(understandings: tuple[ProjectUnderstanding, ...]) -> tuple[str, ...]:
        projects_by_risk: dict[str, set[str]] = {}
        display_by_risk: dict[str, str] = {}
        for understanding in understandings:
            for risk in understanding.risks:
                key = risk.casefold()
                projects_by_risk.setdefault(key, set()).add(understanding.project_id)
                display_by_risk[key] = min(risk, display_by_risk.get(key, risk))
        return tuple(sorted(display_by_risk[key] for key, projects in projects_by_risk.items() if len(projects) > 1))
