import os

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from dotenv import load_dotenv


load_dotenv()

SQLALCHEMY_DATABASE_URL = str(os.getenv("DATABASE_URL"))

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def commit_and_refresh(db: Session, model: Base):
    """Commits and refreshes model instance and returns it."""
    db.commit()
    db.refresh(model)
    return model


def add_commit_and_refresh(db: Session, model: Base):
    """Adds, commits and refreshes model instance and returns it."""
    db.add(model)
    return commit_and_refresh(db, model)
