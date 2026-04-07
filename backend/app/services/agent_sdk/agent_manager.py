from typing import Dict, Optional
from .base import BaseAgent
from .orchestrator import OrchestratorAgent
import logging

logger = logging.getLogger(__name__)


class AgentManager:
    _instance: Optional['AgentManager'] = None
    _initialized: bool = False

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        self._initialized = True

        self.orchestrator = OrchestratorAgent()
        self.agents: Dict[str, BaseAgent] = {}

        logger.info("智能体管理器初始化完成")

    def register_agent(self, agent: BaseAgent):
        self.agents[agent.agent_id] = agent
        self.orchestrator.register_agent(agent)
        logger.info(f"智能体管理器注册: {agent.agent_name}")

    def get_agent(self, agent_id: str) -> Optional[BaseAgent]:
        return self.agents.get(agent_id)

    def get_orchestrator(self) -> OrchestratorAgent:
        return self.orchestrator

    def enable_agent(self, agent_id: str):
        if agent_id in self.agents:
            self.agents[agent_id].enabled = True
            logger.info(f"启用智能体: {self.agents[agent_id].agent_name}")

    def disable_agent(self, agent_id: str):
        if agent_id in self.agents:
            self.agents[agent_id].enabled = False
            logger.info(f"禁用智能体: {self.agents[agent_id].agent_name}")

    def list_agents(self) -> Dict[str, dict]:
        return {
            agent_id: {
                "name": agent.agent_name,
                "enabled": agent.enabled
            }
            for agent_id, agent in self.agents.items()
        }


agent_manager = AgentManager()
