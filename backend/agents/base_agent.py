import logging
from typing import Dict, Any
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class BaseAgent:
    def __init__(self, name: str):
        self.name = name
        self.memory = []
        self.status = "idle"
    
    def log(self, msg: str):
        logger.info(f"[{self.name}] {msg}")
    
    async def process(self, data: Dict) -> Dict:
        raise NotImplementedError
    
    def update_memory(self, data: Any):
        self.memory.append({
            "timestamp": datetime.now().isoformat(),
            "data": data
        })
        if len(self.memory) > 100:
            self.memory = self.memory[-50:]

class AgentOrchestrator:
    def __init__(self):
        self.agents = {}
    
    def register(self, agent: BaseAgent):
        self.agents[agent.name] = agent
        self.log(f"Registered {agent.name}")
    
    async def execute(self, workflow: list) -> Dict:
        results = {}
        for step in workflow:
            agent_name = step.get("agent")
            if agent_name in self.agents:
                agent = self.agents[agent_name]
                agent.log(f"Processing: {step.get('name')}")
                try:
                    result = await agent.process(step.get("input", {}))
                    results[agent_name] = result
                    # Pass results to next step
                    for next_step in workflow:
                        if next_step.get("depends_on") == agent_name:
                            next_step["input"] = result
                except Exception as e:
                    agent.log(f"Error: {str(e)}")
                    results[agent_name] = {"error": str(e)}
        return results
    
    def log(self, msg: str):
        logger.info(f"[Orchestrator] {msg}")
