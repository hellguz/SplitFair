from typing import List
from pydantic import BaseModel

from .user import User, UserBalance
from .expense import Expense

class GroupBase(BaseModel):
    name: str

class GroupCreate(GroupBase):
    pass

class GroupJoin(BaseModel):
    invite_code: str

class Group(GroupBase):
    id: int
    invite_code: str

    class Config:
        from_attributes = True

class GroupDetails(Group):
    members: List[User] = []
    expenses: List[Expense] = []
    balances: List[UserBalance] = []
