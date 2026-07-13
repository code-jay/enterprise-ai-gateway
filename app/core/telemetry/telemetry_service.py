"""
Telemetry Response DTO
"""

from datetime import datetime

from pydantic import BaseModel


class TelemetryResponse(BaseModel):
    """Aggregated gateway telemetry."""

    total_requests: int

    successful_requests: int

    failed_requests: int

    average_latency_ms: float

    total_input_tokens: int

    total_output_tokens: int

    total_tokens: int

    total_estimated_cost: float

    active_providers: list[str]

    uptime_seconds: int

    generated_at: datetime