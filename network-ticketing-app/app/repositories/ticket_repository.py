from app.models.ticket import Ticket
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

class TicketRepository:
    @staticmethod
    def create_ticket(user_id: int, ticket_data, db, created_at, updated_at, due_date):
        try:
            new_ticket = Ticket(
                issue_description=ticket_data.issue_description,
                issue_category_id=ticket_data.issue_category_id,
                created_by=user_id,
                status="new",
                created_at=created_at,
                updated_at=updated_at,
                due_date=due_date
            )
            db.add(new_ticket)
            db.commit()
            db.refresh(new_ticket)
            return new_ticket, None
        except SQLAlchemyError as e:
            db.rollback()
            return None, f"DB error during ticket creation: {str(e)}"
        except Exception as e:
            db.rollback()
            return None, f"Unexpected error: {str(e)}"

    @staticmethod
    def get_tickets_without_sla(db):
        try:
            return db.query(Ticket).filter(Ticket.sla_id == None).all()
        except SQLAlchemyError as e:
            return None, f"DB error while fetching unclassified tickets: {str(e)}"
        except Exception as e:
            return None, f"Unexpected error: {str(e)}"

    @staticmethod
    def get_ticket_by_id(ticket_id: int, db: Session):
        try:
            ticket = db.query(Ticket).filter_by(ticket_id=ticket_id).first()
            if not ticket:
                return None, "Ticket not found"
            return ticket, None
        except SQLAlchemyError as e:
            db.rollback()
            return None, f"Database error while fetching ticket: {str(e)}"
        except Exception as e:
            db.rollback()
            return None, f"Unexpected error while fetching ticket: {str(e)}"

    @staticmethod
    def classify_ticket(ticket_id: int, severity, priority, sla_id, due_date, db):
        try:
            ticket = db.query(Ticket).filter(Ticket.ticket_id == ticket_id).first()
            if not ticket:
                return None, "Ticket not found"

            ticket.severity = severity
            ticket.priority = priority
            ticket.sla_id = sla_id
            ticket.due_date = due_date
            ticket.updated_at = datetime.utcnow()

            db.commit()
            db.refresh(ticket)
            return ticket, None
        except SQLAlchemyError as e:
            db.rollback()
            return None, f"DB error during classification: {str(e)}"
        except Exception as e:
            db.rollback()
            return None, f"Unexpected error: {str(e)}"

    @staticmethod
    def assign_ticket(ticket_id: int, assigned_to: int, db):
        try:
            ticket = db.query(Ticket).filter(Ticket.ticket_id == ticket_id).first()
            if not ticket:
                return None, "Ticket not found"

            ticket.assigned_to = assigned_to
            ticket.status = "assigned"
            ticket.updated_at = datetime.utcnow()

            db.commit()
            db.refresh(ticket)
            return ticket, None
        except SQLAlchemyError as e:
            db.rollback()
            return None, f"DB error during assignment: {str(e)}"
        except Exception as e:
            db.rollback()
            return None, f"Unexpected error: {str(e)}"

    @staticmethod
    def update_status(ticket_id: int, new_status: str, db):
        try:
            ticket = db.query(Ticket).filter(Ticket.ticket_id == ticket_id).first()
            if not ticket:
                return None, "Ticket not found"

            ticket.status = new_status
            ticket.updated_at = datetime.utcnow()

            db.commit()
            db.refresh(ticket)
            return ticket, None
        except SQLAlchemyError as e:
            db.rollback()
            return None, f"DB error during status update: {str(e)}"
        except Exception as e:
            db.rollback()
            return None, f"Unexpected error: {str(e)}"
    
    @staticmethod
    def update_status(ticket_id, new_status, db):
        try:
            ticket = db.query(Ticket).filter_by(ticket_id=ticket_id).first()
            if not ticket:
                return None, "Ticket not found"

            ticket.status = new_status
            db.commit()
            db.refresh(ticket)
            return ticket, None
        except SQLAlchemyError as e:
            db.rollback()
            return None, f"Database error during status update: {str(e)}"
        except Exception as e:
            db.rollback()
            return None, f"Unexpected error during status update: {str(e)}"

    @staticmethod
    def get_tickets_by_assignee(user_id, status, db):
        try:
            query = db.query(Ticket).filter(Ticket.assigned_to == user_id)
            if status:
                query = query.filter(Ticket.status == status)
            tickets = query.all()
            return tickets, None
        except SQLAlchemyError as e:
            return None, f"Database error while fetching assigned tickets: {str(e)}"
        except Exception as e:
            return None, f"Unexpected error while fetching assigned tickets: {str(e)}"