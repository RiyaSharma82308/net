from datetime import datetime, timedelta
from app.models.sla import SLA
from app.models.issue_category import IssueCategory
from app.repositories.ticket_repository import TicketRepository
from app.repositories.assignment_repository import AssignmentRepository
from app.repositories.user_repository import UserRepository
from app.schemas.ticket import ClassifyTicketRequest
from sqlalchemy.orm import Session

class TicketService:
    @staticmethod
    def create_ticket(user, ticket_data, db):
        if user.role.value not in ["customer", "admin"]:
            return None, "Only customers and admins can create tickets"

        category = db.query(IssueCategory).filter_by(category_id=ticket_data.issue_category_id).first()
        if not category:
            return None, f"Issue category with ID {ticket_data.issue_category_id} does not exist"

        now = datetime.utcnow()
        ticket, err = TicketRepository.create_ticket(
            user_id=user.user_id,
            ticket_data=ticket_data,
            db=db,
            created_at=now,
            updated_at=now,
            due_date=None
        )
        if err:
            return None, f"Ticket creation failed: {err}"

        return ticket, None

    @staticmethod
    def get_unclassified_tickets(user, db):
        if user.role.value not in ["admin", "manager", "agent"]:
            return None, "Only authorized roles can view unclassified tickets"

        tickets = TicketRepository.get_tickets_without_sla(db)
        if tickets is None:
            return None, "Failed to fetch unclassified tickets"

        return tickets, None

    @staticmethod
    def classify_ticket(user, ticket_id: int, payload: ClassifyTicketRequest, db):
        if user.role.value not in ["admin", "manager", "agent"]:
            return None, "Only authorized roles can classify tickets"

        ticket, err = TicketRepository.get_ticket_by_id(ticket_id, db)
        if err:
            return None, err
        if not ticket:
            return None, "Ticket not found"

        sla = db.query(SLA).filter_by(sla_id=payload.sla_id).first()
        if not sla:
            return None, f"SLA with ID {payload.sla_id} does not exist"

        due_date = datetime.utcnow() + timedelta(hours=sla.time_limit_hr)

        ticket, err = TicketRepository.classify_ticket(
            ticket_id=ticket_id,
            severity=payload.severity,
            priority=payload.priority,
            sla_id=payload.sla_id,
            due_date=due_date,
            db=db
        )
        if err:
            return None, f"Classification failed: {err}"

        return ticket, None

    @staticmethod
    def assign_ticket(user, ticket_id, payload, db):
        if user.role.value != "admin":
            return None, "Only admins can assign tickets"

        engineer = UserRepository.get_user_by_id(payload.assigned_to, db)
        if not engineer or engineer.role.value != "engineer":
            return None, "Assigned user must be a valid engineer"

        ticket, err = TicketRepository.get_ticket_by_id(ticket_id, db)
        if err:
            return None, err
        if not ticket:
            return None, "Ticket not found"

        # ✅ Ensure ticket is classified before assignment
        if not ticket.severity or not ticket.priority or not ticket.sla_id:
            return None, "Ticket must be classified (severity, priority, SLA) before assignment"

        # ✅ Ensure ticket is in a valid state for assignment
        if ticket.status.value not in ["new", "reopened"]:
            return None, f"Ticket with status '{ticket.status.value}' cannot be assigned"

        ticket, err = TicketRepository.assign_ticket(ticket_id, payload.assigned_to, db)
        if err:
            return None, f"Assignment failed: {err}"

        _, log_err = AssignmentRepository.log_assignment(
            ticket_id=ticket_id,
            assigned_to=payload.assigned_to,
            assigned_by=user.user_id,
            db=db
        )
        if log_err:
            return None, f"Assignment log failed: {log_err}"

        return ticket, None



    @staticmethod
    def change_ticket_status(user, ticket_id, new_status: str, db):
        ticket, err = TicketRepository.get_ticket_by_id(ticket_id, db)
        if err:
            return None, err
        if not ticket:
            return None, "Ticket not found"

        current_status = ticket.status.value

        # Engineer rules
        if user.role.value == "engineer":
            if ticket.assigned_to != user.user_id:
                return None, "You are not assigned to this ticket"
            if new_status not in ["on_hold", "resolved"]:
                return None, "Engineers can only change status to 'on_hold' or 'resolved'"
            if current_status not in ["assigned", "in_progress", "on_hold"]:
                return None, f"Cannot change status from '{current_status}'"

        # Admin rules
        elif user.role.value == "admin":
            if new_status == "closed" and current_status != "resolved":
                return None, "Ticket must be resolved before it can be closed"
            if new_status == "reopened" and current_status != "closed":
                return None, "Only closed tickets can be reopened"
            if new_status not in ["closed", "reopened"]:
                return None, "Admins can only change status to 'closed' or 'reopened'"

        else:
            return None, "Only engineers or admins can change ticket status"

        ticket, err = TicketRepository.update_status(ticket_id, new_status, db)
        if err:
            return None, f"Failed to update status: {err}"

        return ticket, None


    @staticmethod
    def get_engineer_tickets(user, status_filter, db):
        if user.role.value != "engineer":
            return None, "Only engineers can view assigned tickets"

        tickets, err = TicketRepository.get_tickets_by_assignee(
            user_id=user.user_id,
            status=status_filter,
            db=db
        )
        if err:
            return None, err

        return tickets, None
    
    @staticmethod
    def start_ticket_work(user, ticket_id, db):
        if user.role.value != "engineer":
            return None, "Only engineers can start ticket work"

        ticket, err = TicketRepository.get_ticket_by_id(ticket_id, db)
        if err:
            return None, err
        if not ticket:
            return None, "Ticket not found"

        if ticket.assigned_to != user.user_id:
            return None, "You are not assigned to this ticket"

        if ticket.status.value == "resolved":
            return None, "Ticket is already resolved"
        
        if ticket.status.value.lower() not in ["new", "assigned"]:
            return None, f"Cannot start ticket with status '{ticket.status.value}'"

        ticket, err = TicketRepository.update_status(ticket_id, "in_progress", db)
        if err:
            return None, f"Failed to update ticket status: {err}"

        return ticket, None


    @staticmethod
    def get_ticket_details(user, ticket_id: int, db: Session):
        ticket, err = TicketRepository.get_ticket_by_id(ticket_id, db)
        if err:
            return None, err
        if not ticket:
            return None, "Ticket not found"

        # 👷 Engineer can only view tickets assigned to them
        if user.role.value == "engineer" and ticket.assigned_to != user.user_id:
            return None, "You are not assigned to this ticket"

        # 👩‍💼 Admin can view any ticket — no restriction
        return ticket, None