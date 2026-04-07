from typing import Any, Dict, List, Optional
from .base import BaseAgent, AgentRequest, AgentResponse
import uuid
import time
import logging

logger = logging.getLogger(__name__)


class OrchestratorAgent(BaseAgent):
    def __init__(self):
        super().__init__("12", "中枢调度智能体")
        self.agents: Dict[str, BaseAgent] = {}

    def register_agent(self, agent: BaseAgent):
        self.agents[agent.agent_id] = agent
        logger.info(f"注册智能体: {agent.agent_name}")

    async def execute(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        workflow_id = str(uuid.uuid4())
        start_time = time.time()

        logger.info(f"开始工作流: {workflow_id}")

        try:
            user_id = request_data.get("user_id")
            request_type = request_data.get("request_type")
            request_data_inner = request_data.get("request_data", {})

            executed_agents = []
            final_result = {}

            if request_type == "profile" and "01" in self.agents:
                result = await self.agents["01"].call(request_data_inner)
                executed_agents.append(result)
                final_result = result.get("result", {})

            elif request_type == "resource" and "02" in self.agents:
                for agent_id in ["02", "03", "04", "05", "06", "07"]:
                    if agent_id in self.agents:
                        result = await self.agents[agent_id].call(request_data_inner)
                        executed_agents.append(result)
                        if agent_id == "02":
                            final_result = result.get("result", {})

            elif request_type == "path" and "08" in self.agents:
                result = await self.agents["08"].call(request_data_inner)
                executed_agents.append(result)
                final_result = result.get("result", {})

            elif request_type == "tutor" and "09" in self.agents:
                result = await self.agents["09"].call(request_data_inner)
                executed_agents.append(result)
                final_result = result.get("result", {})

            elif request_type == "evaluation" and "10" in self.agents:
                result = await self.agents["10"].call(request_data_inner)
                executed_agents.append(result)
                final_result = result.get("result", {})

            if "11" in self.agents and final_result:
                safety_result = await self.agents["11"].call({
                    "content": str(final_result),
                    "content_type": "text"
                })
                executed_agents.append(safety_result)

            end_time = time.time()
            total_duration = end_time - start_time

            return {
                "workflow_id": workflow_id,
                "status": "success" if executed_agents else "partial_success",
                "user_profile": {},
                "executed_agents": executed_agents,
                "safety_check_result": {},
                "final_result": final_result,
                "execution_log": {
                    "start_time": time.strftime("%Y-%m-%dT%H:%M:%S"),
                    "end_time": time.strftime("%Y-%m-%dT%H:%M:%S"),
                    "total_duration": total_duration,
                    "errors": []
                }
            }

        except Exception as e:
            logger.error(f"工作流执行失败: {e}")
            return {
                "workflow_id": workflow_id,
                "status": "failed",
                "user_profile": {},
                "executed_agents": [],
                "safety_check_result": {},
                "final_result": {},
                "execution_log": {
                    "start_time": time.strftime("%Y-%m-%dT%H:%M:%S"),
                    "end_time": time.strftime("%Y-%m-%dT%H:%M:%S"),
                    "total_duration": 0,
                    "errors": [str(e)]
                }
            }

    async def orchestrate(self, request: AgentRequest) -> AgentResponse:
        result = await self.call(request.dict())
        return AgentResponse(**result)
