"""In-process command registry with explicit mutation confirmation."""

from collections.abc import Callable, Mapping
from datetime import datetime, timezone
from typing import Any, TypeAlias

from project_atlas.domain.command import (
    CommandDefinition,
    CommandEffect,
    CommandRequest,
    CommandResult,
    CommandStatus,
)


CommandHandler: TypeAlias = Callable[[Mapping[str, Any]], Mapping[str, Any]]


class CommandCenter:
    """Register and execute only explicitly supplied in-process handlers."""

    def __init__(self) -> None:
        self._commands: dict[str, tuple[CommandDefinition, CommandHandler]] = {}

    def register(self, definition: CommandDefinition, handler: CommandHandler) -> None:
        if not isinstance(definition, CommandDefinition):
            raise TypeError("definition must be a CommandDefinition")
        if not callable(handler):
            raise TypeError("handler must be callable")
        if definition.name in self._commands:
            raise ValueError(f"command is already registered: {definition.name}")
        self._commands[definition.name] = (definition, handler)

    def list_commands(self) -> tuple[CommandDefinition, ...]:
        return tuple(self._commands[name][0] for name in sorted(self._commands))

    def execute(
        self, request: CommandRequest, *, completed_at: datetime | None = None
    ) -> CommandResult:
        if not isinstance(request, CommandRequest):
            raise TypeError("request must be a CommandRequest")
        registered = self._commands.get(request.command_name)
        if registered is None:
            raise KeyError(f"unknown command: {request.command_name}")
        definition, handler = registered
        timestamp = completed_at or datetime.now(timezone.utc)
        if not isinstance(timestamp, datetime):
            raise TypeError("completed_at must be a datetime")
        if timestamp.tzinfo is None or timestamp.utcoffset() is None:
            raise ValueError("completed_at must include timezone information")
        if timestamp < request.requested_at:
            raise ValueError("completed_at must not precede requested_at")
        if definition.effect is CommandEffect.MUTATING and not request.confirmed:
            return CommandResult(
                request_id=request.id,
                command_name=request.command_name,
                status=CommandStatus.REJECTED,
                completed_at=timestamp,
                message="mutating command requires explicit confirmation",
                output={},
            )
        output = handler(request.parameters)
        return CommandResult(
            request_id=request.id,
            command_name=request.command_name,
            status=CommandStatus.SUCCEEDED,
            completed_at=timestamp,
            message="command completed",
            output=output,
        )
