"""
Database model for a Participant.
A participant represents a user's browser, identified by a client-side UUID.
"""
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.models.database import Base

class Participant(Base):
    """Represents a unique user/browser session."""
    __tablename__ = "participants"

    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(String, unique=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    memberships = relationship("GroupMember", back_populates="participant", cascade="all, delete-orphan")

