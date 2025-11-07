from datetime import datetime, timedelta
from app.models.sla import SLA
from app.models.issue_category import IssueCategory
from app.models.address import Address
from app.repositories.ticket_repository import TicketRepository
from app.repositories.assignment_repository import AssignmentRepository
from app.repositories.user_repository import UserRepository
from app.schemas.ticket import ClassifyTicketRequest, TicketResponse
from sqlalchemy.orm import Session
from datetime import datetime
from app.schemas.ticket import UpdateTicketRequest



class TicketService:
    @staticmethod
    def create_ticket(user, ticket_data, db):
        if user.role.value != "customer":
            return None, "Only customers can create tickets"

        # Validate issue category
        category = db.query(IssueCategory).filter_by(category_id=ticket_data.issue_category_id).first()
        if not category:
            return None, f"Issue category with ID {ticket_data.issue_category_id} does not exist"

        # ✅ Validate address
        address = db.query(Address).filter_by(address_id=ticket_data.address_id, user_id=user.user_id).first()
        if not address:
            return None, f"Chosen address does not belong to the user"

        # ✅ Create ticket
        now = datetime.utcnow()
        ticket, err = TicketRepository.create_ticket(
            user_id=user.user_id,
            ticket_data=ticket_data,
            db=db,
            created_at=now,
            updated_at=now,
            due_date=None,
            address_id=ticket_data.address_id  # ✅ Pass address_id
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
        if user.role.value == "customer":
            return None, "Customers can't assign tickets!"

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
            if new_status not in ["on_hold", "resolved", "in_progress"]:
                return None, "Engineers can only change status to 'on_hold', 'in_progress' or 'resolved'"
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
    

    @staticmethod
    def list_by_user(user_id: int, db):
        tickets, err = TicketRepository.list_by_user(user_id, db)
        if err:
            return None, f"Failed to fetch tickets: {err}"

        formatted = [TicketService._format_ticket(t) for t in tickets]
        return formatted, None

    @staticmethod
    def _format_ticket(ticket):
        return {
            "ticket_id": ticket.ticket_id,
            "created_by": ticket.created_by,
            "issue_description": ticket.issue_description,
            "status": ticket.status.value if hasattr(ticket.status, "value") else ticket.status,
            "severity": ticket.severity.value if ticket.severity else None,
            "priority": ticket.priority.value if ticket.priority else None,
            "issue_category_id": ticket.issue_category_id,
            "sla_id": ticket.sla_id,
            "assigned_to": ticket.assigned_to,
            "created_at": ticket.created_at.isoformat() if ticket.created_at else None,
            "updated_at": ticket.updated_at.isoformat() if ticket.updated_at else None,
            "due_date": ticket.due_date.isoformat() if ticket.due_date else None
        }
    


    
    @staticmethod
    def update_ticket_by_customer(ticket_id: int, payload: UpdateTicketRequest, db: Session, user):
        if user.role.value != "customer":
            return None, "Only customers can edit their own tickets"

        # Validate required fields
        if not payload.issue_description or not payload.issue_category_id or not payload.address_id:
            return None, "Missing required fields"

        # Fetch ticket
        ticket, err = TicketRepository.get_ticket_by_customer(ticket_id, user.user_id, db)
        if err:
            return None, err

        # Update ticket
        updated_ticket, err = TicketRepository.update_ticket(ticket, payload, db)
        if err:
            return None, err

        return updated_ticket, None



    
    @staticmethod
    def delete_ticket_by_customer(ticket_id: int, db: Session, user):
        if user.role.value != "customer":
            return None, "Only customers can delete their tickets"

        ticket, err = TicketRepository.get_ticket_by_id(ticket_id, db)
        if err:
            return None, err
        if not ticket:
            return None, "Ticket not found"
        if ticket.created_by != user.user_id:
            return None, "You are not authorized to delete this ticket"

        success, err = TicketRepository.delete_ticket_by_customer(ticket_id, user.user_id, db)
        if err:
            return None, err
        return success, None


    @staticmethod
    def get_ticket_summary_for_customer(ticket_id: int, user, db: Session):
        print("user is: ", user.role.value)
        if user.role.value != "customer":
            return None, "Only customers can view their own tickets"

        ticket, err = TicketRepository.get_ticket_by_id(ticket_id, db)
        if err:
            return None, err
        if not ticket:
            return None, "Ticket not found"
        if ticket.created_by != user.user_id:
            return None, "You are not authorized to view this ticket"

        address, err = TicketRepository.get_address_by_id(ticket.address_id, user.user_id, db)
        if err:
            return None, err
        if not address:
            return None, "Address not found or unauthorized"

        category, err = TicketRepository.get_issue_category_by_id(ticket.issue_category_id, db)
        if err:
            return None, err
        if not category:
            return None, "Issue category not found"

        full_address = f"{address.street}, {address.city}, {address.state}, {address.postal_code}, {address.country}"

        return {
            "ticket_id": ticket.ticket_id,
            "issue_description": ticket.issue_description,
            "address": full_address,
            "status": ticket.status,
            "issue_category_id": ticket.issue_category_id,
            "issue_category_name": category.category_name
        }, None



    @staticmethod
    def get_classified_tickets(user, db):
        if user.role.value not in ["admin", "manager", "agent"]:
            return None, "Only authorized roles can view classified tickets"

        tickets, err = TicketRepository.get_classified_tickets(db)
        if err:
            return None, f"Error fetching classified tickets: {err}"
        if not tickets:
            return [], None

        response = [
            TicketResponse(
                ticket_id=t.ticket_id,
                issue_description=t.issue_description,
                status=t.status.value if hasattr(t.status, "value") else t.status,
                priority=t.priority.value if t.priority else None,
                severity=t.severity.value if t.severity else None,
                created_by=t.created_by,
                assigned_to=t.assigned_to,
                issue_category_id=t.issue_category_id,
                address_id=t.address_id,
                sla_id=t.sla_id,
                created_at=t.created_at,
                updated_at=t.updated_at,
                due_date=t.due_date
            ).model_dump(mode="json")
            for t in tickets
        ]

        return response, None



    @staticmethod
    def get_all_tickets_with_users(db):
        tickets, err = TicketRepository.get_all_with_users(db)
        if err:
            return None, f"Error fetching tickets: {err}"

        response = []
        for t in tickets:
            response.append({
                "ticket_id": t.ticket_id,
                "issue_description": t.issue_description,
                "status": t.status.value if t.status else None,
                "priority": t.priority.value if t.priority else None,
                "severity": t.severity.value if t.severity else None,
                "created_at": t.created_at.isoformat() if t.created_at else None,
                "updated_at": t.updated_at.isoformat() if t.updated_at else None,
                "due_date": t.due_date.isoformat() if t.due_date else None,
                "created_by": {
                    "user_id": t.creator.user_id if t.creator else None,
                    "name": t.creator.name if t.creator else None,
                    "email": t.creator.email if t.creator else None,
                    "role": t.creator.role.value if t.creator and t.creator.role else None,
                    "contact_number": t.creator.contact_number if t.creator else None,
                    "location": t.creator.location if t.creator else None
                },
                "assigned_to": {
                    "user_id": t.assignee.user_id if t.assignee else None,
                    "name": t.assignee.name if t.assignee else None,
                    "email": t.assignee.email if t.assignee else None,
                    "role": t.assignee.role.value if t.assignee and t.assignee.role else None,
                    "contact_number": t.assignee.contact_number if t.assignee else None,
                    "location": t.assignee.location if t.assignee else None
                }
            })

        return response, None
    

    @staticmethod
    def update_ticket_status_by_agent(ticket_id: int, new_status: str, db: Session):
        # ✅ Fetch ticket
        ticket, err = TicketRepository.get_ticket_by_id(ticket_id, db)
        if err:
            return None, err
        if not ticket:
            return None, "Ticket not found"

        current_status = ticket.status.value.lower()
        new_status = new_status.lower()

        # ✅ Define valid transitions
        valid_transitions = {
            "resolved": ["closed"],
            "closed": ["reopened"]
        }

        # ✅ Validate current status
        if current_status not in valid_transitions:
            return None, f"Tickets with status '{current_status}' cannot be modified by agent"

        # ✅ Validate next status
        allowed_next = valid_transitions[current_status]
        if new_status not in allowed_next:
            return None, f"Invalid transition: '{current_status}' → '{new_status}'"

        # ✅ Update via repository
        updated_ticket, err = TicketRepository.update_status(ticket_id, new_status, db)
        if err:
            return None, f"Failed to update ticket status: {err}"

        return updated_ticket, None



    @staticmethod
    def reopen_ticket_by_customer(ticket_id: int, db: Session, user):
            # ✅ Role check
        if user.role.value != "customer":
            return None, "Only customers can reopen tickets"

            # ✅ Fetch ticket
        ticket, err = TicketRepository.get_ticket_by_id(ticket_id, db)
        if err:
            return None, err
        if not ticket:
            return None, "Ticket not found"

            # ✅ Ownership check
        if ticket.created_by != user.user_id:
            return None, "You are not authorized to reopen this ticket"

            # ✅ Status check
        if ticket.status.value.lower() not in ["resolved", "closed"]:
            return None, f"Only resolved or closed tickets can be reopened (current: {ticket.status.value})"

            # ✅ Optional — Time window (48 hours)
        if ticket.updated_at:
            time_diff = datetime.utcnow() - ticket.updated_at
            if time_diff.total_seconds() > 48 * 3600:
                return None, "Reopen window expired (only within 48 hours allowed)"

            # ✅ Update status to 'reopened'
        updated_ticket, err = TicketRepository.update_status(ticket_id, "reopened", db)
        if err:
            return None, err

        return updated_ticket, None



        
