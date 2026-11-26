from sqlalchemy.orm import Session

from app.models import Post
from app.posts.schemas import PostCreate


def create_post(db: Session, data: PostCreate, author_id: int) -> Post:
    post = Post(title=data.title, content=data.content, author_id=author_id)
    db.add(post)
    db.commit()
    db.refresh(post)
    return post


def list_posts(db: Session) -> list[Post]:
    return db.query(Post).order_by(Post.id.desc()).all()


def get_post(db: Session, post_id: int) -> Post | None:
    return db.get(Post, post_id)


def delete_post(db: Session, post: Post) -> None:
    db.delete(post)
    db.commit()
