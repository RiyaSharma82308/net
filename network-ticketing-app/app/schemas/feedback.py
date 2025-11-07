from pydantic import BaseModel, Field
from typing import Optional


class FeedbackCreateRequest(BaseModel):
    rating: int = Field(..., ge=1, le=5, description="Rating between 1 and 5")
    comment: Optional[str] = Field(None, description="Optional comment about the resolution")


class FeedbackResponse(BaseModel):
    feedback_id: int
    ticket_id: int
    rating: int
    comment: Optional[str]
    feedback_time: str
