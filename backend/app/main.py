"""
Main application file for the FastAPI backend.
Initializes the FastAPI app, includes routers, sets up CORS,
and defines the startup event to create database tables.
"""
import os
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Load environment variables
load_dotenv()

# Ensure all models are imported before initializing the database
# This is crucial for Base.metadata.create_all() to work correctly
from app.models.database import engine, Base
from app.models.participant import Participant
from app.models.group import Group, GroupMember
from app.models.expense import Expense

from app.api import groups, expenses

# Create all database tables on startup
def create_tables():
    """Creates all database tables defined in the models."""
    Base.metadata.create_all(bind=engine)

app = FastAPI()

# Event handler for application startup
@app.on_event("startup")
def on_startup():
    """Function to run on application startup."""
    create_tables()

# Configure CORS (Cross-Origin Resource Sharing)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routers
app.include_router(groups.router)
app.include_router(expenses.router)

@app.get("/")
def read_root():
    """Root endpoint for the API."""
    return {"message": "Welcome to the SplitShare API"}
