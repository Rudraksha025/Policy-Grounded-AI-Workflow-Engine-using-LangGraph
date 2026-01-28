from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from src.config import PG_DATABASE_URL, PG_DB, PG_HOST, PG_PASSWORD, PG_PORT, PG_USER
import os

engine = create_engine(PG_DATABASE_URL)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()