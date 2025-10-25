from app.repositories.ticket_repository import TicketRepository
from app.repositories.user_repository import UserRepository
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
    
    @staticmethod
    def assign_ticket(user, ticket_id, payload, db):
        if user.role != "admin":
            return None, "Only admins can assign tickets"

        engineer = UserRepository.get_user_by_id(payload.assigned_to, db)
        if not engineer or engineer.role != "engineer":
            return None, "Assigned user must be a valid engineer"

        return TicketRepository.assign_ticket(ticket_id, payload.assigned_to, db)
    


    @staticmethod
    def update_status(user, ticket_id, new_status, db):
        if user.role.value not in ["engineer", "admin"]:
            return None, "User does not have permission to update status"

        ticket, err = TicketRepository.update_status(ticket_id, new_status, db)
        if err:
            return None, err

        return ticket, None