from sqlalchemy import Column, Integer, String, Enum, TIMESTAMP
from app.database import Base



class IssueCategory(Base):
    __tablename__ = "issue_categories"
    category_id = Column(Integer, primary_key=True, index=True)
    category_name = Column(String(100), nullable=False)

