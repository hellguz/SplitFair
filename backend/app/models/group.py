# ./backend/app/models/group.py
"""
SQLAlchemy ORM model for a Group.
"""
import uuid
from sqlalchemy import Column, String, DateTime, func, Uuid
from sqlalchemy.orm import relationship
from app.db.session import Base

class Group(Base):
    __tablename__ = "groups"

    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    name = Column(String(100), nullable=False)
    invite_code = Column(String(255), unique=True, nullable=False, index=True)
    created_at = Column(DateTime, server_default=func.now())

    users = relationship("User", back_populates="group", cascade="all, delete-orphan")
    expenses = relationship("Expense", back_populates="group", cascade="all, delete-orphan")

