from pydantic import BaseModel
from enum import Enum
from typing import Optional
from datetime import datetime

class TicketStatus(str, Enum):
    new = "New"
    assigned = "Assigned"
    in_progress = "In Progress"
    on_hold = "On Hold"
    resolved = "Resolved"
    closed = "Closed"
    reopened = "Reopened"

class TicketActionLogCreate(BaseModel):
    ticket_id: int
    updated_by: int
    status: TicketStatus
    action_note: Optional[str] = None
    attachment_url: Optional[str] = None

class TicketActionLogOut(BaseModel):
    action_id: int
    ticket_id: int
    updated_by: int
    status: TicketStatus
    action_note: Optional[str]
    attachment_url: Optional[str]
    action_time: datetime

    class Config:
        orm_mode = True
