from pydantic import BaseModel
from enum import Enum
from typing import Optional
from datetime import datetime


class IssueCategoryCreate(BaseModel):
    category_name: str

class IssueCategoryOut(BaseModel):
    category_id: int
    category_name: str

    class Config:
        orm_mode = True
