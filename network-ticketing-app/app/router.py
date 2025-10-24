# app/router.py
from fastapi import APIRouter
from app.views.auth_view import auth_router
from app.views.ticket_view import ticket_router

network_ticketing_router = APIRouter()
print("router loaded!!!!!!!!!!!!")
network_ticketing_router.include_router(auth_router,prefix="/auth")
network_ticketing_router.include_router(ticket_router,prefix="/tickets")

