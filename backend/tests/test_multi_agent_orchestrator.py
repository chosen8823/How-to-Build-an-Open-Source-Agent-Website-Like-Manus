"""
Comprehensive Unit Tests for MultiAgentOrchestrator
Tests task management, agent routing, system prompt integration, and divine resonance
"""

import pytest
import uuid
from unittest.mock import Mock, patch, MagicMock
from backend.ai_engine.orchestrator.orchestrator import (
    MultiAgentOrchestrator, spawn_fractal_teams
)
from backend.ai_engine.orchestrator.schemas import Task, TeamFormation, Agent
from backend.ai_engine.system_prompt import TaskContext, ResourceContext, SystemPromptEngine


class TestMultiAgentOrchestrator:
    """Comprehensive tests for the multi-agent orchestration system"""
    
    def setup_method(self):
        """Set up test fixtures"""
        # Create test agents
        self.test_agents = [
            Agent(id="agent_1", role="project_manager", model="sophia_pm"),
            Agent(id="agent_2", role="developer", model="sophia_dev"),
            Agent(id="agent_3", role="reviewer", model="sophia_review")
        ]
        
        # Create test formation
        self.test_formation = TeamFormation(
            name="test_team",
            agents=self.test_agents,
            routing="round_robin"
        )
        
        # Initialize orchestrator
        with patch('backend.ai_engine.orchestrator.orchestrator.LoveWisdomBridge'):
            with patch('backend.ai_engine.orchestrator.orchestrator.WisdomIntegrationOrchestrator'):
                with patch('backend.ai_engine.orchestrator.orchestrator.DivineResonantEngine'):
                    self.orchestrator = MultiAgentOrchestrator(self.test_formation)
                    
    def test_orchestrator_initialization(self):
        """Test orchestrator initializes properly"""
        assert self.orchestrator.formation == self.test_formation
        assert isinstance(self.orchestrator.tasks, dict)
        assert len(self.orchestrator.tasks) == 0
        assert self.orchestrator.agent_cycle == 0
        
        # Test component initialization
        assert hasattr(self.orchestrator, 'prompt_engine')
        assert hasattr(self.orchestrator, 'love_wisdom_bridge')
        assert hasattr(self.orchestrator, 'wisdom_orchestrator')
        assert hasattr(self.orchestrator, 'divine_engine')
        
        # Test boolean flags
        assert self.orchestrator.wisdom_integration_active == True
        assert self.orchestrator.divine_resonance_active == True
        
    def test_initialization_without_agents(self):
        """Test orchestrator initialization with empty agent list"""
        empty_formation = TeamFormation(
            name="empty_team",
            agents=[],
            routing="round_robin"
        )
        
        with patch('backend.ai_engine.orchestrator.orchestrator.LoveWisdomBridge'):
            with patch('backend.ai_engine.orchestrator.orchestrator.WisdomIntegrationOrchestrator'):
                with patch('backend.ai_engine.orchestrator.orchestrator.DivineResonantEngine'):
                    orchestrator = MultiAgentOrchestrator(empty_formation)
                    
        assert orchestrator.formation == empty_formation
        assert isinstance(orchestrator.tasks, dict)
        
    @patch('backend.ai_engine.orchestrator.orchestrator.DivineResonantEngine')
    def test_divine_agents_initialization(self, mock_divine_engine):
        """Test initialization of divine resonant agents"""
        mock_engine_instance = Mock()
        mock_divine_engine.return_value = mock_engine_instance
        
        mock_resonator = Mock()
        mock_resonator.soul_frequency = 528.0
        mock_resonator.resonator_id = "test_resonator"
        mock_resonator.divine_qualities = ["love", "wisdom"]
        
        mock_engine_instance.create_resonator.return_value = mock_resonator
        
        with patch('backend.ai_engine.orchestrator.orchestrator.LoveWisdomBridge'):
            with patch('backend.ai_engine.orchestrator.orchestrator.WisdomIntegrationOrchestrator'):
                orchestrator = MultiAgentOrchestrator(self.test_formation)
                
        # Should have created resonators for each agent
        assert mock_engine_instance.create_resonator.call_count == len(self.test_agents)
        
        # Check that agents have divine properties
        for agent in self.test_formation.agents:
            assert hasattr(agent, 'divine_properties')
            assert 'soul_frequency' in agent.divine_properties
            assert 'archetype' in agent.divine_properties
            
    def test_set_task_context(self):
        """Test setting task context for dynamic prompts"""
        task_context = TaskContext(
            objective="Test objective",
            domain="software_development",
            complexity=0.8,
            urgency=0.6,
            constraints=["time", "resources"],
            success_criteria=["criterion1", "criterion2"]
        )
        
        resource_context = ResourceContext(
            computational_power=0.9,
            memory_available=0.8,
            time_constraint=0.5,
            collaborative_agents=3
        )
        
        self.orchestrator.set_task_context(task_context, resource_context)
        
        assert self.orchestrator.current_context == task_context
        assert self.orchestrator.current_resources == resource_context
        
    def test_set_task_context_without_resources(self):
        """Test setting task context without resource context"""
        task_context = TaskContext(
            objective="Test objective",
            domain="software_development",
            complexity=0.5,
            urgency=0.5,
            constraints=[],
            success_criteria=["success"]
        )
        
        original_resources = self.orchestrator.current_resources
        
        self.orchestrator.set_task_context(task_context)
        
        assert self.orchestrator.current_context == task_context
        assert self.orchestrator.current_resources == original_resources
        
    def test_add_task_basic(self):
        """Test basic task addition"""
        description = "Test task description"
        
        task = self.orchestrator.add_task(description)
        
        assert isinstance(task, Task)
        assert task.description == description
        assert task.id in self.orchestrator.tasks
        assert self.orchestrator.tasks[task.id] == task
        
    def test_add_task_with_context(self):
        """Test adding task with custom context"""
        description = "Test task with context"
        context = {"custom_key": "custom_value", "system_prompt": "Custom prompt"}
        
        task = self.orchestrator.add_task(description, context)
        
        assert task.context == context
        assert task.context["system_prompt"] == "Custom prompt"
        
    @patch('backend.ai_engine.orchestrator.orchestrator.SystemPromptEngine')
    def test_add_task_generates_system_prompt(self, mock_prompt_engine_class):
        """Test that tasks generate system prompts when context is set"""
        mock_prompt_engine = Mock()
        mock_prompt_engine_class.return_value = mock_prompt_engine
        mock_prompt_engine.initialize_agent_variables.return_value = {"test": "variables"}
        mock_prompt_engine.generate_system_prompt.return_value = "Generated prompt"
        
        # Set task context
        task_context = TaskContext(
            objective="Test",
            domain="test",
            complexity=0.5,
            urgency=0.5,
            constraints=[],
            success_criteria=["success"]
        )
        self.orchestrator.set_task_context(task_context)
        
        task = self.orchestrator.add_task("Test task")
        
        assert "system_prompt" in task.context
        assert task.context["system_prompt"] == "Generated prompt"
        assert "agent_variables" in task.context
        
    @patch('backend.ai_engine.orchestrator.orchestrator.SystemPromptEngine')
    def test_add_task_tree_of_thought_complex(self, mock_prompt_engine_class):
        """Test tree of thought prompt generation for complex tasks"""
        mock_prompt_engine = Mock()
        mock_prompt_engine_class.return_value = mock_prompt_engine
        mock_prompt_engine.initialize_agent_variables.return_value = {"test": "variables"}
        mock_prompt_engine.generate_system_prompt.return_value = "Generated prompt"
        mock_prompt_engine.generate_tree_of_thought_prompt.return_value = "ToT prompt"
        
        # Set high complexity task context
        task_context = TaskContext(
            objective="Complex task",
            domain="test",
            complexity=0.8,  # High complexity
            urgency=0.5,
            constraints=[],
            success_criteria=["success"]
        )
        self.orchestrator.set_task_context(task_context)
        
        task = self.orchestrator.add_task("Complex test task")
        
        assert "tree_of_thought_prompt" in task.context
        assert task.context["tree_of_thought_prompt"] == "ToT prompt"
        
    def test_route_task_round_robin(self):
        """Test round-robin task routing"""
        tasks = []
        assigned_agents = []
        
        # Create multiple tasks
        for i in range(5):
            task = self.orchestrator.add_task(f"Task {i}")
            agent = self.orchestrator.route_task(task)
            tasks.append(task)
            assigned_agents.append(agent)
            
        # Should cycle through agents
        expected_agents = [
            self.test_agents[0], self.test_agents[1], self.test_agents[2],
            self.test_agents[0], self.test_agents[1]  # Cycle repeats
        ]
        
        assert assigned_agents == expected_agents
        
        # Tasks should be marked as assigned
        for task in tasks:
            assert task.status == 'assigned'
            
    def test_route_task_by_role(self):
        """Test role-based task routing"""
        # Create formation with role-based routing
        role_formation = TeamFormation(
            name="role_team",
            agents=self.test_agents,
            routing="by_role"
        )
        
        with patch('backend.ai_engine.orchestrator.orchestrator.LoveWisdomBridge'):
            with patch('backend.ai_engine.orchestrator.orchestrator.WisdomIntegrationOrchestrator'):
                with patch('backend.ai_engine.orchestrator.orchestrator.DivineResonantEngine'):
                    orchestrator = MultiAgentOrchestrator(role_formation)
        
        # Task mentioning "develop" should go to developer
        task = orchestrator.add_task("develop a new feature")
        agent = orchestrator.route_task(task)
        
        assert agent.role == "developer"
        
    def test_route_task_adaptive_quality(self):
        """Test adaptive routing based on quality requirements"""
        # Add experience levels to agents
        self.test_agents[0].experience_level = 0.9  # High experience
        self.test_agents[1].experience_level = 0.7  # Medium experience
        self.test_agents[2].experience_level = 0.5  # Lower experience
        
        # Create task with high quality requirement
        task = self.orchestrator.add_task("Critical task", {
            "agent_variables": {"quality_standard": "high"}
        })
        
        agent = self.orchestrator.route_task(task)
        
        # Should route to most experienced agent
        assert agent.experience_level == 0.9
        
    def test_route_task_adaptive_urgency(self):
        """Test adaptive routing based on urgency"""
        # Add response times to agents
        self.test_agents[0].response_time = 1.0  # Slow
        self.test_agents[1].response_time = 0.5  # Medium
        self.test_agents[2].response_time = 0.3  # Fast
        
        # Create urgent task
        task = self.orchestrator.add_task("Urgent task", {
            "agent_variables": {"urgency_mode": True}
        })
        
        agent = self.orchestrator.route_task(task)
        
        # Should route to fastest agent
        assert agent.response_time == 0.3
        
    def test_complete_task(self):
        """Test task completion"""
        task = self.orchestrator.add_task("Test task")
        results = {
            "output": "Task completed successfully",
            "performance_score": 0.9,
            "completion_time": 0.5,
            "quality_score": 0.85
        }
        
        completed_task = self.orchestrator.complete_task(task.id, results)
        
        assert completed_task.status == 'completed'
        assert completed_task.results == results
        
    def test_complete_task_with_learning(self):
        """Test task completion with adaptive learning"""
        # Set up context for learning
        task_context = TaskContext(
            objective="Learning task",
            domain="test",
            complexity=0.6,
            urgency=0.4,
            constraints=[],
            success_criteria=["success"]
        )
        self.orchestrator.set_task_context(task_context)
        
        task = self.orchestrator.add_task("Learning task")
        results = {
            "performance_score": 0.8,
            "completion_time": 1.2,
            "quality_score": 0.75
        }
        
        with patch.object(self.orchestrator.prompt_engine, 'adaptation_engine') as mock_adaptation:
            mock_adaptation.adapt_based_on_feedback.return_value = {"learned": "improvement"}
            
            completed_task = self.orchestrator.complete_task(task.id, results)
            
            assert completed_task.status == 'completed'
            mock_adaptation.adapt_based_on_feedback.assert_called_once()
            
    def test_pending_tasks(self):
        """Test getting pending tasks"""
        # Add some tasks
        task1 = self.orchestrator.add_task("Task 1")
        task2 = self.orchestrator.add_task("Task 2")
        task3 = self.orchestrator.add_task("Task 3")
        
        # Complete one task
        self.orchestrator.complete_task(task2.id, {"result": "done"})
        
        pending = self.orchestrator.pending_tasks()
        
        assert len(pending) == 2
        assert task1 in pending
        assert task3 in pending
        assert task2 not in pending
        
    def test_get_agent_system_prompt(self):
        """Test retrieving agent system prompts"""
        # Set up agent with prompts
        agent = self.test_agents[0]
        agent.current_prompts = {
            "task1": "Prompt for task 1",
            "task2": "Prompt for task 2"
        }
        
        # Get specific task prompt
        prompt = self.orchestrator.get_agent_system_prompt(agent.id, "task1")
        assert prompt == "Prompt for task 1"
        
        # Get most recent prompt
        recent_prompt = self.orchestrator.get_agent_system_prompt(agent.id)
        assert recent_prompt == "Prompt for task 2"  # Most recent
        
    def test_get_agent_system_prompt_no_prompts(self):
        """Test retrieving system prompt when agent has no prompts"""
        agent = self.test_agents[0]
        
        prompt = self.orchestrator.get_agent_system_prompt(agent.id, "nonexistent")
        assert prompt is None
        
    def test_get_agent_system_prompt_nonexistent_agent(self):
        """Test retrieving system prompt for nonexistent agent"""
        prompt = self.orchestrator.get_agent_system_prompt("nonexistent_agent", "task1")
        assert prompt is None
        
    def test_adapt_to_change(self):
        """Test orchestrator adaptation to environmental changes"""
        # Set up context and add tasks
        task_context = TaskContext(
            objective="Adaptable task",
            domain="test",
            complexity=0.5,
            urgency=0.5,
            constraints=[],
            success_criteria=["success"]
        )
        self.orchestrator.set_task_context(task_context)
        
        task1 = self.orchestrator.add_task("Task 1")
        task2 = self.orchestrator.add_task("Task 2")
        
        # Route tasks to agents
        agent1 = self.orchestrator.route_task(task1)
        agent2 = self.orchestrator.route_task(task2)
        
        with patch.object(self.orchestrator.prompt_engine, 'update_agent_variables') as mock_update:
            mock_update.return_value = {"adapted": "variables"}
            
            with patch.object(self.orchestrator.prompt_engine, 'generate_system_prompt') as mock_generate:
                mock_generate.return_value = "Adapted prompt"
                
                # Simulate adaptation
                result = self.orchestrator.adapt_to_change("High load detected")
                
                assert result == {"adapted": "variables"}
                mock_update.assert_called_with("High load detected")
                
                # Tasks should have updated prompts
                assert task1.context["system_prompt"] == "Adapted prompt"
                assert task2.context["system_prompt"] == "Adapted prompt"
                
    def test_generate_fractal_strategy(self):
        """Test fractal strategy generation for complex tasks"""
        # Set up complex task context
        complex_context = TaskContext(
            objective="Complex fractal task",
            domain="software_development",
            complexity=0.9,  # Very complex
            urgency=0.7,
            constraints=["time", "resources", "quality"],
            success_criteria=["criterion1", "criterion2", "criterion3"]
        )
        self.orchestrator.set_task_context(complex_context)
        
        with patch.object(self.orchestrator.prompt_engine, 'generate_fractal_decomposition') as mock_fractal:
            mock_fractal.return_value = {
                "decomposition_strategy": "recursive_breakdown",
                "levels": 3,
                "aspects": ["aspect1", "aspect2", "aspect3"]
            }
            
            strategy = self.orchestrator.generate_fractal_strategy("Build complex system")
            
            assert "decomposition_strategy" in strategy
            mock_fractal.assert_called_once()
            
    def test_agent_cycle_increment(self):
        """Test that agent cycle increments properly"""
        initial_cycle = self.orchestrator.agent_cycle
        
        # Route several tasks
        for i in range(3):
            task = self.orchestrator.add_task(f"Task {i}")
            self.orchestrator.route_task(task)
            
        # Cycle should have incremented
        assert self.orchestrator.agent_cycle == initial_cycle + 3
        
    def test_task_id_uniqueness(self):
        """Test that task IDs are unique"""
        task_ids = set()
        
        # Create many tasks
        for i in range(100):
            task = self.orchestrator.add_task(f"Task {i}")
            assert task.id not in task_ids
            task_ids.add(task.id)
            
        assert len(task_ids) == 100
        
    def test_resource_context_defaults(self):
        """Test default resource context initialization"""
        assert self.orchestrator.current_resources is not None
        
        resources = self.orchestrator.current_resources
        assert resources.computational_power == 0.8
        assert resources.memory_available == 0.7
        assert resources.time_constraint == 0.6
        assert resources.collaborative_agents == len(self.test_formation.agents)


class TestSpawnFractalTeams:
    """Tests for the fractal team spawning functionality"""
    
    @patch('backend.ai_engine.orchestrator.orchestrator.load_formation')
    @patch('backend.ai_engine.orchestrator.orchestrator.create_orchestrator')
    def test_spawn_fractal_teams_basic(self, mock_create_orch, mock_load_formation):
        """Test basic fractal team spawning"""
        # Mock formation and orchestrator
        mock_formation = Mock()
        mock_load_formation.return_value = mock_formation
        
        mock_orch = Mock()
        mock_agent = Mock()
        mock_agent.id = "test_agent"
        mock_agent.role = "test_role"
        mock_task = Mock()
        mock_task.description = "Test task"
        mock_task.id = "test_task_id"
        
        mock_orch.add_task.return_value = mock_task
        mock_orch.route_task.return_value = mock_agent
        mock_create_orch.return_value = mock_orch
        
        # Test spawning
        result = spawn_fractal_teams(
            task_description="Test fractal task",
            aspects=["aspect1", "aspect2"],
            depth=2,
            formation_name="TestFormation"
        )
        
        assert isinstance(result, dict)
        assert "aspect1" in result
        assert "aspect2" in result
        
        # Should create orchestrators for each aspect
        assert mock_create_orch.call_count == 2
        
    @patch('backend.ai_engine.orchestrator.orchestrator.load_formation')
    @patch('backend.ai_engine.orchestrator.orchestrator.create_orchestrator')
    def test_spawn_fractal_teams_zero_depth(self, mock_create_orch, mock_load_formation):
        """Test fractal team spawning with zero depth"""
        result = spawn_fractal_teams(
            task_description="Test task",
            aspects=["aspect1"],
            depth=0
        )
        
        assert result == {}
        assert mock_create_orch.call_count == 0
        
    @patch('backend.ai_engine.orchestrator.orchestrator.load_formation')
    @patch('backend.ai_engine.orchestrator.orchestrator.create_orchestrator')
    def test_spawn_fractal_teams_recursive(self, mock_create_orch, mock_load_formation):
        """Test recursive fractal team spawning"""
        # Setup mocks
        mock_formation = Mock()
        mock_load_formation.return_value = mock_formation
        
        mock_orch = Mock()
        mock_agent = Mock()
        mock_agent.id = "test_agent"
        mock_agent.role = "test_role"
        mock_task = Mock()
        mock_task.description = "Test task"
        mock_task.id = "test_task_id"
        
        mock_orch.add_task.return_value = mock_task
        mock_orch.route_task.return_value = mock_agent
        mock_create_orch.return_value = mock_orch
        
        result = spawn_fractal_teams(
            task_description="Test fractal task",
            aspects=["aspect1"],
            depth=3
        )
        
        # Should create nested structure
        assert "aspect1" in result
        assert "subteams" in result["aspect1"]
        
        # Should have called create_orchestrator multiple times for recursion
        assert mock_create_orch.call_count > 1
        
    def test_spawn_fractal_teams_empty_aspects(self):
        """Test fractal team spawning with empty aspects list"""
        result = spawn_fractal_teams(
            task_description="Test task",
            aspects=[],
            depth=2
        )
        
        assert result == {}
        
    @patch('backend.ai_engine.orchestrator.orchestrator.SystemPromptEngine')
    @patch('backend.ai_engine.orchestrator.orchestrator.load_formation')
    @patch('backend.ai_engine.orchestrator.orchestrator.create_orchestrator')
    def test_spawn_fractal_teams_with_prompts(self, mock_create_orch, mock_load_formation, mock_prompt_engine_class):
        """Test fractal team spawning includes system prompt generation"""
        # Setup mocks
        mock_formation = Mock()
        mock_load_formation.return_value = mock_formation
        
        mock_orch = Mock()
        mock_agent = Mock()
        mock_agent.id = "test_agent"
        mock_agent.role = "test_role"
        mock_task = Mock()
        mock_task.description = "Test task"
        mock_task.id = "test_task_id"
        
        mock_orch.add_task.return_value = mock_task
        mock_orch.route_task.return_value = mock_agent
        mock_orch.complete_task.return_value = mock_task
        mock_create_orch.return_value = mock_orch
        
        # Mock prompt engine
        mock_prompt_engine = Mock()
        mock_prompt_engine_class.return_value = mock_prompt_engine
        mock_prompt_engine.initialize_agent_variables.return_value = {"test": "vars"}
        mock_prompt_engine.generate_system_prompt.return_value = "Test prompt"
        
        result = spawn_fractal_teams(
            task_description="Test fractal task",
            aspects=["aspect1"],
            depth=1
        )
        
        # Should include system prompt generation
        mock_prompt_engine.generate_system_prompt.assert_called()
        
        # Result should include system prompt usage
        assert result["aspect1"]["system_prompt_used"] == True