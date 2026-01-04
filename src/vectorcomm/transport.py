"""
VectorComm Transport

Transport layer for sending and receiving vector messages between agents.
Supports agent-to-agent, broadcast, and multicast modes.
"""

import asyncio
import logging
from typing import Dict, List, Optional, Callable, Set
from enum import Enum
from dataclasses import dataclass, field
from collections import defaultdict
import time

from .protocol import VectorCommMessage, Intent, Priority
from .serialization import serialize_message, deserialize_message
from .verification import add_checksum, verify_checksum, validate_message

logger = logging.getLogger(__name__)


class TransportMode(Enum):
    """Transport modes"""
    UNICAST = "unicast"  # One-to-one
    BROADCAST = "broadcast"  # One-to-all
    MULTICAST = "multicast"  # One-to-many (specific group)


@dataclass
class TransportStats:
    """Statistics for transport layer"""
    messages_sent: int = 0
    messages_received: int = 0
    messages_dropped: int = 0
    bytes_sent: int = 0
    bytes_received: int = 0
    errors: int = 0
    
    def to_dict(self) -> dict:
        return {
            'messages_sent': self.messages_sent,
            'messages_received': self.messages_received,
            'messages_dropped': self.messages_dropped,
            'bytes_sent': self.bytes_sent,
            'bytes_received': self.bytes_received,
            'errors': self.errors
        }


@dataclass
class MessageRoute:
    """Routing information for a message"""
    message: VectorCommMessage
    mode: TransportMode
    destinations: List[str] = field(default_factory=list)
    timestamp: float = field(default_factory=time.time)
    retries: int = 0
    max_retries: int = 3


class VectorTransport:
    """
    Vector Communication Transport Layer
    
    Manages routing and delivery of vector messages between agents.
    """
    
    def __init__(self, agent_id: str, max_queue_size: int = 1000):
        self.agent_id = agent_id
        self.max_queue_size = max_queue_size
        
        # Message queues
        self.inbox: asyncio.Queue = asyncio.Queue(maxsize=max_queue_size)
        self.outbox: asyncio.Queue = asyncio.Queue(maxsize=max_queue_size)
        
        # Routing tables
        self.agent_routes: Dict[str, 'VectorTransport'] = {}  # Direct agent connections
        self.broadcast_subscribers: Set[str] = set()
        self.multicast_groups: Dict[str, Set[str]] = defaultdict(set)
        
        # Message handlers by intent
        self.handlers: Dict[Intent, List[Callable]] = defaultdict(list)
        
        # Statistics
        self.stats = TransportStats()
        
        # Running flag
        self.running = False
        
    async def start(self):
        """Start transport layer"""
        self.running = True
        logger.info(f"Transport started for agent {self.agent_id}")
        
        # Start message processing loops
        asyncio.create_task(self._process_outbox())
        asyncio.create_task(self._process_inbox())
    
    async def stop(self):
        """Stop transport layer"""
        self.running = False
        logger.info(f"Transport stopped for agent {self.agent_id}")
    
    def register_handler(self, intent: Intent, handler: Callable):
        """
        Register a handler for specific message intent
        
        Args:
            intent: Message intent to handle
            handler: Async function to handle message
        """
        self.handlers[intent].append(handler)
        logger.info(f"Registered handler for {intent.value}")
    
    def connect_agent(self, agent_id: str, transport: 'VectorTransport'):
        """
        Connect to another agent's transport
        
        Args:
            agent_id: ID of agent to connect to
            transport: Transport instance of other agent
        """
        self.agent_routes[agent_id] = transport
        logger.info(f"Connected to agent {agent_id}")
    
    def disconnect_agent(self, agent_id: str):
        """Disconnect from an agent"""
        if agent_id in self.agent_routes:
            del self.agent_routes[agent_id]
            logger.info(f"Disconnected from agent {agent_id}")
    
    def subscribe_broadcast(self):
        """Subscribe to broadcast messages"""
        self.broadcast_subscribers.add(self.agent_id)
    
    def unsubscribe_broadcast(self):
        """Unsubscribe from broadcast messages"""
        self.broadcast_subscribers.discard(self.agent_id)
    
    def join_multicast_group(self, group_id: str):
        """Join a multicast group"""
        self.multicast_groups[group_id].add(self.agent_id)
        logger.info(f"Joined multicast group {group_id}")
    
    def leave_multicast_group(self, group_id: str):
        """Leave a multicast group"""
        if group_id in self.multicast_groups:
            self.multicast_groups[group_id].discard(self.agent_id)
            logger.info(f"Left multicast group {group_id}")
    
    async def send(self, message: VectorCommMessage, add_checksum_flag: bool = True) -> bool:
        """
        Send a message
        
        Args:
            message: Message to send
            add_checksum_flag: Whether to add checksum
        
        Returns:
            True if queued successfully
        """
        try:
            # Validate message
            is_valid, errors = validate_message(message, strict=False)
            if not is_valid:
                logger.error(f"Invalid message: {errors}")
                self.stats.errors += 1
                return False
            
            # Add checksum if requested
            if add_checksum_flag and not message.checksum:
                add_checksum(message)
            
            # Determine routing mode
            if message.metadata.destination_agent is None:
                mode = TransportMode.BROADCAST
                destinations = list(self.broadcast_subscribers)
            else:
                mode = TransportMode.UNICAST
                destinations = [message.metadata.destination_agent]
            
            # Create route
            route = MessageRoute(
                message=message,
                mode=mode,
                destinations=destinations
            )
            
            # Queue for sending
            await self.outbox.put(route)
            
            self.stats.messages_sent += 1
            self.stats.bytes_sent += message.get_size_bytes()
            
            return True
            
        except asyncio.QueueFull:
            logger.error(f"Outbox full, dropping message")
            self.stats.messages_dropped += 1
            return False
        except Exception as e:
            logger.error(f"Error sending message: {e}")
            self.stats.errors += 1
            return False
    
    async def receive(self, timeout: Optional[float] = None) -> Optional[VectorCommMessage]:
        """
        Receive a message from inbox
        
        Args:
            timeout: Timeout in seconds (None = wait forever)
        
        Returns:
            Message or None if timeout
        """
        try:
            if timeout:
                message = await asyncio.wait_for(self.inbox.get(), timeout=timeout)
            else:
                message = await self.inbox.get()
            
            self.stats.messages_received += 1
            self.stats.bytes_received += message.get_size_bytes()
            
            return message
        except asyncio.TimeoutError:
            return None
        except Exception as e:
            logger.error(f"Error receiving message: {e}")
            self.stats.errors += 1
            return None
    
    async def _process_outbox(self):
        """Process outgoing messages"""
        while self.running:
            try:
                route = await asyncio.wait_for(self.outbox.get(), timeout=1.0)
                await self._route_message(route)
            except asyncio.TimeoutError:
                continue
            except Exception as e:
                logger.error(f"Error processing outbox: {e}")
    
    async def _process_inbox(self):
        """Process incoming messages"""
        while self.running:
            try:
                # Get message from inbox
                message = await asyncio.wait_for(self.inbox.get(), timeout=1.0)
                
                # Call registered handlers
                intent = message.metadata.intent
                if intent in self.handlers:
                    for handler in self.handlers[intent]:
                        try:
                            await handler(message)
                        except Exception as e:
                            logger.error(f"Error in handler: {e}")
                
            except asyncio.TimeoutError:
                continue
            except Exception as e:
                logger.error(f"Error processing inbox: {e}")
    
    async def _route_message(self, route: MessageRoute):
        """Route a message to its destination(s)"""
        message = route.message
        
        if route.mode == TransportMode.UNICAST:
            # Send to specific agent
            dest = route.destinations[0]
            if dest in self.agent_routes:
                transport = self.agent_routes[dest]
                try:
                    await transport._deliver(message)
                except Exception as e:
                    logger.error(f"Error delivering to {dest}: {e}")
                    
                    # Retry logic
                    if route.retries < route.max_retries:
                        route.retries += 1
                        await asyncio.sleep(0.1 * route.retries)
                        await self.outbox.put(route)
            else:
                logger.warning(f"No route to agent {dest}")
                self.stats.messages_dropped += 1
        
        elif route.mode == TransportMode.BROADCAST:
            # Send to all connected agents
            for agent_id, transport in self.agent_routes.items():
                try:
                    await transport._deliver(message)
                except Exception as e:
                    logger.error(f"Error broadcasting to {agent_id}: {e}")
    
    async def _deliver(self, message: VectorCommMessage):
        """Deliver message to local inbox"""
        try:
            await self.inbox.put(message)
        except asyncio.QueueFull:
            logger.error(f"Inbox full for agent {self.agent_id}, dropping message")
            self.stats.messages_dropped += 1
    
    def get_stats(self) -> dict:
        """Get transport statistics"""
        return self.stats.to_dict()
    
    def get_queue_sizes(self) -> dict:
        """Get current queue sizes"""
        return {
            'inbox_size': self.inbox.qsize(),
            'outbox_size': self.outbox.qsize(),
            'inbox_max': self.max_queue_size,
            'outbox_max': self.max_queue_size
        }
    
    def get_connections(self) -> dict:
        """Get connection information"""
        return {
            'agent_id': self.agent_id,
            'connected_agents': list(self.agent_routes.keys()),
            'broadcast_subscribed': self.agent_id in self.broadcast_subscribers,
            'multicast_groups': {
                group: list(members)
                for group, members in self.multicast_groups.items()
                if self.agent_id in members
            }
        }


# Convenience functions

async def send_message(
    transport: VectorTransport,
    message: VectorCommMessage
) -> bool:
    """
    Convenience function to send a message
    
    Args:
        transport: Transport to use
        message: Message to send
    
    Returns:
        True if sent successfully
    """
    return await transport.send(message)


async def receive_message(
    transport: VectorTransport,
    timeout: Optional[float] = None
) -> Optional[VectorCommMessage]:
    """
    Convenience function to receive a message
    
    Args:
        transport: Transport to use
        timeout: Timeout in seconds
    
    Returns:
        Message or None
    """
    return await transport.receive(timeout)


async def broadcast_message(
    transport: VectorTransport,
    message: VectorCommMessage
) -> bool:
    """
    Convenience function to broadcast a message
    
    Args:
        transport: Transport to use
        message: Message to broadcast (destination should be None)
    
    Returns:
        True if sent successfully
    """
    # Ensure destination is None for broadcast
    message.metadata.destination_agent = None
    return await transport.send(message)


class MessageBroker:
    """
    Central message broker for managing multiple transports
    
    Routes messages between agents without direct connections.
    """
    
    def __init__(self):
        self.transports: Dict[str, VectorTransport] = {}
        self.stats = TransportStats()
    
    def register_transport(self, agent_id: str, transport: VectorTransport):
        """Register an agent's transport"""
        self.transports[agent_id] = transport
        logger.info(f"Registered transport for {agent_id}")
    
    def unregister_transport(self, agent_id: str):
        """Unregister an agent's transport"""
        if agent_id in self.transports:
            del self.transports[agent_id]
            logger.info(f"Unregistered transport for {agent_id}")
    
    async def route(self, message: VectorCommMessage) -> bool:
        """
        Route a message through the broker
        
        Args:
            message: Message to route
        
        Returns:
            True if routed successfully
        """
        dest = message.metadata.destination_agent
        
        if dest is None:
            # Broadcast to all
            for transport in self.transports.values():
                await transport._deliver(message)
            self.stats.messages_sent += len(self.transports)
            return True
        
        elif dest in self.transports:
            # Deliver to specific agent
            await self.transports[dest]._deliver(message)
            self.stats.messages_sent += 1
            return True
        
        else:
            logger.warning(f"No transport for agent {dest}")
            self.stats.messages_dropped += 1
            return False
    
    def get_stats(self) -> dict:
        """Get broker statistics"""
        return self.stats.to_dict()
    
    def get_registered_agents(self) -> List[str]:
        """Get list of registered agents"""
        return list(self.transports.keys())
