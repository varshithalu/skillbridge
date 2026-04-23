from fastapi import HTTPException
from app.models.attendance import Attendance
from app.models.batch_student import BatchStudent
from app.models.session import Session
from sqlalchemy.orm import Session as DBSession


def mark_attendance(db: DBSession, session_id, student_id, status):
    
    session = db.query(Session).filter(Session.id == session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    # check student belongs to batch
    mapping = db.query(BatchStudent).filter(
        BatchStudent.batch_id == session.batch_id,
        BatchStudent.student_id == student_id
    ).first()

    if not mapping:
        raise HTTPException(status_code=403, detail="Not enrolled in batch")

    attendance = Attendance(
        session_id=session_id,
        student_id=student_id,
        status=status
    )

    db.add(attendance)
    db.commit()

    return {"message": "Attendance marked"}