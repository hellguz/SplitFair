# ./backend/app/api/v1/groups.py
"""
API endpoints for managing groups.
"""
import uuid
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas import group as group_schema
from app.crud import crud_group

router = APIRouter()

@router.post("/groups", response_model=group_schema.Group, status_code=status.HTTP_201_CREATED)
def create_group(
    group_in: group_schema.GroupCreate,
    db: Session = Depends(get_db)
):
    """
    Create a new group. The user creating the group is automatically added as a member.
    """
    return crud_group.create_group_with_user(db=db, group_in=group_in)

@router.get("/groups", response_model=List[group_schema.Group])
def get_user_groups(
    client_uuid: str,
    db: Session = Depends(get_db)
):
    """
    Get all groups that a user is a member of, identified by their client_uuid.
    """
    if not client_uuid:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="client_uuid is required")
    return crud_group.get_user_groups(db=db, client_uuid=client_uuid)

@router.get("/groups/{group_id}", response_model=group_schema.Group)
def get_group_details(
    group_id: uuid.UUID,
    db: Session = Depends(get_db)
):
    """
    Get detailed information for a single group, including users and expenses.
    """
    db_group = crud_group.get_group(db, group_id=group_id)
    if db_group is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Group not found")
    return db_group

@router.post("/groups/join/{invite_code}", response_model=group_schema.Group)
def join_group(
    invite_code: str,
    join_request: group_schema.JoinGroup,
    db: Session = Depends(get_db)
):
    """
    Allow a user to join an existing group using an invite code.
    """
    db_group = crud_group.get_group_by_invite_code(db, invite_code=invite_code)
    if db_group is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid invite code")
    
    crud_group.add_user_to_group(db, group_id=db_group.id, user_in=join_request)
    
    # Return the full group details after joining
    updated_group = crud_group.get_group(db, group_id=db_group.id)
    return updated_group

