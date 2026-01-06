# 🎭 UMAJA WORLDTOUR - Multimedia System API Reference

Complete API reference for the UMAJA autonomous multimedia comedy generation system.

## Base URL

- Development: `http://localhost:5000`
- Production: `https://your-deployment.railway.app`

## Table of Contents

- [Authentication](#authentication)
- [Core Endpoints](#core-endpoints)
- [Worldtour Endpoints](#worldtour-endpoints)
- [Content Generation](#content-generation)
- [Purchase & Monetization](#purchase--monetization)
- [Analytics](#analytics)
- [Error Handling](#error-handling)

---

## Authentication

Currently, the API is open for development. In production, rate limiting will be applied:
- Free tier: 5 requests per IP per day
- Paid tier: Unlimited requests

---

## Core Endpoints

### GET /health

Health check endpoint.

**Response:**
```json
{
  "status": "healthy",
  "service": "UMAJA Worldtour API",
  "version": "1.0.0"
}
```

### GET /api/info

Get API capabilities and available features.

**Response:**
```json
{
  "personalities": ["distinguished_wit", "anxious_analyzer", "energetic_improviser"],
  "content_types": ["text", "audio", "image", "video"],
  "product_tiers": ["text_only", "audio_only", "text_audio", ...],
  "tts_backends": {...},
  "worldtour_enabled": true,
  "sales_enabled": false
}
```

---

## Worldtour Endpoints

### GET /api/worldtour/cities

List all cities with statistics.

**Query Parameters:**
- `visited` (boolean, optional): Filter to show only visited cities

**Response:**
```json
{
  "cities": [
    {
      "id": "new_york",
      "name": "New York",
      "country": "USA",
      "topics": ["pizza", "subway", "Central Park"],
      "visited": true,
      "video_views": 50000
    }
  ],
  "stats": {
    "total_cities": 50,
    "visited_cities": 5,
    "remaining_cities": 45,
    "total_views": 150000,
    "completion_percentage": 10.0
  }
}
```

### GET /api/worldtour/next

Get the next unvisited city.

**Response:**
```json
{
  "id": "tokyo",
  "name": "Tokyo",
  "country": "Japan",
  "topics": ["sushi", "trains", "technology"],
  "stereotypes": ["Ultra polite", "Tech-savvy"],
  "fun_facts": ["37 million in metro area"]
}
```

### GET /api/worldtour/queue?days=7

Get upcoming content queue for N days.

**Query Parameters:**
- `days` (integer, default: 7): Number of days to plan ahead

**Response:**
```json
{
  "queue": [
    {
      "date": "2025-12-31T12:00:00",
      "city_id": "tokyo",
      "city_name": "Tokyo",
      "personality": "energetic_improviser",
      "content_type": "city_review",
      "status": "scheduled"
    }
  ],
  "days": 7
}
```

### POST /api/worldtour/vote

Vote for the next city to visit.

**Request Body:**
```json
{
  "city_id": "paris"
}
```

**Response:**
```json
{
  "success": true,
  "city_id": "paris",
  "message": "Vote recorded for Paris"
}
```

---

## Content Generation

### POST /api/generate/text

Generate text content in a comedian's style.

**Request Body:**
```json
{
  "topic": "New York pizza",
  "personality": "distinguished_wit",
  "length": "medium",
  "style_intensity": 0.7
}
```

**Parameters:**
- `topic` (string, required): Topic to write about
- `personality` (string, required): One of: `distinguished_wit`, `anxious_analyzer`, `energetic_improviser`
- `length` (string, optional): `short` (50-100 words), `medium` (150-250), `long` (300-500)
- `style_intensity` (float, optional): 0.0 to 1.0, default 0.7

**Response:**
```json
{
  "text": "Now, the curious thing about New York pizza...",
  "personality": "distinguished_wit",
  "topic": "New York pizza",
  "word_count": 187,
  "style_intensity": 0.7,
  "humor_markers": ["ironic understatement", "deadpan delivery"],
  "voice_description": "Deep, measured, sarcastic"
}
```

### POST /api/generate/audio

Generate audio from text using personality voice.

**Request Body:**
```json
{
  "text": "Now, the curious thing about...",
  "personality": "distinguished_wit",
  "format": "mp3"
}
```

**Response:**
```json
{
  "success": true,
  "audio_path": "static/audio/john_cleese_abc123.mp3",
  "personality": "distinguished_wit",
  "backend": "gtts",
  "duration_estimate": 15.4,
  "file_size": 245632
}
```

### POST /api/generate/image

Generate image content (quote card or AI image).

**Request Body:**
```json
{
  "type": "quote_card",
  "text": "The curious thing about pizza...",
  "personality": "distinguished_wit",
  "author_name": "The Distinguished Wit"
}
```

**Response:**
```json
{
  "success": true,
  "image_path": "static/images/quote_john_cleese_abc123.png",
  "personality": "distinguished_wit",
  "type": "quote_card",
  "size": [1080, 1080],
  "file_size": 532144
}
```

### POST /api/generate/video

Generate video content.

**Request Body:**
```json
{
  "text": "Now, the curious thing...",
  "audio_path": "static/audio/john_cleese_abc123.mp3",
  "personality": "distinguished_wit",
  "background_image": "static/images/quote_john_cleese_abc123.png"
}
```

**Response:**
```json
{
  "success": true,
  "video_path": "static/videos/lyric_john_cleese_abc123.mp4",
  "personality": "distinguished_wit",
  "type": "lyric_video",
  "duration": 15.4,
  "backend": "moviepy",
  "file_size": 1245632,
  "resolution": "1920x1080"
}
```

### POST /api/generate/city-content

Generate city-specific comedy content.

**Request Body:**
```json
{
  "city_id": "new_york",
  "personality": "distinguished_wit",
  "content_type": "city_review"
}
```

**Parameters:**
- `content_type`: One of `city_review`, `cultural_debate`, `language_lesson`, `tourist_trap`, `food_review`

**Response:**
```json
{
  "city_id": "new_york",
  "city_name": "New York",
  "country": "USA",
  "personality": "distinguished_wit",
  "content_type": "city_review",
  "topic": "Now, the curious thing about New York is...",
  "topics": ["pizza", "subway", "Central Park"],
  "stereotypes": ["Always rushing", "Coffee addicts"],
  "fun_facts": ["Never sleeps", "Hot dog carts"]
}
```

---

## Purchase & Monetization

### POST /api/create-multimedia-sale

Create a complete multimedia purchase package.

**Request Body:**
```json
{
  "email": "customer@example.com",
  "topic": "New York pizza",
  "personality": "distinguished_wit",
  "content_types": ["text", "audio", "image"],
  "extras": ["commercial_license"],
  "length": "medium",
  "style_intensity": 0.7
}
```

**Parameters:**
- `email` (string, required): Customer email
- `topic` (string, required): Content topic
- `personality` (string, required): Comedian personality
- `content_types` (array, required): List of content types to generate
- `extras` (array, optional): Extra add-ons
- `length` (string, optional): Content length
- `style_intensity` (float, optional): Style intensity

**Response:**
```json
{
  "success": true,
  "purchase_id": "a1b2c3d4",
  "package_path": "static/purchases/a1b2c3d4.zip",
  "generated_files": {
    "text": {
      "path": "static/purchases/a1b2c3d4/john_cleese_text.txt",
      "word_count": 187
    },
    "audio": {
      "path": "static/purchases/a1b2c3d4/john_cleese_audio.mp3",
      "duration": 15.4
    }
  },
  "pricing": {
    "total": 13.50,
    "discount_amount": 0.50,
    "charity_amount": 5.40,
    "currency": "EUR"
  },
  "errors": [],
  "download_url": "/download/a1b2c3d4.zip"
}
```

### POST /api/bundle/calculate

Calculate bundle pricing with discounts.

**Request Body:**
```json
{
  "items": ["standard_bundle"],
  "personality_count": 1,
  "extras": ["commercial_license", "rush_delivery"],
  "apply_discount": true
}
```

**Response:**
```json
{
  "items": [{"id": "standard_bundle", "name": "Standard Bundle", "base_price": 5.00}],
  "extras": [{"id": "commercial_license", "name": "Commercial License", "price": 10.00}],
  "base_total": 5.00,
  "extras_total": 10.00,
  "subtotal": 15.00,
  "discount_percentage": 0,
  "discount_amount": 0.00,
  "total": 15.00,
  "charity_amount": 6.00,
  "charity_percentage": 40,
  "currency": "EUR"
}
```

### POST /api/bundle/recommend

Get bundle recommendations and upsells.

**Request Body:**
```json
{
  "items": ["text_only"]
}
```

**Response:**
```json
{
  "recommendations": [
    {
      "type": "upgrade",
      "from": "text_only",
      "to": "text_audio",
      "message": "Add audio for just €2 more!",
      "savings": 1.00
    }
  ],
  "popular_bundles": [...]
}
```

### GET /download/:purchase_id

Download purchased content package.

**Response:** ZIP file download

---

## Analytics

### GET /api/analytics/sales

Get sales analytics.

**Response:**
```json
{
  "total_sales": 150,
  "total_revenue": 1245.50,
  "total_charity": 498.20,
  "average_order_value": 8.30,
  "content_type_popularity": {
    "text": 150,
    "audio": 120,
    "image": 90
  },
  "personality_popularity": {
    "distinguished_wit": 60,
    "anxious_analyzer": 45,
    "energetic_improviser": 45
  },
  "currency": "EUR"
}
```

### GET /api/analytics/worldtour

Get worldtour analytics.

**Response:**
```json
{
  "total_cities": 50,
  "visited_cities": 5,
  "remaining_cities": 45,
  "total_views": 150000,
  "completion_percentage": 10.0
}
```

---

## Error Handling

All errors follow this format:

**Error Response:**
```json
{
  "error": "Error message description"
}
```

**HTTP Status Codes:**
- `200` - Success
- `400` - Bad Request (invalid parameters)
- `404` - Not Found
- `500` - Internal Server Error

**Example Error:**
```json
{
  "error": "Unknown personality: invalid_name. Must be one of ['distinguished_wit', 'anxious_analyzer', 'energetic_improviser']"
}
```

---

## Rate Limiting

Production API includes rate limiting:
- Free tier: 5 requests per IP per day
- Authenticated: Based on subscription tier
- Headers included in response:
  - `X-RateLimit-Limit`: Request limit
  - `X-RateLimit-Remaining`: Remaining requests
  - `X-RateLimit-Reset`: Time until reset

---

## Webhooks

*(Coming soon)*

Receive notifications for:
- New purchase created
- Content generation completed
- City visit scheduled

---

## SDK Examples

### Python
```python
import requests

# Generate text
response = requests.post('http://localhost:5000/api/generate/text', json={
    'topic': 'pizza',
    'personality': 'distinguished_wit',
    'length': 'short'
})

result = response.json()
print(result['text'])
```

### JavaScript
```javascript
// Generate text
fetch('http://localhost:5000/api/generate/text', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({
        topic: 'pizza',
        personality: 'distinguished_wit',
        length: 'short'
    })
})
.then(res => res.json())
.then(data => console.log(data.text));
```

### cURL
```bash
# Generate text
curl -X POST http://localhost:5000/api/generate/text \
  -H "Content-Type: application/json" \
  -d '{
    "topic": "pizza",
    "personality": "distinguished_wit",
    "length": "short"
  }'
```

---

## Support

- Documentation: `/docs`
- Issues: GitHub Issues
- Email: support@umaja-worldtour.com (if applicable)

---

Last updated: 2025-12-31
