# app/router.py
from fastapi import APIRouter
from app.views.auth_view import router as auth_router
# from app.views.ticket_view import router as ticket_router

router = APIRouter()
router.include_router(auth_router)
# router.include_router(ticket_router)
