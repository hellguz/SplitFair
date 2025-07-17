"""
Pydantic schemas for Participant data validation.
"""
import datetime
from pydantic import BaseModel

class ParticipantBase(BaseModel):
    client_id: str

class ParticipantCreate(ParticipantBase):
    pass

class Participant(ParticipantBase):
    id: int
    created_at: datetime.datetime

    class Config:
        from_attributes = True