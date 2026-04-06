from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime


class EvaluationDataRequest(BaseModel):
    user_id: int = Field(..., description="用户ID")
    evaluation_period: str = Field(..., description="评估周期")


class KnowledgeMasteryItem(BaseModel):
    knowledge_id: int = Field(..., description="知识点ID")
    mastery_level: float = Field(..., description="掌握度 0-10")


class LearningEvaluationResponse(BaseModel):
    evaluation_id: int = Field(..., description="评估ID")
    user_id: int = Field(..., description="用户ID")
    evaluation_period: str = Field(..., description="评估周期")
    knowledge_mastery: float = Field(..., description="知识点掌握度")
    answer_accuracy: float = Field(..., description="答题正确率")
    learning_progress_completion: float = Field(..., description="学习进度完成率")
    ability_improvement: float = Field(..., description="能力提升幅度")
    knowledge_gaps: List[str] = Field(default_factory=list, description="知识漏洞标签")
    evaluation_report: str = Field(..., description="评估报告")
    generated_at: datetime = Field(..., description="生成时间")

    class Config:
        from_attributes = True


class EvaluationDashboardData(BaseModel):
    user_id: int = Field(..., description="用户ID")
    knowledge_mastery_trend: List[Dict[str, Any]] = Field(..., description="知识点掌握度趋势")
    answer_accuracy_trend: List[Dict[str, Any]] = Field(..., description="答题正确率趋势")
    progress_completion_trend: List[Dict[str, Any]] = Field(..., description="学习进度完成率趋势")
    ability_improvement_trend: List[Dict[str, Any]] = Field(..., description="能力提升趋势")
    recent_evaluations: List[LearningEvaluationResponse] = Field(default_factory=list, description="最近评估")
    knowledge_gaps: List[str] = Field(default_factory=list, description="知识漏洞")


class EvaluationAgentInterface(BaseModel):
    agent_type: str = Field(..., description="智能体类型")
    user_id: int = Field(..., description="用户ID")
    evaluation_period: Optional[str] = Field(None, description="评估周期")
    input_data: Optional[Dict[str, Any]] = Field(None, description="输入数据")
    enable_agent: bool = Field(default=False, description="是否启用智能体")


class ContentSafetyCheckRequest(BaseModel):
    content: str = Field(..., description="待检查内容")
    content_type: str = Field(default="text", description="内容类型")
    check_type: str = Field(default="all", description="检查类型")


class ContentSafetyCheckResponse(BaseModel):
    is_safe: bool = Field(..., description="是否安全")
    risk_level: str = Field(..., description="风险等级")
    risk_types: List[str] = Field(default_factory=list, description="风险类型")
    suggestion: str = Field(..., description="建议")
    check_result: Dict[str, Any] = Field(default_factory=dict, description="详细检查结果")


class RAGRetrievalRequest(BaseModel):
    query: str = Field(..., description="查询内容")
    top_k: int = Field(default=5, description="返回数量")
    knowledge_ids: Optional[List[int]] = Field(None, description="限定知识点")


class RAGRetrievalItem(BaseModel):
    knowledge_id: int = Field(..., description="知识点ID")
    content: str = Field(..., description="内容")
    similarity: float = Field(..., description="相似度")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="元数据")


class SafetyAgentInterface(BaseModel):
    agent_type: str = Field(..., description="智能体类型")
    content: str = Field(..., description="待检查内容")
    input_data: Optional[Dict[str, Any]] = Field(None, description="输入数据")
    enable_agent: bool = Field(default=False, description="是否启用智能体")
