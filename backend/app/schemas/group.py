# ./backend/app/schemas/group.py
"""
Pydantic schemas for Group data validation and serialization.
"""
from pydantic import BaseModel
from typing import List, Optional
import uuid
from datetime import datetime

# Forward declare Expense and User schemas to handle circular references
from .expense import Expense
from .user import User

class GroupBase(BaseModel):
    name: str

class GroupCreate(GroupBase):
    client_uuid: str
    user_display_name: str

class Group(GroupBase):
    id: uuid.UUID
    invite_code: str
    created_at: datetime
    users: List[User] = []
    expenses: List[Expense] = []

    class Config:
        orm_mode = True

class JoinGroup(BaseModel):
    client_uuid: str
    display_name: str

# Update forward refs now that all models are defined
Group.update_forward_refs()

