# ./backend/app/schemas/user.py
"""
Pydantic schemas for User data validation and serialization.
"""
from pydantic import BaseModel
import uuid
from datetime import datetime

class UserBase(BaseModel):
    display_name: str
    client_uuid: str

class UserCreate(UserBase):
    group_id: uuid.UUID

class User(UserBase):
    id: uuid.UUID
    group_id: uuid.UUID
    created_at: datetime

    class Config:
        orm_mode = True

