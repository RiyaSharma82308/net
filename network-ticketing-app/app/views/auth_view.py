from fastapi import APIRouter, Depends
from fastapi.security import HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from app.schemas.user import UserCreate,LoginRequest
from app.database import get_db
from app.services.auth_service import AuthService
from app.dependencies.auth import AuthMiddleware, security
from fastapi.responses import JSONResponse



auth_router = APIRouter()

@auth_router.post("/signup")
def signup(user: UserCreate, db: Session = Depends(get_db)):
    print("came here in signup!!!!!!!!!!!!!!!!!")
    new_user, err = AuthService.signup(user, db)

    if err == "Email already registered":
        return JSONResponse(status_code=409, content={"status": "error", "message": err})
    if err:
        return JSONResponse(status_code=500, content={"status": "error", "message": err})

    return JSONResponse(
        status_code=201,
        content={
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
        }
    )


@auth_router.post("/login")
def login(user: LoginRequest, db: Session = Depends(get_db)):
    print("here!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    token, err = AuthService.login(user, db)

    if err == "Invalid email or password":
        return JSONResponse(status_code=401, content={"status": "error", "message": err})
    if err:
        return JSONResponse(status_code=500, content={"status": "error", "message": err})

    return JSONResponse(
        status_code=200,
        content={
            "status": "success",
            "message": "Login successful",
            "access_token": token,
            "token_type": "bearer"
        }
    )


@auth_router.get("/me")
def get_current_user(
    db: Session = Depends(get_db),
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    user, err = AuthMiddleware.get_current_user(credentials, db)

    if err:
        return JSONResponse(status_code=401, content={"status": "error", "message": err})

    return JSONResponse(
        status_code=200,
        content={
            "status": "success",
            "data": {
                "user_id": user.user_id,
                "name": user.name,
                "email": user.email,
                "role": user.role,
                "contact_number": user.contact_number,
                "location": user.location
            }
        }
    )



@auth_router.post("/test-schema")
def test_schema(user: UserCreate):
    print("Received user:", user.dict())
    return {"status": "ok"}
