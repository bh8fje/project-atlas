"""Explicit, read-only observation cycle for Project Atlas."""

from collections import Counter
from datetime import datetime, timezone
from hashlib import sha256

from project_atlas.domain import ChangeType, MultiProjectIntelligence, ProjectChange
from project_atlas.domain.agent import AgentObservationCycle, AgentSignal, AgentSignalSeverity, AgentSignalType


class AutonomousProjectAgent:
    """Turn supplied facts into alerts and suggestions without executing actions."""

    def observe(
        self,
        changes: tuple[ProjectChange, ...],
        portfolio: MultiProjectIntelligence,
        *,
        observed_at: datetime | None = None,
    ) -> AgentObservationCycle:
        if not isinstance(changes, tuple) or any(not isinstance(item, ProjectChange) for item in changes):
            raise TypeError("changes must be a tuple of ProjectChange values")
        if len({item.id for item in changes}) != len(changes):
            raise ValueError("change ids must be unique")
        if not isinstance(portfolio, MultiProjectIntelligence):
            raise TypeError("portfolio must be a MultiProjectIntelligence")
        timestamp = observed_at or datetime.now(timezone.utc)
        if not isinstance(timestamp, datetime):
            raise TypeError("observed_at must be a datetime")
        if timestamp.tzinfo is None or timestamp.utcoffset() is None:
            raise ValueError("observed_at must include timezone information")
        if portfolio.generated_at > timestamp:
            raise ValueError("portfolio cannot be generated after observed_at")
        project_ids = tuple(item.project_id for item in portfolio.projects)
        known_projects = set(project_ids)
        if any(item.project_id not in known_projects for item in changes):
            raise ValueError("changes must reference portfolio projects")
        if any(item.recorded_at > timestamp for item in changes):
            raise ValueError("changes cannot be recorded after observed_at")

        signals = [*self._change_signals(changes)]
        signals.extend(self._risk_signals(portfolio, project_ids))
        recommendations: set[str] = set()
        if changes:
            recommendations.add("Review detected changes before accepting the next project snapshot.")
        if portfolio.shared_risks:
            recommendations.add("Coordinate remediation for risks shared by multiple projects.")
        if portfolio.isolated_project_ids:
            recommendations.add("Confirm whether isolated projects are intentionally independent.")
        source_ids = tuple(sorted((*[item.id for item in changes], *portfolio.source_record_keys)))
        cycle_id = sha256((timestamp.isoformat() + "\n" + "\n".join(source_ids)).encode()).hexdigest()
        return AgentObservationCycle(
            id=cycle_id,
            observed_at=timestamp,
            project_ids=project_ids,
            signals=tuple(sorted(signals, key=lambda item: item.id)),
            recommendations=tuple(sorted(recommendations)),
            observed_change_ids=tuple(sorted(item.id for item in changes)),
            source_record_keys=portfolio.source_record_keys,
        )

    def _change_signals(self, changes: tuple[ProjectChange, ...]) -> tuple[AgentSignal, ...]:
        by_project: dict[str, list[ProjectChange]] = {}
        for change in changes:
            by_project.setdefault(change.project_id, []).append(change)
        signals = []
        for project_id, items in by_project.items():
            counts = Counter(item.change_type.value for item in items)
            summary = ", ".join(f"{key}={counts[key]}" for key in sorted(counts))
            severity = AgentSignalSeverity.WARNING if counts[ChangeType.REMOVED.value] else AgentSignalSeverity.INFO
            source_ids = tuple(sorted(item.id for item in items))
            signals.append(self._signal(AgentSignalType.CHANGE_DETECTED, severity, (project_id,), f"Detected {len(items)} project changes ({summary}).", source_ids))
        return tuple(signals)

    def _risk_signals(self, portfolio: MultiProjectIntelligence, project_ids: tuple[str, ...]) -> tuple[AgentSignal, ...]:
        signals = [self._signal(AgentSignalType.SHARED_RISK, AgentSignalSeverity.WARNING, project_ids, f"Shared risk: {risk}", portfolio.source_record_keys or ("portfolio",)) for risk in portfolio.shared_risks]
        signals.extend(self._signal(AgentSignalType.ISOLATED_PROJECT, AgentSignalSeverity.INFO, (project_id,), "Project has no declared portfolio relationships.", (project_id,)) for project_id in portfolio.isolated_project_ids)
        return tuple(signals)

    @staticmethod
    def _signal(signal_type: AgentSignalType, severity: AgentSignalSeverity, project_ids: tuple[str, ...], message: str, source_ids: tuple[str, ...]) -> AgentSignal:
        ordered_projects = tuple(sorted(set(project_ids)))
        ordered_sources = tuple(sorted(set(source_ids)))
        signal_id = sha256((signal_type.value + "\n" + "\n".join(ordered_projects) + "\n" + message + "\n" + "\n".join(ordered_sources)).encode()).hexdigest()
        return AgentSignal(signal_id, signal_type, severity, ordered_projects, message, ordered_sources)
