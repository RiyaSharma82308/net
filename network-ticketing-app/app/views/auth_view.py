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
                "role": new_user.role.value,
                "contact_number": new_user.contact_number,
                "location": new_user.location
            }
        }
    )


@auth_router.post("/login")
def login(user: LoginRequest, db: Session = Depends(get_db)):
    print("here!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    result, err = AuthService.login(user, db)

    if err == "Invalid email or password":
        return JSONResponse(status_code=401, content={"status": "error", "message": err})
    if err:
        return JSONResponse(status_code=500, content={"status": "error", "message": err})
    if result is None:
        return JSONResponse(status_code=500, content={"status": "error", "message": "Unexpected login failure"})

    return JSONResponse(
        status_code=200,
        content={
            "status": "success",
            "message": "Login successful",
            "access_token": result["access_token"],
            "refresh_token": result["refresh_token"],
            "token_type": "bearer",
            "user": result["user"]
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
                "role": user.role.value,
                "contact_number": user.contact_number,
                "location": user.location
            }
        }
    )


@auth_router.post("/refresh")
def refresh_token(payload: dict, db: Session = Depends(get_db)):
    token = payload.get("refresh_token")
    if not token:
        return JSONResponse(status_code=400, content={"status": "error", "message": "Missing refresh token"})

    result, err = AuthService.refresh_access_token(token, db)
    if err:
        return JSONResponse(status_code=401, content={"status": "error", "message": err})

    return JSONResponse(
        status_code=200,
        content={
            "status": "success",
            "access_token": result["access_token"],
            "token_type": "bearer"
        }
    )



@auth_router.post("/logout")
def logout(payload: dict, db: Session = Depends(get_db)):
    token = payload.get("refresh_token")
    if not token:
        return JSONResponse(
            status_code=400,
            content={"status": "error", "message": "Missing refresh token"}
        )

    success, err = AuthService.logout(token, db)

    if err:
        return JSONResponse(
            status_code=500,
            content={"status": "error", "message": f"Logout failed: {err}"}
        )

    if not success:
        return JSONResponse(
            status_code=404,
            content={"status": "error", "message": "Refresh token not found"}
        )

    return JSONResponse(
        status_code=200,
        content={"status": "success", "message": "Logged out successfully"}
    )




def _get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db=Depends(get_db)
):
    user, err = AuthMiddleware.get_current_user(credentials, db)
    if err or not user:
        return None
    return user



@auth_router.post("/admin/signup")
def admin_signup(
    user: UserCreate,
    db: Session = Depends(get_db),
    current_user=Depends(_get_current_user)
):
    if not current_user:
        return JSONResponse(
            status_code=401,
            content={"status": "error", "message": "Invalid or expired token"}
        )

    if current_user.role.value != "admin":
        print("current role ", current_user.role.value)
        return JSONResponse(
            status_code=403,
            content={"status": "error", "message": "Only admins can create new users"}
        )

    new_user, err = AuthService.admin_signup(user, db)

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
                "role": new_user.role.value,
                "contact_number": new_user.contact_number,
                "location": new_user.location
            }
        }
    )
