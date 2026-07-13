"""Score models by workload/task suitability."""

from app.core.recommendation.scorers.base_scorer import BaseScorer
from app.domain.contracts.recommendation_request import (
    RecommendationRequest,
)
from app.domain.enums.task_type import TaskType
from app.domain.models.model_info import ModelInfo
from app.domain.models.score_result import ScoreResult


class TaskScorer(BaseScorer):
    """Scores how directly a model supports the requested task."""

    name = "task"

    def score(
        self,
        model: ModelInfo,
        request: RecommendationRequest,
    ) -> ScoreResult:
        if request.task in model.supported_tasks:
            return ScoreResult(
                score=10.0,
                reason=(
                    f"Model explicitly supports the "
                    f"'{request.task.value}' task."
                ),
            )

        if TaskType.GENERAL in model.supported_tasks:
            return ScoreResult(
                score=7.0,
                reason=(
                    "Model provides general-purpose support "
                    "for this workload."
                ),
            )

        return ScoreResult(
            score=0.0,
            reason="Model does not support the requested task.",
        )