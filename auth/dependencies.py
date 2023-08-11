from datetime import datetime

from jose import jwt
from sqlalchemy.orm import Session
from pydantic import ValidationError
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

from dependencies import get_db
from auth.crud import get_user_by_email
from auth.utils import ALGORITHM, JWT_SECRET_KEY
from auth.schemas import TokenPayload, UserSchema


def get_current_user(
    token: str = Depends(
        OAuth2PasswordBearer(tokenUrl="/api/auth/login", scheme_name="JWT")
    ),
    db: Session = Depends(get_db),
) -> UserSchema:
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[ALGORITHM])
        token_data = TokenPayload(**payload)

        if datetime.fromtimestamp(token_data.exp) < datetime.now():
            raise HTTPException(
                status_code=401,
                detail="Token expired",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except (jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=403,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if (user := get_user_by_email(db, token_data.sub)) is None:
        raise HTTPException(status_code=404, detail="Could not find user")
    return user
