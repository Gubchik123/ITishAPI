from sqlalchemy.orm import Session

from models import User
from auth import schemas
from db import add_commit_and_refresh


def get_user(db: Session, user_schema: schemas.UserSchema):
    """Returns user by email and username."""
    return (
        db.query(User)
        .filter(
            User.email == user_schema.email,
            User.username == user_schema.username,
        )
        .first()
    )


def get_user_by_email(db: Session, email: str):
    """Returns user by email."""
    return db.query(User).filter(User.email == email).first()


def create_user(db: Session, user_auth: schemas.UserAuth):
    """Creates and returns user."""
    return add_commit_and_refresh(db, User(**user_auth.dict()))
