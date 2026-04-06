from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.sql import func
from app.core.database import Base


class UserInfo(Base):
    __tablename__ = "user_info"

    user_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    major = Column(String(100), nullable=True)
    grade = Column(String(50), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    last_login_at = Column(DateTime(timezone=True), onupdate=func.now())
    status = Column(Integer, default=1)


class StudentProfile(Base):
    __tablename__ = "student_profile"

    profile_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, index=True, nullable=False)
    knowledge_level = Column(String(50), nullable=True)
    cognitive_style_tags = Column(Text, nullable=True)
    weakness_tags = Column(Text, nullable=True)
    error_prone_tags = Column(Text, nullable=True)
    learning_goals = Column(Text, nullable=True)
    learning_pace_preference = Column(String(50), nullable=True)
    interest_directions = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
