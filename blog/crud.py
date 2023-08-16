from typing import NoReturn

from fastapi import HTTPException
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.orm import Session, joinedload

import models
from blog import schemas, services
from db import commit_and_refresh, add_commit_and_refresh


# * C - create ----------------------------------------------------------------


def create_post(db: Session, post_schema: schemas.PostSchema):
    """Creates post in database and returns it."""
    post = models.Post(**post_schema.dict(exclude={"tags"}))
    post.tags = services._get_all_tags_for_post_from_(post_schema, db)
    return add_commit_and_refresh(db, post)


def create_comment(db: Session, comment_schema: schemas.CommentSchema):
    """Creates comment in database and returns it."""
    comment = models.Comment(**comment_schema.dict())
    return add_commit_and_refresh(db, comment)


def create_like(db: Session, like_schema: schemas.LikeSchema):
    """Creates like in database and returns it."""
    like = models.Like(**like_schema.dict())
    return add_commit_and_refresh(db, like)


# * R - read ------------------------------------------------------------------


def _get_all_posts_by_query(db: Session, query: str):
    """Returns all posts from database by query."""
    return (
        db.query(models.Post)
        .filter(models.Post.title.ilike(f"%{query}%"))
        .all()
    )


def get_all_posts(db: Session, query: str):
    """Returns all posts from database."""
    return (
        db.query(models.Post).all()
        if not query
        else _get_all_posts_by_query(db, query)
    )


def get_all_tags(db: Session, query: str):
    """Returns all tags from database."""
    return db.query(models.Tag).all()


def get_post_by_slug(db: Session, slug: str):
    """Returns post from database by slug."""
    post = (
        db.query(models.Post)
        .filter(models.Post.slug == slug)
        .options(joinedload(models.Post.tags))
        .first()
    )
    if post is None:
        raise NoResultFound
    return post


def get_tag_by_slug(db: Session, slug: str):
    """Returns tag from database by slug."""
    tag = db.query(models.Tag).filter(models.Tag.slug == slug).first()
    if tag is None:
        raise NoResultFound
    return tag


def _get_comment_by_id(db: Session, comment_id: int):
    """Returns comment from database by id."""
    comment = (
        db.query(models.Comment)
        .filter(models.Comment.id == comment_id)
        .first()
    )
    if comment is None:
        raise NoResultFound
    return comment


# * U - update ----------------------------------------------------------------


def check_if_current_user_if_owner(
    object_user_id, current_user_id
) -> None | NoReturn:
    """Checks if current user is owner of object."""
    if not object_user_id == current_user_id:
        raise HTTPException(status_code=403, detail="Forbidden")


def update_post(
    db: Session,
    slug: str,
    post_schema: schemas.PostSchema,
    current_user_id: int,
):
    """Updates post in database and returns it."""
    post = get_post_by_slug(db, slug)
    check_if_current_user_if_owner(post.user_id, current_user_id)

    post.title = post_schema.title
    post.slug = post.generate_slug()
    post.body = post_schema.body
    post.tags = services._get_all_tags_for_post_from_(post_schema, db)
    return commit_and_refresh(db, post)


def update_comment(
    db: Session,
    comment_update_schema: schemas.CommentUpdateSchema,
    current_user_id: int,
):
    """Updates comment in database and returns it."""
    comment = _get_comment_by_id(db, comment_update_schema.id)
    check_if_current_user_if_owner(comment.user_id, current_user_id)

    comment.body = comment_update_schema.body
    return commit_and_refresh(db, comment)


# * D - delete ----------------------------------------------------------------


def _delete_and_commit(db: Session, model: models.Base):
    """Deletes model from database and returns it."""
    db.delete(model)
    db.commit()
    return model


def delete_post(db: Session, slug: str, current_user_id: int):
    """Deletes post from database and returns it."""
    post = get_post_by_slug(db, slug)
    check_if_current_user_if_owner(post.user_id, current_user_id)
    return _delete_and_commit(db, post)


def delete_comment(db: Session, comment_id: int, current_user_id: int):
    """Deletes comment from database and returns it."""
    comment = _get_comment_by_id(db, comment_id)
    check_if_current_user_if_owner(comment.user_id, current_user_id)
    return _delete_and_commit(db, comment)


def delete_like(
    db: Session, like_schema: schemas.LikeSchema, current_user_id: int
):
    """Deletes like from database and returns it."""
    like = (
        db.query(models.Like)
        .filter(
            models.Like.post_id == like_schema.post_id,
            models.Like.user_id == like_schema.user_id,
        )
        .first()
    )
    if like is None:
        raise NoResultFound
    check_if_current_user_if_owner(like.user_id, current_user_id)
    return _delete_and_commit(db, like)
