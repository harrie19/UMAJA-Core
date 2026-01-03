# 🚂 Railway Deployment Guide for UMAJA-Core

## Quick Deploy to Railway

### Prerequisites
- Railway account (sign up at https://railway.app)
- GitHub repository connected
- This repository pushed to GitHub

### Option 1: Deploy via Railway Dashboard (Recommended)

#### Step 1: Create New Project
1. Go to https://railway.app/dashboard
2. Click "New Project"
3. Select "Deploy from GitHub repo"
4. Choose `harrie19/UMAJA-Core`
5. Railway will automatically detect `railway.json`

#### Step 2: Configure Environment Variables
In Railway Dashboard → Variables, add:

```bash
ENVIRONMENT=production
DEBUG=False
PYTHONUNBUFFERED=1
```

**Note:** Railway automatically sets `PORT` - don't override it!

#### Step 3: Deploy
1. Railway will automatically start building
2. Wait for build to complete (2-3 minutes)
3. Railway will assign a URL: `https://[your-project].up.railway.app`
4. Test health endpoint: `https://[your-project].up.railway.app/health`

### Option 2: Deploy via Railway CLI

#### Install Railway CLI
```bash
# macOS/Linux
npm install -g @railway/cli

# Verify installation
railway --version
```

#### Login to Railway
```bash
railway login
```

#### Link to Project
```bash
cd /path/to/UMAJA-Core
railway link
# Select your project or create a new one
```

#### Deploy
```bash
# Deploy from current directory
railway up

# Check deployment status
railway status

# Open deployed app in browser
railway open

# View logs
railway logs
```

### Deployment Configuration

The deployment is configured in `railway.json`:
```json
{
  "$schema": "https://railway.app/railway.schema.json",
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "startCommand": "gunicorn --bind 0.0.0.0:$PORT wsgi:app",
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 10,
    "healthcheckPath": "/health",
    "healthcheckTimeout": 100
  }
}
```

### Environment Variables Reference

| Variable | Value | Required | Description |
|----------|-------|----------|-------------|
| `ENVIRONMENT` | `production` | ✅ Yes | Sets environment mode |
| `DEBUG` | `False` | ✅ Yes | Disables debug mode |
| `PYTHONUNBUFFERED` | `1` | ✅ Yes | Enables real-time logging |
| `PORT` | (auto-set) | ❌ No | Railway assigns automatically |

### Verify Deployment

#### Test Health Endpoint
```bash
curl https://[your-url].up.railway.app/health
```

Expected response:
```json
{
  "status": "healthy",
  "service": "UMAJA-Core",
  "version": "2.1.0",
  "mission": "8 billion smiles",
  "environment": "production"
}
```

#### Test Daily Smile Endpoint
```bash
curl https://[your-url].up.railway.app/api/daily-smile
```

Expected response:
```json
{
  "content": "Did you know that honey never spoils? ...",
  "archetype": "professor",
  "mission": "Serving 8 billion people",
  "principle": "Truth, Unity, Service"
}
```

#### Test World Tour Status
```bash
curl https://[your-url].up.railway.app/worldtour/status
```

Expected response:
```json
{
  "status": "active",
  "stats": {
    "total_cities": 59,
    "visited_cities": 0,
    ...
  }
}
```

### Update Frontend with Backend URL

After deployment, update the frontend if the Railway URL is different:

1. Edit `docs/index.html`
2. Find line: `const BACKEND_URL = 'https://umaja-core-production.up.railway.app';`
3. Replace with your actual Railway URL
4. Commit and push to trigger GitHub Pages update

### Monitoring

#### View Logs
```bash
# Via CLI
railway logs

# Via Dashboard
Go to Railway Dashboard → Your Project → Logs
```

#### Monitor Health
Set up a cron job or monitoring service to check health endpoint:
```bash
*/5 * * * * curl -f https://[your-url].up.railway.app/health || echo "Health check failed"
```

### Troubleshooting

#### Deployment Fails
1. Check Railway build logs
2. Verify `requirements.txt` is correct
3. Ensure Python 3.11+ is available
4. Check `railway.json` syntax

#### Health Check Fails
1. Verify `/health` endpoint is accessible
2. Check Railway logs for errors
3. Ensure PORT environment variable is not overridden
4. Verify gunicorn is starting correctly

#### Application Errors
1. Check Railway logs for Python exceptions
2. Verify all dependencies installed
3. Test locally first: `python api/simple_server.py`
4. Check environment variables are set correctly

#### CORS Errors
- CORS is enabled by default via Flask-CORS
- If you need to restrict origins, update `api/simple_server.py`:
```python
CORS(app, origins=["https://harrie19.github.io"])
```

### Scaling

#### Free Tier Limits
- 500 hours per month
- 512MB RAM
- 1GB disk space
- Shared CPU

#### Upgrade for More Resources
1. Go to Railway Dashboard → Your Project → Settings
2. Choose "Upgrade Plan"
3. Select appropriate plan for your needs

### Cost

#### Free Tier
- $0/month
- 500 execution hours
- Perfect for testing and low-traffic apps

#### Paid Plans
- Starting at $5/month
- Unlimited execution hours
- More RAM and CPU
- Priority support

### CI/CD Integration

Railway automatically deploys when you push to main branch:

1. Push code to GitHub
2. Railway detects changes
3. Automatic build starts
4. Deployment completes
5. New version live

Disable auto-deploy:
```bash
railway link --no-deploy
```

### Rollback

#### Via Dashboard
1. Go to Railway Dashboard → Your Project → Deployments
2. Find previous successful deployment
3. Click "Redeploy"

#### Via CLI
```bash
# List deployments
railway deployments

# Rollback to specific deployment
railway redeploy [DEPLOYMENT_ID]
```

### Custom Domain

1. Go to Railway Dashboard → Your Project → Settings
2. Click "Add Custom Domain"
3. Enter your domain (e.g., `api.umaja.com`)
4. Add CNAME record to your DNS:
   ```
   CNAME api [your-project].up.railway.app
   ```
5. Wait for DNS propagation (5-30 minutes)
6. SSL automatically provisioned

### Security Best Practices

1. ✅ Always set `DEBUG=False` in production
2. ✅ Use environment variables for secrets
3. ✅ Enable HTTPS (automatic on Railway)
4. ✅ Set up rate limiting (already configured)
5. ✅ Monitor logs regularly
6. ✅ Keep dependencies updated
7. ✅ Use health checks
8. ✅ Implement graceful shutdown (already done)

### Support

- Railway Documentation: https://docs.railway.app
- Railway Discord: https://discord.gg/railway
- GitHub Issues: https://github.com/harrie19/UMAJA-Core/issues

---

**Last Updated:** 2026-01-03
**Railway Version:** 2.0+
**UMAJA Version:** 2.1.0
