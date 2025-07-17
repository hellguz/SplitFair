from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from . import models, schemas

# User CRUD
async def get_user(db: AsyncSession, user_id: int):
    """Retrieves a user by their primary key ID."""
    result = await db.execute(select(models.User).filter(models.User.id == user_id))
    return result.scalar_one_or_none()

async def get_user_by_uuid(db: AsyncSession, user_uuid: str):
    """Retrieves a user by their public UUID."""
    result = await db.execute(select(models.User).filter(models.User.uuid == user_uuid))
    return result.scalar_one_or_none()

async def create_user(db: AsyncSession, user: schemas.UserCreate):
    """Creates a new user in the database."""
    db_user = models.User(uuid=user.uuid, name=user.name)
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user

# Group CRUD
async def create_group(db: AsyncSession, group: schemas.GroupCreate, user_id: int, invite_code: str):
    """Creates a new group and adds the creator as the first member."""
    db_group = models.Group(name=group.name, invite_code=invite_code)
    db.add(db_group)
    await db.commit()
    await db.refresh(db_group)
    
    # Add creator as member
    await add_user_to_group(db, user_id=user_id, group_id=db_group.id)
    
    return db_group

async def get_group(db: AsyncSession, group_id: int):
    """Retrieves a single group by its ID."""
    result = await db.execute(select(models.Group).filter(models.Group.id == group_id))
    return result.scalar_one_or_none()
    
async def get_group_by_invite_code(db: AsyncSession, invite_code: str):
    """Retrieves a single group by its unique invite code."""
    result = await db.execute(select(models.Group).filter(models.Group.invite_code == invite_code))
    return result.scalar_one_or_none()

async def get_user_groups(db: AsyncSession, user_id: int):
    """Retrieves all groups a user is a member of."""
    result = await db.execute(
        select(models.Group)
        .join(models.group_members)
        .filter(models.group_members.c.user_id == user_id)
    )
    return result.scalars().all()

async def add_user_to_group(db: AsyncSession, user_id: int, group_id: int):
    """Adds a user to a group's membership list."""
    stmt = models.group_members.insert().values(user_id=user_id, group_id=group_id)
    await db.execute(stmt)
    await db.commit()

async def get_group_members(db: AsyncSession, group_id: int) -> List[models.User]:
    """Retrieves all users who are members of a specific group."""
    result = await db.execute(
        select(models.User)
        .join(models.group_members)
        .filter(models.group_members.c.group_id == group_id)
    )
    return result.scalars().all()

async def is_user_in_group(db: AsyncSession, user_id: int, group_id: int) -> bool:
    """Checks if a user is a member of a group."""
    result = await db.execute(
        select(models.group_members)
        .filter_by(user_id=user_id, group_id=group_id)
    )
    return result.first() is not None

async def are_users_in_group(db: AsyncSession, user_uuids: List[str], group_id: int) -> bool:
    """Checks if all specified users (by UUID) are members of a group."""
    members = await get_group_members(db, group_id)
    member_uuids = {member.uuid for member in members}
    return set(user_uuids).issubset(member_uuids)

# Expense CRUD
async def create_expense(db: AsyncSession, expense: schemas.ExpenseCreate, group_id: int):
    """Creates a new expense and links it to its participants."""
    payer = await get_user_by_uuid(db, user_uuid=expense.payer_uuid)
    if not payer:
        return None # Should be handled in API layer

    db_expense = models.Expense(
        description=expense.description,
        amount=expense.amount,
        group_id=group_id,
        payer_id=payer.id
    )
    db.add(db_expense)
    await db.commit()
    await db.refresh(db_expense)
    
    # Link participants
    for user_uuid in expense.participant_uuids:
        participant = await get_user_by_uuid(db, user_uuid=user_uuid)
        if participant:
            stmt = models.expense_participants.insert().values(
                user_id=participant.id, 
                expense_id=db_expense.id
            )
            await db.execute(stmt)
    
    await db.commit()
    await db.refresh(db_expense)
    # Eagerly load relationships for the response model
    result = await db.execute(
        select(models.Expense).options(selectinload(models.Expense.participants)).filter_by(id=db_expense.id)
    )
    return result.scalar_one()

async def get_expense(db: AsyncSession, expense_id: int):
    """Retrieves a single expense by ID."""
    result = await db.execute(select(models.Expense).filter_by(id=expense_id))
    return result.scalar_one_or_none()

async def get_group_expenses(db: AsyncSession, group_id: int) -> List[models.Expense]:
    """Retrieves all expenses associated with a specific group."""
    result = await db.execute(
        select(models.Expense)
        .filter(models.Expense.group_id == group_id)
        .order_by(models.Expense.created_at.desc())
    )
    return result.scalars().all()

async def get_expense_participants(db: AsyncSession, expense_id: int) -> List[models.User]:
    """Retrieves all users who participated in a specific expense."""
    result = await db.execute(
        select(models.User)
        .join(models.expense_participants)
        .filter(models.expense_participants.c.expense_id == expense_id)
    )
    return result.scalars().all()

async def delete_expense(db: AsyncSession, expense_id: int):
    """Deletes an expense from the database."""
    db_expense = await get_expense(db, expense_id)
    if db_expense:
        await db.delete(db_expense)
        await db.commit()