from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.comments import service
from app.comments.schemas import CommentCreate, CommentOut
from app.database import get_db
from app.deps import get_current_user
from app.models import Post, User

router = APIRouter(prefix="/posts/{post_id}/comments", tags=["comments"])


def ensure_post(db: Session, post_id: int) -> None:
    if db.get(Post, post_id) is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")


@router.post("", response_model=CommentOut, status_code=status.HTTP_201_CREATED)
def create_comment(post_id: int, data: CommentCreate, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    ensure_post(db, post_id)
    return service.create_comment(db, post_id, user.id, data)


@router.get("", response_model=list[CommentOut])
def list_comments(post_id: int, db: Session = Depends(get_db)):
    ensure_post(db, post_id)
    return service.list_comments(db, post_id)
