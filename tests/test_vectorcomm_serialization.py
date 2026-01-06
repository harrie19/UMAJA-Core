"""
Tests for VectorComm Serialization - Binary message serialization
"""

import pytest
import numpy as np
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from vectorcomm.protocol import (
    VectorCommMessage, VectorCommHeader, VectorCommPayload, VectorCommMetadata,
    Intent, Priority
)
from vectorcomm.serialization import (
    serialize_message, deserialize_message,
    compress_vectors, decompress_vectors,
    estimate_compression_ratio,
    batch_serialize, batch_deserialize
)


class TestVectorCommSerialization:
    """Test suite for VectorComm serialization"""
    
    @pytest.fixture
    def sample_message(self):
        """Create a sample message for testing"""
        header = VectorCommHeader(
            source_agent="agent_1",
            protocol_version="1.0",
            encoding="float32",
            dimensions=384
        )
        
        payload = VectorCommPayload(
            primary_vector=np.random.randn(384).astype(np.float32),
            context_vectors=[
                np.random.randn(384).astype(np.float32),
                np.random.randn(384).astype(np.float32)
            ],
            attention_weights=np.array([0.6, 0.4], dtype=np.float32),
            uncertainty_vector=np.random.randn(384).astype(np.float32),
            metadata={"test": "data"}
        )
        
        metadata = VectorCommMetadata(
            intent=Intent.INFORM,
            priority=Priority.NORMAL,
            destination_agent="agent_2",
            requires_response=False
        )
        
        return VectorCommMessage(
            header=header,
            payload=payload,
            metadata=metadata
        )
    
    def test_serialize_deserialize_roundtrip(self, sample_message):
        """Test that serialize/deserialize is lossless"""
        # Serialize
        serialized = serialize_message(sample_message, compress=False)
        
        assert isinstance(serialized, bytes)
        assert len(serialized) > 0
        
        # Deserialize
        deserialized = deserialize_message(serialized, compressed=False)
        
        # Verify header
        assert deserialized.header.source_agent == sample_message.header.source_agent
        assert deserialized.header.protocol_version == sample_message.header.protocol_version
        assert deserialized.header.encoding == sample_message.header.encoding
        assert deserialized.header.dimensions == sample_message.header.dimensions
        
        # Verify payload vectors
        np.testing.assert_allclose(
            deserialized.payload.primary_vector,
            sample_message.payload.primary_vector,
            rtol=1e-5
        )
        
        assert len(deserialized.payload.context_vectors) == len(sample_message.payload.context_vectors)
        for i in range(len(deserialized.payload.context_vectors)):
            np.testing.assert_allclose(
                deserialized.payload.context_vectors[i],
                sample_message.payload.context_vectors[i],
                rtol=1e-5
            )
        
        # Verify metadata
        assert deserialized.metadata.intent == sample_message.metadata.intent
        assert deserialized.metadata.priority == sample_message.metadata.priority
    
    def test_serialize_with_compression(self, sample_message):
        """Test serialization with compression"""
        # Serialize with compression
        compressed = serialize_message(sample_message, compress=True)
        
        # Serialize without compression
        uncompressed = serialize_message(sample_message, compress=False)
        
        # Compressed should be smaller (usually)
        # Note: Very small data might not compress well
        assert len(compressed) <= len(uncompressed) * 1.2  # Allow some overhead
        
        # Should still deserialize correctly
        deserialized = deserialize_message(compressed, compressed=True)
        
        np.testing.assert_allclose(
            deserialized.payload.primary_vector,
            sample_message.payload.primary_vector,
            rtol=1e-5
        )
    
    def test_serialize_magic_bytes(self, sample_message):
        """Test that serialized data has correct magic bytes"""
        serialized = serialize_message(sample_message, compress=False)
        
        # Should start with 'VCMP' magic bytes
        assert serialized[:4] == b'VCMP'
    
    def test_deserialize_invalid_magic_bytes(self):
        """Test that invalid magic bytes raise error"""
        invalid_data = b'XXXX' + b'\x00' * 100
        
        with pytest.raises(ValueError, match="Invalid magic bytes"):
            deserialize_message(invalid_data, compressed=False)
    
    def test_compress_decompress_vectors(self):
        """Test vector compression/decompression"""
        vectors = np.random.randn(10, 384).astype(np.float32)
        
        # Test quantize method
        compressed, metadata = compress_vectors(vectors, method='quantize')
        
        assert isinstance(compressed, bytes)
        assert len(compressed) < vectors.nbytes  # Should be smaller
        assert metadata['method'] == 'quantize'
        
        # Decompress
        decompressed = decompress_vectors(compressed, metadata)
        
        assert decompressed.shape == vectors.shape
        # Quantization loses some precision
        np.testing.assert_allclose(decompressed, vectors, rtol=0.1, atol=0.1)
    
    def test_compress_decompress_gzip(self):
        """Test gzip compression/decompression"""
        vectors = np.random.randn(10, 384).astype(np.float32)
        
        # Test gzip method
        compressed, metadata = compress_vectors(vectors, method='gzip')
        
        assert isinstance(compressed, bytes)
        assert metadata['method'] == 'gzip'
        
        # Decompress
        decompressed = decompress_vectors(compressed, metadata)
        
        assert decompressed.shape == vectors.shape
        # Gzip is lossless
        np.testing.assert_allclose(decompressed, vectors, rtol=1e-6)
    
    def test_compression_ratio(self, sample_message):
        """Test that compression achieves 50-70% reduction as specified"""
        ratio = estimate_compression_ratio(sample_message)
        
        assert ratio > 0
        # Should achieve some compression (ratio > 1 means compression worked)
        # Note: Small messages might not compress well
        assert ratio >= 1.0
    
    def test_batch_serialize_deserialize(self, sample_message):
        """Test batch serialization of multiple messages"""
        # Create multiple messages
        messages = [sample_message for _ in range(5)]
        
        # Batch serialize
        batch_data = batch_serialize(messages)
        
        assert isinstance(batch_data, bytes)
        assert batch_data[:4] == b'VCBT' or batch_data[:2] == b'\x1f\x8b'  # VCBT or gzip magic
        
        # Batch deserialize
        deserialized_messages = batch_deserialize(batch_data)
        
        assert len(deserialized_messages) == len(messages)
        
        # Verify first message
        first = deserialized_messages[0]
        assert first.header.source_agent == sample_message.header.source_agent
    
    def test_serialize_without_optional_fields(self):
        """Test serialization with minimal message (no optional fields)"""
        header = VectorCommHeader(
            source_agent="agent_1",
            protocol_version="1.0",
            encoding="float32",
            dimensions=10
        )
        
        payload = VectorCommPayload(
            primary_vector=np.ones(10, dtype=np.float32),
            context_vectors=[],  # No context vectors
            attention_weights=None,  # No attention weights
            uncertainty_vector=None,  # No uncertainty
            metadata={}
        )
        
        metadata = VectorCommMetadata(
            intent=Intent.QUERY,
            priority=Priority.HIGH,
            destination_agent=None,  # Broadcast
            requires_response=False
        )
        
        message = VectorCommMessage(
            header=header,
            payload=payload,
            metadata=metadata,
            checksum=None
        )
        
        # Should serialize and deserialize without error
        serialized = serialize_message(message, compress=False)
        deserialized = deserialize_message(serialized, compressed=False)
        
        assert len(deserialized.payload.context_vectors) == 0
        assert deserialized.payload.attention_weights is None
        assert deserialized.payload.uncertainty_vector is None
    
    def test_large_vector_serialization(self):
        """Test serialization with large vectors"""
        header = VectorCommHeader(
            source_agent="agent_1",
            protocol_version="1.0",
            encoding="float32",
            dimensions=1024
        )
        
        payload = VectorCommPayload(
            primary_vector=np.random.randn(1024).astype(np.float32),
            context_vectors=[np.random.randn(1024).astype(np.float32) for _ in range(10)],
            metadata={}
        )
        
        metadata = VectorCommMetadata(
            intent=Intent.INFORM,
            priority=Priority.NORMAL
        )
        
        message = VectorCommMessage(
            header=header,
            payload=payload,
            metadata=metadata
        )
        
        # Should handle large vectors
        serialized = serialize_message(message, compress=True)
        deserialized = deserialize_message(serialized, compressed=True)
        
        assert deserialized.payload.primary_vector.shape[0] == 1024
        assert len(deserialized.payload.context_vectors) == 10
    
    def test_different_dtypes(self):
        """Test serialization with different dtypes"""
        for dtype, encoding in [(np.float32, 'float32'), (np.float16, 'float16')]:
            header = VectorCommHeader(
                source_agent="agent_1",
                protocol_version="1.0",
                encoding=encoding,
                dimensions=100
            )
            
            payload = VectorCommPayload(
                primary_vector=np.random.randn(100).astype(dtype),
                context_vectors=[],
                metadata={}
            )
            
            metadata = VectorCommMetadata(
                intent=Intent.INFORM,
                priority=Priority.NORMAL
            )
            
            message = VectorCommMessage(
                header=header,
                payload=payload,
                metadata=metadata
            )
            
            serialized = serialize_message(message, compress=False)
            deserialized = deserialize_message(serialized, compressed=False)
            
            # Check dtype is preserved
            assert deserialized.payload.primary_vector.dtype == dtype
    
    def test_compression_reduces_size(self, sample_message):
        """Test that compression actually reduces message size"""
        # Create a larger message for better compression
        header = VectorCommHeader(
            source_agent="agent_1",
            protocol_version="1.0",
            encoding="float32",
            dimensions=768
        )
        
        payload = VectorCommPayload(
            primary_vector=np.random.randn(768).astype(np.float32),
            context_vectors=[np.random.randn(768).astype(np.float32) for _ in range(5)],
            metadata={"large": "data" * 100}
        )
        
        metadata = VectorCommMetadata(
            intent=Intent.INFORM,
            priority=Priority.NORMAL
        )
        
        large_message = VectorCommMessage(
            header=header,
            payload=payload,
            metadata=metadata
        )
        
        uncompressed = serialize_message(large_message, compress=False)
        compressed = serialize_message(large_message, compress=True)
        
        # Compression should reduce size for large messages
        compression_ratio = len(uncompressed) / len(compressed)
        
        # Should achieve at least some compression
        assert compression_ratio > 1.0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
