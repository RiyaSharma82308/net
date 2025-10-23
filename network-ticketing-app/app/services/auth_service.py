from sqlalchemy.orm import Session
from app.schemas.user import UserCreate
from app.repositories.auth_repo import create_user, get_user_by_email
from app.utils.jwt import create_access_token
from passlib.hash import bcrypt

def signup_service(user: UserCreate, db: Session):
    existing_user, err = get_user_by_email(user.email, db)
    if err:
        return None, "Database error during email check"
    if existing_user:
        return None, "Email already registered"

    # ✅ Truncate password to 72 characters
    safe_password = user.password[:72]
    hashed_pw, err = create_user(user, bcrypt.hash(safe_password), db)
    if err:
        return None, "Database error during user creation"
    return hashed_pw, None



def login_service(email: str, password: str, db: Session):
    user = get_user_by_email(email, db)
    if not user or not bcrypt.verify(password, user.password_hash):
        return None
    token = create_access_token({"sub": user.email, "role": user.role.value})
    return token
