from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime


class TutorDialogRequest(BaseModel):
    user_id: int = Field(..., description="用户ID")
    question: str = Field(..., description="用户问题")
    question_type: Optional[str] = Field(None, description="问题类型")
    code_content: Optional[str] = Field(None, description="代码内容")
    image_url: Optional[str] = Field(None, description="图片URL")
    conversation_id: Optional[str] = Field(None, description="对话ID")
    enable_agent: bool = Field(default=False, description="是否启用智能体")


class TutorDialogResponse(BaseModel):
    conversation_id: str = Field(..., description="对话ID")
    answer: str = Field(..., description="回答内容")
    answer_type: str = Field(..., description="回答类型")
    code_suggestion: Optional[str] = Field(None, description="代码建议")
    diagram_url: Optional[str] = Field(None, description="图解URL")
    related_exercises: Optional[List[int]] = Field(default_factory=list, description="相关题目")


class CodeRunRequest(BaseModel):
    user_id: int = Field(..., description="用户ID")
    code_content: str = Field(..., description="代码内容")
    language: str = Field(default="python", description="编程语言")


class CodeRunResponse(BaseModel):
    success: bool = Field(..., description="是否成功")
    output: str = Field(..., description="执行输出")
    errors: Optional[str] = Field(None, description="错误信息")
    execution_time: float = Field(..., description="执行时间（秒）")


class ErrorAnalysisRequest(BaseModel):
    user_id: int = Field(..., description="用户ID")
    exercise_id: int = Field(..., description="题目ID")
    user_answer: str = Field(..., description="用户答案")


class ErrorAnalysisResponse(BaseModel):
    error_type: str = Field(..., description="错误类型")
    knowledge_point: str = Field(..., description="知识点")
    correct_answer: str = Field(..., description="正确答案")
    explanation: str = Field(..., description="解析")
    similar_exercises: Optional[List[int]] = Field(default_factory=list, description="类似题目")


class TutorAgentInterface(BaseModel):
    agent_type: str = Field(..., description="智能体类型")
    user_id: int = Field(..., description="用户ID")
    input_data: Optional[Dict[str, Any]] = Field(None, description="输入数据")
    enable_agent: bool = Field(default=False, description="是否启用智能体")
