from sqlalchemy import Column, Integer, String, Text, Enum, ForeignKey, TIMESTAMP
from sqlalchemy.orm import relationship
from app.database import Base
import enum



class Feedback(Base):
    __tablename__ = "feedback"

    feedback_id = Column(Integer, primary_key=True, index=True)
    ticket_id = Column(Integer, ForeignKey("tickets.ticket_id"), nullable=False)
    rating = Column(Integer, nullable=False)
    comment = Column(Text)
    feedback_time = Column(TIMESTAMP, nullable=False)
