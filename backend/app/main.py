from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import api_router
from app.db.session import Base, engine


app = FastAPI(title="SplitWise Clone API")

@app.on_event("startup")
async def on_startup():
    """
    This function runs when the application starts.
    It connects to the database and creates all tables
    defined in the SQLAlchemy models if they don't already exist.
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Allows the React frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api")

@app.get("/")
async def root():
    """
    Root endpoint for the API.
    """
    return {"message": "Welcome to the SplitWise Clone API"}