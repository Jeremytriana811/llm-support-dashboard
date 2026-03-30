"""
main.py — The main FastAPI application.

FastAPI is a Python framework for building web APIs (ways for programs to talk to each other).
This file sets up all the "endpoints" (URLs your app responds to).
"""

from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import func

from database import engine, get_db, Base
from models import Ticket
from schemas import TicketCreate, TicketResponse, MetricsResponse
from ml import classify_ticket, summarize_ticket

# ---------------------------------------------------------------------------
# 1. Create the database tables (if they don't exist yet)
# ---------------------------------------------------------------------------
Base.metadata.create_all(bind=engine)

# ---------------------------------------------------------------------------
# 2. Create the FastAPI app
# ---------------------------------------------------------------------------
app = FastAPI(
    title="LLM Support Analytics Dashboard",
    description="AI-powered support ticket classification & summarization",
    version="1.0.0",
)

# ---------------------------------------------------------------------------
# 3. Set up CORS (Cross-Origin Resource Sharing)
# ---------------------------------------------------------------------------
# CORS is a security feature in browsers. By default, a web page on
# localhost:5173 (React frontend) can't call an API on localhost:8000
# (backend). This middleware tells the browser "it's okay, let them talk."
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],       # Allow any origin (fine for development)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------------------------------------------------------------------------
# 4. Endpoints
# ---------------------------------------------------------------------------

@app.get("/")
def root():
    """Health check — visit http://localhost:8000/ to verify the API is up."""
    return {"message": "LLM Support Analytics API is running!"}


@app.post("/tickets", response_model=TicketResponse)
def create_ticket(ticket: TicketCreate, db: Session = Depends(get_db)):
    """
    POST /tickets — Create a new support ticket.

    1. User sends JSON with 'title' and 'description'.
    2. AI classifies the ticket and generates a summary.
    3. The ticket is saved to PostgreSQL and returned.
    """
    category = classify_ticket(ticket.description)
    summary = summarize_ticket(ticket.description)

    db_ticket = Ticket(
        title=ticket.title,
        description=ticket.description,
        category=category,
        summary=summary,
    )
    db.add(db_ticket)
    db.commit()
    db.refresh(db_ticket)
    return db_ticket


@app.get("/tickets", response_model=list[TicketResponse])
def list_tickets(db: Session = Depends(get_db)):
    """GET /tickets — Return all tickets, newest first."""
    return db.query(Ticket).order_by(Ticket.id.desc()).all()


@app.get("/metrics/tickets", response_model=MetricsResponse)
def ticket_metrics(db: Session = Depends(get_db)):
    """
    GET /metrics/tickets — Return aggregate stats.
    Example response: { "total": 12, "by_category": {"bug": 5, "feature": 3} }
    """
    total = db.query(func.count(Ticket.id)).scalar()
    rows = (
        db.query(Ticket.category, func.count(Ticket.id))
        .group_by(Ticket.category)
        .all()
    )
    by_category = {cat: cnt for cat, cnt in rows}
    return {"total": total, "by_category": by_category}
