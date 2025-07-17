from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base

from app.core.config import settings

# Create an asynchronous engine
engine = create_async_engine(settings.DATABASE_URL, echo=False)

# Create a session maker bound to the engine
AsyncSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

# Base class for declarative models
Base = declarative_base()

async def get_db() -> AsyncSession:
    """
    Dependency to get a database session.
    Ensures the session is closed after the request.
    """
    async with AsyncSessionLocal() as session:
        yield session
