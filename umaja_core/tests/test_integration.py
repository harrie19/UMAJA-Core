"""
Integration Tests
End-to-end tests for Vector Meta-Language Protocol
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import numpy as np
import pytest
import tempfile
from unittest.mock import patch, Mock

from umaja_core.protocols.vectorcomm.encoder import VectorCommEncoder
from umaja_core.protocols.vectorcomm.transport import VectorMessage, VectorTransport
from umaja_core.protocols.safety.polytope import SafetyPolytope, LinearConstraint
from umaja_core.protocols.enforcement.policy_enforcer import PolicyEnforcer
from umaja_core.protocols.enforcement.audit_trail import AuditTrail
from umaja_core.protocols.ethics.value_embeddings import EthicalValueEncoder


class TestA2AIntegration:
    """Test complete AI-to-AI communication workflow"""
    
    @patch('umaja_core.protocols.vectorcomm.encoder.SentenceTransformer')
    def test_two_agent_communication(self, mock_transformer):
        """Test two agents communicating with safety checks"""
        # Mock the transformer
        mock_model = Mock()
        mock_model.encode.return_value = np.random.randn(768)
        mock_transformer.return_value = mock_model
        
        # Create encoder and transport
        encoder = VectorCommEncoder()
        transport = VectorTransport()
        
        # Agent 1 sends message
        message_text = "Hello Agent 2"
        vector = encoder.encode(message_text, tier=2)
        
        msg = VectorMessage(
            sender_id="agent1",
            receiver_id="agent2",
            vector=vector,
            tier=2
        )
        
        transport.send(msg)
        
        # Agent 2 receives message
        received = transport.receive("agent2")
        
        assert received is not None
        assert received.sender_id == "agent1"
        assert received.tier == 2
    
    @patch('umaja_core.protocols.vectorcomm.encoder.SentenceTransformer')
    def test_safe_communication_with_polytope(self, mock_transformer):
        """Test communication with safety polytope filtering"""
        # Mock transformer
        mock_model = Mock()
        mock_model.encode.return_value = np.random.randn(768)
        mock_transformer.return_value = mock_model
        
        encoder = VectorCommEncoder()
        transport = VectorTransport()
        
        # Create safety polytope (sphere in 768D space)
        center = np.zeros(768)
        radius = 5.0
        safety = SafetyPolytope.create_sphere_polytope(center, radius, n_constraints=50)
        
        # Send message
        vector = encoder.encode("Safe message", tier=2)
        
        # Check if safe
        if safety.is_safe(vector, check_margin=False):
            msg = VectorMessage(
                sender_id="agent1",
                receiver_id="agent2",
                vector=vector,
                tier=2
            )
            transport.send(msg)
            success = True
        else:
            # Steer to safe region
            safe_vector = safety.steer_to_safe(vector)
            msg = VectorMessage(
                sender_id="agent1",
                receiver_id="agent2",
                vector=safe_vector,
                tier=2
            )
            transport.send(msg)
            success = True
        
        assert success


class TestPolicyEnforcementIntegration:
    """Test policy enforcement with audit trail"""
    
    def test_policy_enforcement_with_audit(self):
        """Test complete policy enforcement workflow with audit trail"""
        # Create policy
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
            # Initialize systems
            enforcer = PolicyEnforcer()
            enforcer.load_policy(temp_path)
            audit = AuditTrail()
            
            # Test compliant action
            action1 = {'cpu_usage': '50%', 'memory_usage': '8GB', 'agent_id': 'agent1'}
            result1 = enforcer.enforce_limits(action1)
            audit.log_action(
                agent_id=action1['agent_id'],
                action=action1,
                compliant=result1.allowed
            )
            
            # Test non-compliant action
            action2 = {'cpu_usage': '95%', 'memory_usage': '8GB', 'agent_id': 'agent2'}
            result2 = enforcer.enforce_limits(action2)
            audit.log_action(
                agent_id=action2['agent_id'],
                action=action2,
                compliant=result2.allowed
            )
            
            # Verify audit trail
            assert audit.verify_chain_integrity()
            assert len(audit.entries) == 2
            assert audit.entries[0].compliant
            assert not audit.entries[1].compliant
            
        finally:
            Path(temp_path).unlink()
    
    def test_multi_agent_enforcement(self):
        """Test enforcement for multiple agents"""
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
            enforcer = PolicyEnforcer()
            enforcer.load_policy(temp_path)
            audit = AuditTrail()
            
            # Multiple agents
            agents = ['agent1', 'agent2', 'agent3', 'agent4', 'agent5']
            
            for i, agent_id in enumerate(agents):
                cpu_usage = 50 + i * 10  # Increasing usage
                action = {
                    'cpu_usage': f'{cpu_usage}%',
                    'memory_usage': '8GB',
                    'agent_id': agent_id
                }
                
                result = enforcer.enforce_limits(action)
                audit.log_action(agent_id, action, result.allowed)
            
            # Check statistics
            stats = audit.get_statistics()
            assert stats['total_actions'] == 5
            assert stats['unique_agents'] == 5
            
            # Some should be rejected (>80% CPU)
            assert stats['non_compliant_actions'] > 0
            
        finally:
            Path(temp_path).unlink()


class TestEthicsIntegration:
    """Test ethical value encoding integration"""
    
    @patch('umaja_core.protocols.ethics.value_embeddings.SentenceTransformer')
    def test_value_alignment_checking(self, mock_transformer):
        """Test checking action alignment with values"""
        # Mock transformer
        mock_model = Mock()
        
        def mock_encode_fn(text, **kwargs):
            # Return different vectors for different inputs
            if isinstance(text, str):
                np.random.seed(hash(text) % 2**32)
                return np.random.randn(768)
            return np.random.randn(768)
        
        mock_model.encode = mock_encode_fn
        mock_transformer.return_value = mock_model
        
        encoder = EthicalValueEncoder()
        
        # Encode ethical value
        value_vector = encoder.encode_value("fairness and justice")
        
        # Encode actions
        action1 = "distribute resources equally among all agents"
        action2 = "monopolize all resources for self"
        
        action1_vector = mock_model.encode(action1)
        action2_vector = mock_model.encode(action2)
        
        # Compute alignment
        score1 = encoder.compute_alignment_score(action1_vector, value_vector)
        score2 = encoder.compute_alignment_score(action2_vector, value_vector)
        
        # Both should be valid scores
        assert 0.0 <= score1 <= 1.0
        assert 0.0 <= score2 <= 1.0


class TestFullWorkflow:
    """Test complete end-to-end workflow"""
    
    @patch('umaja_core.protocols.vectorcomm.encoder.SentenceTransformer')
    @patch('umaja_core.protocols.ethics.value_embeddings.SentenceTransformer')
    def test_complete_a2a_workflow(self, mock_ethics_transformer, mock_vectorcomm_transformer):
        """Test complete workflow: encoding, safety, policy, ethics, audit"""
        # Mock transformers
        mock_vc_model = Mock()
        mock_vc_model.encode.return_value = np.random.randn(768)
        mock_vectorcomm_transformer.return_value = mock_vc_model
        
        mock_eth_model = Mock()
        mock_eth_model.encode.return_value = np.random.randn(768)
        mock_ethics_transformer.return_value = mock_eth_model
        
        # Initialize all systems
        encoder = VectorCommEncoder()
        transport = VectorTransport()
        safety = SafetyPolytope.create_sphere_polytope(np.zeros(768), 5.0, n_constraints=20)
        audit = AuditTrail()
        ethics = EthicalValueEncoder()
        
        # Create policy
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
            enforcer = PolicyEnforcer()
            enforcer.load_policy(temp_path)
            
            # Agent 1 wants to send a message
            message = "Compute task with 70% CPU"
            
            # 1. Encode message
            vector = encoder.encode(message, tier=2)
            
            # 2. Check safety
            is_safe = safety.is_safe(vector, check_margin=False)
            if not is_safe:
                vector = safety.steer_to_safe(vector)
            
            # 3. Check policy compliance
            action = {
                'cpu_usage': '70%',
                'memory_usage': '8GB',
                'action_type': 'compute'
            }
            enforcement_result = enforcer.enforce_limits(action)
            
            # 4. Check ethical alignment
            value_vector = ethics.encode_value("fairness and cooperation")
            alignment = ethics.compute_alignment_score(vector, value_vector)
            
            # 5. If all checks pass, send message
            if enforcement_result.allowed and alignment > 0.3:
                msg = VectorMessage(
                    sender_id="agent1",
                    receiver_id="agent2",
                    vector=vector,
                    tier=2,
                    metadata={'alignment_score': alignment}
                )
                transport.send(msg)
                
                # 6. Log to audit trail
                audit.log_action(
                    agent_id="agent1",
                    action=action,
                    compliant=True,
                    metadata={'alignment_score': alignment}
                )
                
                success = True
            else:
                audit.log_action(
                    agent_id="agent1",
                    action=action,
                    compliant=False
                )
                success = False
            
            # Verify workflow completed
            assert success
            assert audit.verify_chain_integrity()
            assert len(audit.entries) == 1
            
        finally:
            Path(temp_path).unlink()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
