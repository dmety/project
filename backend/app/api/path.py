from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import Dict, Any, List
from datetime import datetime, timedelta

from app.core.database import get_db
from app.core.response import ApiResponse, success_response
from app.core.security import get_current_user
from app.models.learning import LearningPath, PathNode, LearningResource
from app.schemas.path import (
    LearningPathCreate,
    LearningPathResponse,
    PathGenerateRequest,
    PathNodeUpdateRequest,
    ResourcePushRequest,
    ResourcePushItem,
    PathAgentInterface,
    PathNodeResponse
)

router = APIRouter(prefix="/path", tags=["学习路径"])


def generate_default_path_nodes() -> List[Dict[str, Any]]:
    nodes = []
    knowledge_ids = [1, 2, 3, 4, 5, 6, 7, 8]
    
    for i, kid in enumerate(knowledge_ids):
        node = {
            "knowledge_id": kid,
            "learning_order": i + 1,
            "is_milestone": (i + 1) % 2 == 0,
            "learning_content": f"学习知识点 {kid}",
            "completion_status": 0,
            "planned_completion_time": datetime.now() + timedelta(days=i + 1)
        }
        nodes.append(node)
    
    return nodes


def build_path_node_response(node: PathNode) -> PathNodeResponse:
    return PathNodeResponse(
        node_id=node.node_id,
        path_id=node.path_id,
        knowledge_id=node.knowledge_id,
        learning_order=node.learning_order,
        milestone_flag=node.is_milestone or False,
        learning_content=node.learning_content,
        completion_status=node.completion_status or 0,
        plan_completion_time=node.planned_completion_time,
        actual_completion_time=node.actual_completion_time
    )


def build_path_response(path: LearningPath, nodes: List[PathNode] = None) -> LearningPathResponse:
    if nodes is None:
        nodes = []
    
    node_responses = [build_path_node_response(n) for n in nodes]
    
    return LearningPathResponse(
        path_id=path.path_id,
        user_id=path.user_id,
        path_name=path.path_name,
        learning_cycle=path.learning_cycle,
        total_milestones=path.total_milestones or 0,
        completed_milestones=path.completed_milestones or 0,
        current_progress=path.current_progress or 0.0,
        status=path.status or 0,
        created_at=path.created_at,
        updated_at=path.updated_at,
        nodes=node_responses
    )


@router.post("/generate", response_model=ApiResponse[LearningPathResponse])
def generate_learning_path(
    request: PathGenerateRequest,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    nodes_data = generate_default_path_nodes()
    
    learning_path = LearningPath(
        user_id=request.user_id,
        path_name=request.path_name,
        learning_cycle=30,
        total_milestones=4,
        completed_milestones=0,
        current_progress=0.0,
        status=0
    )
    
    db.add(learning_path)
    db.flush()
    
    path_nodes = []
    for node_data in nodes_data:
        path_node = PathNode(
            path_id=learning_path.path_id,
            **node_data
        )
        db.add(path_node)
        path_nodes.append(path_node)
    
    db.commit()
    db.refresh(learning_path)
    
    return success_response(data=build_path_response(learning_path, path_nodes))


@router.get("/list/{user_id}", response_model=ApiResponse[List[LearningPathResponse]])
def list_learning_paths(
    user_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    paths = db.query(LearningPath).filter(LearningPath.user_id == user_id).all()
    
    path_responses = []
    for path in paths:
        nodes = db.query(PathNode).filter(PathNode.path_id == path.path_id).order_by(PathNode.learning_order).all()
        path_responses.append(build_path_response(path, nodes))
    
    return success_response(data=path_responses)


@router.get("/detail/{path_id}", response_model=ApiResponse[LearningPathResponse])
def get_path_detail(
    path_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    path = db.query(LearningPath).filter(LearningPath.path_id == path_id).first()
    
    if not path:
        return success_response(code=404, message="学习路径不存在")
    
    nodes = db.query(PathNode).filter(PathNode.path_id == path_id).order_by(PathNode.learning_order).all()
    
    return success_response(data=build_path_response(path, nodes))


@router.post("/node/update", response_model=ApiResponse[Dict[str, Any]])
def update_path_node(
    request: PathNodeUpdateRequest,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    node = db.query(PathNode).filter(PathNode.node_id == request.node_id).first()
    
    if not node:
        return success_response(code=404, message="路径节点不存在")
    
    if request.completion_status is not None:
        node.completion_status = request.completion_status
        if request.completion_status == 1:
            node.actual_completion_time = datetime.now()
    
    if request.learning_content is not None:
        node.learning_content = request.learning_content
    
    if request.actual_completion_time is not None:
        node.actual_completion_time = request.actual_completion_time
    
    path = db.query(LearningPath).filter(LearningPath.path_id == node.path_id).first()
    if path:
        all_nodes = db.query(PathNode).filter(PathNode.path_id == path.path_id).all()
        completed = sum(1 for n in all_nodes if n.completion_status == 1)
        path.current_progress = (completed / len(all_nodes)) * 100 if all_nodes else 0
        path.completed_milestones = sum(1 for n in all_nodes if n.completion_status == 1 and n.is_milestone)
        path.updated_at = datetime.now()
    
    db.commit()
    
    return success_response(data={"message": "节点更新成功"})


@router.post("/push", response_model=ApiResponse[List[ResourcePushItem]])
def push_resources(
    request: ResourcePushRequest,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    query = db.query(LearningResource).filter(LearningResource.user_id == request.user_id)
    
    if request.knowledge_id:
        query = query.filter(LearningResource.knowledge_id == request.knowledge_id)
    
    resources = query.order_by(LearningResource.generated_at.desc()).limit(10).all()
    
    push_items = []
    for resource in resources:
        push_items.append(ResourcePushItem(
            resource_id=resource.resource_id,
            knowledge_id=resource.knowledge_id,
            resource_type=resource.resource_type,
            read_status=resource.usage_status
        ))
    
    return success_response(data=push_items)


@router.post("/agent/call", response_model=ApiResponse[Dict[str, Any]])
def call_path_agent(
    request: PathAgentInterface,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    if request.enable_agent:
        return success_response(
            data={
                "message": "学习路径规划智能体调用入口已预留",
                "agent_type": request.agent_type,
                "status": "pending_implementation"
            }
        )
    else:
        return success_response(
            data={
                "message": "智能体未启用，使用基础路径规划逻辑",
                "status": "using_basic_logic"
            }
        )
