from datetime import datetime
from sqlalchemy.exc import SQLAlchemyError
from app.models.assignment import Assignment

class AssignmentRepository:
    @staticmethod
    def log_assignment(ticket_id: int, assigned_to: int, assigned_by: int, db):
        try:
            assignment = Assignment(
                ticket_id=ticket_id,
                assigned_to=assigned_to,
                assigned_by=assigned_by,
                assigned_at=datetime.utcnow()
            )
            db.add(assignment)
            db.commit()
            db.refresh(assignment)
            return assignment, None
        except SQLAlchemyError as e:
            db.rollback()
            return None, f"Database error while logging assignment: {str(e)}"
        except Exception as e:
            db.rollback()
            return None, f"Unexpected error: {str(e)}"
