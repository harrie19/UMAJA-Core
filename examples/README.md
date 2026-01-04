# UMAJA Vector Meta-Language Protocol Examples

This directory contains demonstration examples for the UMAJA Vector Meta-Language Protocol.

## 📋 Examples

### 1. Agent-to-Agent Communication Demo (`a2a_demo.py`)

Demonstrates basic AI-to-AI communication with safety and policy enforcement.

**Features:**
- Two agents exchanging vector-encoded messages
- Safety polytope constraint checking
- Resource policy enforcement
- Ethical value alignment checking
- Tamper-evident audit trail

**Run:**
```bash
cd examples
python a2a_demo.py
```

**Expected Output:**
- Message encoding and transmission
- Safety constraint verification
- Policy violation detection
- Ethical alignment scores
- Audit trail summary

---

### 2. Swarm Simulation Demo (`swarm_demo.py`)

Demonstrates large-scale multi-agent communication (10,000 agents).

**Features:**
- High-throughput message passing
- Safety monitoring at scale
- Performance metrics
- Prometheus metrics export
- Agent activity tracking

**Run:**
```bash
cd examples
python swarm_demo.py
```

**Expected Output:**
- Simulation of 1,000 messages across 10,000 agents
- Throughput measurements (messages/second)
- Safety violation statistics
- Agent participation metrics
- Prometheus-format metrics

---

## 🔧 Configuration Files

### `resource_policy.xml`

Example XML policy file defining resource acquisition limits.

**Structure:**
```xml
<resourceAcquisitionPolicy>
  <limits>
    <cpuUsage max="80%" enforce="true"/>
    <memoryUsage max="16GB" enforce="true"/>
  </limits>
  <prosocialConstraints>
    <fairUsePolicy>...</fairUsePolicy>
  </prosocialConstraints>
</resourceAcquisitionPolicy>
```

**Usage:**
```python
from umaja_core.protocols.enforcement.policy_enforcer import PolicyEnforcer

enforcer = PolicyEnforcer()
policy = enforcer.load_policy('resource_policy.xml')
```

---

## 📊 Performance Benchmarks

### Expected Performance (on CPU)

| Component | Latency | Throughput |
|-----------|---------|------------|
| Tier 1 Encoding (384D) | ~16ms | ~60 msg/sec |
| Tier 2 Encoding (768D) | ~45ms | ~22 msg/sec |
| Tier 3 Encoding (1024D) | ~120ms | ~8 msg/sec |
| Safety Check | <5ms | >200 checks/sec |
| Policy Enforcement | <10ms | >100 checks/sec |

### Swarm Simulation Metrics

With mock encoding (for demonstration):
- **Throughput**: 500-1000 messages/second
- **Active Agents**: 10,000
- **Safety Checks**: 10% sampling rate
- **Memory Usage**: ~500MB

With real encoding (production):
- **Throughput**: 20-60 messages/second (Tier 1)
- **Memory Usage**: ~2-4GB (with model loaded)

---

## 🚀 Quick Start

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run basic demo:**
   ```bash
   python examples/a2a_demo.py
   ```

3. **Run swarm simulation:**
   ```bash
   python examples/swarm_demo.py
   ```

---

## 🧪 Testing

Both examples include built-in error handling and progress indicators. They will:
- Download required models on first run (may take a few minutes)
- Show real-time progress during simulation
- Display formatted results and metrics
- Handle interruptions gracefully (Ctrl+C)

---

## 📚 Learn More

- [Architecture Documentation](../docs/ARCHITECTURE.md)
- [Protocol Specification](../docs/PROTOCOL_SPEC.md)
- [API Reference](../docs/API_REFERENCE.md)

---

## 🔍 Troubleshooting

**Models not downloading:**
- Check internet connection
- Verify `sentence-transformers` is installed
- Models are cached in `~/.cache/torch/sentence_transformers/`

**Out of memory:**
- Use Tier 1 (384D) for lower memory usage
- Reduce batch size in swarm simulation
- Close other applications

**Slow performance:**
- Use CPU-optimized PyTorch (already in requirements.txt)
- Enable model caching
- Consider GPU acceleration for production

---

## 💡 Next Steps

After running the examples:

1. **Modify policies**: Edit `resource_policy.xml` to experiment with different limits
2. **Add agents**: Extend demos with more agent types and behaviors
3. **Custom values**: Add your own ethical values to `value_embeddings.py`
4. **Scale up**: Test with more agents and messages in swarm simulation
5. **Integrate**: Use the protocol in your own multi-agent system

---

## 📝 Notes

- Examples use **mock implementations** for ZK-SNARKs (production requires libsnark/circom)
- Models are downloaded from HuggingFace on first run
- Examples are designed for **educational purposes** and demonstration
- For production use, see [deployment guide](../docs/ARCHITECTURE.md#deployment)
