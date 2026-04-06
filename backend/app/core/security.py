from datetime import datetime, timedelta
from typing import Optional, List
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from sqlalchemy import and_

from app.core.config import settings
from app.core.database import get_db
from app.models.user import UserInfo as User
from app.models import SysRole, SysPermission, SysUserRole, SysRolePermission

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
security = HTTPBearer()


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
    return encoded_jwt


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="无法验证凭证",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        token = credentials.credentials
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    user = db.query(User).filter(User.user_id == int(user_id)).first()
    if user is None:
        raise credentials_exception
    if user.status != 1:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="账号已禁用"
        )
    return user


def get_user_roles(user_id: int, db: Session) -> List[SysRole]:
    return db.query(SysRole).join(
        SysUserRole, SysRole.role_id == SysUserRole.role_id
    ).filter(
        and_(SysUserRole.user_id == user_id, SysRole.status == 1)
    ).all()


def get_user_permissions(user_id: int, db: Session) -> List[SysPermission]:
    roles = get_user_roles(user_id, db)
    role_ids = [role.role_id for role in roles]
    
    permission_ids = []
    for role_id in role_ids:
        role_perms = db.query(SysRolePermission).filter(
            SysRolePermission.role_id == role_id
        ).all()
        permission_ids.extend([rp.permission_id for rp in role_perms])
    
    permissions = db.query(SysPermission).filter(
        and_(SysPermission.permission_id.in_(permission_ids), SysPermission.status == 1)
    ).all()
    return permissions


def has_permission(user_id: int, permission_code: str, db: Session) -> bool:
    permissions = get_user_permissions(user_id, db)
    permission_codes = [p.permission_code for p in permissions]
    
    if "super_admin" in [r.role_code for r in get_user_roles(user_id, db)]:
        return True
    
    return permission_code in permission_codes


def has_any_permission(user_id: int, permission_codes: List[str], db: Session) -> bool:
    for code in permission_codes:
        if has_permission(user_id, code, db):
            return True
    return False


def has_all_permissions(user_id: int, permission_codes: List[str], db: Session) -> bool:
    for code in permission_codes:
        if not has_permission(user_id, code, db):
            return False
    return True


def has_role(user_id: int, role_code: str, db: Session) -> bool:
    roles = get_user_roles(user_id, db)
    return any(r.role_code == role_code for r in roles)


def has_any_role(user_id: int, role_codes: List[str], db: Session) -> bool:
    roles = get_user_roles(user_id, db)
    user_role_codes = [r.role_code for r in roles]
    return any(rc in user_role_codes for rc in role_codes)

