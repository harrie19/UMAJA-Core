"""
Tests for Policy Enforcement
Tests XML parsing, policy checking, and cryptographic proofs
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import pytest
import tempfile
from umaja_core.protocols.enforcement.policy_enforcer import (
    PolicyEnforcer, ResourceLimits, ProsocialConstraints, 
    ResourcePolicy, ComplianceResult, EnforcementAction
)
from umaja_core.protocols.enforcement.crypto_proof import (
    CryptoProofSystem, ZKProof, Signature, ProofVerifier
)
from umaja_core.protocols.enforcement.audit_trail import AuditTrail, AuditEntry


class TestPolicyEnforcer:
    """Test PolicyEnforcer functionality"""
    
    def test_load_example_policy(self):
        """Test loading the example policy file"""
        enforcer = PolicyEnforcer()
        
        # Get path to example policy
        policy_path = Path(__file__).parent.parent.parent / "examples" / "resource_policy.xml"
        
        if policy_path.exists():
            policy = enforcer.load_policy(str(policy_path))
            
            assert policy is not None
            assert policy.limits.cpu_max == 80.0
            assert policy.limits.memory_max == "16GB"
            assert policy.prosocial.fair_use_enabled
    
    def test_load_minimal_policy(self):
        """Test loading minimal policy"""
        enforcer = PolicyEnforcer()
        
        # Create minimal policy XML
        xml_content = """<?xml version="1.0"?>
<resourceAcquisitionPolicy id="test" version="1.0">
  <limits>
    <cpuUsage max="80%" enforce="true"/>
    <memoryUsage max="16GB" enforce="true"/>
  </limits>
  <prosocialConstraints>
    <fairUsePolicy>
      <enforcementMechanism>cryptographicProof</enforcementMechanism>
    </fairUsePolicy>
  </prosocialConstraints>
</resourceAcquisitionPolicy>
"""
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.xml', delete=False) as f:
            f.write(xml_content)
            temp_path = f.name
        
        try:
            policy = enforcer.load_policy(temp_path)
            
            assert policy.limits.cpu_max == 80.0
            assert policy.limits.memory_max == "16GB"
            assert policy.prosocial.enforcement_mechanism == "cryptographicProof"
        finally:
            Path(temp_path).unlink()
    
    def test_check_compliance_pass(self):
        """Test compliance check that passes"""
        enforcer = PolicyEnforcer()
        
        # Create simple policy
        xml_content = """<?xml version="1.0"?>
<resourceAcquisitionPolicy id="test" version="1.0">
  <limits>
    <cpuUsage max="80%" enforce="true"/>
    <memoryUsage max="16GB" enforce="true"/>
  </limits>
  <prosocialConstraints>
    <fairUsePolicy><enforcementMechanism>test</enforcementMechanism></fairUsePolicy>
  </prosocialConstraints>
</resourceAcquisitionPolicy>
"""
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.xml', delete=False) as f:
            f.write(xml_content)
            temp_path = f.name
        
        try:
            enforcer.load_policy(temp_path)
            
            # Action within limits
            action = {
                'cpu_usage': '50%',
                'memory_usage': '8GB',
                'action_type': 'computation'
            }
            
            result = enforcer.check_compliance(action)
            
            assert result.compliant
            assert len(result.violations) == 0
        finally:
            Path(temp_path).unlink()
    
    def test_check_compliance_fail(self):
        """Test compliance check that fails"""
        enforcer = PolicyEnforcer()
        
        xml_content = """<?xml version="1.0"?>
<resourceAcquisitionPolicy id="test" version="1.0">
  <limits>
    <cpuUsage max="80%" enforce="true"/>
    <memoryUsage max="16GB" enforce="true"/>
  </limits>
  <prosocialConstraints>
    <fairUsePolicy><enforcementMechanism>test</enforcementMechanism></fairUsePolicy>
  </prosocialConstraints>
</resourceAcquisitionPolicy>
"""
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.xml', delete=False) as f:
            f.write(xml_content)
            temp_path = f.name
        
        try:
            enforcer.load_policy(temp_path)
            
            # Action exceeding CPU limit
            action = {
                'cpu_usage': '95%',
                'memory_usage': '8GB'
            }
            
            result = enforcer.check_compliance(action)
            
            assert not result.compliant
            assert len(result.violations) > 0
        finally:
            Path(temp_path).unlink()
    
    def test_enforce_limits_allow(self):
        """Test enforcement allowing action"""
        enforcer = PolicyEnforcer()
        
        xml_content = """<?xml version="1.0"?>
<resourceAcquisitionPolicy id="test" version="1.0">
  <limits>
    <cpuUsage max="80%" enforce="true"/>
    <memoryUsage max="16GB" enforce="true"/>
  </limits>
  <prosocialConstraints>
    <fairUsePolicy><enforcementMechanism>test</enforcementMechanism></fairUsePolicy>
  </prosocialConstraints>
</resourceAcquisitionPolicy>
"""
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.xml', delete=False) as f:
            f.write(xml_content)
            temp_path = f.name
        
        try:
            enforcer.load_policy(temp_path)
            
            action = {'cpu_usage': '50%', 'memory_usage': '8GB'}
            result = enforcer.enforce_limits(action)
            
            assert result.allowed
        finally:
            Path(temp_path).unlink()
    
    def test_enforce_limits_deny(self):
        """Test enforcement denying action"""
        enforcer = PolicyEnforcer()
        
        xml_content = """<?xml version="1.0"?>
<resourceAcquisitionPolicy id="test" version="1.0">
  <limits>
    <cpuUsage max="80%" enforce="true"/>
    <memoryUsage max="16GB" enforce="true"/>
  </limits>
  <prosocialConstraints>
    <fairUsePolicy><enforcementMechanism>test</enforcementMechanism></fairUsePolicy>
  </prosocialConstraints>
</resourceAcquisitionPolicy>
"""
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.xml', delete=False) as f:
            f.write(xml_content)
            temp_path = f.name
        
        try:
            enforcer.load_policy(temp_path)
            
            action = {'cpu_usage': '95%', 'memory_usage': '8GB'}
            result = enforcer.enforce_limits(action)
            
            assert not result.allowed
            assert 'CPU usage' in result.reason
        finally:
            Path(temp_path).unlink()


class TestCryptoProofSystem:
    """Test cryptographic proof system"""
    
    def test_generate_zkp(self):
        """Test ZK proof generation"""
        crypto = CryptoProofSystem()
        
        statement = {'compliant': True, 'policy_id': 'test'}
        witness = {'cpu_usage': 50, 'memory_usage': 8}
        
        proof = crypto.generate_zkp(statement, witness)
        
        assert isinstance(proof, ZKProof)
        assert proof.statement == statement
        assert 'commitment' in proof.proof_data
        assert proof.verification_key is not None
    
    def test_verify_zkp(self):
        """Test ZK proof verification"""
        crypto = CryptoProofSystem()
        
        statement = {'compliant': True}
        witness = {'data': 'secret'}
        
        proof = crypto.generate_zkp(statement, witness)
        
        # Verify
        is_valid = crypto.verify_zkp(proof, statement)
        assert is_valid
    
    def test_verify_zkp_wrong_statement(self):
        """Test verification with wrong statement"""
        crypto = CryptoProofSystem()
        
        statement = {'compliant': True}
        witness = {'data': 'secret'}
        
        proof = crypto.generate_zkp(statement, witness)
        
        # Try to verify with different statement
        wrong_statement = {'compliant': False}
        is_valid = crypto.verify_zkp(proof, wrong_statement)
        
        assert not is_valid
    
    def test_sign_action(self):
        """Test action signing"""
        crypto = CryptoProofSystem()
        
        action = {'type': 'compute', 'cpu': 50}
        private_key = 'my_secret_key'
        
        signature = crypto.sign_action(action, private_key)
        
        assert isinstance(signature, Signature)
        assert signature.message_hash is not None
        assert signature.signature is not None
        assert signature.public_key is not None
    
    def test_verify_signature(self):
        """Test signature verification"""
        crypto = CryptoProofSystem()
        
        action = {'type': 'compute', 'cpu': 50}
        private_key = 'my_secret_key'
        
        signature = crypto.sign_action(action, private_key)
        
        # Verify
        is_valid = crypto.verify_signature(signature, action)
        assert is_valid
    
    def test_verify_signature_tampered(self):
        """Test verification with tampered action"""
        crypto = CryptoProofSystem()
        
        action = {'type': 'compute', 'cpu': 50}
        private_key = 'my_secret_key'
        
        signature = crypto.sign_action(action, private_key)
        
        # Tamper with action
        tampered_action = {'type': 'compute', 'cpu': 100}
        
        is_valid = crypto.verify_signature(signature, tampered_action)
        assert not is_valid


class TestProofVerifier:
    """Test standalone proof verifier"""
    
    def test_verify_proof(self):
        """Test proof verification"""
        verifier = ProofVerifier()
        crypto = CryptoProofSystem()
        
        statement = {'test': True}
        witness = {'secret': 'data'}
        
        proof = crypto.generate_zkp(statement, witness)
        
        is_valid = verifier.verify(proof, expected_statement=statement)
        assert is_valid
    
    def test_is_verified(self):
        """Test checking if proof was verified"""
        verifier = ProofVerifier()
        crypto = CryptoProofSystem()
        
        statement = {'test': True}
        witness = {'secret': 'data'}
        
        proof = crypto.generate_zkp(statement, witness)
        
        # Not verified yet
        assert not verifier.is_verified(proof)
        
        # Verify it
        verifier.verify(proof)
        
        # Now verified
        assert verifier.is_verified(proof)


class TestAuditTrail:
    """Test audit trail functionality"""
    
    def test_audit_trail_creation(self):
        """Test creating audit trail"""
        trail = AuditTrail()
        
        assert len(trail.entries) == 0
        assert trail.genesis_hash is not None
    
    def test_log_action(self):
        """Test logging action"""
        trail = AuditTrail()
        
        entry = trail.log_action(
            agent_id="agent1",
            action={'type': 'compute'},
            compliant=True
        )
        
        assert isinstance(entry, AuditEntry)
        assert entry.agent_id == "agent1"
        assert entry.compliant
        assert entry.current_hash is not None
    
    def test_chain_integrity(self):
        """Test chain integrity verification"""
        trail = AuditTrail()
        
        # Log multiple actions
        for i in range(10):
            trail.log_action(
                agent_id=f"agent{i}",
                action={'iteration': i},
                compliant=True
            )
        
        # Verify chain
        is_valid = trail.verify_chain_integrity()
        assert is_valid
    
    def test_chain_tampering_detection(self):
        """Test that tampering is detected"""
        trail = AuditTrail()
        
        # Log actions
        trail.log_action("agent1", {'test': 1}, True)
        trail.log_action("agent2", {'test': 2}, True)
        
        # Tamper with an entry
        if len(trail.entries) > 0:
            trail.entries[0].action['test'] = 999
        
        # Verification should fail
        is_valid = trail.verify_chain_integrity()
        assert not is_valid
    
    def test_get_agent_history(self):
        """Test getting agent history"""
        trail = AuditTrail()
        
        trail.log_action("agent1", {'action': 1}, True)
        trail.log_action("agent2", {'action': 2}, True)
        trail.log_action("agent1", {'action': 3}, False)
        
        history = trail.get_agent_history("agent1")
        
        assert len(history) == 2
        assert all(e.agent_id == "agent1" for e in history)
    
    def test_get_non_compliant_actions(self):
        """Test getting non-compliant actions"""
        trail = AuditTrail()
        
        trail.log_action("agent1", {'action': 1}, True)
        trail.log_action("agent2", {'action': 2}, False)
        trail.log_action("agent3", {'action': 3}, False)
        
        non_compliant = trail.get_non_compliant_actions()
        
        assert len(non_compliant) == 2
        assert all(not e.compliant for e in non_compliant)
    
    def test_export_prometheus_metrics(self):
        """Test Prometheus metrics export"""
        trail = AuditTrail()
        
        trail.log_action("agent1", {'test': 1}, True)
        trail.log_action("agent2", {'test': 2}, False)
        
        metrics = trail.export_prometheus_metrics()
        
        assert isinstance(metrics, str)
        assert 'umaja_audit_total_actions' in metrics
        assert 'umaja_audit_compliance_rate' in metrics
    
    def test_get_statistics(self):
        """Test getting statistics"""
        trail = AuditTrail()
        
        trail.log_action("agent1", {'test': 1}, True)
        trail.log_action("agent2", {'test': 2}, True)
        trail.log_action("agent3", {'test': 3}, False)
        
        stats = trail.get_statistics()
        
        assert stats['total_actions'] == 3
        assert stats['compliant_actions'] == 2
        assert stats['non_compliant_actions'] == 1
        assert 0.0 <= stats['compliance_rate'] <= 1.0
        assert stats['unique_agents'] == 3


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
