"""
database.py — Database connection setup.

SQLAlchemy is a Python library that lets you talk to databases using Python
objects instead of writing raw SQL. This file configures the connection to
PostgreSQL.

KEY CONCEPT: A "session" is like an open conversation with the database.
You open one, do some reads/writes, then close it.
"""

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# ---------------------------------------------------------------------------
# 1. Build the database URL
# ---------------------------------------------------------------------------
# We read the URL from an environment variable so we can change it easily
# (e.g., different passwords in development vs. production).
# Format: postgresql://USERNAME:PASSWORD@HOST:PORT/DATABASE_NAME
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres:postgres@localhost:5432/support_dashboard"
)

# ---------------------------------------------------------------------------
# 2. Create the SQLAlchemy engine
# ---------------------------------------------------------------------------
# The "engine" is the main connection pool to the database.
engine = create_engine(DATABASE_URL)

# ---------------------------------------------------------------------------
# 3. Create a session factory
# ---------------------------------------------------------------------------
# SessionLocal is a *class* that produces new database sessions when called.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# ---------------------------------------------------------------------------
# 4. Base class for our models
# ---------------------------------------------------------------------------
# Every database model (like Ticket) will inherit from this Base class.
Base = declarative_base()


# ---------------------------------------------------------------------------
# 5. Dependency — get a database session
# ---------------------------------------------------------------------------
# FastAPI uses "dependencies" to inject things into endpoint functions.
# This function opens a session, gives it to the endpoint, then closes it.
def get_db():
    db = SessionLocal()
    try:
        yield db       # The endpoint uses 'db' here
    finally:
        db.close()     # Always close the session when done
