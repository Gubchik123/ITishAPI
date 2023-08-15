from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from auth import crud
from auth import utils
from auth import schemas
from dependencies import get_db


auth_router = APIRouter()


@auth_router.post("/signup")
def create_user(user_auth: schemas.UserSchema, db: Session = Depends(get_db)):
    user = crud.get_user(db, user_auth)
    if user is not None:
        raise HTTPException(
            status_code=400,
            detail="User with this email or username already exist.",
        )
    return crud.create_user(db, user_auth)


@auth_router.post(
    "/login",
    response_model=schemas.TokenSchema,
    summary="Create access and refresh tokens for user",
)
def login(
    db: Session = Depends(get_db),
    form_data: OAuth2PasswordRequestForm = Depends(),
):
    user = crud.get_user_by_email(db, form_data.username)
    if user is None or not user.is_valid_(form_data.password):
        raise HTTPException(
            status_code=400, detail="Incorrect email or password"
        )
    return {
        "user_id": user.id,
        "access_token": utils.create_access_token(user.email),
        "refresh_token": utils.create_refresh_token(user.email),
    }
