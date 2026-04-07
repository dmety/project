from typing import Any, Dict, Optional
from pydantic import BaseModel
import logging

logger = logging.getLogger(__name__)


class AgentRequest(BaseModel):
    user_id: int
    request_type: str
    request_data: Dict[str, Any]


class AgentResponse(BaseModel):
    workflow_id: str
    status: str
    final_result: Dict[str, Any]
    execution_log: Dict[str, Any]


class BaseAgent:
    def __init__(self, agent_id: str, agent_name: str):
        self.agent_id = agent_id
        self.agent_name = agent_name
        self.enabled = True

    async def execute(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        raise NotImplementedError("子类必须实现execute方法")

    async def call(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        if not self.enabled:
            logger.warning(f"智能体 {self.agent_name} 未启用")
            return self._get_fallback_response()

        try:
            logger.info(f"调用智能体: {self.agent_name}")
            result = await self.execute(request_data)
            logger.info(f"智能体 {self.agent_name} 执行完成")
            return result
        except Exception as e:
            logger.error(f"智能体 {self.agent_name} 执行失败: {e}")
            return self._get_fallback_response()

    def _get_fallback_response(self) -> Dict[str, Any]:
        return {
            "agent_id": self.agent_id,
            "agent_name": self.agent_name,
            "status": "fallback",
            "result": {},
            "message": "智能体暂时不可用，使用基础逻辑"
        }
