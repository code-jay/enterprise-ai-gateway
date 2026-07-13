from app.domain.contracts.base_response import BaseResponse

from app.domain.enums.provider_type import ProviderType


class RecommendationResponse(BaseResponse):

    provider: ProviderType

    model: str

    score: float

    reason: list[str]

    alternatives: list[str]