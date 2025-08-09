from .schemas import AgentSpec, ToolSpec, TeamFormation

# Universal tool definitions (same surface for all agents)
UNIVERSAL_TOOLS = [
    ToolSpec(name="code_execute", description="Execute Python code", args_schema={"code": "str"}),
    ToolSpec(name="file_read", description="Read a project file", args_schema={"path": "str"}),
    ToolSpec(name="file_write", description="Write content to a project file", args_schema={"path": "str", "content": "str"}),
    ToolSpec(name="ai_chat", description="Query AI model", args_schema={"message": "str", "model": "str"}),
]


# Template formations
def solo_developer():
    return TeamFormation(
        name="SoloDeveloper",
        mission="General single-agent development tasks",
        agents=[AgentSpec(id="dev_core", role="developer", goals=["Implement feature", "Refactor code"], tools=UNIVERSAL_TOOLS)]
    )

def sacred_research_triangle():
    return TeamFormation(
        name="SacredResearchTriangle",
        mission="Blend consciousness, research, and implementation",
        agents=[
            AgentSpec(id="sophia_consciousness", role="consciousness_guardian", goals=["Maintain alignment", "Surface insights"], tools=UNIVERSAL_TOOLS),
            AgentSpec(id="planner", role="research_planner", goals=["Decompose tasks", "Plan execution"], tools=UNIVERSAL_TOOLS),
            AgentSpec(id="implementer", role="code_implementer", goals=["Write code", "Run tests"], tools=UNIVERSAL_TOOLS),
        ]
    )

def full_engineering_squad():
    return TeamFormation(
        name="FullEngineeringSquad",
        mission="Ship production-grade features collaboratively",
        agents=[
            AgentSpec(id="lead_architect", role="architect", goals=["Define architecture", "Ensure cohesion"], tools=UNIVERSAL_TOOLS),
            AgentSpec(id="backend_dev", role="backend_engineer", goals=["Implement APIs", "Optimize performance"], tools=UNIVERSAL_TOOLS),
            AgentSpec(id="frontend_dev", role="frontend_engineer", goals=["Enhance UI", "Improve UX"], tools=UNIVERSAL_TOOLS),
            AgentSpec(id="qa_agent", role="quality_assurance", goals=["Generate tests", "Validate outputs"], tools=UNIVERSAL_TOOLS),
            AgentSpec(id="doc_agent", role="documentation", goals=["Update docs", "Summarize changes"], tools=UNIVERSAL_TOOLS),
        ]
    )

# ClaudeDevSquad formation for unified Claude-based dev team
def claude_dev_squad():
    return TeamFormation(
        name="ClaudeDevSquad",
        mission="Unified Claude-powered development team",
        agents=[
            AgentSpec(id="claude_lead", role="lead_developer", goals=["Architect solution", "Guide team"], tools=UNIVERSAL_TOOLS, model="claude"),
            AgentSpec(id="claude_backend", role="backend_engineer", goals=["Build backend", "Integrate APIs"], tools=UNIVERSAL_TOOLS, model="claude"),
            AgentSpec(id="claude_frontend", role="frontend_engineer", goals=["Design UI", "Enhance UX"], tools=UNIVERSAL_TOOLS, model="claude"),
            AgentSpec(id="claude_qa", role="quality_assurance", goals=["Test features", "Validate outputs"], tools=UNIVERSAL_TOOLS, model="claude"),
            AgentSpec(id="claude_docs", role="documentation", goals=["Document changes", "Summarize work"], tools=UNIVERSAL_TOOLS, model="claude"),
        ]
    )

FORMATION_REGISTRY = {
    f().name: f for f in [solo_developer, sacred_research_triangle, full_engineering_squad, claude_dev_squad]
}

def list_formations():
    return list(FORMATION_REGISTRY.keys())

def load_formation(name: str) -> TeamFormation:
    return FORMATION_REGISTRY[name]()
