# 🚀 Railway Web-Based Deployment (Recommended)

Deploy UMAJA Worldtour to Railway using GitHub integration - **no CLI, no tokens, no secrets needed!**

## Why Railway GitHub Integration?

Railway's GitHub App integration is the **easiest way** to deploy:

- ✅ **No CLI Installation** - Everything in the browser
- ✅ **No GitHub Secrets** - Railway uses OAuth, not API tokens
- ✅ **No Token Management** - Railway handles authentication automatically
- ✅ **Auto-Deploy on Push** - Every git push triggers a new deployment
- ✅ **Built-in HTTPS/SSL** - Free certificates automatically
- ✅ **Real-time Logs** - Monitor deployment and runtime in dashboard
- ✅ **Easy Rollback** - One-click revert to previous versions

## 🌟 Quick Start (3 Steps)

### Step 1: Connect GitHub to Railway

1. Go to **https://railway.app**
2. Click **"Login"** → Sign in with GitHub
3. Grant Railway access to your repositories

### Step 2: Create Project from GitHub

1. Click **"New Project"**
2. Select **"Deploy from GitHub repo"**
3. Choose **harrie19/UMAJA-Core** (or your fork)
4. Railway automatically detects:
   - `railway.json` configuration
   - `requirements.txt` dependencies
   - Python project with Flask
   - Nixpacks builder

### Step 3: Configure Environment Variables

Railway needs environment variables to run UMAJA. Go to your project → **"Variables"** tab:

**Minimal Configuration (Copy these 6 variables):**

```env
ENVIRONMENT=production
DEBUG=False
WORLDTOUR_MODE=true
SALES_ENABLED=false
USE_OFFLINE_TTS=true
PORT=5000
```

Click **"+ New Variable"** for each one. Then click **"Deploy"**!

### Step 4: Get Your Public URL

1. Go to **"Settings"** tab
2. Under **"Networking"**, click **"Generate Domain"**
3. Railway creates URL like: `umaja-production.up.railway.app`
4. **Test it:**
   ```bash
   curl https://your-app.up.railway.app/health
   ```

**That's it!** 🎉 Your UMAJA Worldtour is live!

---

## 📖 Detailed Guide

See **[docs/RAILWAY_AUTO_DEPLOY.md](../docs/RAILWAY_AUTO_DEPLOY.md)** for:
- Complete step-by-step instructions
- Environment variable reference
- Premium features setup (ElevenLabs, Stability AI)
- Monitoring and logs
- Troubleshooting
- Advanced configuration

---

## 🔄 Auto-Deploy on Git Push

Railway automatically redeploys when you push to GitHub:

```bash
git add .
git commit -m "Update personality engine"
git push origin main
```

Railway detects the push and:
1. Pulls latest code
2. Rebuilds application
3. Runs health checks
4. Deploys with zero downtime

**No manual steps needed!**

---

## 🛠️ Alternative: Railway CLI (Advanced)

If you prefer command-line deployment:

### Setup Railway CLI

```bash
# Install Railway CLI
npm install -g @railway/cli

# Login (opens browser for OAuth)
railway login

# Link to existing project
railway link

# Or create new project
railway init
```

### Deploy via CLI

```bash
# Deploy current directory
railway up

# Set environment variables
railway variables set ENVIRONMENT=production
railway variables set WORLDTOUR_MODE=true
railway variables set USE_OFFLINE_TTS=true

# View logs
railway logs

# Open in browser
railway open
```

### Environment Variables via CLI

```bash
# Set individual variables
railway variables set KEY=value

# Set multiple from .env file
railway variables set $(cat .env)

# List all variables
railway variables
```

---

## 🌐 Alternative: GitHub Actions (Legacy - Not Recommended)

**Note:** This method requires GitHub Secrets and is more complex than Railway's GitHub integration. We recommend using Railway's web-based deployment instead.

<details>
<summary>Click to expand GitHub Actions setup (legacy method)</summary>

### Setup GitHub Secrets

This repository includes automated deployment via GitHub Actions, but it requires manual secret configuration:

#### For Railway Deployment via Actions

1. **Get Railway Token:**
   - Go to https://railway.app
   - Navigate to Account Settings → Tokens
   - Create a new token

2. **Add GitHub Secret:**
   - Go to repository → Settings → Secrets and variables → Actions
   - Click "New repository secret"
   - Name: `RAILWAY_TOKEN`
   - Value: Your Railway token

3. **Deploy:**
   - Go to **Actions** tab
   - Select **Deploy UMAJA WORLDTOUR** workflow
   - Click **Run workflow**

**Why we don't recommend this:**
- Requires manual token management
- Tokens expire and need rotation
- More complex setup than Railway GitHub integration
- GitHub Actions has limited build minutes on free tier

</details>

---

## 📊 Monitoring Your Deployment

### Railway Dashboard

1. **View Logs:**
   - Click **"Logs"** tab for real-time output
   - Filter by severity (info, warning, error)

2. **Check Metrics:**
   - CPU usage
   - Memory usage
   - Request rate
   - Response time

3. **Health Check:**
   - Railway monitors `/health` endpoint
   - Auto-restarts on failure
   - Configured in `railway.json`

### Test Endpoints

```bash
# Health check
curl https://your-app.up.railway.app/health

# Generate content
curl -X POST https://your-app.up.railway.app/api/generate/text \
  -H "Content-Type: application/json" \
  -d '{"topic":"test","personality":"john_cleese","length":"short"}'

# Worldtour cities
curl https://your-app.up.railway.app/api/worldtour/cities
```

---

## 🔍 Troubleshooting

### Deployment fails with "Build error"

**Solution:**
1. Check **Build Logs** in Railway dashboard
2. Verify `requirements.txt` has all dependencies
3. Ensure Python 3.11+ specified

### App crashes after deployment

**Solution:**
1. Check **Runtime Logs** for error messages
2. Verify environment variables are set correctly
3. Ensure server binds to `0.0.0.0:$PORT`

### Health check failing

**Solution:**
1. Verify `/health` endpoint exists in code
2. Check server is listening on correct port
3. Ensure `PORT` environment variable is set

---

## ✅ Pre-Deployment Checklist

Run this before deploying:

```bash
python scripts/railway_deploy_check.py
```

This validates:
- [x] Python version 3.11+
- [x] Required files present
- [x] Dependencies installed
- [x] Environment template configured
- [x] Core modules working
- [x] Health endpoint exists
- [x] Railway config valid

---

## 💰 Cost Estimate

Railway pricing (as of 2024):

| Setup | Monthly Cost |
|-------|-------------|
| **Trial** | $0 (7 days with $5 credit) |
| **Minimal** (512MB RAM) | $3-5 |
| **Standard** (1GB RAM) | $8-12 |
| **Premium** (2GB RAM) | $15-20 |

**UMAJA Worldtour runs well on minimal setup!**

---

## 🔐 Security Best Practices

### Protect API Keys

- ✅ Never commit secrets to GitHub
- ✅ Use Railway's Variables UI only
- ✅ Enable `.gitignore` for `.env` files
- ✅ Rotate keys regularly in Railway dashboard

### Railway Security Features

- 🔒 Variables encrypted at rest
- 🔒 Not exposed in logs (Railway redacts)
- 🔒 Only visible to project members
- 🔒 Free SSL certificates

---

## 📞 Getting Help

### Railway Support
- 📖 [Railway Documentation](https://docs.railway.app)
- 💬 [Railway Discord](https://discord.gg/railway)
- 📧 Email: team@railway.app

### UMAJA Worldtour Help
- 📖 [Railway Auto-Deploy Guide](../docs/RAILWAY_AUTO_DEPLOY.md)
- 📚 [Full Deployment Guide](../docs/DEPLOYMENT.md)
- 📊 [API Documentation](../docs/MULTIMEDIA_SYSTEM.md)
- 🐛 [GitHub Issues](https://github.com/harrie19/UMAJA-Core/issues)

---

## ✅ Summary: Web vs CLI vs GitHub Actions

| Method | Ease | Setup Time | Auto-Deploy | Recommended |
|--------|------|-----------|-------------|-------------|
| **Railway Web** | ⭐⭐⭐⭐⭐ | 5 min | ✅ Yes | **✅ YES** |
| Railway CLI | ⭐⭐⭐⭐ | 10 min | ✅ Yes | If you prefer CLI |
| GitHub Actions | ⭐⭐ | 20 min | ✅ Yes | Not recommended |
| Heroku Web | ⭐⭐⭐ | 10 min | ✅ Yes | Alternative |

**We strongly recommend Railway Web-Based deployment** for the easiest experience!

---

**Made with ❤️ and 😂 by the UMAJA Team**

*Deploy once, laugh forever!* 🎭🌍
