from typing import List
from pydantic import BaseModel, Field
import datetime

class ExpenseBase(BaseModel):
    description: str
    amount: float = Field(..., gt=0)

class ExpenseCreate(ExpenseBase):
    payer_uuid: str
    participant_uuids: List[str] = Field(..., min_length=1)

class Expense(ExpenseBase):
    id: int
    created_at: datetime.datetime
    payer_id: int
    group_id: int

    class Config:
        from_attributes = True
