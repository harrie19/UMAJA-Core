# UMAJA Communication Protocols and API Specifications

## Overview

This document defines the communication protocols, API specifications, and inter-agent communication patterns used throughout the UMAJA-Core system.

---

## API Protocol Specifications

### REST API Design

UMAJA-Core follows RESTful design principles with the following characteristics:

#### Base URLs
- **Production:** `https://umaja-core-production.up.railway.app`
- **GitHub Pages:** `https://harrie19.github.io/UMAJA-Core/`

#### HTTP Methods
- `GET`: Retrieve resources (idempotent, cacheable)
- `POST`: Create resources or trigger actions
- `PUT`: Update resources (future)
- `DELETE`: Remove resources (future)

#### Response Format
All responses use JSON with consistent structure:

```json
{
  "status": "success|error",
  "data": { /* response payload */ },
  "error": { /* error details if status=error */ },
  "metadata": {
    "timestamp": "2026-01-04T23:00:00Z",
    "version": "2.1.0",
    "request_id": "uuid"
  }
}
```

---

## Core API Endpoints

### Health and Status

#### GET /health

**Purpose:** Service health monitoring

**Request:**
```http
GET /health HTTP/1.1
Host: umaja-core-production.up.railway.app
Accept: application/json
```

**Response:**
```json
{
  "status": "healthy",
  "service": "UMAJA-Core",
  "version": "2.1.0",
  "mission": "8 billion smiles",
  "timestamp": "2026-01-04T23:00:00Z",
  "environment": "production",
  "security": {
    "rate_limiting": "enabled",
    "request_timeout": "30s",
    "cors": "enabled"
  },
  "checks": {
    "api": "ok",
    "smiles_loaded": true,
    "archetypes_available": ["professor", "worrier", "enthusiast"],
    "content_generation": "ok"
  }
}
```

**Status Codes:**
- `200 OK`: Service healthy
- `503 Service Unavailable`: Service unhealthy

#### GET /version

**Purpose:** Version and deployment information

**Response:**
```json
{
  "version": "2.1.0",
  "deployment_date": "2026-01-02",
  "service": "UMAJA-Core Minimal Server",
  "mission": "Bringing smiles to 8 billion people",
  "principle": "Service, not profit",
  "python_version": "3.11.0"
}
```

---

### Content Delivery

#### GET /api/daily-smile

**Purpose:** Retrieve daily inspiration

**Request:**
```http
GET /api/daily-smile HTTP/1.1
Host: umaja-core-production.up.railway.app
Accept: application/json
```

**Response:**
```json
{
  "content": "Did you know that honey never spoils? Archaeologists have found 3000-year-old honey in Egyptian tombs that's still perfectly edible. Nature's time capsule! 🍯",
  "archetype": "professor",
  "mission": "Serving 8 billion people",
  "principle": "Truth, Unity, Service"
}
```

**Rate Limits:**
- Standard: 100 requests/hour per IP
- Burst: 20 requests/minute

#### GET /api/smile/{archetype}

**Purpose:** Get archetype-specific content

**Parameters:**
- `archetype` (path): One of `professor`, `worrier`, `enthusiast`

**Request:**
```http
GET /api/smile/professor HTTP/1.1
Host: umaja-core-production.up.railway.app
Accept: application/json
```

**Response:**
```json
{
  "content": "Let me share a fascinating fact...",
  "archetype": "professor",
  "language": "en",
  "category": "educational"
}
```

**Status Codes:**
- `200 OK`: Success
- `400 Bad Request`: Invalid archetype
- `404 Not Found`: No content available
- `429 Too Many Requests`: Rate limit exceeded

---

### World Tour API

#### POST /worldtour/start

**Purpose:** Trigger world tour content generation

**Request:**
```http
POST /worldtour/start HTTP/1.1
Host: umaja-core-production.up.railway.app
Content-Type: application/json

{
  "city_id": "optional",
  "personalities": ["john_cleese", "c3po", "robin_williams"],
  "content_types": ["city_review", "food_review"]
}
```

**Response:**
```json
{
  "status": "started",
  "city": "Cairo",
  "personalities": ["john_cleese", "c3po", "robin_williams"],
  "content_types": ["city_review", "food_review", "cultural_debate", "language_lesson", "tourist_trap"],
  "estimated_completion": "2026-01-04T23:05:00Z",
  "job_id": "uuid"
}
```

**Rate Limits:**
- 10 requests/minute
- 50 requests/hour

#### GET /worldtour/status

**Purpose:** Get world tour statistics

**Request:**
```http
GET /worldtour/status HTTP/1.1
Host: umaja-core-production.up.railway.app
Accept: application/json
```

**Response:**
```json
{
  "status": "live",
  "total_cities": 59,
  "cities_visited": 5,
  "progress_percentage": 8.5,
  "current_city": "Cairo",
  "next_city": "Mumbai",
  "launch_date": "2026-01-02",
  "content_generated": {
    "total_pieces": 75,
    "by_personality": {
      "john_cleese": 25,
      "c3po": 25,
      "robin_williams": 25
    },
    "by_type": {
      "city_review": 15,
      "food_review": 15,
      "cultural_debate": 15,
      "language_lesson": 15,
      "tourist_trap": 15
    }
  }
}
```

#### GET /worldtour/cities

**Purpose:** List all cities in the tour

**Query Parameters:**
- `status` (optional): Filter by `visited` or `pending`
- `page` (optional): Pagination, default 1
- `per_page` (optional): Results per page, default 20, max 100

**Request:**
```http
GET /worldtour/cities?status=visited&page=1&per_page=10 HTTP/1.1
Host: umaja-core-production.up.railway.app
Accept: application/json
```

**Response:**
```json
{
  "cities": [
    {
      "id": "cairo",
      "name": "Cairo",
      "country": "Egypt",
      "region": "Middle East",
      "population": 20000000,
      "visited": true,
      "visit_date": "2026-01-03",
      "content_count": 15
    }
  ],
  "pagination": {
    "page": 1,
    "per_page": 10,
    "total_items": 5,
    "total_pages": 1
  }
}
```

---

## Inter-Agent Communication Protocol

### Agent Message Format

Agents communicate using a standardized message format:

```python
{
  "message_id": "uuid",
  "timestamp": "2026-01-04T23:00:00Z",
  "sender": "ContentGenerator",
  "recipient": "QualityChecker",
  "message_type": "task|response|notification|error",
  "priority": 1-10,
  "payload": {
    # Message-specific data
  },
  "metadata": {
    "correlation_id": "uuid",
    "retry_count": 0,
    "expires_at": "2026-01-04T23:30:00Z"
  }
}
```

### Message Types

#### Task Message
Sender requests recipient to perform work:

```python
{
  "message_type": "task",
  "payload": {
    "action": "generate_content",
    "parameters": {
      "archetype": "professor",
      "language": "en",
      "topic": "science"
    },
    "callback": "QualityChecker.validate"
  }
}
```

#### Response Message
Recipient returns results:

```python
{
  "message_type": "response",
  "payload": {
    "status": "success|failure",
    "result": {
      "content": "Generated content...",
      "quality_score": 0.87
    },
    "error": null
  }
}
```

#### Notification Message
Agent broadcasts information:

```python
{
  "message_type": "notification",
  "payload": {
    "event": "content_generated",
    "details": {
      "count": 24,
      "timestamp": "2026-01-04T23:00:00Z"
    }
  }
}
```

#### Error Message
Agent reports failure:

```python
{
  "message_type": "error",
  "payload": {
    "error_type": "ValidationError",
    "error_message": "Content failed quality check",
    "error_details": {
      "quality_score": 0.45,
      "threshold": 0.70
    },
    "recoverable": true,
    "retry_suggested": true
  }
}
```

---

## Agent-Specific Protocols

### ContentGenerator → Translator

**Protocol:** Generate content in English, then translate

```python
# Step 1: ContentGenerator creates base content
{
  "sender": "ContentGenerator",
  "recipient": "Translator",
  "message_type": "task",
  "payload": {
    "action": "translate_content",
    "source_language": "en",
    "target_languages": ["es", "fr", "ar", "zh", "hi", "pt", "sw"],
    "content": {
      "text": "Did you know...",
      "archetype": "professor",
      "metadata": {
        "topic": "science",
        "tone": "educational"
      }
    }
  }
}

# Step 2: Translator returns translations
{
  "sender": "Translator",
  "recipient": "ContentGenerator",
  "message_type": "response",
  "payload": {
    "status": "success",
    "translations": {
      "es": "¿Sabías que...",
      "fr": "Saviez-vous...",
      "ar": "هل تعلم...",
      "zh": "你知道吗...",
      "hi": "क्या आप जानते हैं...",
      "pt": "Você sabia...",
      "sw": "Je, ulijua..."
    }
  }
}
```

### Translator → QualityChecker

**Protocol:** Validate translated content

```python
# Step 1: Translator requests validation
{
  "sender": "Translator",
  "recipient": "QualityChecker",
  "message_type": "task",
  "payload": {
    "action": "validate_translations",
    "original": {
      "language": "en",
      "text": "Did you know..."
    },
    "translations": {
      "es": "¿Sabías que...",
      "fr": "Saviez-vous..."
    },
    "criteria": {
      "semantic_similarity": 0.85,
      "cultural_appropriateness": true,
      "tone_match": true
    }
  }
}

# Step 2: QualityChecker returns validation results
{
  "sender": "QualityChecker",
  "recipient": "Translator",
  "message_type": "response",
  "payload": {
    "status": "success",
    "validation_results": {
      "es": {
        "approved": true,
        "semantic_similarity": 0.92,
        "issues": []
      },
      "fr": {
        "approved": true,
        "semantic_similarity": 0.89,
        "issues": []
      }
    },
    "overall_approved": true
  }
}
```

### QualityChecker → Distributor

**Protocol:** Distribute approved content

```python
# Step 1: QualityChecker sends approved content
{
  "sender": "QualityChecker",
  "recipient": "Distributor",
  "message_type": "task",
  "payload": {
    "action": "distribute_content",
    "content": {
      "archetype": "professor",
      "translations": {
        "en": "...",
        "es": "...",
        # ... all languages
      },
      "metadata": {
        "quality_score": 0.91,
        "approved_at": "2026-01-04T23:00:00Z",
        "approved_by": "QualityChecker"
      }
    },
    "channels": ["cdn", "api_cache"]
  }
}

# Step 2: Distributor confirms distribution
{
  "sender": "Distributor",
  "recipient": "QualityChecker",
  "message_type": "response",
  "payload": {
    "status": "success",
    "distribution_results": {
      "cdn": {
        "status": "success",
        "file_path": "cdn/smiles/professor/en/1.json",
        "url": "https://harrie19.github.io/UMAJA-Core/cdn/smiles/professor/en/1.json"
      },
      "api_cache": {
        "status": "success",
        "cache_key": "smile:professor:en:20260104"
      }
    }
  }
}
```

### ErrorHandler → All Agents

**Protocol:** Error notification and recovery

```python
# Step 1: Agent encounters error
{
  "sender": "ContentGenerator",
  "recipient": "ErrorHandler",
  "message_type": "error",
  "payload": {
    "error_type": "APITimeout",
    "error_message": "OpenAI API timeout after 30s",
    "task_id": "uuid",
    "retryable": true
  }
}

# Step 2: ErrorHandler decides recovery strategy
{
  "sender": "ErrorHandler",
  "recipient": "ContentGenerator",
  "message_type": "task",
  "payload": {
    "action": "retry_task",
    "task_id": "uuid",
    "retry_delay": 10,
    "retry_count": 1,
    "max_retries": 3,
    "fallback_strategy": "use_cached_content"
  }
}
```

### Analytics → LearningAgent

**Protocol:** Share performance metrics for optimization

```python
# Step 1: Analytics sends metrics
{
  "sender": "Analytics",
  "recipient": "LearningAgent",
  "message_type": "notification",
  "payload": {
    "event": "daily_metrics",
    "metrics": {
      "content_generated": 72,
      "average_quality_score": 0.87,
      "generation_time_avg_ms": 2834,
      "translation_accuracy": 0.91,
      "distribution_success_rate": 0.98
    },
    "period": {
      "start": "2026-01-04T00:00:00Z",
      "end": "2026-01-04T23:59:59Z"
    }
  }
}

# Step 2: LearningAgent identifies optimization opportunity
{
  "sender": "LearningAgent",
  "recipient": "CoordinatorAgent",
  "message_type": "notification",
  "payload": {
    "event": "optimization_identified",
    "recommendation": {
      "area": "content_generation",
      "current_performance": 2834,
      "target_performance": 2000,
      "strategy": "increase_batch_size",
      "expected_improvement": "30% faster"
    }
  }
}
```

---

## CDN Protocol

### Content Delivery Protocol

#### File Structure
```
cdn/
└── smiles/
    ├── manifest.json           # Index of all content
    ├── professor/
    │   ├── en/
    │   │   ├── 1.json         # Original JSON
    │   │   └── 1.json.gz      # Gzip compressed
    │   ├── es/
    │   └── ...
    ├── worrier/
    └── enthusiast/
```

#### Manifest Format
```json
{
  "version": "2.1.0",
  "last_updated": "2026-01-04T23:00:00Z",
  "total_smiles": 8760,
  "archetypes": {
    "professor": {
      "count": 2920,
      "languages": ["en", "es", "fr", "ar", "zh", "hi", "pt", "sw"]
    },
    "worrier": {
      "count": 2920,
      "languages": ["en", "es", "fr", "ar", "zh", "hi", "pt", "sw"]
    },
    "enthusiast": {
      "count": 2920,
      "languages": ["en", "es", "fr", "ar", "zh", "hi", "pt", "sw"]
    }
  },
  "index": [
    {
      "id": 1,
      "archetype": "professor",
      "languages": ["en", "es", "fr", "ar", "zh", "hi", "pt", "sw"],
      "date": "2026-01-01",
      "paths": {
        "en": "cdn/smiles/professor/en/1.json"
      }
    }
  ]
}
```

#### Content File Format
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

#### Client Request Protocol

**Preferred Method (CDN):**
```javascript
// 1. Fetch manifest
const manifest = await fetch('https://harrie19.github.io/UMAJA-Core/cdn/smiles/manifest.json');

// 2. Select content based on user preferences
const archetype = 'professor';
const language = 'en';
const contentId = getTodayContentId();

// 3. Fetch specific content (try compressed first)
const url = `https://harrie19.github.io/UMAJA-Core/cdn/smiles/${archetype}/${language}/${contentId}.json.gz`;
const response = await fetch(url);
const content = await response.json();
```

**Fallback Method (API):**
```javascript
// If CDN fails, use API
const response = await fetch('https://umaja-core-production.up.railway.app/api/daily-smile');
const content = await response.json();
```

---

## Rate Limiting Protocol

### Rate Limit Headers

All API responses include rate limit information:

```http
HTTP/1.1 200 OK
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1704283200
X-RateLimit-Retry-After: 60
```

**Header Meanings:**
- `X-RateLimit-Limit`: Maximum requests allowed in window
- `X-RateLimit-Remaining`: Requests remaining in current window
- `X-RateLimit-Reset`: Unix timestamp when limit resets
- `X-RateLimit-Retry-After`: Seconds to wait before retrying (only when limited)

### Rate Limit Response

When rate limit exceeded:

```http
HTTP/1.1 429 Too Many Requests
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 0
X-RateLimit-Reset: 1704283200
X-RateLimit-Retry-After: 120
Content-Type: application/json

{
  "status": "error",
  "error": {
    "code": "RATE_LIMIT_EXCEEDED",
    "message": "Rate limit exceeded. Please try again in 120 seconds.",
    "details": {
      "limit": 100,
      "window": "1 hour",
      "retry_after": 120
    }
  }
}
```

### Rate Limit Tiers

| Endpoint | Requests/Minute | Requests/Hour |
|----------|-----------------|---------------|
| GET /health | 20 | 100 |
| GET /api/daily-smile | 20 | 100 |
| GET /api/smile/{archetype} | 20 | 100 |
| POST /worldtour/start | 10 | 50 |
| GET /worldtour/status | 20 | 100 |
| GET /worldtour/cities | 20 | 100 |

---

## Error Response Protocol

### Standard Error Format

```json
{
  "status": "error",
  "error": {
    "code": "ERROR_CODE",
    "message": "Human-readable error message",
    "details": {
      "field": "additional context"
    },
    "documentation": "https://github.com/harrie19/UMAJA-Core/docs/protocols.md#error-code"
  },
  "metadata": {
    "timestamp": "2026-01-04T23:00:00Z",
    "request_id": "uuid",
    "version": "2.1.0"
  }
}
```

### Error Codes

| Code | HTTP Status | Description |
|------|-------------|-------------|
| INVALID_REQUEST | 400 | Malformed request |
| INVALID_ARCHETYPE | 400 | Unknown archetype |
| INVALID_LANGUAGE | 400 | Unsupported language |
| NOT_FOUND | 404 | Resource not found |
| RATE_LIMIT_EXCEEDED | 429 | Too many requests |
| INTERNAL_ERROR | 500 | Server error |
| SERVICE_UNAVAILABLE | 503 | Service down |
| CONTENT_NOT_AVAILABLE | 404 | No content for request |
| VALIDATION_FAILED | 400 | Content validation failed |
| GENERATION_FAILED | 500 | Content generation failed |

---

## Versioning Protocol

### API Versioning

Current approach: Version in URL path (future)
```
/api/v2/daily-smile
```

Current: Version in response headers
```http
X-API-Version: 2.1.0
```

### Backward Compatibility

**Guarantees:**
- Existing endpoints remain functional
- Response format additive (new fields OK, removing fields = breaking change)
- Breaking changes increment major version
- Deprecation warnings 90 days before removal

**Deprecation Header:**
```http
X-API-Deprecated: true
X-API-Sunset-Date: 2026-04-01
X-API-Replacement: /api/v3/daily-inspiration
```

---

## WebSocket Protocol (Future)

### Planned for Real-Time Features

```javascript
// Connection
const ws = new WebSocket('wss://umaja-core-production.up.railway.app/ws');

// Subscribe to events
ws.send(JSON.stringify({
  action: 'subscribe',
  events: ['new_content', 'worldtour_update']
}));

// Receive updates
ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  // { event: 'new_content', payload: {...} }
};
```

---

## References

- [Architecture Documentation](architecture.md)
- [API Documentation](API_DOCUMENTATION.md)
- [Security Specifications](safety.md)

---

**Last Updated:** January 4, 2026  
**Version:** 1.0.0  
**Status:** Production
