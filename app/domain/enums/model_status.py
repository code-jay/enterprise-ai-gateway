"""Model operational status."""

from enum import Enum


class ModelStatus(str, Enum):
    ACTIVE = "active"
    DEGRADED = "degraded"
    DISABLED = "disabled"
    DEPRECATED = "deprecated"