"""Relative model pricing categories."""

from enum import Enum


class CostTier(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"