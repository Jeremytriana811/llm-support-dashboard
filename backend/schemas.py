"""
schemas.py — Pydantic schemas (data validation).

Pydantic schemas define the "shape" of data coming in and going out of your API.
Think of them as contracts:
  - TicketCreate says "to create a ticket, you MUST send title + description"
  - TicketResponse says "when I return a ticket, it will have these fields"
"""

from datetime import datetime
from pydantic import BaseModel


class TicketCreate(BaseModel):
    """What the user sends when creating a ticket (POST /tickets)."""
    title: str
    description: str


class TicketResponse(BaseModel):
    """What the API returns for a ticket."""
    id: int
    title: str
    description: str
    category: str | None = None
    summary: str | None = None
    created_at: datetime | None = None

    class Config:
        from_attributes = True   # Lets Pydantic read SQLAlchemy model objects


class MetricsResponse(BaseModel):
    """What GET /metrics/tickets returns."""
    total: int
    by_category: dict[str, int]
