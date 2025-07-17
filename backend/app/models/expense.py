# ./backend/app/models/expense.py
"""
SQLAlchemy ORM models for an Expense and its Participants.
"""
import uuid
from sqlalchemy import Column, String, DateTime, ForeignKey, func, Float, Uuid
from sqlalchemy.orm import relationship
from app.db.session import Base

class Expense(Base):
    __tablename__ = "expenses"

    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    description = Column(String(255), nullable=False)
    amount = Column(Float, nullable=False)
    date = Column(DateTime, server_default=func.now())
    group_id = Column(Uuid, ForeignKey("groups.id"), nullable=False)
    payer_id = Column(Uuid, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, server_default=func.now())

    group = relationship("Group", back_populates="expenses")
    payer = relationship("User", back_populates="paid_expenses")
    participants = relationship("ExpenseParticipant", back_populates="expense", cascade="all, delete-orphan")

class ExpenseParticipant(Base):
    __tablename__ = "expense_participants"

    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    expense_id = Column(Uuid, ForeignKey("expenses.id"), nullable=False)
    user_id = Column(Uuid, ForeignKey("users.id"), nullable=False)

    expense = relationship("Expense", back_populates="participants")
    user = relationship("User", back_populates="involved_in_expenses")


