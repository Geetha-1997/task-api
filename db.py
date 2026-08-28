"""
Database configuration.

Reads DATABASE_URL from the environment so the same code works with:
  - SQLite for local dev:      sqlite:///tasks.db  (this is the default)
  - Postgres in production:    postgresql://user:pass@host:5432/dbname

This is a standard "12-factor app" pattern — config lives in the
environment, not hardcoded in the code, so the same image can run
against different databases in different environments (local, AWS RDS,
Azure Database for PostgreSQL, etc.) with zero code changes.
"""

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = os.environ.get("DATABASE_URL", "sqlite:////app/data/tasks.db")

# check_same_thread is only needed for SQLite; harmless to set conditionally.
connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}

engine = create_engine(DATABASE_URL, connect_args=connect_args)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base = declarative_base()


def init_db():
    """
    Create tables if they don't exist. Called once at app startup.

    Guarded with try/except because Gunicorn spawns multiple worker
    processes, each of which imports this module independently. Without
    this guard, two workers can race to CREATE TABLE at nearly the same
    instant — one succeeds, the other hits "table already exists" and
    crashes. SQLAlchemy's checkfirst does a SELECT then CREATE, which
    isn't atomic, so the race is possible even though it's rare.
    """
    from sqlalchemy.exc import OperationalError
    try:
        Base.metadata.create_all(bind=engine)
    except OperationalError as e:
        if "already exists" not in str(e):
            raise