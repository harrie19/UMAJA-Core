# 🔧 UMAJA-Core Troubleshooting Guide

**Common Issues and Solutions**

This guide helps you diagnose and fix common problems with UMAJA-Core deployment and operation.

---

## 📋 Table of Contents

- [Quick Diagnostics](#quick-diagnostics)
- [Deployment Issues](#deployment-issues)
- [Runtime Errors](#runtime-errors)
- [API Issues](#api-issues)
- [World Tour Problems](#world-tour-problems)
- [Frontend Issues](#frontend-issues)
- [Performance Problems](#performance-problems)
- [GitHub Actions Issues](#github-actions-issues)
- [Dependencies](#dependencies)

---

## 🔍 Quick Diagnostics

### Health Check Test
```bash
# Test backend health
curl https://your-railway-url.up.railway.app/health

# Expected response:
{
  "status": "healthy",
  "service": "UMAJA-Core",
  "version": "2.1.0",
  "timestamp": "2026-01-02T15:30:35.922000+00:00"
}
```

### Common Quick Fixes
1. **Check Railway logs**: Railway Dashboard → Deployments → Logs
2. **Verify environment variables**: Railway Dashboard → Variables
3. **Test locally**: `python api/simple_server.py`
4. **Clear browser cache**: Hard refresh (Ctrl+Shift+R)
5. **Check GitHub Actions**: Actions tab → Recent workflow runs

---

## 🚂 Deployment Issues

### Problem: Railway Build Fails

**Symptom**: Build fails during dependency installation

**Solution**:
```bash
1. Check requirements.txt format
   - Each dependency on a new line
   - No blank lines at the end
   - Correct version syntax

2. Verify Python version
   - Railway uses Python 3.11 by default
   - Check runtime.txt if you need a specific version

3. Check for conflicting dependencies
   - torch>=2.0.0 (not 2.6.0 for better compatibility)
   - numpy>=1.24.3,<2.0.0 (pin major version)

4. Review Railway build logs for specific errors
```

### Problem: Service Crashes on Startup

**Symptom**: Railway shows "Crashed" status immediately after deployment

**Solution**:
```bash
1. Check start command in railway.json:
   "startCommand": "gunicorn --bind 0.0.0.0:$PORT wsgi:app"

2. Verify wsgi.py exists and imports correctly:
   from api.simple_server import app
   application = app

3. Check Railway logs for Python errors:
   - Import errors: Missing dependencies
   - Port binding errors: Check PORT variable
   - Module not found: Path issues

4. Test locally:
   gunicorn --bind 0.0.0.0:5000 wsgi:app
```

### Problem: Health Check Fails

**Symptom**: Railway shows "Unhealthy" status

**Solution**:
```bash
1. Verify health endpoint works:
   curl https://your-url/health

2. Check railway.json configuration:
   {
     "healthcheckPath": "/health",
     "healthcheckTimeout": 100
   }

3. Ensure health endpoint returns 200:
   - Check api/simple_server.py health() function
   - Verify no exceptions in health check code

4. Increase timeout if needed:
   "healthcheckTimeout": 120
```

### Problem: Deployment Takes Too Long

**Symptom**: Build/deployment exceeds 10 minutes

**Solution**:
```bash
1. Check for large dependencies:
   - torch can be slow to install
   - Consider using CPU-only version

2. Enable build caching:
   - Railway caches pip packages by default
   - First build will be slow, subsequent builds faster

3. Optimize requirements.txt:
   - Pin specific versions for faster resolution
   - Remove unused dependencies

4. Monitor Railway build logs:
   - Identify which step takes longest
   - Optimize that specific step
```

---

## ⚠️ Runtime Errors

### Problem: ModuleNotFoundError

**Symptom**: `ModuleNotFoundError: No module named 'X'`

**Solution**:
```bash
# Common missing modules and fixes:

1. torch / sentence_transformers:
   Add to requirements.txt:
   torch>=2.0.0
   sentence-transformers>=2.2.2

2. pycountry / pysrt:
   Add to requirements.txt:
   pycountry>=22.3.0
   pysrt>=1.1.2

3. Application modules:
   Check sys.path configuration
   Verify file structure matches imports
   
4. Redeploy after updating requirements.txt
```

### Problem: Timezone Warning

**Symptom**: `DeprecationWarning: datetime.datetime.now()` without timezone

**Solution**:
```python
# Fixed in api/simple_server.py (already implemented):
from datetime import datetime, timezone

# WRONG:
timestamp = datetime.now().isoformat()

# CORRECT:
timestamp = datetime.now(timezone.utc).isoformat()
```

### Problem: Memory Errors

**Symptom**: `MemoryError` or OOM (Out of Memory) crashes

**Solution**:
```bash
1. Use CPU-only torch:
   pip install torch --index-url https://download.pytorch.org/whl/cpu

2. Reduce model size:
   Use 'all-MiniLM-L6-v2' (default, lightweight)
   Avoid larger models unless necessary

3. Optimize VektorAnalyzer usage:
   - Cache embeddings when possible
   - Batch process texts
   - Clear memory after large operations

4. Railway memory limits:
   - Free tier: 512MB-1GB
   - Upgrade plan if needed for larger models
```

---

## 🔌 API Issues

### Problem: Rate Limit Errors

**Symptom**: `429 Too Many Requests`

**Solution**:
```bash
1. Current limits (api/simple_server.py):
   - Default: 100 requests/hour per IP
   - /worldtour/start: 10 requests/minute
   - /worldtour/visit: 20 requests/minute

2. For testing:
   - Temporarily increase limits
   - Use different IPs or wait

3. For production:
   - Limits are appropriate for abuse prevention
   - Upgrade limits only if legitimate use case

4. Check error response:
   {
     "error": "Too many requests",
     "retry_after": "58 seconds"
   }
```

### Problem: CORS Errors

**Symptom**: Browser console shows CORS policy errors

**Solution**:
```bash
1. Verify flask-cors is installed:
   pip list | grep Flask-CORS

2. Check CORS configuration in api/simple_server.py:
   from flask_cors import CORS
   CORS(app)

3. Browser troubleshooting:
   - Hard refresh (Ctrl+Shift+R)
   - Check Network tab for preflight OPTIONS requests
   - Verify request headers

4. Backend URL:
   - No trailing slash in frontend config
   - Use correct protocol (https://)
```

### Problem: Endpoint Not Found

**Symptom**: `404 Not Found` for valid endpoints

**Solution**:
```bash
1. Verify endpoint exists:
   Check api/simple_server.py route definitions

2. Available endpoints:
   GET  /health
   GET  /version
   GET  /api/daily-smile
   GET  /api/smile/<archetype>
   POST /worldtour/start
   POST /worldtour/visit/<city_id>
   GET  /worldtour/status
   GET  /worldtour/cities
   GET  /worldtour/content/<city_id>

3. Check URL formatting:
   - Correct spelling
   - Proper HTTP method (GET vs POST)
   - URL parameters in correct format

4. Test with curl:
   curl -X POST https://your-url/worldtour/start
```

### Problem: Slow Response Times

**Symptom**: API requests take >5 seconds

**Solution**:
```bash
1. First request may be slow:
   - Model loading (sentence-transformers)
   - Cold start on Railway
   - Expected: 3-5 seconds first request

2. Subsequent requests should be fast:
   - Models cached in memory
   - Expected: <2 seconds

3. Optimize if consistently slow:
   - Check Railway resource usage
   - Profile code for bottlenecks
   - Consider caching strategies

4. Request timeout configuration:
   REQUEST_TIMEOUT = 30  # seconds
   Increase if needed for complex operations
```

---

## 🎭 World Tour Problems

### Problem: Template Formatting Error (c3po)

**Symptom**: `KeyError: 'number'` or `KeyError: 'comparison'` in city_review

**Solution**:
```python
# FIXED in src/worldtour_generator.py:

if content_type == 'city_review':
    if personality == 'c3po':
        # c3po template uses {number}
        topic = template.format(
            city=city['name'],
            number=random.randint(100, 9999)
        )
    else:
        # Other personalities use {comparison}
        topic = template.format(
            city=city['name'],
            comparison=comparison
        )
```

### Problem: City Not Found

**Symptom**: `404 City not found`

**Solution**:
```bash
1. Verify city ID format:
   - Use lowercase with underscores: "new_york"
   - Not: "New York" or "newyork"

2. Check available cities:
   curl https://your-url/worldtour/cities

3. City database location:
   data/worldtour_cities.json

4. Add new cities:
   - Edit worldtour_generator.py
   - Add to _initialize_default_cities()
   - Redeploy
```

### Problem: Content Generation Fails

**Symptom**: Empty or malformed content from World Tour

**Solution**:
```bash
1. Verify personality and content_type:
   Valid personalities: john_cleese, c3po, robin_williams
   Valid content_types: city_review, cultural_debate, 
                        language_lesson, tourist_trap, food_review

2. Check city data completeness:
   - topics: List of local topics
   - stereotypes: Cultural stereotypes
   - fun_facts: Interesting facts
   - local_phrases: Common phrases

3. Test endpoint directly:
   curl -X POST https://your-url/worldtour/visit/london \
     -H "Content-Type: application/json" \
     -d '{"personality":"john_cleese","content_type":"city_review"}'

4. Check Railway logs for errors
```

---

## 🌐 Frontend Issues

### Problem: Dashboard Shows "Offline"

**Symptom**: Status indicator is red/offline despite backend running

**Solution**:
```javascript
1. Check BACKEND_URL in docs/index.html:
   const BACKEND_URL = 'https://your-railway-url.up.railway.app';
   // No trailing slash!

2. Verify FALLBACK_MODE is false:
   const FALLBACK_MODE = false;  // Live mode

3. Test backend directly:
   curl https://your-railway-url/health

4. Check browser console for errors:
   - Network tab for failed requests
   - Console tab for JavaScript errors
```

### Problem: Auto-Refresh Not Working

**Symptom**: Metrics don't update every 60 seconds

**Solution**:
```javascript
1. Check JavaScript console for errors

2. Verify setInterval is running:
   // Should see in code:
   setInterval(fetchData, 60000);

3. Browser may throttle inactive tabs:
   - Keep tab active/visible
   - Reduce interval if needed

4. Check for JavaScript errors:
   - Open Developer Tools
   - Monitor Console tab
```

### Problem: Mobile Layout Issues

**Symptom**: Dashboard doesn't display correctly on mobile

**Solution**:
```html
1. Verify viewport meta tag in docs/index.html:
   <meta name="viewport" content="width=device-width, initial-scale=1">

2. Test responsive design:
   - Use browser DevTools mobile emulation
   - Test on actual devices

3. Check CSS media queries:
   @media (max-width: 768px) { ... }

4. Clear mobile browser cache
```

---

## ⚡ Performance Problems

### Problem: High Memory Usage

**Symptom**: Railway shows high memory consumption

**Solution**:
```bash
1. Monitor in Railway dashboard:
   - Check Metrics tab
   - Look for memory spikes

2. Optimize VektorAnalyzer:
   - Use smaller model
   - Clear embeddings cache periodically
   - Batch process efficiently

3. Check for memory leaks:
   - Review long-running processes
   - Monitor over 24 hours
   - Profile with memory_profiler

4. Upgrade Railway plan if needed:
   - Free tier may be insufficient for heavy use
```

### Problem: Slow Cold Starts

**Symptom**: First request after idle takes >10 seconds

**Solution**:
```bash
1. Expected behavior on Railway free tier:
   - Services sleep after 30 minutes idle
   - First request wakes service (slow)
   - Keep-alive pings can help

2. Optimize model loading:
   - Lazy loading (already implemented)
   - Cache models in memory

3. Implement health check pings:
   - Periodic requests to keep service warm
   - Use external monitoring service

4. Upgrade to paid plan:
   - No sleeping
   - Faster cold starts
```

---

## 🤖 GitHub Actions Issues

### Problem: Workflow Infinite Loop

**Symptom**: Autonomous agent triggers itself repeatedly

**Solution**:
```yaml
# FIXED in .github/workflows/autonomous-agent.yml:

jobs:
  intelligent_review:
    # Prevent infinite loops
    if: |
      github.actor != 'github-actions[bot]' &&
      github.actor != 'copilot-swe-agent[bot]' &&
      !contains(github.event.head_commit.message, '[skip-ci]')
```

### Problem: Test Failures

**Symptom**: pytest fails in CI but passes locally

**Solution**:
```bash
1. Check Python version:
   - CI uses 3.11
   - Ensure local matches

2. Dependencies:
   - CI installs from requirements.txt
   - Verify all test dependencies listed

3. Environment differences:
   - Set test environment variables in workflow
   - Use fixtures for consistent state

4. Network issues:
   - Tests may fail if external services down
   - Mock external dependencies
```

### Problem: Workflow Not Triggering

**Symptom**: Push to branch doesn't start workflow

**Solution**:
```bash
1. Check workflow triggers:
   on:
     pull_request:
       types: [opened, synchronize, reopened]

2. Verify workflow file location:
   .github/workflows/*.yml

3. Check YAML syntax:
   - Use yamllint
   - Validate in GitHub Actions editor

4. Review workflow permissions:
   permissions:
     contents: write
     pull-requests: write
```

---

## 📦 Dependencies

### Problem: Dependency Conflicts

**Symptom**: `ERROR: Cannot install X and Y together`

**Solution**:
```bash
1. Check conflicting versions:
   pip list | grep <package>

2. Pin compatible versions:
   numpy>=1.24.3,<2.0.0  # Pin major version
   
3. Create fresh virtual environment:
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt

4. Use pip-compile for resolution:
   pip install pip-tools
   pip-compile requirements.txt
```

### Problem: torch Installation Fails

**Symptom**: `ERROR: Failed building wheel for torch`

**Solution**:
```bash
1. Use specific torch version:
   torch>=2.0.0  # Not 2.6.0

2. Install CPU-only version:
   pip install torch --index-url https://download.pytorch.org/whl/cpu

3. Increase build timeout:
   - Railway: Automatic
   - Local: Wait 5-10 minutes

4. Check disk space:
   - torch is large (~700MB)
   - Ensure sufficient space
```

---

## 📞 Getting Help

### Before Asking for Help

1. **Check this guide** for your specific issue
2. **Review Railway logs** for error messages
3. **Test health endpoint** to verify backend status
4. **Check browser console** for frontend errors
5. **Try locally** to isolate environment issues

### How to Report Issues

Include this information:
```
1. What you're trying to do
2. What you expected to happen
3. What actually happened
4. Error messages (full text)
5. Railway logs (relevant sections)
6. Browser console errors (if frontend issue)
7. Steps to reproduce
```

### Contact

- **Email**: Umaja1919@googlemail.com
- **GitHub Issues**: [Create Issue](https://github.com/harrie19/UMAJA-Core/issues)
- **Railway Support**: [Railway Help](https://railway.app/help)

---

## 🔗 Additional Resources

- [Deployment Guide](DEPLOYMENT_GUIDE.md)
- [Go-Live Checklist](GO_LIVE_CHECKLIST.md)
- [Railway Documentation](https://docs.railway.app)
- [Flask Documentation](https://flask.palletsprojects.com)

---

**Made with ❤️ for 8 billion people**

*"The earth is but one country, and mankind its citizens"* — Bahá'u'lláh
