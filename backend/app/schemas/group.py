"""
Pydantic schemas for Group and GroupMember data validation.
"""
from typing import List, Optional
from pydantic import BaseModel

class GroupMemberBase(BaseModel):
    nickname: str

class GroupMemberCreate(GroupMemberBase):
    pass

class GroupMember(GroupMemberBase):
    id: int
    group_id: int
    participant_id: int

    class Config:
        from_attributes = True

class GroupBase(BaseModel):
    name: str

class GroupCreate(GroupBase):
    creator_nickname: str

class Group(GroupBase):
    id: int
    invite_code: str
    members: List[GroupMember] = []

    class Config:
        from_attributes = True

class GroupMemberJoin(BaseModel):
    nickname: str
