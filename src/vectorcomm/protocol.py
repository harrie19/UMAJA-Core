"""
VectorComm Protocol Classes

Defines the formal structure for vector-based AI-to-AI communication.
"""

import numpy as np
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any
from enum import Enum
from datetime import datetime, timezone


class Intent(Enum):
    """Message intent types"""
    QUERY = "query"
    RESPONSE = "response"
    COMMAND = "command"
    NOTIFICATION = "notification"
    UPDATE = "update"
    ERROR = "error"
    HEARTBEAT = "heartbeat"


class Priority(Enum):
    """Message priority levels (0-10)"""
    LOWEST = 0
    LOW = 2
    NORMAL = 5
    HIGH = 7
    CRITICAL = 10


@dataclass
class VectorCommHeader:
    """
    Header for vector communication protocol
    
    Contains metadata about the vector encoding and format.
    """
    dimension: int  # 384, 768, or 4096
    encoding: str  # 'float32', 'float16', 'bfloat16'
    semantic_space: str  # e.g., 'all-MiniLM-L6-v2', 'text-embedding-ada-002'
    confidence: float  # 0.0-1.0, how confident in semantic encoding
    version: str = "1.0"
    
    def __post_init__(self):
        # Validate dimension
        if self.dimension not in [384, 768, 1536, 4096]:
            raise ValueError(f"Unsupported dimension: {self.dimension}. Use 384, 768, 1536, or 4096")
        
        # Validate encoding
        if self.encoding not in ['float32', 'float16', 'bfloat16']:
            raise ValueError(f"Unsupported encoding: {self.encoding}")
        
        # Validate confidence
        if not 0.0 <= self.confidence <= 1.0:
            raise ValueError(f"Confidence must be 0.0-1.0, got {self.confidence}")
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'dimension': self.dimension,
            'encoding': self.encoding,
            'semantic_space': self.semantic_space,
            'confidence': self.confidence,
            'version': self.version
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'VectorCommHeader':
        return cls(
            dimension=data['dimension'],
            encoding=data['encoding'],
            semantic_space=data['semantic_space'],
            confidence=data['confidence'],
            version=data.get('version', '1.0')
        )


@dataclass
class VectorCommPayload:
    """
    Payload containing vector data
    
    Supports multiple vectors for complex semantic communication.
    """
    primary_vector: np.ndarray  # Main semantic content
    context_vectors: List[np.ndarray] = field(default_factory=list)  # Additional context
    attention_weights: Optional[np.ndarray] = None  # Importance weights for context
    uncertainty_vector: Optional[np.ndarray] = None  # Epistemic uncertainty
    metadata: Dict[str, Any] = field(default_factory=dict)  # Additional payload metadata
    
    def __post_init__(self):
        # Ensure primary_vector is numpy array
        if not isinstance(self.primary_vector, np.ndarray):
            self.primary_vector = np.array(self.primary_vector)
        
        # Ensure context_vectors are numpy arrays
        self.context_vectors = [
            np.array(v) if not isinstance(v, np.ndarray) else v
            for v in self.context_vectors
        ]
        
        # Convert attention_weights if provided
        if self.attention_weights is not None and not isinstance(self.attention_weights, np.ndarray):
            self.attention_weights = np.array(self.attention_weights)
        
        # Convert uncertainty_vector if provided
        if self.uncertainty_vector is not None and not isinstance(self.uncertainty_vector, np.ndarray):
            self.uncertainty_vector = np.array(self.uncertainty_vector)
    
    def get_dimension(self) -> int:
        """Get the dimension of the primary vector"""
        return len(self.primary_vector)
    
    def has_context(self) -> bool:
        """Check if payload has context vectors"""
        return len(self.context_vectors) > 0
    
    def has_uncertainty(self) -> bool:
        """Check if payload has uncertainty vector"""
        return self.uncertainty_vector is not None
    
    def get_total_vectors(self) -> int:
        """Get total number of vectors in payload"""
        total = 1  # primary
        total += len(self.context_vectors)
        if self.uncertainty_vector is not None:
            total += 1
        return total


@dataclass
class VectorCommMetadata:
    """
    Metadata about the message
    
    Contains routing and identification information.
    """
    source_agent: str  # ID of sending agent
    destination_agent: Optional[str] = None  # ID of receiving agent (None for broadcast)
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    intent: Intent = Intent.QUERY
    priority: Priority = Priority.NORMAL
    message_id: Optional[str] = None  # Unique message ID
    conversation_id: Optional[str] = None  # ID for related messages
    reply_to: Optional[str] = None  # Message ID this is replying to
    expires_at: Optional[str] = None  # ISO8601 timestamp when message expires
    metadata: Dict[str, Any] = field(default_factory=dict)  # Additional metadata
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'source_agent': self.source_agent,
            'destination_agent': self.destination_agent,
            'timestamp': self.timestamp,
            'intent': self.intent.value,
            'priority': self.priority.value,
            'message_id': self.message_id,
            'conversation_id': self.conversation_id,
            'reply_to': self.reply_to,
            'expires_at': self.expires_at,
            'metadata': self.metadata
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'VectorCommMetadata':
        return cls(
            source_agent=data['source_agent'],
            destination_agent=data.get('destination_agent'),
            timestamp=data.get('timestamp', datetime.now(timezone.utc).isoformat()),
            intent=Intent(data.get('intent', 'query')),
            priority=Priority(data.get('priority', 5)),
            message_id=data.get('message_id'),
            conversation_id=data.get('conversation_id'),
            reply_to=data.get('reply_to'),
            expires_at=data.get('expires_at'),
            metadata=data.get('metadata', {})
        )
    
    def is_broadcast(self) -> bool:
        """Check if message is broadcast"""
        return self.destination_agent is None
    
    def is_expired(self) -> bool:
        """Check if message has expired"""
        if self.expires_at is None:
            return False
        
        expires = datetime.fromisoformat(self.expires_at.replace('Z', '+00:00'))
        now = datetime.now(timezone.utc)
        return now > expires


@dataclass
class VectorCommMessage:
    """
    Complete vector communication message
    
    Combines header, payload, and metadata into a complete message.
    """
    header: VectorCommHeader
    payload: VectorCommPayload
    metadata: VectorCommMetadata
    checksum: Optional[str] = None  # SHA256 checksum for integrity
    
    def validate(self) -> bool:
        """Validate message structure"""
        # Check dimensions match
        if self.payload.get_dimension() != self.header.dimension:
            return False
        
        # Check context vectors have same dimension
        for context_vec in self.payload.context_vectors:
            if len(context_vec) != self.header.dimension:
                return False
        
        # Check uncertainty vector if present
        if self.payload.has_uncertainty():
            if len(self.payload.uncertainty_vector) != self.header.dimension:
                return False
        
        # Check attention weights if present
        if self.payload.attention_weights is not None:
            if len(self.payload.attention_weights) != len(self.payload.context_vectors):
                return False
        
        # Check if expired
        if self.metadata.is_expired():
            return False
        
        return True
    
    def get_size_bytes(self) -> int:
        """Estimate message size in bytes"""
        # Header: ~200 bytes
        size = 200
        
        # Payload vectors
        bytes_per_element = {
            'float32': 4,
            'float16': 2,
            'bfloat16': 2
        }
        bytes_per = bytes_per_element.get(self.header.encoding, 4)
        
        # Primary vector
        size += self.header.dimension * bytes_per
        
        # Context vectors
        size += len(self.payload.context_vectors) * self.header.dimension * bytes_per
        
        # Uncertainty vector
        if self.payload.has_uncertainty():
            size += self.header.dimension * bytes_per
        
        # Attention weights
        if self.payload.attention_weights is not None:
            size += len(self.payload.attention_weights) * 4  # float32
        
        # Metadata: ~500 bytes
        size += 500
        
        # Checksum: 64 bytes
        size += 64
        
        return size
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert message to dictionary (for JSON serialization)"""
        return {
            'header': self.header.to_dict(),
            'payload': {
                'primary_vector': self.payload.primary_vector.tolist(),
                'context_vectors': [v.tolist() for v in self.payload.context_vectors],
                'attention_weights': self.payload.attention_weights.tolist() if self.payload.attention_weights is not None else None,
                'uncertainty_vector': self.payload.uncertainty_vector.tolist() if self.payload.uncertainty_vector is not None else None,
                'metadata': self.payload.metadata
            },
            'metadata': self.metadata.to_dict(),
            'checksum': self.checksum
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'VectorCommMessage':
        """Create message from dictionary"""
        header = VectorCommHeader.from_dict(data['header'])
        
        payload_data = data['payload']
        payload = VectorCommPayload(
            primary_vector=np.array(payload_data['primary_vector']),
            context_vectors=[np.array(v) for v in payload_data.get('context_vectors', [])],
            attention_weights=np.array(payload_data['attention_weights']) if payload_data.get('attention_weights') else None,
            uncertainty_vector=np.array(payload_data['uncertainty_vector']) if payload_data.get('uncertainty_vector') else None,
            metadata=payload_data.get('metadata', {})
        )
        
        metadata = VectorCommMetadata.from_dict(data['metadata'])
        
        return cls(
            header=header,
            payload=payload,
            metadata=metadata,
            checksum=data.get('checksum')
        )
    
    def __repr__(self) -> str:
        return (
            f"VectorCommMessage("
            f"from={self.metadata.source_agent}, "
            f"to={self.metadata.destination_agent or 'broadcast'}, "
            f"intent={self.metadata.intent.value}, "
            f"dim={self.header.dimension}, "
            f"vectors={self.payload.get_total_vectors()}, "
            f"size={self.get_size_bytes()}B)"
        )


def create_message(
    source_agent: str,
    primary_vector: np.ndarray,
    destination_agent: Optional[str] = None,
    intent: Intent = Intent.QUERY,
    priority: Priority = Priority.NORMAL,
    context_vectors: Optional[List[np.ndarray]] = None,
    semantic_space: str = "all-MiniLM-L6-v2",
    confidence: float = 1.0
) -> VectorCommMessage:
    """
    Helper function to create a VectorComm message
    
    Args:
        source_agent: ID of sending agent
        primary_vector: Main semantic vector
        destination_agent: ID of receiving agent (None for broadcast)
        intent: Message intent
        priority: Message priority
        context_vectors: Additional context vectors
        semantic_space: Name of embedding model used
        confidence: Confidence in encoding (0.0-1.0)
    
    Returns:
        Complete VectorCommMessage
    """
    # Determine dimension from primary vector
    dimension = len(primary_vector)
    
    # Determine encoding based on dtype
    if primary_vector.dtype == np.float16:
        encoding = 'float16'
    elif primary_vector.dtype == np.float32:
        encoding = 'float32'
    else:
        encoding = 'float32'  # default
        primary_vector = primary_vector.astype(np.float32)
    
    # Create header
    header = VectorCommHeader(
        dimension=dimension,
        encoding=encoding,
        semantic_space=semantic_space,
        confidence=confidence
    )
    
    # Create payload
    payload = VectorCommPayload(
        primary_vector=primary_vector,
        context_vectors=context_vectors or []
    )
    
    # Create metadata
    metadata = VectorCommMetadata(
        source_agent=source_agent,
        destination_agent=destination_agent,
        intent=intent,
        priority=priority
    )
    
    # Create message
    message = VectorCommMessage(
        header=header,
        payload=payload,
        metadata=metadata
    )
    
    return message
