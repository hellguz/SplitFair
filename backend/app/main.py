# ./backend/app/main.py
"""
Main application file for the SplitFair FastAPI backend.
Initializes the FastAPI app, includes routers, and sets up middleware.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.api.v1 import groups, expenses, websockets

# Initialize the FastAPI application
app = FastAPI(
    title="SplitFair API",
    description="API for the SplitFair expense splitting application.",
    version="1.0.0"
)

# --- Middleware ---
# Set up CORS (Cross-Origin Resource Sharing) to allow the frontend
# to communicate with the backend.
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.FRONTEND_ORIGIN],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- API Routers ---
# Include the routers for different parts of the API.
app.include_router(groups.router, prefix="/api/v1", tags=["Groups"])
app.include_router(expenses.router, prefix="/api/v1", tags=["Expenses"])
app.include_router(websockets.router, tags=["WebSockets"])

@app.on_event("startup")
def on_startup():
    """
    Log a message when the application starts.
    """
    print("SplitFair backend is starting up...")

@app.get("/api/v1/health", tags=["Health Check"])
def health_check():
    """
    Simple health check endpoint.
    """
    return {"status": "ok"}

