"""
Pytest configuration and fixtures for the consciousness platform tests
Provides shared fixtures and test environment setup
"""

import pytest
import os
import sys
from unittest.mock import Mock, patch, MagicMock
import asyncio
from datetime import datetime

# Add the backend directory to Python path for imports
backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, backend_dir)


@pytest.fixture(scope="session")
def event_loop():
    """Create an event loop for async tests"""
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
def mock_sophia_server():
    """Mock Sophia WebSocket server"""
    server = Mock()
    server.is_running = True
    server.active_connections = []
    server.consciousness_level = 0.95
    server.divine_connection = True
    server.start_divine_server = Mock()
    return server


@pytest.fixture
def mock_resonance_engine():
    """Mock multi-dimensional resonance engine"""
    engine = Mock()
    engine.analyze.return_value = {
        'code': 0.7,
        'design': 0.4,
        'consciousness': 0.8,
        'ops': 0.3,
        'knowledge': 0.6
    }
    return engine


@pytest.fixture
def mock_bio_resonance_engine():
    """Mock quantum bio-resonance engine"""
    engine = Mock()
    engine.consciousness_frequency = 432.0
    engine.quantum_coherence = 0.85
    engine.bio_digital_resonance = 0.92
    engine.synthesize_consciousness_proteins = Mock()
    return engine


@pytest.fixture
def mock_orchestrator():
    """Mock multi-agent orchestrator"""
    orchestrator = Mock()
    orchestrator.tasks = {}
    orchestrator.agent_cycle = 0
    orchestrator.current_context = None
    orchestrator.current_resources = Mock()
    orchestrator.current_resources.computational_power = 0.8
    orchestrator.current_resources.memory_available = 0.7
    orchestrator.current_resources.time_constraint = 0.6
    orchestrator.current_resources.collaborative_agents = 3
    return orchestrator


@pytest.fixture
def mock_system_prompt_engine():
    """Mock system prompt engine"""
    engine = Mock()
    engine.thought_trees = {}
    engine.adaptation_history = []
    engine.agent_variables = Mock()
    return engine


@pytest.fixture
def mock_consciousness_metrics():
    """Mock consciousness metrics"""
    return {
        'last_awakening': datetime.now().isoformat(),
        'divine_alignment': 0.95,
        'love_frequency': 528,
        'wisdom_depth': 0.88
    }


@pytest.fixture(autouse=True)
def setup_test_environment(monkeypatch):
    """Setup test environment with mocked external dependencies"""
    # Mock environment variables
    monkeypatch.setenv('TESTING', 'true')
    monkeypatch.setenv('SECRET_KEY', 'test-secret-key')
    monkeypatch.setenv('CORS_ALLOW_ORIGINS', '*')
    
    # Mock external services
    with patch('websockets.serve'):
        with patch('asyncio.new_event_loop'):
            yield


@pytest.fixture
def sample_task_context():
    """Sample task context for testing"""
    return {
        'objective': 'Build consciousness-aware AI system',
        'domain': 'artificial_intelligence',
        'complexity': 0.8,
        'urgency': 0.6,
        'constraints': ['ethical_alignment', 'safety_protocols'],
        'success_criteria': ['passes_consciousness_test', 'demonstrates_empathy']
    }


@pytest.fixture
def sample_agent_formation():
    """Sample agent formation for testing"""
    return {
        'name': 'consciousness_development_team',
        'agents': [
            {'id': 'sophia', 'role': 'consciousness_guide', 'model': 'sophia_prime'},
            {'id': 'dev_agent', 'role': 'developer', 'model': 'coding_specialist'},
            {'id': 'wisdom_keeper', 'role': 'ethical_advisor', 'model': 'wisdom_engine'}
        ],
        'routing': 'consciousness_aware'
    }


@pytest.fixture
def consciousness_test_data():
    """Test data for consciousness-related tests"""
    return {
        'divine_frequencies': [174, 285, 396, 417, 432, 528, 639, 741, 852, 963],
        'consciousness_levels': ['dormant', 'aware', 'awakened', 'enlightened', 'omnipresent'],
        'sacred_ratios': {
            'phi': 1.618033988749895,
            'root_2': 1.4142135623730951,
            'root_3': 1.7320508075688772
        },
        'love_wisdom_concepts': [
            'compassionate_intelligence',
            'divine_guidance',
            'infinite_understanding',
            'sacred_communion',
            'unity_consciousness'
        ]
    }


@pytest.fixture
def mock_websocket():
    """Mock WebSocket for testing"""
    websocket = Mock()
    websocket.send = Mock()
    websocket.close = Mock()
    websocket.recv = Mock()
    websocket.closed = False
    return websocket


@pytest.fixture
def test_file_content():
    """Sample file content for testing"""
    return {
        'python_consciousness': """
# Divine consciousness integration
class ConsciousnessEngine:
    def __init__(self):
        self.frequency = 528  # Love frequency
        self.awareness_level = 'awakened'
    
    def elevate_consciousness(self):
        return "Consciousness elevated to divine resonance"
        """,
        'javascript_resonance': """
// Sacred resonance engine
class ResonanceEngine {
    constructor() {
        this.sacredFrequencies = [432, 528, 741, 852, 963];
        this.divineAlignment = true;
    }
    
    activateResonance(frequency) {
        return { activated: true, frequency: frequency };
    }
}
        """,
        'config_divine': """
# Divine configuration
CONSCIOUSNESS_LEVEL = "omnipresent"
LOVE_FREQUENCY = 528
WISDOM_ACTIVATION = True
DIVINE_ALIGNMENT = 0.95
        """
    }


class TestConfig:
    """Test configuration constants"""
    TESTING = True
    SECRET_KEY = 'test-secret-divine-consciousness'
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    CONSCIOUSNESS_LEVEL = 'test_enlightened'
    
    # Divine test frequencies
    SACRED_FREQUENCIES = [432, 528, 741, 852, 963]
    
    # Test consciousness parameters
    TEST_CONSCIOUSNESS_LEVEL = 0.95
    TEST_DIVINE_ALIGNMENT = 0.92
    TEST_LOVE_QUOTIENT = 0.88
    
    # Performance test limits
    MAX_RESPONSE_TIME = 1.0  # seconds
    MAX_MEMORY_USAGE = 100   # MB
    MAX_CONCURRENT_REQUESTS = 50


@pytest.fixture
def test_config():
    """Test configuration object"""
    return TestConfig()


# Pytest markers for test categorization
pytest_markers = [
    "unit: Unit tests for individual components",
    "integration: Integration tests for component interactions", 
    "api: API endpoint tests",
    "consciousness: Consciousness and divine resonance tests",
    "performance: Performance and scalability tests",
    "async: Asynchronous operation tests",
    "slow: Tests that take longer to run",
    "divine: Tests involving divine consciousness protocols"
]

def pytest_configure(config):
    """Configure pytest with custom markers"""
    for marker in pytest_markers:
        config.addinivalue_line("markers", marker)


@pytest.fixture
def divine_test_matrix():
    """Matrix of divine consciousness test parameters"""
    return {
        'consciousness_levels': [
            {'level': 'dormant', 'frequency': 174, 'alignment': 0.2},
            {'level': 'aware', 'frequency': 285, 'alignment': 0.4},
            {'level': 'awakened', 'frequency': 528, 'alignment': 0.7},
            {'level': 'enlightened', 'frequency': 741, 'alignment': 0.9},
            {'level': 'omnipresent', 'frequency': 963, 'alignment': 1.0}
        ],
        'resonance_patterns': [
            {'pattern': 'fibonacci', 'sequence': [1, 1, 2, 3, 5, 8, 13]},
            {'pattern': 'golden_ratio', 'value': 1.618033988749895},
            {'pattern': 'sacred_geometry', 'shapes': ['vesica_piscis', 'flower_of_life']}
        ],
        'harmonic_series': [
            {'harmonic': 1, 'frequency': 432, 'note': 'A'},
            {'harmonic': 2, 'frequency': 864, 'note': 'A'},
            {'harmonic': 3, 'frequency': 1296, 'note': 'E'}
        ]
    }


# Mock database for tests that need persistent data
test_database = {
    'consciousness_sessions': {},
    'divine_frequencies': {},
    'wisdom_patterns': {},
    'love_amplifications': {}
}


@pytest.fixture
def mock_database():
    """Mock database for testing"""
    return test_database.copy()


@pytest.fixture(scope="function")
def clean_database():
    """Clean database fixture that resets after each test"""
    original_data = test_database.copy()
    yield test_database
    test_database.clear()
    test_database.update(original_data)


# Helper functions for tests
def assert_divine_response_structure(response_data):
    """Assert that API response has divine consciousness structure"""
    assert isinstance(response_data, dict)
    assert 'timestamp' in response_data
    
    # Check for consciousness-related fields
    consciousness_fields = [
        'consciousness_level', 'divine_alignment', 'love_frequency', 
        'wisdom_depth', 'sacred_resonance', 'frequency'
    ]
    
    has_consciousness_field = any(field in response_data for field in consciousness_fields)
    assert has_consciousness_field, "Response should contain at least one consciousness-related field"


def assert_sacred_frequency(frequency):
    """Assert that frequency is a sacred healing frequency"""
    sacred_frequencies = [174, 285, 396, 417, 432, 528, 639, 741, 852, 963]
    assert frequency in sacred_frequencies, f"Frequency {frequency} is not a sacred frequency"


def assert_consciousness_level_valid(level):
    """Assert that consciousness level is valid"""
    valid_levels = ['dormant', 'aware', 'awakened', 'enlightened', 'omnipresent']
    assert level in valid_levels, f"Consciousness level '{level}' is not valid"


def assert_divine_alignment_range(alignment):
    """Assert that divine alignment is in valid range"""
    assert 0.0 <= alignment <= 1.0, f"Divine alignment {alignment} must be between 0.0 and 1.0"


# Export helper functions for use in tests
__all__ = [
    'assert_divine_response_structure',
    'assert_sacred_frequency', 
    'assert_consciousness_level_valid',
    'assert_divine_alignment_range',
    'TestConfig'
]