from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime


class ProfileDimension(BaseModel):
    knowledge_level: Optional[float] = Field(None, description="知识基础水平评分 0-10")
    cognitive_style: Optional[str] = Field(None, description="认知学习风格")
    knowledge_weakness: Optional[List[str]] = Field(default_factory=list, description="知识薄弱点")
    error_prone_points: Optional[List[str]] = Field(default_factory=list, description="易错点")
    learning_goals: Optional[str] = Field(None, description="学习目标")
    learning_pace: Optional[str] = Field(None, description="学习节奏偏好")
    interest_directions: Optional[List[str]] = Field(default_factory=list, description="兴趣方向")
    learning_behavior: Optional[str] = Field(None, description="学习行为习惯")


class ProfileDialogRequest(BaseModel):
    user_id: int = Field(..., description="用户ID")
    message: str = Field(..., description="用户对话消息")
    conversation_id: Optional[str] = Field(None, description="对话ID")


class ProfileDialogResponse(BaseModel):
    conversation_id: str = Field(..., description="对话ID")
    assistant_message: str = Field(..., description="助手回复")
    extracted_features: Optional[Dict[str, Any]] = Field(None, description="抽取的画像特征")


class ProfileUpdateRequest(BaseModel):
    user_id: int = Field(..., description="用户ID")
    dimensions: ProfileDimension = Field(..., description="画像维度数据")


class ProfileVisualizationData(BaseModel):
    user_id: int = Field(..., description="用户ID")
    radar_data: Dict[str, float] = Field(..., description="雷达图数据")
    heatmap_data: List[List[float]] = Field(..., description="热力图数据")
    dimension_details: ProfileDimension = Field(..., description="维度详情")
    updated_at: datetime = Field(..., description="更新时间")


class ProfileAgentInterface(BaseModel):
    agent_type: str = Field(..., description="智能体类型")
    user_id: int = Field(..., description="用户ID")
    input_data: Optional[Dict[str, Any]] = Field(None, description="输入数据")
    enable_agent: bool = Field(default=False, description="是否启用智能体")
