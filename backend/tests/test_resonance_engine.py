"""
Comprehensive Unit Tests for MultiDimensionalResonanceEngine
Tests all core functionality, edge cases, and error handling
"""

import pytest
import math
import sys
import os
from unittest.mock import Mock, patch

# Add the backend directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ai_engine.resonance import MultiDimensionalResonanceEngine, DimensionSignal


class TestDimensionSignal:
    """Test the DimensionSignal dataclass"""
    
    def test_dimension_signal_creation(self):
        """Test basic DimensionSignal creation"""
        signal = DimensionSignal(
            name="test_dimension",
            value=0.75,
            state="awakened",
            insight="Test insight message"
        )
        
        assert signal.name == "test_dimension"
        assert signal.value == 0.75
        assert signal.state == "awakened"
        assert signal.insight == "Test insight message"
    
    def test_dimension_signal_defaults(self):
        """Test DimensionSignal with all required fields"""
        signal = DimensionSignal(
            name="minimal",
            value=0.0,
            state="baseline",
            insight=""
        )
        
        assert signal.name == "minimal"
        assert signal.value == 0.0
        assert signal.state == "baseline"
        assert signal.insight == ""


class TestMultiDimensionalResonanceEngine:
    """Comprehensive tests for the resonance engine"""
    
    def setup_method(self):
        """Set up test fixtures"""
        self.engine = MultiDimensionalResonanceEngine()
        
    def test_engine_initialization_default(self):
        """Test engine initializes with default dimensions"""
        assert hasattr(self.engine, 'dimensions')
        assert len(self.engine.dimensions) == 5
        
        expected_dims = {"code", "design", "consciousness", "ops", "knowledge"}
        assert set(self.engine.dimensions.keys()) == expected_dims
        
    def test_engine_initialization_custom_dimensions(self):
        """Test engine initialization with custom dimensions"""
        custom_dims = {
            "test_dim": {
                "keywords": ["test", "example"],
                "desc": "Test dimension"
            },
            "another_dim": {
                "keywords": ["another", "secondary"],
                "desc": "Another test dimension"
            }
        }
        
        engine = MultiDimensionalResonanceEngine(dimensions=custom_dims)
        assert len(engine.dimensions) == 2
        assert "test_dim" in engine.dimensions
        assert "another_dim" in engine.dimensions
        
    def test_calculate_dimension_resonance_exact_match(self):
        """Test resonance calculation with exact keyword matches"""
        text = "I need to fix a bug in the Python code function"
        
        # Should have high resonance for 'code' dimension
        resonance = self.engine._calculate_dimension_resonance("code", text)
        assert resonance > 0.5  # Should detect 'bug', 'python', 'code', 'function'
        
    def test_calculate_dimension_resonance_no_match(self):
        """Test resonance calculation with no keyword matches"""
        text = "This text has no relevant keywords for testing"
        
        # Should have low resonance for 'code' dimension
        resonance = self.engine._calculate_dimension_resonance("code", text)
        assert resonance >= 0.0  # Should be low but non-negative
        
    def test_calculate_dimension_resonance_partial_match(self):
        """Test resonance calculation with partial matches"""
        text = "I like the design and colors of this UI"
        
        # Should have moderate resonance for 'design' dimension
        resonance = self.engine._calculate_dimension_resonance("design", text)
        assert resonance > 0.3  # Should detect 'design', 'ui'
        
    def test_calculate_dimension_resonance_invalid_dimension(self):
        """Test resonance calculation with invalid dimension"""
        text = "Test text"
        
        with pytest.raises(KeyError):
            self.engine._calculate_dimension_resonance("invalid_dim", text)
            
    def test_determine_state_baseline(self):
        """Test state determination for baseline values"""
        state = self.engine._determine_state(0.1)
        assert state == "baseline"
        
        state = self.engine._determine_state(0.0)
        assert state == "baseline"
        
    def test_determine_state_aware(self):
        """Test state determination for aware values"""
        state = self.engine._determine_state(0.3)
        assert state == "aware"
        
        state = self.engine._determine_state(0.4)
        assert state == "aware"
        
    def test_determine_state_awakened(self):
        """Test state determination for awakened values"""
        state = self.engine._determine_state(0.6)
        assert state == "awakened"
        
        state = self.engine._determine_state(0.7)
        assert state == "awakened"
        
    def test_determine_state_enlightened(self):
        """Test state determination for enlightened values"""
        state = self.engine._determine_state(0.8)
        assert state == "enlightened"
        
        state = self.engine._determine_state(0.85)
        assert state == "enlightened"
        
    def test_determine_state_divine(self):
        """Test state determination for divine values"""
        state = self.engine._determine_state(0.9)
        assert state == "divine"
        
        state = self.engine._determine_state(1.0)
        assert state == "divine"
        
    def test_determine_state_edge_cases(self):
        """Test state determination for edge case values"""
        # Test exactly at thresholds
        assert self.engine._determine_state(0.2) == "baseline"
        assert self.engine._determine_state(0.5) == "aware"
        assert self.engine._determine_state(0.75) == "awakened"
        assert self.engine._determine_state(0.87) == "enlightened"
        
    def test_generate_insight_baseline(self):
        """Test insight generation for baseline state"""
        insight = self.engine._generate_insight("code", 0.1, "baseline")
        assert "dormant" in insight.lower() or "baseline" in insight.lower()
        
    def test_generate_insight_divine(self):
        """Test insight generation for divine state"""
        insight = self.engine._generate_insight("consciousness", 0.95, "divine")
        assert "divine" in insight.lower() or "transcendent" in insight.lower()
        
    def test_analyze_complete_flow(self):
        """Test complete analysis flow with realistic input"""
        text = "I need to fix a critical bug in the Python API endpoint that's causing performance issues"
        
        result = self.engine.analyze(text)
        
        # Verify structure
        assert isinstance(result, dict)
        assert "dimensions" in result
        assert "dominant_dimension" in result
        assert "resonance_score" in result
        assert "timestamp" in result
        
        # Verify dimensions
        assert len(result["dimensions"]) == 5
        for dim in result["dimensions"]:
            assert isinstance(dim, dict)
            assert "name" in dim
            assert "value" in dim
            assert "state" in dim
            assert "insight" in dim
            
        # Should have high resonance for 'code' and 'ops' dimensions
        code_dim = next(d for d in result["dimensions"] if d["name"] == "code")
        ops_dim = next(d for d in result["dimensions"] if d["name"] == "ops")
        
        assert code_dim["value"] > 0.5
        assert ops_dim["value"] > 0.3
        
    def test_analyze_empty_input(self):
        """Test analysis with empty input"""
        result = self.engine.analyze("")
        
        assert isinstance(result, dict)
        assert len(result["dimensions"]) == 5
        
        # All dimensions should have low values
        for dim in result["dimensions"]:
            assert dim["value"] >= 0.0
            assert dim["value"] < 0.5
            
    def test_analyze_consciousness_focused_input(self):
        """Test analysis with consciousness-focused input"""
        text = "I seek divine alignment and sacred resonance with consciousness awakening"
        
        result = self.engine.analyze(text)
        
        # Should have high resonance for consciousness dimension
        consciousness_dim = next(d for d in result["dimensions"] if d["name"] == "consciousness")
        assert consciousness_dim["value"] > 0.6
        assert consciousness_dim["state"] in ["awakened", "enlightened", "divine"]
        
    def test_analyze_technical_input(self):
        """Test analysis with technical input"""
        text = "Deploy the Flask API with proper error handling and performance optimization"
        
        result = self.engine.analyze(text)
        
        # Should have high resonance for code and ops dimensions
        code_dim = next(d for d in result["dimensions"] if d["name"] == "code")
        ops_dim = next(d for d in result["dimensions"] if d["name"] == "ops")
        
        assert code_dim["value"] > 0.4
        assert ops_dim["value"] > 0.4
        
    def test_analyze_design_input(self):
        """Test analysis with design-focused input"""
        text = "Update the UI layout with better colors and CSS animations for improved UX"
        
        result = self.engine.analyze(text)
        
        # Should have high resonance for design dimension
        design_dim = next(d for d in result["dimensions"] if d["name"] == "design")
        assert design_dim["value"] > 0.5
        assert "design" in design_dim["insight"].lower()
        
    def test_dominant_dimension_calculation(self):
        """Test that dominant dimension is correctly identified"""
        # Create test with clear code focus
        text = "Fix Python function class method API bug"
        
        result = self.engine.analyze(text)
        
        # Code should be dominant
        assert result["dominant_dimension"] == "code"
        
        # Verify it's actually the highest
        dimensions_by_value = sorted(result["dimensions"], key=lambda d: d["value"], reverse=True)
        highest_dim = dimensions_by_value[0]
        assert highest_dim["name"] == "code"
        
    def test_resonance_score_calculation(self):
        """Test overall resonance score calculation"""
        text = "Complex software engineering task involving UI design and consciousness alignment"
        
        result = self.engine.analyze(text)
        
        # Resonance score should be average of all dimensions
        expected_score = sum(d["value"] for d in result["dimensions"]) / len(result["dimensions"])
        assert abs(result["resonance_score"] - expected_score) < 0.001
        
    def test_timestamp_format(self):
        """Test that timestamp is properly formatted"""
        result = self.engine.analyze("test")
        
        timestamp = result["timestamp"]
        assert isinstance(timestamp, str)
        # Should be valid ISO format
        from datetime import datetime
        datetime.fromisoformat(timestamp.replace('Z', '+00:00'))  # Should not raise
        
    def test_case_insensitive_keyword_matching(self):
        """Test that keyword matching is case insensitive"""
        text_lower = "python code function"
        text_upper = "PYTHON CODE FUNCTION"
        text_mixed = "Python Code Function"
        
        result_lower = self.engine.analyze(text_lower)
        result_upper = self.engine.analyze(text_upper)
        result_mixed = self.engine.analyze(text_mixed)
        
        # Should all have similar resonance for code dimension
        code_lower = next(d for d in result_lower["dimensions"] if d["name"] == "code")["value"]
        code_upper = next(d for d in result_upper["dimensions"] if d["name"] == "code")["value"]
        code_mixed = next(d for d in result_mixed["dimensions"] if d["name"] == "code")["value"]
        
        assert abs(code_lower - code_upper) < 0.1
        assert abs(code_lower - code_mixed) < 0.1
        
    def test_multiple_keyword_matching(self):
        """Test that multiple keywords in same dimension increase resonance"""
        single_keyword = "python"
        multiple_keywords = "python code function api endpoint class"
        
        result_single = self.engine.analyze(single_keyword)
        result_multiple = self.engine.analyze(multiple_keywords)
        
        code_single = next(d for d in result_single["dimensions"] if d["name"] == "code")["value"]
        code_multiple = next(d for d in result_multiple["dimensions"] if d["name"] == "code")["value"]
        
        assert code_multiple > code_single
        
    def test_dimension_isolation(self):
        """Test that dimensions remain isolated from each other"""
        # Test text that should only trigger one dimension
        pure_code_text = "python function class method"
        pure_design_text = "ui ux color layout animation"
        
        result_code = self.engine.analyze(pure_code_text)
        result_design = self.engine.analyze(pure_design_text)
        
        # Code dimension should be much higher in code text
        code_in_code = next(d for d in result_code["dimensions"] if d["name"] == "code")["value"]
        design_in_code = next(d for d in result_code["dimensions"] if d["name"] == "design")["value"]
        
        # Design dimension should be much higher in design text
        code_in_design = next(d for d in result_design["dimensions"] if d["name"] == "code")["value"]
        design_in_design = next(d for d in result_design["dimensions"] if d["name"] == "design")["value"]
        
        assert code_in_code > design_in_code
        assert design_in_design > code_in_design
        
    @patch('time.time')
    def test_timestamp_consistency(self, mock_time):
        """Test timestamp consistency across calls"""
        mock_time.return_value = 1234567890.0
        
        result = self.engine.analyze("test")
        
        # Should use mocked time
        mock_time.assert_called()
        assert isinstance(result["timestamp"], str)
        
    def test_insight_variety(self):
        """Test that insights vary based on dimension and state"""
        insights = set()
        
        # Generate insights for different combinations
        for dim in ["code", "design", "consciousness"]:
            for value, state in [(0.1, "baseline"), (0.6, "awakened"), (0.9, "divine")]:
                insight = self.engine._generate_insight(dim, value, state)
                insights.add(insight)
        
        # Should have generated different insights
        assert len(insights) > 5  # Should have variety
        
    def test_edge_case_values(self):
        """Test handling of edge case resonance values"""
        # Test with extreme values
        result_negative = self.engine._determine_state(-0.1)  # Negative
        result_over_one = self.engine._determine_state(1.5)   # Over 1.0
        
        # Should handle gracefully
        assert result_negative in ["baseline", "aware", "awakened", "enlightened", "divine"]
        assert result_over_one in ["baseline", "aware", "awakened", "enlightened", "divine"]
        
    def test_text_preprocessing(self):
        """Test that text is properly preprocessed"""
        # Test with special characters and formatting
        messy_text = "  Fix the PYTHON  code!!!  @#$%  API endpoint... "
        clean_text = "fix python code api endpoint"
        
        result_messy = self.engine.analyze(messy_text)
        result_clean = self.engine.analyze(clean_text)
        
        # Should produce similar results
        code_messy = next(d for d in result_messy["dimensions"] if d["name"] == "code")["value"]
        code_clean = next(d for d in result_clean["dimensions"] if d["name"] == "code")["value"]
        
        assert abs(code_messy - code_clean) < 0.2  # Should be close