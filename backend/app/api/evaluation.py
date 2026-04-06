from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import Dict, Any, List
from datetime import datetime, timedelta
import random

from app.core.database import get_db
from app.core.response import ApiResponse, success_response
from app.core.security import get_current_user
from app.models.learning import LearningEvaluation
from app.schemas.evaluation import (
    EvaluationDataRequest,
    LearningEvaluationResponse,
    EvaluationDashboardData,
    EvaluationAgentInterface,
    ContentSafetyCheckRequest,
    ContentSafetyCheckResponse,
    RAGRetrievalRequest,
    RAGRetrievalItem,
    SafetyAgentInterface
)
from app.services.xfyun_sdk.content_audit_sdk import ContentAuditSDK

router = APIRouter(prefix="/evaluation", tags=["学习评估与内容安全"])


def generate_trend_data(base_value: float, periods: int = 7) -> List[Dict[str, Any]]:
    trend = []
    for i in range(periods):
        date = (datetime.now() - timedelta(days=periods - 1 - i)).strftime("%Y-%m-%d")
        value = max(0, min(10, base_value + random.uniform(-1, 1)))
        trend.append({"date": date, "value": round(value, 2)})
    return trend


def generate_evaluation_report(user_id: int, period: str) -> str:
    report = f"""# 学习效果评估报告

## 用户ID: {user_id}
## 评估周期: {period}
## 生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

---

## 评估概述

本次评估基于您最近的学习行为数据、答题记录和资源使用情况进行综合分析。

### 主要发现

1. **知识点掌握度**: 整体表现良好，部分知识点需要加强
2. **答题正确率**: 处于中等偏上水平，建议多练习难题
3. **学习进度**: 按计划推进，建议保持当前节奏
4. **能力提升**: 与上期相比有明显进步

### 建议

1. 针对知识漏洞进行专项练习
2. 增加实践环节，提升动手能力
3. 定期复习已学知识点
4. 利用智能辅导功能解决疑问

---

*注：此为示例报告，实际使用时将通过智能体生成更精准的评估内容。*
"""
    return report


@router.post("/generate", response_model=ApiResponse[LearningEvaluationResponse])
def generate_evaluation(
    request: EvaluationDataRequest,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    knowledge_mastery = random.uniform(6, 9)
    answer_accuracy = random.uniform(65, 90)
    learning_progress_completion = random.uniform(50, 85)
    ability_improvement = random.uniform(5, 20)
    
    knowledge_gaps = ["知识点2", "知识点5", "知识点7"]
    
    evaluation = LearningEvaluation(
        user_id=request.user_id,
        evaluation_period=request.evaluation_period,
        knowledge_mastery=knowledge_mastery,
        answer_accuracy=answer_accuracy,
        learning_progress_completion=learning_progress_completion,
        ability_improvement=ability_improvement,
        knowledge_gaps_tags=",".join(knowledge_gaps),
        evaluation_report=generate_evaluation_report(request.user_id, request.evaluation_period)
    )
    
    db.add(evaluation)
    db.commit()
    db.refresh(evaluation)
    
    return success_response(
        data=LearningEvaluationResponse(
            evaluation_id=evaluation.evaluation_id,
            user_id=evaluation.user_id,
            evaluation_period=evaluation.evaluation_period,
            knowledge_mastery=evaluation.knowledge_mastery or 0,
            answer_accuracy=evaluation.answer_accuracy or 0,
            learning_progress_completion=evaluation.learning_progress_completion or 0,
            ability_improvement=evaluation.ability_improvement or 0,
            knowledge_gaps=knowledge_gaps,
            evaluation_report=evaluation.evaluation_report or "",
            generated_at=evaluation.generated_at
        )
    )


@router.get("/dashboard/{user_id}", response_model=ApiResponse[EvaluationDashboardData])
def get_evaluation_dashboard(
    user_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    recent_evaluations = db.query(LearningEvaluation)\
                           .filter(LearningEvaluation.user_id == user_id)\
                           .order_by(LearningEvaluation.generated_at.desc())\
                           .limit(5)\
                           .all()
    
    eval_responses = []
    for eval_item in recent_evaluations:
        eval_response = LearningEvaluationResponse(
            evaluation_id=eval_item.evaluation_id,
            user_id=eval_item.user_id,
            evaluation_period=eval_item.evaluation_period,
            knowledge_mastery=eval_item.knowledge_mastery or 0,
            answer_accuracy=eval_item.answer_accuracy or 0,
            learning_progress_completion=eval_item.learning_progress_completion or 0,
            ability_improvement=eval_item.ability_improvement or 0,
            knowledge_gaps=eval_item.knowledge_gaps_tags.split(",") if eval_item.knowledge_gaps_tags else [],
            evaluation_report=eval_item.evaluation_report or "",
            generated_at=eval_item.generated_at
        )
        eval_responses.append(eval_response)
    
    return success_response(
        data=EvaluationDashboardData(
            user_id=user_id,
            knowledge_mastery_trend=generate_trend_data(7.5),
            answer_accuracy_trend=generate_trend_data(78),
            progress_completion_trend=generate_trend_data(70),
            ability_improvement_trend=generate_trend_data(12),
            recent_evaluations=eval_responses,
            knowledge_gaps=["知识点2", "知识点5", "知识点7"]
        )
    )


@router.post("/agent/call", response_model=ApiResponse[Dict[str, Any]])
def call_evaluation_agent(
    request: EvaluationAgentInterface,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    if request.enable_agent:
        return success_response(
            data={
                "message": "学习效果评估智能体调用入口已预留",
                "agent_type": request.agent_type,
                "status": "pending_implementation"
            }
        )
    else:
        return success_response(
            data={
                "message": "智能体未启用，使用基础评估逻辑",
                "status": "using_basic_logic"
            }
        )


@router.post("/safety/check", response_model=ApiResponse[ContentSafetyCheckResponse])
def check_content_safety(
    request: ContentSafetyCheckRequest,
    current_user = Depends(get_current_user)
):
    try:
        sdk = ContentAuditSDK()
        result = sdk.check_text(request.content)
        
        is_safe = result.get("is_safe", True)
        risk_level = result.get("risk_level", "low")
        risk_types = result.get("risk_types", [])
        suggestion = "内容安全，可以正常使用" if is_safe else "内容存在风险，请修改后重试"
        
        return success_response(
            data=ContentSafetyCheckResponse(
                is_safe=is_safe,
                risk_level=risk_level,
                risk_types=risk_types,
                suggestion=suggestion,
                check_result=result
            )
        )
    except Exception as e:
        return success_response(
            data=ContentSafetyCheckResponse(
                is_safe=True,
                risk_level="low",
                risk_types=[],
                suggestion="内容安全检查服务暂不可用，已默认通过",
                check_result={"error": str(e)}
            )
        )


@router.post("/rag/retrieve", response_model=ApiResponse[List[RAGRetrievalItem]])
def rag_retrieve(
    request: RAGRetrievalRequest,
    current_user = Depends(get_current_user)
):
    mock_results = []
    for i in range(request.top_k):
        mock_results.append(RAGRetrievalItem(
            knowledge_id=i + 1,
            content=f"这是关于 '{request.query}' 的相关知识点内容示例 {i + 1}",
            similarity=random.uniform(0.7, 0.95),
            metadata={"source": "Python程序设计课程知识库"}
        ))
    
    return success_response(data=mock_results)


@router.post("/safety/agent/call", response_model=ApiResponse[Dict[str, Any]])
def call_safety_agent(
    request: SafetyAgentInterface,
    current_user = Depends(get_current_user)
):
    if request.enable_agent:
        return success_response(
            data={
                "message": "内容安全与防幻觉智能体调用入口已预留",
                "agent_type": request.agent_type,
                "status": "pending_implementation"
            }
        )
    else:
        return success_response(
            data={
                "message": "智能体未启用，使用基础安全校验逻辑",
                "status": "using_basic_logic"
            }
        )
