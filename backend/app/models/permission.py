from sqlalchemy import Column, Integer, String, Text, BigInteger, DateTime
from sqlalchemy.dialects.mysql import TINYINT
from sqlalchemy.sql import func
from app.core.database import Base


class SysRole(Base):
    __tablename__ = "sys_role"
    
    role_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    role_name = Column(String(50), nullable=False)
    role_code = Column(String(50), nullable=False, unique=True, index=True)
    role_type = Column(String(20), nullable=False, default="custom")
    role_desc = Column(String(255))
    sort_order = Column(Integer, default=0)
    status = Column(TINYINT, default=1, index=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())


class SysPermission(Base):
    __tablename__ = "sys_permission"
    
    permission_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    permission_name = Column(String(50), nullable=False)
    permission_code = Column(String(100), nullable=False, unique=True, index=True)
    permission_type = Column(String(20), nullable=False, index=True)
    parent_id = Column(Integer, default=0, index=True)
    route_path = Column(String(200))
    component_path = Column(String(200))
    icon = Column(String(50))
    sort_order = Column(Integer, default=0)
    status = Column(TINYINT, default=1)
    created_at = Column(DateTime, server_default=func.now())


class SysUserRole(Base):
    __tablename__ = "sys_user_role"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, nullable=False, index=True)
    role_id = Column(Integer, nullable=False, index=True)
    created_at = Column(DateTime, server_default=func.now())


class SysRolePermission(Base):
    __tablename__ = "sys_role_permission"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    role_id = Column(Integer, nullable=False, index=True)
    permission_id = Column(Integer, nullable=False, index=True)
    created_at = Column(DateTime, server_default=func.now())


class SysOperationLog(Base):
    __tablename__ = "sys_operation_log"
    
    log_id = Column(BigInteger, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, index=True)
    role_code = Column(String(50))
    module = Column(String(50), index=True)
    operation_type = Column(String(20))
    request_url = Column(String(255))
    request_method = Column(String(10))
    request_params = Column(Text)
    response_result = Column(Text)
    operation_ip = Column(String(50))
    operation_time = Column(DateTime, server_default=func.now(), index=True)
    duration = Column(Integer)
    status = Column(TINYINT, default=1)
    error_msg = Column(Text)
