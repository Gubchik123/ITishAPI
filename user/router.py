from typing import Callable, NoReturn

from sqlalchemy.orm import Session
from fastapi.responses import FileResponse
from fastapi.exceptions import HTTPException
from fastapi import APIRouter, UploadFile, BackgroundTasks, Depends, File

from models import User
from dependencies import get_db
from decorators import catch_model_not_fount
from user import crud, services, schemas
from auth.dependencies import get_current_user


user_router = APIRouter()


def _get_user_overview(user: str, db: Session = Depends(get_db)):
    """Returns user overview."""
    return crud.get_user_by_username(db, user)


def _get_user_posts(user: str, db: Session = Depends(get_db)):
    """Returns user posts."""
    return crud.get_user_by_username(db, user).posts.all()


def _get_user_comments(user: str, db: Session = Depends(get_db)):
    """Returns user comments."""
    return crud.get_user_by_username(db, user).comments.all()


def _get_user_liked_posts(user: str, db: Session = Depends(get_db)):
    """Returns user liked posts."""
    return crud.get_user_by_username(db, user).likes.all()


def _get_process_function(tab: str) -> Callable | NoReturn:
    """Returns function for processing tab."""
    if tab not in ("", "overview", "posts", "comments", "likes"):
        raise HTTPException(status_code=404, detail="Tab not found")
    return {
        "": _get_user_overview,
        "overview": _get_user_overview,
        "posts": _get_user_posts,
        "comments": _get_user_comments,
        "likes": _get_user_liked_posts,
    }.get(tab)


@user_router.get("/me")
def get_me(
    tab: str = "overview",
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return _get_process_function(tab)(user, db)


@user_router.put("/me")
@catch_model_not_fount("User")
def update_user(
    user_schema: schemas.UserSchema,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    """Updates user by username and returns user."""
    return crud.update_user(db, user, user_schema)


@user_router.put("/me/avatar")
@catch_model_not_fount("User")
def update_user_avatar(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    """Updates user avatar by username."""
    file_format = file.content_type.split("/")[-1]
    if file_format not in ("png", "jpg", "jpeg"):
        raise HTTPException(status_code=400, detail="Invalid file format")

    file_name = f"media/avatars/{user.username}.{file_format}"
    background_tasks.add_task(services.write_avatar, file_name, file)

    crud.update_user_avatar(db, user, file_name)
    return {"avatar": file_name}


@user_router.delete("/me")
@catch_model_not_fount("User")
def delete_user(
    user: User = Depends(get_current_user), db: Session = Depends(get_db)
):
    """Deletes user by username."""
    return crud.delete_user_by_username(db, user)


@user_router.get("/{username}")
@catch_model_not_fount("User")
def user_home_page(
    username: str, tab: str = "overview", db: Session = Depends(get_db)
):
    """Returns user by username."""
    return _get_process_function(tab)(username, db)


@user_router.get("/{username}/avatar")
@catch_model_not_fount("User")
def get_user_avatar(username: str, db: Session = Depends(get_db)):
    """Returns user avatar by username."""
    user = crud.get_user_by_username(db, username)
    return FileResponse(user.avatar)
