# app/router.py
from fastapi import APIRouter
from app.views.auth_view import auth_router
from app.views.user_view import user_router
from app.views.ticket_view import ticket_router
from app.views.issue_category_view import issue_category_router
from app.views.sla_view import sla_router
from app.views.address_view import address_router

network_ticketing_router = APIRouter()
network_ticketing_router.include_router(auth_router,prefix="/auth", tags = ["authentication"])
network_ticketing_router.include_router(user_router,prefix="/user", tags = ["user"])
network_ticketing_router.include_router(ticket_router,prefix="/tickets", tags = ["tickets"])
network_ticketing_router.include_router(issue_category_router,prefix="/issue/category", tags = ["issue category"])
network_ticketing_router.include_router(sla_router,prefix="/sla", tags = ["SLA"])
network_ticketing_router.include_router(address_router,prefix="/address", tags = ["address"] )
