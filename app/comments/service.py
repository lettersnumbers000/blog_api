from sqlalchemy.orm import Session

from app.comments.schemas import CommentCreate
from app.models import Comment


def create_comment(db: Session, post_id: int, author_id: int, data: CommentCreate) -> Comment:
    comment = Comment(text=data.text, post_id=post_id, author_id=author_id)
    db.add(comment)
    db.commit()
    db.refresh(comment)
    return comment


def list_comments(db: Session, post_id: int) -> list[Comment]:
    return db.query(Comment).filter(Comment.post_id == post_id).order_by(Comment.id).all()
