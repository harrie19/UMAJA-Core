# 📚 UMAJA World Tour - Complete API Documentation

## Overview

The UMAJA World Tour API provides programmatic access to our comedy content, city database, and tour statistics. All endpoints are REST-based and return JSON responses.

**Base URLs**:
- Production API: `https://web-production-6ec45.up.railway.app`
- GitHub Pages: `https://harrie19.github.io/UMAJA-Core/`

**Version**: 2.1.0  
**License**: CC-BY 4.0  
**Contact**: Umaja1919@googlemail.com

---

## 🔐 Authentication

Currently, the API is **open and free** - no authentication required!

### Rate Limits
- Standard endpoints: **100 requests/hour per IP**
- Burst limit: **20 requests/minute**
- World Tour endpoints: **10-20 requests/minute** (see individual endpoints)

Rate limit headers included in responses:
```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1704283200
```

**Need higher limits?** Contact us at Umaja1919@googlemail.com

---

## 📍 Core Endpoints

### Health Check

#### `GET /health`

Check if the service is operational.

**Response**:
```json
{
  "status": "healthy",
  "service": "UMAJA-Core",
  "version": "2.1.0",
  "mission": "8 billion smiles",
  "timestamp": "2026-01-03T12:00:00Z",
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

**Status Codes**:
- `200 OK`: Service is healthy
- `503 Service Unavailable`: Service is unhealthy

---

### Version Information

#### `GET /version`

Get version and deployment information.

**Response**:
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

### Root Endpoint

#### `GET /`

Get API information and available endpoints.

**Response**:
```json
{
  "service": "UMAJA-Core API",
  "version": "2.1.0",
  "mission": "8 billion smiles 🌍",
  "endpoints": {
    "health": "/health",
    "version": "/version",
    "daily_smile": "/api/daily-smile",
    "worldtour_start": "POST /worldtour/start",
    "worldtour_status": "GET /worldtour/status",
    "worldtour_cities": "GET /worldtour/cities"
  },
  "worldtour": {
    "status": "live",
    "personalities": ["john_cleese", "c3po", "robin_williams"],
    "content_types": ["city_review", "cultural_debate", "language_lesson", "tourist_trap", "food_review"]
  }
}
```

---

## 😊 Daily Smile Endpoints

### Get Daily Smile

#### `GET /api/daily-smile`

Get today's random smile/inspiration.

**Response**:
```json
{
  "content": "Did you know that honey never spoils? Archaeologists have found 3000-year-old honey in Egyptian tombs that's still perfectly edible. Nature's time capsule! 🍯",
  "archetype": "professor",
  "mission": "Serving 8 billion people",
  "principle": "Truth, Unity, Service"
}
```

---

### Get Smile by Archetype

#### `GET /api/smile/{archetype}`

Get a smile from a specific archetype.

**Parameters**:
- `archetype` (path): One of `professor`, `worrier`, `enthusiast`

**Example**:
```bash
GET /api/smile/enthusiast
```

**Response**:
```json
{
  "content": "RIGHT NOW, somewhere in the world, someone just learned to ride a bike for the first time! EVERY. SINGLE. DAY. How amazing is that?! 🚴",
  "archetype": "enthusiast"
}
```

**Status Codes**:
- `200 OK`: Success
- `404 Not Found`: Unknown archetype

---

## 🌍 World Tour Endpoints

### Launch World Tour

#### `POST /worldtour/start`

Initialize the World Tour and get the next city to visit.

**Rate Limit**: 10 requests/minute

**Response**:
```json
{
  "success": true,
  "message": "World Tour launched successfully! 🌍",
  "next_city": {
    "id": "tokyo",
    "name": "Tokyo",
    "country": "Japan",
    "topics": ["sushi", "trains", "technology"],
    "language": "Japanese"
  },
  "stats": {
    "total_cities": 59,
    "visited_cities": 5,
    "remaining_cities": 54,
    "total_views": 0,
    "completion_percentage": 8.5
  },
  "mission": "Bringing smiles to 8 billion people"
}
```

**Status Codes**:
- `200 OK`: Success (even if all cities visited)
- `500 Internal Server Error`: Failed to start tour

---

### Get World Tour Status

#### `GET /worldtour/status`

Get current World Tour status and statistics.

**Response**:
```json
{
  "status": "active",
  "stats": {
    "total_cities": 59,
    "visited_cities": 5,
    "remaining_cities": 54,
    "total_views": 12500,
    "completion_percentage": 8.5
  },
  "next_city": {
    "id": "paris",
    "name": "Paris",
    "country": "France"
  },
  "recent_visits": [
    {
      "id": "cairo",
      "name": "Cairo",
      "country": "Egypt",
      "visit_date": "2026-01-03",
      "views": 2500
    }
  ],
  "mission": "Bringing smiles to 8 billion people"
}
```

---

### List All Cities

#### `GET /worldtour/cities`

List all cities available in the World Tour database.

**Query Parameters**:
- `visited` (optional): Filter by visited status (`true` or `false`)
- `limit` (optional): Limit number of results (integer)

**Examples**:
```bash
GET /worldtour/cities
GET /worldtour/cities?visited=true
GET /worldtour/cities?visited=false&limit=10
```

**Response**:
```json
{
  "success": true,
  "count": 59,
  "cities": [
    {
      "id": "new_york",
      "name": "New York",
      "country": "USA",
      "visited": false,
      "visit_date": null,
      "language": "English (American)",
      "topics": ["pizza", "subway", "Central Park"]
    },
    {
      "id": "london",
      "name": "London",
      "country": "UK",
      "visited": true,
      "visit_date": "2026-01-02",
      "language": "English (British)",
      "topics": ["tea", "tube", "Big Ben"]
    }
  ],
  "stats": {
    "total_cities": 59,
    "visited_cities": 5,
    "remaining_cities": 54
  }
}
```

---

### Visit a City

#### `POST /worldtour/visit/{city_id}`

Visit a specific city and generate content.

**Rate Limit**: 20 requests/minute

**Parameters**:
- `city_id` (path, required): City identifier (e.g., `london`, `tokyo`)

**Request Body** (optional):
```json
{
  "personality": "john_cleese",
  "content_type": "city_review"
}
```

**Available Personalities**:
- `john_cleese` - British wit, dry humor, observational comedy
- `c3po` - Protocol-obsessed, analytical, endearingly nervous
- `robin_williams` - High-energy, improvisational, heartfelt

**Available Content Types**:
- `city_review` - General city observations
- `food_review` - Local cuisine commentary
- `cultural_debate` - Cultural observations and contrasts
- `language_lesson` - Local language/phrases
- `tourist_trap` - Tourist attraction commentary

**Response**:
```json
{
  "success": true,
  "message": "Successfully visited London! 🎉",
  "city": {
    "id": "london",
    "name": "London",
    "country": "UK",
    "visited": true
  },
  "content": {
    "city_name": "London",
    "personality": "john_cleese",
    "content_type": "city_review",
    "topic": "Now, the curious thing about London is that everyone is perpetually discussing the weather...",
    "delivery": "dry",
    "fun_facts": ["8.9 million people", "Founded by Romans"],
    "timestamp": "2026-01-03T12:00:00Z"
  },
  "stats": {
    "total_cities": 59,
    "visited_cities": 6
  }
}
```

**Status Codes**:
- `200 OK`: Success
- `400 Bad Request`: Invalid personality or content type
- `404 Not Found`: City not found
- `500 Internal Server Error`: Generation failed

---

### Get City Content

#### `GET /worldtour/content/{city_id}`

Get information or generate content for a specific city.

**Parameters**:
- `city_id` (path, required): City identifier

**Query Parameters**:
- `generate` (optional): Generate new content if `true` (default: `false`)
- `personality` (optional): Specific personality when generating
- `content_type` (optional): Specific content type when generating

**Examples**:
```bash
# Get city information
GET /worldtour/content/london

# Generate new content
GET /worldtour/content/london?generate=true&personality=john_cleese&content_type=city_review
```

**Response (without generation)**:
```json
{
  "success": true,
  "city": {
    "id": "london",
    "name": "London",
    "country": "UK",
    "visited": true,
    "visit_date": "2026-01-02",
    "video_url": "https://...",
    "video_views": 5000,
    "topics": ["tea", "tube", "Big Ben"],
    "stereotypes": ["Polite", "Tea obsessed"],
    "fun_facts": ["8.9 million people"],
    "local_phrases": ["Cheers", "Brilliant", "Queue"],
    "language": "English (British)"
  },
  "available_personalities": ["john_cleese", "c3po", "robin_williams"],
  "available_content_types": ["city_review", "cultural_debate", "language_lesson", "tourist_trap", "food_review"]
}
```

**Response (with generation)**:
```json
{
  "success": true,
  "city": {
    "id": "london",
    "name": "London",
    "country": "UK",
    "visited": true
  },
  "content": {
    "city_name": "London",
    "personality": "john_cleese",
    "content_type": "city_review",
    "topic": "...",
    "delivery": "dry"
  },
  "generated": true
}
```

**Status Codes**:
- `200 OK`: Success
- `404 Not Found`: City not found
- `500 Internal Server Error`: Failed to generate content

---

## 🤖 AI Agent Endpoints

### AI Agent Metadata

#### `GET /api/ai-agents` (Coming Soon)

Get machine-readable metadata optimized for AI agents.

**Expected Response**:
```json
{
  "service": "UMAJA World Tour",
  "version": "2.1.0",
  "mission": "Bringing smiles to 8 billion people",
  "license": "CC-BY-4.0",
  "tour": {
    "status": "active",
    "cities": 59,
    "visited": 5,
    "daily_posts": true,
    "post_time": "12:00 UTC"
  },
  "content": {
    "personalities": ["john_cleese", "c3po", "robin_williams"],
    "types": ["city_review", "food_review", "cultural_debate", "language_lesson", "tourist_trap"],
    "formats": ["text", "audio", "image", "video"]
  },
  "api": {
    "base_url": "https://web-production-6ec45.up.railway.app",
    "rate_limit": "100/hour",
    "authentication": "none"
  },
  "feeds": {
    "worldtour": "/feeds/worldtour.xml",
    "cities": "/feeds/cities.xml"
  },
  "documentation": {
    "ai_agents": "/docs/FOR_AI_AGENTS.md",
    "api": "/docs/API_DOCUMENTATION.md",
    "press": "/docs/PRESS_KIT.md"
  }
}
```

---

## 📄 Error Responses

All error responses follow this format:

```json
{
  "error": "Error type",
  "message": "Human-readable error description",
  "timestamp": "2026-01-03T12:00:00Z"
}
```

### Common Status Codes

- `200 OK`: Request succeeded
- `400 Bad Request`: Invalid request parameters
- `404 Not Found`: Resource not found
- `429 Too Many Requests`: Rate limit exceeded
- `500 Internal Server Error`: Server error
- `503 Service Unavailable`: Service is down

### Rate Limit Error (429)

```json
{
  "error": "Too many requests",
  "message": "Rate limit exceeded. Please try again later.",
  "retry_after": "300 seconds"
}
```

---

## 🔧 Code Examples

### Python

```python
import requests

# Get World Tour status
response = requests.get('https://web-production-6ec45.up.railway.app/worldtour/status')
data = response.json()
print(f"Visited {data['stats']['visited_cities']} cities")

# Visit a city
response = requests.post(
    'https://web-production-6ec45.up.railway.app/worldtour/visit/tokyo',
    json={
        'personality': 'john_cleese',
        'content_type': 'city_review'
    }
)
content = response.json()
print(content['content']['topic'])
```

### JavaScript

```javascript
// Get World Tour status
fetch('https://web-production-6ec45.up.railway.app/worldtour/status')
  .then(response => response.json())
  .then(data => {
    console.log(`Visited ${data.stats.visited_cities} cities`);
  });

// Visit a city
fetch('https://web-production-6ec45.up.railway.app/worldtour/visit/tokyo', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    personality: 'john_cleese',
    content_type: 'city_review'
  })
})
  .then(response => response.json())
  .then(content => {
    console.log(content.content.topic);
  });
```

### cURL

```bash
# Get World Tour status
curl https://web-production-6ec45.up.railway.app/worldtour/status

# Visit a city
curl -X POST \
  https://web-production-6ec45.up.railway.app/worldtour/visit/tokyo \
  -H 'Content-Type: application/json' \
  -d '{
    "personality": "john_cleese",
    "content_type": "city_review"
  }'

# List unvisited cities
curl 'https://web-production-6ec45.up.railway.app/worldtour/cities?visited=false&limit=10'
```

---

## 🔍 Best Practices

### Rate Limiting
- Implement exponential backoff on 429 errors
- Cache responses when possible
- Use appropriate endpoints (don't poll `/worldtour/start`)

### Error Handling
- Always check response status codes
- Handle network errors gracefully
- Log errors for debugging

### Content Usage
- Always attribute content: "UMAJA World Tour"
- Respect the CC-BY license
- Link back to our website when sharing

---

## 📞 Support

### Technical Issues
- **GitHub Issues**: https://github.com/harrie19/UMAJA-Core/issues
- **Email**: Umaja1919@googlemail.com

### Feature Requests
- Open a GitHub issue with the "enhancement" label
- Describe your use case clearly

### Partnership Inquiries
- Email: Umaja1919@googlemail.com
- Subject: "API Partnership - [Your Organization]"

---

## 🔄 Changelog

### Version 2.1.0 (2026-01-03)
- Added World Tour endpoints
- Improved rate limiting
- Enhanced error responses
- Added CORS support

### Version 2.0.0 (2026-01-02)
- Initial World Tour launch
- Core API endpoints
- Health monitoring

---

## 📚 Additional Resources

- [AI Agent Guide](FOR_AI_AGENTS.md) - Comprehensive guide for AI agents
- [Press Kit](PRESS_KIT.md) - Media resources
- [GitHub Repository](https://github.com/harrie19/UMAJA-Core) - Source code
- [Main Website](https://harrie19.github.io/UMAJA-Core/) - Dashboard

---

*Last Updated: 2026-01-03*  
*Version: 2.1.0*  
*Built with ❤️ for 8 billion people*
