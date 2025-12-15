from fastapi import APIRouter, HTTPException, status

from app.db.database import get_db
from app.models.auth_schemas import UserRegister, UserLogin, Token, UserResponse
from app.services.auth_service import register_user, authenticate_user, generate_token

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(user_data: UserRegister):
    try:
        with get_db() as conn:
            user = register_user(conn, user_data.username, user_data.password)
        return user
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post("/login", response_model=Token)
def login(credentials: UserLogin):
    try:
        with get_db() as conn:
            user = authenticate_user(conn, credentials.username, credentials.password)
        token = generate_token(user["username"])
        return Token(access_token=token)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))