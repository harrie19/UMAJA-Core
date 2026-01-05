# 🚀 UMAJA-Core Dual-Deployment Guide

Complete guide for deploying UMAJA-Core with both Railway (backend) and GitHub Pages (frontend dashboard).

## 📋 Table of Contents

- [Overview](#overview)
- [Railway Backend Deployment](#railway-backend-deployment)
- [GitHub Pages Dashboard Deployment](#github-pages-dashboard-deployment)
- [Configuration](#configuration)
- [Troubleshooting](#troubleshooting)
- [Post-Deployment Checklist](#post-deployment-checklist)

## 🎯 Overview

UMAJA-Core uses a dual-deployment strategy:

- **Railway**: Hosts the Python Flask backend API (`api/simple_server.py`)
- **GitHub Pages**: Serves the static HTML dashboard that displays system status

### Architecture

```
┌─────────────────┐
│  GitHub Pages   │  ← Static Dashboard (HTML/CSS/JS)
│   (Frontend)    │
└────────┬────────┘
         │
         │ HTTP Requests
         ↓
┌─────────────────┐
│    Railway      │  ← Flask API Server
│   (Backend)     │
└─────────────────┘
```

## 🚂 Railway Backend Deployment

### Prerequisites

1. **Railway Account**: Sign up at [railway.app](https://railway.app)
2. **Railway Token**: Generate a token in Railway dashboard
3. **GitHub Secret**: Add `RAILWAY_TOKEN` to repository secrets

### Setup Steps

1. **Configure Railway Secret**
   ```bash
   # Go to: https://github.com/harrie19/UMAJA-Core/settings/secrets/actions
   # Add new secret:
   # Name: RAILWAY_TOKEN
   # Value: <your-railway-token>
   ```

2. **Update Railway Service Name** (if needed)
   Edit `.github/workflows/railway-deploy.yml` line 47:
   ```yaml
   service: umaja-core-backend  # Change to match your Railway service name
   ```

3. **Automatic Deployment**
   - Push to `main` branch triggers automatic deployment
   - Or manually trigger via Actions tab → "🚂 Deploy to Railway"

3. **Workflow File**
   Located at `.github/workflows/railway-deploy.yml`

### Health Checks

The deployment includes pre and post-deploy health checks:

- ✅ Flask import validation
- ✅ Core modules verification
- ✅ Deployment completion status

### Manual Deployment

To manually deploy:

```bash
# Via GitHub Actions UI
1. Go to Actions tab
2. Select "🚂 Deploy to Railway"
3. Click "Run workflow"
4. Choose environment (production/staging)
```

## 🌐 GitHub Pages Dashboard Deployment

### Prerequisites

1. **Enable GitHub Pages**
   ```
   Settings → Pages → Source: GitHub Actions
   ```

2. **Wait for First Deployment**
   - First deployment takes 2-3 minutes
   - Dashboard URL: `https://harrie19.github.io/UMAJA-Core/`

### Setup Steps

1. **Enable Pages** (ONE-TIME SETUP)
   - Go to repository Settings
   - Navigate to Pages section
   - Under "Source", select "GitHub Actions"
   - Save changes

2. **Automatic Deployment**
   - Pushes to `main` that modify `docs/**` trigger deployment
   - Or manually trigger via Actions tab

3. **Workflow File**
   Located at `.github/workflows/pages-deploy.yml`

### Dashboard Features

The dashboard (`docs/index.html`) includes:

- 🟢 Live backend health monitoring
- 📊 System metrics display
- 🎭 Smile generator with API integration
- 📡 API endpoint documentation
- 🔄 Auto-refresh every 60 seconds
- 🛡️ Fallback/demo mode when backend is offline

## ⚙️ Configuration

### Update Backend URL in Dashboard

After Railway deployment completes:

1. **Get Railway URL**
   - Check Railway dashboard for your deployment URL
   - Example: `https://web-production-6ec45.up.railway.app`

2. **Update Dashboard Configuration**
   ```javascript
   // In docs/index.html, around line 243
   const BACKEND_URL = 'https://your-actual-railway-url.up.railway.app';
   const FALLBACK_MODE = false; // Set to false once backend is live
   ```

3. **Commit and Push**
   ```bash
   git add docs/index.html
   git commit -m "Update dashboard with Railway backend URL"
   git push
   ```

### Environment Variables

Backend supports these environment variables:

| Variable | Description | Default |
|----------|-------------|---------|
| `PORT` | Server port | 5000 |
| `ENVIRONMENT` | Deployment environment | production |
| `DEBUG` | Debug mode | false |

## 🔧 Troubleshooting

### Railway Deployment Issues

**Problem**: Deployment fails with module import error
```bash
Solution:
1. Check requirements.txt includes all dependencies
2. Verify Python version (3.11)
3. Review Railway logs for specific errors
```

**Problem**: Health check fails
```bash
Solution:
1. Test locally: python api/simple_server.py
2. Check for missing dependencies
3. Verify Flask installation
```

### GitHub Pages Issues

**Problem**: Pages deployment fails with "Not Found"
```bash
Solution:
1. Enable GitHub Pages in Settings → Pages
2. Set Source to "GitHub Actions"
3. Wait 2-3 minutes for propagation
```

**Problem**: Dashboard shows "Offline" status
```bash
Solution:
1. Verify Railway backend is deployed
2. Check BACKEND_URL in docs/index.html
3. Ensure CORS is enabled on backend
4. Test backend URL directly: https://your-url/health
```

**Problem**: CORS errors in browser console
```bash
Solution:
1. Backend already has flask-cors enabled
2. Check browser console for actual error
3. Verify backend URL is correct
```

### Network Connectivity

**Test Backend Connectivity**
```bash
# Test health endpoint
curl https://your-railway-url/health

# Should return:
# {"status": "healthy", "mission": "8 billion smiles", ...}
```

**Test Dashboard**
```bash
# Open in browser
https://harrie19.github.io/UMAJA-Core/

# Check browser console for errors
# Dashboard should show "Demo Mode" or "Healthy" status
```

## ✅ Post-Deployment Checklist

After deploying both services:

### Railway Backend

- [ ] Deployment completed successfully
- [ ] Health endpoint returns 200: `https://your-url/health`
- [ ] Version endpoint accessible: `https://your-url/version`
- [ ] Daily smile endpoint works: `https://your-url/api/daily-smile`
- [ ] No errors in Railway logs

### GitHub Pages Dashboard

- [ ] Dashboard accessible: `https://harrie19.github.io/UMAJA-Core/`
- [ ] Status indicator shows correct state (green/demo mode)
- [ ] "Generate Smile" button works
- [ ] Metrics display correctly
- [ ] Backend URL updated in configuration
- [ ] No CORS errors in browser console

### Integration Testing

- [ ] Dashboard successfully connects to backend
- [ ] Smile generation returns live data from backend
- [ ] Health check updates every 60 seconds
- [ ] All API endpoints documented correctly
- [ ] Mobile responsive design works

## 🎯 Success Criteria

Your deployment is successful when:

1. ✅ Railway backend responds to `/health` endpoint
2. ✅ GitHub Pages dashboard loads without errors
3. ✅ Dashboard shows "Healthy" status (not "Offline")
4. ✅ "Generate Smile" button returns smiles from backend
5. ✅ System metrics update automatically
6. ✅ Both deployments complete within 5 minutes

## 📞 Support

If you encounter issues:

1. Check GitHub Actions logs for workflow errors
2. Review Railway deployment logs
3. Test endpoints manually with `curl`
4. Verify all configuration URLs are correct
5. Ensure GitHub Pages is enabled in repository settings

## 🌟 Bahá'í Principles in Deployment

- **Truth**: Honest status reporting with real health checks
- **Service**: Free dashboard accessible to all
- **Unity**: Backend and frontend working together harmoniously

---

**Made with ❤️ for 8 billion people** • [GitHub](https://github.com/harrie19/UMAJA-Core) • [Dashboard](https://harrie19.github.io/UMAJA-Core/)
