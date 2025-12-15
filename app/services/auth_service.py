from sqlalchemy.orm import Session
from jose import JWTError

from app.db.models import User
from app.core.security import hash_password, verify_password, create_access_token, decode_access_token


def register_user(db: Session, username: str, password: str) -> User:
    existing_user = db.query(User).filter(User.username == username).first()
    if existing_user:
        raise ValueError("Username already exists")
    
    hashed_password = hash_password(password)
    user = User(username=username, hashed_password=hashed_password)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def authenticate_user(db: Session, username: str, password: str) -> User:
    user = db.query(User).filter(User.username == username).first()
    if not user or not verify_password(password, user.hashed_password):
        raise ValueError("Invalid credentials")
    if not user.is_active:
        raise ValueError("User is inactive")
    return user


def generate_token(username: str) -> str:
    return create_access_token({"sub": username})


def verify_token(token: str) -> str:
    try:
        payload = decode_access_token(token)
        username = payload.get("sub")
        if not username:
            raise ValueError("Invalid token")
        return username
    except JWTError:
        raise ValueError("Invalid token")