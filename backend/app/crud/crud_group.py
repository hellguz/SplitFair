"""
CRUD operations for Group and GroupMember models.
"""
import uuid
from sqlalchemy.orm import Session
from app.models import group as group_model
from app.models import participant as participant_model
from app.schemas import group as group_schema

def get_group(db: Session, group_id: int):
    """Retrieves a single group by its ID."""
    return db.query(group_model.Group).filter(group_model.Group.id == group_id).first()

def get_group_by_invite_code(db: Session, invite_code: str):
    """Retrieves a single group by its unique invite code."""
    return db.query(group_model.Group).filter(group_model.Group.invite_code == invite_code).first()

def get_groups_for_participant(db: Session, participant_id: int):
    """Retrieves all groups a participant is a member of."""
    return db.query(group_model.Group).join(group_model.GroupMember).filter(group_model.GroupMember.participant_id == participant_id).all()

def create_group_with_member(db: Session, group: group_schema.GroupCreate, participant: participant_model.Participant, nickname: str):
    """Creates a new group and adds the first member."""
    # Create the group
    db_group = group_model.Group(
        name=group.name,
        invite_code=str(uuid.uuid4())
    )
    db.add(db_group)
    db.commit()
    db.refresh(db_group)

    # Add the creator as a member
    add_member_to_group(db, group_id=db_group.id, participant_id=participant.id, nickname=nickname)
    db.refresh(db_group)
    return db_group

def add_member_to_group(db: Session, group_id: int, participant_id: int, nickname: str):
    """Adds a participant to a group."""
    db_member = group_model.GroupMember(
        group_id=group_id,
        participant_id=participant_id,
        nickname=nickname
    )
    db.add(db_member)
    db.commit()
    db.refresh(db_member)
    return db_member

def get_group_members(db: Session, group_id: int):
    """Retrieves all members of a specific group."""
    return db.query(group_model.GroupMember).filter(group_model.GroupMember.group_id == group_id).all()

def get_member(db: Session, member_id: int):
    """Retrieves a group member by their unique member ID."""
    return db.query(group_model.GroupMember).filter(group_model.GroupMember.id == member_id).first()

def get_member_by_participant_id(db: Session, group_id: int, participant_id: int):
    """Retrieves a group member by group and participant ID."""
    return db.query(group_model.GroupMember).filter(group_model.GroupMember.group_id == group_id, group_model.GroupMember.participant_id == participant_id).first()

