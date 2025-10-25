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


class TicketActionLog(Base):
    __tablename__ = "ticket_action_logs"

    action_id = Column(Integer, primary_key=True, index=True)
    ticket_id = Column(Integer, ForeignKey("tickets.ticket_id"), nullable=False)
    updated_by = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    status = Column(Enum(TicketStatus), nullable=False)
    action_note = Column(Text)
    attachment_url = Column(String(255))
    action_time = Column(TIMESTAMP, nullable=False)
