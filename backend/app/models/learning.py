from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, Float
from sqlalchemy.sql import func
from app.core.database import Base


class LearningPath(Base):
    __tablename__ = "learning_path"

    path_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, index=True, nullable=False)
    path_name = Column(String(200), nullable=False)
    learning_cycle = Column(String(50), nullable=True)
    total_milestones = Column(Integer, default=0)
    completed_milestones = Column(Integer, default=0)
    current_progress = Column(Float, default=0.0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    status = Column(Integer, default=1)


class PathNode(Base):
    __tablename__ = "path_node"

    node_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    path_id = Column(Integer, index=True, nullable=False)
    knowledge_id = Column(Integer, nullable=False)
    learning_order = Column(Integer, nullable=False)
    is_milestone = Column(Boolean, default=False)
    learning_content = Column(Text, nullable=True)
    completion_status = Column(Integer, default=0)
    planned_completion_time = Column(DateTime(timezone=True), nullable=True)
    actual_completion_time = Column(DateTime(timezone=True), nullable=True)


class LearningResource(Base):
    __tablename__ = "learning_resource"

    resource_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, index=True, nullable=False)
    knowledge_id = Column(Integer, index=True, nullable=False)
    resource_type = Column(String(50), nullable=False)
    resource_content = Column(Text, nullable=False)
    generated_at = Column(DateTime(timezone=True), server_default=func.now())
    usage_status = Column(Integer, default=0)
    user_feedback = Column(Text, nullable=True)
    is_compliant = Column(Boolean, default=True)


class LearningBehavior(Base):
    __tablename__ = "learning_behavior"

    behavior_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, index=True, nullable=False)
    resource_id = Column(Integer, index=True, nullable=True)
    behavior_type = Column(String(50), nullable=False)
    behavior_duration = Column(Integer, nullable=True)
    operation_time = Column(DateTime(timezone=True), server_default=func.now())
    page_stay_duration = Column(Integer, nullable=True)
    interaction_details = Column(Text, nullable=True)


class ExerciseInfo(Base):
    __tablename__ = "exercise_info"

    exercise_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    knowledge_id = Column(Integer, index=True, nullable=False)
    difficulty_level = Column(Integer, default=1)
    exercise_type = Column(String(50), nullable=False)
    exercise_content = Column(Text, nullable=False)
    answer = Column(Text, nullable=False)
    explanation = Column(Text, nullable=True)
    error_prone_tags = Column(Text, nullable=True)


class UserExerciseRecord(Base):
    __tablename__ = "user_exercise_record"

    record_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, index=True, nullable=False)
    exercise_id = Column(Integer, index=True, nullable=False)
    user_answer = Column(Text, nullable=False)
    is_correct = Column(Boolean, default=False)
    answer_duration = Column(Integer, nullable=True)
    answer_time = Column(DateTime(timezone=True), server_default=func.now())
    is_error = Column(Boolean, default=False)
    explanation_viewed = Column(Boolean, default=False)


class LearningEvaluation(Base):
    __tablename__ = "learning_evaluation"

    evaluation_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, index=True, nullable=False)
    evaluation_period = Column(String(50), nullable=False)
    knowledge_mastery = Column(Float, nullable=True)
    answer_accuracy = Column(Float, nullable=True)
    learning_progress_completion = Column(Float, nullable=True)
    ability_improvement = Column(Float, nullable=True)
    knowledge_gaps_tags = Column(Text, nullable=True)
    evaluation_report = Column(Text, nullable=True)
    generated_at = Column(DateTime(timezone=True), server_default=func.now())
