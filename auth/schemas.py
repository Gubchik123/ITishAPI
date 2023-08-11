from pydantic import BaseModel

from user.schemas import UserSchema


class TokenSchema(BaseModel):
    """Schema for token response"""

    access_token: str
    refresh_token: str


class TokenPayload(BaseModel):
    """Schema for token payload"""

    sub: str
    exp: int


class UserAuth(UserSchema):
    """Schema for user authentication."""
