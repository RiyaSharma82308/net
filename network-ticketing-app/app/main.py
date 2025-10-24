# app/main.py
from fastapi import FastAPI
from app.router import network_ticketing_router
from app.database import Base, engine
from app.models.user import User

app = FastAPI()
print("in main!!!!!!!!!!!!!!!!!!!!!!!!!!!")
app.include_router(network_ticketing_router)
Base.metadata.create_all(bind=engine)