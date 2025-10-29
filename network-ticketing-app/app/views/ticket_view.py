from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from fastapi.security import HTTPAuthorizationCredentials
from fastapi.responses import JSONResponse
from app.dependencies.auth import AuthMiddleware, security
from app.services.ticket_service import TicketService
from app.schemas.ticket import (
    TicketCreateRequest,
    AssignTicketRequest,
    UpdateStatusRequest,
    ClassifyTicketRequest,
    UpdateTicketRequest
)
from app.database import get_db

ticket_router = APIRouter()

# 🎫 Create Ticket
@ticket_router.post("/tickets")
def create_ticket(
    ticket_data: TicketCreateRequest,
    db: Session = Depends(get_db),
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    user, err = AuthMiddleware.get_current_user(credentials, db)
    if err:
        return JSONResponse(status_code=401, content={"status": "error", "message": err})

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
                "issue_category_id": ticket.issue_category_id,
                "sla_id": ticket.sla_id,
                "assigned_to": ticket.assigned_to,
                "created_at": str(ticket.created_at),
                "updated_at": str(ticket.updated_at),
                "due_date": str(ticket.due_date) if ticket.due_date else None,
                "address_id": ticket.address_id  
            }
        }
    )



# 🧮 Get Unclassified Tickets
@ticket_router.get("/tickets/unclassified")
def get_unclassified_tickets(
    db: Session = Depends(get_db),
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    user, err = AuthMiddleware.get_current_user(credentials, db)
    if err:
        return JSONResponse(status_code=401, content={"status": "error", "message": err})

    tickets, err = TicketService.get_unclassified_tickets(user, db)
    if err:
        return JSONResponse(status_code=403, content={"status": "error", "message": err})

    return JSONResponse(
        status_code=200,
        content={
            "status": "success",
            "message": "Unclassified tickets fetched",
            "data": [  # Simplified list
                {
                    "ticket_id": t.ticket_id,
                    "issue_description": t.issue_description,
                    "status": t.status.value if t.status else None,
                    "created_by": t.created_by,
                    "created_at": str(t.created_at)
                } for t in tickets
            ]
        }
    )

# 🛠️ Classify Ticket
@ticket_router.patch("/tickets/{ticket_id}/classify")
def classify_ticket(
    ticket_id: int,
    payload: ClassifyTicketRequest,
    db: Session = Depends(get_db),
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    user, err = AuthMiddleware.get_current_user(credentials, db)
    if err:
        return JSONResponse(status_code=401, content={"status": "error", "message": err})

    ticket, err = TicketService.classify_ticket(user, ticket_id, payload, db)
    if err:
        return JSONResponse(status_code=403, content={"status": "error", "message": err})

    return JSONResponse(
        status_code=200,
        content={
            "status": "success",
            "message": "Ticket classified successfully",
            "data": {
                "ticket_id": ticket.ticket_id,
                "severity": ticket.severity.value if ticket.severity else None,
                "priority": ticket.priority.value if ticket.priority else None,
                "sla_id": ticket.sla_id,
                "due_date": str(ticket.due_date) if ticket.due_date else None
            }
        }
    )

# 👷 Assign Ticket
@ticket_router.put("/tickets/{ticket_id}/assign")
def assign_ticket(
    ticket_id: int,
    payload: AssignTicketRequest,
    db: Session = Depends(get_db),
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    user, err = AuthMiddleware.get_current_user(credentials, db)
    if err:
        return JSONResponse(status_code=401, content={"status": "error", "message": err})

    ticket, err = TicketService.assign_ticket(user, ticket_id, payload, db)
    if err:
        return JSONResponse(
            status_code=403 if "Only admins" in err else 400,
            content={"status": "error", "message": err}
        )

    return JSONResponse(
        status_code=200,
        content={
            "status": "success",
            "message": "Ticket assigned successfully",
            "data": {
                "ticket_id": ticket.ticket_id,
                "assigned_to": ticket.assigned_to,
                "status": ticket.status.value if ticket.status else None
            }
        }
    )

# 🔄 Update Ticket Status
@ticket_router.patch("/tickets/{ticket_id}/status")
def change_ticket_status(
    ticket_id: int,
    payload: UpdateStatusRequest,
    db: Session = Depends(get_db),
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    user, err = AuthMiddleware.get_current_user(credentials, db)
    if err:
        return JSONResponse(status_code=401, content={"status": "error", "message": err})

    ticket, err = TicketService.change_ticket_status(user, ticket_id, payload.status.value, db)
    if err:
        return JSONResponse(status_code=403, content={"status": "error", "message": err})

    return JSONResponse(
        status_code=200,
        content={
            "status": "success",
            "message": f"Ticket status updated to '{ticket.status.value}'",
            "data": {
                "ticket_id": ticket.ticket_id,
                "status": ticket.status.value
            }
        }
    )


@ticket_router.get("/tickets/assigned")
def get_assigned_tickets(
    status: str = None,
    db: Session = Depends(get_db),
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    user, err = AuthMiddleware.get_current_user(credentials, db)
    if err:
        return JSONResponse(status_code=401, content={"status": "error", "message": err})

    tickets, err = TicketService.get_engineer_tickets(user, status, db)
    if err:
        return JSONResponse(status_code=400, content={"status": "error", "message": err})

    return JSONResponse(
        status_code=200,
        content={
            "status": "success",
            "message": "Assigned tickets fetched",
            "data": [
                {
                    "ticket_id": t.ticket_id,
                    "issue_description": t.issue_description,
                    "status": t.status.value if t.status else None,
                    "severity": t.severity.value if t.severity else None,
                    "priority": t.priority.value if t.priority else None,
                    "sla_id": t.sla_id,
                    "assigned_to": t.assigned_to,
                    "created_at": str(t.created_at),
                    "due_date": str(t.due_date) if t.due_date else None
                } for t in tickets
            ]
        }
    )



@ticket_router.put("/tickets/{ticket_id}/start")
def start_ticket_work(
    ticket_id: int,
    db: Session = Depends(get_db),
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    user, err = AuthMiddleware.get_current_user(credentials, db)
    if err:
        return JSONResponse(status_code=401, content={"status": "error", "message": err})

    ticket, err = TicketService.start_ticket_work(user, ticket_id, db)
    if err:
        return JSONResponse(
            status_code=403 if "not assigned" in err else 400,
            content={"status": "error", "message": err}
        )

    return JSONResponse(
        status_code=200,
        content={
            "status": "success",
            "message": "Ticket marked as in progress",
            "data": {
                "ticket_id": ticket.ticket_id,
                "status": ticket.status.value
            }
        }
    )



@ticket_router.get("/tickets/{ticket_id}")
def get_ticket_details(
    ticket_id: int,
    db: Session = Depends(get_db),
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    user, err = AuthMiddleware.get_current_user(credentials, db)
    if err:
        return JSONResponse(status_code=401, content={"status": "error", "message": err})

    ticket, err = TicketService.get_ticket_details(user, ticket_id, db)
    if err:
        return JSONResponse(
            status_code=403 if "not assigned" in err else 404,
            content={"status": "error", "message": err}
        )

    return JSONResponse(
        status_code=200,
        content={
            "status": "success",
            "message": "Ticket details fetched successfully",
            "data": {
                "ticket_id": ticket.ticket_id,
                "status": ticket.status.value,
                "assigned_to": ticket.assigned_to,
                "created_by": ticket.created_by,
                "issue_description": ticket.issue_description,
                "severity": ticket.severity.value if ticket.severity else None,
                "priority": ticket.priority.value if ticket.priority else None,
                "issue_category_id": ticket.issue_category_id,
                "sla_id": ticket.sla_id,
                "created_at": str(ticket.created_at),
                "updated_at": str(ticket.updated_at),
                "due_date": str(ticket.due_date) if ticket.due_date else None
            }
        }
    )



# customer can edit the raised ticket
@ticket_router.put("/{ticket_id}/edit")
def edit_ticket_by_customer(
    ticket_id: int,
    payload: UpdateTicketRequest,
    db: Session = Depends(get_db),
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    user, err = AuthMiddleware.get_current_user(credentials, db)
    if err:
        return JSONResponse(status_code=401, content={"status": "error", "message": err})

    ticket, err = TicketService.update_ticket_by_customer(ticket_id, payload, db, user)
    if err:
        return JSONResponse(
            status_code=403 if "Only customers" in err else 400,
            content={"status": "error", "message": err}
        )

    return JSONResponse(
        status_code=200,
        content={
            "status": "success",
            "message": "Ticket updated successfully",
            "data": {
                "ticket_id": ticket.ticket_id,
                "issue_description": ticket.issue_description,
                "issue_category_id": ticket.issue_category_id,
                "address_id": ticket.address_id,
                "updated_at": str(ticket.updated_at)
            }
        }
    )



# customers can delete their raised ticket
@ticket_router.delete("/{ticket_id}/delete")
def delete_ticket_by_customer(
    ticket_id: int,
    db: Session = Depends(get_db),
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    user, err = AuthMiddleware.get_current_user(credentials, db)
    if err:
        return JSONResponse(status_code=401, content={"status": "error", "message": err})

    success, err = TicketService.delete_ticket_by_customer(ticket_id, db, user)
    if err:
        status_code = 403 if "Only customers" in err or "unauthorized" in err else 400
        return JSONResponse(status_code=status_code, content={"status": "error", "message": err})

    if not success:
        return JSONResponse(status_code=500, content={"status": "error", "message": "Unknown error during deletion"})

    return JSONResponse(
        status_code=200,
        content={"status": "success", "message": "Ticket deleted successfully"}
    )
