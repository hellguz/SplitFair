from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.db.session import Base

class User(Base):
    """
    SQLAlchemy model for a user.
    """
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    uuid = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, nullable=False)

    # A user can be a member of many groups
    groups = relationship("Group", secondary="group_members", back_populates="members")
    # A user can participate in many expenses
    expenses_participated = relationship("Expense", secondary="expense_participants", back_populates="participants")
