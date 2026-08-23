"""Repository domain model without Git integration."""

from collections.abc import Mapping
from dataclasses import dataclass
from typing import Any, Self

from ._validation import require_non_empty


@dataclass(frozen=True, slots=True)
class Repository:
    """A declared code repository and its known branch label."""

    id: str
    name: str
    root_path: str
    branch: str

    def __post_init__(self) -> None:
        require_non_empty(self.id, "id")
        require_non_empty(self.name, "name")
        require_non_empty(self.root_path, "root_path")
        require_non_empty(self.branch, "branch")

    def to_dict(self) -> dict[str, str]:
        """Return a JSON-compatible representation of the repository."""

        return {
            "id": self.id,
            "name": self.name,
            "root_path": self.root_path,
            "branch": self.branch,
        }

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> Self:
        """Create a validated repository from serialized data."""

        return cls(
            id=require_non_empty(data.get("id"), "id"),
            name=require_non_empty(data.get("name"), "name"),
            root_path=require_non_empty(data.get("root_path"), "root_path"),
            branch=require_non_empty(data.get("branch"), "branch"),
        )
