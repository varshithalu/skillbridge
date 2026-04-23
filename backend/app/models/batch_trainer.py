from sqlalchemy import Column, Integer
from app.db.base import Base

class BatchTrainer(Base):
    __tablename__ = "batch_trainers"

    id = Column(Integer, primary_key=True)
    batch_id = Column(Integer)
    trainer_id = Column(Integer)