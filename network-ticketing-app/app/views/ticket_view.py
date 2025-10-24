from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from fastapi.security import HTTPAuthorizationCredentials
from fastapi.responses import JSONResponse
from app.dependencies.auth import AuthMiddleware, security
from app.services.ticket_service import TicketService
from app.schemas.ticket import TicketCreateRequest
from app.database import get_db

ticket_router = APIRouter()

@ticket_router.post("/tickets")
def create_ticket(
    ticket_data: TicketCreateRequest,
    db: Session = Depends(get_db),
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    user, err = AuthMiddleware.get_current_user(credentials, db)
    if err:
        return JSONResponse(
            status_code=401,
            content={"status": "error", "message": err}
        )

    ticket, err = TicketService.create_ticket(user, ticket_data, db)
    if err:
        return JSONResponse(
            status_code=403 if "Only users" in err else 500,
            content={"status": "error", "message": err}
        )

    return JSONResponse(
        status_code=201,
        content={
            "status": "success",
            "message": "Ticket created successfully",
            "data": {
                "ticket_id": ticket.ticket_id,
                "created_by": ticket.created_by,
                "issue_description": ticket.issue_description,
                "status": ticket.status.value if ticket.status else None,
                "severity": ticket.severity.value if ticket.severity else None,
                "priority": ticket.priority.value if ticket.priority else None,
                "assigned_to": ticket.assigned_to,
                "created_at": str(ticket.created_at),
                "updated_at": str(ticket.updated_at)
            }
        }
    )
