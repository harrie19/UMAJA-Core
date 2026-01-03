"""
Test Vector Agent System without requiring model downloads

These tests validate the core logic and structure without needing HuggingFace models
"""

import sys
import os
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

import numpy as np
from unittest.mock import Mock, MagicMock, patch


def test_imports():
    """Test that all modules can be imported"""
    from vector_agents import VectorAgent, VectorAgentOrchestrator
    from vector_agents import ResearchAgent, CodeAgent, CreativeAgent, MathAgent, TeacherAgent
    
    assert VectorAgent is not None
    assert VectorAgentOrchestrator is not None
    assert ResearchAgent is not None
    assert CodeAgent is not None
    assert CreativeAgent is not None
    assert MathAgent is not None
    assert TeacherAgent is not None
    print("✅ All imports successful")


def test_vector_agent_creation():
    """Test creating a VectorAgent with mocked analyzer"""
    from vector_agents.base_agent import VectorAgent
    
    # Mock the VektorAnalyzer
    mock_analyzer = Mock()
    mock_analyzer.encode_texts = Mock(return_value=np.array([np.random.randn(384)]))
    
    # Create agent
    agent = VectorAgent(
        competence_description="Test agent",
        analyzer=mock_analyzer
    )
    
    assert agent is not None
    assert agent.agent_id is not None
    assert agent.signal_weight == 0.7
    assert agent.noise_weight == 0.3
    print(f"✅ VectorAgent created: {agent.agent_id}")


def test_can_handle_method():
    """Test the can_handle method"""
    from vector_agents.base_agent import VectorAgent
    
    # Mock the analyzer
    mock_analyzer = Mock()
    mock_analyzer.encode_texts = Mock(return_value=np.array([np.random.randn(384)]))
    mock_analyzer.cosine_similarity = Mock(return_value=0.85)
    
    agent = VectorAgent(
        competence_description="Test agent",
        analyzer=mock_analyzer
    )
    
    # Test can_handle
    can_do, similarity = agent.can_handle("Test task", threshold=0.7)
    
    assert isinstance(can_do, bool)
    assert isinstance(similarity, float)
    assert can_do == True  # Should be True since similarity (0.85) > threshold (0.7)
    print(f"✅ can_handle works: {can_do}, similarity: {similarity}")


def test_agent_communication():
    """Test communication between agents"""
    from vector_agents.base_agent import VectorAgent
    
    # Mock analyzer
    mock_analyzer = Mock()
    mock_analyzer.encode_texts = Mock(return_value=np.array([np.random.randn(384)]))
    mock_analyzer.cosine_similarity = Mock(return_value=0.75)
    
    agent1 = VectorAgent(competence_description="Agent 1", analyzer=mock_analyzer)
    agent2 = VectorAgent(competence_description="Agent 2", analyzer=mock_analyzer)
    
    comm_result = agent1.communicate_with(agent2)
    
    assert 'similarity' in comm_result
    assert 'competence_similarity' in comm_result
    assert 'aligned' in comm_result
    assert 'complementary' in comm_result
    print(f"✅ Agent communication works: similarity={comm_result['similarity']}")


def test_agent_clone():
    """Test agent cloning"""
    from vector_agents.base_agent import VectorAgent
    
    mock_analyzer = Mock()
    mock_analyzer.encode_texts = Mock(return_value=np.array([np.random.randn(384)]))
    
    parent = VectorAgent(competence_description="Parent agent", analyzer=mock_analyzer)
    clone = parent.clone()
    
    assert clone is not None
    assert clone.agent_id != parent.agent_id
    assert "clone" in clone.agent_id
    print(f"✅ Agent cloning works: {parent.agent_id} -> {clone.agent_id}")


def test_agent_merge():
    """Test merging two agents"""
    from vector_agents.base_agent import VectorAgent
    
    mock_analyzer = Mock()
    mock_analyzer.encode_texts = Mock(return_value=np.array([np.random.randn(384)]))
    
    agent1 = VectorAgent(competence_description="Agent 1", analyzer=mock_analyzer)
    agent2 = VectorAgent(competence_description="Agent 2", analyzer=mock_analyzer)
    
    merged = agent1.merge_with(agent2)
    
    assert merged is not None
    assert merged.agent_id != agent1.agent_id
    assert merged.agent_id != agent2.agent_id
    assert "merged" in merged.agent_id
    print(f"✅ Agent merging works: {agent1.agent_id} + {agent2.agent_id} = {merged.agent_id}")


def test_specialized_agents():
    """Test creating specialized agents"""
    from vector_agents.specialized_agents import (
        ResearchAgent, CodeAgent, CreativeAgent, MathAgent, TeacherAgent
    )
    
    mock_analyzer = Mock()
    mock_analyzer.encode_texts = Mock(return_value=np.array([np.random.randn(384)]))
    
    # Create each specialized agent
    agents = {
        'research': ResearchAgent(analyzer=mock_analyzer),
        'code': CodeAgent(analyzer=mock_analyzer),
        'creative': CreativeAgent(analyzer=mock_analyzer),
        'math': MathAgent(analyzer=mock_analyzer),
        'teacher': TeacherAgent(analyzer=mock_analyzer)
    }
    
    # Check signal/noise ratios
    assert agents['research'].signal_weight == 0.80
    assert agents['code'].signal_weight == 0.85
    assert agents['creative'].signal_weight == 0.60
    assert agents['math'].signal_weight == 0.95
    assert agents['teacher'].signal_weight == 0.75
    
    print("✅ All specialized agents created with correct signal/noise ratios")


def test_orchestrator_creation():
    """Test creating an orchestrator"""
    from vector_agents.orchestrator import VectorAgentOrchestrator
    
    # Mock the VektorAnalyzer at module level
    with patch('vector_agents.orchestrator.VektorAnalyzer') as mock_analyzer_class:
        mock_analyzer = Mock()
        mock_analyzer.encode_texts = Mock(return_value=np.array([np.random.randn(384)]))
        mock_analyzer_class.return_value = mock_analyzer
        
        orchestrator = VectorAgentOrchestrator()
        
        assert orchestrator is not None
        assert len(orchestrator.agents) == 0
        print("✅ VectorAgentOrchestrator created")


def test_orchestrator_spawn_agent():
    """Test spawning agents via orchestrator"""
    from vector_agents.orchestrator import VectorAgentOrchestrator
    
    with patch('vector_agents.orchestrator.VektorAnalyzer') as mock_analyzer_class:
        mock_analyzer = Mock()
        mock_analyzer.encode_texts = Mock(return_value=np.array([np.random.randn(384)]))
        mock_analyzer_class.return_value = mock_analyzer
        
        orchestrator = VectorAgentOrchestrator()
        
        # Spawn a research agent
        agent_id = orchestrator.spawn_agent('research')
        
        assert agent_id is not None
        assert agent_id in orchestrator.agents
        assert orchestrator.stats['total_agents'] == 1
        print(f"✅ Agent spawned: {agent_id}")


def test_orchestrator_add_task():
    """Test adding tasks to orchestrator"""
    from vector_agents.orchestrator import VectorAgentOrchestrator
    
    with patch('vector_agents.orchestrator.VektorAnalyzer') as mock_analyzer_class:
        mock_analyzer = Mock()
        mock_analyzer.encode_texts = Mock(return_value=np.array([np.random.randn(384)]))
        mock_analyzer_class.return_value = mock_analyzer
        
        orchestrator = VectorAgentOrchestrator()
        
        task_id = orchestrator.add_task("Test task", priority=7)
        
        assert task_id is not None
        assert orchestrator.stats['total_tasks'] == 1
        print(f"✅ Task added: {task_id}")


def test_package_version():
    """Test package version and metadata"""
    import vector_agents
    
    assert hasattr(vector_agents, '__version__')
    assert vector_agents.__version__ == "1.0.0"
    
    # Test helper functions
    assert hasattr(vector_agents, 'get_version')
    assert hasattr(vector_agents, 'list_agent_types')
    
    agent_types = vector_agents.list_agent_types()
    assert 'research' in agent_types
    assert 'code' in agent_types
    assert 'creative' in agent_types
    assert 'math' in agent_types
    assert 'teacher' in agent_types
    
    print(f"✅ Package version: {vector_agents.__version__}")
    print(f"✅ Agent types: {agent_types}")


if __name__ == "__main__":
    print("=" * 70)
    print("🌌 UMAJA Vector Agent System - Unit Tests")
    print("=" * 70)
    print()
    
    tests = [
        ("Imports", test_imports),
        ("Vector Agent Creation", test_vector_agent_creation),
        ("Can Handle Method", test_can_handle_method),
        ("Agent Communication", test_agent_communication),
        ("Agent Clone", test_agent_clone),
        ("Agent Merge", test_agent_merge),
        ("Specialized Agents", test_specialized_agents),
        ("Orchestrator Creation", test_orchestrator_creation),
        ("Orchestrator Spawn Agent", test_orchestrator_spawn_agent),
        ("Orchestrator Add Task", test_orchestrator_add_task),
        ("Package Version", test_package_version),
    ]
    
    passed = 0
    failed = 0
    
    for name, test_func in tests:
        try:
            print(f"Running: {name}...")
            test_func()
            passed += 1
            print()
        except Exception as e:
            print(f"❌ FAILED: {e}")
            failed += 1
            print()
    
    print("=" * 70)
    print(f"Results: {passed} passed, {failed} failed")
    print("=" * 70)
    
    if failed == 0:
        print("✨ All tests passed!")
    else:
        print(f"⚠️  {failed} test(s) failed")
        exit(1)
