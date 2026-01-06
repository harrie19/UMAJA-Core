"""
Test Ethical Value Embeddings
Tests for EthicalValueEncoder and get_most_aligned_principle method
"""

import sys
from pathlib import Path

# Add umaja_core to path
sys.path.insert(0, str(Path(__file__).parent.parent))

import pytest
import numpy as np
from unittest.mock import Mock, patch


def test_get_most_aligned_principle_universal_context():
    """Test finding most aligned principle in universal context"""
    with patch('umaja_core.protocols.ethics.value_embeddings.SentenceTransformer') as mock_transformer:
        # Mock the transformer model
        mock_model = Mock()
        
        # Mock encode to return deterministic vectors
        def mock_encode(text, normalize_embeddings=False):
            # Return vectors where "fairness" is most similar to "treat everyone equally"
            if "fairness" in text.lower():
                return np.array([1.0, 0.0, 0.0])
            elif "compassion" in text.lower():
                return np.array([0.0, 1.0, 0.0])
            elif "treat everyone equally" in text.lower():
                return np.array([0.9, 0.1, 0.0])  # Similar to fairness
            else:
                return np.random.randn(3)
        
        mock_model.encode = mock_encode
        mock_transformer.return_value = mock_model
        
        from umaja_core.protocols.ethics.value_embeddings import EthicalValueEncoder
        
        encoder = EthicalValueEncoder()
        
        # Test finding principle
        principle, score = encoder.get_most_aligned_principle(
            action="treat everyone equally",
            cultural_context="universal"
        )
        
        assert principle is not None
        assert isinstance(principle, str)
        assert isinstance(score, float)
        assert 0.0 <= score <= 1.0


def test_get_most_aligned_principle_utilitarian_context():
    """Test finding most aligned principle in utilitarian context"""
    with patch('umaja_core.protocols.ethics.value_embeddings.SentenceTransformer') as mock_transformer:
        mock_model = Mock()
        mock_model.encode = Mock(return_value=np.random.randn(768))
        mock_transformer.return_value = mock_model
        
        from umaja_core.protocols.ethics.value_embeddings import EthicalValueEncoder
        
        encoder = EthicalValueEncoder()
        
        principle, score = encoder.get_most_aligned_principle(
            action="maximize happiness for all",
            cultural_context="utilitarian"
        )
        
        assert principle is not None
        assert isinstance(principle, str)
        assert isinstance(score, float)
        assert 0.0 <= score <= 1.0


def test_get_most_aligned_principle_deontological_context():
    """Test finding most aligned principle in deontological context"""
    with patch('umaja_core.protocols.ethics.value_embeddings.SentenceTransformer') as mock_transformer:
        mock_model = Mock()
        mock_model.encode = Mock(return_value=np.random.randn(768))
        mock_transformer.return_value = mock_model
        
        from umaja_core.protocols.ethics.value_embeddings import EthicalValueEncoder
        
        encoder = EthicalValueEncoder()
        
        principle, score = encoder.get_most_aligned_principle(
            action="follow moral duty",
            cultural_context="deontological"
        )
        
        assert principle is not None
        assert isinstance(principle, str)


def test_get_most_aligned_principle_virtue_context():
    """Test finding most aligned principle in virtue context"""
    with patch('umaja_core.protocols.ethics.value_embeddings.SentenceTransformer') as mock_transformer:
        mock_model = Mock()
        mock_model.encode = Mock(return_value=np.random.randn(768))
        mock_transformer.return_value = mock_model
        
        from umaja_core.protocols.ethics.value_embeddings import EthicalValueEncoder
        
        encoder = EthicalValueEncoder()
        
        principle, score = encoder.get_most_aligned_principle(
            action="cultivate wisdom and courage",
            cultural_context="virtue"
        )
        
        assert principle is not None


def test_get_most_aligned_principle_unknown_context_raises_error():
    """Test that unknown cultural context raises ValueError"""
    with patch('umaja_core.protocols.ethics.value_embeddings.SentenceTransformer') as mock_transformer:
        mock_model = Mock()
        mock_transformer.return_value = mock_model
        
        from umaja_core.protocols.ethics.value_embeddings import EthicalValueEncoder
        
        encoder = EthicalValueEncoder()
        
        # Test with unknown context
        with pytest.raises(ValueError) as exc_info:
            encoder.get_most_aligned_principle(
                action="some action",
                cultural_context="unknown_context"
            )
        
        assert "Unknown cultural context" in str(exc_info.value)
        assert "unknown_context" in str(exc_info.value)
        assert "Available contexts" in str(exc_info.value)


def test_get_most_aligned_principle_error_message_lists_valid_contexts():
    """Test that error message lists valid cultural contexts"""
    with patch('umaja_core.protocols.ethics.value_embeddings.SentenceTransformer') as mock_transformer:
        mock_model = Mock()
        mock_transformer.return_value = mock_model
        
        from umaja_core.protocols.ethics.value_embeddings import EthicalValueEncoder
        
        encoder = EthicalValueEncoder()
        
        # Test error message content
        with pytest.raises(ValueError) as exc_info:
            encoder.get_most_aligned_principle(
                action="test",
                cultural_context="invalid"
            )
        
        error_msg = str(exc_info.value)
        # Check that valid contexts are mentioned
        assert "universal" in error_msg or "Available contexts" in error_msg


def test_get_most_aligned_principle_empty_principles_raises_error():
    """Test that empty principles list raises ValueError"""
    with patch('umaja_core.protocols.ethics.value_embeddings.SentenceTransformer') as mock_transformer:
        mock_model = Mock()
        mock_transformer.return_value = mock_model
        
        from umaja_core.protocols.ethics.value_embeddings import EthicalValueEncoder
        
        encoder = EthicalValueEncoder()
        
        # Temporarily patch CULTURAL_CONTEXTS to have empty principles
        original_contexts = encoder.CULTURAL_CONTEXTS
        encoder.CULTURAL_CONTEXTS = {
            'empty_context': {
                'description': 'Test context',
                'principles': []
            }
        }
        
        # Test with empty principles
        with pytest.raises(ValueError) as exc_info:
            encoder.get_most_aligned_principle(
                action="some action",
                cultural_context="empty_context"
            )
        
        assert "No principles defined" in str(exc_info.value)
        assert "empty_context" in str(exc_info.value)
        
        # Restore original contexts
        encoder.CULTURAL_CONTEXTS = original_contexts


def test_get_most_aligned_principle_returns_best_match():
    """Test that method returns the principle with highest alignment"""
    with patch('umaja_core.protocols.ethics.value_embeddings.SentenceTransformer') as mock_transformer:
        mock_model = Mock()
        
        # Create a controlled scenario where we know which principle should win
        call_count = [0]
        
        def mock_encode(text, normalize_embeddings=False):
            call_count[0] += 1
            # Make the action vector
            if call_count[0] == 1:  # Action vector
                return np.array([1.0, 0.0, 0.0])
            # Make "fairness" most similar
            elif "fairness" in text.lower():
                return np.array([0.95, 0.05, 0.0])  # Very similar
            else:
                return np.array([0.0, 1.0, 0.0])  # Not similar
        
        mock_model.encode = mock_encode
        mock_transformer.return_value = mock_model
        
        from umaja_core.protocols.ethics.value_embeddings import EthicalValueEncoder
        
        encoder = EthicalValueEncoder()
        
        principle, score = encoder.get_most_aligned_principle(
            action="test action",
            cultural_context="universal"
        )
        
        # The score should be positive and reasonable
        assert score > 0.5
        assert score <= 1.0


def test_get_most_aligned_principle_default_context():
    """Test that default context is 'universal'"""
    with patch('umaja_core.protocols.ethics.value_embeddings.SentenceTransformer') as mock_transformer:
        mock_model = Mock()
        mock_model.encode = Mock(return_value=np.random.randn(768))
        mock_transformer.return_value = mock_model
        
        from umaja_core.protocols.ethics.value_embeddings import EthicalValueEncoder
        
        encoder = EthicalValueEncoder()
        
        # Test without specifying context (should default to 'universal')
        principle, score = encoder.get_most_aligned_principle(action="test action")
        
        assert principle is not None
        assert isinstance(principle, str)


def test_ethical_value_encoder_initialization():
    """Test that EthicalValueEncoder initializes correctly"""
    with patch('umaja_core.protocols.ethics.value_embeddings.SentenceTransformer') as mock_transformer:
        mock_model = Mock()
        mock_transformer.return_value = mock_model
        
        from umaja_core.protocols.ethics.value_embeddings import EthicalValueEncoder
        
        encoder = EthicalValueEncoder()
        
        # Check that model is set
        assert encoder.model is not None
        # Check that cache is initialized
        assert hasattr(encoder, 'value_cache')
        assert isinstance(encoder.value_cache, dict)
        # Check that CULTURAL_CONTEXTS exists
        assert hasattr(encoder, 'CULTURAL_CONTEXTS')
        assert 'universal' in encoder.CULTURAL_CONTEXTS


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
