from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum


class ResourceType(str, Enum):
    COURSE_DOC = "course_doc"
    MIND_MAP = "mind_map"
    EXERCISE = "exercise"
    CODE_CASE = "code_case"
    EXTENSION_READING = "extension_reading"
    MULTIMODAL_DIAGRAM = "multimodal_diagram"


class DifficultyLevel(str, Enum):
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"


class ResourceGenerateRequest(BaseModel):
    user_id: int = Field(..., description="用户ID")
    knowledge_id: int = Field(..., description="知识点ID")
    resource_type: ResourceType = Field(..., description="资源类型")
    difficulty: DifficultyLevel = Field(default=DifficultyLevel.MEDIUM, description="难度等级")
    enable_agent: bool = Field(default=False, description="是否启用智能体")


class ResourceResponse(BaseModel):
    resource_id: int = Field(..., description="资源ID")
    user_id: int = Field(..., description="用户ID")
    knowledge_id: int = Field(..., description="知识点ID")
    resource_type: str = Field(..., description="资源类型")
    resource_content: str = Field(..., description="资源内容")
    generated_at: datetime = Field(..., description="生成时间")
    usage_status: int = Field(..., description="使用状态")
    is_compliant: bool = Field(..., description="是否合规")

    class Config:
        from_attributes = True


class ResourceListRequest(BaseModel):
    user_id: int = Field(..., description="用户ID")
    knowledge_id: Optional[int] = Field(None, description="知识点ID")
    resource_type: Optional[str] = Field(None, description="资源类型")
    page: int = Field(default=1, description="页码")
    page_size: int = Field(default=10, description="每页数量")


class ResourceListResponse(BaseModel):
    total: int = Field(..., description="总数")
    page: int = Field(..., description="页码")
    page_size: int = Field(..., description="每页数量")
    resources: List[ResourceResponse] = Field(..., description="资源列表")


class ResourceFeedbackRequest(BaseModel):
    resource_id: int = Field(..., description="资源ID")
    user_id: int = Field(..., description="用户ID")
    rating: int = Field(..., description="评分 1-5")
    feedback: Optional[str] = Field(None, description="反馈内容")


class ResourceAgentInterface(BaseModel):
    agent_type: str = Field(..., description="智能体类型")
    user_id: int = Field(..., description="用户ID")
    knowledge_id: int = Field(..., description="知识点ID")
    resource_type: str = Field(..., description="资源类型")
    input_data: Optional[Dict[str, Any]] = Field(None, description="输入数据")
    enable_agent: bool = Field(default=False, description="是否启用智能体")


class GenerateProgressResponse(BaseModel):
    progress: float = Field(..., description="进度 0-100")
    status: str = Field(..., description="状态")
    message: str = Field(..., description="消息")
