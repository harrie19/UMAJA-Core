# 🚀 UMAJA WORLDTOUR Deployment Guide

Complete guide for deploying the UMAJA system to production.

## Table of Contents

- [Quick Start](#quick-start)
- [Local Development](#local-development)
- [Railway Deployment](#railway-deployment)
- [Heroku Deployment](#heroku-deployment)
- [Environment Configuration](#environment-configuration)
- [Database Setup](#database-setup)
- [Monitoring](#monitoring)

---

## Quick Start

### Prerequisites

- Python 3.11+
- Git
- 2GB+ RAM
- 10GB+ disk space

### Local Setup (5 minutes)

```bash
# Clone repository
git clone https://github.com/harrie19/UMAJA-Core.git
cd UMAJA-Core

# Run setup
python scripts/setup_multimedia.py --quick

# Start server
python api/simple_server.py
```

Visit http://localhost:5000

---

## Local Development

### Full Setup (with demos)

```bash
# Install dependencies
pip install -r requirements.txt

# Setup (includes demo generation)
python scripts/setup_multimedia.py

# Configure environment
cp .env.example .env
# Edit .env with your API keys

# Run server
python api/simple_server.py
```

### Development Server

```bash
# With auto-reload
python api/simple_server.py

# Custom port
PORT=8000 python api/simple_server.py

# Debug mode
DEBUG=true python api/simple_server.py
```

### Testing

```bash
# Test core modules
python -m pytest tests/ -v

# Test specific module
python -c "from src.personality_engine import PersonalityEngine; print('OK')"

# Generate test content
curl -X POST http://localhost:5000/api/generate/text \
  -H "Content-Type: application/json" \
  -d '{"topic":"pizza","personality":"john_cleese","length":"short"}'
```

---

## Railway Deployment

Railway.app offers the easiest deployment with automatic HTTPS and scaling.

### Steps

1. **Create Railway Account**
   - Go to https://railway.app
   - Sign up with GitHub

2. **Deploy from GitHub**
   ```bash
   # Install Railway CLI
   npm install -g @railway/cli
   
   # Login
   railway login
   
   # Initialize project
   railway init
   
   # Link to GitHub repo
   railway link
   
   # Deploy
   railway up
   ```

3. **Configure Environment**
   - Go to Railway dashboard
   - Click on your project
   - Go to Variables tab
   - Add environment variables from `.env.example`

4. **Set Custom Domain (Optional)**
   - Go to Settings
   - Add custom domain
   - Update DNS records

### Railway Configuration

The `railway.json` file is already configured:

```json
{
  "$schema": "https://railway.app/railway.schema.json",
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "startCommand": "python api/simple_server.py",
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 10
  }
}
```

### Railway Environment Variables

Required:
```
ENVIRONMENT=production
DEBUG=False
PORT=5000
```

Optional (for full features):
```
ELEVENLABS_API_KEY=your_key
STABILITY_AI_KEY=your_key
USE_LOCAL_STABLE_DIFFUSION=false
```

### Railway Monitoring

- View logs: `railway logs`
- Check status: Railway dashboard
- Metrics: Built-in Railway monitoring

---

## Heroku Deployment

### Steps

1. **Install Heroku CLI**
   ```bash
   # macOS
   brew tap heroku/brew && brew install heroku
   
   # Other: https://devcenter.heroku.com/articles/heroku-cli
   ```

2. **Login and Create App**
   ```bash
   heroku login
   heroku create umaja-worldtour
   ```

3. **Configure Buildpacks**
   ```bash
   heroku buildpacks:add --index 1 heroku/python
   ```

4. **Set Environment Variables**
   ```bash
   heroku config:set ENVIRONMENT=production
   heroku config:set DEBUG=False
   heroku config:set SALES_ENABLED=true
   
   # Optional API keys
   heroku config:set ELEVENLABS_API_KEY=your_key
   ```

5. **Deploy**
   ```bash
   git push heroku main
   ```

6. **Open App**
   ```bash
   heroku open
   ```

### Heroku Configuration

The `Procfile` is already configured:

```
web: python api/simple_server.py
```

### Heroku Add-ons (Optional)

```bash
# PostgreSQL (if needed later)
heroku addons:create heroku-postgresql:hobby-dev

# Redis (for caching)
heroku addons:create heroku-redis:hobby-dev

# Papertrail (logging)
heroku addons:create papertrail:choklad
```

### Heroku Monitoring

```bash
# View logs
heroku logs --tail

# Check status
heroku ps

# Scale dynos
heroku ps:scale web=2
```

---

## Environment Configuration

### Required Variables

```env
# Application
ENVIRONMENT=production  # or development
DEBUG=False
LOG_LEVEL=INFO
PORT=5000
```

### Optional Voice Synthesis

```env
# ElevenLabs (premium quality)
ELEVENLABS_API_KEY=your_key_here

# Google TTS (good quality, requires API key)
GOOGLE_TTS_API_KEY=your_key_here

# Offline TTS (basic quality, no API needed)
USE_OFFLINE_TTS=true
```

### Optional Image Generation

```env
# Stability AI (cloud)
STABILITY_AI_KEY=your_key_here

# Local Stable Diffusion (requires GPU)
USE_LOCAL_STABLE_DIFFUSION=false
```

### Worldtour Settings

```env
WORLDTOUR_MODE=true
DAILY_POST_TIME=12:00
AUTO_POST_ENABLED=false  # Set true for automation
CITIES_PER_WEEK=7
```

### Monetization

```env
SALES_ENABLED=true
LAUNCH_DATE=2026-03-31
EARLY_ACCESS_ENABLED=true
EARLY_ACCESS_SLOTS=100
```

### Social Media (for auto-posting)

```env
TIKTOK_USERNAME=your_username
TIKTOK_PASSWORD=your_password
YOUTUBE_API_KEY=your_key
INSTAGRAM_USERNAME=your_username
INSTAGRAM_PASSWORD=your_password
```

---

## Database Setup

Currently using JSON file storage. For production scale, consider:

### SQLite (Built-in, no setup)

Already works out of the box for development.

### PostgreSQL (Recommended for production)

```python
# In future version:
# pip install psycopg2-binary
# Update multimedia_text_seller.py to use PostgreSQL
```

### Redis (Optional, for caching)

```python
# For caching generated content
# pip install redis
```

---

## SSL/HTTPS

### Railway
- Automatic SSL certificates
- HTTPS enabled by default

### Heroku
- Automatic SSL certificates
- HTTPS enabled by default

### Custom Server
```bash
# Using Certbot (Let's Encrypt)
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d yourdomain.com
```

---

## Scaling

### Horizontal Scaling

**Railway:**
```bash
# Scale via dashboard or CLI
railway scale --replicas 3
```

**Heroku:**
```bash
# Scale dynos
heroku ps:scale web=3
```

### Vertical Scaling

Upgrade instance size in platform dashboard.

### Caching

Add Redis for caching:
- Generated content
- API responses
- Session data

### CDN

Use CDN for static files:
- Cloudflare
- AWS CloudFront
- Railway CDN (built-in)

---

## Monitoring

### Application Monitoring

**Logs:**
```bash
# Railway
railway logs --tail

# Heroku
heroku logs --tail

# Local
tail -f umaja.log
```

**Health Checks:**
```bash
# Automated health check
curl https://your-app.com/health

# Should return:
# {"status":"healthy","service":"UMAJA Worldtour API","version":"1.0.0"}
```

### Performance Monitoring

**Railway:**
- Built-in metrics dashboard
- CPU, memory, network usage

**Heroku:**
- Heroku Metrics
- New Relic (add-on)
- Datadog (add-on)

**Custom:**
```python
# Add to server.py
from flask import request
import time

@app.before_request
def before_request():
    request.start_time = time.time()

@app.after_request
def after_request(response):
    diff = time.time() - request.start_time
    logger.info(f"Request took {diff:.3f}s")
    return response
```

### Error Tracking

**Sentry Integration:**
```bash
pip install sentry-sdk[flask]
```

```python
# In api/simple_server.py
import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration

sentry_sdk.init(
    dsn="your-sentry-dsn",
    integrations=[FlaskIntegration()]
)
```

---

## Backup & Recovery

### Backup Generated Content

```bash
# Automated daily backup
0 2 * * * tar -czf /backup/umaja-$(date +\%Y\%m\%d).tar.gz /app/static/
```

### Backup Database

```bash
# JSON files
cp data/*.json backup/

# PostgreSQL (when migrated)
pg_dump umaja_db > backup/umaja_db_$(date +%Y%m%d).sql
```

### Recovery

```bash
# Restore files
tar -xzf backup/umaja-20251231.tar.gz

# Restore PostgreSQL
psql umaja_db < backup/umaja_db_20251231.sql
```

---

## Security

### Best Practices

1. **Environment Variables**
   - Never commit `.env` file
   - Use platform's secret management
   - Rotate API keys regularly

2. **HTTPS Only**
   - Force HTTPS in production
   - Set secure cookies
   - HSTS headers

3. **Rate Limiting**
   ```python
   from flask_limiter import Limiter
   
   limiter = Limiter(app, key_func=lambda: request.remote_addr)
   
   @app.route('/api/generate/text')
   @limiter.limit("5 per minute")
   def generate_text():
       ...
   ```

4. **Input Validation**
   - Sanitize all user inputs
   - Validate file uploads
   - Limit request sizes

5. **CORS Configuration**
   ```python
   from flask_cors import CORS
   
   CORS(app, origins=['https://yourdomain.com'])
   ```

---

## Troubleshooting

### Common Issues

**Issue: Module import errors**
```bash
# Solution: Ensure dependencies installed
pip install -r requirements.txt
```

**Issue: Port already in use**
```bash
# Solution: Use different port
PORT=8000 python api/simple_server.py
```

**Issue: TTS not working**
```bash
# Solution: Check TTS backend availability
python -c "from src.voice_synthesizer import VoiceSynthesizer; s = VoiceSynthesizer(); print(s.list_available_backends())"
```

**Issue: Out of memory**
```bash
# Solution: 
# 1. Upgrade instance size
# 2. Disable local Stable Diffusion
# 3. Use external APIs instead
```

**Issue: Slow generation**
```bash
# Solution:
# 1. Enable caching
# 2. Use faster TTS (gTTS)
# 3. Pre-generate common content
```

---

## Performance Optimization

### Tips

1. **Caching**
   - Cache generated content
   - Use Redis for sessions
   - Enable browser caching

2. **Async Processing**
   - Use Celery for background jobs
   - Queue video generation
   - Batch operations

3. **CDN**
   - Serve static files from CDN
   - Cache API responses
   - Optimize images

4. **Database**
   - Index frequently queried fields
   - Use connection pooling
   - Regular maintenance

---

## Support

- Documentation: `/docs` folder
- GitHub Issues: https://github.com/harrie19/UMAJA-Core/issues
- Email: (if applicable)

---

Happy deploying! 🚀
