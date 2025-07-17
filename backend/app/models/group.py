from sqlalchemy import Column, Integer, String, Table, ForeignKey
from sqlalchemy.orm import relationship

from app.db.session import Base

# Association Table for the many-to-many relationship between Users and Groups
group_members = Table(
    "group_members",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("users.id"), primary_key=True),
    Column("group_id", Integer, ForeignKey("groups.id"), primary_key=True),
)

class Group(Base):
    """
    SQLAlchemy model for a group.
    """
    __tablename__ = "groups"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    invite_code = Column(String, unique=True, index=True, nullable=False)

    # A group has many members (users)
    members = relationship("User", secondary=group_members, back_populates="groups")
    # A group has many expenses
    expenses = relationship("Expense", back_populates="group", cascade="all, delete-orphan")
