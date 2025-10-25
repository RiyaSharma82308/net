from sqlalchemy import Column, Integer, String, Enum, TIMESTAMP
from app.database import Base
import enum


class Severity(enum.Enum):
    low = "Low"
    medium = "Medium"
    high = "High"

class Priority(enum.Enum):
    low = "Low"
    medium = "Medium"
    high = "High"


class SLA(Base):
    __tablename__ = "slas"

    sla_id = Column(Integer, primary_key=True, index=True)
    severity = Column(Enum(Severity), nullable=False)
    priority = Column(Enum(Priority), nullable=False)
    time_limit_hr = Column(Integer, nullable=False)

