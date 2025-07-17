"""
API endpoints for group-related operations.
"""
from typing import List, Dict
from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session

from app.crud import crud_group, crud_participant, crud_expense
from app.schemas import group as group_schemas
from app.schemas import balance as balance_schemas
from app.models.database import get_db

router = APIRouter()

def get_or_create_participant(client_id: str, db: Session):
    """
    Retrieves a participant by client_id or creates a new one if not found.
    A common dependency for endpoints requiring a participant context.
    """
    if not client_id:
        raise HTTPException(status_code=400, detail="Client-ID header is required")
    return crud_participant.get_or_create_participant(db, client_id=client_id)


@router.post("/groups", response_model=group_schemas.Group)
def create_group(group: group_schemas.GroupCreate, client_id: str = Header(None), db: Session = Depends(get_db)):
    """Creates a new group and adds the creator as the first member."""
    participant = get_or_create_participant(client_id, db)
    return crud_group.create_group_with_member(db=db, group=group, participant=participant, nickname=group.creator_nickname)

@router.get("/groups", response_model=List[group_schemas.Group])
def read_groups_for_participant(client_id: str = Header(None), db: Session = Depends(get_db)):
    """Fetches all groups that the participant is a member of."""
    participant = get_or_create_participant(client_id, db)
    return crud_group.get_groups_for_participant(db=db, participant_id=participant.id)

@router.get("/groups/join/{invite_code}", response_model=group_schemas.Group)
def get_group_by_invite_code(invite_code: str, db: Session = Depends(get_db)):
    """Retrieves group details using an invite code."""
    db_group = crud_group.get_group_by_invite_code(db, invite_code=invite_code)
    if db_group is None:
        raise HTTPException(status_code=404, detail="Group not found")
    return db_group

@router.post("/groups/{group_id}/join", response_model=group_schemas.GroupMember)
def join_group(group_id: int, member_join: group_schemas.GroupMemberJoin, client_id: str = Header(None), db: Session = Depends(get_db)):
    """Adds a participant to a specific group."""
    participant = get_or_create_participant(client_id, db)
    db_group = crud_group.get_group(db, group_id=group_id)
    if db_group is None:
        raise HTTPException(status_code=404, detail="Group not found")

    existing_member = crud_group.get_member_by_participant_id(db, group_id=group_id, participant_id=participant.id)
    if existing_member:
        raise HTTPException(status_code=400, detail="User is already a member of this group")

    return crud_group.add_member_to_group(db=db, group_id=group_id, participant_id=participant.id, nickname=member_join.nickname)

@router.get("/groups/{group_id}", response_model=group_schemas.Group)
def read_group(group_id: int, db: Session = Depends(get_db)):
    """Fetches details for a single group."""
    db_group = crud_group.get_group(db, group_id=group_id)
    if db_group is None:
        raise HTTPException(status_code=404, detail="Group not found")
    return db_group

@router.get("/groups/{group_id}/balances", response_model=balance_schemas.BalanceReport)
def get_group_balances(group_id: int, db: Session = Depends(get_db)):
    """
    Calculates and returns the current balances for all members of a group.
    This is the core settlement logic.
    """
    members = crud_group.get_group_members(db, group_id=group_id)
    if not members:
        return balance_schemas.BalanceReport(balances={}, transactions=[])

    expenses = crud_expense.get_expenses_for_group(db, group_id=group_id)
    
    # Initialize balances for all members to zero
    net_balances = {member.id: 0.0 for member in members}

    # Process each expense to calculate net balances
    for expense in expenses:
        if not expense.participants:
            continue
        
        share = expense.amount / len(expense.participants)
        
        # The payer gets credited the full amount
        net_balances[expense.paid_by_member_id] += expense.amount
        
        # Each participant gets debited their share
        for participant_member in expense.participants:
            net_balances[participant_member.id] -= share
    
    # Create simplified balance list for the response
    balances_list = [
        balance_schemas.Balance(member_id=member.id, nickname=member.nickname, balance=round(net_balances[member.id], 2))
        for member in members
    ]
    
    # Calculate settlement transactions
    debtors = {mid: bal for mid, bal in net_balances.items() if bal < -0.01}
    creditors = {mid: bal for mid, bal in net_balances.items() if bal > 0.01}
    transactions = []

    # Match debtors to creditors
    while debtors and creditors:
        debtor_id, debt = max(debtors.items(), key=lambda item: item[1])
        creditor_id, credit = max(creditors.items(), key=lambda item: item[1])
        
        amount = min(abs(debt), credit)
        
        transactions.append(balance_schemas.Transaction(
            from_member_id=debtor_id,
            to_member_id=creditor_id,
            amount=round(amount, 2)
        ))

        debtors[debtor_id] += amount
        creditors[creditor_id] -= amount

        if abs(debtors[debtor_id]) < 0.01:
            del debtors[debtor_id]
        if abs(creditors[creditor_id]) < 0.01:
            del creditors[creditor_id]
            
    return balance_schemas.BalanceReport(balances=balances_list, transactions=transactions)

