from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.sql import func
from app.core.database import Base


class CourseKnowledge(Base):
    __tablename__ = "course_knowledge"

    knowledge_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    course_id = Column(Integer, index=True, nullable=False)
    knowledge_name = Column(String(200), nullable=False)
    chapter_belong = Column(String(100), nullable=True)
    difficulty_level = Column(Integer, default=1)
    pre_knowledge = Column(Text, nullable=True)
    post_knowledge = Column(Text, nullable=True)
    knowledge_detail = Column(Text, nullable=True)
