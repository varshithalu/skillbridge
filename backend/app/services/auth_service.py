from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models.user import User
from app.core.security import hash_password, verify_password, create_access_token

VALID_ROLES = [
    "student",
    "trainer",
    "institution",
    "programme_manager",
    "monitoring_officer"
]


def create_user(db: Session, name: str, email: str, password: str, role: str):
    
    # 🔥 Check duplicate email
    existing_user = db.query(User).filter(User.email == email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    # 🔥 Validate role
    if role not in VALID_ROLES:
        raise HTTPException(status_code=400, detail="Invalid role")

    user = User(
        name=name,
        email=email,
        hashed_password=hash_password(password),
        role=role
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def authenticate_user(db: Session, email: str, password: str):
    user = db.query(User).filter(User.email == email).first()

    if not user or not verify_password(password, user.hashed_password):
        return None

    token = create_access_token({
        "user_id": user.id,
        "role": user.role
    })

    return token