from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.database import get_db
from app.schemas.sla import SLACreateRequest, SLAUpdateRequest
from app.services.sla_service import SLAService
from app.dependencies.auth import AuthMiddleware
from app.utils.role_guard import RoleGuard


security = HTTPBearer()

sla_router = APIRouter()

@sla_router.post("/slas")
def create_sla(
    payload: SLACreateRequest,
    db: Session = Depends(get_db),
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    print("payload is!!!!!!!", payload)
    user, err = AuthMiddleware.get_current_user(credentials, db)
    if err:
        return JSONResponse(status_code=401, content={"status": "error", "message": err})

    if not RoleGuard.has_role(user, ["admin"]):
        return JSONResponse(status_code=403, content={"status": "error", "message": "Only admins can create SLAs"})

    response, err = SLAService.create(payload, db)
    if err:
        return JSONResponse(status_code=400, content={"status": "error", "message": err})

    return JSONResponse(status_code=201, content={"status": "success", "data": response})


@sla_router.get("/slas")
def list_slas(db: Session = Depends(get_db)):
    response, err = SLAService.list_all(db)
    if err:
        return JSONResponse(status_code=500, content={"status": "error", "message": err})

    return JSONResponse(status_code=200, content={"status": "success", "data": response})


@sla_router.put("/slas/{sla_id}")
def update_sla(
    sla_id: int,
    payload: SLAUpdateRequest,
    db: Session = Depends(get_db),
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    user, err = AuthMiddleware.get_current_user(credentials, db)
    if err:
        return JSONResponse(status_code=401, content={"status": "error", "message": err})

    if not RoleGuard.has_role(user, ["admin"]):
        return JSONResponse(status_code=403, content={"status": "error", "message": "Only admins can update SLAs"})

    response, err = SLAService.update(sla_id, payload, db)
    if err:
        return JSONResponse(status_code=400, content={"status": "error", "message": err})

    return JSONResponse(status_code=200, content={"status": "success", "data": response})


@sla_router.delete("/slas/{sla_id}")
def delete_sla(
    sla_id: int,
    db: Session = Depends(get_db),
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    user, err = AuthMiddleware.get_current_user(credentials, db)
    if err:
        return JSONResponse(status_code=401, content={"status": "error", "message": err})

    if not RoleGuard.has_role(user, ["admin"]):
        return JSONResponse(status_code=403, content={"status": "error", "message": "Only admins can delete SLAs"})

    success, err = SLAService.delete(sla_id, db)
    if err:
        return JSONResponse(status_code=400, content={"status": "error", "message": err})

    return JSONResponse(status_code=200, content={"status": "success", "message": "SLA deleted successfully"})
