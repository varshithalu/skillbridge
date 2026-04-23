import uuid
from datetime import datetime, timedelta
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.batch import Batch
from app.models.batch_invite import BatchInvite
from app.models.batch_student import BatchStudent


def create_batch(db: Session, name: str, institution_id: int):
    batch = Batch(name=name, institution_id=institution_id)
    db.add(batch)
    db.commit()
    db.refresh(batch)
    return batch


def generate_invite(db: Session, batch_id: int, trainer_id: int):
    token = str(uuid.uuid4())

    invite = BatchInvite(
        batch_id=batch_id,
        token=token,
        created_by=trainer_id,
        expires_at=datetime.utcnow() + timedelta(hours=24)
    )

    db.add(invite)
    db.commit()
    db.refresh(invite)

    return invite


def join_batch(db, token: str, student_id: int):
    invite = db.query(BatchInvite).filter(BatchInvite.token == token).first()

    if not invite:
        raise HTTPException(status_code=404, detail="Invalid token")

    if invite.used:
        raise HTTPException(status_code=400, detail="Token already used")

    if invite.expires_at < datetime.utcnow():
        raise HTTPException(status_code=400, detail="Token expired")

    # Add student to batch
    db.add(BatchStudent(
        batch_id=invite.batch_id,
        student_id=student_id
    ))

    invite.used = True

    db.commit()

    return {"message": "Joined batch successfully"}