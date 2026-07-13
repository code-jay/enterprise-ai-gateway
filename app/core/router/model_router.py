from app.core.recommendation.recommendation_service import (
    recommendation_service,
)

from app.core.router.provider_selector import (
    ProviderSelector,
)

from app.domain.contracts.gateway_request import GatewayRequest

from app.domain.contracts.gateway_response import GatewayResponse

from app.domain.contracts.provider_request import (
    ProviderRequest,
)

from app.domain.contracts.recommendation_request import (
    RecommendationRequest,
)

from app.core.router.routing_policy import RoutingPolicy

from app.core.router.routing_result import RoutingResult


class ModelRouter:

    def __init__(self):

        self.selector = ProviderSelector()

    async def route(
        self,
        request: GatewayRequest,
    ) -> GatewayResponse:

        recommendation = recommendation_service.recommend(

            RecommendationRequest(

                task=request.task,

                context_length=request.context_length,

                budget=request.budget,

                privacy=request.privacy,

                response_speed=request.response_speed,

                requires_vision=request.requires_vision,

                requires_tools=request.requires_tools,

            )

        )

        provider = self.selector.select(

            recommendation.provider

        )

        provider_request = ProviderRequest(

            model=recommendation.model,

            prompt=request.prompt,

            system_prompt=request.system_prompt,

            temperature=request.temperature,

            max_tokens=request.max_tokens,

            stream=request.stream,

        )

        provider_response = await provider.generate(

            provider_request

        )

        return GatewayResponse(

            provider=provider_response.provider,

            model=provider_response.model,

            content=provider_response.content,

            latency_ms=provider_response.latency_ms,

            input_tokens=provider_response.input_tokens,

            output_tokens=provider_response.output_tokens,

            total_tokens=provider_response.total_tokens,

            routing_reason=recommendation.reason,

            recommendation_score=recommendation.score,

        )
    
model_router = ModelRouter()