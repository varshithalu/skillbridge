from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_current_user
from app.schemas.attendance import AttendanceMark
from app.services.attendance_service import mark_attendance
from app.utils.role_checker import require_role

router = APIRouter(prefix="/attendance", tags=["Attendance"])


@router.post("/mark")
def mark_attendance_route(
    data: AttendanceMark,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    require_role(current_user, ["student"])

    return mark_attendance(db, data.session_id, current_user.id, data.status)