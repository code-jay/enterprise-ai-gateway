"""
Base request contract.
"""

from datetime import datetime
from uuid import uuid4

from pydantic import BaseModel, Field


class BaseRequest(BaseModel):

    request_id: str = Field(
        default_factory=lambda: str(uuid4())
    )

    user_id: str | None = None

    session_id: str | None = None

    conversation_id: str | None = None

    tenant_id: str | None = None

    created_at: datetime = Field(
        default_factory=datetime.utcnow
    )