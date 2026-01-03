# 🐛 Known Issues & Workarounds

*Last Updated: 2026-01-03*

---

## ✅ RESOLVED

### Backend URL Mismatch (CRITICAL)
- **Issue:** Dashboard connected to wrong Railway URL
- **Status:** ✅ FIXED in PR #52
- **Date:** 2026-01-03

---

## 🟡 ACTIVE (Non-Critical)

### 1. Personality Naming Inconsistency
**Severity:** Medium (Legal Risk)

**Problem:** 
Code uses two different naming systems:
- OLD: `john_cleese`, `c3po`, `robin_williams` (celebrity names)
- NEW: `the_professor`, `the_worrier`, `the_enthusiast` (generic)

**Files Affected:**
- `src/worldtour_generator.py` (OLD)
- `api/simple_server.py` (MIXED)
- `src/personality_engine.py` (NEW)

**Impact:** Potential trademark issues, confusion

**Workaround:** System works, but naming should be unified

**Planned Fix:** Global search-replace in Phase 3

---

### 2. PR Management Overload
**Severity:** Medium (Maintenance)

**Problem:** 27 open PRs with significant overlap

**Analysis:**
- PR #52 & #53: Duplicates (both fix URL)
- Many deployment PRs overlap (similarity >85%)
- Copilot Agent creates too many PRs

**Impact:** Hard to track what's active/needed

**Workaround:** Focus on this PR (#52), ignore others

**Planned Fix:** Close duplicates, consolidate

---

### 3. World Tour Progress
**Severity:** Low (By Design)

**Status:** 8/59 cities visited (13.6%)

**Not a bug** - this is expected progress! System is designed for gradual rollout.

**Next Steps:** Continue daily city visits

---

## 📋 FEATURE REQUESTS (Future)

### 1. Multi-Language UI
- Currently: Backend supports 8 languages
- Missing: Frontend UI translation
- Priority: Medium
- Effort: 2-3 days

### 2. Analytics Dashboard
- Currently: No usage tracking
- Desired: User engagement metrics
- Priority: Medium
- Effort: 1 week

### 3. Social Media Automation
- Currently: Manual posting
- Desired: Auto-post to TikTok/Instagram
- Priority: High
- Effort: 2 weeks (API approval time)

---

## 🔍 HOW TO REPORT ISSUES

1. Check this file first (known issues?)
2. Check `docs/TROUBLESHOOTING.md` (common problems?)
3. Search existing GitHub Issues
4. If new: Create issue with template

**Email:** Umaja1919@googlemail.com

---

**Transparency is a Bahá'í principle. We document everything. 🕊️**
