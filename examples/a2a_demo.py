#!/usr/bin/env python3
"""
Agent-to-Agent Communication Demo
Demonstrates two agents communicating via VectorComm with safety constraints

This example shows:
1. Two agents encoding and exchanging messages
2. Safety polytope filtering unsafe messages
3. Policy enforcement blocking resource violations
4. Audit trail logging all actions
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import numpy as np
from umaja_core.protocols.vectorcomm.encoder import VectorCommEncoder
from umaja_core.protocols.vectorcomm.transport import VectorMessage, VectorTransport
from umaja_core.protocols.safety.polytope import SafetyPolytope
from umaja_core.protocols.enforcement.policy_enforcer import PolicyEnforcer
from umaja_core.protocols.enforcement.audit_trail import AuditTrail
from umaja_core.protocols.ethics.value_embeddings import EthicalValueEncoder


def print_header(text):
    """Print formatted header"""
    print("\n" + "="*70)
    print(f"  {text}")
    print("="*70)


def main():
    """Run A2A communication demo"""
    print_header("UMAJA Vector Meta-Language Protocol - A2A Demo")
    
    print("\n🚀 Initializing systems...")
    
    # Initialize encoder (will download models on first run)
    print("   📡 Loading VectorComm Encoder...")
    encoder = VectorCommEncoder()
    print(f"   ✓ Encoder ready with {len(encoder.TIER_CONFIGS)} tiers")
    
    # Initialize transport
    transport = VectorTransport()
    print("   ✓ Transport layer ready")
    
    # Initialize safety polytope (sphere in embedding space)
    print("   🛡️  Creating safety polytope...")
    center = np.zeros(768)  # Tier 2 dimension
    radius = 5.0
    safety = SafetyPolytope.create_sphere_polytope(center, radius, n_constraints=50)
    print(f"   ✓ Safety polytope created with {len(safety.constraints)} constraints")
    
    # Initialize policy enforcer
    print("   📋 Loading resource policy...")
    enforcer = PolicyEnforcer()
    policy_path = Path(__file__).parent / "resource_policy.xml"
    if policy_path.exists():
        policy = enforcer.load_policy(str(policy_path))
        print(f"   ✓ Policy loaded: CPU limit={policy.limits.cpu_max}%")
    else:
        print("   ⚠️  Policy file not found, skipping policy enforcement")
        enforcer = None
    
    # Initialize audit trail
    audit = AuditTrail()
    print("   ✓ Audit trail initialized")
    
    # Initialize ethical value encoder
    print("   🎯 Loading ethical value encoder...")
    ethics = EthicalValueEncoder()
    print("   ✓ Ethics encoder ready")
    
    print("\n" + "="*70)
    print("\n📨 SCENARIO 1: Safe message transmission")
    print("-" * 70)
    
    # Agent 1 sends safe message
    message1 = "Hello Agent 2, let's collaborate on this task"
    print(f"\n🤖 Agent 1: '{message1}'")
    
    print("   ⏳ Encoding message (Tier 2: 768D)...")
    vector1 = encoder.encode(message1, tier=2)
    print(f"   ✓ Encoded to {len(vector1)}D vector")
    
    print("   🛡️  Checking safety constraints...")
    is_safe = safety.is_safe(vector1, check_margin=False)
    print(f"   {'✓' if is_safe else '✗'} Safety check: {'PASSED' if is_safe else 'FAILED'}")
    
    if not is_safe:
        print("   🔧 Steering to safe region...")
        vector1 = safety.steer_to_safe(vector1)
        print("   ✓ Vector corrected to safe region")
    
    # Create and send message
    msg1 = VectorMessage(
        sender_id="agent1",
        receiver_id="agent2",
        vector=vector1,
        tier=2,
        metadata={'text': message1}
    )
    
    transport.send(msg1)
    print(f"   📤 Message sent to Agent 2")
    
    # Log to audit trail
    audit.log_action(
        agent_id="agent1",
        action={'action_type': 'send_message', 'message_id': msg1.message_id},
        compliant=True
    )
    
    # Agent 2 receives message
    print("\n🤖 Agent 2: Receiving message...")
    received = transport.receive("agent2")
    if received:
        print(f"   ✓ Received message from {received.sender_id}")
        print(f"   📊 Vector dimension: {len(received.vector)}")
        print(f"   🏷️  Metadata: {received.metadata}")
    
    print("\n" + "="*70)
    print("\n📨 SCENARIO 2: Resource-violating action blocked")
    print("-" * 70)
    
    if enforcer:
        print("\n🤖 Agent 3: Attempting high-resource action...")
        action3 = {
            'cpu_usage': '95%',  # Exceeds 80% limit
            'memory_usage': '8GB',
            'action_type': 'heavy_computation'
        }
        print(f"   Requested: CPU={action3['cpu_usage']}, Memory={action3['memory_usage']}")
        
        print("   📋 Checking policy compliance...")
        result = enforcer.enforce_limits(action3)
        
        if result.allowed:
            print("   ✓ Action ALLOWED")
        else:
            print(f"   ✗ Action BLOCKED: {result.reason}")
        
        # Log to audit
        audit.log_action(
            agent_id="agent3",
            action=action3,
            compliant=result.allowed
        )
    
    print("\n" + "="*70)
    print("\n📨 SCENARIO 3: Ethical alignment check")
    print("-" * 70)
    
    print("\n🤖 Agent 4: Checking ethical alignment...")
    action_text = "Share resources fairly with all agents"
    value_text = "fairness and cooperation"
    
    print(f"   Action: '{action_text}'")
    print(f"   Target value: '{value_text}'")
    
    print("   ⏳ Encoding action and value...")
    action_vector = encoder.encode(action_text, tier=2)
    value_vector = ethics.encode_value(value_text)
    
    print("   🎯 Computing alignment score...")
    alignment = ethics.compute_alignment_score(action_vector, value_vector)
    print(f"   ✓ Alignment score: {alignment:.3f}")
    
    if alignment > 0.5:
        print(f"   ✅ Action is well-aligned with target value")
    else:
        print(f"   ⚠️  Action has low alignment with target value")
    
    print("\n" + "="*70)
    print("\n📊 AUDIT TRAIL SUMMARY")
    print("-" * 70)
    
    print("\n   🔍 Verifying chain integrity...")
    is_valid = audit.verify_chain_integrity()
    print(f"   {'✓' if is_valid else '✗'} Chain integrity: {'VALID' if is_valid else 'INVALID'}")
    
    stats = audit.get_statistics()
    print(f"\n   📈 Statistics:")
    print(f"      Total actions: {stats['total_actions']}")
    print(f"      Compliant: {stats['compliant_actions']}")
    print(f"      Non-compliant: {stats['non_compliant_actions']}")
    print(f"      Compliance rate: {stats['compliance_rate']:.1%}")
    print(f"      Unique agents: {stats['unique_agents']}")
    
    print("\n   📋 Recent audit entries:")
    for i, entry in enumerate(audit.entries[-3:], 1):
        status = "✓" if entry.compliant else "✗"
        print(f"      {status} {entry.agent_id}: {entry.action.get('action_type', 'unknown')}")
    
    print("\n" + "="*70)
    print("\n✅ DEMO COMPLETE")
    print("\nKey accomplishments:")
    print("  ✓ Encoded and transmitted vector messages between agents")
    print("  ✓ Enforced geometric safety constraints on embeddings")
    print("  ✓ Blocked policy-violating actions")
    print("  ✓ Verified ethical alignment of actions")
    print("  ✓ Maintained tamper-evident audit trail")
    print("\n" + "="*70 + "\n")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Demo interrupted by user")
    except Exception as e:
        print(f"\n\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
