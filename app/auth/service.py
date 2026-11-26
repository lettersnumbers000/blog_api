from sqlalchemy.orm import Session

from app.auth.schemas import UserCreate
from app.models import User
from app.security import hash_password, verify_password


def get_user_by_username(db: Session, username: str) -> User | None:
    return db.query(User).filter(User.username == username).first()


def create_user(db: Session, data: UserCreate) -> User:
    role = "admin" if db.query(User).count() == 0 else "user"
    user = User(username=data.username, hashed_password=hash_password(data.password), role=role)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def authenticate(db: Session, username: str, password: str) -> User | None:
    user = get_user_by_username(db, username)
    if user is None or not verify_password(password, user.hashed_password):
        return None
    return user
