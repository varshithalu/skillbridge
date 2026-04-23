from pydantic import BaseModel, EmailStr, field_validator

VALID_ROLES = [
    "student",
    "trainer",
    "institution",
    "programme_manager",
    "monitoring_officer"
]

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    role: str

    @field_validator("role")
    def validate_role(cls, value):
        if value not in VALID_ROLES:
            raise ValueError("Invalid role")
        return value


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"