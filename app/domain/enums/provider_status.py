from enum import Enum


class ProviderStatus(str, Enum):

    AVAILABLE = "available"

    DEGRADED = "degraded"

    UNAVAILABLE = "unavailable"

    MAINTENANCE = "maintenance"