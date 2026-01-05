# UMAJA Safety, Security, and Privacy Specifications

## Overview

This document defines the safety, security, and privacy standards for UMAJA-Core, ensuring the system operates safely, protects user data, and maintains ethical AI practices.

---

## Safety Principles

### Core Safety Values

1. **Human Wellbeing First**: All decisions prioritize human welfare
2. **Do No Harm**: Content must be universally positive and constructive
3. **Cultural Sensitivity**: Respect all cultures, religions, and identities
4. **Transparency**: Clear about AI nature and limitations
5. **Controllability**: Emergency stop mechanisms always available

### Bahá'í Ethical Framework

UMAJA-Core operates according to Bahá'í principles:

- **Truth**: AI must distinguish fact from hallucination
- **Unity**: Content promotes human unity, never division
- **Service**: System serves humanity, not commercial interests
- **Justice**: Equal treatment for all users regardless of background

---

## Content Safety

### Content Guidelines

#### Approved Content
✅ **Always Allowed:**
- Educational facts and science
- Positive humor and comedy
- Cultural appreciation and learning
- Inspirational quotes and wisdom
- Universal human values
- Nature and environmental awareness

#### Prohibited Content
❌ **Never Allowed:**
- Hate speech or discrimination
- Violence or harm
- Sexual or inappropriate content
- Misinformation or conspiracy theories
- Political partisanship
- Religious proselytization
- Commercial advertising
- Personal attacks

### Content Validation Pipeline

```
┌─────────────────────────────────────────┐
│     Content Generation (Step 1)         │
│  - Generate base content in English     │
│  - Apply archetype personality          │
└─────────────────┬───────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────┐
│     Language Check (Step 2)             │
│  - Profanity detection                  │
│  - Hate speech detection                │
│  - Inappropriate content filter         │
└─────────────────┬───────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────┐
│     Cultural Validation (Step 3)        │
│  - Cultural sensitivity check           │
│  - Religious respect verification       │
│  - Regional appropriateness             │
└─────────────────┬───────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────┐
│     Quality Check (Step 4)              │
│  - Vector similarity analysis           │
│  - Fact verification                    │
│  - Tone and sentiment analysis          │
│  - Quality score ≥ 0.70 required        │
└─────────────────┬───────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────┐
│     Human Review (Step 5, if needed)    │
│  - Manual review for edge cases         │
│  - Final approval authority             │
└─────────────────┬───────────────────────┘
                  │
                  ▼
          [APPROVED/REJECTED]
```

### Quality Scoring

Content must achieve minimum quality scores:

```python
quality_metrics = {
    "semantic_coherence": 0.70,      # Clear and logical
    "cultural_sensitivity": 0.90,    # Respectful to all
    "factual_accuracy": 0.85,        # True or clearly fiction
    "positive_sentiment": 0.75,      # Uplifting and constructive
    "appropriateness": 1.00,         # Never inappropriate
    "translation_quality": 0.85      # Accurate across languages
}

# Overall quality score
overall_score = weighted_average(quality_metrics)
approved = overall_score >= 0.70 and all_critical_metrics_pass()
```

### Content Monitoring

**Continuous Monitoring:**
- All generated content logged
- Quality scores tracked over time
- User feedback collection (planned)
- Regular audits of content library

**Escalation Process:**
1. Automated filter catches issues
2. QualityChecker agent reviews
3. If uncertain, flag for human review
4. Human reviewer makes final decision
5. Learn from decision to improve filters

---

## Security Specifications

### Security Architecture Layers

```
┌─────────────────────────────────────────┐
│   Layer 1: Network Security             │
│   - HTTPS only, TLS 1.3                 │
│   - CORS restrictions                   │
│   - DDoS protection (Cloudflare)        │
└─────────────────┬───────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────┐
│   Layer 2: API Security                 │
│   - Rate limiting                       │
│   - Input validation                    │
│   - Authentication (future)             │
└─────────────────┬───────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────┐
│   Layer 3: Application Security         │
│   - No SQL injection (no database)      │
│   - XSS protection                      │
│   - CSRF protection                     │
└─────────────────┬───────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────┐
│   Layer 4: Data Security                │
│   - No personal data storage            │
│   - Content sanitization                │
│   - Secure secret management            │
└─────────────────────────────────────────┘
```

### Authentication and Authorization

**Current State:**
- No authentication required (open API)
- Rate limiting prevents abuse
- Public content only

**Future Plans:**
- Optional user accounts for personalization
- OAuth 2.0 integration (Google, GitHub)
- API keys for partners
- Role-based access control (RBAC)

### API Security

#### Rate Limiting
```python
# Configuration
RATE_LIMITS = {
    "standard": {
        "per_minute": 20,
        "per_hour": 100
    },
    "worldtour": {
        "per_minute": 10,
        "per_hour": 50
    }
}

# Implementation
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["100 per hour", "20 per minute"]
)

@app.route('/api/daily-smile')
@limiter.limit("100/hour;20/minute")
def daily_smile():
    return jsonify(get_smile())
```

#### CORS Configuration
```python
# Allowed origins
ALLOWED_ORIGINS = [
    "https://harrie19.github.io",
    "https://web-production-6ec45.up.railway.app"
]

# CORS setup
from flask_cors import CORS
CORS(app, 
     origins=ALLOWED_ORIGINS,
     methods=["GET", "POST"],
     allow_headers=["Content-Type"],
     max_age=3600)
```

#### Input Validation
```python
from flask import request, abort
import bleach

def validate_archetype(archetype):
    """Validate archetype parameter"""
    VALID_ARCHETYPES = ["professor", "worrier", "enthusiast"]
    if archetype not in VALID_ARCHETYPES:
        abort(400, description=f"Invalid archetype. Must be one of: {VALID_ARCHETYPES}")
    return archetype

def sanitize_input(text):
    """Sanitize user input to prevent XSS"""
    return bleach.clean(text, strip=True)

@app.route('/api/smile/<archetype>')
def get_smile(archetype):
    archetype = validate_archetype(archetype)
    archetype = sanitize_input(archetype)
    return jsonify(fetch_smile(archetype))
```

### Infrastructure Security

#### GitHub Actions Security
```yaml
# Minimal permissions
permissions:
  contents: write  # Only what's needed
  id-token: write  # For OIDC

# Secret management
env:
  GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}  # Auto-generated, scoped

# No third-party secrets stored
# No AWS keys, API tokens, or credentials needed
```

#### Railway Security
```bash
# Environment variables (not in code)
DEPLOYMENT_ENV=railway
FLASK_ENV=production
ALLOWED_ORIGINS=https://harrie19.github.io

# No database credentials
# No API keys stored
# Minimal attack surface
```

### Dependency Security

**Vulnerability Scanning:**
```bash
# Regular security audits
pip-audit

# Dependency updates
pip list --outdated
pip install --upgrade [package]

# GitHub Dependabot enabled
# Automated pull requests for security updates
```

**Minimal Dependencies:**
```txt
# requirements.txt (minimal surface area)
Flask==3.0.0
Flask-CORS==4.0.0
Flask-Limiter==3.5.0
gunicorn==21.2.0
```

### Secrets Management

**No Secrets in Code:**
```python
# ❌ NEVER do this
API_KEY = "sk-abc123..."

# ✅ Always use environment variables
import os
API_KEY = os.getenv("API_KEY")
if not API_KEY:
    raise ValueError("API_KEY environment variable required")
```

**Git Security:**
```bash
# .gitignore includes
.env
.env.local
*.secret
*.key
credentials.json

# Pre-commit hook checks for secrets
git-secrets --scan
```

---

## Privacy Specifications

### Privacy Principles

1. **Data Minimization**: Collect only what's needed
2. **Purpose Limitation**: Use data only for stated purpose
3. **Transparency**: Clear privacy policy
4. **User Control**: Users control their data
5. **Security**: Protect all data collected

### Current Data Collection

**What We Collect:**
- ❌ **No personal information**
- ❌ **No email addresses**
- ❌ **No phone numbers**
- ❌ **No geolocation** (except country from IP for language)
- ✅ **Anonymous usage logs** (IP address, request count)
- ✅ **Browser preferences** (stored locally only)

**What We Don't Collect:**
- User accounts (currently)
- Browsing history
- Personal identifiers
- Sensitive personal data
- Cross-site tracking data

### Local Storage Usage

**Browser LocalStorage:**
```javascript
// Only stores user preferences locally
localStorage.setItem('umaja_archetype', 'professor');
localStorage.setItem('umaja_language', 'en');
localStorage.setItem('umaja_visited', 'true');

// Never sent to server
// User can clear anytime
// No tracking across sites
```

### Analytics (Future)

**Privacy-First Analytics:**
```javascript
// Planned: Privacy-preserving analytics
// - No personal identifiers
// - Aggregated data only
// - Opt-out always available
// - GDPR/CCPA compliant

analytics.track('page_view', {
  page: '/daily-smile',
  archetype: 'professor',
  language: 'en',
  // No user ID, no session ID
});
```

### Cookie Policy

**Current:**
- ❌ No cookies used
- ❌ No tracking cookies
- ❌ No advertising cookies

**Future (if needed):**
- Session cookies only (essential)
- Expire after 24 hours
- Secure and HttpOnly flags
- SameSite=Strict

### GDPR Compliance

**Data Subject Rights:**
1. **Right to Access**: No data stored, nothing to access
2. **Right to Rectification**: No data stored, nothing to rectify
3. **Right to Erasure**: Clear browser storage
4. **Right to Data Portability**: Export local storage (JSON)
5. **Right to Object**: Stop using service

**Legal Basis:**
- Legitimate interest (providing service)
- Consent (for future features requiring data)

### CCPA Compliance

**Consumer Rights:**
1. **Right to Know**: Transparent about data practices
2. **Right to Delete**: No centralized data to delete
3. **Right to Opt-Out**: Don't use service = opted out
4. **Right to Non-Discrimination**: Service free for all

**We Do Not:**
- Sell personal information
- Share data with third parties
- Track for advertising

---

## AI Safety and Alignment

### AI Truth Framework

**Core Principle:** AI must distinguish truth from hallucination

```python
class TruthValidator:
    """Ensures AI-generated content is truthful"""
    
    def validate_claim(self, claim):
        """Validate factual claims"""
        # Check against known facts
        if self.is_verifiable_fact(claim):
            return self.verify_with_sources(claim)
        
        # Mark as opinion/fiction if not factual
        if self.is_opinion(claim):
            return {"valid": True, "type": "opinion"}
        
        # Reject hallucinations
        if self.is_hallucination(claim):
            return {"valid": False, "type": "hallucination"}
    
    def verify_with_sources(self, claim):
        """Verify claim against reliable sources"""
        sources = self.fetch_sources(claim)
        confidence = self.calculate_confidence(sources)
        return {
            "valid": confidence > 0.85,
            "confidence": confidence,
            "sources": sources
        }
```

### Alignment with Human Values

**Value Alignment:**
```python
# Bahá'í principles encoded as constraints
ALIGNMENT_PRINCIPLES = {
    "unity": "Promote human unity, never division",
    "truth": "Be truthful, acknowledge uncertainty",
    "service": "Serve humanity without profit motive",
    "justice": "Treat all people equally",
    "compassion": "Show empathy and understanding"
}

def check_alignment(content):
    """Verify content aligns with values"""
    for principle, description in ALIGNMENT_PRINCIPLES.items():
        if not content_aligns_with(content, principle):
            return {
                "aligned": False,
                "violated_principle": principle,
                "description": description
            }
    return {"aligned": True}
```

### Autonomous Behavior Limits

**Hard Limits on Autonomous Agents:**

1. **No Financial Transactions**: Agents cannot spend money
2. **No External Communications**: Agents cannot email/SMS without approval
3. **No Data Deletion**: Agents cannot delete content without review
4. **No System Changes**: Agents cannot modify infrastructure
5. **Emergency Stop**: Human can always stop all agents

**Emergency Stop Mechanism:**
```json
// .github/emergency_stop.json
{
  "autonomous_mode": "RUNNING|STOPPED",
  "last_updated": "2026-01-04T23:00:00Z",
  "reason": "Normal operation",
  "stopped_by": null
}

// All workflows check this file
// If STOPPED, all agents exit immediately
// Can be changed by repository owner anytime
```

### Bias Prevention

**Multi-Cultural Team (Future):**
- Content reviewers from diverse backgrounds
- Translation quality checks by native speakers
- Cultural sensitivity training for AI

**Current Measures:**
- 8 languages from diverse regions
- 3 archetypes respecting different personalities
- Bahá'í principles of unity and equality
- No stereotypes or cultural assumptions

### Transparency Requirements

**AI Disclosure:**
```javascript
// All content clearly marked as AI-generated
{
  "content": "Did you know...",
  "metadata": {
    "generated_by": "AI",
    "model": "GPT-4",
    "human_reviewed": false,
    "source": "UMAJA-Core autonomous system"
  }
}
```

**Model Cards (Future):**
- Document AI capabilities and limitations
- Explain training data and biases
- Provide performance metrics
- Include use case recommendations

---

## Hardware Safety (Future)

### Physical System Safety

**If UMAJA expands to hardware:**

#### Robotics Safety (Hypothetical)
```python
# Three Laws of Robotics (Asimov-inspired)
SAFETY_LAWS = [
    "Never harm humans or allow harm through inaction",
    "Obey human orders unless conflicting with Law 1",
    "Protect own existence unless conflicting with Laws 1-2"
]

# Implementation
class SafetyController:
    def evaluate_action(self, action):
        # Check if action could cause harm
        if self.could_harm_humans(action):
            return "BLOCKED: Violates Law 1"
        
        # Check if action conflicts with human orders
        if self.conflicts_with_orders(action):
            return "BLOCKED: Violates Law 2"
        
        # Check if action risks system safety
        if self.risks_system(action) and not self.required_for_laws_1_2(action):
            return "BLOCKED: Violates Law 3"
        
        return "APPROVED"
```

#### Physical Constraints
- Maximum speed limits
- Force limits for actuators
- Collision detection and avoidance
- Emergency stop button (hardware)
- Failsafe mechanisms

---

## Incident Response

### Incident Classification

**Severity Levels:**

| Level | Description | Response Time | Example |
|-------|-------------|---------------|---------|
| P0 - Critical | System down | Immediate | API completely offline |
| P1 - High | Major functionality broken | < 1 hour | Content generation failed |
| P2 - Medium | Minor functionality broken | < 4 hours | Translation quality issue |
| P3 - Low | Cosmetic issue | < 1 day | Typo in documentation |
| P4 - Info | No impact | Best effort | Feature request |

### Incident Response Process

```
1. Detection
   ├─ Automated monitoring alerts
   ├─ User reports
   └─ Team discovers issue

2. Triage
   ├─ Assess severity
   ├─ Assign priority
   └─ Notify stakeholders

3. Response
   ├─ Emergency stop if needed
   ├─ Investigate root cause
   ├─ Implement fix
   └─ Test fix

4. Recovery
   ├─ Deploy fix
   ├─ Verify resolution
   └─ Resume normal operations

5. Post-Mortem
   ├─ Document incident
   ├─ Root cause analysis
   ├─ Identify improvements
   └─ Update procedures
```

### Security Incident Response

**Security Issue Process:**
1. **Report**: security@umaja-core (future)
2. **Acknowledge**: Within 24 hours
3. **Assess**: Determine severity
4. **Fix**: Develop patch
5. **Disclose**: Responsible disclosure after fix
6. **Learn**: Update security practices

**Vulnerability Disclosure Policy:**
- Responsible disclosure encouraged
- 90-day disclosure timeline
- Credit to reporters (if desired)
- No legal action against good-faith researchers

---

## Compliance and Auditing

### Regular Audits

**Quarterly Reviews:**
- [ ] Content quality review
- [ ] Security vulnerability scan
- [ ] Privacy compliance check
- [ ] Performance metrics analysis
- [ ] User feedback review

**Annual Reviews:**
- [ ] Full security audit
- [ ] Legal compliance review
- [ ] Ethical AI assessment
- [ ] Infrastructure review
- [ ] Disaster recovery test

### Compliance Checklist

**Security:**
- [x] HTTPS only
- [x] Rate limiting enabled
- [x] Input validation
- [x] CORS configured
- [x] No secrets in code
- [ ] Security audit (annual)

**Privacy:**
- [x] No personal data collection
- [x] Privacy policy published
- [x] GDPR compliant
- [x] CCPA compliant
- [ ] Privacy audit (annual)

**Content:**
- [x] Quality validation pipeline
- [x] Cultural sensitivity checks
- [x] Fact verification
- [x] Prohibited content filters
- [ ] Human review process (periodic)

### Documentation

**Required Documentation:**
- [x] Architecture documentation
- [x] API documentation
- [x] Security specifications (this doc)
- [x] Privacy policy
- [ ] Terms of service (future)
- [ ] Incident response playbook

---

## Future Safety Enhancements

### Roadmap

**Q1 2026:**
- [ ] Automated content moderation improvements
- [ ] Enhanced fact-checking system
- [ ] User feedback mechanism
- [ ] Security audit

**Q2 2026:**
- [ ] Privacy-preserving analytics
- [ ] User accounts with strong privacy
- [ ] Advanced AI safety measures
- [ ] Third-party security review

**Q3-Q4 2026:**
- [ ] Real-time content monitoring
- [ ] AI explainability features
- [ ] Comprehensive audit trail
- [ ] ISO 27001 compliance (consider)

---

## References

- [Architecture Documentation](architecture.md)
- [Protocols Documentation](protocols.md)
- [Spiritual Foundation](SPIRITUAL_FOUNDATION.md)
- [Bahá'í Principles](https://www.bahai.org)

---

## Contact

**Security Issues:** Create a GitHub issue with "Security" label  
**Privacy Questions:** Create a GitHub discussion  
**General Safety Concerns:** Create a GitHub issue

---

**Last Updated:** January 4, 2026  
**Version:** 1.0.0  
**Status:** Production  
**Next Review:** April 4, 2026
