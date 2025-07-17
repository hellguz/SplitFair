# ./backend/app/schemas/expense.py
"""
Pydantic schemas for Expense data validation and serialization.
"""
from pydantic import BaseModel
from typing import List
import uuid
from datetime import datetime

# Import User schema for nesting
from .user import User

class ExpenseParticipant(BaseModel):
    user: User

    class Config:
        orm_mode = True

class ExpenseBase(BaseModel):
    description: str
    amount: float

class ExpenseCreate(ExpenseBase):
    payer_id: uuid.UUID
    participant_ids: List[uuid.UUID]

class ExpenseUpdate(ExpenseBase):
    payer_id: uuid.UUID
    participant_ids: List[uuid.UUID]

class Expense(ExpenseBase):
    id: uuid.UUID
    date: datetime
    payer: User
    participants: List[ExpenseParticipant]

    class Config:
        orm_mode = True

