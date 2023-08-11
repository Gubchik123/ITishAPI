import re
from datetime import datetime

from sqlalchemy.orm import relationship, backref
from sqlalchemy import (
    Table,
    Column,
    Integer,
    String,
    Text,
    DateTime,
    ForeignKey,
)

from db import Base
from auth.utils import password_context, get_hashed_password


class User(Base):
    """Model for storing information about users."""

    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String(50), nullable=False, unique=True)
    email = Column(String(255), nullable=False, unique=True)
    password = Column(String(110), nullable=False)
    created = Column(DateTime, default=datetime.today())
    avatar = Column(String, nullable=True, default="media/avatars/default.png")

    posts = relationship(
        "Post",
        backref=backref("user", lazy="joined"),
        lazy="dynamic",
        passive_deletes=True,
    )
    comments = relationship(
        "Comment",
        backref=backref("user", lazy="joined"),
        lazy="dynamic",
        passive_deletes=True,
    )
    likes = relationship(
        "Like",
        backref=backref("user", lazy="joined"),
        lazy="dynamic",
        passive_deletes=True,
    )

    def __init__(self, *args, **kwargs) -> None:
        """Adds hashed password to user instance."""
        super(User, self).__init__(*args, **kwargs)
        self.password = get_hashed_password(self.password)

    def is_valid_(self, password: str) -> bool:
        """Checks if given password is valid."""
        return password_context.verify(password, self.password)


class _ModelWithSlug:
    """Mixin for models with 'slug' column."""

    def __str__(self) -> str:
        """Returns string representation of model instance."""
        return f"<{self.title}>"

    def __repr__(self) -> str:
        """Returns string representation of model instance."""
        return f"<{self.title}>"

    def generate_slug(self) -> None:
        """Generates slug from title."""
        self.slug = self._get_correct_slug_from_(self.title)

    def _get_correct_slug_from_(self, title: str) -> str:
        """Returns correct slug from given string."""
        return re.sub(pattern=r"[^\w+]", repl="-", string=title).lower()


# Table for many-to-many relationship between posts and tags
post_tags = Table(
    "post_tags",
    Base.metadata,
    Column("post_id", Integer, ForeignKey("posts.id")),
    Column("tag_id", Integer, ForeignKey("tags.id")),
)


class Post(_ModelWithSlug, Base):
    """Model for storing information about posts"""

    __tablename__ = "posts"

    id = Column(Integer, primary_key=True)
    title = Column(String(70), nullable=False, unique=True)
    slug = Column(String(70), nullable=True, unique=True)
    body = Column(Text, nullable=False)
    created = Column(DateTime, default=datetime.today())
    user_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    tags = relationship(
        "Tag", secondary=post_tags, backref=backref("posts", lazy="dynamic")
    )
    comments = relationship(
        "Comment",
        backref=backref("post", lazy="joined"),
        lazy="dynamic",
        passive_deletes=True,
    )
    likes = relationship(
        "Like",
        backref=backref("post", lazy="joined"),
        lazy="dynamic",
        passive_deletes=True,
    )

    def __init__(self, *args, **kwargs) -> None:
        """For setting correct slug during initializing"""
        super(Post, self).__init__(*args, **kwargs)
        self.generate_slug()


class Tag(_ModelWithSlug, Base):
    """Model for storing information about tags"""

    __tablename__ = "tags"

    id = Column(Integer, primary_key=True)
    title = Column(String(30), nullable=False, unique=True)
    slug = Column(String(30), nullable=False, unique=True)

    def __init__(self, *args, **kwargs) -> None:
        """For setting correct slug during initializing"""
        super(Tag, self).__init__(*args, **kwargs)
        self.generate_slug()


class Comment(Base):
    """Model for storing information about comments"""

    __tablename__ = "comments"

    id = Column(Integer, primary_key=True)
    body = Column(Text, nullable=False)
    created = Column(DateTime, default=datetime.today())
    user_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    post_id = Column(
        Integer, ForeignKey("posts.id", ondelete="CASCADE"), nullable=False
    )


class Like(Base):
    """Model for storing information about likes"""

    __tablename__ = "likes"

    id = Column(Integer, primary_key=True)
    created = Column(DateTime, default=datetime.today())
    user_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    post_id = Column(
        Integer, ForeignKey("posts.id", ondelete="CASCADE"), nullable=False
    )
