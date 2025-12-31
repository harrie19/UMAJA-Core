# Safety Guidelines - Best Practices

## 🔒 Core Safety Principles

### 1. Test First, Launch Later
**Always run dry-run before actual launch**

```bash
# ALWAYS start with dry run
python scripts/launch_world_tour.py --dry-run

# Review results carefully
cat output/safety/dry_run_*.json

# Only then go live
python scripts/launch_world_tour.py --go-live
```

### 2. Start Small, Scale Up
**Test with limited scope first**

```bash
# Test with 1 city, 1 language, 1 platform
python scripts/launch_world_tour.py \
  --cities "new_york" \
  --languages "en" \
  --platforms "tiktok" \
  --dry-run

# Then expand gradually
python scripts/launch_world_tour.py --count 5 --dry-run
python scripts/launch_world_tour.py --count 10 --dry-run
python scripts/launch_world_tour.py --go-live  # Full launch
```

### 3. Monitor Everything
**Active monitoring is mandatory**

```bash
# Launch with monitoring enabled
python scripts/launch_world_tour.py --go-live --monitor

# Check dashboard regularly
open output/monitoring/launch_dashboard.html

# Watch alert log
tail -f output/monitoring/alerts.jsonl
```

## 🚨 Critical Safety Checks

### Pre-Launch Checklist
- [ ] **Content validated** - QA passed with 95%+ success rate
- [ ] **Backups created** - Automatic backups in `output/safety/`
- [ ] **Team briefed** - Everyone knows their role
- [ ] **Emergency procedures tested** - Know how to stop if needed
- [ ] **Dry run completed** - Verified everything works
- [ ] **Confirmation ready** - Type 'I UNDERSTAND' correctly

### During Launch
- [ ] **Monitor first hour closely** - Catch issues early
- [ ] **Check engagement every 30 min** - Track metrics
- [ ] **Respond to negative comments** - Community management
- [ ] **Watch for API errors** - Platform issues
- [ ] **Track sentiment** - Overall community reaction

### Post-Launch
- [ ] **Review all metrics** - Analyze performance
- [ ] **Document learnings** - What worked, what didn't
- [ ] **Thank community** - Acknowledge participation
- [ ] **Plan improvements** - Iterate for next time

## 🛡️ Content Safety

### Cultural Sensitivity
**Always check cultural appropriateness**

```python
from quality_assurance import QualityAssurance

qa = QualityAssurance()

# Check each language/culture
for lang in ['ar', 'ja', 'zh']:
    result = qa.cultural_safety_check(content, lang)
    if not result['safe']:
        print(f"⚠️  Issues with {lang}: {result['concerns']}")
```

**Cultural Guidelines:**
- **Arabic/Middle East**: Avoid alcohol, pork, religious topics
- **Asian Cultures**: Avoid direct confrontation, maintain harmony
- **European**: Be aware of historical sensitivities
- **Latin America**: Family-focused, warm tone

### Platform Compliance
**Follow platform-specific rules**

| Platform | Key Rules |
|----------|-----------|
| TikTok | No spam, 150 char limit, authentic content |
| Instagram | No misleading content, proper hashtags |
| YouTube | Community guidelines, copyright respect |

### Prohibited Content
❌ **Never include:**
- Hate speech or discrimination
- Violence or graphic content
- Spam or misleading information
- Copyrighted material without permission
- Political or controversial topics
- Religious criticism
- Personal attacks

✅ **Always include:**
- Positive, uplifting messages
- Community engagement questions
- Cultural respect
- Authenticity
- Proper attribution

## 🔐 Technical Safety

### Rate Limiting
**Respect platform limits**

```python
# Platform rate limits
RATE_LIMITS = {
    'tiktok': {'posts_per_day': 100, 'calls_per_hour': 1000},
    'instagram': {'posts_per_hour': 25, 'calls_per_hour': 200},
    'youtube': {'videos_per_day': 50, 'calls_per_hour': 100}
}

# Implement delays
import time
time.sleep(2)  # 2 seconds between API calls
```

### API Security
**Protect credentials**

```bash
# Use environment variables
export TIKTOK_API_KEY="your_key_here"
export INSTAGRAM_ACCESS_TOKEN="your_token"

# Never commit credentials
echo ".env" >> .gitignore
echo "*.key" >> .gitignore
```

### Backup Strategy
**Automated backups before every launch**

```python
from safety_system import SafetySystem

safety = SafetySystem()

# Automatic backup
safety._create_backup(launch_data)

# Verify backup exists
import os
backups = os.listdir('output/safety/')
print(f"Backups: {len([b for b in backups if 'backup' in b])}")
```

## 🚑 Emergency Procedures

### Emergency Stop
**If something goes wrong, stop immediately**

```python
from safety_system import SafetySystem

safety = SafetySystem()

# PANIC BUTTON
safety.emergency_stop("Reason for stop")

# Verify stopped
status = safety.get_safety_status()
print(f"Emergency stops: {status['emergency_stops']}")
```

**When to emergency stop:**
- Critical content error detected
- Severe negative sentiment (>50%)
- Platform policy violation
- Technical failure affecting posts
- Security breach
- Community crisis

### Rollback Procedure
**If posts need to be removed**

```python
# Step 1: Emergency stop
safety.emergency_stop("Content issue - initiating rollback")

# Step 2: Rollback
rollback_result = safety.rollback_capability('launch_20260101')

# Step 3: Verify
print(f"Rollback status: {rollback_result['status']}")

# Step 4: Communicate
# - Issue statement to community
# - Explain what happened
# - Share corrective actions
```

### Crisis Communication Template
```
🙏 Important Update

We've identified an issue with today's content and have 
temporarily paused our posts. 

What happened: [Brief explanation]
What we're doing: [Corrective action]
What's next: [Timeline]

We apologize for any confusion and appreciate your patience 
and understanding. Your feedback helps us improve! 😊

Questions? Reply below or DM us.
```

## 📊 Monitoring Best Practices

### Real-Time Monitoring
**Set up continuous monitoring**

```python
from launch_day_monitor import LaunchDayMonitor

monitor = LaunchDayMonitor()

# Create dashboard
dashboard = monitor.create_realtime_dashboard(launch_data)
print(f"Monitor at: {dashboard}")

# Set alert thresholds
ALERT_THRESHOLDS = {
    'viral': 100000,  # Views for viral alert
    'negative_sentiment': 0.3,  # >30% negative triggers alert
    'failure_rate': 0.05  # >5% failures triggers alert
}
```

### Metric Tracking
**Key metrics to watch**

1. **Engagement Rate** = (Likes + Comments + Shares) / Views
   - Target: >5%
   - Alert if: <2%

2. **Sentiment Score** = Positive Comments / Total Comments
   - Target: >80%
   - Alert if: <70%

3. **Success Rate** = Successful Posts / Total Posts
   - Target: >95%
   - Alert if: <90%

4. **Viral Coefficient** = Shares / Views
   - Target: >0.02
   - Good sign: >0.05

### Alert Response Times
| Alert Type | Response Time | Action |
|------------|---------------|--------|
| Viral Post | 5 minutes | Boost, engage comments |
| Negative Sentiment | 10 minutes | Investigate, prepare response |
| Technical Failure | Immediate | Emergency stop if needed |
| Milestone | 15 minutes | Celebrate, thank community |

## 👥 Team Safety

### Role Assignment
**Clear responsibilities prevent chaos**

1. **Launch Lead**
   - Overall coordination
   - Decision making
   - Communication

2. **Content Monitor**
   - Watch posts going live
   - Track quality issues
   - Report problems

3. **Community Manager**
   - Respond to comments
   - Manage sentiment
   - Engage community

4. **Technical Lead**
   - Handle system issues
   - Monitor APIs
   - Emergency procedures

5. **Analyst**
   - Track metrics
   - Generate reports
   - Identify trends

### Communication Protocol
```
Severity Levels:

🟢 INFO: Normal operations
  - Post updates in team chat
  - No immediate action needed

🟡 WARNING: Attention needed
  - Alert team in chat
  - Monitor closely
  - Prepare response

🟠 URGENT: Action required
  - @ mention relevant people
  - Take corrective action
  - Document in log

🔴 CRITICAL: Emergency
  - Alert all team members
  - Emergency stop if needed
  - Immediate response
```

## 📝 Documentation Requirements

### Mandatory Logs
1. **Safety Log** - All confirmations and stops
2. **Monitoring Log** - Metrics and alerts
3. **Issue Log** - Problems encountered
4. **Action Log** - Decisions made

### Post-Mortem Template
```markdown
# Launch Post-Mortem: [Date]

## Summary
- Total posts: 
- Success rate:
- Total reach:
- Issues encountered:

## What Went Well
1. 
2. 
3. 

## What Went Wrong
1. 
2. 
3. 

## Corrective Actions
1. 
2. 
3. 

## Lessons Learned
1. 
2. 
3. 

## Recommendations
1. 
2. 
3. 
```

## 🎯 Success Criteria

Launch is safe and successful when:
- ✅ Zero critical issues
- ✅ 95%+ posts successful
- ✅ 80%+ positive sentiment
- ✅ All backups created
- ✅ No emergency stops needed
- ✅ Team coordination smooth
- ✅ Community reaction positive
- ✅ All documentation complete

## ⚠️ Red Flags

**Stop and reassess if:**
- QA success rate <90%
- Negative sentiment >30%
- API failure rate >10%
- Team member unavailable
- Unclear emergency procedures
- No backups created
- Untested dry-run
- Community concerns raised

---

**Remember:** Safety first, always. Better to delay than to launch with issues! 🔒😊
