# UMAJA Core API Reference

**Version 0.1.0**

Complete API documentation for all public classes and functions.

---

## Table of Contents

1. [VectorComm Protocol](#vectorcomm-protocol)
2. [Safety Systems](#safety-systems)
3. [Policy Enforcement](#policy-enforcement)
4. [Ethics Systems](#ethics-systems)

---

## VectorComm Protocol

### VectorCommEncoder

Multi-tier encoder for semantic message encoding.

#### Constructor

```python
VectorCommEncoder(cache_dir: Optional[str] = None)
```

**Parameters:**
- `cache_dir`: Optional directory for caching downloaded models

**Example:**
```python
encoder = VectorCommEncoder()
```

#### Methods

##### encode()

```python
encode(
    message: Union[str, List[str]], 
    tier: int = 2,
    normalize: bool = True
) -> np.ndarray
```

Encode message(s) into vector representation.

**Parameters:**
- `message`: Text message or list of messages
- `tier`: Encoding tier (1, 2, or 3)
- `normalize`: Whether to L2-normalize embeddings

**Returns:**
- numpy array of shape `(dim,)` or `(n_messages, dim)`

**Example:**
```python
vector = encoder.encode("Hello world", tier=2)
print(vector.shape)  # (768,)
```

##### decode()

```python
decode(
    vector: np.ndarray, 
    tier: int = 2,
    candidates: Optional[List[str]] = None,
    top_k: int = 5
) -> str
```

Decode vector back to nearest message (approximate).

**Parameters:**
- `vector`: Embedding vector to decode
- `tier`: Tier level used for encoding
- `candidates`: Optional candidate messages to search
- `top_k`: Number of top candidates to return

**Returns:**
- Most likely decoded message string

**Example:**
```python
decoded = encoder.decode(vector, tier=2, candidates=["Hello", "Hi", "Hey"])
print(decoded)  # "Hello"
```

##### compress_to_tier()

```python
compress_to_tier(
    vector: np.ndarray, 
    source_tier: int, 
    target_tier: int
) -> np.ndarray
```

Compress embedding from higher tier to lower tier.

**Parameters:**
- `vector`: Source embedding vector
- `source_tier`: Original tier (higher dimension)
- `target_tier`: Target tier (lower dimension)

**Returns:**
- Compressed vector at target tier dimension

**Example:**
```python
high_dim = encoder.encode("Test", tier=3)  # 1024D
low_dim = encoder.compress_to_tier(high_dim, source_tier=3, target_tier=1)
print(low_dim.shape)  # (384,)
```

##### get_tier_info()

```python
get_tier_info(tier: int) -> dict
```

Get information about a specific tier.

**Returns:**
- Dictionary with tier configuration

**Example:**
```python
info = encoder.get_tier_info(2)
print(info)
# {'model': '...', 'dim': 768, 'latency_ms': 45, 'description': '...'}
```

##### list_tiers()

```python
list_tiers() -> dict
```

List all available tiers.

**Returns:**
- Dictionary mapping tier number to configuration

---

### VectorMessage

Structured message for VectorComm protocol.

#### Constructor

```python
VectorMessage(
    sender_id: str,
    receiver_id: str,
    vector: np.ndarray,
    tier: int,
    metadata: Optional[Dict[str, Any]] = None,
    message_id: Optional[str] = None
)
```

**Example:**
```python
msg = VectorMessage(
    sender_id="agent1",
    receiver_id="agent2",
    vector=np.random.randn(768),
    tier=2,
    metadata={'priority': 'high'}
)
```

#### Methods

##### to_dict()

```python
to_dict() -> Dict[str, Any]
```

Serialize message to dictionary.

##### from_dict()

```python
@classmethod
from_dict(cls, data: Dict[str, Any]) -> VectorMessage
```

Deserialize message from dictionary.

##### to_json() / from_json()

```python
to_json() -> str
from_json(cls, json_str: str) -> VectorMessage
```

JSON serialization/deserialization.

---

### VectorTransport

Transport layer for VectorComm messages.

#### Constructor

```python
VectorTransport()
```

#### Methods

##### send()

```python
send(message: VectorMessage) -> bool
```

Send a vector message.

**Returns:**
- True if sent successfully

##### receive()

```python
receive(agent_id: str) -> Optional[VectorMessage]
```

Receive next message for agent.

**Returns:**
- Next VectorMessage or None

##### receive_all()

```python
receive_all(agent_id: str) -> List[VectorMessage]
```

Receive all pending messages for agent.

##### has_messages()

```python
has_messages(agent_id: str) -> bool
```

Check if agent has pending messages.

---

### LMNet

Language Model Network utilities.

#### Static Methods

##### compute_similarity()

```python
@staticmethod
compute_similarity(vec1: np.ndarray, vec2: np.ndarray) -> float
```

Compute cosine similarity between two vectors.

**Returns:**
- Similarity score in [0, 1]

##### find_nearest_agents()

```python
@staticmethod
find_nearest_agents(
    query_vector: np.ndarray,
    agent_vectors: List[np.ndarray],
    agent_ids: List[str],
    top_k: int = 5
) -> List[Tuple[str, float]]
```

Find k nearest agents based on vector similarity.

**Returns:**
- List of (agent_id, similarity_score) tuples

##### aggregate_vectors()

```python
@staticmethod
aggregate_vectors(
    vectors: List[np.ndarray],
    method: str = 'mean',
    weights: Optional[List[float]] = None
) -> np.ndarray
```

Aggregate multiple vectors.

**Parameters:**
- `method`: 'mean', 'max', or 'weighted'

---

## Safety Systems

### SafetyPolytope

Convex polytope defining safe region in embedding space.

#### Constructor

```python
SafetyPolytope(
    constraints: List[LinearConstraint],
    margin: float = 0.1
)
```

**Example:**
```python
constraints = [
    LinearConstraint(a=np.array([1, 0]), b=5.0),
    LinearConstraint(a=np.array([0, 1]), b=5.0)
]
polytope = SafetyPolytope(constraints)
```

#### Methods

##### is_safe()

```python
is_safe(vector: np.ndarray, check_margin: bool = True) -> bool
```

Check if vector lies within safe region.

**Example:**
```python
safe = polytope.is_safe(vector)
if not safe:
    print("Vector violates safety constraints")
```

##### steer_to_safe()

```python
steer_to_safe(
    vector: np.ndarray,
    max_iterations: int = 100,
    step_size: float = 0.1
) -> np.ndarray
```

Project unsafe vector to nearest safe point.

**Returns:**
- Corrected safe vector

##### get_constraint_violations()

```python
get_constraint_violations(
    vector: np.ndarray
) -> List[Tuple[LinearConstraint, float]]
```

Get all constraint violations for a vector.

**Returns:**
- List of (constraint, violation_amount) tuples

##### visualize_boundary()

```python
visualize_boundary(
    method: str = 'pca',
    n_samples: int = 1000
) -> dict
```

Visualize polytope boundary in 2D.

#### Factory Methods

##### create_sphere_polytope()

```python
@staticmethod
create_sphere_polytope(
    center: np.ndarray,
    radius: float,
    n_constraints: int = 20
) -> SafetyPolytope
```

Create polytope approximating a sphere.

##### create_box_polytope()

```python
@staticmethod
create_box_polytope(
    lower_bounds: np.ndarray,
    upper_bounds: np.ndarray
) -> SafetyPolytope
```

Create axis-aligned box polytope.

---

### LinearConstraint

Linear constraint: a^T x <= b

#### Constructor

```python
LinearConstraint(
    a: np.ndarray,
    b: float,
    description: str = ""
)
```

#### Methods

##### is_satisfied()

```python
is_satisfied(x: np.ndarray) -> bool
```

Check if point x satisfies this constraint.

##### distance()

```python
distance(x: np.ndarray) -> float
```

Signed distance to constraint boundary.

---

### OODDetector

Out-of-distribution detector for embedding safety.

#### Constructor

```python
OODDetector(
    contamination: float = 0.1,
    threshold: Optional[float] = None
)
```

#### Methods

##### fit()

```python
fit(embeddings: np.ndarray)
```

Fit detector on safe embedding distribution.

##### is_ood()

```python
is_ood(embedding: np.ndarray) -> bool
```

Check if embedding is out-of-distribution.

##### get_anomaly_score()

```python
get_anomaly_score(embedding: np.ndarray) -> float
```

Get anomaly score for embedding.

##### check_batch()

```python
check_batch(embeddings: np.ndarray) -> np.ndarray
```

Check batch of embeddings for OOD.

---

## Policy Enforcement

### PolicyEnforcer

XML-based resource acquisition policy enforcement.

#### Constructor

```python
PolicyEnforcer()
```

#### Methods

##### load_policy()

```python
load_policy(xml_path: str) -> ResourcePolicy
```

Load policy from XML file.

**Example:**
```python
enforcer = PolicyEnforcer()
policy = enforcer.load_policy('resource_policy.xml')
```

##### check_compliance()

```python
check_compliance(agent_action: Dict[str, Any]) -> ComplianceResult
```

Check if agent action complies with policy.

**Parameters:**
- `agent_action`: Dictionary with keys like 'cpu_usage', 'memory_usage'

**Returns:**
- ComplianceResult with violations list

**Example:**
```python
action = {'cpu_usage': '70%', 'memory_usage': '8GB'}
result = enforcer.check_compliance(action)
print(result.compliant)  # True or False
print(result.violations)  # List of violation messages
```

##### enforce_limits()

```python
enforce_limits(action: Dict[str, Any]) -> EnforcementAction
```

Enforce policy limits on action.

**Returns:**
- EnforcementAction with allowed flag and reason

##### generate_proof()

```python
generate_proof(action: Dict[str, Any]) -> ZKProof
```

Generate zero-knowledge proof of compliance.

---

### CryptoProofSystem

Cryptographic proof system for policy enforcement.

#### Constructor

```python
CryptoProofSystem()
```

#### Methods

##### generate_zkp()

```python
generate_zkp(
    statement: Dict[str, Any], 
    witness: Dict[str, Any]
) -> ZKProof
```

Generate zero-knowledge proof.

**Example:**
```python
crypto = CryptoProofSystem()
proof = crypto.generate_zkp(
    statement={'compliant': True},
    witness={'cpu': 50}
)
```

##### verify_zkp()

```python
verify_zkp(
    proof: ZKProof, 
    statement: Dict[str, Any]
) -> bool
```

Verify zero-knowledge proof.

##### sign_action()

```python
sign_action(
    action: Dict[str, Any], 
    private_key: str
) -> Signature
```

Sign action with private key.

##### verify_signature()

```python
verify_signature(
    signature: Signature, 
    action: Dict[str, Any]
) -> bool
```

Verify digital signature.

---

### AuditTrail

Immutable audit trail with SHA256 chain.

#### Constructor

```python
AuditTrail()
```

#### Methods

##### log_action()

```python
log_action(
    agent_id: str, 
    action: Dict[str, Any], 
    compliant: bool,
    metadata: Optional[Dict[str, Any]] = None
) -> AuditEntry
```

Log an agent action to the audit trail.

**Example:**
```python
trail = AuditTrail()
entry = trail.log_action(
    agent_id="agent1",
    action={'type': 'compute'},
    compliant=True
)
```

##### verify_chain_integrity()

```python
verify_chain_integrity() -> bool
```

Verify integrity of entire audit chain.

**Returns:**
- True if chain is intact and unmodified

##### export_prometheus_metrics()

```python
export_prometheus_metrics() -> str
```

Export metrics in Prometheus format.

##### get_statistics()

```python
get_statistics() -> Dict[str, Any]
```

Get audit trail statistics.

**Returns:**
- Dictionary with stats like 'total_actions', 'compliance_rate'

---

## Ethics Systems

### EthicalValueEncoder

Encode ethical principles as high-dimensional vectors.

#### Constructor

```python
EthicalValueEncoder(
    model_name: str = 'sentence-transformers/all-mpnet-base-v2'
)
```

#### Methods

##### encode_value()

```python
encode_value(
    principle: str, 
    culture: str = 'universal'
) -> np.ndarray
```

Encode ethical principle as vector.

**Parameters:**
- `principle`: Ethical principle description
- `culture`: Cultural context ('universal', 'utilitarian', etc.)

**Example:**
```python
ethics = EthicalValueEncoder()
value = ethics.encode_value("fairness and justice")
```

##### compute_alignment_score()

```python
compute_alignment_score(
    action_vector: np.ndarray, 
    value_vector: np.ndarray
) -> float
```

Compute alignment between action and ethical value.

**Returns:**
- Alignment score in [0, 1]

##### optimize_for_values()

```python
optimize_for_values(
    actions: List[np.ndarray], 
    target_values: List[np.ndarray],
    weights: Optional[List[float]] = None
) -> np.ndarray
```

Find action that best aligns with target values.

##### rank_actions_by_value()

```python
rank_actions_by_value(
    actions: List[str],
    target_value: str,
    culture: str = 'universal'
) -> List[Tuple[str, float]]
```

Rank actions by alignment with ethical value.

**Returns:**
- List of (action, alignment_score) tuples, sorted by score

##### get_value_profile()

```python
get_value_profile(
    action: str,
    culture: str = 'universal'
) -> Dict[str, float]
```

Get value alignment profile for an action.

**Returns:**
- Dictionary mapping principles to alignment scores

---

## Data Classes

### ResourcePolicy

```python
@dataclass
class ResourcePolicy:
    limits: ResourceLimits
    prosocial: ProsocialConstraints
    policy_id: Optional[str] = None
    version: str = "1.0"
```

### ComplianceResult

```python
@dataclass
class ComplianceResult:
    compliant: bool
    violations: List[str]
    warnings: List[str]
    metadata: Dict[str, Any]
```

### ZKProof

```python
@dataclass
class ZKProof:
    statement: Dict[str, Any]
    proof_data: Dict[str, Any]
    verification_key: str
```

### AuditEntry

```python
@dataclass
class AuditEntry:
    entry_id: int
    timestamp: str
    agent_id: str
    action: Dict[str, Any]
    compliant: bool
    previous_hash: str
    current_hash: str
    metadata: Optional[Dict[str, Any]] = None
```

---

## Constants

### TIER_CONFIGS

```python
TIER_CONFIGS = {
    1: {
        'model': 'sentence-transformers/all-MiniLM-L6-v2',
        'dim': 384,
        'latency_ms': 16
    },
    2: {
        'model': 'sentence-transformers/all-mpnet-base-v2',
        'dim': 768,
        'latency_ms': 45
    },
    3: {
        'model': 'sentence-transformers/all-roberta-large-v1',
        'dim': 1024,
        'latency_ms': 120
    }
}
```

---

*Last Updated: 2026-01-04*
*Version: 0.1.0*
