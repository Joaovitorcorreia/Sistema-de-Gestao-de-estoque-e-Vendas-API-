import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

load_dotenv()

os.environ["PGCLIENTENDCODING"] = "utf-8"
os.environ["LC_ALL"] = "C"

# Get database URL from environment, fallback to a local SQLite file for development
DATABASE_URL = os.getenv("DATABASE_URL") or "sqlite:///./dev.db"

# For SQLite we must pass check_same_thread; otherwise leave defaults for other DBs
if DATABASE_URL.startswith("sqlite"):
    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
else:
    engine = create_engine(DATABASE_URL, pool_pre_ping=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()