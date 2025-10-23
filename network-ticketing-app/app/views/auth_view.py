# app/views/auth_view.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.user import UserCreate, UserOut
from app.services.auth_service import signup_service, login_service
from app.models.user import User

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/signup", response_model=UserOut)
def signup(user: UserCreate, db: Session = Depends(get_db)):
    new_user, err = signup_service(user, db)
    if err:
        raise HTTPException(status_code=400, detail=err)
    return new_user


@router.post("/login")
def login(email: str, password: str, db: Session = Depends(get_db)):
    return login_service(email, password, db)
