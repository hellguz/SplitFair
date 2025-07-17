"""
Pydantic schemas for Expense data validation.
"""
import datetime
from typing import List
from pydantic import BaseModel
from app.schemas.group import GroupMember

class ExpenseBase(BaseModel):
    description: str
    amount: float

class ExpenseCreate(ExpenseBase):
    group_id: int
    paid_by_member_id: int
    participant_member_ids: List[int]

class Expense(ExpenseBase):
    id: int
    date: datetime.datetime
    group_id: int
    paid_by_member_id: int
    payer: GroupMember
    participants: List[GroupMember] = []
    
    class Config:
        from_attributes = True
