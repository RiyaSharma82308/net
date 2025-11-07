from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
from fastapi.security import HTTPAuthorizationCredentials
from app.dependencies.auth import AuthMiddleware, security
from app.schemas.feedback import FeedbackCreateRequest
from app.services.feedback_service import FeedbackService
from app.database import get_db

feedback_router = APIRouter()

# 💬 Submit Feedback
@feedback_router.post("/feedback/{ticket_id}")
def submit_feedback(
    ticket_id: int,
    payload: FeedbackCreateRequest,
    db: Session = Depends(get_db),
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    # ✅ Auth check
    user, err = AuthMiddleware.get_current_user(credentials, db)
    if err:
        return JSONResponse(status_code=401, content={"status": "error", "message": err})

    feedback, err = FeedbackService.submit_feedback(user, ticket_id, payload, db)
    if err:
        return JSONResponse(
            status_code=403 if "unauthorized" in err.lower() else 400,
            content={"status": "error", "message": err},
        )

    return JSONResponse(
        status_code=201,
        content={
            "status": "success",
            "message": "Feedback submitted successfully",
            "data": {
                "feedback_id": feedback.feedback_id,
                "ticket_id": feedback.ticket_id,
                "rating": feedback.rating,
                "comment": feedback.comment,
                "feedback_time": str(feedback.feedback_time),
            },
        },
    )


# 👀 Get Feedback for a Ticket
@feedback_router.get("/feedback/{ticket_id}")
def get_feedback(
    ticket_id: int,
    db: Session = Depends(get_db),
    credentials: HTTPAuthorizationCredentials = Depends(security),
):
    user, err = AuthMiddleware.get_current_user(credentials, db)
    if err:
        return JSONResponse(status_code=401, content={"status": "error", "message": err})

    feedback, err = FeedbackService.get_feedback(ticket_id, user, db)
    if err:
        return JSONResponse(status_code=404, content={"status": "error", "message": err})

    if not feedback:
        return JSONResponse(status_code=404, content={"status": "error", "message": "No feedback found for this ticket"})

    return JSONResponse(
        status_code=200,
        content={
            "status": "success",
            "data": {
                "feedback_id": feedback.feedback_id,
                "ticket_id": feedback.ticket_id,
                "rating": feedback.rating,
                "comment": feedback.comment,
                "feedback_time": str(feedback.feedback_time),
            },
        },
    )
