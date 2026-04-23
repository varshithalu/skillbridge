from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_current_user
from app.schemas.batch import BatchCreate, InviteResponse, JoinBatchRequest
from app.services.batch_service import create_batch, generate_invite, join_batch
from app.utils.role_checker import require_role

router = APIRouter(prefix="/batches", tags=["Batches"])


@router.post("/")
def create_batch_route(
    batch: BatchCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    require_role(current_user, ["trainer", "institution"])

    return create_batch(db, batch.name, batch.institution_id)


@router.post("/{batch_id}/invite", response_model=InviteResponse)
def create_invite(
    batch_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    require_role(current_user, ["trainer"])

    invite = generate_invite(db, batch_id, current_user.id)

    return {"token": invite.token}


@router.post("/join")
def join_batch_route(
    data: JoinBatchRequest,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    require_role(current_user, ["student"])

    return join_batch(db, data.token, current_user.id)

@router.get("/{batch_id}/summary")
def batch_summary(
    batch_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    require_role(current_user, ["institution"])

    from app.models.attendance import Attendance
    from app.models.session import Session

    sessions = db.query(Session).filter(Session.batch_id == batch_id).all()

    total = 0
    present = 0

    for s in sessions:
        records = db.query(Attendance).filter(Attendance.session_id == s.id).all()
        total += len(records)
        present += len([r for r in records if r.status == "present"])

    return {
        "total_records": total,
        "present": present,
        "attendance_rate": (present / total * 100) if total else 0
    }