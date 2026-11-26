from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.deps import get_current_user, require_role
from app.models import User
from app.posts import service
from app.posts.schemas import PostCreate, PostOut
from app.tasks import notify_post_created

router = APIRouter(prefix="/posts", tags=["posts"])


@router.post("", response_model=PostOut, status_code=status.HTTP_201_CREATED)
def create_post(data: PostCreate, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    post = service.create_post(db, data, user.id)
    notify_post_created.delay(post.id, user.username)
    return post


@router.get("", response_model=list[PostOut])
def list_posts(db: Session = Depends(get_db)):
    return service.list_posts(db)


@router.get("/{post_id}", response_model=PostOut)
def get_post(post_id: int, db: Session = Depends(get_db)):
    post = service.get_post(db, post_id)
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    return post


@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(post_id: int, db: Session = Depends(get_db), _: User = Depends(require_role("admin"))):
    post = service.get_post(db, post_id)
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    service.delete_post(db, post)
