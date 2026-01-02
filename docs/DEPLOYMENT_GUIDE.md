# 🚀 UMAJA-Core Deployment Guide

**Quick Start Guide for Production Deployment**

This consolidated guide covers deploying UMAJA-Core to production with Railway (backend) and GitHub Pages (frontend).

## 📋 Table of Contents

- [Overview](#overview)
- [Prerequisites](#prerequisites)
- [Railway Backend Deployment](#railway-backend-deployment)
- [GitHub Pages Frontend Setup](#github-pages-frontend-setup)
- [Environment Configuration](#environment-configuration)
- [Verification & Testing](#verification--testing)
- [Troubleshooting](#troubleshooting)
- [Post-Deployment](#post-deployment)

---

## 🎯 Overview

UMAJA-Core uses a **dual-deployment architecture**:

- **Backend (Railway)**: Python Flask API serving smiles, health checks, and World Tour endpoints
- **Frontend (GitHub Pages)**: Static HTML dashboard displaying system status and metrics

### Architecture Flow
```
User → GitHub Pages (Static Dashboard) → Railway API (Backend) → Response
```

**Cost**: $0 (both platforms have free tiers)

---

## ✅ Prerequisites

### Required Accounts
- [x] GitHub account (for repository and Pages)
- [x] Railway account (sign up at [railway.app](https://railway.app))

### Repository Setup
- [x] Repository forked/cloned
- [x] `main` branch accessible
- [x] GitHub Actions enabled

---

## 🚂 Railway Backend Deployment

### Step 1: Create Railway Project

1. **Sign in to Railway**
   - Go to [railway.app](https://railway.app)
   - Connect your GitHub account

2. **Create New Project**
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose `harrie19/UMAJA-Core`

3. **Configure Deployment**
   - Railway will auto-detect Python
   - Start command: `gunicorn --bind 0.0.0.0:$PORT wsgi:app`
   - Build command: `pip install -r requirements.txt`

### Step 2: Configure Environment Variables

In Railway dashboard, add these variables:

```bash
ENVIRONMENT=production
DEBUG=false
PORT=5000  # Railway sets this automatically
```

### Step 3: Deploy

- Railway will automatically deploy on first setup
- Subsequent pushes to `main` trigger automatic redeployment
- Deployment takes ~2-3 minutes

### Step 4: Get Your Backend URL

After deployment:
- Railway provides a URL like: `https://umaja-core-production.up.railway.app`
- Copy this URL for frontend configuration

### Health Check Configuration

The `railway.json` file includes:
```json
{
  "deploy": {
    "startCommand": "gunicorn --bind 0.0.0.0:$PORT wsgi:app",
    "healthcheckPath": "/health",
    "healthcheckTimeout": 100,
    "restartPolicyType": "ON_FAILURE"
  }
}
```

This ensures Railway monitors your service health and uses gunicorn for production-grade WSGI serving.

---

## 🌐 GitHub Pages Frontend Setup

### Step 1: Enable GitHub Pages

1. Go to repository **Settings**
2. Navigate to **Pages** section (left sidebar)
3. Under **Source**, select **GitHub Actions**
4. Save changes

### Step 2: Configure Frontend

Update the backend URL in `docs/index.html`:

```javascript
// Around line 243
const BACKEND_URL = 'https://umaja-core-production.up.railway.app';
const FALLBACK_MODE = false; // Disable demo mode once backend is live
```

### Step 3: Deploy

- Push changes to `main` branch
- GitHub Actions automatically deploys to Pages
- First deployment takes 2-3 minutes
- Access at: `https://harrie19.github.io/UMAJA-Core/`

### Dashboard Features

The dashboard includes:
- 🟢 Live backend health status
- 📊 System metrics and version info
- 🎭 Interactive smile generator
- 📡 API endpoint documentation
- 🔄 Auto-refresh every 60 seconds

---

## ⚙️ Environment Configuration

### Backend Environment Variables (.env.example reference)

```bash
# Minimal Production Setup
ENVIRONMENT=production
DEBUG=False
WORLDTOUR_MODE=true
SALES_ENABLED=false
USE_OFFLINE_TTS=true
PORT=5000

# Contact Information
CONTACT_EMAIL=Umaja1919@googlemail.com
```

### Railway-Specific Notes

- `PORT` is auto-set by Railway (don't override)
- `PYTHONUNBUFFERED=1` ensures logs appear in console
- Health check endpoint: `/health`

---

## ✅ Verification & Testing

### Test Backend

```bash
# Health check
curl https://your-railway-url.up.railway.app/health

# Expected response:
{
  "status": "healthy",
  "service": "UMAJA-Core",
  "version": "2.1.0",
  "mission": "8 billion smiles"
}

# Test daily smile endpoint
curl https://your-railway-url.up.railway.app/api/daily-smile
```

### Test Frontend

1. Open `https://harrie19.github.io/UMAJA-Core/`
2. Verify status indicator is green (healthy)
3. Click "Generate Smile" button
4. Check browser console for errors
5. Verify metrics update after 60 seconds

### Integration Test

- Dashboard should connect to backend automatically
- "Generate Smile" should return live data (not demo data)
- Health status should show "Healthy" (not "Demo Mode")

---

## 🔧 Troubleshooting

### Railway Issues

**Problem**: Deployment fails with module import error
```bash
Solution:
1. Verify requirements.txt has all dependencies:
   - Flask==3.0.0
   - gunicorn==23.0.0
   - torch>=2.0.0
   - sentence-transformers>=2.2.2
   - numpy>=1.24.3,<2.0.0
   - pycountry>=22.3.0
   - pysrt>=1.1.2
2. Check Railway logs for specific error
3. Ensure Python 3.11 is being used
```

**Problem**: Health check fails
```bash
Solution:
1. Test locally: python api/simple_server.py
2. Verify health endpoint returns 200
3. Check railway.json has correct healthcheckPath
```

**Problem**: Application crashes on startup
```bash
Solution:
1. Check Railway logs for error messages
2. Verify environment variables are set correctly
3. Ensure PORT is not hardcoded (Railway sets it)
```

### GitHub Pages Issues

**Problem**: Pages not deploying
```bash
Solution:
1. Settings → Pages → Source: "GitHub Actions"
2. Check Actions tab for deployment status
3. Wait 2-3 minutes for DNS propagation
```

**Problem**: Dashboard shows "Offline" status
```bash
Solution:
1. Verify Railway backend is running
2. Check BACKEND_URL in docs/index.html is correct
3. Test backend health endpoint directly
4. Check browser console for CORS errors
```

**Problem**: CORS errors in browser console
```bash
Solution:
1. Backend has flask-cors enabled by default
2. Verify backend URL doesn't have trailing slash
3. Check Railway logs for CORS configuration
```

### Common Issues

**Import Errors**: Missing dependencies
```bash
# Add to requirements.txt:
torch>=2.0.0
sentence-transformers>=2.2.2
numpy>=1.24.3,<2.0.0
pycountry>=22.3.0
pysrt>=1.1.2
gunicorn==23.0.0
```

**Timezone Warnings**: Deprecated datetime usage
```bash
# Already fixed in api/simple_server.py:
from datetime import datetime, timezone
datetime.now(timezone.utc).isoformat()
```

---

## 🎯 Post-Deployment

### Checklist

#### Backend Verification
- [ ] `/health` endpoint returns 200
- [ ] `/version` endpoint shows correct version
- [ ] `/api/daily-smile` generates smiles
- [ ] No errors in Railway logs
- [ ] Health checks passing in Railway dashboard

#### Frontend Verification  
- [ ] Dashboard loads at GitHub Pages URL
- [ ] Status shows "Healthy" (green indicator)
- [ ] "Generate Smile" returns live backend data
- [ ] Metrics display correctly
- [ ] Auto-refresh working (60s interval)
- [ ] No errors in browser console

#### Integration Tests
- [ ] Dashboard connects to backend successfully
- [ ] CORS working (no browser errors)
- [ ] All API endpoints documented and accessible
- [ ] Mobile responsive design functional

### Monitoring

**Railway Dashboard**:
- Monitor deployment status
- Check application logs
- View resource usage
- Set up alerts (optional)

**GitHub Pages**:
- Check Actions tab for deployment history
- Monitor Pages build status
- Verify DNS updates

---

## 📞 Support & Contact

If you encounter issues:

1. **Check Logs**
   - Railway: Dashboard → Deployments → Logs
   - GitHub: Actions tab → Workflow runs

2. **Test Endpoints Manually**
   ```bash
   curl https://your-railway-url.up.railway.app/health
   ```

3. **Verify Configuration**
   - Environment variables in Railway
   - Backend URL in docs/index.html
   - GitHub Pages source setting

4. **Contact**
   - **Email**: Umaja1919@googlemail.com
   - **GitHub Issues**: [Create an issue](https://github.com/harrie19/UMAJA-Core/issues)

---

## 🌟 Success Criteria

Your deployment is successful when:

✅ Railway backend responds to `/health` with `200 OK`  
✅ GitHub Pages dashboard loads without errors  
✅ Dashboard shows "Healthy" status indicator  
✅ Smile generation works with live backend data  
✅ No CORS errors in browser console  
✅ Both services deployed within 5 minutes  
✅ Auto-refresh updates metrics every 60 seconds  

---

## 📚 Additional Resources

- **Detailed Dual Deployment**: See [DUAL_DEPLOYMENT.md](DUAL_DEPLOYMENT.md)
- **Railway Documentation**: [docs.railway.app](https://docs.railway.app)
- **GitHub Pages Guide**: [docs.github.com/pages](https://docs.github.com/en/pages)

---

**Made with ❤️ for 8 billion people**

*"The earth is but one country, and mankind its citizens"* — Bahá'u'lláh
