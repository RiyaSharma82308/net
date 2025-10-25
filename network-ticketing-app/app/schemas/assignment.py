from pydantic import BaseModel
from datetime import datetime

class AssignmentCreate(BaseModel):
    ticket_id: int
    assigned_to: int
    assigned_by: int

class AssignmentOut(BaseModel):
    assignment_id: int
    ticket_id: int
    assigned_to: int
    assigned_by: int
    assigned_at: datetime

    class Config:
        orm_mode = True
