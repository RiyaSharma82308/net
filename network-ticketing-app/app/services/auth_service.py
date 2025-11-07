from passlib.hash import bcrypt
from app.repositories.user_repository import UserRepository
from app.utils.jwt_handler import JWTHandler
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.models.user import User
from app.repositories.token_repository import TokenRepository



class AuthService:
    @staticmethod
    def signup(user, db):
        existing_user, err = UserRepository.get_user_by_email(user.email, db)
        if user.role != "customer":
            return None, "Cant have any other role than customer"
        if err:
            return None, "Database error during email check"
        if existing_user:
            return None, "Email already registered"

        safe_password = user.password[:72]
        hashed_pw = bcrypt.hash(safe_password)
        new_user, err = UserRepository.create_user(user, hashed_pw, db)
        if err:
            return None, f"User creation failed: {err}"

        return new_user, None
    
    @staticmethod
    def login(user_data, db):
        print("service entered")
        print("Email is: ", user_data.email)
        user, err = UserRepository.get_user_by_email(user_data.email, db)
        print("user", user)
        if err:
            return None, "Database error during email check"
        if not user or not bcrypt.verify(user_data.password, user.password_hash):
            return None, "Invalid email or password"

        access_token = JWTHandler.create_access_token(
            {"sub": user.email},
            expires_delta=timedelta(minutes=15)
        )

        refresh_token = JWTHandler.create_refresh_token(
            {"sub": user.email},
            expires_delta=timedelta(days=7)
        )

        _, token_err = TokenRepository.store_refresh_token(user.user_id, refresh_token, db)
        if token_err:
            return None, f"Failed to store refresh token: {token_err}"

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "user": {
                "user_id": user.user_id,
                "name": user.name,
                "email": user.email,
                "role": user.role.value,
                "contact_number": user.contact_number,
                "location": user.location
            }
        }, None
    

    @staticmethod
    def refresh_access_token(refresh_token: str, db: Session):
        token_record, err = TokenRepository.get_token(refresh_token, db)
        if err or not token_record:
            return None, "Invalid or expired refresh token"

        # Optional: check expiry
        if token_record.expires_at < datetime.utcnow():
            return None, "Refresh token has expired"

        user = db.query(User).filter_by(user_id=token_record.user_id).first()
        if not user:
            return None, "User not found"

        new_access_token = JWTHandler.create_access_token(
            {"sub": user.email},
            expires_delta=timedelta(minutes=15)
        )

        return {"access_token": new_access_token}, None



   
    @staticmethod
    def logout(refresh_token: str, db: Session):
        try:
            deleted, err = TokenRepository.delete_token(refresh_token, db)
            if err:
                return False, f"Repository error: {err}"
            if not deleted:
                return False, None  # Token not found
            return True, None
        except Exception as e:
            return False, f"Service exception: {str(e)}"
        
    

    @staticmethod
    def admin_signup(user, db):
        existing_user, err = UserRepository.get_user_by_email(user.email, db)
        if err:
            return None, "Database error during email check"
        if existing_user:
            return None, "Email already registered"

        safe_password = user.password[:72]
        hashed_pw = bcrypt.hash(safe_password)
        new_user, err = UserRepository.create_user(user, hashed_pw, db)
        if err:
            return None, f"User creation failed: {err}"

        return new_user, None