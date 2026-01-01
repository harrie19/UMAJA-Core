# 🚀 UMAJA-Core GO LIVE Checklist - January 1, 2026

**Contact:** Umaja1919@googlemail.com

## Pre-Launch Verification

### ✅ Infrastructure (P0 - Critical)
- [x] Test suite passing (all 2 tests green)
- [x] Dependencies security checked (no vulnerabilities)
- [x] Backend `/health` endpoint functional
- [x] GitHub Pages workflow configured
- [ ] Railway backend deployed (manual step required)

### ✅ Content (P1 - Required for Day 1)
- [x] All 24 Day 1 smile files exist (3 archetypes × 8 languages)
- [x] CDN manifest.json accurate
- [x] Sample files validated (Dreamer, Warrior, Healer)

### ✅ Documentation (P2 - Launch Communication)
- [x] Live status badges in README.md
- [x] STATUS_LIVE.md created with system status
- [x] Contact email verified (Umaja1919@googlemail.com)
- [x] Railway deployment guide updated
- [x] Deployment workflows documented

---

## Deployment Steps

### Step 1: Enable GitHub Pages (REQUIRED)
**Owner action required:**
1. Go to: https://github.com/harrie19/UMAJA-Core/settings/pages
2. Under "Build and deployment":
   - Source: **Deploy from a branch**
   - Branch: **main** 
   - Folder: **/docs**
3. Click **Save**
4. Wait 2-3 minutes for first deployment
5. Verify at: https://harrie19.github.io/UMAJA-Core/

### Step 2: Deploy Backend to Railway (RECOMMENDED: Web UI)
**Choose Option A OR Option B:**

#### Option A: Railway Web UI (RECOMMENDED - No secrets needed)
1. Visit https://railway.app
2. Click "New Project"
3. Select "Deploy from GitHub"
4. Choose `harrie19/UMAJA-Core` repository
5. Railway auto-detects `railway.json` configuration
6. Add environment variables:
   ```
   ENVIRONMENT=production
   DEBUG=False
   WORLDTOUR_MODE=true
   SALES_ENABLED=false
   USE_OFFLINE_TTS=true
   PORT=5000
   ```
7. Click "Deploy"
8. Copy the generated Railway URL (e.g., `https://umaja-core-production.up.railway.app`)
9. Update `docs/index.html` line 12 with your Railway URL:
   ```javascript
   const BACKEND_URL = 'https://your-app.railway.app'; // Replace this!
   ```
10. Commit and push the change

#### Option B: GitHub Actions (Requires RAILWAY_TOKEN secret)
1. Get Railway token: https://railway.app/account/tokens
2. Add to GitHub: Settings → Secrets → Actions → New repository secret
   - Name: `RAILWAY_TOKEN`
   - Value: [your-token]
3. Trigger workflow: Actions → "🚂 Deploy to Railway" → Run workflow
4. Follow steps 8-10 from Option A

### Step 3: Verify Deployment
Run these checks:

```bash
# 1. Check GitHub Pages
curl https://harrie19.github.io/UMAJA-Core/

# 2. Check backend health
curl https://your-railway-app.railway.app/health

# 3. Check API endpoint
curl https://your-railway-app.railway.app/api/daily-smile

# 4. Check CDN access
curl https://raw.githubusercontent.com/harrie19/UMAJA-Core/main/cdn/smiles/Dreamer/en/1.json
```

Expected responses:
- GitHub Pages: HTML page loads
- Health endpoint: `{"status": "healthy", ...}`
- API endpoint: Daily smile JSON
- CDN: Day 1 smile JSON

---

## Post-Launch Validation

### Functional Testing
- [ ] Open https://harrie19.github.io/UMAJA-Core/
- [ ] Complete archetype quiz (select answers)
- [ ] Verify Day 1 smile displays correctly
- [ ] Test on mobile device
- [ ] Test on different browser
- [ ] Check console for errors (F12)

### System Health
- [ ] GitHub Actions workflows all green
- [ ] Railway logs show no errors
- [ ] No 404 errors on CDN files
- [ ] Backend responds within 500ms

### Monitoring (First 24 hours)
- [ ] Check Railway dashboard every 4 hours
- [ ] Monitor GitHub Actions runs
- [ ] Review any error reports
- [ ] Test from different locations/networks

---

## Known Limitations - Day 1

### Expected Behavior
✅ **What Works:**
- Frontend loads instantly from GitHub Pages
- Archetype quiz functional
- Day 1 smiles available in 8 languages
- CDN delivers content via GitHub Raw
- Health check endpoint responds

⚠️ **Known Limitations:**
- Only Day 1 content available (Day 2+ coming daily)
- Backend API optional (CDN is primary source)
- No user accounts/profiles yet
- No push notifications
- Railway may need 30-60 seconds to wake up (free tier)

### Fallback Strategy
If backend is unavailable:
1. Frontend automatically uses CDN (GitHub Raw)
2. Hardcoded fallback smile as last resort
3. System remains functional without backend

---

## Emergency Rollback

If critical issues occur:

### Quick Disable
```bash
# Disable GitHub Pages
# Go to: Settings → Pages → Source: None

# Pause Railway service
# Go to: Railway Dashboard → Service → Settings → Pause
```

### Revert Code
```bash
# Revert to last stable commit
git revert HEAD
git push origin main
```

---

## Success Criteria

**Declare GO LIVE when ALL checked:**
- [x] Tests passing (green CI)
- [x] Documentation complete
- [ ] GitHub Pages live and accessible
- [ ] Backend deployed and healthy (OR CDN fallback confirmed working)
- [ ] Day 1 smiles accessible
- [ ] Manual smoke test passed
- [ ] No critical errors in logs

---

## Contact & Support

**Mission Owner:** Marek Grischa Engel  
**Email:** Umaja1919@googlemail.com  
**Repository:** https://github.com/harrie19/UMAJA-Core  

For issues:
1. Check Railway logs: https://railway.app
2. Check GitHub Actions: https://github.com/harrie19/UMAJA-Core/actions
3. Review STATUS_LIVE.md for system status
4. Open GitHub issue with error details

---

**🕊️ "Let deeds, not words, be your adorning." — Bahá'u'lláh**

**This is Day 1. Let's bring smiles to 8 billion people. 🌍😊**
