import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

load_dotenv()

os.environ["PGCLIENTENDCODING"] = "utf-8"
os.environ["LC_ALL"] = "C"

# Get database URL from environment. PostgreSQL is required for this deployment.
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise RuntimeError(
        "DATABASE_URL environment variable is not set. Set it to your PostgreSQL DSN, e.g. 'postgresql://user:pass@host:port/dbname'"
    )

# Create engine with pool pre-ping to handle dropped connections
engine = create_engine(DATABASE_URL, pool_pre_ping=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()