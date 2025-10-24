from app.models.ticket import Ticket

class TicketRepository:
    @staticmethod
    def create_ticket(user_id: int, ticket_data, db):
        try:
            new_ticket = Ticket(
                title = ticket_data.title,
                issue_description = ticket_data.issue_description,
                priority = ticket_data.priority,
                severity = ticket_data.severity,
                issue_category_id = ticket_data.issue_category_id,
                sla_id = ticket_data.sla_id,
                created_by = user_id,
                status = "New"
            )
            db.add(new_ticket)
            db.commit()
            db.refresh(new_ticket)
            return new_ticket, None
        except Exception as e:
            return None, str(e)
