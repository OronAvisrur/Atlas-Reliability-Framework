from app.core.security import hash_password, verify_password, create_access_token, decode_access_token
from jose import JWTError


def register_user(conn, username: str, password: str) -> dict:
    cursor = conn.cursor()
    
    cursor.execute("SELECT id FROM users WHERE username = %s", (username,))
    if cursor.fetchone():
        cursor.close()
        raise ValueError("Username already exists")
    
    hashed_password = hash_password(password)
    cursor.execute(
        "INSERT INTO users (username, hashed_password) VALUES (%s, %s) RETURNING id, username, is_active",
        (username, hashed_password)
    )
    user = cursor.fetchone()
    cursor.close()
    
    return {"id": user[0], "username": user[1], "is_active": user[2]}


def authenticate_user(conn, username: str, password: str) -> dict:
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, username, hashed_password, is_active FROM users WHERE username = %s",
        (username,)
    )
    user = cursor.fetchone()
    cursor.close()
    
    if not user:
        raise ValueError("Invalid credentials")
    
    if not verify_password(password, user[2]):
        raise ValueError("Invalid credentials")
    
    if not user[3]:
        raise ValueError("User is inactive")
    
    return {"id": user[0], "username": user[1], "is_active": user[3]}


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