"""
Tests for VectorComm Protocol
Tests encoding, decoding, and tier compression
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import numpy as np
import pytest
from unittest.mock import Mock, patch
from umaja_core.protocols.vectorcomm.encoder import VectorCommEncoder
from umaja_core.protocols.vectorcomm.transport import VectorMessage, VectorTransport
from umaja_core.protocols.vectorcomm.lmnet import LMNet


class TestVectorCommEncoder:
    """Test VectorCommEncoder functionality"""
    
    def test_encoder_initialization(self):
        """Test encoder can be initialized"""
        encoder = VectorCommEncoder()
        assert encoder is not None
        assert len(encoder.TIER_CONFIGS) == 3
    
    def test_tier_info(self):
        """Test getting tier information"""
        encoder = VectorCommEncoder()
        
        tier1_info = encoder.get_tier_info(1)
        assert tier1_info['dim'] == 384
        assert tier1_info['latency_ms'] == 16
        
        tier2_info = encoder.get_tier_info(2)
        assert tier2_info['dim'] == 768
        
        tier3_info = encoder.get_tier_info(3)
        assert tier3_info['dim'] == 1024
    
    def test_list_tiers(self):
        """Test listing all tiers"""
        encoder = VectorCommEncoder()
        tiers = encoder.list_tiers()
        
        assert len(tiers) == 3
        assert 1 in tiers and 2 in tiers and 3 in tiers
        assert all('dimension' in info for info in tiers.values())
    
    @patch('umaja_core.protocols.vectorcomm.encoder.SentenceTransformer')
    def test_encode_mock(self, mock_transformer):
        """Test encoding with mocked model"""
        # Mock the encoder
        mock_model = Mock()
        mock_model.encode.return_value = np.random.randn(768)
        mock_transformer.return_value = mock_model
        
        encoder = VectorCommEncoder()
        vector = encoder.encode("Hello world", tier=2)
        
        assert isinstance(vector, np.ndarray)
        mock_model.encode.assert_called_once()
    
    @patch('umaja_core.protocols.vectorcomm.encoder.SentenceTransformer')
    def test_decode_with_candidates(self, mock_transformer):
        """Test decoding with candidate messages"""
        mock_model = Mock()
        
        # Mock encode to return different vectors for different inputs
        def mock_encode_fn(texts, **kwargs):
            if isinstance(texts, list):
                return np.random.randn(len(texts), 768)
            return np.random.randn(768)
        
        mock_model.encode = mock_encode_fn
        mock_transformer.return_value = mock_model
        
        encoder = VectorCommEncoder()
        test_vector = np.random.randn(768)
        candidates = ["Hello", "World", "Test"]
        
        result = encoder.decode(test_vector, tier=2, candidates=candidates)
        assert result in candidates
    
    @patch('umaja_core.protocols.vectorcomm.encoder.SentenceTransformer')
    def test_compress_to_tier(self, mock_transformer):
        """Test tier compression"""
        encoder = VectorCommEncoder()
        
        # Create a high-dimensional vector
        high_dim_vector = np.random.randn(1024)
        
        # Compress from tier 3 to tier 1
        compressed = encoder.compress_to_tier(high_dim_vector, source_tier=3, target_tier=1)
        
        assert len(compressed) == 384


class TestVectorTransport:
    """Test VectorTransport functionality"""
    
    def test_message_creation(self):
        """Test creating vector message"""
        vector = np.random.randn(768)
        msg = VectorMessage(
            sender_id="agent1",
            receiver_id="agent2",
            vector=vector,
            tier=2
        )
        
        assert msg.sender_id == "agent1"
        assert msg.receiver_id == "agent2"
        assert msg.tier == 2
        assert np.array_equal(msg.vector, vector)
        assert msg.message_id is not None
    
    def test_message_serialization(self):
        """Test message to/from dict"""
        vector = np.random.randn(384)
        msg = VectorMessage(
            sender_id="agent1",
            receiver_id="agent2",
            vector=vector,
            tier=1,
            metadata={'test': 'data'}
        )
        
        # Serialize
        msg_dict = msg.to_dict()
        assert 'message_id' in msg_dict
        assert 'vector' in msg_dict
        
        # Deserialize
        msg2 = VectorMessage.from_dict(msg_dict)
        assert msg2.sender_id == msg.sender_id
        assert msg2.tier == msg.tier
        assert np.array_equal(msg2.vector, msg.vector)
    
    def test_message_json(self):
        """Test message JSON serialization"""
        vector = np.random.randn(768)
        msg = VectorMessage(
            sender_id="agent1",
            receiver_id="agent2",
            vector=vector,
            tier=2
        )
        
        json_str = msg.to_json()
        assert isinstance(json_str, str)
        
        msg2 = VectorMessage.from_json(json_str)
        assert np.array_equal(msg2.vector, msg.vector)
    
    def test_transport_send_receive(self):
        """Test sending and receiving messages"""
        transport = VectorTransport()
        
        msg = VectorMessage(
            sender_id="agent1",
            receiver_id="agent2",
            vector=np.random.randn(768),
            tier=2
        )
        
        # Send
        success = transport.send(msg)
        assert success
        
        # Check has messages
        assert transport.has_messages("agent2")
        
        # Receive
        received = transport.receive("agent2")
        assert received is not None
        assert received.message_id == msg.message_id
    
    def test_transport_no_messages(self):
        """Test receiving when no messages"""
        transport = VectorTransport()
        
        received = transport.receive("agent_unknown")
        assert received is None
        assert not transport.has_messages("agent_unknown")
    
    def test_receive_all(self):
        """Test receiving all messages"""
        transport = VectorTransport()
        
        # Send multiple messages
        for i in range(5):
            msg = VectorMessage(
                sender_id=f"sender{i}",
                receiver_id="agent1",
                vector=np.random.randn(768),
                tier=2
            )
            transport.send(msg)
        
        # Receive all
        messages = transport.receive_all("agent1")
        assert len(messages) == 5
        
        # Should be empty now
        assert not transport.has_messages("agent1")


class TestLMNet:
    """Test LMNet utilities"""
    
    def test_compute_similarity(self):
        """Test similarity computation"""
        vec1 = np.array([1.0, 0.0, 0.0])
        vec2 = np.array([1.0, 0.0, 0.0])
        
        sim = LMNet.compute_similarity(vec1, vec2)
        assert 0.0 <= sim <= 1.0
        assert sim > 0.9  # Should be very similar
    
    def test_find_nearest_agents(self):
        """Test finding nearest agents"""
        query = np.random.randn(768)
        
        agent_vectors = [np.random.randn(768) for _ in range(10)]
        agent_ids = [f"agent{i}" for i in range(10)]
        
        nearest = LMNet.find_nearest_agents(query, agent_vectors, agent_ids, top_k=3)
        
        assert len(nearest) == 3
        assert all(isinstance(item, tuple) for item in nearest)
        assert all(isinstance(item[0], str) for item in nearest)
        assert all(isinstance(item[1], float) for item in nearest)
    
    def test_aggregate_vectors_mean(self):
        """Test vector aggregation with mean"""
        vectors = [
            np.array([1.0, 2.0, 3.0]),
            np.array([2.0, 3.0, 4.0]),
            np.array([3.0, 4.0, 5.0])
        ]
        
        aggregated = LMNet.aggregate_vectors(vectors, method='mean')
        expected = np.array([2.0, 3.0, 4.0])
        
        np.testing.assert_array_almost_equal(aggregated, expected)
    
    def test_aggregate_vectors_weighted(self):
        """Test weighted aggregation"""
        vectors = [
            np.array([1.0, 0.0]),
            np.array([0.0, 1.0])
        ]
        weights = [0.7, 0.3]
        
        aggregated = LMNet.aggregate_vectors(vectors, method='weighted', weights=weights)
        
        assert aggregated[0] > aggregated[1]  # Should be weighted toward first vector
    
    def test_interpolate_vectors(self):
        """Test vector interpolation"""
        vec1 = np.array([0.0, 0.0])
        vec2 = np.array([10.0, 10.0])
        
        # 50% interpolation
        mid = LMNet.interpolate_vectors(vec1, vec2, alpha=0.5)
        expected = np.array([5.0, 5.0])
        
        np.testing.assert_array_almost_equal(mid, expected)
    
    def test_compute_diversity(self):
        """Test diversity computation"""
        # Identical vectors = low diversity
        identical = [np.array([1.0, 0.0, 0.0])] * 3
        diversity_low = LMNet.compute_diversity(identical)
        
        # Random vectors = higher diversity
        diverse = [np.random.randn(10) for _ in range(5)]
        diversity_high = LMNet.compute_diversity(diverse)
        
        assert 0.0 <= diversity_low <= 1.0
        assert 0.0 <= diversity_high <= 1.0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
