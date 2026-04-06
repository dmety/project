from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class RoleBase(BaseModel):
    role_name: str = Field(..., max_length=50, description="角色名称")
    role_code: str = Field(..., max_length=50, description="角色标识")
    role_type: str = Field(default="custom", max_length=20, description="角色类型")
    role_desc: Optional[str] = Field(None, max_length=255, description="角色描述")
    sort_order: int = Field(default=0, description="排序")
    status: int = Field(default=1, description="状态")


class RoleCreate(RoleBase):
    pass


class RoleUpdate(RoleBase):
    role_name: Optional[str] = None
    role_code: Optional[str] = None


class Role(RoleBase):
    role_id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class PermissionBase(BaseModel):
    permission_name: str = Field(..., max_length=50, description="权限名称")
    permission_code: str = Field(..., max_length=100, description="权限标识")
    permission_type: str = Field(..., max_length=20, description="权限类型")
    parent_id: int = Field(default=0, description="父级ID")
    route_path: Optional[str] = Field(None, max_length=200, description="路由地址")
    component_path: Optional[str] = Field(None, max_length=200, description="组件路径")
    icon: Optional[str] = Field(None, max_length=50, description="图标")
    sort_order: int = Field(default=0, description="排序")
    status: int = Field(default=1, description="状态")


class PermissionCreate(PermissionBase):
    pass


class PermissionUpdate(PermissionBase):
    permission_name: Optional[str] = None
    permission_code: Optional[str] = None


class Permission(PermissionBase):
    permission_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True


class UserRoleCreate(BaseModel):
    user_id: int
    role_id: int


class UserRole(BaseModel):
    id: int
    user_id: int
    role_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True


class RolePermissionCreate(BaseModel):
    role_id: int
    permission_id: int


class RolePermission(BaseModel):
    id: int
    role_id: int
    permission_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True


class OperationLogBase(BaseModel):
    user_id: Optional[int] = None
    role_code: Optional[str] = Field(None, max_length=50, description="角色标识")
    module: Optional[str] = Field(None, max_length=50, description="操作模块")
    operation_type: Optional[str] = Field(None, max_length=20, description="操作类型")
    request_url: Optional[str] = Field(None, max_length=255, description="请求地址")
    request_method: Optional[str] = Field(None, max_length=10, description="请求方法")
    request_params: Optional[str] = None
    response_result: Optional[str] = None
    operation_ip: Optional[str] = Field(None, max_length=50, description="操作IP")
    duration: Optional[int] = None
    status: int = Field(default=1, description="状态")
    error_msg: Optional[str] = None


class OperationLogCreate(OperationLogBase):
    pass


class OperationLog(OperationLogBase):
    log_id: int
    operation_time: datetime
    
    class Config:
        from_attributes = True


class UserRoleUpdate(BaseModel):
    role_ids: List[int]


class RolePermissionUpdate(BaseModel):
    permission_ids: List[int]


class LoginRequest(BaseModel):
    username: str
    password: str


class LoginResponse(BaseModel):
    token: str
    user_id: int
    username: str
    roles: List[str]
    permissions: List[str]
