"""
VectorComm Protocol - Formal AI-to-AI Communication

A vector-based meta-language that allows AI agents to communicate
semantically without natural language ambiguity.

Key Features:
- Binary serialization for efficiency
- Checksum verification for integrity
- Multi-vector messages for complex communication
- Agent-to-agent and broadcast modes
- Standard dimensions: 384, 768, or 4096
"""

from .protocol import (
    VectorCommHeader,
    VectorCommPayload,
    VectorCommMetadata,
    VectorCommMessage,
    Intent,
    Priority
)

from .serialization import (
    serialize_message,
    deserialize_message,
    compress_vectors,
    decompress_vectors
)

from .verification import (
    calculate_checksum,
    verify_checksum,
    validate_message
)

from .transport import (
    VectorTransport,
    TransportMode,
    send_message,
    receive_message,
    broadcast_message
)

__all__ = [
    # Protocol classes
    'VectorCommHeader',
    'VectorCommPayload',
    'VectorCommMetadata',
    'VectorCommMessage',
    'Intent',
    'Priority',
    
    # Serialization
    'serialize_message',
    'deserialize_message',
    'compress_vectors',
    'decompress_vectors',
    
    # Verification
    'calculate_checksum',
    'verify_checksum',
    'validate_message',
    
    # Transport
    'VectorTransport',
    'TransportMode',
    'send_message',
    'receive_message',
    'broadcast_message'
]

__version__ = '1.0.0'
