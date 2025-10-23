from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate
from datetime import datetime
from passlib.hash import bcrypt

def create_user(user: UserCreate, hashed_pw: str, db: Session):
    new_user = User(
        name=user.name,
        email=user.email,
        password_hash=hashed_pw,
        role=user.role,
        contact_number=user.contact_number,
        location=user.location,
    )
    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user, None
    except Exception as e:
        db.rollback()
        return None, str(e)



def get_user_by_email(email: str, db: Session):
    try:
        user = db.query(User).filter(User.email == email).first()
        return user, None
    except Exception as e:
        return None, e


