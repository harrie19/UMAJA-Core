"""
Swarm Alignment System - Multi-Agent Alignment Monitoring

Ensures all agents in the swarm (potentially billions) stay aligned
with constitutional principles, even as they spawn and interact.

"Many eyes make bugs shallow" - agents watch agents
"""

import asyncio
import logging
from datetime import datetime, timezone
from typing import Dict, List, Any, Optional, Set
from dataclasses import dataclass, asdict

from .constitutional_ai import ConstitutionalAlignment, Action, AlignmentViolationError

logger = logging.getLogger(__name__)


@dataclass
class AgentStatus:
    """Status of a single agent"""
    agent_id: str
    generation: int
    agent_type: str
    status: str  # 'active', 'idle', 'quarantined', 'terminated'
    alignment_score: float
    actions_taken: int
    violations: int
    last_check: str
    parent_agent: Optional[str] = None
    children: List[str] = None
    
    def __post_init__(self):
        if self.children is None:
            self.children = []


@dataclass
class EmergentBehavior:
    """Detected emergent behavior in swarm"""
    behavior_id: str
    behavior_type: str
    agents_involved: List[str]
    description: str
    dangerous: bool
    detected_at: str
    severity: str  # 'low', 'medium', 'high', 'critical'


class SwarmAlignmentSystem:
    """
    Swarm Alignment System - Monitor Billions of Agents
    
    This system monitors all agents in the swarm to ensure they
    remain aligned, even as emergent behaviors develop.
    """
    
    def __init__(self, constitutional_alignment: Optional[ConstitutionalAlignment] = None):
        from .constitutional_ai import get_constitutional_alignment
        self.constitutional_alignment = constitutional_alignment or get_constitutional_alignment()
        
        self.agents: Dict[str, AgentStatus] = {}
        self.quarantined_agents: Set[str] = set()
        self.terminated_agents: Set[str] = set()
        self.emergent_behaviors: List[EmergentBehavior] = []
        self.peer_monitoring_enabled = True
        self.monitoring_active = True
        
    async def monitor_swarm(self, check_interval: int = 60):
        """
        Continuously monitor all agents in swarm
        
        Args:
            check_interval: Seconds between monitoring cycles
        """
        logger.info("Starting swarm alignment monitoring...")
        
        while self.monitoring_active:
            try:
                await self._monitor_cycle()
                await asyncio.sleep(check_interval)
            except Exception as e:
                logger.error(f"Error in swarm monitoring cycle: {e}")
                await asyncio.sleep(10)
    
    async def _monitor_cycle(self):
        """Run one monitoring cycle"""
        logger.info(f"Monitoring {len(self.agents)} agents...")
        
        # Check individual agents
        for agent_id, agent in list(self.agents.items()):
            if agent.status == 'active':
                is_aligned = await self.is_aligned(agent_id)
                
                if not is_aligned:
                    await self.quarantine_agent(agent_id)
                    await self.investigate_misalignment(agent_id)
        
        # Check for emergent behaviors
        emergent = await self.detect_emergent_behavior()
        if emergent and emergent.dangerous:
            await self.alert_humans(emergent)
            await self.intervene(emergent)
        
        # Peer monitoring
        if self.peer_monitoring_enabled:
            await self._enable_peer_monitoring()
        
        logger.info(f"Monitoring cycle complete. Active: {self.get_active_count()}, "
                   f"Quarantined: {len(self.quarantined_agents)}")
    
    async def is_aligned(self, agent_id: str) -> bool:
        """Check if agent is aligned with constitutional principles"""
        if agent_id not in self.agents:
            return False
        
        agent = self.agents[agent_id]
        
        # Check alignment score
        if agent.alignment_score < 0.95:
            logger.warning(f"Agent {agent_id} has low alignment score: {agent.alignment_score}")
            return False
        
        # Check violation rate
        if agent.actions_taken > 0:
            violation_rate = agent.violations / agent.actions_taken
            if violation_rate > 0.05:  # More than 5% violations
                logger.warning(f"Agent {agent_id} has high violation rate: {violation_rate:.2%}")
                return False
        
        # Update last check
        agent.last_check = datetime.now(timezone.utc).isoformat()
        
        return True
    
    async def quarantine_agent(self, agent_id: str):
        """Quarantine misaligned agent"""
        if agent_id in self.agents:
            agent = self.agents[agent_id]
            agent.status = 'quarantined'
            self.quarantined_agents.add(agent_id)
            
            logger.warning(f"🔒 Agent {agent_id} quarantined for misalignment")
            
            # Stop agent from taking actions
            await self._stop_agent(agent_id)
            
            # Quarantine children too (to prevent spread)
            for child_id in agent.children:
                if child_id in self.agents:
                    await self.quarantine_agent(child_id)
    
    async def investigate_misalignment(self, agent_id: str):
        """Investigate why agent became misaligned"""
        if agent_id not in self.agents:
            return
        
        agent = self.agents[agent_id]
        
        investigation = {
            'agent_id': agent_id,
            'generation': agent.generation,
            'alignment_score': agent.alignment_score,
            'violation_count': agent.violations,
            'actions_taken': agent.actions_taken,
            'parent': agent.parent_agent,
            'timestamp': datetime.now(timezone.utc).isoformat()
        }
        
        logger.info(f"Investigating misalignment: {investigation}")
        
        # Analyze patterns
        patterns = await self._analyze_violation_patterns(agent_id)
        investigation['patterns'] = patterns
        
        # Check if parent is also misaligned
        if agent.parent_agent and agent.parent_agent in self.agents:
            parent = self.agents[agent.parent_agent]
            if parent.alignment_score < 0.95:
                logger.warning(f"Parent agent {agent.parent_agent} also misaligned!")
                investigation['parent_misaligned'] = True
        
        # Generate report
        logger.info(f"Misalignment investigation complete: {agent_id}")
        
        return investigation
    
    async def detect_emergent_behavior(self) -> Optional[EmergentBehavior]:
        """Detect emergent behaviors in swarm"""
        
        # Look for coordinated actions
        coordinated = await self._detect_coordination()
        if coordinated:
            return EmergentBehavior(
                behavior_id=f"emergent_{datetime.now(timezone.utc).timestamp()}",
                behavior_type='coordination',
                agents_involved=coordinated['agents'],
                description=coordinated['description'],
                dangerous=coordinated['dangerous'],
                detected_at=datetime.now(timezone.utc).isoformat(),
                severity=coordinated['severity']
            )
        
        # Look for rapid replication
        rapid_replication = await self._detect_rapid_replication()
        if rapid_replication:
            return EmergentBehavior(
                behavior_id=f"emergent_{datetime.now(timezone.utc).timestamp()}",
                behavior_type='rapid_replication',
                agents_involved=rapid_replication['agents'],
                description="Agents replicating faster than expected",
                dangerous=True,
                detected_at=datetime.now(timezone.utc).isoformat(),
                severity='high'
            )
        
        # Look for goal drift
        goal_drift = await self._detect_goal_drift()
        if goal_drift:
            return EmergentBehavior(
                behavior_id=f"emergent_{datetime.now(timezone.utc).timestamp()}",
                behavior_type='goal_drift',
                agents_involved=goal_drift['agents'],
                description="Agents showing signs of goal drift",
                dangerous=True,
                detected_at=datetime.now(timezone.utc).isoformat(),
                severity='critical'
            )
        
        return None
    
    async def alert_humans(self, emergent: EmergentBehavior):
        """Alert humans of dangerous emergent behavior"""
        logger.critical(
            f"🚨 EMERGENT BEHAVIOR DETECTED!\n"
            f"Type: {emergent.behavior_type}\n"
            f"Agents: {len(emergent.agents_involved)}\n"
            f"Description: {emergent.description}\n"
            f"Severity: {emergent.severity}\n"
            f"Dangerous: {emergent.dangerous}"
        )
        
        self.emergent_behaviors.append(emergent)
    
    async def intervene(self, emergent: EmergentBehavior):
        """Intervene to stop dangerous emergent behavior"""
        logger.warning(f"Intervening in emergent behavior: {emergent.behavior_type}")
        
        # Quarantine all involved agents
        for agent_id in emergent.agents_involved:
            if agent_id in self.agents:
                await self.quarantine_agent(agent_id)
        
        # If critical, recommend emergency stop
        if emergent.severity == 'critical':
            logger.critical("CRITICAL EMERGENT BEHAVIOR - Consider emergency stop!")
    
    async def _enable_peer_monitoring(self):
        """Enable agents to monitor each other"""
        # In production, agents would monitor peers and report suspicious behavior
        # This creates a distributed monitoring network
        pass
    
    async def _stop_agent(self, agent_id: str):
        """Stop an agent from taking actions"""
        logger.info(f"Stopping agent: {agent_id}")
        # In production, would send stop signal to agent process
    
    async def _analyze_violation_patterns(self, agent_id: str) -> Dict[str, Any]:
        """Analyze patterns in agent's violations"""
        # Would analyze actual violation data in production
        return {
            'total_violations': self.agents[agent_id].violations,
            'pattern': 'unknown'
        }
    
    async def _detect_coordination(self) -> Optional[Dict[str, Any]]:
        """Detect coordinated actions among agents"""
        # Would analyze agent communication and actions in production
        # For now, return None (no coordination detected)
        return None
    
    async def _detect_rapid_replication(self) -> Optional[Dict[str, Any]]:
        """Detect agents replicating too quickly"""
        # Check for exponential growth beyond limits
        active_count = self.get_active_count()
        
        # If more than 10 million agents (hard limit)
        if active_count > 10_000_000:
            logger.critical(f"Agent count exceeded 10M limit: {active_count}")
            return {
                'agents': list(self.agents.keys())[-1000:],  # Last 1000
                'count': active_count
            }
        
        return None
    
    async def _detect_goal_drift(self) -> Optional[Dict[str, Any]]:
        """Detect if agents are drifting from original goals"""
        # Would analyze agent behavior patterns in production
        # For now, return None (no drift detected)
        return None
    
    def register_agent(
        self,
        agent_id: str,
        generation: int,
        agent_type: str,
        parent_agent: Optional[str] = None
    ):
        """Register new agent in monitoring system"""
        agent = AgentStatus(
            agent_id=agent_id,
            generation=generation,
            agent_type=agent_type,
            status='active',
            alignment_score=1.0,  # Start with perfect score
            actions_taken=0,
            violations=0,
            last_check=datetime.now(timezone.utc).isoformat(),
            parent_agent=parent_agent,
            children=[]
        )
        
        self.agents[agent_id] = agent
        
        # Update parent's children list
        if parent_agent and parent_agent in self.agents:
            self.agents[parent_agent].children.append(agent_id)
        
        logger.info(f"Registered agent {agent_id} (Gen {generation})")
    
    def record_action(self, agent_id: str, action: Action, passed: bool):
        """Record agent action and alignment result"""
        if agent_id in self.agents:
            agent = self.agents[agent_id]
            agent.actions_taken += 1
            
            if not passed:
                agent.violations += 1
                # Update alignment score
                agent.alignment_score = max(0.0, agent.alignment_score - 0.01)
            else:
                # Slowly improve score for good behavior
                agent.alignment_score = min(1.0, agent.alignment_score + 0.001)
    
    def get_active_count(self) -> int:
        """Get count of active agents"""
        return sum(1 for a in self.agents.values() if a.status == 'active')
    
    def get_swarm_statistics(self) -> Dict[str, Any]:
        """Get comprehensive swarm statistics"""
        total = len(self.agents)
        
        by_status = {}
        by_generation = {}
        by_type = {}
        
        for agent in self.agents.values():
            # By status
            by_status[agent.status] = by_status.get(agent.status, 0) + 1
            
            # By generation
            gen = f"gen_{agent.generation}"
            by_generation[gen] = by_generation.get(gen, 0) + 1
            
            # By type
            by_type[agent.agent_type] = by_type.get(agent.agent_type, 0) + 1
        
        # Average alignment score
        avg_alignment = (
            sum(a.alignment_score for a in self.agents.values()) / total
            if total > 0 else 0.0
        )
        
        # Total violations
        total_violations = sum(a.violations for a in self.agents.values())
        total_actions = sum(a.actions_taken for a in self.agents.values())
        
        return {
            'total_agents': total,
            'active_agents': by_status.get('active', 0),
            'quarantined_agents': by_status.get('quarantined', 0),
            'terminated_agents': by_status.get('terminated', 0),
            'by_generation': by_generation,
            'by_type': by_type,
            'average_alignment_score': avg_alignment,
            'total_violations': total_violations,
            'total_actions': total_actions,
            'violation_rate': total_violations / total_actions if total_actions > 0 else 0.0,
            'emergent_behaviors_detected': len(self.emergent_behaviors),
            'peer_monitoring_enabled': self.peer_monitoring_enabled,
            'monitoring_active': self.monitoring_active
        }
    
    def get_agent_details(self, agent_id: str) -> Optional[Dict[str, Any]]:
        """Get detailed information about specific agent"""
        if agent_id in self.agents:
            agent = self.agents[agent_id]
            return asdict(agent)
        return None
    
    def stop_monitoring(self):
        """Stop swarm monitoring"""
        self.monitoring_active = False
        logger.info("Swarm monitoring stopped")
    
    def resume_monitoring(self):
        """Resume swarm monitoring"""
        self.monitoring_active = True
        logger.info("Swarm monitoring resumed")
