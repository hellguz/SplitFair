# ./backend/app/models/user.py
"""
SQLAlchemy ORM model for a User (participant in a group).
"""
import uuid
from sqlalchemy import Column, String, DateTime, ForeignKey, func, Uuid
from sqlalchemy.orm import relationship
from app.db.session import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    client_uuid = Column(String(255), nullable=False, index=True)
    display_name = Column(String(100), nullable=False)
    group_id = Column(Uuid, ForeignKey("groups.id"), nullable=False)
    created_at = Column(DateTime, server_default=func.now())

    group = relationship("Group", back_populates="users")
    paid_expenses = relationship("Expense", back_populates="payer")
    # A user can be part of many expenses through the association
    involved_in_expenses = relationship("ExpenseParticipant", back_populates="user")


