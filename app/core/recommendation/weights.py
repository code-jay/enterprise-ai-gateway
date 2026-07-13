"""Weights used by the model recommendation engine."""

from dataclasses import dataclass


@dataclass(frozen=True)
class ScoringWeights:
    """Configurable recommendation scoring weights."""

    task: float = 0.30
    quality: float = 0.20
    speed: float = 0.15
    cost: float = 0.15
    privacy: float = 0.10
    context: float = 0.05
    capability: float = 0.05

    def as_dict(self) -> dict[str, float]:
        weights = {
            "task": self.task,
            "quality": self.quality,
            "speed": self.speed,
            "cost": self.cost,
            "privacy": self.privacy,
            "context": self.context,
            "capability": self.capability,
        }

        total = sum(weights.values())

        if abs(total - 1.0) > 0.0001:
            raise ValueError(
                f"Scoring weights must total 1.0; got {total}."
            )

        return weights


DEFAULT_WEIGHTS = ScoringWeights()