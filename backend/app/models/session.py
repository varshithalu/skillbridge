from sqlalchemy import Column, Integer, String, Date, Time, DateTime
from datetime import datetime
from app.db.base import Base

class Session(Base):
    __tablename__ = "sessions"

    id = Column(Integer, primary_key=True)
    batch_id = Column(Integer)
    trainer_id = Column(Integer)
    title = Column(String)
    date = Column(Date)
    start_time = Column(Time)
    end_time = Column(Time)
    created_at = Column(DateTime, default=datetime.utcnow)