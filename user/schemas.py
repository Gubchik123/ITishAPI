from pydantic import BaseModel


class UserSchema(BaseModel):
    """User schema."""

    username: str
    email: str
    password: str