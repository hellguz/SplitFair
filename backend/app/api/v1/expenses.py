# ./backend/app/api/v1/expenses.py
"""
API endpoints for managing expenses within a group.
"""
import uuid
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas import expense as expense_schema
from app.crud import crud_expense, crud_group
from .websockets import manager

router = APIRouter()

@router.post("/groups/{group_id}/expenses", response_model=expense_schema.Expense, status_code=status.HTTP_201_CREATED)
async def create_expense(
    group_id: uuid.UUID,
    expense_in: expense_schema.ExpenseCreate,
    db: Session = Depends(get_db)
):
    """
    Create a new expense in a specific group.
    """
    # Verify group exists
    db_group = crud_group.get_group(db, group_id=group_id)
    if not db_group:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Group not found")
    
    new_expense = crud_expense.create_expense(db=db, group_id=group_id, expense_in=expense_in)
    
    # Notify connected clients via WebSocket
    await manager.broadcast(str(group_id), {"event": "expense_update"})
    
    return new_expense

@router.delete("/expenses/{expense_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_expense(
    expense_id: uuid.UUID,
    db: Session = Depends(get_db)
):
    """
    Delete an expense.
    """
    db_expense = crud_expense.delete_expense(db=db, expense_id=expense_id)
    if db_expense is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Expense not found")

    # Notify connected clients via WebSocket
    await manager.broadcast(str(db_expense.group_id), {"event": "expense_update"})
    return

@router.put("/expenses/{expense_id}", response_model=expense_schema.Expense)
async def update_expense(
    expense_id: uuid.UUID,
    expense_in: expense_schema.ExpenseUpdate,
    db: Session = Depends(get_db)
):
    """
    Update an existing expense.
    """
    db_expense = crud_expense.update_expense(db=db, expense_id=expense_id, expense_in=expense_in)
    if db_expense is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Expense not found")
    
    # Notify connected clients via WebSocket
    await manager.broadcast(str(db_expense.group_id), {"event": "expense_update"})
    
    return db_expense

