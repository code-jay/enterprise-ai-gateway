from pydantic import BaseModel

from app.domain.enums.provider_type import ProviderType


class RoutingResult(BaseModel):

    provider: ProviderType

    model: str

    score: float

    routing_policy: str

    recommendation_reasons: list[str]

    alternatives: list[str]