# 🚀 UMAJA World Tour - Quick Deployment Guide

## Current Status: NOT YET DEPLOYED ⏳

The code is **ready and tested**, but not yet live. Deployment requires merging to `main` branch.

---

## 🌐 Intended Deployment URLs

### GitHub Pages (Dashboard/Frontend)
- **URL**: https://harrie19.github.io/UMAJA-Core/
- **Status**: ⏳ Awaiting merge to main
- **Purpose**: Public dashboard, documentation, sitemap, robots.txt

### Railway (Backend API)
- **URL**: https://umaja-core-production.up.railway.app
- **Status**: ⏳ Awaiting Railway setup + merge to main
- **Purpose**: REST API, World Tour endpoints, AI agent metadata

---

## ✅ What's Ready

All files are prepared and tested:
- ✅ `docs/index.html` - Dashboard with SEO meta tags
- ✅ `docs/sitemap.xml` - All 59 cities mapped
- ✅ `docs/robots.txt` - AI crawler allowlist
- ✅ `api/simple_server.py` - Backend with 7+ endpoints
- ✅ `railway.json` - Railway configuration
- ✅ `.github/workflows/pages-deploy.yml` - Auto-deploy workflow
- ✅ `.github/workflows/railway-deploy.yml` - Auto-deploy workflow
- ✅ All tests passing (19/19)
- ✅ Security scan clean (0 vulnerabilities)

---

## 🚀 Deployment Steps

### Step 1: Merge This PR ⭐ REQUIRED

```bash
# Once approved, merge to main branch
# This triggers automatic deployments
```

### Step 2: Enable GitHub Pages

1. Go to: https://github.com/harrie19/UMAJA-Core/settings/pages
2. **Source**: Deploy from a branch
3. **Branch**: `main`
4. **Folder**: `/docs`
5. Click **Save**

The workflow `.github/workflows/pages-deploy.yml` will automatically deploy on every push to main.

### Step 3: Set Up Railway Backend

#### Option A: Via Railway Dashboard (Recommended)
1. Visit https://railway.app
2. Click **New Project**
3. Select **Deploy from GitHub repo**
4. Choose `harrie19/UMAJA-Core`
5. Railway auto-detects `railway.json` configuration
6. Click **Deploy**
7. Get your deployment URL (e.g., `umaja-core-production.up.railway.app`)

#### Option B: Via Railway CLI
```bash
# Install Railway CLI
npm install -g @railway/cli

# Login
railway login

# Link to project
railway link

# Deploy
railway up
```

### Step 4: Update GitHub Secret (Optional - For Auto-Deploy)

1. Go to: https://github.com/harrie19/UMAJA-Core/settings/secrets/actions
2. Create secret: `RAILWAY_TOKEN`
3. Get token from Railway dashboard: Settings → Tokens
4. Now pushes to main will auto-deploy to Railway

---

## 🧪 Verification After Deployment

### Check GitHub Pages
```bash
# Should return 200
curl -I https://harrie19.github.io/UMAJA-Core/

# Check sitemap
curl https://harrie19.github.io/UMAJA-Core/sitemap.xml

# Check robots.txt
curl https://harrie19.github.io/UMAJA-Core/robots.txt
```

### Check Railway Backend
```bash
# Health check
curl https://umaja-core-production.up.railway.app/health

# AI agents endpoint
curl https://umaja-core-production.up.railway.app/api/ai-agents

# World Tour status
curl https://umaja-core-production.up.railway.app/worldtour/status
```

---

## 📊 Expected Response Times

After deployment:
- **GitHub Pages**: <200ms (CDN)
- **Railway API**: <500ms
- **Both**: Available 24/7 at $0 cost

---

## ❓ Troubleshooting

### GitHub Pages Not Loading
- Check if Pages is enabled in repo settings
- Verify workflow ran successfully: Actions tab
- Check branch is `main` and folder is `/docs`
- Wait 2-3 minutes after merge

### Railway Not Accessible
- Verify Railway project is created and linked
- Check Railway dashboard for deployment logs
- Ensure `railway.json` is in repository root
- Railway provides a unique URL after first deploy

### Need Help?
- GitHub Pages Docs: https://docs.github.com/en/pages
- Railway Docs: https://docs.railway.app/
- Contact: Umaja1919@googlemail.com

---

## 🎯 Summary

**Current State**: Code ready, not deployed  
**Blocker**: Needs merge to `main` branch  
**Time to Deploy**: ~5 minutes after merge  
**Cost**: $0/month (free tiers)  

Once merged, GitHub Pages and Railway will automatically deploy the UMAJA World Tour! 🌍✨

---

*Last Updated: 2026-01-03*  
*Version: 1.0*
