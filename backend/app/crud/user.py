from sqlalchemy.orm import Session
from app.models.user import UserInfo
from app.schemas.user import UserCreate
from app.core.security import get_password_hash


def get_user_by_username(db: Session, username: str):
    return db.query(UserInfo).filter(UserInfo.username == username).first()


def get_user_by_id(db: Session, user_id: int):
    return db.query(UserInfo).filter(UserInfo.user_id == user_id).first()


def create_user(db: Session, user: UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = UserInfo(
        username=user.username,
        password_hash=hashed_password,
        major=user.major,
        grade=user.grade
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
