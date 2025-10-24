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
