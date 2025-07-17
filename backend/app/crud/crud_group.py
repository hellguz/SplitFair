# ./backend/app/crud/crud_group.py
"""
CRUD (Create, Read, Update, Delete) operations for Groups and Users.
"""
import uuid
from sqlalchemy.orm import Session, joinedload
from shortuuid import ShortUUID

from app.models import group as group_model
from app.models import user as user_model
from app.schemas import group as group_schema

def create_group_with_user(db: Session, group_in: group_schema.GroupCreate) -> group_model.Group:
    """
    Creates a new group and adds the creator as the first user.
    
    Args:
        db: The database session.
        group_in: The data for the new group and its first user.
        
    Returns:
        The newly created Group object.
    """
    # Create the group
    invite_code = ShortUUID().random(length=8)
    db_group = group_model.Group(name=group_in.name, invite_code=invite_code)
    db.add(db_group)
    db.flush() # flush to get the group ID

    # Create the first user and associate with the group
    db_user = user_model.User(
        client_uuid=group_in.client_uuid,
        display_name=group_in.user_display_name,
        group_id=db_group.id
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_group)
    return db_group

def get_group_by_invite_code(db: Session, invite_code: str) -> group_model.Group | None:
    """
    Retrieves a group by its unique invite code.
    
    Args:
        db: The database session.
        invite_code: The invite code of the group to retrieve.
        
    Returns:
        The Group object if found, otherwise None.
    """
    return db.query(group_model.Group).filter(group_model.Group.invite_code == invite_code).first()

def add_user_to_group(db: Session, group_id: uuid.UUID, user_in: group_schema.JoinGroup) -> user_model.User | None:
    """
    Adds a new user to an existing group.
    
    Args:
        db: The database session.
        group_id: The ID of the group to join.
        user_in: The data for the new user.
        
    Returns:
        The newly created User object or None if group not found.
    """
    db_group = db.query(group_model.Group).filter(group_model.Group.id == group_id).first()
    if not db_group:
        return None

    # Check if a user with this client_uuid is already in the group
    existing_user = db.query(user_model.User).filter(
        user_model.User.group_id == group_id,
        user_model.User.client_uuid == user_in.client_uuid
    ).first()
    
    if existing_user:
        return existing_user

    db_user = user_model.User(
        client_uuid=user_in.client_uuid,
        display_name=user_in.display_name,
        group_id=group_id
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_group(db: Session, group_id: uuid.UUID) -> group_model.Group | None:
    """
    Retrieves a single group with all its related users and expenses.
    
    Args:
        db: The database session.
        group_id: The ID of the group to retrieve.
        
    Returns:
        The fully loaded Group object if found, otherwise None.
    """
    return db.query(group_model.Group).options(
        joinedload(group_model.Group.users),
        joinedload(group_model.Group.expenses).joinedload(group_model.Expense.payer),
        joinedload(group_model.Group.expenses).joinedload(group_model.Expense.participants).joinedload(group_model.ExpenseParticipant.user)
    ).filter(group_model.Group.id == group_id).first()

def get_user_groups(db: Session, client_uuid: str) -> list[group_model.Group]:
    """
    Retrieves all groups that a specific user (by client_uuid) is a member of.
    
    Args:
        db: The database session.
        client_uuid: The client-side UUID of the user.
        
    Returns:
        A list of Group objects.
    """
    user_group_ids = db.query(user_model.User.group_id).filter(user_model.User.client_uuid == client_uuid).distinct()
    return db.query(group_model.Group).filter(group_model.Group.id.in_(user_group_ids)).all()

