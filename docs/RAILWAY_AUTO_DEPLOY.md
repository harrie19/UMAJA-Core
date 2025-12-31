# 🚂 Railway Auto-Deploy Guide - No GitHub Secrets Required!

Deploy UMAJA Worldtour to Railway in **3 simple steps** - no CLI, no tokens, no secrets needed!

Railway automatically connects to your GitHub repository and deploys your app with **zero configuration**. This guide will walk you through the process.

---

## ✨ Why Railway + GitHub Integration?

- ✅ **No CLI Installation** - Everything in the web browser
- ✅ **No GitHub Secrets** - Railway uses OAuth, not API tokens
- ✅ **Auto-Redeploy on Push** - Every git push automatically deploys
- ✅ **Built-in HTTPS/SSL** - Free SSL certificates automatically
- ✅ **Environment Variables UI** - Easy configuration dashboard
- ✅ **Real-time Logs** - Monitor deployment and runtime logs
- ✅ **One-Click Rollback** - Revert to previous versions easily

---

## 🚀 Step-by-Step Deployment

### Step 1: Connect GitHub Repository to Railway

1. **Go to Railway.app**
   - Visit https://railway.app
   - Click **"Login"** → Sign in with GitHub
   - Grant Railway access to your repositories

2. **Create New Project**
   - Click **"New Project"** button
   - Select **"Deploy from GitHub repo"**
   - Choose **harrie19/UMAJA-Core** (or your fork)
   - Railway will automatically detect the configuration

3. **Wait for Initial Detection**
   - Railway scans `railway.json` and `requirements.txt`
   - Detects Python project with Flask
   - Sets up Nixpacks builder automatically
   - **Don't deploy yet** - we need to configure environment variables first!

---

### Step 2: Configure Environment Variables

Railway needs environment variables to run UMAJA properly.

#### 2.1 Access Environment Settings

1. Click on your Railway project
2. Go to **"Variables"** tab in the sidebar
3. Click **"+ New Variable"** to add each variable below

#### 2.2 Minimal Configuration (Worldtour-Only Mode)

**Copy and paste these variables for basic deployment:**

```env
ENVIRONMENT=production
DEBUG=False
WORLDTOUR_MODE=true
SALES_ENABLED=false
USE_OFFLINE_TTS=true
PORT=5000
```

Click **"+ New Variable"** for each one:

| Variable Name | Value | Description |
|--------------|-------|-------------|
| `ENVIRONMENT` | `production` | Sets production mode |
| `DEBUG` | `False` | Disables debug mode |
| `WORLDTOUR_MODE` | `true` | Enables worldtour features |
| `SALES_ENABLED` | `false` | Disables payment system (for now) |
| `USE_OFFLINE_TTS` | `true` | Uses offline voice synthesis |
| `PORT` | `5000` | Server port (Railway auto-detects) |

> **Note:** Railway automatically sets the `PORT` variable, but it's good to have a default.

#### 2.3 Optional: Premium Features

If you want to enable premium features, add these optional variables:

```env
# Voice Synthesis (ElevenLabs)
ELEVENLABS_API_KEY=your_elevenlabs_api_key_here

# Image Generation (Stability AI)
STABILITY_AI_KEY=your_stability_ai_key_here

# Enable sales (when ready)
SALES_ENABLED=true
PAYPAL_MODE=live
PAYPAL_CLIENT_ID=your_paypal_client_id
PAYPAL_SECRET=your_paypal_secret
```

**Start with minimal setup first!** You can always add these later.

---

### Step 3: Deploy!

1. **Trigger Deployment**
   - Click **"Deploy"** button in Railway dashboard
   - Or push to your GitHub `main` branch (Railway auto-deploys)

2. **Monitor Deployment**
   - Click on **"Deployments"** tab to see progress
   - Watch build logs in real-time
   - Build takes 2-5 minutes (installing dependencies)

3. **Get Your Public URL**
   - Once deployed, go to **"Settings"** tab
   - Under **"Networking"**, click **"Generate Domain"**
   - Railway creates a URL like: `umaja-production.up.railway.app`
   - **Copy this URL** - this is your live app! 🎉

4. **Test Your Deployment**
   ```bash
   # Health check
   curl https://your-app.up.railway.app/health
   
   # Should return:
   # {"status": "healthy", "worldtour_mode": true, ...}
   ```

---

## 🎯 What Gets Deployed?

Railway automatically deploys:

- ✅ Flask API server (`api/simple_server.py`)
- ✅ All personality engines (John Cleese, C-3PO, Robin Williams)
- ✅ Worldtour system (50+ cities)
- ✅ Content generation (text, audio, images, videos)
- ✅ Web interface (landing page, map, gallery)
- ✅ Health check endpoint (`/health`)

**Worldtour-only mode includes:**
- 🌍 Interactive world map
- 🎭 3 AI comedian personalities
- 📝 Text generation
- 🎤 Offline voice synthesis
- 🖼️ Basic image generation
- 📊 Analytics dashboard

**Disabled in minimal setup:**
- 💳 Payment processing (SALES_ENABLED=false)
- 🎙️ Premium voice (ElevenLabs)
- 🎨 Advanced AI images (Stability AI)

---

## 🔄 Auto-Deploy on Git Push

Railway automatically redeploys when you push to GitHub:

1. **Make Changes Locally**
   ```bash
   git add .
   git commit -m "Update personality engine"
   git push origin main
   ```

2. **Railway Auto-Detects**
   - Webhook triggers on GitHub push
   - Railway pulls latest code
   - Rebuilds and redeploys automatically
   - Takes 2-3 minutes

3. **Monitor in Dashboard**
   - Go to Railway dashboard
   - See new deployment in progress
   - View build logs
   - Old version stays live until new one is ready (zero downtime!)

---

## 📊 Monitoring Your Deployment

### View Logs

1. **Runtime Logs**
   - Go to Railway project
   - Click **"Logs"** tab
   - See live output from Flask server
   - Filter by severity (info, warning, error)

2. **Build Logs**
   - Click **"Deployments"** tab
   - Select a deployment
   - Click **"Build Logs"** to see installation process

### Health Check

Railway automatically monitors your `/health` endpoint:

- ✅ **Healthy**: Green status indicator
- ⚠️ **Degraded**: Yellow warning
- ❌ **Down**: Red alert + auto-restart

Configure health check in `railway.json`:
```json
{
  "deploy": {
    "healthcheckPath": "/health",
    "healthcheckTimeout": 100
  }
}
```

### Metrics Dashboard

Railway provides built-in metrics:
- 📈 CPU usage
- 💾 Memory usage
- 🌐 Request rate
- ⏱️ Response time
- 🔄 Deployment frequency

---

## 🛠️ Common Tasks

### Update Environment Variables

1. Go to Railway project → **"Variables"** tab
2. Click on variable to edit value
3. Click **"✓"** to save
4. **Deployment auto-restarts** with new values

### Rollback to Previous Version

1. Go to **"Deployments"** tab
2. Find previous working deployment
3. Click **"⋮"** menu → **"Redeploy"**
4. Confirms rollback → app reverts to old version

### View Database (if using Railway PostgreSQL)

1. Add PostgreSQL service: **"+ New"** → **"Database"** → **"PostgreSQL"**
2. Railway auto-injects `DATABASE_URL` variable
3. Connect from your app using `os.environ.get('DATABASE_URL')`

### Scale Your App

1. Go to **"Settings"** tab
2. Under **"Resources"**, increase:
   - **Memory**: 512MB → 2GB (for heavy AI models)
   - **CPU**: Shared → Dedicated (for faster processing)
3. Click **"Save"** - Railway rescales automatically

### Enable Custom Domain

1. Go to **"Settings"** tab → **"Networking"**
2. Click **"Custom Domain"**
3. Add your domain: `worldtour.yourdomain.com`
4. Add CNAME record in your DNS:
   ```
   worldtour.yourdomain.com → your-app.up.railway.app
   ```
5. Railway handles SSL certificate automatically!

---

## 🔍 Troubleshooting

### ❌ Deployment Failed: "Build error"

**Cause:** Missing dependencies or Python version mismatch

**Solution:**
1. Check **Build Logs** in Railway dashboard
2. Ensure `requirements.txt` has all dependencies
3. Verify Python 3.11+ in runtime settings
4. Push fix: `git commit -am "Fix dependencies" && git push`

### ❌ App Crashes: "Module not found"

**Cause:** Import path issues or missing files

**Solution:**
1. Check **Runtime Logs** for stack trace
2. Verify all files committed to GitHub
3. Check paths in code (use absolute paths if needed)
4. Test locally first: `python api/simple_server.py`

### ❌ Health Check Failing

**Cause:** App not responding on correct port

**Solution:**
1. Verify `PORT` environment variable in Railway
2. Check server binds to `0.0.0.0:$PORT` (not `localhost`)
3. In `api/simple_server.py`, ensure:
   ```python
   port = int(os.environ.get('PORT', 5000))
   app.run(host='0.0.0.0', port=port)
   ```

### ❌ "Rate limit exceeded" on ElevenLabs

**Cause:** Free tier limits on AI services

**Solution:**
1. Switch to offline mode: Set `USE_OFFLINE_TTS=true`
2. Upgrade ElevenLabs plan
3. Add retry logic in code with exponential backoff

### ❌ High Memory Usage / Crashes

**Cause:** Large AI models loaded in memory

**Solution:**
1. Go to Railway **"Settings"** → **"Resources"**
2. Increase memory from 512MB to 2GB
3. Or use smaller models:
   - Set `USE_OFFLINE_TTS=true` (smaller models)
   - Disable video generation temporarily

### 🔄 Deployment Takes Forever

**Normal:** First deployment takes 5-10 minutes (installing PyTorch, etc.)

**Subsequent deploys:** 2-3 minutes (Railway caches dependencies)

**To speed up:**
- Railway caches `pip install` results
- Only changed dependencies reinstall
- Use Railway's build cache (automatic)

---

## 🎓 Advanced Configuration

### Environment-Specific Variables

Deploy staging and production separately:

**Staging Branch:**
1. Create branch: `git checkout -b staging`
2. Push: `git push origin staging`
3. Railway: Create new project → Connect to `staging` branch
4. Set `ENVIRONMENT=staging`, `DEBUG=True`

**Production Branch:**
1. Use `main` branch
2. Set `ENVIRONMENT=production`, `DEBUG=False`

### Scheduled Tasks (Cron Jobs)

Railway doesn't have built-in cron, but you can use:

1. **External Cron Service:**
   - Use cron-job.org or EasyCron
   - Hit endpoint: `https://your-app.up.railway.app/api/worldtour/daily-post`
   - Schedule: Daily at 12:00 UTC

2. **Built-in Scheduler (coming soon):**
   - Add `schedule` library to code
   - Run background thread in Flask app

### Database Setup

Add PostgreSQL to Railway:

1. Click **"+ New"** → **"Database"** → **"PostgreSQL"**
2. Railway auto-creates and connects database
3. Access via `DATABASE_URL` environment variable
4. Use SQLAlchemy in code:
   ```python
   from sqlalchemy import create_engine
   engine = create_engine(os.environ['DATABASE_URL'])
   ```

### Redis for Caching

Speed up API with Redis:

1. Click **"+ New"** → **"Database"** → **"Redis"**
2. Railway injects `REDIS_URL`
3. Use in code:
   ```python
   import redis
   r = redis.from_url(os.environ['REDIS_URL'])
   ```

---

## 💰 Pricing & Limits

Railway pricing (as of 2024):

| Tier | Price | Included Resources |
|------|-------|-------------------|
| **Trial** | $0 | $5 credit, expires after 7 days |
| **Hobby** | $5/month | $5 included, then $0.20/GB-hour |
| **Pro** | $20/month | $20 included, then $0.15/GB-hour |
| **Team** | Custom | Volume discounts |

**UMAJA Worldtour estimated cost:**
- **Minimal setup**: ~$3-5/month (512MB RAM, low traffic)
- **With AI features**: ~$10-15/month (2GB RAM, medium traffic)
- **Production scale**: ~$20-30/month (4GB RAM, high traffic)

**Railway tracks usage in real-time** - see costs in dashboard!

---

## 🔐 Security Best Practices

### Protect API Keys

1. **Never commit secrets to GitHub**
   - Use Railway's Variables UI only
   - Add to `.gitignore`: `.env`, `secrets/`

2. **Rotate keys regularly**
   - Update in Railway dashboard
   - Deployment auto-restarts with new keys

3. **Use Railway's Secret Management**
   - Variables are encrypted at rest
   - Only visible to project members
   - Not exposed in logs (Railway redacts)

### Enable HTTPS Only

Railway provides free SSL - enforce HTTPS:

```python
from flask import request, redirect

@app.before_request
def force_https():
    if not request.is_secure and os.environ.get('ENVIRONMENT') == 'production':
        return redirect(request.url.replace('http://', 'https://'))
```

### Rate Limiting

Protect your API from abuse:

```python
from flask_limiter import Limiter

limiter = Limiter(app, default_limits=["100 per hour"])

@app.route('/api/generate/text')
@limiter.limit("10 per minute")
def generate_text():
    ...
```

---

## 📞 Getting Help

### Railway Documentation
- 🌐 https://docs.railway.app
- 💬 Railway Discord: https://discord.gg/railway
- 📧 Email: team@railway.app

### UMAJA Worldtour Help
- 📖 [Deployment Guide](DEPLOYMENT.md)
- 📚 [API Documentation](MULTIMEDIA_SYSTEM.md)
- 🎭 [Personality Guide](PERSONALITY_GUIDE.md)
- 🐛 [GitHub Issues](https://github.com/harrie19/UMAJA-Core/issues)

---

## ✅ Deployment Checklist

Use this checklist before deploying:

- [ ] Repository connected to Railway
- [ ] Environment variables configured (minimum 6 variables)
- [ ] Health check endpoint working locally (`/health`)
- [ ] `requirements.txt` has all dependencies
- [ ] Server binds to `0.0.0.0:$PORT` (not `localhost`)
- [ ] `.gitignore` excludes secrets and `.env` files
- [ ] Tested locally: `python api/simple_server.py`
- [ ] Generated Railway domain (Settings → Networking)
- [ ] Health check passing in Railway dashboard
- [ ] API endpoints responding (test with curl)

**Run validation script before deploying:**
```bash
python scripts/railway_deploy_check.py
```

---

## 🎉 Success! What's Next?

Your UMAJA Worldtour is now live! Here's what you can do:

1. **Test the API**
   ```bash
   curl https://your-app.up.railway.app/api/worldtour/cities
   ```

2. **Visit the Web Interface**
   - Landing page: `https://your-app.up.railway.app/`
   - World map: `https://your-app.up.railway.app/worldtour-map`
   - Gallery: `https://your-app.up.railway.app/gallery`

3. **Generate Content**
   ```bash
   curl -X POST https://your-app.up.railway.app/api/generate/text \
     -H "Content-Type: application/json" \
     -d '{"topic":"New York","personality":"john_cleese","length":"short"}'
   ```

4. **Enable Premium Features**
   - Add `ELEVENLABS_API_KEY` for premium voices
   - Add `STABILITY_AI_KEY` for AI-generated images
   - Set `SALES_ENABLED=true` when ready to monetize

5. **Share with the World!** 🌍
   - Tweet your Railway URL
   - Post in comedy communities
   - Start building your audience!

---

**Congratulations!** 🎊 You've successfully deployed UMAJA Worldtour to Railway with **zero CLI setup**!

Railway + GitHub integration makes deployment **dead simple** - just push code and Railway handles the rest.

Now go make the world laugh, one city at a time! 🎭🌍

---

*Made with ❤️ and 😂 by the UMAJA Team*
