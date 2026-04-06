from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import timedelta

from app.core.database import get_db
from app.core.response import ApiResponse, success_response
from app.core.security import verify_password, create_access_token
from app.core.config import settings
from app.crud.user import get_user_by_username, create_user
from app.schemas.user import UserCreate, UserLogin, UserResponse, LoginResponse

router = APIRouter(prefix="/auth", tags=["认证"])


@router.post("/register", response_model=ApiResponse[UserResponse])
def register(user: UserCreate, db: Session = Depends(get_db)):
    db_user = get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="用户名已存在"
        )
    new_user = create_user(db=db, user=user)
    return success_response(data=UserResponse.model_validate(new_user))


@router.post("/login", response_model=ApiResponse[LoginResponse])
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = get_user_by_username(db, username=user.username)
    if not db_user or not verify_password(user.password, db_user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户名或密码错误"
        )
    access_token = create_access_token(
        data={"sub": db_user.username},
        expires_delta=timedelta(minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    return success_response(
        data=LoginResponse(
            token=access_token,
            user_info=UserResponse.model_validate(db_user)
        )
    )
