from app.models.session import Session
from sqlalchemy.orm import Session as DBSession


def create_session(db: DBSession, data, trainer_id):
    session = Session(
        batch_id=data.batch_id,
        trainer_id=trainer_id,
        title=data.title,
        date=data.date,
        start_time=data.start_time,
        end_time=data.end_time
    )

    db.add(session)
    db.commit()
    db.refresh(session)

    return session