"""
Database models for Expense and its participants.
"""
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Table
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.models.database import Base

# Association table for the many-to-many relationship between Expense and GroupMember
expense_participants_table = Table('expense_participants', Base.metadata,
    Column('expense_id', Integer, ForeignKey('expenses.id'), primary_key=True),
    Column('member_id', Integer, ForeignKey('group_members.id'), primary_key=True)
)

class Expense(Base):
    """Represents a single expense within a group."""
    __tablename__ = "expenses"

    id = Column(Integer, primary_key=True, index=True)
    description = Column(String)
    amount = Column(Float)
    date = Column(DateTime(timezone=True), server_default=func.now())
    
    group_id = Column(Integer, ForeignKey("groups.id"))
    paid_by_member_id = Column(Integer, ForeignKey("group_members.id"))

    group = relationship("Group", back_populates="expenses")
    payer = relationship("GroupMember", back_populates="paid_expenses", foreign_keys=[paid_by_member_id])

    participants = relationship("GroupMember", secondary=expense_participants_table)

