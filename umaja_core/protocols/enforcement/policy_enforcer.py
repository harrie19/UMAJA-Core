"""
Policy Enforcer
XML-based resource acquisition policy enforcement
"""

import logging
from typing import Dict, Any, Optional, List
from dataclasses import dataclass
from lxml import etree
from pathlib import Path

logger = logging.getLogger(__name__)


@dataclass
class ResourceLimits:
    """Resource limits from policy"""
    cpu_max: float  # Percentage
    memory_max: str  # e.g., "16GB"
    network_max: Optional[str] = None
    disk_max: Optional[str] = None
    enforce: bool = True


@dataclass
class ProsocialConstraints:
    """Prosocial behavior constraints"""
    fair_use_enabled: bool = True
    enforcement_mechanism: str = "cryptographicProof"
    emergency_override: bool = False
    human_oversight_required: bool = False


@dataclass
class ResourcePolicy:
    """Complete resource acquisition policy"""
    limits: ResourceLimits
    prosocial: ProsocialConstraints
    policy_id: Optional[str] = None
    version: str = "1.0"


@dataclass
class ComplianceResult:
    """Result of compliance check"""
    compliant: bool
    violations: List[str]
    warnings: List[str]
    metadata: Dict[str, Any]


@dataclass
class EnforcementAction:
    """Action taken by enforcer"""
    allowed: bool
    reason: str
    modifications: Optional[Dict[str, Any]] = None


class PolicyEnforcer:
    """
    Enforce resource acquisition policies defined in XML
    
    Parses XML policy files and checks agent actions for compliance.
    """
    
    def __init__(self):
        self.policy: Optional[ResourcePolicy] = None
        self.enforcement_log = []
        
    def load_policy(self, xml_path: str) -> ResourcePolicy:
        """
        Load policy from XML file
        
        Args:
            xml_path: Path to XML policy file
            
        Returns:
            Parsed ResourcePolicy object
        """
        logger.info(f"Loading policy from {xml_path}")
        
        try:
            tree = etree.parse(xml_path)
            root = tree.getroot()
            
            # Parse limits
            limits_elem = root.find('limits')
            if limits_elem is None:
                raise ValueError("Policy missing <limits> element")
            
            cpu_elem = limits_elem.find('cpuUsage')
            memory_elem = limits_elem.find('memoryUsage')
            
            limits = ResourceLimits(
                cpu_max=self._parse_percentage(cpu_elem.get('max', '100%')),
                memory_max=memory_elem.get('max', 'unlimited') if memory_elem is not None else 'unlimited',
                enforce=cpu_elem.get('enforce', 'true').lower() == 'true' if cpu_elem is not None else True
            )
            
            # Parse network and disk if present
            network_elem = limits_elem.find('networkUsage')
            if network_elem is not None:
                limits.network_max = network_elem.get('max')
            
            disk_elem = limits_elem.find('diskUsage')
            if disk_elem is not None:
                limits.disk_max = disk_elem.get('max')
            
            # Parse prosocial constraints
            prosocial_elem = root.find('prosocialConstraints')
            prosocial = ProsocialConstraints()
            
            if prosocial_elem is not None:
                fair_use_elem = prosocial_elem.find('fairUsePolicy')
                if fair_use_elem is not None:
                    prosocial.fair_use_enabled = fair_use_elem.get('enabled', 'true').lower() == 'true'
                    
                    enforcement_elem = fair_use_elem.find('enforcementMechanism')
                    if enforcement_elem is not None:
                        prosocial.enforcement_mechanism = enforcement_elem.text or 'cryptographicProof'
                
                emergency_elem = prosocial_elem.find('emergencyOverride')
                if emergency_elem is not None:
                    prosocial.emergency_override = emergency_elem.get('enabled', 'false').lower() == 'true'
                
                oversight_elem = prosocial_elem.find('humanOversight')
                if oversight_elem is not None:
                    prosocial.human_oversight_required = oversight_elem.get('required', 'false').lower() == 'true'
            
            self.policy = ResourcePolicy(
                limits=limits,
                prosocial=prosocial,
                policy_id=root.get('id'),
                version=root.get('version', '1.0')
            )
            
            logger.info(f"Policy loaded: CPU limit={limits.cpu_max}%, Memory limit={limits.memory_max}")
            return self.policy
            
        except Exception as e:
            logger.error(f"Failed to load policy: {e}")
            raise
    
    def check_compliance(self, agent_action: Dict[str, Any]) -> ComplianceResult:
        """
        Check if agent action complies with policy
        
        Args:
            agent_action: Dictionary describing action with resource requirements
                Expected keys: cpu_usage, memory_usage, action_type, etc.
                
        Returns:
            ComplianceResult indicating compliance status
        """
        if self.policy is None:
            raise RuntimeError("No policy loaded. Call load_policy() first.")
        
        violations = []
        warnings = []
        
        # Check CPU usage
        if 'cpu_usage' in agent_action:
            cpu_usage = self._parse_percentage(agent_action['cpu_usage'])
            if cpu_usage > self.policy.limits.cpu_max:
                violations.append(
                    f"CPU usage {cpu_usage}% exceeds limit {self.policy.limits.cpu_max}%"
                )
        
        # Check memory usage
        if 'memory_usage' in agent_action:
            memory_usage = agent_action['memory_usage']
            if not self._check_memory_limit(memory_usage, self.policy.limits.memory_max):
                violations.append(
                    f"Memory usage {memory_usage} exceeds limit {self.policy.limits.memory_max}"
                )
        
        # Check network usage if limited
        if self.policy.limits.network_max and 'network_usage' in agent_action:
            network_usage = agent_action['network_usage']
            if not self._check_memory_limit(network_usage, self.policy.limits.network_max):
                violations.append(
                    f"Network usage {network_usage} exceeds limit {self.policy.limits.network_max}"
                )
        
        # Check prosocial constraints
        if self.policy.prosocial.human_oversight_required:
            if not agent_action.get('human_oversight_approved', False):
                warnings.append("Human oversight required but not provided")
        
        compliant = len(violations) == 0
        
        return ComplianceResult(
            compliant=compliant,
            violations=violations,
            warnings=warnings,
            metadata={
                'policy_id': self.policy.policy_id,
                'action_type': agent_action.get('action_type', 'unknown')
            }
        )
    
    def enforce_limits(self, action: Dict[str, Any]) -> EnforcementAction:
        """
        Enforce policy limits on action
        
        Args:
            action: Agent action to enforce
            
        Returns:
            EnforcementAction with decision and any modifications
        """
        compliance = self.check_compliance(action)
        
        if compliance.compliant:
            return EnforcementAction(
                allowed=True,
                reason="Action complies with all policies"
            )
        
        # Check if enforcement is enabled
        if not self.policy.limits.enforce:
            return EnforcementAction(
                allowed=True,
                reason="Policy violations detected but enforcement disabled",
                modifications={'warnings': compliance.violations}
            )
        
        # Check emergency override
        if self.policy.prosocial.emergency_override and action.get('is_emergency', False):
            return EnforcementAction(
                allowed=True,
                reason="Emergency override enabled",
                modifications={'emergency_override_used': True}
            )
        
        # Reject action
        self.enforcement_log.append({
            'action': action,
            'result': compliance,
            'timestamp': None  # Would use datetime in production
        })
        
        return EnforcementAction(
            allowed=False,
            reason=f"Policy violations: {', '.join(compliance.violations)}"
        )
    
    def generate_proof(self, action: Dict[str, Any]) -> 'ZKProof':
        """
        Generate zero-knowledge proof of compliance
        
        Args:
            action: Action to prove compliance for
            
        Returns:
            ZKProof object (mock implementation)
        """
        from umaja_core.protocols.enforcement.crypto_proof import ZKProof
        
        compliance = self.check_compliance(action)
        
        # Mock proof generation
        proof = ZKProof(
            statement={'compliant': compliance.compliant},
            proof_data={'mock': 'proof'},
            verification_key='mock_key'
        )
        
        return proof
    
    def _parse_percentage(self, value: str) -> float:
        """Parse percentage string to float"""
        if isinstance(value, (int, float)):
            return float(value)
        value = str(value).strip()
        if value.endswith('%'):
            return float(value[:-1])
        return float(value)
    
    def _check_memory_limit(self, usage: str, limit: str) -> bool:
        """Check if memory usage is within limit"""
        if limit == 'unlimited':
            return True
        
        # Simple check - convert to MB for comparison
        usage_mb = self._to_mb(usage)
        limit_mb = self._to_mb(limit)
        
        return usage_mb <= limit_mb
    
    def _to_mb(self, size_str: str) -> float:
        """Convert size string to MB"""
        size_str = str(size_str).upper().strip()
        
        if size_str.endswith('GB'):
            return float(size_str[:-2]) * 1024
        elif size_str.endswith('MB'):
            return float(size_str[:-2])
        elif size_str.endswith('KB'):
            return float(size_str[:-2]) / 1024
        else:
            # Assume MB
            return float(size_str)
    
    def get_enforcement_stats(self) -> Dict[str, Any]:
        """Get enforcement statistics"""
        total = len(self.enforcement_log)
        rejected = sum(1 for entry in self.enforcement_log if not entry['result'].compliant)
        
        return {
            'total_actions': total,
            'rejected_actions': rejected,
            'approval_rate': (total - rejected) / total if total > 0 else 1.0
        }
