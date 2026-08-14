import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

load_dotenv()

os.environ["PGCLIENTENDCODING"] = "utf-8"
os.environ["LC_ALL"] = "C"

# Get database URL from environment. PostgreSQL is required for this deployment.
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")



# Create engine with pool pre-ping to handle dropped connections
engine = create_engine(SQLALCHEMY_DATABASE_URL, pool_pre_ping=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()