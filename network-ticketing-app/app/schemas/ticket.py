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

class Severity(str, Enum):
    low = "Low"
    medium = "Medium"
    high = "High"

class Priority(str, Enum):
    low = "Low"
    medium = "Medium"
    high = "High"

# Request schema for ticket creation
class TicketCreateRequest(BaseModel):
    issue_description: str
    priority: Priority
    severity: Optional[Severity] = None
    # issue_category_id: Optional[int] = None
    # sla_id: Optional[int] = None

# Response schema for full ticket details
class TicketResponse(BaseModel):
    ticket_id: int
    title: str
    issue_description: str
    status: TicketStatus
    severity: Optional[Severity]
    priority: Optional[Priority]
    location: Optional[str]
    created_by: int
    assigned_to: Optional[int]
    # issue_category_id: Optional[int]
    # sla_id: Optional[int]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# Lightweight schema for listing tickets
class TicketOut(BaseModel):
    ticket_id: int
    title: str
    status: TicketStatus
    priority: Optional[Priority]

    class Config:
        orm_mode = True
