from pydantic import BaseModel, Field
from enum import Enum
from typing import Annotated





class Severity(str, Enum):
    low = "Low"
    medium = "Medium"
    high = "High"

class Priority(str, Enum):
    low = "Low"
    medium = "Medium"
    high = "High"

class SLACreateRequest(BaseModel):
    severity: Severity
    priority: Priority
    time_limit_hr: Annotated[int, Field(gt=0)]

class SLAUpdateRequest(BaseModel):
    severity: Severity
    priority: Priority
    time_limit_hr: Annotated[int, Field(gt=0)]

class SLAResponse(BaseModel):
    sla_id: int
    severity: Severity
    priority: Priority
    time_limit_hr: int

    class Config:
        from_attributes = True
