"""Auditable observation contracts for the controlled project agent."""

from collections.abc import Mapping
from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum
from typing import Any, Self

from ._validation import parse_datetime, require_aware_datetime, require_non_empty, require_non_negative_int


class AgentSignalType(StrEnum):
    CHANGE_DETECTED = "CHANGE_DETECTED"
    SHARED_RISK = "SHARED_RISK"
    ISOLATED_PROJECT = "ISOLATED_PROJECT"


class AgentSignalSeverity(StrEnum):
    INFO = "INFO"
    WARNING = "WARNING"


@dataclass(frozen=True, slots=True)
class AgentSignal:
    id: str
    signal_type: AgentSignalType
    severity: AgentSignalSeverity
    project_ids: tuple[str, ...]
    message: str
    source_ids: tuple[str, ...]

    def __post_init__(self) -> None:
        require_non_empty(self.id, "id")
        if not isinstance(self.signal_type, AgentSignalType):
            raise TypeError("signal_type must be an AgentSignalType")
        if not isinstance(self.severity, AgentSignalSeverity):
            raise TypeError("severity must be an AgentSignalSeverity")
        self._ordered_strings(self.project_ids, "project_ids", allow_empty=False)
        require_non_empty(self.message, "message")
        self._ordered_strings(self.source_ids, "source_ids", allow_empty=False)

    def to_dict(self) -> dict[str, Any]:
        return {"id": self.id, "signal_type": self.signal_type.value, "severity": self.severity.value, "project_ids": list(self.project_ids), "message": self.message, "source_ids": list(self.source_ids)}

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> Self:
        return cls(
            id=require_non_empty(data.get("id"), "id"),
            signal_type=AgentSignalType(require_non_empty(data.get("signal_type"), "signal_type")),
            severity=AgentSignalSeverity(require_non_empty(data.get("severity"), "severity")),
            project_ids=cls._string_list(data.get("project_ids"), "project_ids"),
            message=require_non_empty(data.get("message"), "message"),
            source_ids=cls._string_list(data.get("source_ids"), "source_ids"),
        )

    @staticmethod
    def _ordered_strings(value: object, field_name: str, *, allow_empty: bool) -> None:
        if not isinstance(value, tuple) or any(not isinstance(item, str) or not item.strip() for item in value):
            raise TypeError(f"{field_name} must be a tuple of non-empty strings")
        if not allow_empty and not value:
            raise ValueError(f"{field_name} must not be empty")
        if value != tuple(sorted(set(value))):
            raise ValueError(f"{field_name} must be unique and ordered")

    @staticmethod
    def _string_list(value: object, field_name: str) -> tuple[str, ...]:
        if not isinstance(value, list):
            raise TypeError(f"{field_name} must be a list")
        return tuple(value)


@dataclass(frozen=True, slots=True)
class AgentObservationCycle:
    id: str
    observed_at: datetime
    project_ids: tuple[str, ...]
    signals: tuple[AgentSignal, ...]
    recommendations: tuple[str, ...]
    observed_change_ids: tuple[str, ...]
    source_record_keys: tuple[str, ...]
    actions_executed: int = 0

    def __post_init__(self) -> None:
        require_non_empty(self.id, "id")
        require_aware_datetime(self.observed_at, "observed_at")
        AgentSignal._ordered_strings(self.project_ids, "project_ids", allow_empty=False)
        if not isinstance(self.signals, tuple) or any(not isinstance(item, AgentSignal) for item in self.signals):
            raise TypeError("signals must be a tuple of AgentSignal values")
        signal_ids = tuple(item.id for item in self.signals)
        if signal_ids != tuple(sorted(set(signal_ids))):
            raise ValueError("signals must have unique ids ordered by id")
        AgentSignal._ordered_strings(self.recommendations, "recommendations", allow_empty=True)
        AgentSignal._ordered_strings(self.observed_change_ids, "observed_change_ids", allow_empty=True)
        AgentSignal._ordered_strings(self.source_record_keys, "source_record_keys", allow_empty=True)
        require_non_negative_int(self.actions_executed, "actions_executed")
        if self.actions_executed != 0:
            raise ValueError("agent observation cycles cannot execute actions")

    def to_dict(self) -> dict[str, Any]:
        return {"id": self.id, "observed_at": self.observed_at.isoformat(), "project_ids": list(self.project_ids), "signals": [item.to_dict() for item in self.signals], "recommendations": list(self.recommendations), "observed_change_ids": list(self.observed_change_ids), "source_record_keys": list(self.source_record_keys), "actions_executed": self.actions_executed}

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> Self:
        raw_signals = data.get("signals")
        if not isinstance(raw_signals, list):
            raise TypeError("signals must be a list")
        return cls(
            id=require_non_empty(data.get("id"), "id"),
            observed_at=parse_datetime(data.get("observed_at"), "observed_at"),
            project_ids=AgentSignal._string_list(data.get("project_ids"), "project_ids"),
            signals=tuple(AgentSignal.from_dict(item) for item in raw_signals),
            recommendations=AgentSignal._string_list(data.get("recommendations"), "recommendations"),
            observed_change_ids=AgentSignal._string_list(data.get("observed_change_ids"), "observed_change_ids"),
            source_record_keys=AgentSignal._string_list(data.get("source_record_keys"), "source_record_keys"),
            actions_executed=require_non_negative_int(data.get("actions_executed"), "actions_executed"),
        )
