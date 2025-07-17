"""
API endpoints for expense-related operations.
"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.crud import crud_expense, crud_group
from app.schemas import expense as expense_schemas
from app.models.database import get_db

router = APIRouter()

@router.post("/expenses", response_model=expense_schemas.Expense)
def create_expense(expense: expense_schemas.ExpenseCreate, db: Session = Depends(get_db)):
    """Creates a new expense and links it to participants."""
    # Verify the payer and participants are members of the group
    payer_member = crud_group.get_member(db, expense.paid_by_member_id)
    if not payer_member or payer_member.group_id != expense.group_id:
        raise HTTPException(status_code=400, detail="Payer is not a valid member of this group.")
    
    for member_id in expense.participant_member_ids:
        p_member = crud_group.get_member(db, member_id)
        if not p_member or p_member.group_id != expense.group_id:
            raise HTTPException(status_code=400, detail=f"Participant with member ID {member_id} is not in this group.")

    return crud_expense.create_expense(db=db, expense=expense)

@router.get("/groups/{group_id}/expenses", response_model=List[expense_schemas.Expense])
def read_expenses_for_group(group_id: int, db: Session = Depends(get_db)):
    """Fetches all expenses for a given group."""
    expenses = crud_expense.get_expenses_for_group(db, group_id=group_id)
    return expenses

@router.delete("/expenses/{expense_id}", status_code=204)
def delete_expense(expense_id: int, db: Session = Depends(get_db)):
    """Deletes an expense by its ID."""
    db_expense = crud_expense.get_expense(db, expense_id)
    if not db_expense:
        raise HTTPException(status_code=404, detail="Expense not found")
    crud_expense.delete_expense(db, expense_id=expense_id)
    return None

