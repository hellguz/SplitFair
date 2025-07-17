import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Table
from sqlalchemy.orm import relationship

from app.db.session import Base

# Association Table for the many-to-many relationship between Users and Expenses (participants)
expense_participants = Table(
    "expense_participants",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("users.id"), primary_key=True),
    Column("expense_id", Integer, ForeignKey("expenses.id"), primary_key=True),
)

class Expense(Base):
    """
    SQLAlchemy model for an expense.
    """
    __tablename__ = "expenses"

    id = Column(Integer, primary_key=True, index=True)
    description = Column(String, nullable=False)
    amount = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    group_id = Column(Integer, ForeignKey("groups.id"), nullable=False)
    payer_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # An expense belongs to one group
    group = relationship("Group", back_populates="expenses")
    # An expense has one payer (a user)
    payer = relationship("User")
    # An expense has many participants (users)
    participants = relationship("User", secondary=expense_participants, back_populates="expenses_participated")
