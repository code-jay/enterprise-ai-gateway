from enum import Enum


class ResponseSpeed(str, Enum):

    FAST = "fast"

    BALANCED = "balanced"

    BEST_QUALITY = "best_quality"