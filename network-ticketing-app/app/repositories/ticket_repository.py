from app.models.ticket import Ticket
from app.models.address import Address
from app.models.issue_category import IssueCategory
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from app.schemas.ticket import UpdateTicketRequest


class TicketRepository:
    @staticmethod
    def create_ticket(user_id: int, ticket_data, db, created_at, updated_at, due_date, address_id: int):
        try:
            new_ticket = Ticket(
                issue_description=ticket_data.issue_description,
                issue_category_id=ticket_data.issue_category_id,
                created_by=user_id,
                address_id=address_id,  
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
        

    @staticmethod
    def list_by_user(user_id: int, db):
        try:
            tickets = db.query(Ticket).filter(Ticket.created_by == user_id).all()
            return tickets, None
        except Exception as e:
            return None, str(e)
        


    @staticmethod
    def update_ticket_by_customer(ticket_id: int, user_id: int, payload, db: Session):
        try:
            ticket = db.query(Ticket).filter_by(ticket_id=ticket_id, created_by=user_id).first()
            if not ticket:
                return None, "Ticket not found or unauthorized"

            ticket.issue_description = payload.issue_description
            ticket.issue_category_id = payload.issue_category_id
            ticket.address_id = payload.address_id
            ticket.updated_at = datetime.utcnow()

            db.commit()
            db.refresh(ticket)
            return ticket, None
        except SQLAlchemyError as e:
            db.rollback()
            return None, f"DB error during ticket update: {str(e)}"
        except Exception as e:
            db.rollback()
            return None, f"Unexpected error: {str(e)}"


    @staticmethod
    def delete_ticket_by_customer(ticket_id: int, user_id: int, db: Session):
        try:
            ticket = db.query(Ticket).filter_by(ticket_id=ticket_id, created_by=user_id).first()
            if not ticket:
                return None, "Ticket not found or unauthorized"

            db.delete(ticket)
            db.commit()
            return True, None
        except SQLAlchemyError as e:
            db.rollback()
            return None, f"Database error during deletion: {str(e)}"
        except Exception as e:
            db.rollback()
            return None, f"Unexpected error during deletion: {str(e)}"


    @staticmethod
    def get_address_by_id(address_id: int, user_id: int, db: Session):
        try:
            address = db.query(Address).filter_by(address_id=address_id, user_id=user_id).first()
            if not address:
                return None, "Address not found or unauthorized"
            return address, None
        except SQLAlchemyError as e:
            db.rollback()
            return None, f"Database error while fetching address: {str(e)}"
        except Exception as e:
            db.rollback()
            return None, f"Unexpected error while fetching address: {str(e)}"



    @staticmethod
    def get_issue_category_by_id(category_id: int, db: Session):
        try:
            category = db.query(IssueCategory).filter_by(category_id=category_id).first()
            if not category:
                return None, "Issue category not found"
            return category, None
        except Exception as e:
            db.rollback()
            return None, f"Database error while fetching issue category: {str(e)}"



    @staticmethod
    def get_ticket_by_customer(ticket_id: int, user_id: int, db: Session):
        try:
            ticket = db.query(Ticket).filter_by(ticket_id=ticket_id, created_by=user_id).first()
            if not ticket:
                return None, "Ticket not found or unauthorized"
            return ticket, None
        except Exception as e:
            db.rollback()
            return None, f"Database error while fetching ticket: {str(e)}"

    @staticmethod
    def update_ticket(ticket: Ticket, payload: UpdateTicketRequest, db: Session):
        try:
            ticket.issue_description = payload.issue_description
            ticket.issue_category_id = payload.issue_category_id
            ticket.address_id = payload.address_id
            db.commit()
            db.refresh(ticket)
            return ticket, None
        except Exception as e:
            db.rollback()
            return None, f"Database error while updating ticket: {str(e)}"



    @staticmethod
    def get_classified_tickets(db):
        try:
            tickets = db.query(Ticket).filter(
                Ticket.status == "new",
                Ticket.priority.isnot(None),
                Ticket.severity.isnot(None),
                Ticket.assigned_to.is_(None)
            ).all()
            return tickets, None
        except Exception as e:
            return None, str(e)

        

    @staticmethod
    def get_all_with_users(db):
        try:
            # Fetch all tickets and eager-load user relationships
            tickets = db.query(Ticket).all()
            return tickets, None
        except Exception as e:
            return None, str(e)
        

    @staticmethod
    def update_status(ticket_id, new_status, db):
        try:
            ticket = db.query(Ticket).filter_by(ticket_id=ticket_id).first()
            if not ticket:
                return None, "Ticket not found"

            ticket.status = new_status
            ticket.updated_at = datetime.utcnow()
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
    def update_status(ticket_id: int, new_status: str, db: Session):
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
            return None, str(e)