from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.schemas.user import UserCreate, Token, UserResponse
from app.db.deps import get_db
from app.core.exceptions import AppException
from app.services.authservices import register_user, login_user, validate_user
from app.schemas.response import ResponseModel

router = APIRouter()


@router.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):
    if validate_user(db, user.email):
        raise AppException("User already exists", 400)
    
    created_user = register_user(db, user.email, user.password)

    return ResponseModel(
        success=True,
        message="User created",
        data=UserResponse.model_validate(created_user)
    )


@router.post("/login", response_model=ResponseModel)
def login(user: UserCreate, db: Session = Depends(get_db)):
    token = login_user(db, user.email, user.password)

    if not token:
        raise AppException("Invalid credentials", 401)
    
    token_data = {"access_token": token, "token_type": "bearer"}
    return ResponseModel(
        success=True,
        message="Login successful",
        data=Token(**token_data) 
    )