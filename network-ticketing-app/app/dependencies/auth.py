from fastapi import dependencies, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.utils.jwt_handler import JWTHandler
from app.repositories.user_repository import UserRepository
from app.database import get_db

security = HTTPBearer()

class AuthMiddleware:
    @staticmethod
    def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security), db=Depends(get_db)):
        token = credentials.credentials
        payload, err = JWTHandler.decode_token(token)
        if err:
            return None, "Invalid or expired token"
        email = payload.het("sub")
        if not email:
            return None, "Token missing subject"
        
        user, err = UserRepository.get_user_by_email(email, db)
        if err or not user:
            return None, "User not found"
        
        return user, None