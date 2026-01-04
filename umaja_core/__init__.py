"""
UMAJA Core - Vector Meta-Language Protocol
Unified Machine Architecture for Joint Autonomy

This package implements AI-to-AI communication protocols with embedded
alignment and safety mechanisms.
"""

__version__ = "0.1.0"
__author__ = "UMAJA Project"

from umaja_core.protocols.vectorcomm.encoder import VectorCommEncoder
from umaja_core.protocols.safety.polytope import SafetyPolytope
from umaja_core.protocols.enforcement.policy_enforcer import PolicyEnforcer
from umaja_core.protocols.ethics.value_embeddings import EthicalValueEncoder

__all__ = [
    'VectorCommEncoder',
    'SafetyPolytope',
    'PolicyEnforcer',
    'EthicalValueEncoder',
]
