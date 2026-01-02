# 🚂 Railway Deployment Guide

**Contact:** Umaja1919@googlemail.com

Complete guide for deploying UMAJA-Core to Railway with production-ready configuration.

## Table of Contents
- [Quick Start](#quick-start)
- [Prerequisites](#prerequisites)
- [Required Secrets](#required-secrets)
- [Environment Variables](#environment-variables)
- [Deployment Steps](#deployment-steps)
- [Health Checks](#health-checks)
- [Post-Deployment Verification](#post-deployment-verification)
- [Monitoring](#monitoring)
- [Troubleshooting](#troubleshooting)
- [Zero-Downtime Deployments](#zero-downtime-deployments)

---

## Quick Start

For experienced users who have Railway token ready:

```bash
# 1. Set Railway token in GitHub Secrets
# Go to: Settings → Secrets and variables → Actions → New repository secret
# Name: RAILWAY_TOKEN
# Value: <your-railway-token>

# 2. Trigger deployment
# Option A: Push to main branch
git push origin main

# Option B: Manual deployment via GitHub Actions
# Go to: Actions → Deploy UMAJA WORLDTOUR → Run workflow

# 3. Wait 2-3 minutes and verify
curl https://your-railway-app.railway.app/health
```

---

## Prerequisites

### Required Accounts
- ✅ GitHub account (already have it!)
- ✅ Railway account ([railway.app](https://railway.app))

### Required Tools (for local testing)
- Python 3.11+
- pip
- git

### Railway Setup
1. Sign up at [railway.app](https://railway.app)
2. Create a new project
3. Connect to GitHub repository
4. Generate Railway token:
   - Go to Account Settings → Tokens
   - Click "Create Token"
   - Copy the token (you'll need this for GitHub Secrets)

---

## Required Secrets

### GitHub Repository Secrets

Navigate to: **Settings → Secrets and variables → Actions → New repository secret**

| Secret Name | Description | How to Get |
|------------|-------------|------------|
| `RAILWAY_TOKEN` | Railway API token for deployments | Railway Dashboard → Account → Tokens → Create Token |

**That's it!** Only one secret needed for basic deployment.

### Optional Secrets (for advanced features)

| Secret Name | Required | Purpose |
|------------|----------|---------|
| `HEROKU_API_KEY` | No | Alternative deployment to Heroku |
| `HEROKU_APP_NAME` | No | Heroku app identifier |
| `HEROKU_EMAIL` | No | Heroku account email |

---

## Environment Variables

Environment variables are configured in Railway Dashboard after deployment.

### Required Variables

Railway automatically sets these:

- `PORT` - Automatically assigned by Railway (don't override!)
- `RAILWAY_ENVIRONMENT` - Set by Railway platform

### Recommended Production Variables

Set these in Railway Dashboard → Variables:

| Variable | Value | Purpose |
|----------|-------|---------|
| `ENVIRONMENT` | `production` | Identifies deployment environment |
| `PYTHONUNBUFFERED` | `1` | Ensures logs appear in Railway console |
| `DEBUG` | `false` | Disables debug mode in production |

### Optional Variables

| Variable | Default | Purpose |
|----------|---------|---------|
| `LOG_LEVEL` | `INFO` | Logging verbosity (DEBUG, INFO, WARNING, ERROR) |
| `MISSION` | `daily_smile` | Primary mission focus |
| `DEFAULT_ARCHETYPE` | `random` | Default personality archetype |

See `.env.example` for complete list of available configuration options.

---

## Deployment Steps

### Method 1: Automatic Deployment (Recommended)

Deployments automatically trigger on push to `main` branch:

```bash
# Make your changes
git add .
git commit -m "Your changes"
git push origin main

# GitHub Actions automatically deploys to Railway
# Watch progress: https://github.com/your-repo/actions
```

### Method 2: Manual Deployment via GitHub Actions

1. Go to **Actions** tab in your GitHub repository
2. Select **Deploy UMAJA WORLDTOUR** workflow
3. Click **Run workflow**
4. Select options:
   - Platform: `railway`
   - Environment: `production`
5. Click **Run workflow**
6. Wait 2-3 minutes for completion

### Method 3: Direct Railway Deployment

If you prefer deploying directly through Railway:

1. Go to Railway Dashboard
2. Select your project
3. Go to **Deployments** tab
4. Click **Deploy**
5. Railway will automatically pull latest from GitHub and deploy

---

## Health Checks

UMAJA-Core includes comprehensive health check endpoints:

### Primary Health Check
```bash
curl https://your-app.railway.app/health
```

Expected response (200 OK):
```json
{
  "status": "healthy",
  "service": "UMAJA-Core",
  "version": "1.0.0",
  "mission": "8 billion smiles",
  "timestamp": "2026-01-01T12:00:00.000000",
  "environment": "production",
  "checks": {
    "api": "ok",
    "smiles_loaded": true,
    "archetypes_available": ["professor", "worrier", "enthusiast"],
    "content_generation": "ok"
  }
}
```

### Version Endpoint
```bash
curl https://your-app.railway.app/version
```

### Deployment Info
```bash
curl https://your-app.railway.app/deployment-info
```

---

## Post-Deployment Verification

### Automated Health Check

Use the included health check script:

```bash
# Install dependencies
pip install requests

# Run comprehensive health check
python scripts/deployment_health_check.py https://your-app.railway.app

# Output: Detailed report with all endpoint checks
# Saves report to: deployment_report.json
```

### Manual Verification Checklist

- [ ] Health endpoint returns 200 OK
- [ ] Version endpoint shows correct version
- [ ] Daily smile API generates content
- [ ] All archetype endpoints working
- [ ] Error handling returns proper 404/500
- [ ] Logs visible in Railway dashboard
- [ ] Response times under 500ms

### Test All Endpoints

```bash
# Root endpoint
curl https://your-app.railway.app/

# Health check
curl https://your-app.railway.app/health

# Version
curl https://your-app.railway.app/version

# Daily smile
curl https://your-app.railway.app/api/daily-smile

# Specific archetype
curl https://your-app.railway.app/api/smile/professor

# 404 handling
curl https://your-app.railway.app/nonexistent
```

---

## Monitoring

### Continuous Monitoring Script

Monitor your deployment health continuously:

```bash
# Monitor with default 60s interval
python scripts/monitor_deployment.py https://your-app.railway.app

# Monitor with custom interval (30s)
python scripts/monitor_deployment.py https://your-app.railway.app 30

# Monitor for specific duration (300s = 5 minutes)
python scripts/monitor_deployment.py https://your-app.railway.app 60 300
```

The monitor will:
- ✅ Check health every interval
- ✅ Track uptime percentage
- ✅ Measure response times
- ✅ Alert on consecutive failures
- ✅ Save metrics to `deployment_metrics.json`

### Railway Dashboard Monitoring

Railway provides built-in monitoring:

1. **Logs**: Railway Dashboard → Your Service → Logs
   - Real-time application logs
   - Filter by severity
   - Search capabilities

2. **Metrics**: Railway Dashboard → Your Service → Metrics
   - CPU usage
   - Memory usage
   - Network traffic
   - Request rates

3. **Deployments**: Railway Dashboard → Your Service → Deployments
   - Deployment history
   - Build logs
   - Rollback options

### Setting Up Alerts

1. Monitor deployment health with cron job:
```bash
# Add to crontab (check every 5 minutes)
*/5 * * * * /path/to/python /path/to/scripts/deployment_health_check.py https://your-app.railway.app
```

2. Use Railway webhooks for deployment events:
   - Go to Railway Dashboard → Settings → Webhooks
   - Add webhook URL (e.g., Slack, Discord, email service)
   - Select events to monitor

---

## Troubleshooting

### Common Issues and Solutions

#### Issue: Deployment fails with "Port already in use"
**Solution**: Railway automatically assigns `PORT` - don't override it in environment variables.

#### Issue: Application crashes immediately after deploy
**Solutions**:
1. Check Railway logs: Dashboard → Logs
2. Verify all required dependencies in `requirements.txt`
3. Ensure Python version compatibility (3.11+)
4. Check for missing environment variables

#### Issue: Health check returns 503
**Solutions**:
1. Wait 30-60 seconds for application to fully start
2. Check Railway logs for startup errors
3. Verify `startCommand` in `railway.json` is correct
4. Test locally: `python api/simple_server.py`

#### Issue: "Module not found" errors
**Solution**: Add missing package to `requirements.txt` and redeploy

#### Issue: Logs not appearing in Railway
**Solution**: Ensure `PYTHONUNBUFFERED=1` is set in environment variables

#### Issue: Slow response times
**Solutions**:
1. Check Railway service plan (consider upgrading)
2. Review application logs for errors
3. Consider adding caching if needed
4. Check for database connection issues

### Debug Mode

To enable detailed logging for troubleshooting:

1. Go to Railway Dashboard → Variables
2. Set `DEBUG=true`
3. Redeploy
4. Check logs for detailed information
5. **IMPORTANT**: Set back to `DEBUG=false` after debugging!

### Local Testing

Test deployment configuration locally before pushing:

```bash
# Install dependencies
pip install -r requirements.txt

# Set environment variables
export PORT=5000
export ENVIRONMENT=production
export PYTHONUNBUFFERED=1

# Run server
python api/simple_server.py

# In another terminal, test endpoints
curl http://localhost:5000/health
```

### Rollback to Previous Version

If deployment causes issues:

1. Go to Railway Dashboard → Deployments
2. Find last working deployment
3. Click "..." menu → Rollback
4. Railway will redeploy previous version

---

## Zero-Downtime Deployments

Railway automatically handles zero-downtime deployments:

### How It Works

1. Railway builds new version in background
2. New instance starts and passes health checks
3. Traffic gradually shifts to new version
4. Old version stays running until traffic migrates
5. Old version shuts down after migration complete

### Configuration

Health check configuration in `railway.json`:

```json
{
  "deploy": {
    "healthcheckPath": "/health",
    "healthcheckTimeout": 100,
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 10
  }
}
```

### Best Practices

1. **Always include health checks**: Ensures Railway knows when app is ready
2. **Test before deploying**: Run local tests to catch issues early
3. **Monitor logs during deployment**: Watch for startup errors
4. **Use staging environment**: Test changes in staging before production
5. **Keep deployments small**: Smaller changes = easier to debug and rollback

---

## Performance Optimization

### Railway Service Configuration

Recommended settings for production:

- **Plan**: Starter or higher (for better performance)
- **Region**: Choose region closest to your users
- **Autoscaling**: Enable if expecting variable traffic

### Application Optimization

Current configuration is optimized for:
- Fast startup times (< 10 seconds)
- Low memory footprint
- Efficient request handling
- Minimal dependencies

### Monitoring Performance

Track these metrics:

- **Response Time**: Should be < 500ms for most requests
- **Uptime**: Target 99.9% uptime
- **Error Rate**: Should be < 0.1%
- **Memory Usage**: Monitor for memory leaks

---

## Security Considerations

### Environment Variables

- ✅ Never commit secrets to repository
- ✅ Use Railway environment variables for sensitive data
- ✅ Rotate tokens periodically
- ✅ Use different secrets for staging/production

### HTTPS

Railway automatically provides HTTPS for all deployments - no configuration needed!

### CORS

CORS is enabled by default. To restrict origins in production:

1. Update `api/simple_server.py`
2. Configure CORS with specific origins
3. Redeploy

---

## Support and Resources

### Documentation
- Railway Docs: https://docs.railway.app
- UMAJA-Core Docs: See `/docs` directory
- GitHub Actions: https://docs.github.com/actions

### Useful Commands

```bash
# Check deployment status
curl https://your-app.railway.app/health

# View logs (requires Railway CLI)
railway logs

# Test locally
python api/simple_server.py

# Run health check
python scripts/deployment_health_check.py https://your-app.railway.app

# Monitor deployment
python scripts/monitor_deployment.py https://your-app.railway.app
```

---

## Success Checklist

Before considering deployment complete:

- [ ] Railway token configured in GitHub Secrets
- [ ] Environment variables set in Railway Dashboard
- [ ] Health endpoint returns 200 OK
- [ ] All API endpoints functional
- [ ] Logs visible in Railway console
- [ ] Monitoring script tested
- [ ] Health check script tested and passing
- [ ] Response times acceptable (< 500ms)
- [ ] Error handling working (404, 500)
- [ ] HTTPS working (automatic via Railway)
- [ ] Zero-downtime deployment verified

---

## Next Steps

After successful deployment:

1. ✅ Set up monitoring (use `monitor_deployment.py`)
2. ✅ Configure alerting (Railway webhooks or cron jobs)
3. ✅ Test all functionality end-to-end
4. ✅ Share deployment URL with team
5. ✅ Document any custom configurations
6. ✅ Set up staging environment (optional)
7. ✅ Enable Railway metrics dashboard

---

## Contact and Support

- **Repository Issues**: [GitHub Issues](../../issues)
- **Railway Support**: https://railway.app/help
- **Documentation Updates**: Submit PR to this doc

---

**Mission**: Bringing smiles to 8 billion people 🌍  
**Principle**: Service, not profit ✨  
**Status**: Production Ready 🚀

Happy deploying!
