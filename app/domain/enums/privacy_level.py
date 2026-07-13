from enum import Enum


class PrivacyLevel(str, Enum):

    PUBLIC = "public"

    INTERNAL = "internal"

    CONFIDENTIAL = "confidential"

    RESTRICTED = "restricted"