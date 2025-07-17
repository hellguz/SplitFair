"""
Pydantic schemas for representing calculated balances and transactions.
"""
from typing import List
from pydantic import BaseModel

class Balance(BaseModel):
    member_id: int
    nickname: str
    balance: float

class Transaction(BaseModel):
    from_member_id: int
    to_member_id: int
    amount: float

class BalanceReport(BaseModel):
    balances: List[Balance]
    transactions: List[Transaction]

