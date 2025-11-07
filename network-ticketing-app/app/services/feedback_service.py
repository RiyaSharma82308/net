from datetime import datetime
from app.repositories.feedback_repository import FeedbackRepository
from app.repositories.ticket_repository import TicketRepository


class FeedbackService:
    @staticmethod
    def submit_feedback(user, ticket_id, payload, db):
        # ✅ Only customers can submit feedback
        if user.role.value != "customer":
            return None, "Only customers can submit feedback"

        # ✅ Verify ticket exists and belongs to the customer
        ticket, err = TicketRepository.get_ticket_by_id(ticket_id, db)
        if err:
            return None, err
        if not ticket:
            return None, "Ticket not found"
        if ticket.created_by != user.user_id:
            return None, "You are not authorized to give feedback for this ticket"

        # ✅ Ticket must be resolved or closed
        if ticket.status.value not in ["resolved", "closed"]:
            return None, f"Cannot submit feedback for ticket in '{ticket.status.value}' status"

        # ✅ Prevent duplicate feedback
        existing, _ = FeedbackRepository.get_feedback_by_ticket(ticket_id, db)
        if existing:
            return None, "Feedback already submitted for this ticket"

        # ✅ Create feedback
        feedback, err = FeedbackRepository.create_feedback(
            ticket_id=ticket_id,
            rating=payload.rating,
            comment=payload.comment,
            db=db,
        )
        if err:
            return None, err

        return feedback, None

    @staticmethod
    def get_feedback(ticket_id, user, db):
        feedback, err = FeedbackRepository.get_feedback_by_ticket(ticket_id, db)
        if err:
            return None, err
        if not feedback:
            return None, "Feedback not found"

        # ✅ Customer can view their own ticket feedback; agent/manager/admin can view all
        if user.role.value == "customer":
            ticket, err = TicketRepository.get_ticket_by_id(ticket_id, db)
            if not ticket or ticket.created_by != user.user_id:
                return None, "Unauthorized access to feedback"

        return feedback, None
