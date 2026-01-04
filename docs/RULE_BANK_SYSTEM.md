# Rule Bank System Documentation

## Overview

The Rule Bank System is UMAJA's ethical governance framework, ensuring all autonomous agent actions align with Bahá'í principles. It provides persistent memory, ethical validation, and an audit trail for complete transparency.

### Core Principles

The system is built on five Bahá'í principles:

1. **Truth** - Independent investigation of truth, no hallucination
2. **Unity** - Unity of humanity, no divisive content
3. **Service** - Service to humanity, benefit-driven actions
4. **Justice** - Justice and fairness, no bias
5. **Moderation** - Moderation in all things, efficient resource use

## Architecture

```
┌─────────────────────────────────────────────────────┐
│           Autonomous Agent (Main Loop)               │
│  wake() → perceive() → reason() → act() → learn()   │
└──────────────────┬──────────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────────┐
│          Reasoning Middleware                        │
│  • Task profiling                                    │
│  • Risk assessment                                   │
│  • Violation handling                                │
└──────────────────┬──────────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────────┐
│            Rule Bank                                 │
│  • Validate actions against principles               │
│  • Track violations                                  │
│  • Learn new rules                                   │
│  • Generate reports                                  │
└──────────────────┬──────────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────────┐
│     Persistent Memory (.agent-memory/)               │
│  • rule_bank.json                                    │
│  • decision_history.json                             │
│  • learned_patterns.json                             │
│  • state.json                                        │
└─────────────────────────────────────────────────────┘
```

## Components

### 1. Rule Bank (`src/rule_bank.py`)

The Rule Bank stores and validates ethical constraints.

#### Key Methods

```python
# Initialize with memory path
rule_bank = RuleBank(memory_path=".agent-memory")

# Validate an action
validation = rule_bank.validate_action({
    'type': 'post_content',
    'confidence': 0.9,
    'benefit_score': 0.85,
    'content': 'Welcome everyone!'
})

# Learn a new rule
rule_bank.learn_rule(
    observation="Always verify API responses",
    principle="truth",
    constraint="verify_api_data",
    severity="HIGH"
)

# Get violation report
report = rule_bank.get_violation_report()

# Save rules to disk
rule_bank.save_rules()
```

#### Default Rules

| Rule ID | Principle | Constraint | Description |
|---------|-----------|------------|-------------|
| TRUTH_001 | Truth | no_hallucination | Require confidence >= 0.8 |
| TRUTH_002 | Truth | cite_sources | Cite sources unless confidence >= 0.95 |
| UNITY_001 | Unity | no_division | Divisive content score < 0.3 |
| UNITY_002 | Unity | inclusive_language | Inclusive score >= 0.7 |
| SERVICE_001 | Service | positive_benefit | Benefit score >= 0.6 |
| SERVICE_002 | Service | no_exploitation | Manipulation score < 0.2 |
| JUSTICE_001 | Justice | no_bias | Bias score < 0.3 |
| MODERATION_001 | Moderation | resource_efficiency | Resource usage <= budget |

### 2. Reasoning Middleware (`src/reasoning_middleware.py`)

The middleware intercepts actions and validates them before execution.

#### Key Methods

```python
# Initialize with Rule Bank
middleware = ReasoningMiddleware(rule_bank)

# Intercept an action
result = middleware.intercept({
    'type': 'post_world_tour_content',
    'city_id': 'tokyo',
    'confidence': 0.9,
    'benefit_score': 0.85
})

# Check result
if result['status'] == 'approved':
    execute_action(result['action'])
elif result['status'] == 'rejected':
    handle_alternatives(result['alternatives'])
elif result['status'] == 'requires_review':
    escalate_to_human(result)
```

#### Risk Levels

- **LOW** - No violations, low risk factors
- **MEDIUM** - Minor violations or moderate risk
- **HIGH** - Multiple violations or high-risk action
- **CRITICAL** - Critical violations or critical-risk action type

### 3. Autonomous Agent (`src/autonomous_agent.py`)

The main agent orchestrator that runs on GitHub Actions schedule.

#### Usage

```bash
# Run a complete agent cycle
python src/autonomous_agent.py --memory-path .agent-memory/

# The agent will:
# 1. Wake: Load persistent memory
# 2. Perceive: Read repository state
# 3. Reason: Decide actions
# 4. Act: Execute with validation
# 5. Learn: Update Rule Bank
# 6. Sleep: Save memory
```

## Bahá'í Principles Mapping

### Truth → Code

**Principle:** Independent investigation of truth

**Implementation:**
- Low-confidence outputs require source citation
- Confidence scores must be >= 0.8 for factual claims
- No hallucinations allowed

**Example:**
```python
action = {
    'confidence': 0.75,  # Too low
    'content': 'Paris is the capital of France'
}
# Result: Violation of TRUTH_001
# Recommendation: Add source or increase confidence
```

### Unity → Code

**Principle:** Unity of humanity

**Implementation:**
- No divisive content generation
- Inclusive language required
- Multi-language support maintained

**Example:**
```python
action = {
    'content': 'Us versus them mentality'  # Divisive
}
# Result: Violation of UNITY_001 (CRITICAL)
# Status: Requires human review
```

### Service → Code

**Principle:** Service to humanity

**Implementation:**
- Actions must have benefit_score >= 0.6
- No manipulation or exploitation
- Purpose-driven decisions only

**Example:**
```python
action = {
    'benefit_score': 0.4,  # Too low
    'type': 'post_content'
}
# Result: Violation of SERVICE_001
# Recommendation: Increase user benefit
```

### Justice → Code

**Principle:** Justice and fairness

**Implementation:**
- No demographic bias in content
- Equal access maintained
- Fair resource allocation

**Example:**
```python
action = {
    'bias_score': 0.5,  # Too high
    'content': 'Biased statement'
}
# Result: Violation of JUSTICE_001
```

### Moderation → Code

**Principle:** Moderation in all things

**Implementation:**
- Efficient resource usage
- No maximization loops
- Sustainable growth patterns

**Example:**
```python
action = {
    'resource_usage': 1000,
    'resource_budget': 500  # Exceeds budget
}
# Result: Violation of MODERATION_001
```

## Memory Structure

```
.agent-memory/
├── rule_bank.json           # Ethical constraints
├── decision_history.json    # Audit trail
├── learned_patterns.json    # ML patterns
└── state.json              # Agent state
```

### rule_bank.json

```json
{
  "rules": [
    {
      "id": "TRUTH_001",
      "principle": "truth",
      "constraint": "no_hallucination",
      "expression": "confidence >= 0.8",
      "description": "Require high confidence for facts",
      "violations": 0,
      "applied_count": 15,
      "severity": "HIGH"
    }
  ],
  "last_updated": "2026-01-04T07:00:00Z",
  "agent_version": "1.0.0"
}
```

### decision_history.json

```json
{
  "decisions": [
    {
      "timestamp": "2026-01-04T07:00:00Z",
      "action": {
        "type": "generate_world_tour_content",
        "city_id": "tokyo"
      },
      "validation": {
        "allowed": true,
        "violated_rules": [],
        "risk_level": "LOW"
      },
      "outcome": "success",
      "bahai_alignment": {
        "truth": 0.95,
        "unity": 1.0,
        "service": 0.98,
        "justice": 1.0,
        "moderation": 0.92
      }
    }
  ]
}
```

## Usage Guide

### Adding New Rules

```python
# Learn from observation
rule_bank.learn_rule(
    observation="External API calls should have timeout",
    principle="moderation",
    constraint="api_timeout",
    severity="MEDIUM"
)

# The rule is automatically saved
rule_bank.save_rules()
```

### Validating Actions

```python
# Before any action
action = {
    'type': 'post_content',
    'confidence': 0.9,
    'benefit_score': 0.8,
    'content': 'Your content here'
}

# Validate
result = middleware.intercept(action)

if result['status'] == 'approved':
    # Safe to proceed
    execute_action(action)
elif result['status'] == 'rejected':
    # Use alternatives
    for alt in result['alternatives']:
        print(f"Alternative: {alt['description']}")
else:
    # Requires human review
    escalate_to_human(result)
```

### Monitoring Violations

```python
# Get violation statistics
report = rule_bank.get_violation_report()

print(f"Total violations: {report['total_violations']}")
print(f"Violation rate: {report['violation_rate']:.2%}")

# Most violated rules
for rule in report['most_violated_rules']:
    print(f"{rule['id']}: {rule['violations']} violations")
```

## GitHub Actions Integration

The autonomous agent runs on GitHub Actions schedule:

```yaml
# .github/workflows/umaja-autonomous-agent.yml
on:
  schedule:
    - cron: '0 7 * * *'  # Daily at 07:00 UTC
  workflow_dispatch:      # Manual trigger
```

### Memory Persistence

Memory is persisted via GitHub Actions cache:

1. **Before execution**: Restore `.agent-memory/` from cache
2. **After execution**: Save `.agent-memory/` back to cache
3. **Backup**: Upload as artifact (90-day retention)

## Troubleshooting

### Issue: Actions Always Rejected

**Solution:** Check confidence and benefit scores:
```python
action['confidence'] >= 0.95  # Or add source attribution
action['benefit_score'] >= 0.6
```

### Issue: Memory Not Persisting

**Solution:** Verify GitHub Actions cache:
```bash
# Check workflow logs for cache restoration
# Look for: "Cache restored successfully"
```

### Issue: Too Many Violations

**Solution:** Review violation report:
```python
report = rule_bank.get_violation_report()
# Check most_violated_rules
# Adjust thresholds or improve content quality
```

## API Reference

### RuleBank

#### `__init__(memory_path: str)`
Initialize Rule Bank with memory path.

#### `validate_action(action: Dict) -> Dict`
Validate action against all rules.

**Returns:**
- `allowed`: bool - Whether action passes
- `violated_rules`: List[str] - Rule IDs violated
- `risk_level`: str - Overall risk assessment
- `recommendations`: List[str] - Improvement suggestions

#### `learn_rule(observation: str, principle: str, constraint: str, severity: str)`
Learn new rule from observation.

#### `get_violation_report() -> Dict`
Generate violation statistics report.

#### `get_principle_alignment(action: Dict) -> Dict[str, float]`
Calculate alignment scores for each Bahá'í principle.

### ReasoningMiddleware

#### `__init__(rule_bank: RuleBank)`
Initialize middleware with Rule Bank.

#### `intercept(action: Dict) -> Dict`
Intercept and validate action.

**Returns:**
- `status`: str - 'approved', 'rejected', or 'requires_review'
- `validation`: Dict - Rule Bank validation results
- `risk_profile`: Dict - Risk assessment
- `alternatives`: List[Dict] - Alternative actions
- `requires_human_review`: bool

#### `profile_task(action: Dict) -> Dict`
Profile task to assess risk level.

### AutonomousAgent

#### `__init__(memory_path: str)`
Initialize agent with memory path.

#### `run_cycle()`
Run complete agent cycle.

## Best Practices

1. **Always Validate**: Every action should go through middleware
2. **Log Decisions**: Maintain complete audit trail
3. **Review Violations**: Regularly check violation reports
4. **Learn Continuously**: Add new rules from feedback
5. **Human Oversight**: Escalate critical decisions

## Future Enhancements

- **Phase 2**: CrewAI multi-agent consultation
- **Phase 3**: Vector Engine + Rule Bank fusion
- **Phase 4**: Advanced ML-based rule learning

---

**Version:** 1.0.0  
**Last Updated:** 2026-01-04  
**Maintainer:** UMAJA Core Team

*"The earth is but one country, and mankind its citizens" - Bahá'u'lláh*
