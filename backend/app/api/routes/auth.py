from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.schemas.user import UserCreate, UserLogin, TokenResponse
from app.services.auth_service import create_user, authenticate_user
from app.api.deps import get_db, get_current_user
from app.core.config import MONITORING_API_KEY
from app.core.security import create_monitoring_token
from app.utils.role_checker import require_role

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/signup", response_model=TokenResponse)
def signup(user: UserCreate, db: Session = Depends(get_db)):
    new_user = create_user(db, user.name, user.email, user.password, user.role)

    token = authenticate_user(db, user.email, user.password)

    return {"access_token": token}


@router.post("/login", response_model=TokenResponse)
def login(user: UserLogin, db: Session = Depends(get_db)):
    token = authenticate_user(db, user.email, user.password)

    if not token:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    return {"access_token": token}




@router.get("/me")
def get_me(current_user = Depends(get_current_user)):
    return {
        "id": current_user.id,
        "email": current_user.email,
        "role": current_user.role
    }


@router.get("/trainer-only")
def trainer_only(current_user = Depends(get_current_user)):
    require_role(current_user, ["trainer"])
    return {"message": "Welcome trainer!"}


@router.post("/monitoring-token")
def get_monitoring_token(
    key: str,
    current_user = Depends(get_current_user)
):
    if current_user.role != "monitoring_officer":
        raise HTTPException(status_code=403, detail="Not allowed")

    if key != MONITORING_API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API key")

    token = create_monitoring_token({
        "user_id": current_user.id,
        "role": current_user.role
    })

    return {"access_token": token}
