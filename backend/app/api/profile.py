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
    message = message.lower()
    print(f"特征抽取 - 输入消息: {message}")
    
    keywords = {
        "knowledge_level": ["基础", "中级", "高级", "入门", "精通", "了解", "熟悉", "0基础", "零基础", "从零", "新手"],
        "cognitive_style": ["视觉", "听觉", "动觉", "阅读", "实践", "抽象", "具体", "看视频", "看图文", "听讲解", "动手做", "敲代码", "手敲", "独立钻研", "自学", "看教程"],
        "learning_pace": ["快", "慢", "中等", "循序渐进", "快速", "稳步", "着急", "慢慢来", "高效", "紧张", "从容"],
        "learning_goals": ["考试", "就业", "兴趣", "竞赛", "证书", "提升", "找工作", "跳槽", "转行", "以赛促学", "技能突破", "备赛"],
        "interest_directions": ["算法", "数据结构", "web开发", "机器学习", "数据分析", "自动化", "python", "爬虫", "人工智能", "逻辑"]
    }
    
    if any(keyword in message for keyword in keywords["knowledge_level"]):
        if "入门" in message or "了解" in message or "0基础" in message or "零基础" in message or "从零" in message or "新手" in message:
            features["knowledge_level"] = 2
            print("抽取到: 知识水平=入门(2)")
        elif "基础" in message or "熟悉" in message:
            features["knowledge_level"] = 5
            print("抽取到: 知识水平=基础(5)")
        elif "中级" in message:
            features["knowledge_level"] = 7
            print("抽取到: 知识水平=中级(7)")
        elif "高级" in message or "精通" in message:
            features["knowledge_level"] = 9
            print("抽取到: 知识水平=高级(9)")
    
    if any(keyword in message for keyword in keywords["cognitive_style"]):
        if "视觉" in message or "看视频" in message or "看图文" in message or "看教程" in message:
            features["cognitive_style"] = "视觉型"
            print("抽取到: 学习风格=视觉型")
        elif "听觉" in message or "听讲解" in message:
            features["cognitive_style"] = "听觉型"
            print("抽取到: 学习风格=听觉型")
        elif "动觉" in message or "实践" in message or "动手做" in message or "敲代码" in message or "手敲" in message or "独立钻研" in message or "自学" in message:
            features["cognitive_style"] = "动觉型"
            print("抽取到: 学习风格=动觉型")
        elif "阅读" in message:
            features["cognitive_style"] = "阅读型"
            print("抽取到: 学习风格=阅读型")
    
    if any(keyword in message for keyword in keywords["learning_pace"]):
        if "快" in message or "快速" in message or "着急" in message or "高效" in message or "紧张" in message:
            features["learning_pace"] = "快速"
            print("抽取到: 学习节奏=快速")
        elif "慢" in message or "循序渐进" in message or "慢慢来" in message or "从容" in message:
            features["learning_pace"] = "循序渐进"
            print("抽取到: 学习节奏=循序渐进")
        elif "中等" in message or "稳步" in message:
            features["learning_pace"] = "中等"
            print("抽取到: 学习节奏=中等")
    
    if any(keyword in message for keyword in keywords["learning_goals"]):
        if "竞赛" in message or "以赛促学" in message or "备赛" in message:
            features["learning_goals"] = "算法竞赛"
            print("抽取到: 学习目标=算法竞赛")
        elif "就业" in message or "找工作" in message or "跳槽" in message or "转行" in message:
            features["learning_goals"] = "就业"
            print("抽取到: 学习目标=就业")
        elif "考试" in message or "证书" in message:
            features["learning_goals"] = "考试/证书"
            print("抽取到: 学习目标=考试/证书")
        elif "提升" in message or "技能突破" in message:
            features["learning_goals"] = "技能提升"
            print("抽取到: 学习目标=技能提升")
        elif "兴趣" in message:
            features["learning_goals"] = "兴趣学习"
            print("抽取到: 学习目标=兴趣学习")
    
    if any(keyword in message for keyword in keywords["interest_directions"]):
        interests = []
        for interest in keywords["interest_directions"]:
            if interest in message:
                interests.append(interest)
        if interests:
            features["interest_directions"] = interests
            print(f"抽取到: 兴趣方向={interests}")
    
    print(f"特征抽取完成: {features}")
    return features


def generate_visualization_data(profile: StudentProfile) -> Dict[str, Any]:
    knowledge_level = float(profile.knowledge_level) if profile.knowledge_level else 5.0
    
    learning_style_score = 5.0
    if profile.cognitive_style_tags:
        if "视觉" in profile.cognitive_style_tags:
            learning_style_score = 7.5
        elif "听觉" in profile.cognitive_style_tags:
            learning_style_score = 6.5
        elif "动觉" in profile.cognitive_style_tags:
            learning_style_score = 8.0
        elif "阅读" in profile.cognitive_style_tags:
            learning_style_score = 7.0
    
    learning_pace_score = 6.0
    if profile.learning_pace_preference:
        if "快速" in profile.learning_pace_preference:
            learning_pace_score = 8.0
        elif "循序渐进" in profile.learning_pace_preference:
            learning_pace_score = 5.5
        elif "中等" in profile.learning_pace_preference:
            learning_pace_score = 6.5
    
    interest_score = 6.0
    if profile.interest_directions:
        interests = json.loads(profile.interest_directions)
        interest_score = 6.0 + min(len(interests), 4) * 0.5
    
    radar_data = {
        "知识基础": knowledge_level,
        "学习风格": learning_style_score,
        "学习目标": 6.0,
        "学习节奏": learning_pace_score,
        "兴趣方向": interest_score,
        "学习习惯": 6.0,
        "实践能力": knowledge_level * 0.8 + 2.0
    }
    
    heatmap_data = [
        [knowledge_level, learning_style_score - 1, interest_score - 1, learning_pace_score],
        [6.0, 7.0, 6.0, 6.5],
        [5.5, 6.0, interest_score, 5.5],
        [knowledge_level + 1, 6.5, 5.5, 6.0]
    ]
    
    dimension_details = ProfileDimension(
        knowledge_level=knowledge_level,
        cognitive_style=profile.cognitive_style_tags or "暂未设定",
        knowledge_weakness=json.loads(profile.weakness_tags) if profile.weakness_tags else [],
        error_prone_points=json.loads(profile.error_prone_tags) if profile.error_prone_tags else [],
        learning_goals=profile.learning_goals or "暂未设定",
        learning_pace=profile.learning_pace_preference or "暂未设定",
        interest_directions=json.loads(profile.interest_directions) if profile.interest_directions else [],
        learning_behavior="对话收集阶段"
    )
    
    print(f"可视化数据生成完成:")
    print(f"  知识基础: {knowledge_level}")
    print(f"  学习风格: {profile.cognitive_style_tags}")
    print(f"  学习节奏: {profile.learning_pace_preference}")
    print(f"  兴趣方向: {profile.interest_directions}")
    
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
    
    ai_extracted_features = {}
    
    if "专属学习画像" in response_message or "知识基础" in response_message:
        print("检测到AI回复包含结构化画像，尝试提取...")
        
        if "零基础入门" in response_message or "从零搭建" in response_message:
            ai_extracted_features["knowledge_level"] = 2
            print("从AI回复提取: 知识水平=2")
        elif "基础" in response_message:
            ai_extracted_features["knowledge_level"] = 5
            print("从AI回复提取: 知识水平=5")
        
        if "视觉型" in response_message and "动觉型" in response_message:
            ai_extracted_features["cognitive_style"] = "视觉型+动觉型"
            print("从AI回复提取: 学习风格=视觉型+动觉型")
        elif "视觉型" in response_message:
            ai_extracted_features["cognitive_style"] = "视觉型"
            print("从AI回复提取: 学习风格=视觉型")
        elif "动觉型" in response_message:
            ai_extracted_features["cognitive_style"] = "动觉型"
            print("从AI回复提取: 学习风格=动觉型")
        elif "听觉型" in response_message:
            ai_extracted_features["cognitive_style"] = "听觉型"
            print("从AI回复提取: 学习风格=听觉型")
        
        if "快速推进" in response_message or "高效突破" in response_message or "紧张节奏" in response_message:
            ai_extracted_features["learning_pace"] = "快速"
            print("从AI回复提取: 学习节奏=快速")
        elif "循序渐进" in response_message:
            ai_extracted_features["learning_pace"] = "循序渐进"
            print("从AI回复提取: 学习节奏=循序渐进")
        
        if "算法竞赛" in response_message:
            ai_extracted_features["learning_goals"] = "算法竞赛"
            print("从AI回复提取: 学习目标=算法竞赛")
        elif "就业" in response_message:
            ai_extracted_features["learning_goals"] = "就业"
            print("从AI回复提取: 学习目标=就业")
        elif "证书" in response_message:
            ai_extracted_features["learning_goals"] = "证书"
            print("从AI回复提取: 学习目标=证书")
        
        if "算法" in response_message and "逻辑" in response_message:
            ai_extracted_features["interest_directions"] = ["算法", "逻辑"]
            print("从AI回复提取: 兴趣方向=['算法', '逻辑']")
        elif "算法" in response_message:
            ai_extracted_features["interest_directions"] = ["算法"]
            print("从AI回复提取: 兴趣方向=['算法']")
    
    final_features = {**extracted_features, **ai_extracted_features}
    print(f"最终合并后的特征: {final_features}")
    
    if final_features:
        if "我注意到" not in response_message and not ai_extracted_features:
            response_message += " 我注意到您提到了一些关于您学习的特点，这对构建您的画像很有帮助！"
        
        profile = db.query(StudentProfile).filter(StudentProfile.user_id == request.user_id).first()
        print(f"查询到的profile: {profile}")
        if not profile:
            profile = StudentProfile(user_id=request.user_id)
            db.add(profile)
            print(f"创建新profile: {profile}")
        
        if "knowledge_level" in final_features:
            profile.knowledge_level = str(final_features["knowledge_level"])
            print(f"设置knowledge_level: {profile.knowledge_level}")
        
        if "cognitive_style" in final_features:
            profile.cognitive_style_tags = final_features["cognitive_style"]
            print(f"设置cognitive_style_tags: {profile.cognitive_style_tags}")
        
        if "learning_pace" in final_features:
            profile.learning_pace_preference = final_features["learning_pace"]
            print(f"设置learning_pace_preference: {profile.learning_pace_preference}")
        
        if "learning_goals" in final_features:
            profile.learning_goals = final_features["learning_goals"]
            print(f"设置learning_goals: {profile.learning_goals}")
        
        if "interest_directions" in final_features:
            profile.interest_directions = json.dumps(final_features["interest_directions"], ensure_ascii=False)
            print(f"设置interest_directions: {profile.interest_directions}")
        
        db.commit()
        db.refresh(profile)
        print(f"画像已更新提交到数据库: user_id={request.user_id}")
        print(f"刷新后的profile: knowledge_level={profile.knowledge_level}, cognitive_style_tags={profile.cognitive_style_tags}, learning_pace_preference={profile.learning_pace_preference}, learning_goals={profile.learning_goals}, interest_directions={profile.interest_directions}")
    
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
    print(f"获取画像可视化数据: user_id={user_id}")
    profile = db.query(StudentProfile).filter(StudentProfile.user_id == user_id).first()
    print(f"从数据库查询到的profile: {profile}")
    
    if not profile:
        profile = StudentProfile(user_id=user_id, knowledge_level="5.0")
        db.add(profile)
        db.commit()
        db.refresh(profile)
        print(f"创建了新的profile: {profile}")
    
    print(f"准备生成可视化数据...")
    viz_data = generate_visualization_data(profile)
    print(f"可视化数据生成完成: {viz_data}")
    
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
