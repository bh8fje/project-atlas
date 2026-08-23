"""Provider-neutral contracts for explicit AI generation calls."""

from dataclasses import dataclass
from typing import Protocol


@dataclass(frozen=True, slots=True)
class AIRequest:
    """A complete provider request prepared by Project Atlas."""

    system_instructions: str
    input_text: str
    response_format: str = "json"

    def __post_init__(self) -> None:
        for value, name in (
            (self.system_instructions, "system_instructions"),
            (self.input_text, "input_text"),
            (self.response_format, "response_format"),
        ):
            if not isinstance(value, str):
                raise TypeError(f"{name} must be a string")
            if not value.strip():
                raise ValueError(f"{name} must not be empty")


@dataclass(frozen=True, slots=True)
class AIProviderResponse:
    """Raw text returned by one explicitly selected AI provider."""

    provider_name: str
    model_name: str
    content: str

    def __post_init__(self) -> None:
        for value, name in (
            (self.provider_name, "provider_name"),
            (self.model_name, "model_name"),
            (self.content, "content"),
        ):
            if not isinstance(value, str):
                raise TypeError(f"{name} must be a string")
            if not value.strip():
                raise ValueError(f"{name} must not be empty")


class AIProvider(Protocol):
    """Replaceable provider interface; implementations control external I/O."""

    def generate(self, request: AIRequest) -> AIProviderResponse:
        """Generate one response for an explicit request."""

        ...
