"""
Database models for Group and GroupMember.
"""
from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from app.models.database import Base

class Group(Base):
    """Represents a group of participants."""
    __tablename__ = "groups"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    invite_code = Column(String, unique=True, index=True)

    members = relationship("GroupMember", back_populates="group", cascade="all, delete-orphan")
    expenses = relationship("Expense", back_populates="group", cascade="all, delete-orphan")

class GroupMember(Base):
    """Association object between a Group and a Participant."""
    __tablename__ = "group_members"

    id = Column(Integer, primary_key=True, index=True)
    nickname = Column(String)
    group_id = Column(Integer, ForeignKey("groups.id"))
    participant_id = Column(Integer, ForeignKey("participants.id"))

    group = relationship("Group", back_populates="members")
    participant = relationship("Participant", back_populates="memberships")
    
    paid_expenses = relationship("Expense", back_populates="payer", foreign_keys="[Expense.paid_by_member_id]")

    __table_args__ = (UniqueConstraint('group_id', 'participant_id', name='_group_participant_uc'),)

