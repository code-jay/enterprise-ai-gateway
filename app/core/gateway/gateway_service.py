"""Application service for processing Enterprise AI Gateway requests."""

import logging
from time import perf_counter

from app.core.router.model_router import ModelRouter
from app.domain.contracts.gateway_request import GatewayRequest
from app.domain.contracts.gateway_response import GatewayResponse
from app.utils.exceptions import (
    GatewayError,
    ProviderError,
)


logger = logging.getLogger(__name__)


class GatewayService:
    """
    Coordinates the complete gateway request lifecycle.

    The service delegates model recommendation, provider selection,
    and model execution to the ModelRouter.
    """

    def __init__(
        self,
        model_router: ModelRouter,
    ) -> None:
        self._model_router = model_router

    async def generate(
        self,
        request: GatewayRequest,
    ) -> GatewayResponse:
        """
        Process one AI Gateway request.

        Args:
            request: Provider-independent gateway request.

        Returns:
            A normalized GatewayResponse.

        Raises:
            GatewayError: When routing or provider execution fails.
        """

        started_at = perf_counter()

        logger.info(
            "Gateway request started | request_id=%s | task=%s",
            request.request_id,
            request.task.value,
        )

        try:
            response = await self._model_router.route(request)

            total_latency_ms = round(
                (perf_counter() - started_at) * 1000,
                2,
            )

            # Gateway-level latency includes recommendation,
            # routing, provider selection, and provider execution.
            response.metadata["gateway_latency_ms"] = (
                total_latency_ms
            )

            logger.info(
                (
                    "Gateway request completed | "
                    "request_id=%s | provider=%s | "
                    "model=%s | latency_ms=%s"
                ),
                request.request_id,
                response.provider.value,
                response.model,
                total_latency_ms,
            )

            return response

        except ProviderError:
            logger.exception(
                (
                    "Provider execution failed | "
                    "request_id=%s"
                ),
                request.request_id,
            )
            raise

        except GatewayError:
            logger.exception(
                (
                    "Gateway processing failed | "
                    "request_id=%s"
                ),
                request.request_id,
            )
            raise

        except Exception as exc:
            logger.exception(
                (
                    "Unexpected gateway error | "
                    "request_id=%s"
                ),
                request.request_id,
            )

            raise GatewayError(
                "Unexpected error while processing the AI request."
            ) from exc

from app.core.router.model_router import (
    ModelRouter,
    model_router,
)
gateway_service = GatewayService(
    model_router=model_router,
)