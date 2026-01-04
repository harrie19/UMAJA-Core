# UMAJA System Specifications

## Overview

Complete technical specifications for the UMAJA-Core system, including architecture, APIs, data formats, performance requirements, and operational parameters.

---

## System Architecture Specifications

### High-Level Architecture

**System Type:** Distributed web application with autonomous agent network  
**Deployment Model:** Dual deployment (CDN + API)  
**Scale Target:** 8 billion users  
**Availability Target:** 99.9% uptime

### Component Specifications

#### 1. Backend API Server

**Platform:** Railway (production), Local development  
**Runtime:** Python 3.11+  
**Framework:** Flask 3.0.0  
**WSGI Server:** Gunicorn 21.2.0

**Server Configuration:**
```python
# Gunicorn Configuration
bind = "0.0.0.0:5000"
workers = 2
threads = 4
worker_class = "sync"
timeout = 30
keepalive = 2
max_requests = 1000
max_requests_jitter = 50
preload_app = True
```

**Dependencies:**
```txt
Flask==3.0.0
Flask-CORS==4.0.0
Flask-Limiter==3.5.0
gunicorn==21.2.0
requests>=2.31.0
```

#### 2. Frontend CDN

**Platform:** GitHub Pages  
**Content Type:** Static HTML/CSS/JavaScript  
**Compression:** Gzip (60% reduction)  
**Caching:** 24-hour cache headers

**Technology Stack:**
```javascript
// Frontend Technologies
HTML5: Semantic markup
CSS3: Grid + Flexbox layouts
JavaScript: ES6+ (Vanilla, no frameworks)
Service Worker: PWA capabilities
```

#### 3. Autonomous Agent Network

**Agent Types:** 9 specialized agents  
**Execution:** GitHub Actions workflows  
**Coordination:** Agent Orchestrator  
**Communication:** Message passing via task queue

**Agent Specifications:**

| Agent | Purpose | Frequency | Priority | Timeout |
|-------|---------|-----------|----------|---------|
| ContentGenerator | Generate smiles | Every 4h | 8 | 10min |
| Translator | Translate content | On demand | 9 | 5min |
| QualityChecker | Validate content | On demand | 10 | 3min |
| Distributor | Save to CDN | On demand | 7 | 2min |
| Analytics | Track metrics | Hourly | 5 | 2min |
| Scheduler | Plan tasks | Continuous | 6 | 1min |
| ErrorHandler | Handle failures | As needed | 10 | 1min |
| LearningAgent | Optimize | Daily | 4 | 5min |
| CoordinatorAgent | Orchestrate all | Continuous | 9 | 2min |

---

## API Specifications

### REST API Endpoints

#### Health Check
```
GET /health
Response: 200 OK
Content-Type: application/json

{
  "status": "healthy",
  "service": "UMAJA-Core",
  "version": "2.1.0",
  "checks": {
    "api": "ok",
    "smiles_loaded": true,
    "archetypes_available": ["professor", "worrier", "enthusiast"]
  }
}
```

#### Daily Smile
```
GET /api/daily-smile
Response: 200 OK
Content-Type: application/json
Rate Limit: 100/hour, 20/minute

{
  "content": "string (200-500 chars)",
  "archetype": "professor|worrier|enthusiast",
  "mission": "Serving 8 billion people",
  "principle": "Truth, Unity, Service"
}
```

#### World Tour Status
```
GET /worldtour/status
Response: 200 OK
Content-Type: application/json

{
  "status": "live",
  "total_cities": 59,
  "cities_visited": 5,
  "progress_percentage": 8.5,
  "current_city": "string",
  "next_city": "string"
}
```

### Rate Limiting

**Standard Limits:**
- Per IP: 100 requests/hour
- Burst: 20 requests/minute
- World Tour endpoints: 10 requests/minute

**Headers:**
```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1704283200
```

**Exceeded Response:**
```
HTTP/1.1 429 Too Many Requests
Retry-After: 120

{
  "error": {
    "code": "RATE_LIMIT_EXCEEDED",
    "message": "Rate limit exceeded. Please try again in 120 seconds."
  }
}
```

---

## Data Format Specifications

### Content Data Format

**JSON Schema:**
```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "required": ["id", "archetype", "language", "content", "metadata"],
  "properties": {
    "id": {
      "type": "integer",
      "minimum": 1,
      "description": "Unique content identifier"
    },
    "archetype": {
      "type": "string",
      "enum": ["professor", "worrier", "enthusiast"]
    },
    "language": {
      "type": "string",
      "pattern": "^[a-z]{2}$",
      "description": "ISO 639-1 language code"
    },
    "content": {
      "type": "string",
      "minLength": 50,
      "maxLength": 1000,
      "description": "The smile content"
    },
    "metadata": {
      "type": "object",
      "properties": {
        "generated_at": {
          "type": "string",
          "format": "date-time"
        },
        "quality_score": {
          "type": "number",
          "minimum": 0.0,
          "maximum": 1.0
        },
        "topic": {
          "type": "string"
        },
        "word_count": {
          "type": "integer",
          "minimum": 1
        }
      }
    }
  }
}
```

**Example:**
```json
{
  "id": 1,
  "archetype": "professor",
  "language": "en",
  "content": "Did you know that honey never spoils? Archaeologists have found 3000-year-old honey in Egyptian tombs that's still perfectly edible. Nature's time capsule! 🍯",
  "metadata": {
    "generated_at": "2026-01-01T00:00:00Z",
    "quality_score": 0.91,
    "topic": "science",
    "word_count": 28,
    "emoji_count": 1
  }
}
```

### Manifest Format

**CDN Manifest:**
```json
{
  "version": "2.1.0",
  "last_updated": "2026-01-04T23:00:00Z",
  "total_smiles": 8760,
  "archetypes": {
    "professor": { "count": 2920, "languages": ["en", "es", ...] },
    "worrier": { "count": 2920, "languages": ["en", "es", ...] },
    "enthusiast": { "count": 2920, "languages": ["en", "es", ...] }
  },
  "index": [
    {
      "id": 1,
      "archetype": "professor",
      "languages": ["en", "es", "fr", "ar", "zh", "hi", "pt", "sw"],
      "date": "2026-01-01",
      "paths": {
        "en": "cdn/smiles/professor/en/1.json",
        "es": "cdn/smiles/professor/es/1.json"
      }
    }
  ]
}
```

---

## Performance Specifications

### Response Time Requirements

| Endpoint | Target (p50) | Target (p95) | Target (p99) | Max |
|----------|--------------|--------------|--------------|-----|
| GET /health | <50ms | <100ms | <200ms | 500ms |
| GET /api/daily-smile | <75ms | <150ms | <300ms | 1000ms |
| CDN content | <30ms | <100ms | <200ms | 500ms |
| World Tour API | <100ms | <200ms | <500ms | 2000ms |

### Throughput Requirements

**API Server:**
- Minimum: 10 requests/second sustained
- Target: 50 requests/second sustained
- Peak: 100 requests/second for 1 minute

**CDN:**
- Minimum: 1,000 requests/second
- Target: 10,000 requests/second
- Peak: 100,000 requests/second (cached)

### Resource Limits

**GitHub Actions:**
- Monthly limit: 2,000 minutes
- Per workflow: 10 minutes max
- Concurrent workflows: 20

**Railway API:**
- CPU: 0.5 vCPU shared
- Memory: 512 MB
- Storage: 1 GB (ephemeral)
- Bandwidth: Unlimited

**GitHub Pages:**
- Storage: 1 GB (soft limit)
- Bandwidth: 100 GB/month (soft limit)
- Build time: 10 minutes

---

## Data Storage Specifications

### Content Storage

**Structure:**
```
cdn/
└── smiles/
    ├── manifest.json (15-20 KB)
    ├── professor/
    │   ├── en/ (365 files, ~100 KB total)
    │   ├── es/ (365 files, ~100 KB total)
    │   └── ... (8 languages)
    ├── worrier/
    │   └── ... (8 languages)
    └── enthusiast/
        └── ... (8 languages)

Total uncompressed: ~2.6 MB
Total compressed (gzip): ~1 MB
```

**File Naming:**
```
Pattern: {archetype}/{language}/{id}.json
Example: professor/en/1.json

Compressed: {archetype}/{language}/{id}.json.gz
Example: professor/en/1.json.gz
```

### Backup and Versioning

**Git-based Versioning:**
- All content committed to Git
- Full history available
- Point-in-time recovery
- Distributed backups (GitHub)

**Retention Policy:**
- Content: Permanent (Git history)
- Logs: 30 days
- Analytics: 90 days
- Backups: Not needed (Git is backup)

---

## Security Specifications

### Transport Security

**TLS Requirements:**
- Minimum: TLS 1.2
- Recommended: TLS 1.3
- Cipher suites: Modern, strong ciphers only
- Certificate: Valid, trusted CA

**HTTPS Enforcement:**
```nginx
# All HTTP requests redirect to HTTPS
if ($scheme = http) {
    return 301 https://$host$request_uri;
}
```

### API Security

**CORS Policy:**
```python
ALLOWED_ORIGINS = [
    "https://harrie19.github.io",
    "https://umaja-core-production.up.railway.app"
]

CORS(app,
     origins=ALLOWED_ORIGINS,
     methods=["GET", "POST"],
     allow_headers=["Content-Type"],
     max_age=3600)
```

**Input Validation:**
```python
# All inputs validated before processing
def validate_archetype(value):
    VALID = ["professor", "worrier", "enthusiast"]
    if value not in VALID:
        raise ValueError(f"Invalid archetype: {value}")
    return value

def validate_language(value):
    VALID = ["en", "es", "fr", "ar", "zh", "hi", "pt", "sw"]
    if value not in VALID:
        raise ValueError(f"Invalid language: {value}")
    return value
```

### Content Security Policy

**CSP Header:**
```
Content-Security-Policy:
  default-src 'self';
  script-src 'self' 'unsafe-inline';
  style-src 'self' 'unsafe-inline';
  img-src 'self' data: https:;
  connect-src 'self' https://umaja-core-production.up.railway.app;
  font-src 'self';
  frame-ancestors 'none';
  base-uri 'self';
  form-action 'self';
```

---

## Quality Specifications

### Content Quality Metrics

**Required Thresholds:**
```python
QUALITY_THRESHOLDS = {
    "semantic_coherence": 0.70,      # Must be logical and clear
    "cultural_sensitivity": 0.90,    # Must respect all cultures
    "factual_accuracy": 0.85,        # Facts must be verifiable
    "positive_sentiment": 0.75,      # Must be uplifting
    "appropriateness": 1.00,         # Must be appropriate
    "translation_quality": 0.85      # Accurate translation
}

# Overall quality score must be ≥ 0.70
overall_quality = weighted_average(quality_metrics)
approved = overall_quality >= 0.70
```

### System Quality Metrics

**Availability:**
- Target: 99.9% uptime (43 minutes downtime/month)
- Measurement: External monitoring, 1-minute checks
- Acceptable outage: <15 minutes unplanned

**Reliability:**
- Error rate: <1% of requests
- Content generation success: >98%
- Quality check pass rate: >95%

**Performance:**
- API response time p95: <150ms
- CDN response time p95: <100ms
- Content generation time: <30s per piece

---

## Operational Specifications

### Monitoring Requirements

**Health Checks:**
```yaml
Frequency: Every 1 minute
Timeout: 5 seconds
Failure threshold: 3 consecutive failures
Success threshold: 2 consecutive successes

Checks:
  - API /health endpoint responds 200
  - CDN manifest.json accessible
  - GitHub Pages site loads
  - Autonomous workflows running
```

**Alerting:**
```yaml
Critical (immediate):
  - API down >5 minutes
  - CDN unreachable >5 minutes
  - Error rate >10%
  - Quality score <0.60

Warning (1 hour):
  - API slow (p95 >300ms)
  - Error rate >5%
  - Quality score <0.70
  - Resource usage >85%

Info (daily summary):
  - Usage statistics
  - Performance metrics
  - Content generation stats
```

### Deployment Specifications

**Deployment Strategy:**
- Blue-green deployment (future)
- Rolling updates for API
- CDN updates: Instant (Git push)
- Rollback time: <5 minutes

**Deployment Checklist:**
```markdown
Pre-Deployment:
- [ ] Code review completed
- [ ] Tests passing
- [ ] Security scan passed
- [ ] Documentation updated

Deployment:
- [ ] Deploy to staging
- [ ] Run smoke tests
- [ ] Deploy to production
- [ ] Verify health checks

Post-Deployment:
- [ ] Monitor for 30 minutes
- [ ] Check error rates
- [ ] Review performance
- [ ] Confirm functionality
```

---

## Compliance Specifications

### Data Protection

**GDPR Compliance:**
- [x] No personal data collected (currently)
- [x] Privacy policy published
- [x] Data minimization
- [x] User rights respected
- [ ] DPO appointed (if needed)

**CCPA Compliance:**
- [x] No sale of personal information
- [x] Opt-out mechanism (don't use service)
- [x] Privacy notice
- [x] Data access rights

### Accessibility

**WCAG 2.1 Level AA:**
- [ ] Keyboard navigation
- [ ] Screen reader compatible
- [ ] Color contrast ≥4.5:1
- [ ] Text alternatives for images
- [ ] Semantic HTML

### Internationalization

**i18n Support:**
- [x] UTF-8 encoding everywhere
- [x] Right-to-left (RTL) support (Arabic)
- [x] Character set support (Chinese, Arabic, etc.)
- [ ] Number/date formatting per locale
- [ ] Currency formatting (if needed)

---

## Testing Specifications

### Test Coverage Requirements

**Unit Tests:**
- Coverage target: 80%
- Critical paths: 100%
- Run frequency: Every commit

**Integration Tests:**
- API endpoints: 100%
- Agent communication: 100%
- Run frequency: Every PR

**End-to-End Tests:**
- User journeys: Key paths
- Cross-browser: Chrome, Firefox, Safari, Edge
- Run frequency: Before deployment

### Test Data

**Test Content:**
```json
{
  "test_smiles": [
    {
      "id": 9999,
      "archetype": "professor",
      "language": "en",
      "content": "Test content for automated testing",
      "metadata": {
        "test": true
      }
    }
  ]
}
```

---

## Disaster Recovery Specifications

### Backup Strategy

**What's Backed Up:**
- [x] All content (Git)
- [x] Configuration (Git)
- [x] Documentation (Git)
- [ ] User data (when implemented)

**Backup Frequency:**
- Content: Every commit (automatic)
- Configuration: Every change
- Logs: Not backed up (ephemeral)

**Recovery Time Objective (RTO):**
- API server: 30 minutes
- CDN content: 5 minutes (Git revert)
- Complete system: 1 hour

**Recovery Point Objective (RPO):**
- Content loss: 0 (Git history)
- Configuration loss: 0 (Git history)
- Logs loss: Acceptable

### Failover Procedures

**API Failover:**
```
Primary: Railway
    ↓ (if down)
Fallback: Vercel or Heroku
    ↓ (if down)
Static CDN: GitHub Pages
```

**CDN Failover:**
```
Primary: GitHub Pages
    ↓ (if down)
Fallback: Cloudflare Pages
    ↓ (if down)
Tertiary: Vercel
```

---

## Version Control Specifications

### Versioning Scheme

**Semantic Versioning:** MAJOR.MINOR.PATCH

- MAJOR: Breaking changes
- MINOR: New features (backward compatible)
- PATCH: Bug fixes

**Current Version:** 2.1.0

### Changelog

**Required for Each Release:**
```markdown
## [2.1.0] - 2026-01-04

### Added
- World Tour feature
- Autonomous agent system

### Changed
- Improved quality validation

### Fixed
- Translation accuracy issues

### Security
- Added rate limiting
```

---

## Appendices

### Appendix A: Glossary

- **Archetype**: Personality type (Professor, Worrier, Enthusiast)
- **CDN**: Content Delivery Network
- **Smile**: Daily inspirational content piece
- **Agent**: Autonomous software component
- **Vector**: High-dimensional numerical representation

### Appendix B: References

- [Architecture Documentation](architecture.md)
- [API Documentation](API_DOCUMENTATION.md)
- [Safety Documentation](safety.md)
- [Protocols Documentation](protocols.md)

---

**Last Updated:** January 4, 2026  
**Version:** 1.0.0  
**Status:** Production  
**Next Review:** April 2026
