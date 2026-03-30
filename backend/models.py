"""
models.py — Database models (the shape of your data in PostgreSQL).

A "model" here means a Python class that maps to a database table.
Each instance of the class = one row in the table.
"""

from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.sql import func
from database import Base


class Ticket(Base):
    """
    The 'tickets' table in PostgreSQL.

    Columns:
        id          — auto-incrementing unique number (primary key)
        title       — short title like "Login page broken"
        description — full details of the issue
        category    — AI-assigned category: bug, feature, question, documentation
        summary     — AI-generated one-sentence summary
        created_at  — timestamp of when the ticket was created
    """
    __tablename__ = "tickets"

    id          = Column(Integer, primary_key=True, index=True)
    title       = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    category    = Column(String(50), nullable=True)       # filled by AI
    summary     = Column(Text, nullable=True)             # filled by AI
    created_at  = Column(DateTime(timezone=True), server_default=func.now())
