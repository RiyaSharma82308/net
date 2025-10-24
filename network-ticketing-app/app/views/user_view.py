from fastapi import APIRouter, Depends
from fastapi.security import HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from app.dependencies.auth import AuthMiddleware, security
from app.repositories.user_repository import UserRepository
from app.utils.role_guard import RoleGuard
from app.database import get_db


user_router = APIRouter()

@user_router.get("/users")
def get_all_users(db: Session = Depends(get_db), credentials: HTTPAuthorizationCredentials = Depends(security)):
    user, err = AuthMiddleware.get_current_user(credentials, db)
    if err:
        return{"status": "error", "message": err}, 401
    
    if not RoleGuard.has_role(user, ["admin"]):
        return {"status": "error", "message": "Access denied"}, 403
    
    users, err = UserRepository.get_all_users(db)
    if err:
        return {"status": "error", "message":err}, 500
    
    return {"status":"success", "data":users}, 200
