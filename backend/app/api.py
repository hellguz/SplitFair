import secrets
from typing import List, Dict, Any

from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app import crud, schemas
from app.db import session
from app.models import Group, User

api_router = APIRouter()


async def get_current_user(x_user_id: str = Header(...), db: AsyncSession = Depends(session.get_db)) -> User:
    """
    Dependency to get the current user based on the X-User-ID header.
    """
    user = await crud.get_user_by_uuid(db, user_uuid=x_user_id)
    if user is None:
        raise HTTPException(status_code=403, detail="User not found or invalid ID")
    return user

@api_router.post("/users", response_model=schemas.User)
async def create_user(user_in: schemas.UserCreate, db: AsyncSession = Depends(session.get_db)):
    """
    Creates a new user. The frontend calls this on first load if no user UUID exists.
    """
    db_user = await crud.get_user_by_uuid(db, user_uuid=user_in.uuid)
    if db_user:
        raise HTTPException(status_code=400, detail="User with this UUID already exists")
    return await crud.create_user(db=db, user=user_in)

@api_router.get("/users/me", response_model=schemas.User)
async def read_users_me(current_user: User = Depends(get_current_user)):
    """
    Gets the current user's details.
    """
    return current_user


@api_router.post("/groups", response_model=schemas.Group)
async def create_group(
    group_in: schemas.GroupCreate,
    db: AsyncSession = Depends(session.get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Creates a new group, adding the creator as the first member.
    """
    invite_code = secrets.token_urlsafe(8)
    return await crud.create_group(db=db, group=group_in, user_id=current_user.id, invite_code=invite_code)


@api_router.get("/users/me/groups", response_model=List[schemas.Group])
async def get_my_groups(
    db: AsyncSession = Depends(session.get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Retrieves all groups the current user is a member of.
    """
    return await crud.get_user_groups(db, user_id=current_user.id)


@api_router.post("/groups/join", response_model=schemas.Group)
async def join_group(
    join_request: schemas.GroupJoin,
    db: AsyncSession = Depends(session.get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Allows a user to join a group using an invite code.
    """
    group = await crud.get_group_by_invite_code(db, invite_code=join_request.invite_code)
    if not group:
        raise HTTPException(status_code=404, detail="Group with this invite code not found")
    
    is_member = await crud.is_user_in_group(db, user_id=current_user.id, group_id=group.id)
    if is_member:
        # User is already in the group, just return it.
        return group
    
    await crud.add_user_to_group(db, user_id=current_user.id, group_id=group.id)
    return group


@api_router.get("/groups/{group_id}", response_model=schemas.GroupDetails)
async def get_group_details(
    group_id: int,
    db: AsyncSession = Depends(session.get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Retrieves detailed information for a specific group, including members, expenses, and balances.
    """
    if not await crud.is_user_in_group(db, user_id=current_user.id, group_id=group_id):
        raise HTTPException(status_code=403, detail="User is not a member of this group")

    group = await crud.get_group(db, group_id=group_id)
    if not group:
        raise HTTPException(status_code=404, detail="Group not found")

    members = await crud.get_group_members(db, group_id=group_id)
    expenses = await crud.get_group_expenses(db, group_id=group_id)

    # Calculate balances
    balances: Dict[str, float] = {member.uuid: 0.0 for member in members}
    for expense in expenses:
        payer_uuid = next((m.uuid for m in members if m.id == expense.payer_id), None)
        if not payer_uuid:
            continue

        # Add the full amount to the payer
        balances[payer_uuid] += expense.amount
        
        # Deduct the share from each participant
        participants = await crud.get_expense_participants(db, expense_id=expense.id)
        if not participants:
            continue
        
        share = expense.amount / len(participants)
        for participant in participants:
            balances[participant.uuid] -= share

    # Create the detailed response
    group_details = schemas.GroupDetails(
        id=group.id,
        name=group.name,
        invite_code=group.invite_code,
        members=[schemas.User.from_orm(m) for m in members],
        expenses=[schemas.Expense.from_orm(e) for e in expenses],
        balances=[schemas.UserBalance(user_uuid=uuid, balance=round(balance, 2)) for uuid, balance in balances.items()]
    )

    return group_details


@api_router.post("/groups/{group_id}/expenses", response_model=schemas.Expense)
async def create_expense_for_group(
    group_id: int,
    expense_in: schemas.ExpenseCreate,
    db: AsyncSession = Depends(session.get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Adds a new expense to a group.
    """
    if not await crud.is_user_in_group(db, user_id=current_user.id, group_id=group_id):
        raise HTTPException(status_code=403, detail="User is not a member of this group")

    # Verify payer is the current user
    if current_user.uuid != expense_in.payer_uuid:
        raise HTTPException(status_code=403, detail="Payer must be the current user")

    # Verify all participants are members of the group
    all_participants_valid = await crud.are_users_in_group(db, user_uuids=expense_in.participant_uuids, group_id=group_id)
    if not all_participants_valid:
        raise HTTPException(status_code=400, detail="One or more participants are not members of the group")

    return await crud.create_expense(db=db, expense=expense_in, group_id=group_id)


@api_router.delete("/expenses/{expense_id}", status_code=204)
async def delete_expense(
    expense_id: int,
    db: AsyncSession = Depends(session.get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Deletes an expense. Only the user who paid for it can delete it.
    """
    expense = await crud.get_expense(db, expense_id=expense_id)
    if not expense:
        raise HTTPException(status_code=404, detail="Expense not found")
    
    if expense.payer_id != current_user.id:
        raise HTTPException(status_code=403, detail="Only the payer can delete the expense")

    await crud.delete_expense(db, expense_id=expense_id)
    return None
