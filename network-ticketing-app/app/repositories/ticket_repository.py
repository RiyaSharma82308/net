from app.models.ticket import Ticket
from datetime import datetime

class TicketRepository:
    @staticmethod
    def create_ticket(user_id: int, ticket_data, db):
        try:
            new_ticket = Ticket(
                issue_description = ticket_data.issue_description,
                priority = ticket_data.priority,
                severity = ticket_data.severity,
                issue_category_id=ticket_data.issue_category_id,
                sla_id=ticket_data.sla_id,
                created_by = user_id,
                status = "new",
                created_at = datetime.utcnow(),
                updated_at = datetime.utcnow()
            )
            db.add(new_ticket)
            db.commit()
            db.refresh(new_ticket)
            return new_ticket, None
        except Exception as e:
            return None, str(e)
        
    @staticmethod
    def assign_ticket(ticket_id: int, assigned_to: int, db):
        try:
            ticket = db.query(Ticket).filter(Ticket.ticket_id == ticket_id).first()
            if not ticket:
                return None, "Ticket not found"

            ticket.assigned_to = assigned_to
            ticket.status = "assigned"
            db.commit()
            db.refresh(ticket)
            return ticket, None
        except Exception as e:
            return None, str(e)


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
        except Exception as e:
            return None, str(e)
