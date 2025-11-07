from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate
from datetime import datetime
from passlib.hash import bcrypt
from sqlalchemy.orm import Session
from typing import Tuple, Optional, Dict


class UserRepository:
    @staticmethod
    def get_user_by_id(user_id: int, db):
        try:
            user = db.query(User).filter(User.user_id == user_id).first()
            if not user:
                return None
            return user
        except Exception as e:
            return None

    @staticmethod
    def get_user_by_email(email: str, db: Session):
        try:
            print("Querying for email:", email)
            user = db.query(User).filter(User.email == email).first()
            print("Found user:", user)
            return user, None
        except Exception as e:
            print("Error during query:", e)
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
        
    @staticmethod
    def mark_user_logged_out(user_id: int, db: Session) -> Tuple[Optional[Dict], Optional[str]]:
        try:
            user = db.query(User).filter(User.user_id == user_id).first()
            if not user:
                return None, "User not found"

            # Optional: update a field like is_logged_in = False
            # user.is_logged_in = False
            # db.commit()

            print(f"[Logout] User {user.name} logged out.")
            return {"message": f"User {user.name} logged out."}, None
        except Exception as e:
            return None, str(e)
