from sqlalchemy import Column, Integer, String, Text, Enum, ForeignKey, TIMESTAMP
from sqlalchemy.orm import relationship
from app.database import Base
import enum

class TicketStatus(str, enum.Enum):
    new = "new"
    assigned = "assigned"
    in_progress = "in_progress"
    on_hold = "on_hold"
    resolved = "resolved"
    closed = "closed"
    reopened = "reopened"


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
    issue_category_id = Column(Integer, ForeignKey("issue_categories.category_id"), nullable=False)
    sla_id = Column(Integer, ForeignKey("slas.sla_id"), nullable=True)
    assigned_to = Column(Integer, ForeignKey("users.user_id"), nullable=True)
    created_at = Column(TIMESTAMP, nullable=False)
    updated_at = Column(TIMESTAMP, nullable=False)
    due_date = Column(TIMESTAMP, nullable=True)

    # Relationships
    creator = relationship("User", foreign_keys=[created_by])
    assignee = relationship("User", foreign_keys=[assigned_to])
    sla = relationship("SLA") 
    issue_category = relationship("IssueCategory")