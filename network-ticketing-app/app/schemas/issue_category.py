from pydantic import BaseModel
from enum import Enum
from typing import Optional
from datetime import datetime


class IssueCategoryCreateRequest(BaseModel):
    category_name: str

class IssueCategoryUpdateRequest(BaseModel):
    category_name: str

class IssueCategoryResponse(BaseModel):
    category_id: int
    category_name: str

    class Config:
        from_attributes = True


