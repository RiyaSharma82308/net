from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate
from datetime import datetime
from passlib.hash import bcrypt


class UserRepository:
    @staticmethod
    def get_user_by_email(email: str, db: Session):
        try:
            user = db.query(User).filter(User.email == email).first()
            return user, None
        except Exception as e:
            return None, str(e)

    @staticmethod
    def create_user(user_data, hashed_pw: str, db: Session):
        new_user = User(
            name=user_data.name,
            email=user_data.email,
            password_hash=hashed_pw,
            role=user_data.role,
            contact_number=user_data.contact_number,
            location=user_data.location,
        )
        try:
            db.add(new_user)
            db.commit()
            db.refresh(new_user)
            return new_user, None
        except Exception as e:
            db.rollback()
            return None, str(e)
        

    @staticmethod
    def get_all_users(db: Session):
        try:
            users = db.query(User).all()
            return users,None
        except Exception as e:
            return None, str(e)
