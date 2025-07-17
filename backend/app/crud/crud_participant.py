"""
CRUD operations for the Participant model.
"""
from sqlalchemy.orm import Session
from app.models import participant as participant_model

def get_participant_by_client_id(db: Session, client_id: str):
    """Retrieves a participant by their client_id (UUID from browser)."""
    return db.query(participant_model.Participant).filter(participant_model.Participant.client_id == client_id).first()

def create_participant(db: Session, client_id: str):
    """Creates a new participant record."""
    db_participant = participant_model.Participant(client_id=client_id)
    db.add(db_participant)
    db.commit()
    db.refresh(db_participant)
    return db_participant

def get_or_create_participant(db: Session, client_id: str):
    """
    Looks for a participant by client_id and returns it.
    If not found, creates a new one.
    """
    db_participant = get_participant_by_client_id(db, client_id)
    if not db_participant:
        db_participant = create_participant(db, client_id)
    return db_participant

