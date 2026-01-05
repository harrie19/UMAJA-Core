# UMAJA-Core Enhanced Features Guide

## Overview
This guide covers the enhanced monitoring, configuration, and reliability features added to UMAJA-Core.

## Features

### 1. 🔄 Automatic Retry Logic

The dashboard now automatically retries failed backend connections with exponential backoff.

**Configuration:**
- Maximum retries: 3 attempts
- Retry delays: 1s, 2s, 4s (exponential backoff)
- Timeout per request: 5 seconds

**User Experience:**
- Shows "Retrying... (1/3) ⏳" during retry attempts
- Detailed console logging for debugging
- Automatic recovery without page reload

**Benefits:**
- Handles temporary network issues
- Survives Railway cold starts (free tier)
- Better user experience during connection issues

---

### 2. ⚙️ Environment-Based Configuration

Backend URL is now automatically detected based on environment.

**File:** `docs/config.js`

**Automatic Detection:**
- `localhost` or `127.0.0.1` → Development (`http://localhost:5000`)
- Domain contains `staging` or `dev` → Staging
- All other domains → Production (`https://web-production-6ec45.up.railway.app`)

**Manual Override:**
Add `?backendUrl=` parameter to URL:
```
https://harrie19.github.io/UMAJA-Core/?backendUrl=https://custom-backend.com
```

**Configuration:**
```javascript
// docs/config.js
const BACKEND_URLS = {
    production: 'https://web-production-6ec45.up.railway.app',
    staging: 'https://umaja-core-staging.up.railway.app',
    development: 'http://localhost:5000'
};
```

**Benefits:**
- No hardcoded URLs in HTML
- Easy switching between environments
- Testing against different backends
- Supports multiple deployment stages

---

### 3. 📊 Status Page

Real-time health monitoring dashboard with history.

**URL:** `https://harrie19.github.io/UMAJA-Core/status.html`

**Features:**
- ✅ Real-time backend status (Online/Offline)
- ⏱️ Response time measurement
- 📈 Last 20 health checks with timestamps
- 🔄 Auto-refresh every 60 seconds
- 💾 Persistent history (localStorage)
- 🎨 Visual indicators (green/red/orange)

**Metrics Displayed:**
1. **Backend URL** - Current backend being monitored
2. **Response Time** - Latency in milliseconds
3. **Version** - Backend API version
4. **Environment** - Current environment (production/staging/dev)

**History:**
- Stores last 20 health checks
- Shows success/failure status
- Displays timestamp and response time
- Color-coded (green = success, red = failure)
- Persists across page reloads

**Usage:**
```bash
# Access directly
open https://harrie19.github.io/UMAJA-Core/status.html

# Or add to main dashboard as link
```

---

### 4. 🔔 Automated Health Check Monitoring

Background script that continuously monitors backend health and sends alerts.

**File:** `scripts/monitor_health.py`

**Configuration:**
```python
CHECK_INTERVAL = 300      # 5 minutes between checks
ALERT_THRESHOLD = 3       # Alert after 3 consecutive failures
LOG_FILE = "/tmp/umaja_health_monitor.log"
```

**Features:**
- ✅ Runs health checks on schedule (every 5 minutes by default)
- 🚨 Sends alerts after consecutive failures
- 📝 Detailed logging to file
- 💾 Writes alert JSON for external monitoring
- 🔄 Auto-recovery detection

**Running Continuously:**
```bash
# Run in foreground
python3 scripts/monitor_health.py

# Run in background
nohup python3 scripts/monitor_health.py > /dev/null 2>&1 &

# Or use screen/tmux
screen -S umaja-monitor
python3 scripts/monitor_health.py
# Detach with Ctrl+A, D
```

**Schedule with Cron:**
```bash
# Edit crontab
crontab -e

# Add this line (runs every 5 minutes)
*/5 * * * * cd /path/to/UMAJA-Core && python3 scripts/monitor_health.py >> /var/log/umaja_monitor.log 2>&1
```

**Alert Integration (Optional):**

The script includes a template for email alerts. To enable:

1. Set environment variables:
```bash
export ALERT_EMAIL_FROM="alerts@umaja.org"
export ALERT_EMAIL_TO="admin@umaja.org"
export SMTP_SERVER="smtp.gmail.com"
export SMTP_PORT="587"
export SMTP_USER="your-email@gmail.com"
export SMTP_PASSWORD="your-app-password"
```

2. Uncomment email section in `scripts/monitor_health.py`

**Alternative Alerting:**

You can integrate with:
- **Slack:** Use webhook URL
- **Discord:** Use webhook URL
- **Telegram:** Use bot API
- **PagerDuty:** Use integration API
- **SMS:** Use Twilio API

Example Slack integration:
```python
import requests

def send_slack_alert(message):
    webhook_url = os.environ.get('SLACK_WEBHOOK_URL')
    if webhook_url:
        requests.post(webhook_url, json={'text': message})
```

**Log Files:**
- Main log: `/tmp/umaja_health_monitor.log`
- Alert file: `/tmp/umaja_health_alert.json`

**Monitoring the Monitor:**

Check if monitoring is running:
```bash
# Check process
ps aux | grep monitor_health.py

# Check recent logs
tail -f /tmp/umaja_health_monitor.log

# Check for alerts
cat /tmp/umaja_health_alert.json
```

---

## Complete Setup Guide

### Step 1: Deploy Backend to Railway
Ensure your backend is deployed and accessible.

### Step 2: Verify Configuration
```bash
# Test backend URL
python3 scripts/verify_backend_url.py
```

### Step 3: Check Dashboard
Visit: `https://harrie19.github.io/UMAJA-Core/`

Should show:
- ✅ Green "Online" status
- Backend version
- Working "Get Daily Smile" button

### Step 4: Access Status Page
Visit: `https://harrie19.github.io/UMAJA-Core/status.html`

Should show:
- Real-time status
- Response time
- Health history

### Step 5: Start Monitoring (Optional)
```bash
# Test monitoring
python3 scripts/monitor_health.py

# Schedule it (see cron instructions above)
```

---

## Troubleshooting

### Issue: Retries Not Working

**Check:**
1. Open browser console (F12)
2. Look for retry messages: "Retry attempt 1/3"
3. Check network tab for multiple requests

**Solution:**
- Verify `config.js` is loaded
- Check browser console for errors
- Ensure backend URL is correct

### Issue: Wrong Environment Detected

**Check:**
```javascript
// In browser console
console.log(window.UMAJAConfig);
```

**Solution:**
- Use URL parameter override: `?backendUrl=https://correct-url.com`
- Update environment detection logic in `docs/config.js`

### Issue: Status Page Not Updating

**Check:**
1. Open browser console (F12)
2. Check for CORS errors
3. Verify config.js is loaded

**Solution:**
- Clear localStorage: `localStorage.clear()`
- Hard refresh: Ctrl+F5 (Windows) or Cmd+Shift+R (Mac)
- Check backend is accessible

### Issue: Monitoring Not Alerting

**Check:**
```bash
# Check logs
tail -f /tmp/umaja_health_monitor.log

# Check if process is running
ps aux | grep monitor_health
```

**Solution:**
- Verify script has permissions: `chmod +x scripts/monitor_health.py`
- Check ALERT_THRESHOLD is reached
- Verify alert integration is configured

---

## Upgrade Path

### From Previous Version

The changes are backward compatible. To upgrade:

1. Pull latest changes
2. Clear browser cache
3. Reload dashboard

No configuration changes needed unless you want to:
- Customize retry behavior (edit `docs/index.html`)
- Add custom environments (edit `docs/config.js`)
- Configure alerting (edit `scripts/monitor_health.py`)

---

## Performance Impact

### Dashboard (index.html)
- **Before:** Single connection attempt, immediate failure
- **After:** Up to 3 retries with 7-second total delay
- **Impact:** Better reliability, slightly longer initial load if backend is down

### Status Page (status.html)
- **Load:** Minimal (one health check)
- **Auto-refresh:** Every 60 seconds
- **Storage:** ~5KB in localStorage (20 checks)
- **Impact:** Negligible

### Monitoring Script (monitor_health.py)
- **CPU:** Minimal (~0.1% during checks)
- **Memory:** ~20MB RSS
- **Network:** One request per 5 minutes
- **Impact:** Negligible

---

## Security Considerations

1. **URL Override:** Only use with trusted URLs
2. **CORS:** Backend must allow GitHub Pages origin
3. **Monitoring Logs:** May contain backend URLs (secure log files)
4. **Alert Credentials:** Use environment variables, never hardcode

---

## Future Enhancements

Potential additions:
- [ ] SMS alerts via Twilio
- [ ] Dashboard widget for status
- [ ] Historical uptime percentage
- [ ] Performance metrics (P50, P95, P99)
- [ ] Incident timeline
- [ ] Automated incident reports

---

## Support

If issues persist:
1. Check Railway deployment logs
2. Run verification script: `python3 scripts/verify_backend_url.py`
3. Check browser console for errors (F12)
4. Review monitoring logs: `/tmp/umaja_health_monitor.log`
5. Check status page for patterns: `status.html`

---

## Summary

| Feature | File | Status | Impact |
|---------|------|--------|--------|
| Retry Logic | docs/index.html | ✅ Active | High |
| Environment Config | docs/config.js | ✅ Active | High |
| Status Page | docs/status.html | ✅ Available | Medium |
| Monitoring | scripts/monitor_health.py | ⚙️ Optional | Medium |

All features are production-ready and backward compatible.
