from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_current_user
from app.utils.role_checker import require_role

router = APIRouter(prefix="/programme", tags=["Programme"])


@router.get("/summary")
def programme_summary(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    require_role(current_user, ["programme_manager"])

    from app.models.attendance import Attendance

    total = db.query(Attendance).count()

    return {
        "total_attendance_records": total
    }