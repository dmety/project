from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime, timedelta
from jose import JWTError, jwt
import bcrypt
from sqlalchemy import and_

from app.core.database import get_db
from app.models import (
    SysRole, SysPermission, SysUserRole, SysRolePermission, SysOperationLog, UserInfo
)
from app.schemas.permission import (
    Role, RoleCreate, RoleUpdate,
    Permission, PermissionCreate, PermissionUpdate,
    UserRole, UserRoleCreate, UserRoleUpdate,
    RolePermission, RolePermissionCreate, RolePermissionUpdate,
    OperationLog, OperationLogCreate,
    LoginRequest, LoginResponse
)
from app.core.config import settings
from app.core.response import success_response, ApiResponse

router = APIRouter(prefix="/v1/permission", tags=["权限管理"])

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
    return encoded_jwt

@router.post("/login", response_model=ApiResponse[LoginResponse])
def login(request: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(UserInfo).filter(UserInfo.username == request.username).first()
    if not user or not verify_password(request.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户名或密码错误"
        )
    
    if user.status != 1:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="账号已禁用"
        )
    
    roles = db.query(SysRole).join(
        SysUserRole, SysRole.role_id == SysUserRole.role_id
    ).filter(
        and_(SysUserRole.user_id == user.user_id, SysRole.status == 1)
    ).all()
    
    role_codes = [role.role_code for role in roles]
    
    permission_ids = []
    for role in roles:
        role_perms = db.query(SysRolePermission).filter(
            SysRolePermission.role_id == role.role_id
        ).all()
        permission_ids.extend([rp.permission_id for rp in role_perms])
    
    permissions = db.query(SysPermission).filter(
        and_(SysPermission.permission_id.in_(permission_ids), SysPermission.status == 1)
    ).all()
    permission_codes = [perm.permission_code for perm in permissions]
    
    access_token_expires = timedelta(minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(user.user_id), "username": user.username},
        expires_delta=access_token_expires
    )
    
    login_data = LoginResponse(
        token=access_token,
        user_id=user.user_id,
        username=user.username,
        roles=role_codes,
        permissions=permission_codes
    )
    
    return success_response(data=login_data, message="登录成功")

@router.get("/roles", response_model=List[Role])
def get_roles(
    status: Optional[int] = None,
    db: Session = Depends(get_db)
):
    query = db.query(SysRole)
    if status is not None:
        query = query.filter(SysRole.status == status)
    return query.order_by(SysRole.sort_order).all()

@router.post("/roles", response_model=Role)
def create_role(role: RoleCreate, db: Session = Depends(get_db)):
    db_role = SysRole(**role.model_dump())
    db.add(db_role)
    db.commit()
    db.refresh(db_role)
    return db_role

@router.put("/roles/{role_id}", response_model=Role)
def update_role(role_id: int, role: RoleUpdate, db: Session = Depends(get_db)):
    db_role = db.query(SysRole).filter(SysRole.role_id == role_id).first()
    if not db_role:
        raise HTTPException(status_code=404, detail="角色不存在")
    
    update_data = role.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_role, key, value)
    
    db.commit()
    db.refresh(db_role)
    return db_role

@router.get("/permissions", response_model=List[Permission])
def get_permissions(
    permission_type: Optional[str] = None,
    status: Optional[int] = None,
    db: Session = Depends(get_db)
):
    query = db.query(SysPermission)
    if permission_type:
        query = query.filter(SysPermission.permission_type == permission_type)
    if status is not None:
        query = query.filter(SysPermission.status == status)
    return query.order_by(SysPermission.sort_order).all()

@router.post("/permissions", response_model=Permission)
def create_permission(permission: PermissionCreate, db: Session = Depends(get_db)):
    db_perm = SysPermission(**permission.model_dump())
    db.add(db_perm)
    db.commit()
    db.refresh(db_perm)
    return db_perm

@router.put("/permissions/{permission_id}", response_model=Permission)
def update_permission(permission_id: int, permission: PermissionUpdate, db: Session = Depends(get_db)):
    db_perm = db.query(SysPermission).filter(SysPermission.permission_id == permission_id).first()
    if not db_perm:
        raise HTTPException(status_code=404, detail="权限不存在")
    
    update_data = permission.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_perm, key, value)
    
    db.commit()
    db.refresh(db_perm)
    return db_perm

@router.post("/user/{user_id}/roles")
def assign_user_roles(user_id: int, request: UserRoleUpdate, db: Session = Depends(get_db)):
    db.query(SysUserRole).filter(SysUserRole.user_id == user_id).delete()
    
    for role_id in request.role_ids:
        user_role = SysUserRole(user_id=user_id, role_id=role_id)
        db.add(user_role)
    
    db.commit()
    return {"message": "角色分配成功"}

@router.get("/user/{user_id}/roles", response_model=List[Role])
def get_user_roles(user_id: int, db: Session = Depends(get_db)):
    return db.query(SysRole).join(
        SysUserRole, SysRole.role_id == SysUserRole.role_id
    ).filter(SysUserRole.user_id == user_id).all()

@router.post("/role/{role_id}/permissions")
def assign_role_permissions(role_id: int, request: RolePermissionUpdate, db: Session = Depends(get_db)):
    db.query(SysRolePermission).filter(SysRolePermission.role_id == role_id).delete()
    
    for permission_id in request.permission_ids:
        role_perm = SysRolePermission(role_id=role_id, permission_id=permission_id)
        db.add(role_perm)
    
    db.commit()
    return {"message": "权限分配成功"}

@router.get("/role/{role_id}/permissions", response_model=List[Permission])
def get_role_permissions(role_id: int, db: Session = Depends(get_db)):
    return db.query(SysPermission).join(
        SysRolePermission, SysPermission.permission_id == SysRolePermission.permission_id
    ).filter(SysRolePermission.role_id == role_id).all()

@router.get("/logs", response_model=List[OperationLog])
def get_operation_logs(
    user_id: Optional[int] = None,
    module: Optional[str] = None,
    status: Optional[int] = None,
    limit: int = Query(100, le=1000),
    db: Session = Depends(get_db)
):
    query = db.query(SysOperationLog)
    if user_id:
        query = query.filter(SysOperationLog.user_id == user_id)
    if module:
        query = query.filter(SysOperationLog.module == module)
    if status is not None:
        query = query.filter(SysOperationLog.status == status)
    return query.order_by(SysOperationLog.operation_time.desc()).limit(limit).all()
