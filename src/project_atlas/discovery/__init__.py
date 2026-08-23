"""Public local project discovery contracts."""

from .engine import (
    DEFAULT_EXCLUDED_DIRECTORIES,
    DEFAULT_PROJECT_MARKERS,
    DiscoveryScope,
    LocalProjectDiscoveryEngine,
)

__all__ = [
    "DEFAULT_EXCLUDED_DIRECTORIES",
    "DEFAULT_PROJECT_MARKERS",
    "DiscoveryScope",
    "LocalProjectDiscoveryEngine",
]
