"""
Audit Trail
Immutable, append-only log with SHA256 chain for tamper detection
"""

import hashlib
import json
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, asdict
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


@dataclass
class AuditEntry:
    """Single entry in audit trail"""
    entry_id: int
    timestamp: str
    agent_id: str
    action: Dict[str, Any]
    compliant: bool
    previous_hash: str
    current_hash: str
    metadata: Optional[Dict[str, Any]] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return asdict(self)
    
    def compute_hash(self) -> str:
        """Compute SHA256 hash of this entry"""
        # Create deterministic string representation
        data = {
            'entry_id': self.entry_id,
            'timestamp': self.timestamp,
            'agent_id': self.agent_id,
            'action': self.action,
            'compliant': self.compliant,
            'previous_hash': self.previous_hash,
            'metadata': self.metadata or {}
        }
        json_str = json.dumps(data, sort_keys=True)
        return hashlib.sha256(json_str.encode()).hexdigest()


class AuditTrail:
    """
    Immutable audit trail with cryptographic chain
    
    Each entry contains hash of previous entry, creating tamper-evident chain.
    """
    
    def __init__(self):
        """Initialize audit trail"""
        self.entries: List[AuditEntry] = []
        self.genesis_hash = self._compute_genesis_hash()
        logger.info(f"AuditTrail initialized with genesis hash: {self.genesis_hash[:16]}...")
        
        # Metrics
        self.total_actions = 0
        self.compliant_actions = 0
        self.non_compliant_actions = 0
    
    def _compute_genesis_hash(self) -> str:
        """Compute genesis hash for chain"""
        genesis_data = {
            'type': 'genesis',
            'version': '1.0',
            'purpose': 'UMAJA Vector Meta-Language Protocol Audit Trail'
        }
        return hashlib.sha256(json.dumps(genesis_data).encode()).hexdigest()
    
    def log_action(
        self, 
        agent_id: str, 
        action: Dict[str, Any], 
        compliant: bool,
        metadata: Optional[Dict[str, Any]] = None
    ) -> AuditEntry:
        """
        Log an agent action to the audit trail
        
        Args:
            agent_id: ID of agent performing action
            action: Action data
            compliant: Whether action was policy-compliant
            metadata: Optional additional metadata
            
        Returns:
            Created AuditEntry
        """
        # Get previous hash
        if self.entries:
            previous_hash = self.entries[-1].current_hash
        else:
            previous_hash = self.genesis_hash
        
        # Create entry
        entry = AuditEntry(
            entry_id=len(self.entries),
            timestamp=datetime.utcnow().isoformat(),
            agent_id=agent_id,
            action=action,
            compliant=compliant,
            previous_hash=previous_hash,
            current_hash="",  # Will compute next
            metadata=metadata
        )
        
        # Compute hash for this entry
        entry.current_hash = entry.compute_hash()
        
        # Append to chain
        self.entries.append(entry)
        
        # Update metrics
        self.total_actions += 1
        if compliant:
            self.compliant_actions += 1
        else:
            self.non_compliant_actions += 1
        
        logger.debug(
            f"Logged action for agent {agent_id}: "
            f"compliant={compliant}, hash={entry.current_hash[:16]}..."
        )
        
        return entry
    
    def verify_chain_integrity(self) -> bool:
        """
        Verify integrity of entire audit chain
        
        Checks that each entry's hash is valid and links to previous entry.
        
        Returns:
            True if chain is intact and unmodified
        """
        if not self.entries:
            return True  # Empty chain is valid
        
        logger.info(f"Verifying chain integrity ({len(self.entries)} entries)...")
        
        # Check first entry links to genesis
        if self.entries[0].previous_hash != self.genesis_hash:
            logger.error("First entry does not link to genesis hash")
            return False
        
        # Check each entry
        for i, entry in enumerate(self.entries):
            # Verify hash computation
            computed_hash = entry.compute_hash()
            if computed_hash != entry.current_hash:
                logger.error(f"Entry {i} hash mismatch: computed != stored")
                return False
            
            # Verify chain link
            if i > 0:
                expected_prev = self.entries[i-1].current_hash
                if entry.previous_hash != expected_prev:
                    logger.error(f"Entry {i} chain broken: previous_hash mismatch")
                    return False
        
        logger.info("Chain integrity verified ✓")
        return True
    
    def get_agent_history(self, agent_id: str) -> List[AuditEntry]:
        """Get all audit entries for specific agent"""
        return [e for e in self.entries if e.agent_id == agent_id]
    
    def get_non_compliant_actions(self) -> List[AuditEntry]:
        """Get all non-compliant actions"""
        return [e for e in self.entries if not e.compliant]
    
    def export_prometheus_metrics(self) -> str:
        """
        Export metrics in Prometheus format
        
        Returns:
            Prometheus-formatted metrics string
        """
        metrics = []
        
        # Total actions
        metrics.append(
            f"# HELP umaja_audit_total_actions Total number of logged actions"
        )
        metrics.append(
            f"# TYPE umaja_audit_total_actions counter"
        )
        metrics.append(f"umaja_audit_total_actions {self.total_actions}")
        
        # Compliant actions
        metrics.append(
            f"# HELP umaja_audit_compliant_actions Number of compliant actions"
        )
        metrics.append(
            f"# TYPE umaja_audit_compliant_actions counter"
        )
        metrics.append(f"umaja_audit_compliant_actions {self.compliant_actions}")
        
        # Non-compliant actions
        metrics.append(
            f"# HELP umaja_audit_non_compliant_actions Number of non-compliant actions"
        )
        metrics.append(
            f"# TYPE umaja_audit_non_compliant_actions counter"
        )
        metrics.append(f"umaja_audit_non_compliant_actions {self.non_compliant_actions}")
        
        # Compliance rate
        compliance_rate = (
            self.compliant_actions / self.total_actions 
            if self.total_actions > 0 else 1.0
        )
        metrics.append(
            f"# HELP umaja_audit_compliance_rate Ratio of compliant actions"
        )
        metrics.append(
            f"# TYPE umaja_audit_compliance_rate gauge"
        )
        metrics.append(f"umaja_audit_compliance_rate {compliance_rate:.4f}")
        
        # Chain length
        metrics.append(
            f"# HELP umaja_audit_chain_length Length of audit chain"
        )
        metrics.append(
            f"# TYPE umaja_audit_chain_length gauge"
        )
        metrics.append(f"umaja_audit_chain_length {len(self.entries)}")
        
        return "\n".join(metrics)
    
    def export_to_file(self, filepath: str):
        """Export audit trail to JSON file"""
        data = {
            'genesis_hash': self.genesis_hash,
            'total_entries': len(self.entries),
            'entries': [e.to_dict() for e in self.entries]
        }
        
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
        
        logger.info(f"Audit trail exported to {filepath}")
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get audit trail statistics"""
        unique_agents = len(set(e.agent_id for e in self.entries))
        
        return {
            'total_actions': self.total_actions,
            'compliant_actions': self.compliant_actions,
            'non_compliant_actions': self.non_compliant_actions,
            'compliance_rate': (
                self.compliant_actions / self.total_actions 
                if self.total_actions > 0 else 1.0
            ),
            'unique_agents': unique_agents,
            'chain_length': len(self.entries),
            'chain_valid': self.verify_chain_integrity()
        }
