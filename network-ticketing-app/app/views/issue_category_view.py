from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.issue_category import IssueCategoryCreateRequest, IssueCategoryUpdateRequest
from app.services.issue_category_service import IssueCategoryService
from app.dependencies.auth import AuthMiddleware, security
from app.utils.role_guard import RoleGuard
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.router import ticket_router

issue_category_router = APIRouter()
security = HTTPBearer()


@issue_category_router.post("/issue-categories")
def create_category(
    payload: IssueCategoryCreateRequest,
    db: Session = Depends(get_db),
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    user, err = AuthMiddleware.get_current_user(credentials, db)
    if err:
        return JSONResponse(status_code=401, content={"status": "error", "message": err})

    if not RoleGuard.has_role(user, ["admin"]):
        return JSONResponse(status_code=403, content={"status": "error", "message": "Only admins can create categories"})

    response, err = IssueCategoryService.create(payload, db)
    if err:
        return JSONResponse(status_code=400, content={"status": "error", "message": err})

    return JSONResponse(status_code=201, content={"status": "success", "data": response})


@issue_category_router.get("/issue-categories")
def list_categories(db: Session = Depends(get_db)):
    response, err = IssueCategoryService.list_all(db)
    if err:
        return JSONResponse(status_code=500, content={"status": "error", "message": err})

    return JSONResponse(status_code=200, content={"status": "success", "data": response})



@issue_category_router.put("/issue-categories/{category_id}")
def update_category(
    category_id: int,
    payload: IssueCategoryUpdateRequest,
    db: Session = Depends(get_db),
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    user, err = AuthMiddleware.get_current_user(credentials, db)
    if err:
        return JSONResponse(status_code=401, content={"status": "error", "message": err})

    if not RoleGuard.has_role(user, ["admin"]):
        return JSONResponse(status_code=403, content={"status": "error", "message": "Only admins can update categories"})

    response, err = IssueCategoryService.update(category_id, payload, db)
    if err:
        return JSONResponse(status_code=400, content={"status": "error", "message": err})

    return JSONResponse(status_code=200, content={"status": "success", "data": response})


@issue_category_router.delete("/issue-categories/{category_id}")
def delete_category(
    category_id: int,
    db: Session = Depends(get_db),
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    user, err = AuthMiddleware.get_current_user(credentials, db)
    if err:
        return JSONResponse(status_code=401, content={"status": "error", "message": err})

    if not RoleGuard.has_role(user, ["admin"]):
        return JSONResponse(status_code=403, content={"status": "error", "message": "Only admins can delete categories"})

    success, err = IssueCategoryService.delete(category_id, db)
    if err:
        return JSONResponse(status_code=400, content={"status": "error", "message": err})

    return JSONResponse(status_code=200, content={"status": "success", "message": "Category deleted successfully"})
