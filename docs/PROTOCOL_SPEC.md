# UMAJA Vector Meta-Language Protocol Specification

**Version 0.1.0**

## Abstract

This document defines the Vector Meta-Language Protocol for AI-to-AI (A2A) communication. The protocol enables semantic message exchange through vector embeddings with embedded safety constraints, policy enforcement, and ethical alignment mechanisms.

---

## 1. Protocol Overview

### 1.1 Design Goals

1. **Semantic Communication**: Enable meaning-preserving message exchange
2. **Safety**: Geometric constraints prevent unsafe communications
3. **Policy Compliance**: Enforce resource and behavioral policies
4. **Ethical Alignment**: Ensure actions align with values
5. **Auditability**: Maintain tamper-evident record
6. **Efficiency**: Support high-throughput multi-agent systems

### 1.2 Protocol Layers

```
┌─────────────────────────────┐
│    Application Layer        │  Agent logic
├─────────────────────────────┤
│    Ethics Layer             │  Value alignment
├─────────────────────────────┤
│    Policy Layer             │  Resource enforcement
├─────────────────────────────┤
│    Safety Layer             │  Geometric constraints
├─────────────────────────────┤
│    Semantic Layer           │  Vector encoding
├─────────────────────────────┤
│    Transport Layer          │  Message routing
└─────────────────────────────┘
```

---

## 2. Message Format

### 2.1 VectorMessage Structure

```json
{
  "message_id": "uuid-v4",
  "sender_id": "agent_identifier",
  "receiver_id": "agent_identifier",
  "vector": [float, ...],
  "tier": 1 | 2 | 3,
  "timestamp": "ISO-8601",
  "metadata": {
    "encoding_model": "string",
    "safety_verified": boolean,
    "policy_compliant": boolean,
    "alignment_score": float,
    "proof_hash": "string"
  }
}
```

### 2.2 Field Specifications

**message_id**
- Type: UUID v4
- Required: Yes
- Description: Unique message identifier

**sender_id / receiver_id**
- Type: String
- Required: Yes
- Format: `agent_<identifier>`
- Description: Agent identifiers for routing

**vector**
- Type: Array of floats
- Required: Yes
- Length: 384 (Tier 1), 768 (Tier 2), or 1024 (Tier 3)
- Description: Semantic embedding of message

**tier**
- Type: Integer (1, 2, or 3)
- Required: Yes
- Description: Encoding tier used

**timestamp**
- Type: ISO-8601 datetime string
- Required: Yes
- Description: Message creation time (UTC)

**metadata**
- Type: Object
- Required: No
- Description: Additional message metadata

---

## 3. Encoding Specification

### 3.1 Tier Selection

Messages MUST be encoded using one of three tiers:

| Tier | Model | Dimension | Use Case |
|------|-------|-----------|----------|
| 1 | all-MiniLM-L6-v2 | 384 | Fast, low-latency |
| 2 | all-mpnet-base-v2 | 768 | Balanced (default) |
| 3 | all-roberta-large-v1 | 1024 | High accuracy |

### 3.2 Encoding Process

```python
# Pseudocode
function encode_message(text, tier):
    model = load_model(tier)
    vector = model.encode(text, normalize=True)
    assert len(vector) == TIER_DIMENSIONS[tier]
    return vector
```

**Normalization:** All vectors MUST be L2-normalized unless specified otherwise.

### 3.3 Cross-Tier Compression

When downgrading from higher to lower tier:

```
compressed = PCA(n_components=target_dim).fit_transform(vector)
```

Agents SHOULD maintain PCA projectors for consistent compression.

---

## 4. Safety Constraints

### 4.1 Polytope Definition

Safety regions are defined as convex polytopes:

```
Safe Region = {x ∈ ℝⁿ | Ax ≤ b}
```

Where:
- `A` is an `m × n` matrix (constraint normals)
- `b` is an `m`-dimensional vector (offsets)
- Each row defines one half-space constraint

### 4.2 Safety Checking

```python
function is_safe(vector, polytope, margin=0.1):
    for constraint in polytope.constraints:
        distance = dot(constraint.a, vector) - constraint.b
        if distance > margin:
            return False
    return True
```

### 4.3 Steering to Safety

If a vector violates constraints, it MUST be corrected:

```python
function steer_to_safe(vector, polytope):
    while not is_safe(vector, polytope):
        worst_constraint = find_most_violated(vector, polytope)
        gradient = worst_constraint.a
        vector = vector - step_size * gradient
        vector = normalize(vector)
    return vector
```

### 4.4 Safety Margin

Agents SHOULD use a safety margin (default: 0.1) to provide buffer from constraint boundaries.

---

## 5. Policy Enforcement

### 5.1 Policy XML Schema

Policies MUST conform to the following schema:

```xml
<resourceAcquisitionPolicy id="string" version="string">
  <limits>
    <cpuUsage max="percentage" enforce="boolean"/>
    <memoryUsage max="size_with_unit" enforce="boolean"/>
    <networkUsage max="rate_with_unit" enforce="boolean"/>
    <diskUsage max="size_with_unit" enforce="boolean"/>
  </limits>
  <prosocialConstraints>
    <fairUsePolicy enabled="boolean">
      <enforcementMechanism>string</enforcementMechanism>
    </fairUsePolicy>
    <emergencyOverride enabled="boolean"/>
    <humanOversight required="boolean"/>
  </prosocialConstraints>
</resourceAcquisitionPolicy>
```

### 5.2 Compliance Checking

Before executing an action, agents MUST:

1. Parse applicable policy
2. Extract action resource requirements
3. Compare against policy limits
4. Check prosocial constraints
5. Return compliance result

### 5.3 Enforcement Mechanisms

**Hard Enforcement:**
- Actions exceeding limits are BLOCKED
- Non-compliance is logged to audit trail

**Soft Enforcement:**
- Warnings issued but action allowed
- Logged for monitoring

**Emergency Override:**
- If enabled, allows policy bypass with justification
- Requires higher-level approval

---

## 6. Cryptographic Proofs

### 6.1 Zero-Knowledge Proofs

Agents MAY generate ZK-SNARKs to prove compliance without revealing details.

**Statement (Public):**
```json
{
  "compliant": true,
  "policy_id": "policy_identifier",
  "timestamp": "ISO-8601"
}
```

**Witness (Private):**
```json
{
  "actual_cpu_usage": 65.5,
  "actual_memory_usage": "12GB",
  "action_details": {...}
}
```

**Proof:**
```json
{
  "statement": {...},
  "proof_data": {
    "commitment": "hash",
    "challenges": [...],
    "responses": [...]
  },
  "verification_key": "string"
}
```

### 6.2 Digital Signatures

Actions SHOULD be signed with agent's private key:

```python
signature = sign(private_key, hash(action))
```

Signatures enable:
- Authentication (verify agent identity)
- Integrity (detect tampering)
- Non-repudiation (agent cannot deny action)

---

## 7. Audit Trail

### 7.1 Entry Format

```json
{
  "entry_id": 0,
  "timestamp": "ISO-8601",
  "agent_id": "string",
  "action": {...},
  "compliant": boolean,
  "previous_hash": "sha256",
  "current_hash": "sha256",
  "metadata": {...}
}
```

### 7.2 Hash Chain

Each entry links to previous via hash:

```
Genesis Block (H₀)
    ↓
Entry 0: H₁ = SHA256(H₀ || Entry₀)
    ↓
Entry 1: H₂ = SHA256(H₁ || Entry₁)
    ↓
Entry 2: H₃ = SHA256(H₂ || Entry₂)
    ↓
   ...
```

### 7.3 Integrity Verification

To verify chain:

```python
function verify_chain(trail):
    if trail[0].previous_hash != genesis_hash:
        return False
    
    for i in range(len(trail)):
        if trail[i].current_hash != compute_hash(trail[i]):
            return False
        if i > 0 and trail[i].previous_hash != trail[i-1].current_hash:
            return False
    
    return True
```

---

## 8. Ethical Alignment

### 8.1 Value Encoding

Ethical principles are encoded as vectors:

```python
value_vector = encode("fairness and justice")
```

### 8.2 Alignment Scoring

```python
function alignment_score(action_vector, value_vector):
    similarity = cosine_similarity(action_vector, value_vector)
    return (similarity + 1) / 2  # Map to [0, 1]
```

### 8.3 Thresholds

Actions SHOULD meet minimum alignment thresholds:

- **Critical actions**: ≥ 0.7
- **Standard actions**: ≥ 0.5
- **Low-risk actions**: ≥ 0.3

---

## 9. Wire Protocol

### 9.1 Transport Format

Messages MAY be transported via:
- HTTP/HTTPS (REST)
- WebSocket (real-time)
- Message Queue (RabbitMQ, Kafka)
- gRPC (high performance)

### 9.2 REST API Endpoints

**Send Message:**
```
POST /api/v1/messages
Content-Type: application/json

{
  "sender_id": "agent1",
  "receiver_id": "agent2",
  "vector": [...],
  "tier": 2,
  "metadata": {...}
}
```

**Receive Messages:**
```
GET /api/v1/messages/{agent_id}

Response:
{
  "messages": [
    {...},
    {...}
  ]
}
```

**Check Safety:**
```
POST /api/v1/safety/check
Content-Type: application/json

{
  "vector": [...],
  "polytope_id": "default"
}

Response:
{
  "safe": true,
  "violations": []
}
```

---

## 10. Error Handling

### 10.1 Error Codes

| Code | Name | Description |
|------|------|-------------|
| 1001 | UNSAFE_VECTOR | Vector violates safety constraints |
| 1002 | POLICY_VIOLATION | Action exceeds policy limits |
| 1003 | LOW_ALIGNMENT | Insufficient ethical alignment |
| 1004 | INVALID_TIER | Unknown or unsupported tier |
| 1005 | MALFORMED_MESSAGE | Invalid message format |
| 1006 | PROOF_INVALID | Cryptographic proof verification failed |

### 10.2 Error Response Format

```json
{
  "error": {
    "code": 1001,
    "message": "Vector violates safety constraints",
    "details": {
      "violated_constraints": [0, 3, 7],
      "max_violation": 0.35
    }
  }
}
```

---

## 11. Performance Requirements

### 11.1 Latency Targets

- **Encoding (Tier 2)**: < 50ms
- **Safety Check**: < 5ms
- **Policy Check**: < 10ms
- **End-to-end**: < 100ms

### 11.2 Throughput

- **Single Agent**: ≥ 20 messages/second
- **Swarm (10K agents)**: ≥ 500 messages/second aggregate

---

## 12. Security Considerations

### 12.1 Threat Model

**In Scope:**
- Adversarial embeddings
- Policy evasion
- Audit trail tampering
- Denial of service

**Out of Scope:**
- Model extraction attacks
- Side-channel attacks
- Physical security

### 12.2 Mitigations

1. **Adversarial Training**: Train safety polytope with adversarial examples
2. **Proof Verification**: Verify all cryptographic proofs
3. **Rate Limiting**: Limit messages per agent per time window
4. **Monitoring**: Real-time anomaly detection

---

## 13. Compliance

Implementations MUST:
- Support all three encoding tiers
- Enforce safety constraints
- Maintain audit trail integrity
- Provide compliance checking

Implementations SHOULD:
- Generate cryptographic proofs
- Compute ethical alignment
- Export Prometheus metrics
- Support distributed deployment

Implementations MAY:
- Add custom safety constraints
- Define custom ethical values
- Extend metadata fields
- Implement custom transport

---

## 14. Versioning

Protocol version format: `MAJOR.MINOR.PATCH`

- **MAJOR**: Incompatible changes
- **MINOR**: Backward-compatible features
- **PATCH**: Backward-compatible fixes

Current version: **0.1.0**

---

## 15. References

### Normative References

- RFC 4122 (UUID)
- RFC 3339 (ISO-8601)
- RFC 7159 (JSON)
- W3C XML Schema

### Informative References

- Reimers & Gurevych (2019): Sentence-BERT
- Goldwasser et al. (1985): Zero-Knowledge Proofs
- Russell (2019): Human Compatible AI

---

*Last Updated: 2026-01-04*
*Status: Draft*
