from jose import jwt, JWTError
from datetime import datetime, timedelta
from fastapi import Depends
from fastapi.security import HTTPBearer, HTTPAuthCredentials
from app.core.config import settings
from app.core.exceptions import AppException

security = HTTPBearer()

# -------- JWT --------
def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    return jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )

def decode_token(token: str):
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )
        return payload
    except jwt.ExpiredSignatureError:
        raise AppException("Token has expired", 401)
    except JWTError:
        raise AppException("Invalid token", 401)

# -------- AUTH DEPENDENCY --------
async def get_current_user(credentials: HTTPAuthCredentials = Depends(security)) -> int:
    """
    Extract and validate JWT token, return user_id
    
    Token should contain either:
    - 'user_id' claim (preferred)
    - 'sub' claim with user_id value
    
    Returns:
        int: user_id
    """
    token = credentials.credentials
    payload = decode_token(token)
    
    # Try to get user_id from token
    user_id = payload.get("user_id") or payload.get("sub")
    
    if not user_id:
        raise AppException("Invalid token - missing user_id", 401)
    
    # Convert to int if it's a string
    try:
        user_id = int(user_id)
    except (ValueError, TypeError):
        raise AppException("Invalid user_id format", 401)
    
    return user_id

