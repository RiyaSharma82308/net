from pydantic import BaseModel
from enum import Enum

class Severity(str, Enum):
    low = "Low"
    medium = "Medium"
    high = "High"

class Priority(str, Enum):
    low = "Low"
    medium = "Medium"
    high = "High"

class SLACreate(BaseModel):
    severity: Severity
    priority: Priority
    time_limit_hr: int

class SLAOut(BaseModel):
    sla_id: int
    severity: Severity
    priority: Priority
    time_limit_hr: int

    class Config:
        orm_mode = True
