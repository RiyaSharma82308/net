from sqlalchemy import Column, Integer, String, Enum, TIMESTAMP
from app.database import Base
import enum

class UserRole(enum.Enum):
    customer = "customer"
    agent = "agent"
    engineer = "engineer"
    manager = "manager"
    admin = "admin"

class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    role = Column(Enum(UserRole), nullable=False)
    contact_number = Column(String(15))
    location = Column(String(100))
    password_hash = Column(String(255), nullable=False)
    created_at = Column(TIMESTAMP)
