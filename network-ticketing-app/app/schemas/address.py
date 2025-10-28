from pydantic import BaseModel, Field
from datetime import datetime

class AddressBase(BaseModel):
    street: str = Field(..., min_length=3)
    city: str = Field(..., min_length=2)
    state: str = Field(..., min_length=2)
    postal_code: str = Field(..., min_length=4, max_length=10)
    country: str = Field(..., min_length=2)

class AddressCreate(AddressBase):
    pass

class AddressCreateWithUserId(AddressBase):
    user_id: int

class AddressCreateInternal(AddressCreateWithUserId):
    pass


class AddressUpdate(AddressBase):
    pass  # All fields are optional if you want partial updates; otherwise keep as-is

class AddressOut(AddressBase):
    address_id: int
    user_id: int
    created_at: datetime

    class Config:
        from_attributes = True  # replaces orm_mode in Pydantic v2
