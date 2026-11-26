from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.auth import service
from app.auth.schemas import Token, UserCreate, UserOut
from app.database import get_db
from app.deps import get_current_user, require_role
from app.limiter import limiter
from app.models import User
from app.security import create_access_token

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def register(data: UserCreate, db: Session = Depends(get_db)):
    if service.get_user_by_username(db, data.username):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already exists")
    return service.create_user(db, data)


@router.post("/login", response_model=Token)
@limiter.limit("5/minute")
def login(request: Request, form: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = service.authenticate(db, form.username, form.password)
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")
    return Token(access_token=create_access_token(user.username), token_type="bearer")


@router.get("/me", response_model=UserOut)
def me(user: User = Depends(get_current_user)):
    return user


@router.get("/users", response_model=list[UserOut])
def list_users(db: Session = Depends(get_db), _: User = Depends(require_role("admin"))):
    return db.query(User).all()
