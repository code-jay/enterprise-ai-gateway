from app.domain.contracts.base_response import BaseResponse

from app.domain.enums.provider_type import ProviderType


class GatewayResponse(BaseResponse):

    provider: ProviderType

    model: str

    response: str

    latency_ms: float

    input_tokens: int

    output_tokens: int

    total_tokens: int

    estimated_cost: float