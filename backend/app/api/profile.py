from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import json
from datetime import datetime
import uuid
from typing import Dict, Any

from app.core.database import get_db
from app.core.response import ApiResponse, success_response
from app.core.security import get_current_user
from app.models.user import StudentProfile
from app.schemas.profile import (
    ProfileDimension,
    ProfileDialogRequest,
    ProfileDialogResponse,
    ProfileUpdateRequest,
    ProfileVisualizationData,
    ProfileAgentInterface
)
from app.services.xfyun_sdk.spark_sdk import SparkSDK

router = APIRouter(prefix="/profile", tags=["学生画像"])

spark_sdk = SparkSDK()

PROFILE_SYSTEM_PROMPT = """你是一个专业的学生画像构建助手。你的任务是通过自然对话了解用户的学习情况，构建完整的学习画像。

请按照以下方式与用户对话：
1. 主动引导用户提供信息，但不要太机械
2. 根据用户的回答，灵活地继续提问或确认信息
3. 语气要友好、专业，像一个学习顾问
4. 当信息收集得比较完整时，可以告诉用户画像已初步构建完成

需要收集的信息包括：
- 知识基础水平（入门/基础/中级/高级）
- 学习风格（视觉型/听觉型/动觉型/阅读型）
- 学习节奏偏好（快速/循序渐进/中等）
- 学习目标（考试/就业/兴趣/竞赛/证书/提升）
- 兴趣方向（算法/数据结构/Web开发/机器学习/数据分析/自动化等）
- 学习行为习惯

不要一次性问所有问题，要循序渐进地引导！"""


def extract_features_from_dialog(message: str) -> Dict[str, Any]:
    features = {}
    
    keywords = {
        "knowledge_level": ["基础", "中级", "高级", "入门", "精通", "了解", "熟悉"],
        "cognitive_style": ["视觉", "听觉", "动觉", "阅读", "实践", "抽象", "具体"],
        "learning_pace": ["快", "慢", "中等", "循序渐进", "快速", "稳步"],
        "learning_goals": ["考试", "就业", "兴趣", "竞赛", "证书", "提升"],
        "interest_directions": ["算法", "数据结构", "Web开发", "机器学习", "数据分析", "自动化"]
    }
    
    if any(keyword in message for keyword in keywords["knowledge_level"]):
        if "入门" in message or "了解" in message:
            features["knowledge_level"] = 3
        elif "基础" in message or "熟悉" in message:
            features["knowledge_level"] = 6
        elif "中级" in message:
            features["knowledge_level"] = 7
        elif "高级" in message or "精通" in message:
            features["knowledge_level"] = 9
    
    if any(keyword in message for keyword in keywords["cognitive_style"]):
        if "视觉" in message:
            features["cognitive_style"] = "视觉型"
        elif "听觉" in message:
            features["cognitive_style"] = "听觉型"
        elif "动觉" in message or "实践" in message:
            features["cognitive_style"] = "动觉型"
        elif "阅读" in message:
            features["cognitive_style"] = "阅读型"
    
    if any(keyword in message for keyword in keywords["learning_pace"]):
        if "快" in message or "快速" in message:
            features["learning_pace"] = "快速"
        elif "慢" in message or "循序渐进" in message:
            features["learning_pace"] = "循序渐进"
        elif "中等" in message or "稳步" in message:
            features["learning_pace"] = "中等"
    
    if any(keyword in message for keyword in keywords["interest_directions"]):
        interests = []
        for interest in keywords["interest_directions"]:
            if interest in message:
                interests.append(interest)
        if interests:
            features["interest_directions"] = interests
    
    return features


def generate_visualization_data(profile: StudentProfile) -> Dict[str, Any]:
    knowledge_level = float(profile.knowledge_level) if profile.knowledge_level else 5.0
    
    radar_data = {
        "知识基础": knowledge_level,
        "学习风格": 7.0,
        "学习目标": 6.0,
        "学习节奏": 6.5,
        "兴趣方向": 7.5,
        "学习习惯": 6.0,
        "实践能力": 5.5
    }
    
    heatmap_data = [
        [knowledge_level, 6.5, 5.5, 7.0],
        [6.0, 7.0, 6.0, 6.5],
        [5.5, 6.0, 7.5, 5.5],
        [7.0, 6.5, 5.5, 6.0]
    ]
    
    dimension_details = ProfileDimension(
        knowledge_level=knowledge_level,
        cognitive_style=profile.cognitive_style_tags,
        knowledge_weakness=json.loads(profile.weakness_tags) if profile.weakness_tags else [],
        error_prone_points=json.loads(profile.error_prone_tags) if profile.error_prone_tags else [],
        learning_goals=profile.learning_goals,
        learning_pace=profile.learning_pace_preference,
        interest_directions=json.loads(profile.interest_directions) if profile.interest_directions else [],
        learning_behavior="需要更多学习行为数据"
    )
    
    return {
        "radar_data": radar_data,
        "heatmap_data": heatmap_data,
        "dimension_details": dimension_details
    }


@router.post("/dialog", response_model=ApiResponse[ProfileDialogResponse])
def profile_dialog(
    request: ProfileDialogRequest,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    conversation_id = request.conversation_id or str(uuid.uuid4())
    
    extracted_features = extract_features_from_dialog(request.message)
    
    try:
        messages = [
            {"role": "system", "content": PROFILE_SYSTEM_PROMPT}
        ]
        
        if request.history:
            for msg in request.history:
                messages.append({"role": msg.role, "content": msg.content})
        
        messages.append({"role": "user", "content": request.message})
        
        print(f"发送给星火的消息数: {len(messages)}")
        
        spark_response = spark_sdk.chat(messages, temperature=0.8, max_tokens=500)
        print(f"星火API响应: {spark_response}")
        
        if spark_response.get("success"):
            response_message = spark_response["content"]
        else:
            error_msg = spark_response.get("error", "未知错误")
            print(f"星火API调用失败: {error_msg}")
            response_message = f"好的，我已经了解了您的一些情况。让我继续了解更多关于您的学习情况，以便为您构建更准确的画像。(AI服务暂不可用: {error_msg})"
    except Exception as e:
        print(f"星火大模型调用异常: {str(e)}")
        import traceback
        print(f"堆栈信息: {traceback.format_exc()}")
        response_message = f"好的，我已经了解了您的一些情况。让我继续了解更多关于您的学习情况，以便为您构建更准确的画像。(系统异常: {str(e)})"
    
    if extracted_features:
        if "我注意到" not in response_message:
            response_message += " 我注意到您提到了一些关于您学习的特点，这对构建您的画像很有帮助！"
    
    return success_response(
        data=ProfileDialogResponse(
            conversation_id=conversation_id,
            assistant_message=response_message,
            extracted_features=extracted_features
        )
    )


@router.post("/update", response_model=ApiResponse[Dict[str, Any]])
def update_profile(
    request: ProfileUpdateRequest,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    profile = db.query(StudentProfile).filter(StudentProfile.user_id == request.user_id).first()
    
    if not profile:
        profile = StudentProfile(user_id=request.user_id)
        db.add(profile)
    
    profile.knowledge_level = str(request.dimensions.knowledge_level) if request.dimensions.knowledge_level else None
    profile.cognitive_style_tags = request.dimensions.cognitive_style
    profile.weakness_tags = json.dumps(request.dimensions.knowledge_weakness, ensure_ascii=False)
    profile.error_prone_tags = json.dumps(request.dimensions.error_prone_points, ensure_ascii=False)
    profile.learning_goals = request.dimensions.learning_goals
    profile.learning_pace_preference = request.dimensions.learning_pace
    profile.interest_directions = json.dumps(request.dimensions.interest_directions, ensure_ascii=False)
    
    db.commit()
    db.refresh(profile)
    
    return success_response(data={"message": "画像更新成功", "profile_id": profile.profile_id})


@router.get("/visualization/{user_id}", response_model=ApiResponse[ProfileVisualizationData])
def get_profile_visualization(
    user_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    profile = db.query(StudentProfile).filter(StudentProfile.user_id == user_id).first()
    
    if not profile:
        profile = StudentProfile(user_id=user_id, knowledge_level="5.0")
        db.add(profile)
        db.commit()
        db.refresh(profile)
    
    viz_data = generate_visualization_data(profile)
    
    return success_response(
        data=ProfileVisualizationData(
            user_id=user_id,
            radar_data=viz_data["radar_data"],
            heatmap_data=viz_data["heatmap_data"],
            dimension_details=viz_data["dimension_details"],
            updated_at=profile.updated_at or profile.created_at
        )
    )


@router.post("/agent/call", response_model=ApiResponse[Dict[str, Any]])
def call_profile_agent(
    request: ProfileAgentInterface,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    if request.enable_agent:
        return success_response(
            data={
                "message": "智能体调用入口已预留",
                "agent_type": request.agent_type,
                "status": "pending_implementation"
            }
        )
    else:
        return success_response(
            data={
                "message": "智能体未启用，使用基础逻辑",
                "status": "using_basic_logic"
            }
        )
