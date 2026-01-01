# UMAJA-Core Production Deployment Guide

**Version:** 2.0  
**Last Updated:** 2026-01-01  
**Contact:** Umaja1919@googlemail.com

---

## Table of Contents

1. [Overview](#overview)
2. [Quick Start](#quick-start)
3. [Railway Backend Deployment](#railway-backend-deployment)
4. [GitHub Pages Frontend Deployment](#github-pages-frontend-deployment)
5. [Environment Configuration](#environment-configuration)
6. [Health Checks & Verification](#health-checks--verification)
7. [GitHub Actions Workflows](#github-actions-workflows)
8. [Troubleshooting](#troubleshooting)
9. [Monitoring & Maintenance](#monitoring--maintenance)
10. [Emergency Procedures](#emergency-procedures)

---

## Overview

UMAJA-Core uses a dual-deployment strategy to achieve $0 cost at scale:

- **Backend API**: Railway (Python Flask with automatic deployments)
- **Frontend Dashboard**: GitHub Pages (Static HTML/JS)
- **Content Delivery**: CDN via GitHub Pages (pre-generated JSON files)

### Key Features

✅ **Zero Cost**: Free tiers for all services  
✅ **Auto-Deploy**: Push to `main` triggers deployments  
✅ **Global CDN**: GitHub Pages edge network  
✅ **Health Monitoring**: Built-in health check endpoints  
✅ **Scalability**: Static content serves 8 billion users

---

## Quick Start

### Prerequisites

- GitHub account with repository access
- Railway account (free tier)
- Python 3.11+ installed locally
- Git configured

### 5-Minute Deploy

```bash
# 1. Clone repository
git clone https://github.com/harrie19/UMAJA-Core.git
cd UMAJA-Core

# 2. Install dependencies
pip install -r requirements.txt

# 3. Test locally
python api/simple_server.py
# Visit http://localhost:5000/health

# 4. Push to main (triggers auto-deploy)
git push origin main

# 5. Verify deployments
# Backend: https://umaja-core-production.up.railway.app/health
# Frontend: https://harrie19.github.io/UMAJA-Core/
```

---

## Railway Backend Deployment

### Initial Setup

1. **Connect Repository to Railway**
   - Go to [Railway.app](https://railway.app)
   - Click "New Project" → "Deploy from GitHub repo"
   - Select `harrie19/UMAJA-Core`
   - Railway auto-detects Python and uses `railway.json`

2. **Configure Environment Variables**
   
   In Railway dashboard, set:
   ```
   ENVIRONMENT=production
   DEBUG=False
   CONTACT_EMAIL=Umaja1919@googlemail.com
   ```
   
   Note: `PORT` is automatically set by Railway - do not override!

3. **Verify Configuration**
   
   Railway uses `railway.json`:
   ```json
   {
     "build": {
       "builder": "NIXPACKS"
     },
     "deploy": {
       "startCommand": "python api/simple_server.py",
       "restartPolicyType": "ON_FAILURE",
       "restartPolicyMaxRetries": 10,
       "healthcheckPath": "/health",
       "healthcheckTimeout": 100
     }
   }
   ```

### Automatic Deployments

Every push to `main` branch triggers:

1. Railway detects commit
2. Installs dependencies from `requirements.txt`
3. Runs health check on `/health` endpoint
4. Routes traffic to new deployment (zero downtime)
5. Old deployment terminated after health check passes

### Custom Domain (Optional)

1. In Railway dashboard → Settings → Domains
2. Add custom domain: `api.umaja.org`
3. Update DNS with provided CNAME record
4. SSL certificate auto-generated

---

## GitHub Pages Frontend Deployment

### Configuration

GitHub Pages is configured to serve from the `docs/` directory.

**Settings Location**: Repository → Settings → Pages

```yaml
Source: Deploy from a branch
Branch: main
Folder: /docs
```

### Deployment Process

1. Push changes to `docs/` folder
2. GitHub Actions workflow `.github/workflows/pages-deploy.yml` triggers
3. Static files served globally via CDN
4. Available at: `https://harrie19.github.io/UMAJA-Core/`

### Dashboard Features

The `docs/index.html` dashboard provides:

- ✅ Live backend health status
- ✅ Daily smile generator (all archetypes & languages)
- ✅ System metrics and statistics
- ✅ Auto-refresh every 60 seconds

### CDN Content Structure

Pre-generated smiles stored in `cdn/smiles/`:

```
cdn/smiles/
├── manifest.json              # Index of all content
├── Dreamer/
│   ├── en/1.json             # English, Day 1
│   ├── es/1.json             # Spanish, Day 1
│   └── ...                   # 8 languages × 365 days
├── Warrior/
│   └── ...
└── Healer/
    └── ...
```

Total: 8,760 JSON files (3 archetypes × 8 languages × 365 days)

---

## Environment Configuration

### Required Variables

Create `.env` file from template:

```bash
cp .env.example .env
```

**Minimal production configuration:**

```bash
# Core Settings
ENVIRONMENT=production
DEBUG=False
PORT=5000

# Contact
CONTACT_EMAIL=Umaja1919@googlemail.com

# Features
WORLDTOUR_MODE=true
SALES_ENABLED=false
USE_OFFLINE_TTS=true
```

### Optional Variables

See `.env.example` for full list of configuration options:

- Mission settings
- Personality configuration
- Content generation parameters
- Output formatting
- Community engagement settings
- Development flags

---

## Health Checks & Verification

### Backend Health Check

**Endpoint**: `GET /health`

```bash
curl https://umaja-core-production.up.railway.app/health
```

**Expected Response:**
```json
{
  "status": "alive",
  "mission": "8 billion smiles"
}
```

### Comprehensive Verification

```bash
# 1. Backend health
curl https://umaja-core-production.up.railway.app/health

# 2. Daily smile endpoint
curl https://umaja-core-production.up.railway.app/api/daily-smile

# 3. Archetype-specific smile
curl https://umaja-core-production.up.railway.app/api/smile/Dreamer

# 4. Frontend dashboard (browser)
open https://harrie19.github.io/UMAJA-Core/

# 5. CDN content (sample)
curl https://harrie19.github.io/UMAJA-Core/cdn/smiles/Dreamer/en/1.json
```

### Automated Health Monitoring

Use `scripts/deployment_health_check.py`:

```bash
python scripts/deployment_health_check.py
```

This script verifies:
- ✅ Backend API responsiveness
- ✅ All API endpoints functional
- ✅ CDN content accessible
- ✅ Response times < 200ms
- ✅ No error responses

---

## GitHub Actions Workflows

### 1. Text Generation Workflow

**File**: `.github/workflows/text-generation.yml`

**Purpose**: On-demand text generation with quality analysis

**Usage**:
1. Go to Actions tab in GitHub
2. Select "Text Generation Workflow"
3. Click "Run workflow"
4. Provide inputs:
   - **Topic**: Subject for generation (e.g., "artificial intelligence")
   - **Length**: `short` or `long`
   - **Noise Level**: 0.0 to 1.0 (creativity level)

**Outputs**:
- `generated_text.txt` - Human-readable output with quality metrics
- `generated_text_output.json` - Structured data for analysis
- Artifacts retained for 30 days

**Example**:
```yaml
Topic: artificial intelligence
Length: short
Noise Level: 0.3
```

**Result includes**:
- Generated text
- Quality rating (excellent/good/acceptable/poor)
- Theme similarity score
- Inter-sentence coherence
- Overall quality score

### 2. Railway Deploy Workflow

**File**: `.github/workflows/railway-deploy.yml`

Triggers on:
- Push to `main` branch
- Pull requests to `main`

Actions:
- Installs dependencies
- Runs tests
- Deploys to Railway (on merge to main)

### 3. Daily Worldtour Workflow

**File**: `.github/workflows/daily-worldtour.yml`

Scheduled generation of daily content at 06:00 UTC.

### 4. Tests Workflow

**File**: `.github/workflows/tests.yml`

Runs on all pull requests:
- Python syntax check
- Unit tests
- Integration tests
- Code quality checks

---

## Troubleshooting

### Common Issues

#### 1. Railway Deployment Fails

**Symptoms**: Build fails, health check times out

**Solutions**:
```bash
# Check Railway logs
railway logs

# Verify requirements.txt
pip install -r requirements.txt

# Test locally
python api/simple_server.py

# Check health endpoint
curl http://localhost:5000/health
```

#### 2. GitHub Pages Not Updating

**Symptoms**: Changes to docs/ not reflected on live site

**Solutions**:
- Check Actions tab for Pages deployment status
- Verify Pages is enabled: Settings → Pages
- Clear browser cache: Ctrl+Shift+R
- Wait 2-3 minutes for CDN propagation

#### 3. Missing Dependencies

**Symptoms**: `ModuleNotFoundError` in logs

**Solution**:
```bash
# Verify all dependencies in requirements.txt
pip freeze > requirements-frozen.txt
diff requirements.txt requirements-frozen.txt

# Add missing packages (example with correct version)
echo "sentence-transformers>=2.3.0" >> requirements.txt
```

#### 4. VektorAnalyzer Errors

**Symptoms**: Text generation fails with analyzer errors

**Solution**:
```bash
# Test VektorAnalyzer locally
python -c "
from src.vektor_analyzer import VektorAnalyzer
analyzer = VektorAnalyzer()
result = analyzer.analyze_coherence('AI is powerful. Tech evolves.', 'technology')
print(result)
"

# Expected: {'quality': 'good', 'theme_similarity': 0.7, ...}
```

#### 5. CORS Issues

**Symptoms**: Frontend can't access backend API

**Solution**:
- Verify `flask-cors` installed
- Check CORS configuration in `api/simple_server.py`
- Test with curl to isolate issue

---

## Monitoring & Maintenance

### Daily Checks

```bash
# Automated health check
python scripts/deployment_health_check.py

# Manual verification
curl https://umaja-core-production.up.railway.app/health
```

### Weekly Tasks

1. **Review Railway Logs**
   - Check for errors or warnings
   - Monitor resource usage
   - Verify health check success rate

2. **Update Dependencies**
   ```bash
   pip list --outdated
   # Update critical security patches
   pip install --upgrade [package]
   ```

3. **Content Generation**
   - Use text-generation workflow to create new content
   - Review quality metrics
   - Add high-quality content to CDN

### Monthly Tasks

1. **Security Updates**
   - Update Python dependencies
   - Review and apply security advisories
   - Run CodeQL security scan

2. **Performance Review**
   - Check Railway metrics dashboard
   - Analyze GitHub Pages traffic
   - Optimize slow endpoints

3. **Backup**
   - Export configuration
   - Archive generated content
   - Document any custom changes

### Metrics to Monitor

| Metric | Target | Check Location |
|--------|--------|----------------|
| Backend Uptime | 99.9% | Railway Dashboard |
| Health Check Response | < 100ms | Railway Logs |
| CDN Response Time | < 50ms | Browser DevTools |
| Error Rate | < 0.1% | Railway Logs |
| Daily Active Users | Growing | Analytics |

---

## Emergency Procedures

### Emergency Contact

**Technical Issues**: Umaja1919@googlemail.com

### Emergency Kill Switch

**File**: `.github/emergency_stop.json`

To immediately halt automated operations:

```json
{
  "emergency_stop": true,
  "reason": "Critical issue detected",
  "stopped_at": "2026-01-01T12:00:00Z"
}
```

Commit and push this change to stop all automated workflows.

### Rollback Procedure

#### Railway Rollback

1. Go to Railway Dashboard
2. Select deployment history
3. Click "Rollback" on last known good deployment
4. Verify health check passes

#### GitHub Pages Rollback

```bash
# Revert docs/ changes
git log docs/
git revert [commit-hash]
git push origin main

# Or restore from specific commit
git checkout [commit-hash] -- docs/
git commit -m "Rollback docs to working version"
git push origin main
```

### Critical Failure Response

1. **Stop Automated Operations**
   - Enable emergency stop
   - Pause GitHub Actions workflows

2. **Identify Issue**
   - Check Railway logs
   - Review recent commits
   - Test endpoints manually

3. **Mitigate**
   - Rollback to last known good state
   - Disable problematic feature
   - Switch to fallback mode

4. **Communicate**
   - Update status page
   - Notify users via GitHub
   - Email technical contact

5. **Resolve & Test**
   - Fix root cause
   - Test thoroughly in staging
   - Deploy fix incrementally

6. **Post-Mortem**
   - Document incident
   - Update procedures
   - Implement preventive measures

---

## Cost Breakdown

### Current Monthly Cost: $0.00

| Service | Plan | Cost | Limits |
|---------|------|------|--------|
| Railway | Free Tier | $0 | 500 hours/month |
| GitHub Pages | Free | $0 | 100GB bandwidth/month |
| GitHub Actions | Free | $0 | 2,000 minutes/month |
| Domain (Optional) | N/A | $12/year | 1 domain |

### Scaling Considerations

**Free Tier Capacity**:
- Backend: ~500,000 requests/month
- Frontend: ~100GB/month = 500M page loads
- Actions: ~30 workflow runs/day

**When to Upgrade**:
- Backend > 1M requests/month → Railway Pro ($5/month)
- Pages bandwidth exceeded → Cloudflare (free tier)
- Need faster builds → GitHub Actions Pro ($4/month)

---

## Production Checklist

Before considering the system production-ready:

### Technical Requirements

- [x] Backend deployed to Railway with health checks
- [x] Frontend deployed to GitHub Pages
- [x] All API endpoints functional
- [x] CDN content properly structured
- [x] Environment variables configured
- [x] Dependencies correctly specified
- [x] Automated deployments working
- [x] Health monitoring in place

### Quality Requirements

- [x] VektorAnalyzer methods implemented and tested
- [x] Text generation produces high-quality output
- [x] Quality analysis provides accurate metrics
- [x] No critical security vulnerabilities
- [x] Code review passed
- [x] Documentation complete and accurate

### Operational Requirements

- [x] Contact email updated across all files
- [x] Emergency procedures documented
- [x] Rollback procedures tested
- [x] Monitoring alerts configured
- [x] Backup strategy defined

---

## Additional Resources

### Documentation

- [Main README](../README.md) - Project overview
- [CONTRIBUTING](../CONTRIBUTING.md) - Contribution guidelines
- [Railway Deployment](./RAILWAY_DEPLOYMENT.md) - Detailed Railway guide
- [Dual Deployment](./DUAL_DEPLOYMENT.md) - Architecture details

### Useful Links

- **Backend API**: https://umaja-core-production.up.railway.app
- **Frontend Dashboard**: https://harrie19.github.io/UMAJA-Core/
- **Repository**: https://github.com/harrie19/UMAJA-Core
- **Railway Dashboard**: https://railway.app/dashboard
- **GitHub Actions**: https://github.com/harrie19/UMAJA-Core/actions

### Support

For deployment issues or questions:
- 📧 Email: Umaja1919@googlemail.com
- 💬 GitHub Issues: [Create Issue](https://github.com/harrie19/UMAJA-Core/issues)
- 📖 Discussions: [GitHub Discussions](https://github.com/harrie19/UMAJA-Core/discussions)

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 2.0 | 2026-01-01 | Consolidated deployment guide for production readiness |
| 1.0 | 2025-12-15 | Initial deployment documentation |

---

**🕊️ Built with ❤️ for 8 billion humans 🕊️**

---

*Last updated: 2026-01-01*
*Maintained by: UMAJA Development Team*
*Contact: Umaja1919@googlemail.com*
