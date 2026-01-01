# 🚀 UMAJA-Core Deployment Checklist

Complete pre-deployment checklist to ensure smooth production deployment to Railway.

## Pre-Deployment Setup

### 1. Railway Account & Project Setup
- [ ] Railway account created ([railway.app](https://railway.app))
- [ ] New project created in Railway
- [ ] GitHub repository connected to Railway
- [ ] Railway token generated (Settings → Tokens)

### 2. GitHub Repository Configuration
- [ ] Repository forked/cloned
- [ ] Branch protection enabled on `main` (recommended)
- [ ] GitHub Actions enabled
- [ ] Workflow permissions configured (Settings → Actions → General)

### 3. Required Secrets Configuration
- [ ] `RAILWAY_TOKEN` added to GitHub Secrets
  - Location: Settings → Secrets and variables → Actions
  - Value: Railway API token from Railway Dashboard

### 4. Optional Secrets (if using Heroku)
- [ ] `HEROKU_API_KEY` configured (if using Heroku deployment)
- [ ] `HEROKU_APP_NAME` configured (if using Heroku)
- [ ] `HEROKU_EMAIL` configured (if using Heroku)

## Code Readiness

### 5. Dependencies
- [ ] `requirements.txt` is up to date
- [ ] All dependencies have compatible versions
- [ ] Python version compatible (3.11+)
- [ ] No security vulnerabilities in dependencies

### 6. Configuration Files
- [ ] `railway.json` present and valid
- [ ] `Procfile` present (web: python api/simple_server.py)
- [ ] `.env.example` documented
- [ ] `.gitignore` excludes sensitive files

### 7. Application Code
- [ ] Health check endpoint implemented (`/health`)
- [ ] Version endpoint implemented (`/version`)
- [ ] Deployment info endpoint implemented (`/deployment-info`)
- [ ] Error handling for 404/500 errors
- [ ] Logging configured
- [ ] Graceful shutdown implemented
- [ ] Environment variable validation on startup

## Testing

### 8. Local Testing
- [ ] Application starts locally without errors
- [ ] Health endpoint accessible: `curl http://localhost:5000/health`
- [ ] All API endpoints tested and working
- [ ] Environment variables properly loaded
- [ ] Graceful shutdown works (Ctrl+C)

### 9. Automated Tests
- [ ] Existing tests pass: `python -m pytest` (if applicable)
- [ ] Personality engine test passes
- [ ] Worldtour generator test passes
- [ ] Bundle builder test passes
- [ ] No critical linting errors

### 10. Health Check Validation
- [ ] Deployment health check script tested locally
- [ ] Script executes without errors
- [ ] All endpoint checks included
- [ ] Report generation works

## Environment Variables

### 11. Production Environment Variables
Set these in Railway Dashboard → Variables:

**Required**:
- [ ] `ENVIRONMENT=production`
- [ ] `PYTHONUNBUFFERED=1`
- [ ] `DEBUG=false`

**Optional** (with sensible defaults):
- [ ] `MISSION` (default: daily_smile)
- [ ] `DEFAULT_ARCHETYPE` (default: random)
- [ ] `CONTENT_TONE` (default: warm)

**Railway Auto-Set** (do not override):
- [ ] `PORT` - Auto-assigned by Railway
- [ ] `RAILWAY_ENVIRONMENT` - Auto-set by Railway

## Documentation

### 12. Documentation Review
- [ ] `README.md` includes deployment instructions
- [ ] `docs/RAILWAY_DEPLOYMENT.md` reviewed and accurate
- [ ] `DEPLOYMENT_CHECKLIST.md` (this file) completed
- [ ] `.env.example` includes all variables with descriptions
- [ ] API endpoints documented

## Security

### 13. Security Checks
- [ ] No secrets/tokens in source code
- [ ] `.gitignore` excludes `.env` file
- [ ] Sensitive data uses environment variables
- [ ] CORS configuration appropriate for production
- [ ] HTTPS enabled (automatic on Railway)
- [ ] Debug mode disabled in production

### 14. Dependency Security
- [ ] No known vulnerabilities in dependencies
- [ ] Dependencies pinned to specific versions
- [ ] Regular dependency updates scheduled

## Deployment

### 15. Initial Deployment
- [ ] All checklist items above completed
- [ ] Changes committed to git
- [ ] Changes pushed to `main` branch OR
- [ ] Manual workflow triggered via GitHub Actions

### 16. Deployment Monitoring
- [ ] Watch GitHub Actions workflow progress
- [ ] Monitor Railway deployment logs
- [ ] Check for build errors
- [ ] Verify application starts successfully

### 17. Post-Deployment Verification
- [ ] Health check endpoint accessible and returns 200 OK
- [ ] Version endpoint shows correct version
- [ ] All API endpoints functional
- [ ] Response times acceptable (< 500ms)
- [ ] Logs visible in Railway dashboard
- [ ] Error handling works (test 404 endpoint)

### 18. Automated Verification
- [ ] Run deployment health check:
  ```bash
  python scripts/deployment_health_check.py https://your-app.railway.app
  ```
- [ ] All checks pass (100% success rate)
- [ ] Review generated `deployment_report.json`

### 19. Monitoring Setup
- [ ] Monitor script tested:
  ```bash
  python scripts/monitor_deployment.py https://your-app.railway.app 60 300
  ```
- [ ] Monitoring metrics saved to `deployment_metrics.json`
- [ ] Uptime tracking confirmed
- [ ] Alert thresholds configured (optional)

## Post-Deployment

### 20. Production Validation
- [ ] Smoke test: Generate daily smile
- [ ] Test each archetype endpoint
- [ ] Verify error responses
- [ ] Check CORS headers (if needed)
- [ ] Validate deployment info endpoint

### 21. Performance Baseline
- [ ] Record baseline response times
- [ ] Note initial memory/CPU usage
- [ ] Document concurrent request handling
- [ ] Establish uptime baseline (target 99.9%)

### 22. Ongoing Monitoring
- [ ] Set up continuous monitoring (cron job or external service)
- [ ] Configure Railway alerts/webhooks
- [ ] Schedule regular health checks
- [ ] Plan for log review schedule

### 23. Rollback Plan
- [ ] Previous deployment version identified
- [ ] Rollback procedure documented
- [ ] Rollback tested (if time permits)
- [ ] Team knows how to perform rollback

## Communication

### 24. Team Notification
- [ ] Deployment announcement sent
- [ ] Deployment URL shared
- [ ] Documentation links provided
- [ ] Known issues (if any) communicated

### 25. Documentation Updates
- [ ] Deployment date/time recorded
- [ ] Version number updated
- [ ] Changelog updated (if applicable)
- [ ] Production URL documented

## Troubleshooting Preparation

### 26. Emergency Contacts
- [ ] Railway support contact available
- [ ] GitHub Actions documentation bookmarked
- [ ] Team emergency contact list updated
- [ ] Escalation procedure defined

### 27. Debug Tools Ready
- [ ] Railway CLI installed (optional)
- [ ] Local environment matches production
- [ ] Debug mode toggle procedure documented
- [ ] Log analysis tools ready

## Long-Term Maintenance

### 28. Maintenance Planning
- [ ] Dependency update schedule defined
- [ ] Security patch procedure established
- [ ] Backup strategy documented (if needed)
- [ ] Disaster recovery plan outlined

### 29. Scaling Preparation
- [ ] Railway plan evaluated for traffic expectations
- [ ] Autoscaling configured (if needed)
- [ ] Load testing plan created
- [ ] Performance optimization targets set

### 30. Continuous Improvement
- [ ] Feedback mechanism established
- [ ] Performance monitoring dashboard set up
- [ ] Regular review schedule for this checklist
- [ ] Lessons learned documented

---

## Quick Reference

### Essential Commands

```bash
# Test locally
python api/simple_server.py

# Run health check
python scripts/deployment_health_check.py https://your-app.railway.app

# Monitor deployment
python scripts/monitor_deployment.py https://your-app.railway.app

# Check health endpoint
curl https://your-app.railway.app/health

# View version
curl https://your-app.railway.app/version
```

### Essential URLs
- GitHub Actions: `https://github.com/YOUR_USERNAME/UMAJA-Core/actions`
- Railway Dashboard: `https://railway.app/dashboard`
- Deployment Docs: `docs/RAILWAY_DEPLOYMENT.md`

---

## Deployment Success Criteria

✅ **Deployment is successful when:**
1. Health check endpoint returns 200 OK
2. All API endpoints functional
3. Response times < 500ms
4. Zero errors in Railway logs
5. Deployment health check script passes 100%
6. Monitoring shows 100% uptime for first hour
7. All features working as expected

---

## Sign-Off

**Deployment Date:** _________________

**Deployed By:** _________________

**Deployment URL:** _________________

**Notes/Issues:** 
_________________________________
_________________________________
_________________________________

**Status:** [ ] Success  [ ] Success with issues  [ ] Failed

---

**Mission:** Bringing smiles to 8 billion people 🌍  
**Principle:** Service, not profit ✨  
**Status:** Ready for Production 🚀

Remember: Take your time, follow each step, and don't skip validation!
