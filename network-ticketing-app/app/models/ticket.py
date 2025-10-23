from sqlalchemy import Column, Integer, String, Text, Enum, ForeignKey, TIMESTAMP
from sqlalchemy.orm import relationship
from app.database import Base
import enum

class TicketStatus(enum.Enum):
    new = "New"
    assigned = "Assigned"
    in_progress = "In Progress"
    on_hold = "On Hold"
    resolved = "Resolved"
    closed = "Closed"
    reopened = "Reopened"

class Severity(enum.Enum):
    low = "Low"
    medium = "Medium"
    high = "High"

class Priority(enum.Enum):
    low = "Low"
    medium = "Medium"
    high = "High"

class Ticket(Base):
    __tablename__ = "tickets"

    ticket_id = Column(Integer, primary_key=True, index=True)
    created_by = Column(Integer, ForeignKey("users.user_id"))
    issue_description = Column(Text, nullable=False)
    status = Column(Enum(TicketStatus), default=TicketStatus.new)
    severity = Column(Enum(Severity), nullable=True)
    priority = Column(Enum(Priority), nullable=True)
    issue_category_id = Column(Integer, ForeignKey("issue_categories.category_id"), nullable=True)
    sla_id = Column(Integer, ForeignKey("slas.sla_id"), nullable=True)
    assigned_to = Column(Integer, ForeignKey("users.user_id"), nullable=True)
    created_at = Column(TIMESTAMP)
    updated_at = Column(TIMESTAMP)

    # Relationships
    creator = relationship("User", foreign_keys=[created_by])
    assignee = relationship("User", foreign_keys=[assigned_to])
