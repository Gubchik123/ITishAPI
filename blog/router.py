from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, Body
from fastapi.exceptions import HTTPException

from blog import crud, schemas
from dependencies import get_db
from models import User, Comment
from decorators import catch_model_not_fount
from auth.dependencies import get_current_user


blog_router = APIRouter()


@blog_router.get("/")
def home_blog_page(
    tab: str = "posts", q: str = None, db: Session = Depends(get_db)
):
    """Returns all posts or tags from database."""
    if tab not in ("posts", "tags", ""):
        raise HTTPException(status_code=404, detail="Tab not found")
    return {
        "": crud.get_all_posts,
        "posts": crud.get_all_posts,
        "tags": crud.get_all_tags,
    }.get(tab)(db, q)


# * Post ----------------------------------------------------------------------


@blog_router.post("/post")
def create_post(
    post_schema: schemas.PostSchema,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    """Creates post in database and returns it."""
    post_schema.user_id = user.id
    return crud.create_post(db, post_schema)


@blog_router.get("/post/{slug}")
@catch_model_not_fount(model="Post")
def get_post_by_slug(slug: str, db: Session = Depends(get_db)):
    """Returns post from database by slug."""
    return crud.get_post_by_slug(db, slug)


@blog_router.get("/post/{slug}/comments")
@catch_model_not_fount(model="Post")
def get_all_post_comments(slug: str, db: Session = Depends(get_db)):
    """Returns post from database by slug."""
    return (
        crud.get_post_by_slug(db, slug)
        .comments.order_by(Comment.id.desc())
        .all()
    )


@blog_router.get("/post/{slug}/likes")
@catch_model_not_fount(model="Post")
def get_all_post_likes(slug: str, db: Session = Depends(get_db)):
    """Returns post from database by slug."""
    return [like.user_id for like in crud.get_post_by_slug(db, slug).likes]


@blog_router.put("/post/{slug}")
@catch_model_not_fount(model="Post")
def update_post(
    slug: str,
    post_update_schema: schemas.PostUpdateSchema,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    """Updates post in database and returns it."""
    return crud.update_post(db, slug, post_update_schema, user.id)


@blog_router.delete("/post/{slug}")
@catch_model_not_fount(model="Post")
def delete_post_by_slug(
    slug: str,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    """Deletes post from database by slug."""
    return crud.delete_post(db, slug, user.id)


# * Tag -----------------------------------------------------------------------


@blog_router.get("/tag/{slug}")
@catch_model_not_fount(model="Tag")
def get_all_posts_by_tag_slug(slug: str, db: Session = Depends(get_db)):
    """Returns all posts by tag slug."""
    return crud.get_tag_by_slug(db, slug).posts.all()


# * Comment -------------------------------------------------------------------


@blog_router.post("/comment")
def create_comment(
    comment_schema: schemas.CommentSchema,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    comment_schema.user_id = user.id
    return crud.create_comment(db, comment_schema)


@blog_router.put("/comment")
@catch_model_not_fount(model="Comment")
def update_comment(
    comment_update_schema: schemas.CommentUpdateSchema,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    return crud.update_comment(db, comment_update_schema, user.id)


@blog_router.delete("/comment")
@catch_model_not_fount(model="Comment")
def delete_comment(
    comment_delete_schema: schemas.CommentDeleteSchema,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    return crud.delete_comment(db, comment_delete_schema.id, user.id)


# * Like ----------------------------------------------------------------------


@blog_router.post("/like")
def create_like(
    like_schema: schemas.LikeSchema,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    return crud.create_like(db, like_schema)


@blog_router.delete("/like")
@catch_model_not_fount(model="Like")
def delete_like(
    like_schema: schemas.LikeSchema,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    return crud.delete_like(db, like_schema, user.id)
