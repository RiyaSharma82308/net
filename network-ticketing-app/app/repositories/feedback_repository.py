from app.models.feedback import Feedback
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime


class FeedbackRepository:
    @staticmethod
    def create_feedback(ticket_id, rating, comment, db):
        try:
            feedback = Feedback(
                ticket_id=ticket_id,
                rating=rating,
                comment=comment,
                feedback_time=datetime.utcnow(),
            )
            db.add(feedback)
            db.commit()
            db.refresh(feedback)
            return feedback, None
        except SQLAlchemyError as e:
            db.rollback()
            return None, f"Database error while creating feedback: {str(e)}"
        except Exception as e:
            db.rollback()
            return None, f"Unexpected error while creating feedback: {str(e)}"

    @staticmethod
    def get_feedback_by_ticket(ticket_id, db):
        try:
            feedback = db.query(Feedback).filter_by(ticket_id=ticket_id).first()
            return feedback, None
        except SQLAlchemyError as e:
            return None, f"Database error while fetching feedback: {str(e)}"
        except Exception as e:
            return None, f"Unexpected error while fetching feedback: {str(e)}"
