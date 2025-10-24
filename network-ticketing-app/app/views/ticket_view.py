from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from fastapi.security import HTTPAuthorizationCredentials
from app.dependencies.auth import AuthMiddleware, security
from app.services.ticket_service import TicketService
from app.schemas.ticket import TicketCreateRequest, TicketResponse
from app.database import get_db

ticket_router = APIRouter()

@ticket_router.post("/tickets", response_model=TicketResponse)
def create_ticket(ticket_data: TicketCreateRequest, db: Session = Depends(get_db), credentials: HTTPAuthorizationCredentials = Depends(security)):
    user, err = AuthMiddleware.get_current_user(credentials, db)
    if err:
        return {"status": "error", "message": err}, 401

    ticket, err = TicketService.create_ticket(user, ticket_data, db)
    if err:
        return {"status": "error", "message": err}, 403 if "Only users" in err else 500

    return ticket, 201