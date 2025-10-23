from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.user import UserCreate,LoginRequest
from app.database import get_db
from app.services.auth_service import AuthService

auth_router = APIRouter()

@auth_router.post("/signup")
def signup(user: UserCreate, db: Session = Depends(get_db)):
    new_user, err = AuthService.signup(user, db)

    if err == "Email already registered":
        return {"status": "error", "message": err}, 409
    if err:
        return {"status": "error", "message": err}, 500

    return {
        "status": "success",
        "message": "User created successfully",
        "data": {
            "user_id": new_user.user_id,
            "name": new_user.name,
            "email": new_user.email,
            "role": new_user.role,
            "contact_number": new_user.contact_number,
            "location": new_user.location
        }
    }, 201


@auth_router.post("/login")
def login(user: LoginRequest, db: Session = Depends(get_db)):
    token, err = AuthService.login(user,db)
    if err == "Invalid email or password":
        return {"status": "error", "message":err}, 401
    if err:
        return {"status":"error", "message":err}, 500
    
    return {
        "status": "success",
        "message": "Login successful",
        "access_token": token,
        "token_type": "bearer"
    }, 200