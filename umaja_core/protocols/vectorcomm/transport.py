"""
VectorComm Transport Layer
Handles message transmission and protocol formatting
"""

import json
import uuid
from typing import Dict, Any, Optional
from datetime import datetime
import numpy as np


class VectorMessage:
    """Structured message for VectorComm protocol"""
    
    def __init__(
        self,
        sender_id: str,
        receiver_id: str,
        vector: np.ndarray,
        tier: int,
        metadata: Optional[Dict[str, Any]] = None,
        message_id: Optional[str] = None
    ):
        self.message_id = message_id or str(uuid.uuid4())
        self.sender_id = sender_id
        self.receiver_id = receiver_id
        self.vector = vector
        self.tier = tier
        self.metadata = metadata or {}
        self.timestamp = datetime.utcnow().isoformat()
        
    def to_dict(self) -> Dict[str, Any]:
        """Serialize message to dictionary"""
        return {
            'message_id': self.message_id,
            'sender_id': self.sender_id,
            'receiver_id': self.receiver_id,
            'vector': self.vector.tolist(),
            'tier': self.tier,
            'metadata': self.metadata,
            'timestamp': self.timestamp
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'VectorMessage':
        """Deserialize message from dictionary"""
        msg = cls(
            sender_id=data['sender_id'],
            receiver_id=data['receiver_id'],
            vector=np.array(data['vector']),
            tier=data['tier'],
            metadata=data.get('metadata', {}),
            message_id=data.get('message_id')
        )
        msg.timestamp = data.get('timestamp', msg.timestamp)
        return msg
    
    def to_json(self) -> str:
        """Serialize to JSON string"""
        return json.dumps(self.to_dict())
    
    @classmethod
    def from_json(cls, json_str: str) -> 'VectorMessage':
        """Deserialize from JSON string"""
        return cls.from_dict(json.loads(json_str))


class VectorTransport:
    """
    Transport layer for VectorComm messages
    Handles routing, buffering, and delivery
    """
    
    def __init__(self):
        self.message_buffer = {}
        self.delivery_log = []
        
    def send(self, message: VectorMessage) -> bool:
        """
        Send a vector message
        
        Args:
            message: VectorMessage to send
            
        Returns:
            True if sent successfully
        """
        # In a real implementation, this would handle network transmission
        # For now, we buffer messages
        receiver_id = message.receiver_id
        
        if receiver_id not in self.message_buffer:
            self.message_buffer[receiver_id] = []
        
        self.message_buffer[receiver_id].append(message)
        self.delivery_log.append({
            'message_id': message.message_id,
            'timestamp': datetime.utcnow().isoformat(),
            'status': 'delivered'
        })
        
        return True
    
    def receive(self, agent_id: str) -> Optional[VectorMessage]:
        """
        Receive next message for agent
        
        Args:
            agent_id: ID of receiving agent
            
        Returns:
            Next VectorMessage or None if no messages
        """
        if agent_id not in self.message_buffer or not self.message_buffer[agent_id]:
            return None
        
        return self.message_buffer[agent_id].pop(0)
    
    def receive_all(self, agent_id: str) -> list:
        """Receive all pending messages for agent"""
        messages = self.message_buffer.get(agent_id, [])
        self.message_buffer[agent_id] = []
        return messages
    
    def has_messages(self, agent_id: str) -> bool:
        """Check if agent has pending messages"""
        return agent_id in self.message_buffer and len(self.message_buffer[agent_id]) > 0
    
    def get_delivery_stats(self) -> Dict[str, int]:
        """Get delivery statistics"""
        return {
            'total_delivered': len(self.delivery_log),
            'agents_with_messages': len([k for k, v in self.message_buffer.items() if v])
        }
