"""
CRUD operations for the Expense model.
"""
from sqlalchemy.orm import Session
from app.models import expense as expense_model
from app.schemas import expense as expense_schema
from app.crud import crud_group

def get_expense(db: Session, expense_id: int):
    """Retrieves a single expense by its ID."""
    return db.query(expense_model.Expense).filter(expense_model.Expense.id == expense_id).first()

def get_expenses_for_group(db: Session, group_id: int):
    """Retrieves all expenses associated with a specific group."""
    return db.query(expense_model.Expense).filter(expense_model.Expense.group_id == group_id).order_by(expense_model.Expense.date.desc()).all()

def create_expense(db: Session, expense: expense_schema.ExpenseCreate):
    """Creates a new expense record."""
    db_expense = expense_model.Expense(
        description=expense.description,
        amount=expense.amount,
        group_id=expense.group_id,
        paid_by_member_id=expense.paid_by_member_id
    )
    db.add(db_expense)
    db.commit()
    db.refresh(db_expense)

    # Link participants to the expense
    for member_id in expense.participant_member_ids:
        member = crud_group.get_member(db, member_id=member_id)
        if member:
            db_expense.participants.append(member)
    
    db.commit()
    db.refresh(db_expense)
    return db_expense

def delete_expense(db: Session, expense_id: int):
    """Deletes an expense from the database."""
    db_expense = db.query(expense_model.Expense).filter(expense_model.Expense.id == expense_id).first()
    if db_expense:
        db.delete(db_expense)
        db.commit()
    return db_expense

