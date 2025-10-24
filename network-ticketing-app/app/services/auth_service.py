from passlib.hash import bcrypt
from app.repositories.user_repository import UserRepository
from app.utils.jwt_handler import JWTHandler
class AuthService:
    @staticmethod
    def signup(user, db):
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
    
    @staticmethod
    def login(user_data, db):
        user,err = UserRepository.get_user_by_email(user_data.email, db)
        if err:
            return None, "Database error during email check"
        if not user:
            return None, "Invalid email or password"
        if not bcrypt.verify(user_data.password, user.password_hash):
            return None, "Invalid email or password"
        
        token = JWTHandler.create_access_token({"sub": user.email})
        return token, None