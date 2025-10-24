from app.repositories.ticket_repository import TicketRepository

class TicketService:
    @staticmethod
    def create_ticket(user, ticket_data, db):
        # print("user role is: ", user.role.value)
        if user.role.value != "customer":
            return None, "Only users can create tickets"
        
        ticket, err = TicketRepository.create_ticket(user.user_id, ticket_data, db)
        if err:
            return None, f"Ticket creation failed: {err}"
        
        return ticket, None