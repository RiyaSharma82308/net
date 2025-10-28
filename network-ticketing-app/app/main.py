# app/main.py
from fastapi import FastAPI
from app.router import network_ticketing_router
from app.database import Base, engine
from app.models.user import User
from app.models.issue_category import IssueCategory
from app.models.sla import SLA
from app.models.ticket import Ticket
from app.models.feedback import Feedback
from app.models.assignment import Assignment
from app.models.ticket_action_log import TicketActionLog
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



app.include_router(network_ticketing_router)
# print("Creating tables now...")
# Base.metadata.create_all(bind=engine)
# print("Tables created.")