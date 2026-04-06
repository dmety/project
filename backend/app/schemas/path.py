from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime


class PathNodeBase(BaseModel):
    knowledge_id: int = Field(..., description="知识点ID")
    learning_order: int = Field(..., description="学习顺序")
    milestone_flag: bool = Field(default=False, description="里程碑标记")
    learning_content: Optional[str] = Field(None, description="学习内容")
    completion_status: int = Field(default=0, description="完成状态 0-未完成 1-已完成")
    plan_completion_time: Optional[datetime] = Field(None, description="计划完成时间")


class PathNodeCreate(PathNodeBase):
    pass


class PathNodeResponse(PathNodeBase):
    node_id: int = Field(..., description="节点ID")
    path_id: int = Field(..., description="路径ID")
    actual_completion_time: Optional[datetime] = Field(None, description="实际完成时间")

    class Config:
        from_attributes = True


class LearningPathBase(BaseModel):
    user_id: int = Field(..., description="用户ID")
    path_name: str = Field(..., description="路径名称")
    learning_cycle: Optional[int] = Field(None, description="学习周期（天）")


class LearningPathCreate(LearningPathBase):
    nodes: List[PathNodeCreate] = Field(..., description="路径节点列表")


class LearningPathUpdate(LearningPathBase):
    pass


class LearningPathResponse(LearningPathBase):
    path_id: int = Field(..., description="路径ID")
    total_milestones: int = Field(default=0, description="总里程碑数")
    completed_milestones: int = Field(default=0, description="已完成里程碑数")
    current_progress: float = Field(default=0.0, description="当前进度 0-100")
    status: int = Field(default=0, description="状态 0-进行中 1-已完成")
    created_at: datetime = Field(..., description="创建时间")
    updated_at: Optional[datetime] = Field(None, description="更新时间")
    nodes: List[PathNodeResponse] = Field(default_factory=list, description="路径节点")

    class Config:
        from_attributes = True


class PathGenerateRequest(BaseModel):
    user_id: int = Field(..., description="用户ID")
    path_name: str = Field(..., description="路径名称")
    start_knowledge_id: Optional[int] = Field(None, description="起始知识点ID")
    target_knowledge_id: Optional[int] = Field(None, description="目标知识点ID")
    enable_agent: bool = Field(default=False, description="是否启用智能体")


class PathNodeUpdateRequest(BaseModel):
    node_id: int = Field(..., description="节点ID")
    completion_status: Optional[int] = Field(None, description="完成状态")
    learning_content: Optional[str] = Field(None, description="学习内容")
    actual_completion_time: Optional[datetime] = Field(None, description="实际完成时间")


class ResourcePushRequest(BaseModel):
    user_id: int = Field(..., description="用户ID")
    path_id: Optional[int] = Field(None, description="路径ID")
    node_id: Optional[int] = Field(None, description="节点ID")
    knowledge_id: Optional[int] = Field(None, description="知识点ID")


class ResourcePushItem(BaseModel):
    resource_id: int = Field(..., description="资源ID")
    knowledge_id: int = Field(..., description="知识点ID")
    resource_type: str = Field(..., description="资源类型")
    read_status: int = Field(default=0, description="阅读状态 0-未读 1-已读")


class PathAgentInterface(BaseModel):
    agent_type: str = Field(..., description="智能体类型")
    user_id: int = Field(..., description="用户ID")
    path_id: Optional[int] = Field(None, description="路径ID")
    input_data: Optional[Dict[str, Any]] = Field(None, description="输入数据")
    enable_agent: bool = Field(default=False, description="是否启用智能体")
