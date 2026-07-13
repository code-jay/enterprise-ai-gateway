"""
Base response contract.
"""

from datetime import datetime

from pydantic import BaseModel, Field


class BaseResponse(BaseModel):

    success: bool = True

    message: str = "Success"

    timestamp: datetime = Field(
        default_factory=datetime.utcnow
    )