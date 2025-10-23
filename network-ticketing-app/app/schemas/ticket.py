from pydantic import BaseModel
from enum import Enum
from typing import Optional

class TicketStatus(str, Enum):
    new = "New"
    assigned = "Assigned"
    in_progress = "In Progress"
    on_hold = "On Hold"
    resolved = "Resolved"
    closed = "Closed"
    reopened = "Reopened"

class Severity(str, Enum):
    low = "Low"
    medium = "Medium"
    high = "High"

class Priority(str, Enum):
    low = "Low"
    medium = "Medium"
    high = "High"

class TicketCreate(BaseModel):
    created_by: int
    issue_description: str
    severity: Optional[Severity]
    priority: Optional[Priority]

class TicketOut(BaseModel):
    ticket_id: int
    issue_description: str
    status: TicketStatus
    severity: Optional[Severity]
    priority: Optional[Priority]

    class Config:
        orm_mode = True
