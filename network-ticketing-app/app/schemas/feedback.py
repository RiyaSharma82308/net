from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class FeedbackCreate(BaseModel):
    ticket_id: int
    rating: int = Field(..., ge=1, le=5)
    comment: Optional[str] = None

class FeedbackOut(BaseModel):
    feedback_id: int
    ticket_id: int
    rating: int
    comment: Optional[str]
    feedback_time: datetime

    class Config:
        orm_mode = True
