"""
Test Holographic AI System
===========================

Tests for the holographic AI system including:
- Holographic fragments
- Personality agents
- Memory agents
- System orchestration
- Integration with existing systems
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

import pytest
import asyncio
import numpy as np


# =============================================================================
# HOLOGRAPHIC FRAGMENT TESTS
# =============================================================================

def test_holographic_fragment_creation():
    """Test creating a holographic fragment"""
    from holographic_ai_system import HolographicFragment
    
    vector = np.random.randn(128)
    fragment = HolographicFragment(
        id="test_fragment",
        vector=vector,
        metadata={"test": "data"},
        energy_level=1.0
    )
    
    assert fragment.id == "test_fragment"
    assert fragment.energy_level == 1.0
    assert fragment.metadata["test"] == "data"
    assert isinstance(fragment.vector, np.ndarray)


def test_fragment_serialization():
    """Test fragment to/from dict conversion"""
    from holographic_ai_system import HolographicFragment
    
    vector = np.random.randn(128)
    fragment = HolographicFragment(
        id="test_fragment",
        vector=vector,
        metadata={"test": "data"}
    )
    
    # Convert to dict
    fragment_dict = fragment.to_dict()
    assert 'id' in fragment_dict
    assert 'vector' in fragment_dict
    assert 'metadata' in fragment_dict
    
    # Convert back from dict
    restored = HolographicFragment.from_dict(fragment_dict)
    assert restored.id == fragment.id
    assert np.allclose(restored.vector, fragment.vector)


# =============================================================================
# HOLOGRAPHIC PERSONALITY AGENT TESTS
# =============================================================================

def test_personality_agent_initialization():
    """Test personality agent initializes correctly"""
    from holographic_ai_system import HolographicPersonalityAgent
    
    agent = HolographicPersonalityAgent("john_cleese", dimension=128)
    
    assert agent.name == "john_cleese"
    assert agent.dimension == 128
    assert len(agent.fragments) == 5  # Should have 5 trait fragments
    assert agent.interference_matrix is not None


def test_personality_vector_generation():
    """Test getting combined personality vector"""
    from holographic_ai_system import HolographicPersonalityAgent
    
    agent = HolographicPersonalityAgent("professor", dimension=128)
    
    vector = agent.get_personality_vector()
    
    assert isinstance(vector, np.ndarray)
    assert len(vector) == 128
    # Should be normalized
    assert np.isclose(np.linalg.norm(vector), 1.0, atol=0.01)


def test_query_trait():
    """Test querying specific traits"""
    from holographic_ai_system import HolographicPersonalityAgent
    
    agent = HolographicPersonalityAgent("enthusiast", dimension=128)
    
    # Query for 'humor' trait
    humor_fragment = agent.query_trait('humor')
    
    assert humor_fragment is not None
    assert humor_fragment.metadata['trait'] == 'humor'
    assert humor_fragment.metadata['personality'] == 'enthusiast'


def test_energy_update():
    """Test updating fragment energy"""
    from holographic_ai_system import HolographicPersonalityAgent
    
    agent = HolographicPersonalityAgent("worrier", dimension=128)
    
    # Get a fragment and lower its energy first
    fragment_id = agent.fragments[0].id
    agent.fragments[0].energy_level = 0.5
    original_energy = agent.fragments[0].energy_level
    
    # Update energy
    agent.update_energy(fragment_id, 0.1)
    
    # Energy should have increased
    new_energy = agent.fragments[0].energy_level
    assert new_energy > original_energy
    assert new_energy == 0.6


def test_interference_matrix():
    """Test interference matrix computation"""
    from holographic_ai_system import HolographicPersonalityAgent
    
    agent = HolographicPersonalityAgent("c3po", dimension=128)
    
    # Should have interference matrix
    assert agent.interference_matrix is not None
    assert agent.interference_matrix.shape == (5, 5)
    
    # Diagonal should be zero (no self-interference)
    for i in range(5):
        assert agent.interference_matrix[i, i] == 0


# =============================================================================
# HOLOGRAPHIC MEMORY AGENT TESTS
# =============================================================================

@pytest.mark.asyncio
async def test_memory_agent_initialization():
    """Test memory agent initializes"""
    from holographic_ai_system import HolographicMemoryAgent
    
    agent = HolographicMemoryAgent(dimension=128, max_memories=100)
    
    assert agent.dimension == 128
    assert agent.max_memories == 100
    assert len(agent.memories) == 0


@pytest.mark.asyncio
async def test_store_memory():
    """Test storing a memory"""
    from holographic_ai_system import HolographicMemoryAgent
    
    agent = HolographicMemoryAgent()
    
    memory_id = await agent.store_memory("Test memory content", {"type": "test"})
    
    assert memory_id is not None
    assert len(agent.memories) == 1
    assert agent.memories[0].metadata['content'] == "Test memory content"


@pytest.mark.asyncio
async def test_recall_memory():
    """Test recalling memories"""
    from holographic_ai_system import HolographicMemoryAgent
    
    agent = HolographicMemoryAgent()
    
    # Store some memories
    await agent.store_memory("Python programming", {"topic": "code"})
    await agent.store_memory("Machine learning", {"topic": "ai"})
    await agent.store_memory("Web development", {"topic": "code"})
    
    # Recall similar memories
    recalled = await agent.recall_memory("Python code", top_k=2)
    
    assert len(recalled) <= 2
    assert all(isinstance(m.vector, np.ndarray) for m in recalled)


@pytest.mark.asyncio
async def test_memory_decay():
    """Test memory energy decay"""
    from holographic_ai_system import HolographicMemoryAgent
    
    agent = HolographicMemoryAgent()
    
    # Store a memory
    await agent.store_memory("Test memory", {})
    original_energy = agent.memories[0].energy_level
    
    # Apply decay
    await agent.decay_memories(decay_rate=0.1)
    
    # Energy should have decreased
    new_energy = agent.memories[0].energy_level
    assert new_energy < original_energy


@pytest.mark.asyncio
async def test_memory_capacity_limit():
    """Test memory capacity limits"""
    from holographic_ai_system import HolographicMemoryAgent
    
    agent = HolographicMemoryAgent(max_memories=5)
    
    # Store more memories than capacity
    for i in range(10):
        await agent.store_memory(f"Memory {i}", {})
    
    # Should only have max_memories
    assert len(agent.memories) == 5


# =============================================================================
# HOLOGRAPHIC AI SYSTEM TESTS
# =============================================================================

def test_holographic_system_initialization():
    """Test holographic AI system initializes"""
    from holographic_ai_system import HolographicAISystem
    
    system = HolographicAISystem()
    
    assert system is not None
    assert len(system.personality_agents) == 6  # 3 comedians + 3 archetypes
    assert system.memory_agent is not None
    assert system.system_energy == 1.0


@pytest.mark.asyncio
async def test_process_query():
    """Test processing a query"""
    from holographic_ai_system import HolographicAISystem
    
    system = HolographicAISystem()
    
    result = await system.process_query("What makes people smile?", personality="professor")
    
    assert result is not None
    assert 'query' in result
    assert 'personality' in result
    assert result['personality'] == 'professor'
    assert 'processing_time_ms' in result


def test_interference_patterns():
    """Test getting interference patterns between personalities"""
    from holographic_ai_system import HolographicAISystem
    
    system = HolographicAISystem()
    
    # Get interference between two personalities
    interference = system.get_interference_patterns('john_cleese', 'c3po')
    
    assert interference is not None
    assert isinstance(interference, float)
    assert -1.0 <= interference <= 1.0  # Dot product range


def test_system_state():
    """Test getting system state"""
    from holographic_ai_system import HolographicAISystem
    
    system = HolographicAISystem()
    
    state = system.get_system_state()
    
    assert 'personalities' in state
    assert 'memories' in state
    assert 'system_energy' in state
    assert len(state['personalities']) == 6


@pytest.mark.asyncio
async def test_self_heal():
    """Test self-healing process"""
    from holographic_ai_system import HolographicAISystem
    
    system = HolographicAISystem()
    
    # Store some memories
    await system.memory_agent.store_memory("Test 1", {})
    await system.memory_agent.store_memory("Test 2", {})
    
    # Weaken a fragment
    first_agent = list(system.personality_agents.values())[0]
    first_agent.fragments[0].energy_level = 0.3
    
    # Run self-heal
    await system.self_heal()
    
    # Fragment should be reinforced
    assert first_agent.fragments[0].energy_level > 0.3


def test_save_and_load_state():
    """Test saving and loading system state"""
    from holographic_ai_system import HolographicAISystem
    import tempfile
    import shutil
    
    # Create temporary directory
    temp_dir = tempfile.mkdtemp()
    
    try:
        # Create system and save state
        system1 = HolographicAISystem(data_dir=temp_dir)
        system1.personality_agents['john_cleese'].fragments[0].energy_level = 0.5
        system1.save_state()
        
        # Create new system and load state
        system2 = HolographicAISystem(data_dir=temp_dir)
        loaded = system2.load_state()
        
        assert loaded == True
        # Energy should be restored
        assert system2.personality_agents['john_cleese'].fragments[0].energy_level == 0.5
    
    finally:
        # Clean up
        shutil.rmtree(temp_dir)


# =============================================================================
# UMAJA HOLOGRAPHIC INTEGRATION TESTS
# =============================================================================

def test_holographic_integration_initialization():
    """Test UMAJA holographic integration initializes"""
    from holographic_ai_system import UMAJAHolographicIntegration
    
    integration = UMAJAHolographicIntegration()
    
    assert integration is not None
    assert integration.holographic_system is not None


@pytest.mark.asyncio
async def test_generate_with_holographic_personality():
    """Test generating content with holographic personality"""
    from holographic_ai_system import UMAJAHolographicIntegration
    
    integration = UMAJAHolographicIntegration()
    
    result = await integration.generate_with_holographic_personality(
        topic="happiness",
        personality="enthusiast"
    )
    
    assert result is not None
    assert 'holographic_metadata' in result
    assert 'personality' in result


def test_get_system_health():
    """Test getting system health"""
    from holographic_ai_system import UMAJAHolographicIntegration
    
    integration = UMAJAHolographicIntegration()
    
    health = integration.get_system_health()
    
    assert 'holographic' in health
    assert 'timestamp' in health


def test_get_holographic_integration_singleton():
    """Test global holographic integration instance"""
    from holographic_ai_system import get_holographic_integration
    
    integration1 = get_holographic_integration()
    integration2 = get_holographic_integration()
    
    # Should be same instance (singleton)
    assert integration1 is integration2


# =============================================================================
# INTEGRATION WITH EXISTING SYSTEMS
# =============================================================================

def test_integration_with_personality_engine():
    """Test integration with existing personality engine"""
    from holographic_ai_system import UMAJAHolographicIntegration
    
    integration = UMAJAHolographicIntegration()
    
    # Should have integrated personality engine if available
    if integration.personality_engine:
        assert integration.personality_engine is not None
        # Should have same personalities
        comedians = integration.personality_engine.list_comedians()
        assert len(comedians) > 0


def test_integration_with_energy_monitor():
    """Test integration with energy monitor"""
    from holographic_ai_system import UMAJAHolographicIntegration
    
    integration = UMAJAHolographicIntegration()
    
    # Should have integrated energy monitor if available
    if integration.energy_monitor:
        assert integration.energy_monitor is not None


# =============================================================================
# PERSONALITY VECTOR CONFIGURATION TESTS
# =============================================================================

def test_personality_vectors_file():
    """Test personality vectors configuration file"""
    import json
    
    vectors_path = Path(__file__).parent.parent / "data" / "personality_vectors.json"
    
    assert vectors_path.exists()
    
    with open(vectors_path, 'r') as f:
        data = json.load(f)
    
    assert 'personalities' in data
    assert 'john_cleese' in data['personalities']
    assert 'professor' in data['personalities']
    
    # Check structure
    john = data['personalities']['john_cleese']
    assert 'traits' in john
    assert 'dimension' in john
    assert john['dimension'] == 128


def test_interference_patterns_config():
    """Test interference patterns configuration"""
    import json
    
    vectors_path = Path(__file__).parent.parent / "data" / "personality_vectors.json"
    
    with open(vectors_path, 'r') as f:
        data = json.load(f)
    
    assert 'interference_patterns' in data
    patterns = data['interference_patterns']
    
    assert 'strong_constructive' in patterns
    assert 'balanced' in patterns
    assert 'creative_tension' in patterns


# =============================================================================
# PERFORMANCE TESTS
# =============================================================================

@pytest.mark.asyncio
async def test_query_processing_performance():
    """Test that query processing is reasonably fast"""
    import time
    from holographic_ai_system import HolographicAISystem
    
    system = HolographicAISystem()
    
    start_time = time.time()
    result = await system.process_query("Test query", personality="professor")
    elapsed = (time.time() - start_time) * 1000  # ms
    
    # Should complete in reasonable time (< 1 second)
    assert elapsed < 1000
    assert result['processing_time_ms'] < 1000


def test_vector_operations_efficiency():
    """Test that vector operations are efficient"""
    from holographic_ai_system import HolographicPersonalityAgent
    import time
    
    agent = HolographicPersonalityAgent("robin_williams", dimension=128)
    
    # Get personality vector multiple times
    start_time = time.time()
    for _ in range(100):
        vector = agent.get_personality_vector()
    elapsed = time.time() - start_time
    
    # Should be very fast (< 100ms for 100 operations)
    assert elapsed < 0.1


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
