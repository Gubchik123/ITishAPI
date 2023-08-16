from pydantic import BaseModel


class _PostBaseSchema(BaseModel):
    """Post base schema."""

    title: str
    body: str
    tags: str = None


class PostSchema(_PostBaseSchema):
    """Post schema."""

    user_id: int = None


class PostUpdateSchema(_PostBaseSchema):
    """Post update schema."""


class CommentSchema(BaseModel):
    """Comment schema."""

    body: str
    post_id: int
    user_id: int = None


class CommentUpdateSchema(BaseModel):
    """Comment update schema."""

    id: int
    body: str


class LikeSchema(BaseModel):
    """Like schema."""

    post_id: int
    user_id: int
