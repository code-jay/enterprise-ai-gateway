from app.domain.contracts.base_request import BaseRequest

from app.domain.enums.task_type import TaskType

from app.domain.enums.privacy_level import PrivacyLevel

from app.domain.enums.response_speed import ResponseSpeed


class RecommendationRequest(BaseRequest):

    task: TaskType

    context_length: int

    budget: str

    privacy: PrivacyLevel

    response_speed: ResponseSpeed