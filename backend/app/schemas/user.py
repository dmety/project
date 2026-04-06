from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class UserBase(BaseModel):
    username: str = Field(..., description="用户名")
    major: Optional[str] = Field(None, description="专业")
    grade: Optional[str] = Field(None, description="年级")


class UserCreate(UserBase):
    password: str = Field(..., description="密码")


class UserLogin(BaseModel):
    username: str = Field(..., description="用户名")
    password: str = Field(..., description="密码")


class UserResponse(UserBase):
    user_id: int = Field(..., description="用户ID")
    created_at: datetime = Field(..., description="注册时间")
    last_login_at: Optional[datetime] = Field(None, description="最后登录时间")
    status: int = Field(..., description="状态")

    class Config:
        from_attributes = True


class LoginResponse(BaseModel):
    token: str = Field(..., description="访问令牌")
    user_info: UserResponse = Field(..., description="用户信息")


class StudentProfileBase(BaseModel):
    user_id: int = Field(..., description="用户ID")
    knowledge_level: Optional[str] = Field(None, description="知识基础等级")
    cognitive_style_tags: Optional[str] = Field(None, description="认知风格标签")
    weakness_tags: Optional[str] = Field(None, description="薄弱点标签")
    error_prone_tags: Optional[str] = Field(None, description="易错点标签")
    learning_goals: Optional[str] = Field(None, description="学习目标")
    learning_pace_preference: Optional[str] = Field(None, description="学习节奏偏好")
    interest_directions: Optional[str] = Field(None, description="兴趣方向")


class StudentProfileCreate(StudentProfileBase):
    pass


class StudentProfileUpdate(StudentProfileBase):
    pass


class StudentProfileResponse(StudentProfileBase):
    profile_id: int = Field(..., description="画像ID")
    created_at: datetime = Field(..., description="创建时间")
    updated_at: Optional[datetime] = Field(None, description="更新时间")

    class Config:
        from_attributes = True
