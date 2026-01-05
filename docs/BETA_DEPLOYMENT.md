# UMAJA Beta System - Deployment Guide

## Overview

The UMAJA Beta system provides a complete analytics and user management platform for beta testers. It runs alongside the existing World Tour system.

## Architecture

```
UMAJA-Core/
├── api/
│   ├── simple_server.py    # Original World Tour API
│   └── beta_server.py       # Beta System API (NEW)
├── src/
│   ├── beta_tracker.py      # Analytics tracking
│   ├── freemium_model.py    # Pricing logic
│   └── personality_engine.py # Content generation
├── templates/
│   ├── beta_landing.html    # Beta landing page
│   └── dashboard.html       # User dashboard
└── static/
    └── css/
        └── unified.css      # Unified styling
```

## Deployment Options

### Option 1: Beta Server Only (Recommended for Beta Launch)

Update `wsgi.py` to use beta_server:

```python
from api.beta_server import app
```

Then deploy as usual:
```bash
gunicorn --bind 0.0.0.0:$PORT wsgi:app
```

### Option 2: Dual Deployment

Run both servers on different ports:

**World Tour (Port 5000):**
```bash
gunicorn --bind 0.0.0.0:5000 wsgi:app
```

**Beta System (Port 5001):**
```bash
gunicorn --bind 0.0.0.0:5001 api.beta_server:app
```

### Option 3: Environment-Based Selection

Modify `wsgi.py`:

```python
import os

if os.environ.get('BETA_MODE', 'false').lower() == 'true':
    from api.beta_server import app
else:
    from api.simple_server import app

application = app
```

Then set environment variable:
```bash
export BETA_MODE=true
gunicorn --bind 0.0.0.0:$PORT wsgi:app
```

## Railway Deployment

### Current Configuration (railway.json)

The existing configuration works for both servers:

```json
{
  "deploy": {
    "startCommand": "gunicorn --bind 0.0.0.0:$PORT wsgi:app"
  }
}
```

### For Beta Launch

1. **Update wsgi.py** to import beta_server
2. **Set environment variable** `BETA_MODE=true` in Railway dashboard
3. **Deploy** - Railway will automatically rebuild

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `PORT` | 5000 | Server port |
| `BETA_MODE` | false | Use beta_server when true |
| `DEBUG` | false | Debug mode |
| `SECRET_KEY` | auto | Flask session secret |

## Testing Locally

### Start Beta Server

```bash
cd /path/to/UMAJA-Core
python api/beta_server.py
```

Visit: http://localhost:5000

### Start World Tour Server

```bash
cd /path/to/UMAJA-Core
python api/simple_server.py
```

Visit: http://localhost:5000

## Key Endpoints

### Beta System (`api/beta_server.py`)

- `GET /` - Beta landing page
- `POST /api/beta/consent` - Record user consent
- `GET /app` - User dashboard (requires session)
- `POST /api/generate` - Generate content
- `POST /api/feedback` - Submit feedback
- `GET /api/analytics/insights` - View analytics
- `GET /health` - Health check

### World Tour (`api/simple_server.py`)

- `GET /health` - Health check
- `GET /api/daily-smile` - Get daily smile
- `POST /worldtour/start` - Start world tour
- `GET /worldtour/status` - Tour status
- (All existing endpoints remain unchanged)

## Data Storage

Beta analytics data is stored in:
```
data/beta_analytics/
├── sessions.jsonl      # Anonymous sessions
├── interactions.jsonl  # User interactions
├── feedback.jsonl      # User feedback
└── consent.jsonl       # Consent records
```

**Note:** This directory is in `.gitignore` to protect user privacy.

## Privacy & GDPR Compliance

✅ No personal data collected  
✅ Anonymous session IDs only  
✅ User can request data deletion  
✅ Full transparency  
✅ Explicit consent required

## Monitoring

Check analytics insights:
```bash
curl http://localhost:5000/api/analytics/insights
```

## Rollback Plan

If beta system has issues, simply:

1. Change `wsgi.py` back to `from api.simple_server import app`
2. Redeploy
3. World Tour continues unaffected

## Support

- **Email:** Umaja1919@googlemail.com
- **GitHub:** https://github.com/harrie19/UMAJA-Core/issues

---

**Built with love for 8 billion people 🌍**
