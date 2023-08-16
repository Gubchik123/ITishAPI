from sqlalchemy.orm import Session
from sqlalchemy.orm.exc import NoResultFound

import models
from user.schemas import UserSchema
from auth.utils import get_hashed_password


def get_user_by_id(db: Session, id: int):
    """Returns user from database by id."""
    user = db.query(models.User).filter_by(id=id).first()
    if user is None:
        raise NoResultFound
    return user


def get_user_by_username(db: Session, user: str):
    """Returns user from database by username."""
    if isinstance(user, models.User):
        return user
    user = db.query(models.User).filter_by(username=user).first()
    if user is None:
        raise NoResultFound
    return user


def update_user(db: Session, username: str, user_schema: UserSchema):
    """Updates user in database by username."""
    user = get_user_by_username(db, username)
    user.username = user_schema.username
    user.email = user_schema.email
    user.password = get_hashed_password(user_schema.password)
    db.commit()
    return user


def update_user_avatar(db: Session, username: str, file_name: str):
    """Updates user avatar."""
    user = get_user_by_username(db, username)
    user.avatar = file_name
    db.commit()


def delete_user_by_username(db: Session, username: str):
    """Deletes user from database by username."""
    user = get_user_by_username(db, username)
    db.delete(user)
    db.commit()
    return user
