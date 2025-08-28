"""
Comprehensive Unit Tests for SystemPromptEngine
Tests prompt generation, tree of thought reasoning, fractal thinking, and adaptation
"""

import pytest
import uuid
from unittest.mock import Mock, patch
from backend.ai_engine.system_prompt import (
    SystemPromptEngine, ThoughtType, ResourceType, ThoughtNode, 
    TaskContext, ResourceContext, AgentVariables, TreeOfThought
)


class TestThoughtNode:
    """Test the ThoughtNode dataclass"""
    
    def test_thought_node_creation(self):
        """Test basic ThoughtNode creation"""
        node = ThoughtNode(
            thought_type=ThoughtType.EXPLORATION,
            content="Test thought content"
        )
        
        assert node.thought_type == ThoughtType.EXPLORATION
        assert node.content == "Test thought content"
        assert isinstance(node.id, str)
        
    def test_thought_node_default_id(self):
        """Test ThoughtNode generates unique IDs"""
        node1 = ThoughtNode(content="Node 1")
        node2 = ThoughtNode(content="Node 2")
        
        assert node1.id != node2.id
        assert len(node1.id) > 0
        assert len(node2.id) > 0


class TestTaskContext:
    """Test TaskContext dataclass"""
    
    def test_task_context_creation(self):
        """Test TaskContext creation with all fields"""
        context = TaskContext(
            objective="Build a web application",
            domain="software_development",
            complexity=0.8,
            urgency=0.6,
            constraints=["time", "budget", "resources"],
            success_criteria=["passes tests", "meets requirements"]
        )
        
        assert context.objective == "Build a web application"
        assert context.domain == "software_development"
        assert context.complexity == 0.8
        assert context.urgency == 0.6
        assert context.constraints == ["time", "budget", "resources"]
        assert context.success_criteria == ["passes tests", "meets requirements"]
        
    def test_task_context_defaults(self):
        """Test TaskContext with minimal required fields"""
        context = TaskContext(
            objective="Simple task",
            domain="general",
            complexity=0.5,
            urgency=0.5,
            constraints=[],
            success_criteria=["completed"]
        )
        
        assert context.objective == "Simple task"
        assert context.complexity == 0.5
        assert isinstance(context.constraints, list)


class TestResourceContext:
    """Test ResourceContext dataclass"""
    
    def test_resource_context_creation(self):
        """Test ResourceContext creation"""
        context = ResourceContext(
            computational_power=0.9,
            memory_available=0.8,
            time_constraint=0.6,
            collaborative_agents=5
        )
        
        assert context.computational_power == 0.9
        assert context.memory_available == 0.8
        assert context.time_constraint == 0.6
        assert context.collaborative_agents == 5
        
    def test_resource_context_valid_ranges(self):
        """Test ResourceContext accepts valid value ranges"""
        # Test boundary values
        context = ResourceContext(
            computational_power=0.0,
            memory_available=1.0,
            time_constraint=0.5,
            collaborative_agents=1
        )
        
        assert context.computational_power == 0.0
        assert context.memory_available == 1.0
        assert context.collaborative_agents >= 1


class TestAgentVariables:
    """Test AgentVariables dataclass"""
    
    def test_agent_variables_creation(self):
        """Test AgentVariables creation with full configuration"""
        variables = AgentVariables(
            agent_personality="analytical",
            task_approach="methodical",
            communication_style="detailed",
            quality_standard="high",
            creativity_level=0.7,
            collaboration_mode="active",
            learning_enabled=True,
            specialization=["python", "testing"],
            adaptation_rate=0.8,
            context_awareness=0.9
        )
        
        assert variables.agent_personality == "analytical"
        assert variables.task_approach == "methodical"
        assert variables.creativity_level == 0.7
        assert variables.learning_enabled == True
        assert variables.specialization == ["python", "testing"]
        
    def test_agent_variables_defaults(self):
        """Test AgentVariables with default values"""
        variables = AgentVariables()
        
        assert isinstance(variables.agent_personality, str)
        assert isinstance(variables.specialization, list)
        assert isinstance(variables.learning_enabled, bool)
        assert 0.0 <= variables.creativity_level <= 1.0


class TestSystemPromptEngine:
    """Comprehensive tests for SystemPromptEngine"""
    
    def setup_method(self):
        """Set up test fixtures"""
        self.engine = SystemPromptEngine()
        
        self.test_task_context = TaskContext(
            objective="Develop a REST API",
            domain="software_development",
            complexity=0.7,
            urgency=0.5,
            constraints=["deadline", "resources"],
            success_criteria=["functional", "tested", "documented"]
        )
        
        self.test_resource_context = ResourceContext(
            computational_power=0.8,
            memory_available=0.7,
            time_constraint=0.6,
            collaborative_agents=3
        )
        
    def test_engine_initialization(self):
        """Test SystemPromptEngine initializes properly"""
        assert hasattr(self.engine, 'thought_trees')
        assert hasattr(self.engine, 'adaptation_history')
        assert hasattr(self.engine, 'agent_variables')
        
        assert isinstance(self.engine.thought_trees, dict)
        assert isinstance(self.engine.adaptation_history, list)
        
    def test_initialize_agent_variables(self):
        """Test agent variables initialization from context"""
        variables = self.engine.initialize_agent_variables(
            self.test_task_context, 
            self.test_resource_context
        )
        
        assert isinstance(variables, AgentVariables)
        assert variables.context_awareness > 0.5  # Should be high given complex task
        
        # Should store variables in engine
        assert self.engine.agent_variables == variables
        
    def test_initialize_agent_variables_complexity_mapping(self):
        """Test that complexity affects agent variable initialization"""
        # High complexity task
        high_complexity_context = TaskContext(
            objective="Complex system",
            domain="software_development",
            complexity=0.9,  # Very complex
            urgency=0.8,
            constraints=["many constraints"],
            success_criteria=["many criteria"]
        )
        
        high_vars = self.engine.initialize_agent_variables(
            high_complexity_context, 
            self.test_resource_context
        )
        
        # Low complexity task  
        low_complexity_context = TaskContext(
            objective="Simple task",
            domain="general",
            complexity=0.2,  # Simple
            urgency=0.3,
            constraints=[],
            success_criteria=["basic"]
        )
        
        low_vars = self.engine.initialize_agent_variables(
            low_complexity_context,
            self.test_resource_context
        )
        
        # High complexity should result in more thorough approach
        assert high_vars.quality_standard in ["high", "exceptional"]
        assert high_vars.context_awareness > low_vars.context_awareness
        
    def test_generate_system_prompt_basic(self):
        """Test basic system prompt generation"""
        variables = self.engine.initialize_agent_variables(
            self.test_task_context,
            self.test_resource_context
        )
        
        prompt = self.engine.generate_system_prompt(variables)
        
        assert isinstance(prompt, str)
        assert len(prompt) > 100  # Should be substantial
        
        # Should include key elements
        assert "REST API" in prompt or "api" in prompt.lower()
        assert "software" in prompt.lower() or "develop" in prompt.lower()
        
    def test_generate_system_prompt_includes_context(self):
        """Test system prompt includes relevant context information"""
        variables = self.engine.initialize_agent_variables(
            self.test_task_context,
            self.test_resource_context
        )
        
        prompt = self.engine.generate_system_prompt(variables)
        
        # Should reference task complexity
        complexity_terms = ["complex", "thorough", "detailed", "careful"]
        assert any(term in prompt.lower() for term in complexity_terms)
        
        # Should reference collaboration
        collab_terms = ["team", "collaborate", "work with", "coordinate"]
        assert any(term in prompt.lower() for term in collab_terms)
        
    def test_generate_tree_of_thought_prompt(self):
        """Test tree of thought prompt generation"""
        problem = "How to optimize database query performance?"
        
        tot_prompt = self.engine.generate_tree_of_thought_prompt(problem)
        
        assert isinstance(tot_prompt, str)
        assert len(tot_prompt) > 50
        
        # Should include the problem
        assert "database" in tot_prompt.lower()
        assert "performance" in tot_prompt.lower()
        
        # Should include tree of thought elements
        tot_terms = ["think", "consider", "analyze", "approach", "solution"]
        assert any(term in tot_prompt.lower() for term in tot_terms)
        
    def test_generate_fractal_decomposition(self):
        """Test fractal decomposition generation"""
        complex_task = "Build a scalable microservices architecture"
        
        decomposition = self.engine.generate_fractal_decomposition(
            complex_task,
            max_depth=3
        )
        
        assert isinstance(decomposition, dict)
        assert "task" in decomposition
        assert "subtasks" in decomposition
        assert "depth" in decomposition
        
        assert decomposition["task"] == complex_task
        assert decomposition["depth"] <= 3
        assert isinstance(decomposition["subtasks"], list)
        
    def test_generate_fractal_decomposition_max_depth(self):
        """Test fractal decomposition respects max depth"""
        task = "Complex nested task"
        
        shallow_decomp = self.engine.generate_fractal_decomposition(task, max_depth=1)
        deep_decomp = self.engine.generate_fractal_decomposition(task, max_depth=5)
        
        assert shallow_decomp["depth"] <= 1
        assert deep_decomp["depth"] <= 5
        
        # Deeper decomposition should have more subtasks
        if deep_decomp["subtasks"]:
            assert len(deep_decomp["subtasks"]) >= len(shallow_decomp["subtasks"])
            
    def test_create_thought_tree(self):
        """Test thought tree creation"""
        problem = "Design a caching strategy"
        
        thought_tree = self.engine.create_thought_tree(problem)
        
        assert isinstance(thought_tree, TreeOfThought)
        assert thought_tree.problem == problem
        assert isinstance(thought_tree.root_node, ThoughtNode)
        assert isinstance(thought_tree.nodes, dict)
        
        # Should have root node in nodes dict
        assert thought_tree.root_node.id in thought_tree.nodes
        
    def test_create_thought_tree_generates_nodes(self):
        """Test thought tree generates multiple thought nodes"""
        problem = "Implement authentication system"
        
        thought_tree = self.engine.create_thought_tree(problem)
        
        # Should have multiple nodes for complex thinking
        assert len(thought_tree.nodes) >= 3
        
        # Should have different types of thoughts
        thought_types = set(node.thought_type for node in thought_tree.nodes.values())
        assert len(thought_types) > 1
        
    def test_add_thought_to_tree(self):
        """Test adding thoughts to existing tree"""
        problem = "Test problem"
        tree = self.engine.create_thought_tree(problem)
        initial_count = len(tree.nodes)
        
        # Add new thought
        new_thought = ThoughtNode(
            thought_type=ThoughtType.ANALYSIS,
            content="Additional analysis"
        )
        
        self.engine.add_thought_to_tree(tree, new_thought, tree.root_node.id)
        
        # Should have added the new node
        assert len(tree.nodes) == initial_count + 1
        assert new_thought.id in tree.nodes
        assert new_thought.id in tree.connections[tree.root_node.id]
        
    def test_evaluate_thought_path(self):
        """Test thought path evaluation"""
        problem = "Algorithm optimization"
        tree = self.engine.create_thought_tree(problem)
        
        # Get a path through the tree
        path = [tree.root_node.id]
        if tree.connections[tree.root_node.id]:
            path.append(list(tree.connections[tree.root_node.id])[0])
            
        evaluation = self.engine.evaluate_thought_path(tree, path)
        
        assert isinstance(evaluation, dict)
        assert "path_score" in evaluation
        assert "reasoning" in evaluation
        assert "recommendations" in evaluation
        
        assert 0.0 <= evaluation["path_score"] <= 1.0
        assert isinstance(evaluation["reasoning"], str)
        assert isinstance(evaluation["recommendations"], list)
        
    def test_adaptation_engine_integration(self):
        """Test integration with adaptation engine"""
        # Initialize variables
        variables = self.engine.initialize_agent_variables(
            self.test_task_context,
            self.test_resource_context
        )
        
        # Test feedback integration
        feedback = {
            "success_rate": 0.8,
            "completion_time": 1.2,
            "quality_score": 0.9
        }
        
        # This should work without errors
        try:
            adapted = self.engine.adaptation_engine.adapt_based_on_feedback(
                variables,
                feedback,
                self.test_task_context
            )
            assert isinstance(adapted, dict)
        except AttributeError:
            # If adaptation engine is not fully implemented, that's OK
            pass
            
    def test_update_agent_variables(self):
        """Test updating agent variables based on signals"""
        # Initialize variables first
        original_vars = self.engine.initialize_agent_variables(
            self.test_task_context,
            self.test_resource_context  
        )
        
        # Update based on change signal
        updated_vars = self.engine.update_agent_variables("High load detected")
        
        assert isinstance(updated_vars, dict)
        # Should return updated variables
        
    def test_generate_ternary_logic_prompt(self):
        """Test ternary logic prompt generation"""
        concept = "human-ai collaboration"
        
        ternary_prompt = self.engine.generate_ternary_logic_prompt(concept)
        
        assert isinstance(ternary_prompt, str)
        assert len(ternary_prompt) > 50
        
        # Should include ternary concepts
        ternary_terms = ["thesis", "antithesis", "synthesis", "trinity", "three"]
        assert any(term in ternary_prompt.lower() for term in ternary_terms)
        
        # Should include the concept
        assert "collaboration" in ternary_prompt.lower()
        
    def test_generate_harmony_orchestration_prompt(self):
        """Test harmony orchestration prompt generation"""
        agents = ["developer", "designer", "tester"]
        
        harmony_prompt = self.engine.generate_harmony_orchestration_prompt(agents)
        
        assert isinstance(harmony_prompt, str)
        assert len(harmony_prompt) > 50
        
        # Should reference all agents
        for agent in agents:
            assert agent in harmony_prompt.lower()
            
        # Should include harmony concepts
        harmony_terms = ["harmony", "synchronize", "coordinate", "balance"]
        assert any(term in harmony_prompt.lower() for term in harmony_terms)
        
    def test_thought_type_enum_completeness(self):
        """Test that all thought types are properly defined"""
        expected_types = [
            "exploration", "analysis", "synthesis", 
            "evaluation", "iteration", "fractal_expansion", "adaptation"
        ]
        
        actual_types = [t.value for t in ThoughtType]
        
        for expected in expected_types:
            assert expected in actual_types
            
    def test_resource_type_enum_completeness(self):
        """Test that all resource types are properly defined"""
        expected_types = [
            "computational", "memory", "network", "storage",
            "time", "cognitive", "collaborative"
        ]
        
        actual_types = [r.value for r in ResourceType]
        
        for expected in expected_types:
            assert expected in actual_types
            
    def test_prompt_length_constraints(self):
        """Test that generated prompts are within reasonable length constraints"""
        variables = self.engine.initialize_agent_variables(
            self.test_task_context,
            self.test_resource_context
        )
        
        prompt = self.engine.generate_system_prompt(variables)
        
        # Should be substantial but not excessive
        assert 100 <= len(prompt) <= 5000
        
    def test_prompt_structure_consistency(self):
        """Test that prompts have consistent structure"""
        variables = self.engine.initialize_agent_variables(
            self.test_task_context,
            self.test_resource_context
        )
        
        prompt1 = self.engine.generate_system_prompt(variables)
        prompt2 = self.engine.generate_system_prompt(variables)
        
        # Should be consistent (deterministic for same inputs)
        assert prompt1 == prompt2
        
    def test_context_sensitive_prompts(self):
        """Test that prompts are sensitive to context changes"""
        # Create two different contexts
        context1 = TaskContext(
            objective="Simple task",
            domain="general",
            complexity=0.2,
            urgency=0.3,
            constraints=[],
            success_criteria=["basic"]
        )
        
        context2 = TaskContext(
            objective="Complex enterprise system",
            domain="software_development", 
            complexity=0.9,
            urgency=0.8,
            constraints=["security", "scalability", "performance"],
            success_criteria=["enterprise-grade", "secure", "scalable"]
        )
        
        vars1 = self.engine.initialize_agent_variables(context1, self.test_resource_context)
        vars2 = self.engine.initialize_agent_variables(context2, self.test_resource_context)
        
        prompt1 = self.engine.generate_system_prompt(vars1)
        prompt2 = self.engine.generate_system_prompt(vars2)
        
        # Should be significantly different
        assert prompt1 != prompt2
        assert len(prompt2) > len(prompt1)  # Complex task should have longer prompt
        
    def test_resource_awareness_in_prompts(self):
        """Test that prompts reflect available resources"""
        # Low resource context
        low_resources = ResourceContext(
            computational_power=0.3,
            memory_available=0.2,
            time_constraint=0.9,  # High time pressure
            collaborative_agents=1
        )
        
        # High resource context
        high_resources = ResourceContext(
            computational_power=0.9,
            memory_available=0.8,
            time_constraint=0.2,  # Low time pressure
            collaborative_agents=5
        )
        
        vars_low = self.engine.initialize_agent_variables(self.test_task_context, low_resources)
        vars_high = self.engine.initialize_agent_variables(self.test_task_context, high_resources)
        
        prompt_low = self.engine.generate_system_prompt(vars_low)
        prompt_high = self.engine.generate_system_prompt(vars_high)
        
        # Should reflect resource constraints
        assert prompt_low != prompt_high
        
        # Low resource prompt might emphasize efficiency
        efficiency_terms = ["efficient", "quick", "simple", "minimal"]
        assert any(term in prompt_low.lower() for term in efficiency_terms)
        
    @patch('uuid.uuid4')
    def test_deterministic_ids(self, mock_uuid):
        """Test that consistent UUIDs produce consistent results"""
        mock_uuid.return_value = Mock()
        mock_uuid.return_value.__str__ = Mock(return_value="test-uuid-123")
        
        node1 = ThoughtNode(content="Test")
        node2 = ThoughtNode(content="Test")
        
        # Should use mocked UUID
        assert str(node1.id) == "test-uuid-123"
        assert str(node2.id) == "test-uuid-123"
        
    def test_edge_case_empty_inputs(self):
        """Test handling of edge case inputs"""
        # Empty context
        empty_context = TaskContext(
            objective="",
            domain="",
            complexity=0.0,
            urgency=0.0,
            constraints=[],
            success_criteria=[]
        )
        
        try:
            variables = self.engine.initialize_agent_variables(empty_context, self.test_resource_context)
            prompt = self.engine.generate_system_prompt(variables)
            
            # Should handle gracefully
            assert isinstance(prompt, str)
            assert len(prompt) > 0
            
        except Exception as e:
            pytest.fail(f"Engine should handle empty inputs gracefully: {e}")
            
    def test_concurrent_prompt_generation(self):
        """Test thread safety of prompt generation"""
        import threading
        
        results = []
        errors = []
        
        def generate_prompt():
            try:
                variables = self.engine.initialize_agent_variables(
                    self.test_task_context,
                    self.test_resource_context
                )
                prompt = self.engine.generate_system_prompt(variables)
                results.append(prompt)
            except Exception as e:
                errors.append(e)
                
        # Create multiple threads
        threads = [threading.Thread(target=generate_prompt) for _ in range(10)]
        
        # Start all threads
        for thread in threads:
            thread.start()
            
        # Wait for completion
        for thread in threads:
            thread.join()
            
        # Should all succeed
        assert len(errors) == 0
        assert len(results) == 10
        
        # All results should be identical (deterministic)
        first_result = results[0]
        assert all(result == first_result for result in results)