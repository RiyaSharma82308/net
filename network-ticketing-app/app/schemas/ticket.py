from pydantic import BaseModel
from enum import Enum
from typing import Optional
from datetime import datetime

# Enums for status, severity, and priority
class TicketStatus(str, Enum):
    new = "new"
    assigned = "assigned"
    in_progress = "in_progress"
    on_hold = "on_hold"
    resolved = "resolved"
    closed = "closed"
    reopened = "reopened"

class Severity(str, Enum):
    low = "Low"
    medium = "Medium"
    high = "High"

class Priority(str, Enum):
    low = "Low"
    medium = "Medium"
    high = "High"

# ✅ Request schema for ticket creation (used by customer/admin)
class TicketCreateRequest(BaseModel):
    issue_description: str
    issue_category_id: int  # Now required

# ✅ Request schema for ticket classification (used by admin/manager/agent)
class ClassifyTicketRequest(BaseModel):
    severity: Severity
    priority: Priority
    sla_id: int

# ✅ Request schema for assignment (used by admin)
class AssignTicketRequest(BaseModel):
    assigned_to: int

# ✅ Request schema for status update (used by engineer/admin)
class UpdateStatusRequest(BaseModel):
    status: TicketStatus

# ✅ Full ticket response schema
class TicketResponse(BaseModel):
    ticket_id: int
    title: Optional[str] = None
    issue_description: str
    status: TicketStatus
    severity: Optional[Severity] = None
    priority: Optional[Priority] = None
    location: Optional[str] = None
    created_by: int
    assigned_to: Optional[int] = None
    issue_category_id: int
    sla_id: Optional[int] = None
    due_date: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True  # Pydantic v2 style

# ✅ Lightweight schema for listing tickets
class TicketOut(BaseModel):
    ticket_id: int
    title: Optional[str] = None
    status: TicketStatus
    priority: Optional[Priority] = None

    class Config:
        orm_mode = True
