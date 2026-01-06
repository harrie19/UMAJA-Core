"""
Test Dual-Layer Agent

Comprehensive tests for the dual-layer agent that integrates cognitive
and vector processing layers.
"""

import sys
import os
import tempfile
import shutil
from pathlib import Path
import numpy as np
import pytest
from unittest.mock import Mock, patch, MagicMock

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))


def create_temp_path():
    """Helper to create temp directory and path"""
    temp_dir = tempfile.mkdtemp()
    temp_path = os.path.join(temp_dir, f"test_state_{id(temp_dir)}.json")
    return temp_dir, temp_path


def cleanup_temp(temp_dir):
    """Helper to cleanup temp directory"""
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)


@patch('worldtour_generator.WorldtourGenerator')
@patch('personality_engine.PersonalityEngine')
@patch('sentence_transformers.SentenceTransformer')
def test_dual_layer_agent_initialization(mock_transformer, mock_personality_engine, mock_worldtour):
    """Test DualLayerAgent initialization"""
    # Mock sentence transformer
    mock_model = MagicMock()
    mock_model.encode.return_value = np.random.randn(768)
    mock_transformer.return_value = mock_model
    
    # Mock personality engine
    mock_personality = MagicMock()
    mock_personality.name = "Test Comedian"
    mock_personality.traits = ["witty", "clever"]
    
    mock_engine = MagicMock()
    mock_engine.get_comedian.return_value = mock_personality
    mock_personality_engine.return_value = mock_engine
    
    mock_wt = MagicMock()
    mock_worldtour.return_value = mock_wt
    
    temp_dir, temp_path = create_temp_path()
    
    try:
        from agents.dual_layer_agent import DualLayerAgent
        agent = DualLayerAgent(personality_id="test_comedian", vector_state_path=temp_path)
        
        assert agent.personality_id == "test_comedian"
        assert agent.veto_threshold == 0.3
        assert agent.generation_count == 0
        assert agent.veto_count == 0
        
        print("✅ DualLayerAgent initialization test passed")
    finally:
        cleanup_temp(temp_dir)


@patch('worldtour_generator.WorldtourGenerator')
@patch('personality_engine.PersonalityEngine')
@patch('sentence_transformers.SentenceTransformer')
def test_generate_content(mock_transformer, mock_personality_engine, mock_worldtour):
    """Test content generation with dual-layer architecture"""
    # Mock sentence transformer
    mock_model = MagicMock()
    mock_model.encode.return_value = np.random.randn(768)
    mock_transformer.return_value = mock_model
    
    # Mock personality
    mock_personality = MagicMock()
    mock_personality.name = "Test Comedian"
    mock_personality.generate_smile_text.return_value = "This is a funny joke!"
    
    mock_engine = MagicMock()
    mock_engine.get_comedian.return_value = mock_personality
    mock_personality_engine.return_value = mock_engine
    
    mock_wt = MagicMock()
    mock_worldtour.return_value = mock_wt
    
    temp_dir, temp_path = create_temp_path()
    
    try:
        from agents.dual_layer_agent import DualLayerAgent
        agent = DualLayerAgent(vector_state_path=temp_path)
        
        # Generate content
        result = agent.generate_content("cats", content_type="joke")
        
        # Check result structure
        assert 'content' in result
        assert 'metadata' in result
        assert 'vector_context' in result
        
        # Check metadata
        metadata = result['metadata']
        assert 'priority' in metadata
        assert 'risk' in metadata
        assert 'alignment' in metadata
        assert 'vetoed' in metadata
        assert 'generation_count' in metadata
        
        # Check that generation count incremented
        assert agent.generation_count == 1
        
        print("✅ Generate content test passed")
    finally:
        cleanup_temp(temp_dir)


@patch('worldtour_generator.WorldtourGenerator')
@patch('personality_engine.PersonalityEngine')
@patch('sentence_transformers.SentenceTransformer')
def test_get_statistics(mock_transformer, mock_personality_engine, mock_worldtour):
    """Test agent statistics retrieval"""
    # Mock sentence transformer
    mock_model = MagicMock()
    mock_model.encode.return_value = np.random.randn(768)
    mock_transformer.return_value = mock_model
    
    # Mock personality
    mock_personality = MagicMock()
    mock_personality.name = "Test"
    mock_personality.generate_smile_text.return_value = "Content"
    
    mock_engine = MagicMock()
    mock_engine.get_comedian.return_value = mock_personality
    mock_personality_engine.return_value = mock_engine
    
    mock_wt = MagicMock()
    mock_worldtour.return_value = mock_wt
    
    temp_dir, temp_path = create_temp_path()
    
    try:
        from agents.dual_layer_agent import DualLayerAgent
        agent = DualLayerAgent(vector_state_path=temp_path)
        agent.generate_content("test")
        
        # Get statistics
        stats = agent.get_statistics()
        
        assert 'generation_count' in stats
        assert 'veto_count' in stats
        assert 'veto_rate' in stats
        assert 'personality_id' in stats
        assert 'veto_threshold' in stats
        assert 'vector_state' in stats
        
        assert stats['generation_count'] >= 1
        
        print("✅ Get statistics test passed")
    finally:
        cleanup_temp(temp_dir)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
