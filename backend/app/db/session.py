# ./backend/app/db/session.py
"""
Database session management for SQLAlchemy.
"""
import os
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from app.core.config import settings

# Construct the database URL from settings
DATABASE_URL = f"mysql+pymysql://{settings.MYSQL_USER}:{settings.MYSQL_PASSWORD}@{settings.MYSQL_HOST}/{settings.MYSQL_DATABASE}"

# Create the SQLAlchemy engine
engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def init_db():
    """
    Creates all database tables based on the defined models.
    This is a simple way to initialize the schema for a new project.
    """
    try:
        # A simple check to see if we can connect
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
        print("Database connection successful.")
        # Create tables
        Base.metadata.create_all(bind=engine)
        print("Database tables created successfully.")
    except Exception as e:
        print(f"Error connecting to or initializing the database: {e}")
        raise

# Dependency to get a DB session in API endpoints
def get_db():
    """
    FastAPI dependency that provides a database session for each request.
    Ensures the session is closed after the request is finished.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Initialize DB on first import (e.g., when app starts)
init_db()

