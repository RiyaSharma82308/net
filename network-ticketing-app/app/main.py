# app/main.py
from fastapi import FastAPI
from app.router import router
from app.database import Base, engine
from app.models.user import User

app = FastAPI()
app.include_router(router)
Base.metadata.create_all(bind=engine)