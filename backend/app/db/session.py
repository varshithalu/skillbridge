from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import DATABASE_URL

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    pool_recycle=300,
    connect_args={"sslmode": "require"}  # 🔥 important for Neon
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)