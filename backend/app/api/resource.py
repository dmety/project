from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import Dict, Any
from datetime import datetime

from app.core.database import get_db
from app.core.response import ApiResponse, success_response
from app.core.security import get_current_user
from app.models.learning import LearningResource
from app.schemas.resource import (
    ResourceGenerateRequest,
    ResourceResponse,
    ResourceListRequest,
    ResourceListResponse,
    ResourceFeedbackRequest,
    ResourceAgentInterface,
    GenerateProgressResponse
)

router = APIRouter(prefix="/resource", tags=["学习资源"])


def generate_resource_content(
    knowledge_id: int,
    resource_type: str,
    difficulty: str
) -> str:
    type_names = {
        "course_doc": "课程讲解文档",
        "mind_map": "知识点思维导图",
        "exercise": "分难度练习题",
        "code_case": "Python代码实操案例",
        "extension_reading": "拓展阅读材料",
        "multimodal_diagram": "多模态教学图解"
    }
    
    difficulty_names = {
        "easy": "简单",
        "medium": "中等",
        "hard": "困难"
    }
    
    content = f"""# {type_names.get(resource_type, "学习资源")}

## 知识点ID: {knowledge_id}
## 难度等级: {difficulty_names.get(difficulty, "中等")}

### 内容概述

这是一个基于知识点ID {knowledge_id} 生成的{type_names.get(resource_type, "学习资源")}，
难度等级为{difficulty_names.get(difficulty, "中等")}。

### 资源说明

- 该资源是系统自动生成的示例内容
- 实际使用时将根据用户画像和知识点内容动态生成
- 可以通过启用智能体来获得更精准的资源生成

### 学习建议

1. 首先阅读资源的整体框架
2. 重点关注核心概念和示例
3. 完成配套的练习题
4. 如有疑问，使用智能辅导功能

---
*生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*
"""
    return content


@router.post("/generate", response_model=ApiResponse[ResourceResponse])
def generate_resource(
    request: ResourceGenerateRequest,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    resource_content = generate_resource_content(
        request.knowledge_id,
        request.resource_type.value,
        request.difficulty.value
    )
    
    resource = LearningResource(
        user_id=request.user_id,
        knowledge_id=request.knowledge_id,
        resource_type=request.resource_type.value,
        resource_content=resource_content,
        usage_status=0,
        is_compliant=True
    )
    
    db.add(resource)
    db.commit()
    db.refresh(resource)
    
    return success_response(data=resource)


@router.get("/progress/{task_id}", response_model=ApiResponse[GenerateProgressResponse])
def get_generate_progress(
    task_id: str,
    current_user = Depends(get_current_user)
):
    return success_response(
        data=GenerateProgressResponse(
            progress=100.0,
            status="completed",
            message="资源生成完成"
        )
    )


@router.get("/list", response_model=ApiResponse[ResourceListResponse])
def list_resources(
    user_id: int,
    knowledge_id: int = None,
    resource_type: str = None,
    page: int = 1,
    page_size: int = 10,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    query = db.query(LearningResource).filter(LearningResource.user_id == user_id)
    
    if knowledge_id:
        query = query.filter(LearningResource.knowledge_id == knowledge_id)
    
    if resource_type:
        query = query.filter(LearningResource.resource_type == resource_type)
    
    total = query.count()
    resources = query.order_by(LearningResource.generated_at.desc()) \
                    .offset((page - 1) * page_size) \
                    .limit(page_size) \
                    .all()
    
    return success_response(
        data=ResourceListResponse(
            total=total,
            page=page,
            page_size=page_size,
            resources=resources
        )
    )


@router.get("/detail/{resource_id}", response_model=ApiResponse[ResourceResponse])
def get_resource_detail(
    resource_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    resource = db.query(LearningResource).filter(LearningResource.resource_id == resource_id).first()
    
    if not resource:
        return success_response(code=404, message="资源不存在")
    
    return success_response(data=resource)


@router.post("/feedback", response_model=ApiResponse[Dict[str, Any]])
def submit_resource_feedback(
    request: ResourceFeedbackRequest,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    resource = db.query(LearningResource).filter(
        LearningResource.resource_id == request.resource_id,
        LearningResource.user_id == request.user_id
    ).first()
    
    if not resource:
        return success_response(code=404, message="资源不存在")
    
    resource.user_feedback = request.feedback
    resource.usage_status = 1
    
    db.commit()
    
    return success_response(data={"message": "反馈提交成功"})


@router.post("/agent/call", response_model=ApiResponse[Dict[str, Any]])
def call_resource_agent(
    request: ResourceAgentInterface,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    if request.enable_agent:
        return success_response(
            data={
                "message": "多智能体协同调用入口已预留",
                "agent_type": request.agent_type,
                "status": "pending_implementation"
            }
        )
    else:
        return success_response(
            data={
                "message": "智能体未启用，使用基础生成逻辑",
                "status": "using_basic_logic"
            }
        )
