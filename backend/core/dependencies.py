from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer

from backend.db.database import get_connection
from backend.services.auth_service import verify_token

security = HTTPBearer()


def get_current_user(token: str = Depends(security)) -> dict:
    try:
        username = verify_token(token.credentials)
        
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id, username, is_active FROM users WHERE username = %s",
            (username,)
        )
        user = cursor.fetchone()
        cursor.close()
        conn.close()
        
        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
        
        if not user[2]:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Inactive user")
        
        return {"id": user[0], "username": user[1], "is_active": user[2]}
    except ValueError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")