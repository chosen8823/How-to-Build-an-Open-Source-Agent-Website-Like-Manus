from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional

@dataclass
class ToolSpec:
    name: str
    description: str
    args_schema: Dict[str, Any] = field(default_factory=dict)

@dataclass
class AgentSpec:
    id: str
    role: str
    goals: List[str]
    tools: List[ToolSpec] = field(default_factory=list)
    memory: Dict[str, Any] = field(default_factory=dict)
    model: str = "sophia"

@dataclass
class TeamFormation:
    name: str
    mission: str
    agents: List[AgentSpec]
    comms: str = "socketio"  # 'socketio' | 'rest'
    routing: str = "round_robin"  # 'round_robin' | 'by_role' | 'llm_planner'

@dataclass
class Task:
    id: str
    description: str
    context: Dict[str, Any] = field(default_factory=dict)
    status: str = "pending"
    assigned_to: Optional[str] = None
    results: Dict[str, Any] = field(default_factory=dict)
