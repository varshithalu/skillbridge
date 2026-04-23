from pydantic import BaseModel


class AttendanceMark(BaseModel):
    session_id: int
    status: str  # present / absent / late