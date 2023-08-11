from sqlalchemy.orm import Session

from models import Post, Tag
from blog.schemas import PostSchema


def _there_is_not_tag_with_such_(title: str, db: Session) -> bool:
    """Returns True if there is not tag with such title in database."""
    return not db.query(Tag).filter(Tag.title == title).first()


def _create_non_existent_tags_from_(
    tag_titles: list[str], db: Session
) -> None:
    """Creates non-existent tags from given list of tag titles."""
    for tag_title in tag_titles:
        if _there_is_not_tag_with_such_(tag_title, db):
            db.add(Tag(title=tag_title))
    db.commit()


def _get_tag_titles_from_(tags: str, db: Session):
    """Returns tag titles from the given string."""
    tag_titles = [tag_title.strip().lower() for tag_title in tags.split(",")]
    _create_non_existent_tags_from_(tag_titles, db)
    return tag_titles


def _get_all_tags_for_post_from_(post_schema: PostSchema, db: Session):
    """Returns all tags for post from given post schema."""
    return (
        [
            db.query(Tag).filter(Tag.title == tag_title).first()
            for tag_title in _get_tag_titles_from_(post_schema.tags, db)
        ]
        if post_schema.tags
        else []
    )
