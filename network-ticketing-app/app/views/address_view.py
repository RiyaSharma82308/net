from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.database import get_db
from app.schemas.address import (
    AddressCreate,
    AddressUpdate,
    AddressCreateInternal,
    AddressCreateWithUserId
)
from app.services.address_service import AddressService
from app.dependencies.auth import AuthMiddleware, security
from app.utils.role_guard import RoleGuard

address_router = APIRouter()
security = HTTPBearer()

# 🧾 Customer creates their own address
@address_router.post("/me/addresses")
def create_my_address(
    payload: AddressCreate,
    db: Session = Depends(get_db),
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    user, err = AuthMiddleware.get_current_user(credentials, db)
    if err:
        return JSONResponse(status_code=401, content={"status": "error", "message": err})

    if not RoleGuard.has_role(user, ["customer"]):
        return JSONResponse(status_code=403, content={"status": "error", "message": "Only customers can use this endpoint"})

    enriched_payload = AddressCreateInternal(**payload.model_dump(), user_id=user.user_id)
    response, err = AddressService.create_for_self(enriched_payload, db)
    if err:
        return JSONResponse(status_code=400, content={"status": "error", "message": err})

    return JSONResponse(status_code=201, content={"status": "success", "data": response})


# 🧾 Admin/Agent creates address for any user
@address_router.post("/admin/addresses")
def create_address_for_user(
    payload: AddressCreateWithUserId,
    db: Session = Depends(get_db),
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    user, err = AuthMiddleware.get_current_user(credentials, db)
    if err:
        return JSONResponse(status_code=401, content={"status": "error", "message": err})

    if not RoleGuard.has_role(user, ["admin", "agent"]):
        return JSONResponse(status_code=403, content={"status": "error", "message": "Only admins and agents can use this endpoint"})

    response, err = AddressService.create_for_user(payload, db)
    if err:
        return JSONResponse(status_code=400, content={"status": "error", "message": err})

    return JSONResponse(status_code=201, content={"status": "success", "data": response})


# 📦 List addresses for a user (admin or self)

@address_router.get("/me/addresses")
def list_my_addresses(
    db: Session = Depends(get_db),
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    user, err = AuthMiddleware.get_current_user(credentials, db)
    if err:
        return JSONResponse(status_code=401, content={"status": "error", "message": err})

    if not RoleGuard.has_role(user, ["customer"]):
        return JSONResponse(status_code=403, content={"status": "error", "message": "Only customers can view their own addresses"})

    response, err = AddressService.list_by_user(user.user_id, db)
    if err:
        return JSONResponse(status_code=500, content={"status": "error", "message": err})

    return JSONResponse(status_code=200, content={"status": "success", "data": response})


@address_router.get("/admin/addresses/user/{user_id}")
def list_user_addresses(
    user_id: int,
    db: Session = Depends(get_db),
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    user, err = AuthMiddleware.get_current_user(credentials, db)
    if err:
        return JSONResponse(status_code=401, content={"status": "error", "message": err})

    if not RoleGuard.has_role(user, ["admin", "agent", "manager"]):
        return JSONResponse(status_code=403, content={"status": "error", "message": "Unauthorized to view addresses for this user"})

    response, err = AddressService.list_by_user(user_id, db)
    if err:
        return JSONResponse(status_code=500, content={"status": "error", "message": err})

    return JSONResponse(status_code=200, content={"status": "success", "data": response})


# ✏️ Update address (ownership check optional)
@address_router.put("/update/addresses/{address_id}")
def update_address(
    address_id: int,
    payload: AddressUpdate,
    db: Session = Depends(get_db),
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    user, err = AuthMiddleware.get_current_user(credentials, db)
    if err:
        return JSONResponse(status_code=401, content={"status": "error", "message": err})

    # Fetch the address first
    address, err = AddressService.get_by_id(address_id, db)
    if err:
        return JSONResponse(status_code=404, content={"status": "error", "message": err})

    # Enforce ownership for customers
    if RoleGuard.has_role(user, ["customer"]) and address["user_id"] != user.user_id:
        return JSONResponse(status_code=403, content={"status": "error", "message": "You can only update your own address"})

    # Proceed with update
    response, err = AddressService.update(address_id, payload, db)
    if err:
        return JSONResponse(status_code=400, content={"status": "error", "message": err})

    return JSONResponse(status_code=200, content={"status": "success", "data": response})




@address_router.put("/admin/addresses/{address_id}")
def admin_update_address(
    address_id: int,
    payload: AddressUpdate,
    db: Session = Depends(get_db),
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    user, err = AuthMiddleware.get_current_user(credentials, db)
    if err:
        return JSONResponse(status_code=401, content={"status": "error", "message": err})

    if not RoleGuard.has_role(user, ["admin", "agent"]):
        return JSONResponse(status_code=403, content={"status": "error", "message": "Only admins and agents can update any address"})

    response, err = AddressService.update(address_id, payload, db)
    if err:
        return JSONResponse(status_code=400, content={"status": "error", "message": err})

    return JSONResponse(status_code=200, content={"status": "success", "data": response})



# 🗑️ Delete address (ownership check optional)
@address_router.delete("/addresses/{address_id}")
def delete_address(
    address_id: int,
    db: Session = Depends(get_db),
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    user, err = AuthMiddleware.get_current_user(credentials, db)
    if err:
        return JSONResponse(status_code=401, content={"status": "error", "message": err})

    # Fetch the address first
    address, err = AddressService.get_by_id(address_id, db)
    if err:
        return JSONResponse(status_code=404, content={"status": "error", "message": err})

    # Enforce ownership for customers
    if RoleGuard.has_role(user, ["customer"]) and address["user_id"] != user.user_id:
        return JSONResponse(status_code=403, content={"status": "error", "message": "You can only delete your own address"})

    # Proceed with deletion
    success, err = AddressService.delete(address_id, db)
    if err:
        return JSONResponse(status_code=400, content={"status": "error", "message": err})

    return JSONResponse(status_code=200, content={"status": "success", "message": "Address deleted successfully"})



@address_router.delete("/admin/delete/addresses/{address_id}")
def admin_delete_address(
    address_id: int,
    db: Session = Depends(get_db),
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    user, err = AuthMiddleware.get_current_user(credentials, db)
    if err:
        return JSONResponse(status_code=401, content={"status": "error", "message": err})

    if not RoleGuard.has_role(user, ["admin", "agent"]):
        return JSONResponse(status_code=403, content={"status": "error", "message": "Only admins and agents can delete any address"})

    success, err = AddressService.delete(address_id, db)
    if err:
        return JSONResponse(status_code=400, content={"status": "error", "message": err})

    return JSONResponse(status_code=200, content={"status": "success", "message": "Address deleted successfully"})
