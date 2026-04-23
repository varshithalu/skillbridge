from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.core.security import decode_token
from app.models.attendance import Attendance

router = APIRouter(prefix="/monitoring", tags=["Monitoring"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


@router.get("/attendance")
def monitoring_attendance(
    request: Request,
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    # ❗ Enforce GET only (extra safety)
    if request.method != "GET":
        raise HTTPException(status_code=405, detail="Method Not Allowed")

    payload = decode_token(token)

    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")

    if payload.get("scope") != "monitoring":
        raise HTTPException(status_code=401, detail="Invalid monitoring token")

    return db.query(Attendance).all()