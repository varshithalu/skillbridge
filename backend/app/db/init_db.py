from app.db.base import Base
from app.db.session import engine, SessionLocal

from app.models.user import User
from app.models.batch import Batch
from app.models.batch_invite import BatchInvite
from app.models.batch_student import BatchStudent
from app.models.batch_trainer import BatchTrainer
from app.models.session import Session
from app.models.attendance import Attendance

from app.core.security import hash_password

from datetime import date, time


def init_db():
    try:
        Base.metadata.create_all(bind=engine)

        db = SessionLocal()

        existing_inst = db.query(User).filter(User.email == "inst1@mail.com").first()
        if existing_inst:
            db.close()
            return

        # 🏫 Institutions
        inst1 = User(   
            name="Institution A",
            email="inst1@mail.com",
            hashed_password=hash_password("123"),
            role="institution"
        )
        inst2 = User(
            name="Institution B",
            email="inst2@mail.com",
            hashed_password=hash_password("123"),
            role="institution"
        )

        db.add_all([inst1, inst2])
        db.commit()
        db.refresh(inst1)
        db.refresh(inst2)

        # 👨‍🏫 Trainers
        trainers = []
        for i in range(4):
            trainer = User(
                name=f"Trainer {i}",
                email=f"trainer{i}@mail.com",
                hashed_password=hash_password("123"),
                role="trainer",
                institution_id=inst1.id
            )
            trainers.append(trainer)

        db.add_all(trainers)
        db.commit()
        for t in trainers:
            db.refresh(t)

        # 👨‍🎓 Students
        students = []
        for i in range(15):
            student = User(
                name=f"Student {i}",
                email=f"student{i}@mail.com",
                hashed_password=hash_password("123"),
                role="student",
                institution_id=inst1.id
            )
            students.append(student)

        db.add_all(students)
        db.commit()
        for s in students:
            db.refresh(s)

        # 📦 Batches
        batches = []
        for i in range(3):
            batch = Batch(
                name=f"Batch {i}",
                institution_id=inst1.id
            )
            batches.append(batch)

        db.add_all(batches)
        db.commit()
        for b in batches:
            db.refresh(b)

        # 🔗 Assign trainers + students
        for batch in batches:
            for t in trainers[:2]:
                db.add(BatchTrainer(batch_id=batch.id, trainer_id=t.id))

            for s in students[:5]:
                db.add(BatchStudent(batch_id=batch.id, student_id=s.id))

        db.commit()

        # 📅 Sessions
        sessions = []
        for i in range(8):
            session = Session(
                batch_id=batches[i % 3].id,
                trainer_id=trainers[0].id,
                title=f"Session {i}",
                date=date.today(),
                start_time=time(10, 0),
                end_time=time(11, 0)
            )
            sessions.append(session)

        db.add_all(sessions)
        db.commit()
        for s in sessions:
            db.refresh(s)

        # 📊 Attendance
        for session in sessions:
            for student in students[:5]:
                db.add(Attendance(
                    session_id=session.id,
                    student_id=student.id,
                    status="present"
                ))

        db.commit()

        db.close()

    except Exception as e:
        print("DB INIT ERROR:", str(e))  