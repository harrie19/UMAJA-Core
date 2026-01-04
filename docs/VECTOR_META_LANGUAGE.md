# 📡 VectorComm Protocol - Vector Meta-Language for AI Communication

## Overview

VectorComm is a formal vector-based communication protocol that allows AI agents to communicate semantically without natural language ambiguity. It uses high-dimensional vectors as the primary communication medium.

> "When AIs talk to AIs, they speak in vectors, not words."

---

## 🎯 Key Features

- **Binary Serialization** - Efficient transmission (50-70% compression)
- **Checksum Verification** - SHA256 integrity checks  
- **Multi-Vector Messages** - Complex semantic communication
- **Multiple Transport Modes** - Unicast, broadcast, multicast
- **Standard Dimensions** - 384, 768, 1536, or 4096
- **Multiple Encodings** - float32, float16, bfloat16

---

## 🏗️ Protocol Structure

```
┌─────────────────────────────────────┐
│      VectorCommMessage              │
├─────────────────────────────────────┤
│  ┌────────────────────────────┐    │
│  │  Header                    │    │
│  │  - dimension (384/768/...)  │    │
│  │  - encoding (float32/...)   │    │
│  │  - semantic_space (model)   │    │
│  │  - confidence (0.0-1.0)     │    │
│  └────────────────────────────┘    │
│                                     │
│  ┌────────────────────────────┐    │
│  │  Payload                   │    │
│  │  - primary_vector          │    │
│  │  - context_vectors []      │    │
│  │  - attention_weights       │    │
│  │  - uncertainty_vector      │    │
│  └────────────────────────────┘    │
│                                     │
│  ┌────────────────────────────┐    │
│  │  Metadata                  │    │
│  │  - source_agent            │    │
│  │  - destination_agent       │    │
│  │  - intent (query/response) │    │
│  │  - priority (0-10)         │    │
│  │  - timestamp               │    │
│  └────────────────────────────┘    │
│                                     │
│  └─ checksum (SHA256)              │
└─────────────────────────────────────┘
```

---

## 📦 Components

### 1. Protocol (`protocol.py`)

Defines message structure and types.

**Example:**
```python
from vectorcomm import create_message, Intent, Priority
import numpy as np

# Create semantic vector
vector = np.random.randn(384).astype(np.float32)

# Create message
message = create_message(
    source_agent='researcher_1',
    primary_vector=vector,
    destination_agent='coordinator',
    intent=Intent.QUERY,
    priority=Priority.HIGH
)
```

### 2. Serialization (`serialization.py`)

Binary encoding for efficient transmission.

**Example:**
```python
from vectorcomm import serialize_message, deserialize_message

# Serialize (with compression)
data = serialize_message(message, compress=True)

# Transmit...

# Deserialize
reconstructed = deserialize_message(data, compressed=True)
```

**Compression Ratios:**
- Typical: 50-70% size reduction
- Quantization: 75-85% reduction (slight precision loss)

### 3. Verification (`verification.py`)

Integrity and validation checks.

**Example:**
```python
from vectorcomm import add_checksum, verify_checksum, validate_message

# Add checksum
message = add_checksum(message)

# Verify integrity
is_valid = verify_checksum(message)

# Full validation
is_valid, errors = validate_message(message)
```

### 4. Transport (`transport.py`)

Message routing and delivery.

**Example:**
```python
from vectorcomm import VectorTransport

# Create transport
transport = VectorTransport('agent_1')

# Connect to other agents
transport.connect_agent('agent_2', other_transport)

# Start
await transport.start()

# Send message
await transport.send(message)

# Receive message
received = await transport.receive(timeout=5.0)
```

---

## 🚀 Usage Examples

### Simple Query-Response

```python
import numpy as np
from vectorcomm import create_message, VectorTransport, Intent

# Agent 1: Create query
query_vector = encode_text("What is the weather?")
query = create_message(
    source_agent='user_agent',
    primary_vector=query_vector,
    destination_agent='weather_agent',
    intent=Intent.QUERY
)

# Send
await transport1.send(query)

# Agent 2: Receive and respond
received_query = await transport2.receive()
response_vector = encode_text("It's sunny, 72°F")
response = create_message(
    source_agent='weather_agent',
    primary_vector=response_vector,
    destination_agent='user_agent',
    intent=Intent.RESPONSE
)

await transport2.send(response)
```

### Broadcast Notification

```python
# Create broadcast message (no destination)
notification_vector = encode_text("System update at midnight")
notification = create_message(
    source_agent='system',
    primary_vector=notification_vector,
    destination_agent=None,  # Broadcast
    intent=Intent.NOTIFICATION
)

# All subscribed agents will receive
await transport.send(notification)
```

### Multi-Vector Context

```python
# Complex message with context
primary = encode_text("Analyze this document")
context1 = encode_text("Document is legal contract")  
context2 = encode_text("Focus on terms and conditions")

message = VectorCommMessage(
    header=VectorCommHeader(384, 'float32', 'model-name', 0.9),
    payload=VectorCommPayload(
        primary_vector=primary,
        context_vectors=[context1, context2],
        attention_weights=np.array([0.7, 0.3])  # Relative importance
    ),
    metadata=VectorCommMetadata(
        source_agent='user',
        destination_agent='analyzer'
    )
)
```

---

## 📊 Message Intents

| Intent | Purpose | Response Expected |
|--------|---------|-------------------|
| `QUERY` | Ask question | Yes |
| `RESPONSE` | Answer query | No |
| `COMMAND` | Give instruction | Optional |
| `NOTIFICATION` | Broadcast info | No |
| `UPDATE` | State change | No |
| `ERROR` | Report error | Optional |
| `HEARTBEAT` | Keep-alive | No |

---

## 🎚️ Priority Levels

| Priority | Value | Use Case |
|----------|-------|----------|
| `LOWEST` | 0 | Background tasks |
| `LOW` | 2 | Non-urgent |
| `NORMAL` | 5 | Regular messages |
| `HIGH` | 7 | Important |
| `CRITICAL` | 10 | Emergency only |

---

## 🔐 Security Features

### 1. Checksum Verification
```python
# Detect tampering
message = add_checksum(message)
if not verify_checksum(message):
    raise SecurityError("Message tampered!")
```

### 2. HMAC Authentication
```python
# Authenticated messages
secret_key = b'shared_secret'
checksum = calculate_checksum(message, secret_key)
```

### 3. Anomaly Detection
```python
# Detect suspicious patterns
anomalies = detect_anomalies(message)
if anomalies:
    alert_security(anomalies)
```

---

## 📈 Performance

### Message Sizes

| Dimension | Encoding | Size (uncompressed) | Size (compressed) |
|-----------|----------|---------------------|-------------------|
| 384 | float32 | ~2 KB | ~1 KB |
| 768 | float32 | ~4 KB | ~2 KB |
| 1536 | float32 | ~7 KB | ~3.5 KB |
| 4096 | float32 | ~17 KB | ~8 KB |

### Throughput

- **Serialization**: ~1000 messages/sec
- **Deserialization**: ~800 messages/sec
- **Transport**: ~500 messages/sec (local)
- **Network**: Depends on bandwidth

---

## 🧪 Testing

All tests pass (11/11):

```bash
pytest tests/vectorcomm/ -v

# Results:
# ✅ Header creation
# ✅ Message creation  
# ✅ Validation
# ✅ Serialization
# ✅ Checksum verification
# ✅ Transport layer
# ✅ Multi-vector messages
# ✅ Compression
# ✅ Batch serialization
# ✅ Broadcasting
# ✅ Size estimation
```

---

## 🔮 Future Enhancements

1. **Encryption** - End-to-end encrypted messages
2. **Routing** - Multi-hop routing for distributed swarms
3. **QoS** - Quality of service guarantees
4. **Persistence** - Message queuing and replay
5. **Monitoring** - Real-time protocol analytics

---

## 📚 API Reference

### Core Functions

```python
# Create message
message = create_message(source, vector, dest, intent, priority)

# Serialize
data = serialize_message(message, compress=True)

# Deserialize  
message = deserialize_message(data, compressed=True)

# Verify
is_valid, errors = validate_message(message)

# Send
success = await transport.send(message)

# Receive
message = await transport.receive(timeout=5.0)
```

---

## 🤝 Integration with UMAJA

VectorComm is the communication backbone for:

1. **Agent Swarm** - Billion agents coordinate via vectors
2. **Research Engine** - Share discoveries semantically
3. **Memory System** - Store/retrieve vector memories
4. **Personality System** - Communicate with different tones

All built on top of the **Alignment System** foundation.

---

## 💡 Why Vectors?

1. **Language-Independent** - Works across all human languages
2. **Semantic Precision** - No ambiguity like natural language
3. **Efficient** - Compact representation
4. **Computable** - Direct similarity calculations
5. **Extensible** - Add context vectors as needed

---

**VectorComm: When AIs need to talk to AIs at the speed of thought.** 🌊📡✨
