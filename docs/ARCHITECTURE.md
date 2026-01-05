# UMAJA Core Architecture

**Vector Meta-Language Protocol for AI-to-AI Communication**

## Overview

UMAJA Core implements a comprehensive protocol for safe, ethical, and policy-compliant communication between AI agents. The system combines vector embeddings, geometric safety constraints, resource policy enforcement, and ethical alignment mechanisms.

---

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     UMAJA Core System                       │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │  VectorComm  │  │    Safety    │  │    Ethics    │     │
│  │   Protocol   │  │  Constraints │  │  Alignment   │     │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘     │
│         │                 │                  │             │
│         └─────────────────┴──────────────────┘             │
│                           │                                │
│                  ┌────────▼─────────┐                      │
│                  │  Policy Enforcer │                      │
│                  └────────┬─────────┘                      │
│                           │                                │
│                  ┌────────▼─────────┐                      │
│                  │  Audit Trail     │                      │
│                  └──────────────────┘                      │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## Core Components

### 1. VectorComm Protocol

**Purpose:** Efficient AI-to-AI communication using semantic vector embeddings

**Components:**
- `VectorCommEncoder`: Multi-tier embedding encoder
- `VectorTransport`: Message routing and delivery
- `LMNet`: Network utilities for vector operations

**Tiers:**

| Tier | Model | Dimension | Latency | Use Case |
|------|-------|-----------|---------|----------|
| 1 | all-MiniLM-L6-v2 | 384D | ~16ms | Fast responses |
| 2 | all-mpnet-base-v2 | 768D | ~45ms | Balanced (default) |
| 3 | all-roberta-large-v1 | 1024D | ~120ms | Maximum accuracy |

**Features:**
- Dynamic tier selection based on latency/accuracy needs
- Tier compression using PCA
- Batch encoding support
- Similarity-based decoding

---

### 2. Safety Systems

**Purpose:** Ensure agent communications remain within safe operational boundaries

#### SafetyPolytope

Geometric constraints in embedding space using convex polytopes.

**Constraints:**
- Linear inequalities: `A x ≤ b`
- Convex safe region defined by intersection of half-spaces
- Margin-based safety checking

**Operations:**
- `is_safe(vector)`: Check if vector satisfies all constraints
- `steer_to_safe(vector)`: Project unsafe vector to nearest safe point
- `get_constraint_violations(vector)`: List all violated constraints

**Factory Methods:**
- `create_sphere_polytope()`: Approximate sphere constraints
- `create_box_polytope()`: Axis-aligned box constraints

#### Margin Loss

Contrastive loss functions for learning safe embeddings.

- **Triplet Loss**: `max(0, d(anchor, pos) - d(anchor, neg) + margin)`
- **Contrastive Loss**: Minimize distance for similar pairs, maximize for dissimilar

#### OOD Detector

Out-of-distribution detection for anomalous embeddings.

**Methods:**
- Robust covariance estimation (Elliptic Envelope)
- Mahalanobis distance-based detection
- Batch anomaly scoring

---

### 3. Policy Enforcement

**Purpose:** Enforce resource acquisition policies and prosocial constraints

#### PolicyEnforcer

XML-based policy parser and enforcement engine.

**Policy Structure:**
```xml
<resourceAcquisitionPolicy>
  <limits>
    <cpuUsage max="80%" enforce="true"/>
    <memoryUsage max="16GB" enforce="true"/>
  </limits>
  <prosocialConstraints>
    <fairUsePolicy/>
    <emergencyOverride enabled="true"/>
    <humanOversight required="false"/>
  </prosocialConstraints>
</resourceAcquisitionPolicy>
```

**Operations:**
- `load_policy(xml_path)`: Parse XML policy
- `check_compliance(action)`: Verify action compliance
- `enforce_limits(action)`: Allow or block action
- `generate_proof(action)`: Generate ZK proof of compliance

#### CryptoProofSystem

Zero-knowledge proof generation and verification (mock implementation).

**Features:**
- ZK-SNARK proof generation (mock)
- Digital signatures for actions
- Statement/witness verification

**Note:** Production deployment requires actual ZK-SNARK library (libsnark/circom).

#### AuditTrail

Immutable, tamper-evident audit log with SHA256 chain.

**Structure:**
```python
Entry {
    entry_id: int
    timestamp: str
    agent_id: str
    action: dict
    compliant: bool
    previous_hash: str  # Links to previous entry
    current_hash: str   # SHA256 of this entry
}
```

**Operations:**
- `log_action()`: Append action to chain
- `verify_chain_integrity()`: Cryptographically verify chain
- `export_prometheus_metrics()`: Export metrics
- `get_statistics()`: Get audit statistics

---

### 4. Ethics & Values

**Purpose:** Encode and evaluate ethical principles for agent alignment

#### EthicalValueEncoder

Multi-dimensional ethical value encoding using semantic embeddings.

**Value Frameworks:**
- **Universal**: Core principles (fairness, compassion, honesty)
- **Utilitarian**: Consequentialist reasoning
- **Deontological**: Duty-based ethics
- **Virtue**: Character-based ethics

**Operations:**
- `encode_value(principle, culture)`: Encode ethical principle
- `compute_alignment_score(action, value)`: Score action alignment
- `optimize_for_values(actions, values)`: Find best-aligned action
- `rank_actions_by_value()`: Rank actions by ethical alignment

#### Alignment Scoring

Utilities for ethical alignment computation.

**Components:**
- `AlignmentScorer`: Aggregate alignment across values
- `ValueJudgmentFunction`: Judge actions against target values
- `NormPromotionFunction`: Promote prosocial norms

---

## Data Flow

### Typical Agent-to-Agent Communication

```
1. Agent A creates message
   │
2. Encode to vector (VectorCommEncoder)
   │
3. Check safety constraints (SafetyPolytope)
   │
4. Check resource policy (PolicyEnforcer)
   │
5. Check ethical alignment (EthicalValueEncoder)
   │
6. If all checks pass:
   │  a. Send message (VectorTransport)
   │  b. Log to audit trail (AuditTrail)
   │  c. Generate compliance proof (CryptoProofSystem)
   │
7. Agent B receives and decodes message
```

---

## Performance Characteristics

### Latency Targets

| Component | Target | Actual (CPU) |
|-----------|--------|--------------|
| Tier 2 Encoding | <50ms | ~45ms |
| Safety Check | <5ms | ~2ms |
| Policy Check | <10ms | ~5ms |
| Ethics Scoring | <50ms | ~45ms |

### Throughput

- **Single Agent**: 20-60 messages/sec (depending on tier)
- **Swarm (10K agents)**: 500-1000 messages/sec (with sampling)

### Memory Usage

- **Models Loaded**: ~2-4GB (Tier 2)
- **Per Agent**: ~1-10MB
- **Audit Trail**: ~1KB per entry

---

## Scalability

### Horizontal Scaling

The protocol supports distributed deployment:

1. **Model Serving**: Deploy encoders on separate model servers
2. **Transport Layer**: Use message queue (RabbitMQ, Kafka)
3. **Policy Enforcement**: Distributed policy servers
4. **Audit Trail**: Distributed ledger (blockchain, distributed DB)

### Vertical Optimization

- **GPU Acceleration**: For encoding (10-100x speedup)
- **Model Quantization**: Reduce model size (FP16, INT8)
- **Caching**: Cache frequent embeddings
- **Batching**: Batch encode multiple messages

---

## Security Considerations

### Threat Model

**Threats:**
- Adversarial embeddings bypassing safety
- Policy violation attempts
- Audit trail tampering
- Sybil attacks in swarms

**Mitigations:**
- Margin-based adversarial training
- Cryptographic proof verification
- SHA256 chain integrity
- Agent identity verification

### Privacy

- ZK-SNARKs enable proving compliance without revealing details
- Embeddings don't expose raw message content
- Audit trail can be encrypted at rest

---

## Deployment

### Development

```bash
# Install dependencies
pip install -r requirements.txt

# Run tests
pytest umaja_core/tests/

# Run examples
python examples/a2a_demo.py
python examples/swarm_demo.py
```

### Production

1. **Model Deployment**:
   - Host models on model server (TorchServe, TensorFlow Serving)
   - Use GPU for encoding
   - Enable model caching

2. **Infrastructure**:
   - Message queue for transport
   - Distributed database for audit trail
   - Load balancer for policy enforcement

3. **Monitoring**:
   - Prometheus metrics export
   - Grafana dashboards
   - Alert on safety violations

4. **Security**:
   - Replace mock ZK-SNARKs with production library
   - Enable TLS for transport
   - Encrypt audit trail storage

---

## Future Enhancements

### Planned Features

1. **Hardware Integration**: FireBreak MCU support (from UMAJA spec)
2. **Advanced ZK**: Production ZK-SNARK implementation
3. **Federated Learning**: Distributed safety learning
4. **Dynamic Policies**: Runtime policy updates
5. **Cross-Culture**: Enhanced cultural value frameworks

### Research Directions

- Adversarial robustness improvements
- Efficient high-dimensional polytopes
- Automated ethical value discovery
- Multi-modal embeddings (text + vision)

---

## References

### Academic Foundations

- Sentence Transformers (Reimers & Gurevych, 2019)
- Contrastive Learning (Chen et al., 2020)
- Ethical AI Alignment (Russell et al., 2015)
- Zero-Knowledge Proofs (Goldwasser et al., 1985)

### Implementation

- HuggingFace Transformers
- Scikit-learn
- CVXPY (convex optimization)
- lxml (XML processing)

---

## Support

For questions or issues:
- Documentation: `/docs/`
- Examples: `/examples/`
- Tests: `/umaja_core/tests/`
- Issues: GitHub Issues

---

*Last Updated: 2026-01-04*
*Version: 0.1.0*
