"""Validated contracts for explicit Project Atlas commands."""

from collections.abc import Mapping
from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum
import json
from types import MappingProxyType
from typing import Any, Self

from ._validation import parse_datetime, require_aware_datetime, require_non_empty


class CommandEffect(StrEnum):
    """Whether a command can change state."""

    READ_ONLY = "READ_ONLY"
    MUTATING = "MUTATING"


class CommandStatus(StrEnum):
    """Auditable command completion state."""

    SUCCEEDED = "SUCCEEDED"
    REJECTED = "REJECTED"


def _json_object(value: object, field_name: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        raise TypeError(f"{field_name} must be a mapping")
    copied = dict(value)
    if any(not isinstance(key, str) for key in copied):
        raise TypeError(f"{field_name} keys must be strings")
    try:
        normalized = json.loads(json.dumps(copied, allow_nan=False))
    except (TypeError, ValueError) as error:
        raise ValueError(f"{field_name} must be JSON-compatible") from error
    return MappingProxyType(normalized)


@dataclass(frozen=True, slots=True)
class CommandDefinition:
    name: str
    description: str
    effect: CommandEffect = CommandEffect.READ_ONLY

    def __post_init__(self) -> None:
        require_non_empty(self.name, "name")
        require_non_empty(self.description, "description")
        if not isinstance(self.effect, CommandEffect):
            raise TypeError("effect must be a CommandEffect")

    def to_dict(self) -> dict[str, str]:
        return {"name": self.name, "description": self.description, "effect": self.effect.value}


@dataclass(frozen=True, slots=True)
class CommandRequest:
    id: str
    command_name: str
    parameters: Mapping[str, Any]
    requested_at: datetime
    confirmed: bool = False

    def __post_init__(self) -> None:
        require_non_empty(self.id, "id")
        require_non_empty(self.command_name, "command_name")
        object.__setattr__(self, "parameters", _json_object(self.parameters, "parameters"))
        require_aware_datetime(self.requested_at, "requested_at")
        if not isinstance(self.confirmed, bool):
            raise TypeError("confirmed must be a bool")

    def to_dict(self) -> dict[str, Any]:
        return {"id": self.id, "command_name": self.command_name, "parameters": dict(self.parameters), "requested_at": self.requested_at.isoformat(), "confirmed": self.confirmed}

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> Self:
        return cls(
            id=require_non_empty(data.get("id"), "id"),
            command_name=require_non_empty(data.get("command_name"), "command_name"),
            parameters=data.get("parameters"),
            requested_at=parse_datetime(data.get("requested_at"), "requested_at"),
            confirmed=data.get("confirmed", False),
        )


@dataclass(frozen=True, slots=True)
class CommandResult:
    request_id: str
    command_name: str
    status: CommandStatus
    completed_at: datetime
    message: str
    output: Mapping[str, Any]

    def __post_init__(self) -> None:
        require_non_empty(self.request_id, "request_id")
        require_non_empty(self.command_name, "command_name")
        if not isinstance(self.status, CommandStatus):
            raise TypeError("status must be a CommandStatus")
        require_aware_datetime(self.completed_at, "completed_at")
        require_non_empty(self.message, "message")
        object.__setattr__(self, "output", _json_object(self.output, "output"))

    def to_dict(self) -> dict[str, Any]:
        return {"request_id": self.request_id, "command_name": self.command_name, "status": self.status.value, "completed_at": self.completed_at.isoformat(), "message": self.message, "output": dict(self.output)}

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> Self:
        try:
            status = CommandStatus(data.get("status"))
        except (TypeError, ValueError) as error:
            raise ValueError("status must be a valid CommandStatus") from error
        return cls(
            request_id=require_non_empty(data.get("request_id"), "request_id"),
            command_name=require_non_empty(data.get("command_name"), "command_name"),
            status=status,
            completed_at=parse_datetime(data.get("completed_at"), "completed_at"),
            message=require_non_empty(data.get("message"), "message"),
            output=data.get("output"),
        )
