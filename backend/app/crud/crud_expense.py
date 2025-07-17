# ./backend/app/crud/crud_expense.py
"""
CRUD operations for Expenses.
"""
import uuid
from sqlalchemy.orm import Session

from app.models import expense as expense_model
from app.schemas import expense as expense_schema

def create_expense(db: Session, group_id: uuid.UUID, expense_in: expense_schema.ExpenseCreate) -> expense_model.Expense:
    """
    Creates a new expense and links it to participants.
    
    Args:
        db: The database session.
        group_id: The ID of the group where the expense occurred.
        expense_in: The data for the new expense.
        
    Returns:
        The newly created Expense object.
    """
    db_expense = expense_model.Expense(
        description=expense_in.description,
        amount=expense_in.amount,
        payer_id=expense_in.payer_id,
        group_id=group_id
    )
    db.add(db_expense)
    db.flush() # To get the expense ID

    # Add participants
    for user_id in expense_in.participant_ids:
        db_participant = expense_model.ExpenseParticipant(
            expense_id=db_expense.id,
            user_id=user_id
        )
        db.add(db_participant)

    db.commit()
    db.refresh(db_expense)
    return db_expense

def delete_expense(db: Session, expense_id: uuid.UUID) -> expense_model.Expense | None:
    """
    Deletes an expense from the database.
    
    Args:
        db: The database session.
        expense_id: The ID of the expense to delete.
        
    Returns:
        The deleted Expense object if found, otherwise None.
    """
    db_expense = db.query(expense_model.Expense).filter(expense_model.Expense.id == expense_id).first()
    if db_expense:
        db.delete(db_expense)
        db.commit()
    return db_expense

def update_expense(db: Session, expense_id: uuid.UUID, expense_in: expense_schema.ExpenseUpdate) -> expense_model.Expense | None:
    """
    Updates an existing expense, including its participants.
    
    Args:
        db: The database session.
        expense_id: The ID of the expense to update.
        expense_in: The new data for the expense.
        
    Returns:
        The updated Expense object if found, otherwise None.
    """
    db_expense = db.query(expense_model.Expense).filter(expense_model.Expense.id == expense_id).first()
    if not db_expense:
        return None

    # Update expense fields
    db_expense.description = expense_in.description
    db_expense.amount = expense_in.amount
    db_expense.payer_id = expense_in.payer_id

    # Remove old participants
    db.query(expense_model.ExpenseParticipant).filter(expense_model.ExpenseParticipant.expense_id == expense_id).delete()
    
    # Add new participants
    for user_id in expense_in.participant_ids:
        db_participant = expense_model.ExpenseParticipant(
            expense_id=db_expense.id,
            user_id=user_id
        )
        db.add(db_participant)

    db.commit()
    db.refresh(db_expense)
    return db_expense

