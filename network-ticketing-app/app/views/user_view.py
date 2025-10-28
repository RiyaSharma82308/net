from fastapi import APIRouter, Depends
from fastapi.security import HTTPAuthorizationCredentials
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.dependencies.auth import AuthMiddleware, security
from app.repositories.user_repository import UserRepository
from app.services.address_service import AddressService
from app.services.ticket_service import TicketService  # ← make sure this exists
from app.utils.role_guard import RoleGuard
from app.database import get_db

user_router = APIRouter()

# 🧑‍💼 Admin: Get all users
@user_router.get("/users")
def get_all_users(
    db: Session = Depends(get_db),
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    user, err = AuthMiddleware.get_current_user(credentials, db)
    if err:
        return JSONResponse(status_code=401, content={"status": "error", "message": err})

    if not RoleGuard.has_role(user, ["admin"]):
        return JSONResponse(status_code=403, content={"status": "error", "message": "Access denied"})

    users, err = UserRepository.get_all_users(db)
    if err:
        return JSONResponse(status_code=500, content={"status": "error", "message": err})

    serialized_users = [
        {
            "user_id": u.user_id,
            "name": u.name,
            "email": u.email,
            "role": u.role.value if hasattr(u.role, "value") else u.role,
            "created_at": str(u.created_at)
        }
        for u in users
    ]

    return JSONResponse(
        status_code=200,
        content={
            "status": "success",
            "message": "Users fetched successfully",
            "data": serialized_users
        }
    )

# 🧑‍💻 Customer: Dashboard view
@user_router.get("/me/dashboard")
def get_customer_dashboard(
    db: Session = Depends(get_db),
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    user, err = AuthMiddleware.get_current_user(credentials, db)
    if err:
        return JSONResponse(status_code=401, content={"status": "error", "message": err})

    if not RoleGuard.has_role(user, ["customer"]):
        return JSONResponse(status_code=403, content={"status": "error", "message": "Access denied"})

    profile = {
        "name": user.name,
        "email": user.email,
        "role": user.role.value if hasattr(user.role, "value") else str(user.role)
    }

    addresses, addr_err = AddressService.list_by_user(user.user_id, db)
    tickets, ticket_err = TicketService.list_by_user(user.user_id, db)

    return JSONResponse(status_code=200, content={
        "status": "success",
        "data": {
            "profile": profile,
            "addresses": addresses if not addr_err else [],
            "tickets": tickets if not ticket_err else []
        }
    })
