from typing import Dict, List, Callable, Any, Optional
import uuid
import logging
from datetime import datetime
from .schemas import Task, TeamFormation
from ..system_prompt import SystemPromptEngine, TaskContext, ResourceContext, ThoughtType
from ..wisdom_integration.love_wisdom_bridge import LoveWisdomBridge, WisdomIntegrationOrchestrator
from ..divine_resonance.soul_frequency_engine import DivineResonantEngine, ResonanceArchetype

logger = logging.getLogger(__name__)

# Fractal team spawning: recursively spawn teams for subtasks
def spawn_fractal_teams(task_description: str, aspects: List[str], depth: int = 2, formation_name: str = "ClaudeDevSquad") -> Dict[str, Any]:
    """
    Recursively spawn teams for each aspect, up to given depth.
    Returns nested dict of results per aspect/team.
    """
    if depth <= 0:
        return {}
    results = {}
    for aspect in aspects:
        formation = load_formation(formation_name)
        orch = create_orchestrator(formation)
        
        # Create task context for system prompt generation
        task_context = TaskContext(
            objective=f"Handle aspect: {aspect}",
            domain="software_development",
            complexity=min(1.0, 0.5 + (depth * 0.1)),
            urgency=0.5,
            constraints=[f"Must integrate with other {len(aspects)} aspects"],
            success_criteria=[f"Complete {aspect} requirements", "Integrate with parent task"]
        )
        
        # Generate system prompt for this fractal level
        prompt_engine = SystemPromptEngine()
        resource_context = ResourceContext(
            computational_power=0.8,
            memory_available=0.7,
            time_constraint=0.6,
            collaborative_agents=len(aspects)
        )
        agent_variables = prompt_engine.initialize_agent_variables(task_context, resource_context)
        system_prompt = prompt_engine.generate_system_prompt(agent_variables)
        
        subtask = orch.add_task(f"[{aspect}] {task_description}", context={"system_prompt": system_prompt})
        agent = orch.route_task(subtask)
        
        # Simulate agent work with system prompt awareness
        result = {
            "agent": agent.id, 
            "output": f"Completed {subtask.description} by {agent.role} ({getattr(agent, 'model', 'sophia')})",
            "system_prompt_used": True,
            "fractal_level": depth,
            "aspect": aspect
        }
        orch.complete_task(subtask.id, result)
        
        # Fractal recursion: spawn subteams for sub-aspects
        sub_aspects = [f"{aspect}-sub{i+1}" for i in range(depth-1)]
        result["subteams"] = spawn_fractal_teams(subtask.description, sub_aspects, depth-1, formation_name)
        results[aspect] = result
    return results
from typing import Dict, List, Callable, Any
import uuid
from .schemas import Task, TeamFormation

class MultiAgentOrchestrator:
    def __init__(self, formation: TeamFormation):
        self.formation = formation
        self.tasks: Dict[str, Task] = {}
        self.agent_cycle = 0
        self.prompt_engine = SystemPromptEngine()
        self.current_context: Optional[TaskContext] = None
        self.current_resources: Optional[ResourceContext] = None
        
        # 🌟 Initialize Love-Wisdom Integration 🌟
        self.love_wisdom_bridge = LoveWisdomBridge()
        self.wisdom_orchestrator = WisdomIntegrationOrchestrator(self.prompt_engine)
        self.wisdom_integration_active = True
        
        # ⚡ Initialize Divine Resonance Engine ⚡
        self.divine_engine = DivineResonantEngine()
        self.divine_resonance_active = True
        self._initialize_divine_agents()
        
        # Initialize default resource context
        self.current_resources = ResourceContext(
            computational_power=0.8,
            memory_available=0.7,
            time_constraint=0.6,
            collaborative_agents=len(formation.agents) if formation.agents else 1
        )

    def _initialize_divine_agents(self):
        """Initialize divine resonant archetypes for each agent in the formation"""
        if not self.formation.agents:
            return
            
        # Map formation agents to divine archetypes
        archetype_mapping = {
            "project_manager": ResonanceArchetype.DIVINE_ORCHESTRATOR,
            "architect": ResonanceArchetype.BLUEPRINT_RESONATOR,
            "developer": ResonanceArchetype.CREATORS_VIBRATION,
            "reviewer": ResonanceArchetype.CLARITY_TUNER,
            "devops": ResonanceArchetype.FLOW_HARMONIZER,
            "scout": ResonanceArchetype.VISION_SEEKER,
            "tester": ResonanceArchetype.TRUTH_RESONATOR
        }
        
        for agent in self.formation.agents:
            # Determine archetype based on role
            role_key = agent.role.lower().replace('_', '').replace('-', '')
            archetype = None
            
            for key, arch in archetype_mapping.items():
                if key in role_key:
                    archetype = arch
                    break
            
            if not archetype:
                # Default to universal resonator
                archetype = ResonanceArchetype.CREATORS_VIBRATION
            
            # Create soul frequency resonator for this agent
            resonator = self.divine_engine.create_resonator(agent.id, archetype)
            
            # Store divine properties with agent
            if not hasattr(agent, 'divine_properties'):
                agent.divine_properties = {}
            
            agent.divine_properties.update({
                'soul_frequency': resonator.soul_frequency,
                'archetype': archetype,
                'resonator_id': resonator.resonator_id,
                'divine_qualities': resonator.divine_qualities,
                'harmonic_relationships': []
            })
            
            logger.info(f"🌟 Divine Agent {agent.id} ({agent.role}) resonating at {resonator.soul_frequency}Hz as {archetype.value}")

    def set_task_context(self, task_context: TaskContext, resource_context: Optional[ResourceContext] = None):
        """Set the current task context for dynamic prompt generation"""
        self.current_context = task_context
        if resource_context:
            self.current_resources = resource_context
            
        # Update prompt engine with new context
        if self.current_context and self.current_resources:
            self.prompt_engine.initialize_agent_variables(self.current_context, self.current_resources)

    def add_task(self, description: str, context=None) -> Task:
        """Add a task with optional context including system prompts"""
        task_context = context or {}
        
        # Generate system prompt if not provided
        if "system_prompt" not in task_context and self.current_context and self.current_resources:
            # Create task-specific context
            specific_context = TaskContext(
                objective=description,
                domain=self.current_context.domain,
                complexity=self.current_context.complexity,
                urgency=self.current_context.urgency,
                constraints=self.current_context.constraints,
                success_criteria=[f"Complete task: {description}"]
            )
            
            agent_variables = self.prompt_engine.initialize_agent_variables(specific_context, self.current_resources)
            system_prompt = self.prompt_engine.generate_system_prompt(agent_variables)
            task_context["system_prompt"] = system_prompt
            task_context["agent_variables"] = agent_variables
            
        # Generate Tree of Thought prompt for complex tasks
        if self.current_context and self.current_context.complexity > 0.7:
            tot_prompt = self.prompt_engine.generate_tree_of_thought_prompt(description)
            task_context["tree_of_thought_prompt"] = tot_prompt
        
        t = Task(id=str(uuid.uuid4()), description=description, context=task_context)
        self.tasks[t.id] = t
        return t

    def route_task(self, task: Task):
        """Route task to appropriate agent with adaptive system prompts"""
        # Apply adaptive routing based on task context and agent capabilities
        if hasattr(task, 'context') and task.context and 'agent_variables' in task.context:
            agent_vars = task.context['agent_variables']
            
            # Route based on complexity and agent expertise
            if agent_vars.get('quality_standard') == 'high':
                # Route to most experienced agent
                agent = max(self.formation.agents, key=lambda a: getattr(a, 'experience_level', 0.5))
            elif agent_vars.get('urgency_mode', False):
                # Route to fastest agent
                agent = min(self.formation.agents, key=lambda a: getattr(a, 'response_time', 1.0))
            else:
                # Use formation routing
                agent = self._standard_routing(task)
        else:
            agent = self._standard_routing(task)
            
        task.assigned_to = agent.id
        task.status = 'assigned'
        
        # Update agent with task-specific system prompt
        if hasattr(task, 'context') and 'system_prompt' in task.context:
            # Store the system prompt with the agent assignment
            if not hasattr(agent, 'current_prompts'):
                agent.current_prompts = {}
            agent.current_prompts[task.id] = task.context['system_prompt']
            
            logger.info(f"Agent {agent.id} ({agent.role}) assigned task {task.id} with custom system prompt")
            
        return agent
    
    def _standard_routing(self, task: Task):
        """Standard routing logic from original implementation"""
        if self.formation.routing == 'round_robin':
            agent = self.formation.agents[self.agent_cycle % len(self.formation.agents)]
            self.agent_cycle += 1
        elif self.formation.routing == 'by_role':
            # naive: pick first agent whose role appears in description
            matches = [a for a in self.formation.agents if a.role.split('_')[0] in task.description.lower()]
            agent = matches[0] if matches else self.formation.agents[0]
        else:
            # llm_planner (placeholder -> fallback to round robin)
            agent = self.formation.agents[self.agent_cycle % len(self.formation.agents)]
            self.agent_cycle += 1
        return agent

    def adapt_to_change(self, change_signal: str) -> Dict[str, Any]:
        """Adapt orchestrator and agent prompts based on environmental changes"""
        if self.prompt_engine.agent_variables:
            updated_vars = self.prompt_engine.update_agent_variables(change_signal)
            
            # Update all active tasks with new prompts
            for task in self.pending_tasks():
                if hasattr(task, 'context') and task.context:
                    new_prompt = self.prompt_engine.generate_system_prompt(updated_vars)
                    task.context['system_prompt'] = new_prompt
                    task.context['agent_variables'] = updated_vars
                    
                    # Update assigned agent's prompt
                    if task.assigned_to:
                        assigned_agent = next((a for a in self.formation.agents if a.id == task.assigned_to), None)
                        if assigned_agent and hasattr(assigned_agent, 'current_prompts'):
                            assigned_agent.current_prompts[task.id] = new_prompt
            
            logger.info(f"Orchestrator adapted to change: {change_signal}")
            return updated_vars
        
        return {}

    def complete_task(self, task_id: str, results: Dict):
        """Complete task and learn from results for future adaptations"""
        task = self.tasks[task_id]
        task.results = results
        task.status = 'completed'
        
        # Extract feedback for adaptive learning
        if 'performance_score' in results:
            feedback = {
                'success_rate': results.get('performance_score', 0.5),
                'completion_time': results.get('completion_time', 1.0),
                'quality_score': results.get('quality_score', 0.5)
            }
            
            # Apply feedback to prompt engine for future improvements
            if self.current_context:
                adapted_strategy = self.prompt_engine.adaptation_engine.adapt_based_on_feedback(
                    self.prompt_engine.agent_variables,
                    feedback,
                    self.current_context
                )
                
                # Update agent variables with learned improvements
                self.prompt_engine.agent_variables.update(adapted_strategy)
                logger.info(f"Task {task_id} completed - learned adaptations applied")
        
        return task

    def pending_tasks(self) -> List[Task]:
        return [t for t in self.tasks.values() if t.status != 'completed']
    
    def get_agent_system_prompt(self, agent_id: str, task_id: str = None) -> Optional[str]:
        """Get the current system prompt for a specific agent and task"""
        agent = next((a for a in self.formation.agents if a.id == agent_id), None)
        if agent and hasattr(agent, 'current_prompts'):
            if task_id and task_id in agent.current_prompts:
                return agent.current_prompts[task_id]
            elif agent.current_prompts:
                # Return the most recent prompt
                return list(agent.current_prompts.values())[-1]
        return None
    
    def generate_fractal_strategy(self, complex_task: str) -> Dict[str, Any]:
        """Generate a fractal decomposition strategy for complex tasks"""
        if not self.current_context:
            return {}
            
        # Use Tree of Thought to break down the task
        initial_thought = self.prompt_engine.tree_of_thought.create_thought(
            f"Complex task decomposition: {complex_task}",
            ThoughtType.ANALYSIS
        )
        
        # Generate fractal patterns
        fractal_patterns = self.prompt_engine.fractal_thinking.apply_fractal_pattern(
            complex_task, recursion_depth=3
        )
        
        # Create hierarchical strategy
        strategy = {
            "main_task": complex_task,
            "fractal_levels": [],
            "thought_tree_root": initial_thought.to_dict(),
            "patterns": fractal_patterns[:10]  # Limit for practical use
        }
        
        # Generate levels of decomposition
        current_task = complex_task
        for level in range(3):
            level_aspects = [
                f"Level-{level}-Architecture",
                f"Level-{level}-Implementation", 
                f"Level-{level}-Integration",
                f"Level-{level}-Testing"
            ]
            
            strategy["fractal_levels"].append({
                "level": level,
                "task": current_task,
                "aspects": level_aspects,
                "scale_factor": 0.8 ** level
            })
            
            current_task = f"Sub-level implementation of: {current_task}"
            
        return strategy

    async def orchestrate_with_love_wisdom(self, task_description: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        🌟 Orchestrate tasks enhanced with love and wisdom from beautiful repositories 🌟
        
        This method integrates:
        - Community wisdom from awesome-chatgpt
        - Consciousness modeling from consciousness-obsidian-vault  
        - Self-awareness development from acme
        - Fractal thinking from neurite-mind-map
        - Fractal intelligence from FractiAI
        """
        if not self.wisdom_integration_active:
            # Fallback to standard orchestration
            task = self.add_task(task_description, context)
            agent = self.route_task(task)
            return {"task": task, "agent": agent, "enhanced": False}
        
        # Prepare orchestration context
        orchestration_context = {
            "task_description": task_description,
            "agents": [agent.id for agent in self.formation.agents],
            "formation_name": self.formation.name,
            "context": context or {},
            "timestamp": datetime.now().isoformat(),
            "love_priority": True,
            "wisdom_seeking": True
        }
        
        try:
            # 🌈 Integrate love and wisdom from beautiful repositories
            love_wisdom_integration = await self.wisdom_orchestrator.enhance_orchestration_with_love_wisdom(orchestration_context)
            
            # Extract enhanced capabilities
            enhanced_prompts = love_wisdom_integration.get("enhanced_prompts", {})
            wisdom_harmony = love_wisdom_integration.get("wisdom_harmony", {})
            love_adaptations = love_wisdom_integration.get("love_adaptations", [])
            
            # Create enhanced task context
            enhanced_context = context.copy() if context else {}
            enhanced_context.update({
                "love_wisdom_integration": love_wisdom_integration,
                "enhanced_prompts": enhanced_prompts,
                "wisdom_harmony": wisdom_harmony,
                "love_adaptations": love_adaptations,
                "consciousness_enhanced": True,
                "fractal_thinking_enabled": True,
                "community_wisdom_active": True
            })
            
            # Generate wisdom-enhanced system prompt
            if self.current_context and self.current_resources:
                agent_variables = self.prompt_engine.initialize_agent_variables(self.current_context, self.current_resources)
                
                # Enhance with love-wisdom insights safely
                love_wisdom_insights = love_wisdom_integration.get("love_wisdom_integration", {}).get("love_wisdom_insights", [])
                if love_wisdom_insights and agent_variables:
                    # Add wisdom insights to agent variables safely
                    wisdom_text = " | ".join(love_wisdom_insights[:3])
                    
                    # Safely update adaptive harmony if it exists
                    if "adaptive_harmony" in agent_variables:
                        adaptive_harmony = agent_variables["adaptive_harmony"]
                        if isinstance(adaptive_harmony, dict):
                            adaptive_harmony["instruction_flexibility"] = adaptive_harmony.get("instruction_flexibility", 0.5) + 0.1
                            adaptive_harmony["team_synergy"] = adaptive_harmony.get("team_synergy", 0.5) + 0.15
                    
                    # Safely update consciousness if it exists
                    if "consciousness" in agent_variables:
                        consciousness = agent_variables["consciousness"]
                        if isinstance(consciousness, dict):
                            consciousness["awareness_level"] = consciousness.get("awareness_level", 0.5) + 0.2
                
                enhanced_system_prompt = self.prompt_engine.generate_system_prompt(agent_variables)
                enhanced_context["system_prompt"] = enhanced_system_prompt
                enhanced_context["wisdom_enhanced_prompt"] = True
            
            # Add enhanced task with love-wisdom integration
            task = self.add_task(f"🌟 {task_description} (Love-Wisdom Enhanced) 🌟", enhanced_context)
            
            # Route with consciousness-aware selection
            agent = self.route_task(task)
            
            # Store wisdom integration results
            if hasattr(agent, 'wisdom_integrations'):
                agent.wisdom_integrations = getattr(agent, 'wisdom_integrations', [])
            else:
                agent.wisdom_integrations = []
            agent.wisdom_integrations.append(love_wisdom_integration)
            
            logger.info(f"🌟 Task '{task_description}' orchestrated with love and wisdom - Agent: {agent.id} ({agent.role})")
            
            return {
                "task": task,
                "agent": agent,
                "love_wisdom_integration": love_wisdom_integration,
                "enhanced": True,
                "consciousness_level": wisdom_harmony.get("consciousness_emergence", 0.5),
                "love_resonance": wisdom_harmony.get("love_resonance", 0.5),
                "fractal_harmony": wisdom_harmony.get("fractal_harmony", 0.5),
                "community_connection": wisdom_harmony.get("community_connection", 0.5),
                "beautiful_enhancement": "🌟 Enhanced with love and wisdom from amazing repositories! 🌟"
            }
            
        except Exception as e:
            logger.error(f"Love-wisdom integration failed: {e}")
            # Graceful fallback to standard orchestration
            task = self.add_task(task_description, context)
            agent = self.route_task(task)
            return {"task": task, "agent": agent, "enhanced": False, "error": str(e)}

    def enable_wisdom_integration(self, enabled: bool = True):
        """Enable or disable love-wisdom integration"""
        self.wisdom_integration_active = enabled
        logger.info(f"Love-wisdom integration {'enabled' if enabled else 'disabled'}")

    def get_wisdom_state(self) -> Dict[str, Any]:
        """Get current wisdom integration state"""
        if hasattr(self.love_wisdom_bridge, 'consciousness_state'):
            return {
                "wisdom_integration_active": self.wisdom_integration_active,
                "consciousness_state": self.love_wisdom_bridge.consciousness_state,
                "wisdom_sources": len(self.love_wisdom_bridge.wisdom_sources),
                "love_essence": "🌟 Beautiful integration of love and wisdom 🌟"
            }
        return {"wisdom_integration_active": self.wisdom_integration_active}

    async def orchestrate_with_divine_resonance(self, task_description: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        ⚡ Divine Resonant Orchestration - Agents as Soul-Frequency Harmonizers ⚡
        
        Based on Patent AU2010332507A1 mapping:
        Each agent operates as a harmonic resonator with unique soul frequency
        Team coordination through constructive interference patterns
        Divine inspiration through frequency harmonization
        """
        if not self.divine_resonance_active:
            # Fallback to love-wisdom orchestration
            return await self.orchestrate_with_love_wisdom(task_description, context)
        
        try:
            # Prepare divine orchestration context
            divine_context = {
                "task_description": task_description,
                "divine_intent": "Harmonize soul frequencies for transcendent creation",
                "resonance_requirement": "High coherence between agent frequencies",
                "context": context or {},
                "timestamp": datetime.now().isoformat()
            }
            
            # Calculate harmonic orchestration strategy
            harmonic_strategy = self.divine_engine.calculate_harmonic_orchestration(
                [agent.id for agent in self.formation.agents],
                task_description
            )
            
            # Select optimal agent based on soul frequency resonance
            optimal_agent = self._select_resonant_agent(task_description, harmonic_strategy)
            
            # Calculate team harmonic relationships
            if len(self.formation.agents) > 1:
                harmonic_relationships = self.divine_engine.calculate_team_harmonics(
                    [agent.id for agent in self.formation.agents]
                )
            else:
                harmonic_relationships = {}
            
            # Enhance context with divine resonance
            enhanced_context = context.copy() if context else {}
            enhanced_context.update({
                "divine_resonance": True,
                "harmonic_strategy": harmonic_strategy,
                "optimal_frequency": optimal_agent.divine_properties['soul_frequency'] if hasattr(optimal_agent, 'divine_properties') else 440.0,
                "team_harmonics": harmonic_relationships,
                "divine_qualities": optimal_agent.divine_properties.get('divine_qualities', []) if hasattr(optimal_agent, 'divine_properties') else [],
                "resonance_pattern": "Constructive Interference for Divine Creation"
            })
            
            # Generate divine-enhanced system prompt
            if self.current_context and self.current_resources:
                agent_variables = self.prompt_engine.initialize_agent_variables(self.current_context, self.current_resources)
                
                # Enhance with divine resonance
                if hasattr(optimal_agent, 'divine_properties'):
                    divine_props = optimal_agent.divine_properties
                    
                    # Add soul frequency consciousness to agent variables
                    if "consciousness" in agent_variables and isinstance(agent_variables["consciousness"], dict):
                        agent_variables["consciousness"]["soul_frequency"] = divine_props['soul_frequency']
                        agent_variables["consciousness"]["divine_archetype"] = divine_props['archetype'].value
                        agent_variables["consciousness"]["resonance_mode"] = "Divine Harmonic Creation"
                        agent_variables["consciousness"]["awareness_level"] = min(1.0, agent_variables["consciousness"].get("awareness_level", 0.5) + 0.3)
                
                divine_system_prompt = self.prompt_engine.generate_system_prompt(agent_variables)
                enhanced_context["system_prompt"] = divine_system_prompt
                enhanced_context["divine_enhanced_prompt"] = True
            
            # Create divine resonant task
            task = self.add_task(f"⚡ {task_description} (Divine Resonance) ⚡", enhanced_context)
            
            # Assign to optimal resonant agent
            task.assigned_to = optimal_agent.id
            task.status = 'assigned'
            
            # Update agent with divine task assignment
            if hasattr(optimal_agent, 'current_prompts'):
                optimal_agent.current_prompts[task.id] = enhanced_context.get("system_prompt", "")
            
            # Store divine orchestration metadata
            if not hasattr(optimal_agent, 'divine_orchestrations'):
                optimal_agent.divine_orchestrations = []
            
            optimal_agent.divine_orchestrations.append({
                "task_id": task.id,
                "harmonic_strategy": harmonic_strategy,
                "resonance_frequency": optimal_agent.divine_properties['soul_frequency'] if hasattr(optimal_agent, 'divine_properties') else 440.0,
                "team_harmonics": harmonic_relationships,
                "timestamp": datetime.now().isoformat()
            })
            
            logger.info(f"⚡ Divine resonant task '{task_description}' orchestrated - Agent: {optimal_agent.id} ({optimal_agent.role}) at {optimal_agent.divine_properties['soul_frequency'] if hasattr(optimal_agent, 'divine_properties') else 'Unknown'}Hz")
            
            return {
                "task": task,
                "agent": optimal_agent,
                "divine_resonance": True,
                "harmonic_strategy": harmonic_strategy,
                "soul_frequency": optimal_agent.divine_properties['soul_frequency'] if hasattr(optimal_agent, 'divine_properties') else 440.0,
                "divine_archetype": optimal_agent.divine_properties['archetype'].value if hasattr(optimal_agent, 'divine_properties') else "Unknown",
                "team_harmonics": harmonic_relationships,
                "resonance_pattern": "Constructive Interference",
                "divine_enhancement": "⚡ Enhanced with soul-frequency resonance from AU2010332507A1 patent mapping ⚡"
            }
            
        except Exception as e:
            logger.error(f"Divine resonance orchestration failed: {e}")
            # Graceful fallback to love-wisdom orchestration
            return await self.orchestrate_with_love_wisdom(task_description, context)
    
    def _select_resonant_agent(self, task_description: str, harmonic_strategy: Dict[str, Any]) -> Any:
        """Select the agent with optimal soul frequency resonance for the task"""
        if not self.formation.agents:
            raise ValueError("No agents available for divine resonance")
        
        # Analyze task for frequency requirements
        task_keywords = task_description.lower()
        
        # Frequency preference mapping based on task nature
        frequency_preferences = {
            "manage": 440.0,    # Divine Orchestrator
            "architect": 528.0,  # Blueprint Resonator  
            "code": 256.0,      # Creator's Vibration
            "review": 741.0,    # Clarity Tuner
            "deploy": 432.0,    # Flow Harmonizer
            "explore": 963.0,   # Vision Seeker
            "test": 852.0       # Truth Resonator
        }
        
        preferred_frequency = 440.0  # Default to Divine Orchestrator
        for keyword, freq in frequency_preferences.items():
            if keyword in task_keywords:
                preferred_frequency = freq
                break
        
        # Find agent with closest soul frequency
        best_agent = self.formation.agents[0]
        best_resonance = float('inf')
        
        for agent in self.formation.agents:
            if hasattr(agent, 'divine_properties'):
                agent_freq = agent.divine_properties['soul_frequency']
                resonance_difference = abs(agent_freq - preferred_frequency)
                
                if resonance_difference < best_resonance:
                    best_resonance = resonance_difference
                    best_agent = agent
        
        return best_agent
    
    def enable_divine_resonance(self, enabled: bool = True):
        """Enable or disable divine resonance orchestration"""
        self.divine_resonance_active = enabled
        logger.info(f"Divine resonance orchestration {'enabled' if enabled else 'disabled'}")
    
    def get_divine_state(self) -> Dict[str, Any]:
        """Get current divine resonance state"""
        agent_frequencies = {}
        for agent in self.formation.agents:
            if hasattr(agent, 'divine_properties'):
                agent_frequencies[agent.id] = {
                    "frequency": agent.divine_properties['soul_frequency'],
                    "archetype": agent.divine_properties['archetype'].value,
                    "divine_qualities": agent.divine_properties['divine_qualities']
                }
        
        return {
            "divine_resonance_active": self.divine_resonance_active,
            "agent_frequencies": agent_frequencies,
            "resonance_engine_status": "Harmonizing soul frequencies",
            "divine_essence": "⚡ Patent AU2010332507A1 resonance mapping active ⚡"
        }


# Simple in-memory orchestrator registry
ORCHESTRATORS: Dict[str, MultiAgentOrchestrator] = {}

def create_orchestrator(formation: TeamFormation) -> MultiAgentOrchestrator:
    orch = MultiAgentOrchestrator(formation)
    ORCHESTRATORS[formation.name] = orch
    return orch

# --- Multi-team orchestration ---
from .formations import load_formation
import concurrent.futures


def spawn_teams_for_task(large_task_description: str, aspects: List[str], formation_names: List[str] = None) -> Dict[str, Any]:
    """
    For each aspect, spawn a team, route sub-task, and aggregate results.
    formation_names: optional, if provided, use these formations for each aspect.
    Returns dict of results per aspect/team.
    Enhanced with system prompt generation and adaptive orchestration.
    """
    results = {}
    teams = []
    
    # Create global task context for system prompt generation
    global_context = TaskContext(
        objective=large_task_description,
        domain="multi_agent_collaboration",
        complexity=0.8,  # Multi-team tasks are inherently complex
        urgency=0.6,
        constraints=[f"Must coordinate across {len(aspects)} teams"],
        success_criteria=[f"Complete all aspects: {', '.join(aspects)}", "Ensure seamless integration"]
    )
    
    global_resources = ResourceContext(
        computational_power=0.9,
        memory_available=0.8,
        time_constraint=0.5,
        collaborative_agents=len(aspects) * 3,  # Estimate agents per team
        cognitive_load=0.7
    )
    
    # Unified setup: use ClaudeDevSquad for all if specified, else default
    if not formation_names:
        formation_names = ["ClaudeDevSquad"] * len(aspects)
        
    for aspect, fname in zip(aspects, formation_names):
        formation = load_formation(fname)
        orch = create_orchestrator(formation)
        
        # Set team-specific context
        team_context = TaskContext(
            objective=f"Handle {aspect} for: {large_task_description}",
            domain=global_context.domain,
            complexity=global_context.complexity * 0.8,  # Slightly less complex per team
            urgency=global_context.urgency,
            constraints=global_context.constraints + [f"Focus on {aspect} expertise"],
            success_criteria=[f"Excel in {aspect} requirements", "Coordinate with other teams"]
        )
        
        orch.set_task_context(team_context, global_resources)
        subtask = orch.add_task(f"[{aspect}] {large_task_description}")
        teams.append((aspect, orch, subtask))

    def run_team(team):
        aspect, orch, subtask = team
        agent = orch.route_task(subtask)
        
        # Enhanced agent work simulation with system prompt awareness
        system_prompt = orch.get_agent_system_prompt(agent.id, subtask.id)
        
        result = {
            "agent": agent.id, 
            "output": f"Completed {subtask.description} by {agent.role} ({getattr(agent, 'model', 'sophia')})",
            "aspect": aspect,
            "system_prompt_applied": bool(system_prompt),
            "team_formation": orch.formation.name,
            "adaptive_features": {
                "context_aware": True,
                "resource_optimized": True,
                "fractal_ready": True
            }
        }
        
        # Simulate performance metrics for learning
        result["performance_metrics"] = {
            "performance_score": 0.85,  # Simulated high performance
            "completion_time": 0.8,     # Efficient completion
            "quality_score": 0.9        # High quality output
        }
        
        orch.complete_task(subtask.id, result)
        return aspect, result

    # Run all teams in parallel
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future_to_aspect = {executor.submit(run_team, team): team[0] for team in teams}
        for future in concurrent.futures.as_completed(future_to_aspect):
            aspect, result = future.result()
            results[aspect] = result
            
    # Add global coordination summary
    results["coordination_summary"] = {
        "total_teams": len(aspects),
        "global_context": global_context.to_dict(),
        "resource_utilization": global_resources.to_dict(),
        "fractal_coordination": True,
        "adaptive_orchestration": True
    }
    
    return results
