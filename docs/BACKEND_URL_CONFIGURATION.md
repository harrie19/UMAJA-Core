# Backend URL Configuration Guide

## Overview
This guide explains how to configure and verify the backend URL for the UMAJA-Core dashboard at `docs/index.html`.

## Current Configuration

**File:** `docs/index.html`  
**Line:** 324  
**Current URL:** `https://web-production-6ec45.up.railway.app`

```javascript
const BACKEND_URL = 'https://web-production-6ec45.up.railway.app';
```

## How to Verify the Correct Railway URL

### Step 1: Access Railway Dashboard
1. Go to [https://railway.app/dashboard](https://railway.app/dashboard)
2. Log in with your GitHub account
3. Find the `UMAJA-Core` project
4. Click on the deployment

### Step 2: Find the Deployment URL
1. In the Railway deployment view, look for the "Deployments" or "Settings" section
2. Find the auto-generated URL
3. It should follow the format: `https://[project-name].up.railway.app`

### Step 3: Update docs/index.html
If the URL is different from what's configured:

1. Open `docs/index.html`
2. Find the line with `const BACKEND_URL =` (line 324)
3. Update it to match your Railway deployment URL:

```javascript
const BACKEND_URL = 'https://your-actual-railway-url.up.railway.app';
```

4. Commit and push the changes
5. GitHub Pages will automatically update

## Verification

### Using the Verification Script
Run the automated verification script:

```bash
python3 scripts/verify_backend_url.py
```

This will test:
- ✅ Backend health endpoint (`/health`)
- ✅ CORS configuration  
- ✅ Daily smile API (`/api/daily-smile`)
- ✅ World Tour API (`/worldtour/status`)

### Manual Verification
Test the health endpoint directly:

```bash
curl https://web-production-6ec45.up.railway.app/health
```

Expected response:
```json
{
  "status": "healthy",
  "version": "2.1.0",
  "environment": "production",
  "checks": {
    "archetypes_available": ["professor", "worrier", "enthusiast"]
  }
}
```

### Dashboard Verification
After updating, visit [https://harrie19.github.io/UMAJA-Core/](https://harrie19.github.io/UMAJA-Core/) and verify:

- ✅ Green "Connected" status indicator
- ✅ Backend version displays correctly
- ✅ "Get Daily Smile" button generates smiles
- ✅ World Tour status loads
- ✅ No CORS errors in browser console (F12)

## Common Issues

### Issue: Backend shows "Offline ❌"

**Causes:**
1. Backend not deployed on Railway
2. Wrong URL configured
3. CORS not allowing GitHub Pages origin
4. Railway deployment sleeping (free tier)

**Solutions:**
1. Verify Railway deployment is active
2. Check URL matches Railway dashboard
3. Ensure backend has `CORS(app)` enabled (already configured in `api/simple_server.py`)
4. If using Railway free tier, first request may wake up the service (30s delay)

### Issue: CORS errors in browser console

**Error:** `Access to fetch at 'https://...' from origin 'https://harrie19.github.io' has been blocked by CORS policy`

**Solution:**
Backend CORS is already configured to allow all origins in `api/simple_server.py` (currently line 35, search for `CORS(app)`):
```python
from flask_cors import CORS
app = Flask(__name__)
CORS(app)  # Allows all origins
```

If you want to restrict to specific origins:
```python
CORS(app, origins=[
    "https://harrie19.github.io",
    "http://localhost:5000",  # For local development
    "http://localhost:3000"   # For alternative local port
])
```

### Issue: Wrong URL in Configuration

**Previous Wrong URL:** `https://web-production-6ec45.up.railway.app`  
**Correct URL:** `https://web-production-6ec45.up.railway.app`

If you see the old wrong URL, update it immediately in `docs/index.html`.

## Railway Deployment Checklist

- [ ] Railway project created and connected to GitHub
- [ ] Backend deployed and showing "Active" status
- [ ] Deployment URL noted from Railway dashboard
- [ ] `docs/index.html` BACKEND_URL matches Railway URL
- [ ] Health endpoint returns 200 OK: `/health`
- [ ] CORS headers include `Access-Control-Allow-Origin: *`
- [ ] GitHub Pages published from `docs/` directory
- [ ] Dashboard loads without errors

## Files to Check

When updating the backend URL, verify these files:

1. **docs/index.html** (line 324) - Dashboard configuration
2. **docs/index.html** (line ~309) - API Health link in footer
3. **api/simple_server.py** (line 35) - CORS configuration (search for `CORS(app)`)

Note: Line numbers may change as code evolves. Use search to locate exact lines.

## Testing Workflow

1. **Update URL** in `docs/index.html` if needed
2. **Commit changes**: `git commit -am "Update backend URL to match Railway deployment"`
3. **Push to GitHub**: `git push origin main`
4. **Run verification**: `python3 scripts/verify_backend_url.py`
5. **Test dashboard**: Visit GitHub Pages URL and check status
6. **Check console**: Open browser DevTools (F12) and verify no errors

## Support

If issues persist:
- **Railway Logs**: Check Railway dashboard → Deployments → Logs
- **GitHub Actions**: Check if Pages deployment succeeded
- **Browser Console**: Check for JavaScript errors (F12 → Console)
- **Network Tab**: Check failed requests (F12 → Network)

## Reference URLs

- **Railway Dashboard**: https://railway.app/dashboard
- **GitHub Pages**: https://harrie19.github.io/UMAJA-Core/
- **Backend Health**: https://web-production-6ec45.up.railway.app/health
- **Repository**: https://github.com/harrie19/UMAJA-Core
