"""
UMAJA Core - Vector Meta-Language Protocol
Unified Machine Architecture for Joint Autonomy

This package implements AI-to-AI communication protocols with embedded
alignment and safety mechanisms.
"""

__version__ = "0.1.0"
__author__ = "UMAJA Project"

# Optional imports - only load when needed to support testing without heavy dependencies
__all__ = [
    'VectorCommEncoder',
    'SafetyPolytope',
    'PolicyEnforcer',
    'EthicalValueEncoder',
]

def __getattr__(name):
    """Lazy import to avoid loading heavy dependencies on package import"""
    if name == 'VectorCommEncoder':
        from umaja_core.protocols.vectorcomm.encoder import VectorCommEncoder
        return VectorCommEncoder
    elif name == 'SafetyPolytope':
        from umaja_core.protocols.safety.polytope import SafetyPolytope
        return SafetyPolytope
    elif name == 'PolicyEnforcer':
        from umaja_core.protocols.enforcement.policy_enforcer import PolicyEnforcer
        return PolicyEnforcer
    elif name == 'EthicalValueEncoder':
        from umaja_core.protocols.ethics.value_embeddings import EthicalValueEncoder
        return EthicalValueEncoder
    raise AttributeError(f"module '{__name__}' has no attribute '{name}'")
