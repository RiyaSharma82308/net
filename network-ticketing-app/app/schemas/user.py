from pydantic import BaseModel, EmailStr, Field, validator
from enum import Enum

class UserRole(str, Enum):
    customer = "customer"
    agent = "agent"
    engineer = "engineer"
    manager = "manager"

class UserCreate(BaseModel):
    name: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=6, max_length=72)
    role: UserRole
    contact_number: str = Field(..., pattern=r"^\d{10}$")
    location: str = Field(..., min_length=2)

    @validator("name")
    def name_must_be_alpha(cls, v):
        if not v.replace(" ", "").isalpha():
            raise ValueError("Name must contain only letters and spaces")
        return v

    @validator("password")
    def password_strength(cls, v):
        if not any(char.isdigit() for char in v):
            raise ValueError("Password must contain at least one digit")
        return v

class UserOut(BaseModel):
    user_id: int
    name: str
    email: EmailStr
    role: UserRole
    contact_number: str
    location: str

    class Config:
        orm_mode = True
