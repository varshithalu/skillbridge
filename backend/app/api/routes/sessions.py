from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_current_user
from app.schemas.session import SessionCreate
from app.services.session_service import create_session
from app.utils.role_checker import require_role

router = APIRouter(prefix="/sessions", tags=["Sessions"])


@router.post("/")
def create_session_route(
    data: SessionCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    require_role(current_user, ["trainer"])

    return create_session(db, data, current_user.id)


@router.get("/{session_id}/attendance")
def get_attendance(
    session_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    require_role(current_user, ["trainer"])

    from app.models.attendance import Attendance

    return db.query(Attendance).filter(Attendance.session_id == session_id).all()