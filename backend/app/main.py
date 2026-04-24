from fastapi import FastAPI
from app.db.init_db import init_db
from app.api.routes import auth, batches, sessions, attendance, programme

app = FastAPI()

@app.on_event("startup")
def on_startup():
    try:
        init_db()
    except Exception as e:
        print("Startup failed but app will continue:", e)

@app.get("/")
def root():
    return {"message": "SkillBridge API is running 🚀"}

from app.api.routes import auth, batches, sessions, attendance, programme

app.include_router(auth.router)
app.include_router(batches.router)
app.include_router(sessions.router)
app.include_router(attendance.router)
app.include_router(programme.router)
