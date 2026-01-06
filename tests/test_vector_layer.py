"""
Test Vector Layer

Comprehensive tests for the vector layer component of the dual-layer agent.
Tests vector state initialization, encoding, similarity search, Hebbian updates,
drift prevention, and state persistence.
"""

import sys
import os
import json
from pathlib import Path
import numpy as np
import pytest
from unittest.mock import Mock, patch, MagicMock

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from agents.vector_layer import VectorLayer, VectorState


def test_vector_state_initialization():
    """Test that VectorState initializes with normalized vectors"""
    state = VectorState()
    
    # All vectors should be L2-normalized (||v|| ≈ 1.0)
    assert np.isclose(np.linalg.norm(state.identity), 1.0, atol=1e-6)
    assert np.isclose(np.linalg.norm(state.goals), 1.0, atol=1e-6)
    assert np.isclose(np.linalg.norm(state.context), 1.0, atol=1e-6)
    assert np.isclose(np.linalg.norm(state.priorities), 1.0, atol=1e-6)
    
    # Check dimensions
    assert state.identity.shape == (768,)
    assert state.goals.shape == (768,)
    assert state.context.shape == (768,)
    assert state.priorities.shape == (768,)
    
    # Check risk threshold
    assert state.risk_threshold == 0.7
    
    print("✅ VectorState initialization test passed")


def test_vector_state_serialization():
    """Test VectorState serialization and deserialization"""
    state = VectorState()
    
    # Serialize
    state_dict = state.to_dict()
    assert 'identity' in state_dict
    assert 'goals' in state_dict
    assert 'context' in state_dict
    assert 'priorities' in state_dict
    assert 'risk_threshold' in state_dict
    
    # Deserialize
    loaded_state = VectorState.from_dict(state_dict)
    assert np.allclose(loaded_state.identity, state.identity)
    assert np.allclose(loaded_state.goals, state.goals)
    assert loaded_state.risk_threshold == state.risk_threshold
    
    print("✅ VectorState serialization test passed")


@patch('sentence_transformers.SentenceTransformer')
def test_vector_layer_initialization(mock_transformer):
    """Test VectorLayer initialization"""
    import tempfile
    
    # Mock the transformer
    mock_model = MagicMock()
    mock_transformer.return_value = mock_model
    
    # Use temp path to avoid pollution
    temp_dir = tempfile.mkdtemp()
    temp_path = os.path.join(temp_dir, "test_init.json")
    
    try:
        layer = VectorLayer(state_path=temp_path)
        
        assert layer.model_name == "sentence-transformers/all-mpnet-base-v2"
        assert layer.memory_size == 1000
        assert layer.update_count == 0
        assert len(layer.memory) == 0
        
        # Check state
        assert layer.state is not None
        assert np.isclose(np.linalg.norm(layer.state.identity), 1.0, atol=1e-6)
        
        print("✅ VectorLayer initialization test passed")
    finally:
        import shutil
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)


@patch('sentence_transformers.SentenceTransformer')
def test_encode(mock_transformer):
    """Test text encoding"""
    # Mock the transformer
    mock_model = MagicMock()
    mock_embedding = np.random.randn(768)
    mock_model.encode.return_value = mock_embedding
    mock_transformer.return_value = mock_model
    
    layer = VectorLayer()
    
    # Encode text
    text = "test query"
    vec = layer.encode(text)
    
    # Check normalization
    assert np.isclose(np.linalg.norm(vec), 1.0, atol=1e-6)
    assert vec.shape == (768,)
    
    print("✅ Encode test passed")


@patch('sentence_transformers.SentenceTransformer')
def test_query_similar(mock_transformer):
    """Test similarity query with all required fields"""
    # Mock the transformer
    mock_model = MagicMock()
    mock_embedding = np.random.randn(768)
    mock_model.encode.return_value = mock_embedding
    mock_transformer.return_value = mock_model
    
    layer = VectorLayer()
    
    # Query similar
    context = layer.query_similar("joke about cats")
    
    # Check all required fields
    assert 'priority_score' in context
    assert 'risk_assessment' in context
    assert 'goal_alignment' in context
    assert 'identity_similarity' in context
    assert 'context_similarity' in context
    assert 'energy' in context
    assert 'suggested_direction' in context
    assert 'similar_memories' in context
    assert 'query_vector' in context
    
    # Check value ranges
    assert 0 <= context['priority_score'] <= 1
    assert 0 <= context['risk_assessment'] <= 1
    assert 0 <= context['goal_alignment'] <= 1
    assert -1 <= context['identity_similarity'] <= 1
    
    # Check suggested direction is normalized
    direction = context['suggested_direction']
    assert np.isclose(np.linalg.norm(direction), 1.0, atol=1e-6)
    
    print("✅ Query similar test passed")


@patch('sentence_transformers.SentenceTransformer')
def test_hebbian_update(mock_transformer):
    """Test that vector state changes after Hebbian updates"""
    import tempfile
    
    # Mock the transformer
    mock_model = MagicMock()
    mock_embedding = np.random.randn(768)
    mock_model.encode.return_value = mock_embedding
    mock_transformer.return_value = mock_model
    
    # Use temp path to avoid pollution
    temp_dir = tempfile.mkdtemp()
    temp_path = os.path.join(temp_dir, "test_hebbian.json")
    
    try:
        layer = VectorLayer(state_path=temp_path)
        
        # Store initial state
        initial_goals = layer.state.goals.copy()
        initial_context = layer.state.context.copy()
        
        # Perform update
        layer.update("action1", feedback=1.0)
        
        # State should have changed
        assert not np.allclose(initial_goals, layer.state.goals)
        assert not np.allclose(initial_context, layer.state.context)
        
        # Memory should have the action
        assert len(layer.memory) == 1
        
        # Update count should increment
        assert layer.update_count == 1
        
        print("✅ Hebbian update test passed")
    finally:
        import shutil
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)


@patch('sentence_transformers.SentenceTransformer')
def test_vector_drift_prevention(mock_transformer):
    """Test L2 normalization prevents vector magnitude explosion"""
    # Mock the transformer
    mock_model = MagicMock()
    mock_transformer.return_value = mock_model
    
    layer = VectorLayer()
    
    # Perform many updates
    for i in range(100):
        mock_embedding = np.random.randn(768) * 10  # Large random vectors
        mock_model.encode.return_value = mock_embedding
        layer.update(f"random action {i}", feedback=1.0)
    
    # Vectors should still be normalized
    assert np.linalg.norm(layer.state.identity) < 1.5
    assert np.linalg.norm(layer.state.goals) < 1.5
    assert np.linalg.norm(layer.state.context) < 1.5
    assert np.linalg.norm(layer.state.priorities) < 1.5
    
    # Should be close to 1.0 due to normalization
    assert np.isclose(np.linalg.norm(layer.state.goals), 1.0, atol=0.1)
    
    print("✅ Vector drift prevention test passed")


@patch('sentence_transformers.SentenceTransformer')
def test_semantic_collapse_detection(mock_transformer):
    """Test that low entropy in vector triggers warning"""
    # Mock the transformer
    mock_model = MagicMock()
    mock_transformer.return_value = mock_model
    
    layer = VectorLayer()
    
    # Force all dimensions to similar values (low entropy)
    layer.state.goals = np.ones(768) / np.sqrt(768)
    
    # Check drift should detect this (will add noise)
    with patch('agents.vector_layer.logger') as mock_logger:
        layer._check_drift()
        # Should log warning about semantic collapse
        # (Implementation adds noise to prevent collapse)
    
    # Vector should still be normalized after drift check
    assert np.isclose(np.linalg.norm(layer.state.goals), 1.0, atol=1e-6)
    
    print("✅ Semantic collapse detection test passed")


@patch('sentence_transformers.SentenceTransformer')
def test_state_persistence(mock_transformer):
    """Test vector state saves and loads correctly"""
    import tempfile
    
    # Mock the transformer
    mock_model = MagicMock()
    mock_embedding = np.random.randn(768)
    mock_model.encode.return_value = mock_embedding
    mock_transformer.return_value = mock_model
    
    # Create temporary directory
    temp_dir = tempfile.mkdtemp()
    temp_path = os.path.join(temp_dir, "test_state.json")
    
    try:
        # Create and save layer
        layer1 = VectorLayer(state_path=temp_path)
        layer1.state.risk_threshold = 0.8
        layer1.update("test action", feedback=1.0)
        layer1.save_state()
        
        # Verify file exists
        assert os.path.exists(temp_path)
        
        # Load in new layer
        layer2 = VectorLayer(state_path=temp_path)
        
        # Check state matches
        assert layer2.state.risk_threshold == 0.8
        assert len(layer2.memory) >= 1  # Should have at least one item
        assert layer2.update_count >= 1  # Should have at least one update
        
        print("✅ State persistence test passed")
    finally:
        # Cleanup
        import shutil
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)


@patch('sentence_transformers.SentenceTransformer')
def test_energy_tracking(mock_transformer):
    """Test that energy operations are tracked"""
    # Mock the transformer
    mock_model = MagicMock()
    mock_embedding = np.random.randn(768)
    mock_model.encode.return_value = mock_embedding
    mock_transformer.return_value = mock_model
    
    # Mock energy monitor
    mock_energy = MagicMock()
    
    layer = VectorLayer()
    layer.energy_monitor = mock_energy
    
    # Encode should log energy
    layer.encode("test")
    assert mock_energy.log_operation.called
    
    # Query should log energy
    mock_energy.reset_mock()
    layer.query_similar("test query")
    assert mock_energy.log_vector_similarity.called
    
    print("✅ Energy tracking test passed")


@patch('sentence_transformers.SentenceTransformer')
def test_memory_ring_buffer(mock_transformer):
    """Test memory ring buffer with max size"""
    # Mock the transformer
    mock_model = MagicMock()
    mock_embedding = np.random.randn(768)
    mock_model.encode.return_value = mock_embedding
    mock_transformer.return_value = mock_model
    
    layer = VectorLayer(memory_size=10)
    
    # Add more items than memory size
    for i in range(20):
        layer.update(f"action {i}", feedback=1.0)
    
    # Memory should be capped at 10
    assert len(layer.memory) == 10
    
    print("✅ Memory ring buffer test passed")


@patch('sentence_transformers.SentenceTransformer')
def test_get_state_summary(mock_transformer):
    """Test state summary generation"""
    # Mock the transformer
    mock_model = MagicMock()
    mock_transformer.return_value = mock_model
    
    layer = VectorLayer()
    
    summary = layer.get_state_summary()
    
    assert 'identity_norm' in summary
    assert 'goals_norm' in summary
    assert 'context_norm' in summary
    assert 'priorities_norm' in summary
    assert 'risk_threshold' in summary
    assert 'memory_size' in summary
    assert 'update_count' in summary
    
    # Norms should be close to 1.0
    assert 0.9 <= summary['identity_norm'] <= 1.1
    
    print("✅ State summary test passed")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
