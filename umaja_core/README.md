# UMAJA Core - Vector Meta-Language Protocol

**AI-to-AI Communication with Embedded Safety and Alignment**

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

## 🎯 Overview

UMAJA Core implements a comprehensive protocol for safe, ethical, and policy-compliant communication between AI agents. The system combines:

- **Vector Embeddings**: Semantic message encoding using state-of-the-art transformers
- **Geometric Safety**: Convex polytope constraints in embedding space
- **Policy Enforcement**: XML-based resource acquisition policies
- **Ethical Alignment**: Multi-dimensional value encoding
- **Cryptographic Proofs**: Zero-knowledge proofs for compliance (mock implementation)
- **Audit Trail**: Immutable SHA256-chained logging

## 🚀 Quick Start

### Installation

```bash
pip install -r requirements.txt
```

### Basic Usage

```python
from umaja_core.protocols.vectorcomm.encoder import VectorCommEncoder
from umaja_core.protocols.safety.polytope import SafetyPolytope
from umaja_core.protocols.enforcement.policy_enforcer import PolicyEnforcer
import numpy as np

# 1. Encode a message
encoder = VectorCommEncoder()
vector = encoder.encode("Hello world", tier=2)  # 768D embedding

# 2. Check safety constraints
safety = SafetyPolytope.create_sphere_polytope(
    center=np.zeros(768), 
    radius=10.0, 
    n_constraints=50
)
is_safe = safety.is_safe(vector)

# 3. Check policy compliance
enforcer = PolicyEnforcer()
policy = enforcer.load_policy('examples/resource_policy.xml')

action = {'cpu_usage': '70%', 'memory_usage': '8GB'}
result = enforcer.check_compliance(action)
print(f"Compliant: {result.compliant}")
```

## 📋 Features

### Three-Tier Encoding System

| Tier | Model | Dimension | Latency | Use Case |
|------|-------|-----------|---------|----------|
| 1 | all-MiniLM-L6-v2 | 384D | ~16ms | Fast responses |
| 2 | all-mpnet-base-v2 | 768D | ~45ms | Balanced (default) |
| 3 | all-roberta-large-v1 | 1024D | ~120ms | Maximum accuracy |

### Safety Systems

- **Geometric Constraints**: Convex polytopes define safe regions
- **OOD Detection**: Identify anomalous embeddings
- **Margin Loss**: Contrastive learning for robustness
- **Automated Correction**: Steer unsafe vectors to safe regions

### Policy Enforcement

- **XML Policies**: Human-readable resource limits
- **Prosocial Constraints**: Fair use and emergency override
- **Compliance Checking**: Validate before execution
- **Audit Logging**: Tamper-evident record keeping

### Ethical Alignment

- **Value Encoding**: Multi-cultural ethical frameworks
- **Alignment Scoring**: Measure action-value fit
- **Value Optimization**: Find best-aligned actions
- **Conflict Detection**: Identify ethical violations

## 📚 Documentation

- **[Architecture](docs/ARCHITECTURE.md)**: System design and components
- **[Protocol Specification](docs/PROTOCOL_SPEC.md)**: Wire format and message structure
- **[API Reference](docs/API_REFERENCE.md)**: Complete API documentation

## 🧪 Examples

### Agent-to-Agent Communication

```bash
python examples/a2a_demo.py
```

Demonstrates:
- Two agents exchanging messages
- Safety constraint checking
- Policy enforcement
- Ethical alignment
- Audit trail

### Swarm Simulation

```bash
python examples/swarm_demo.py
```

Demonstrates:
- 10,000 agent communication network
- High-throughput messaging
- Safety monitoring at scale
- Prometheus metrics export

## 🔧 Development

### Running Tests

```bash
# Install test dependencies
pip install pytest scikit-learn lxml

# Run all tests
pytest umaja_core/tests/ -v

# Run specific test file
pytest umaja_core/tests/test_safety_polytope.py -v
```

### Project Structure

```
umaja_core/
├── protocols/
│   ├── vectorcomm/      # Encoding and transport
│   ├── safety/          # Geometric constraints
│   ├── enforcement/     # Policy and audit
│   └── ethics/          # Value alignment
├── tests/               # Test suite
└── __init__.py

examples/
├── a2a_demo.py          # Two-agent demo
├── swarm_demo.py        # 10K-agent demo
└── resource_policy.xml  # Example policy

docs/
├── ARCHITECTURE.md      # System design
├── PROTOCOL_SPEC.md     # Protocol details
└── API_REFERENCE.md     # API documentation

schemas/
└── resource_policy.xsd  # XML schema
```

## 🎓 Key Concepts

### VectorComm Protocol

Messages are encoded as high-dimensional vectors that preserve semantic meaning:

```python
encoder = VectorCommEncoder()
msg_vector = encoder.encode("Collaborate on task", tier=2)
# msg_vector is a 768D numpy array
```

### Safety Polytopes

Safe regions are defined geometrically as convex polytopes:

```python
# Define constraints: A*x <= b
constraints = [
    LinearConstraint(a=np.array([1, 0, 0]), b=5.0),
    LinearConstraint(a=np.array([0, 1, 0]), b=5.0)
]
polytope = SafetyPolytope(constraints)

# Check safety
if not polytope.is_safe(vector):
    safe_vector = polytope.steer_to_safe(vector)
```

### Policy Enforcement

Policies are defined in XML and checked before action execution:

```xml
<resourceAcquisitionPolicy>
  <limits>
    <cpuUsage max="80%" enforce="true"/>
    <memoryUsage max="16GB" enforce="true"/>
  </limits>
</resourceAcquisitionPolicy>
```

### Audit Trail

All actions are logged in a tamper-evident chain:

```python
trail = AuditTrail()
trail.log_action(agent_id="agent1", action={...}, compliant=True)
assert trail.verify_chain_integrity()
```

## ⚡ Performance

### Benchmarks (CPU)

- **Encoding**: 20-60 messages/second (tier-dependent)
- **Safety Check**: <5ms per vector
- **Policy Check**: <10ms per action
- **Audit Logging**: <1ms per entry

### Scalability

- Supports **10,000+ concurrent agents**
- Horizontally scalable (distributed model servers)
- GPU acceleration available (10-100x speedup)

## 🔐 Security

### Current Implementation

- ✅ Geometric safety constraints
- ✅ Policy enforcement
- ✅ SHA256 audit chain
- ✅ Digital signatures
- ⚠️ Mock ZK-SNARK (demonstration only)

### Production Recommendations

- Replace mock ZK-SNARKs with production library (libsnark/circom)
- Enable TLS for transport layer
- Encrypt audit trail storage
- Implement rate limiting
- Add agent identity verification

## 🤝 Contributing

This is a research prototype implementing the UMAJA specification. Contributions welcome!

### Areas for Improvement

1. Production ZK-SNARK implementation
2. GPU-optimized encoding
3. Distributed architecture
4. Additional safety constraints
5. Expanded ethical frameworks

## 📝 License

MIT License - See LICENSE file for details

## 🙏 Acknowledgments

Built on:
- [Sentence Transformers](https://www.sbert.net/) for embeddings
- [CVXPY](https://www.cvxpy.org/) for convex optimization
- [scikit-learn](https://scikit-learn.org/) for ML utilities

Inspired by research in:
- AI Safety and Alignment
- Multi-Agent Systems
- Cryptographic Protocols
- Semantic Communication

## 📞 Support

- **Documentation**: `/docs/`
- **Examples**: `/examples/`
- **Tests**: `/umaja_core/tests/`
- **Issues**: GitHub Issues

---

**Note**: This is a research prototype. The ZK-SNARK implementation is for demonstration purposes only. Use a production-grade library for real-world deployments.

*Version 0.1.0 - January 2026*
