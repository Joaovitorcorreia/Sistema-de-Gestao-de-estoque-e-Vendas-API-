import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

load_dotenv()

os.environ["PGCLIENTENDCODING"] = "utf-8"
os.environ["LC_ALL"] = "C"


SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()