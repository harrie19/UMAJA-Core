# Troubleshooting Guide

## 🔍 Common Issues and Solutions

### Content Generation Issues

#### Issue: Content generation fails for some cities
**Symptoms:**
```
ERROR: Failed to generate content for tokyo: KeyError 'topics'
```

**Causes:**
- Missing city data in `data/worldtour_cities.json`
- Corrupted city data
- API timeout

**Solutions:**
1. Check city data exists:
   ```python
   from worldtour_generator import WorldtourGenerator
   gen = WorldtourGenerator()
   city = gen.get_city('tokyo')
   print(city)
   ```

2. Regenerate cities database:
   ```python
   gen._initialize_default_cities()
   ```

3. Skip problematic cities:
   ```bash
   python scripts/launch_world_tour.py --cities "new_york,london" --dry-run
   ```

#### Issue: Quality assurance fails
**Symptoms:**
```
WARNING: QA failed - 50 issues found
safe_to_launch: False
```

**Causes:**
- Content too long for platform
- Missing hashtags
- Sensitive terms detected

**Solutions:**
1. Review issues:
   ```python
   from quality_assurance import QualityAssurance
   qa = QualityAssurance()
   results = qa.validate_content_batch(batch)
   print(qa.get_quality_report(results))
   ```

2. Auto-fix issues:
   ```python
   fixed_batch = qa.auto_fix_issues(batch, results['issues'])
   ```

3. Manual review of sensitive content

#### Issue: Translation errors
**Symptoms:**
```
WARNING: Translation for 'ar' appears to be gibberish
```

**Causes:**
- Translation API unavailable
- Unsupported language
- Character encoding issues

**Solutions:**
1. Use English fallback:
   ```bash
   python scripts/launch_world_tour.py --languages "en" --dry-run
   ```

2. Verify language support:
   ```python
   supported_languages = ['en', 'es', 'fr', 'de', 'ja', 'zh', 'ar', 'pt']
   ```

3. Check translation service status

### Scheduling Issues

#### Issue: Incorrect timezone calculations
**Symptoms:**
```
Posts scheduled at wrong local times
Tokyo post at 3am local time (not optimal)
```

**Causes:**
- Wrong timezone offset
- DST not considered
- Date calculation error

**Solutions:**
1. Verify timezone data:
   ```python
   from smart_scheduler import SmartScheduler
   scheduler = SmartScheduler()
   print(scheduler.CITY_TIMEZONES['tokyo'])  # Should be 9
   ```

2. Recalculate optimal times:
   ```python
   optimal = scheduler.calculate_optimal_time('tokyo', 'tiktok')
   print(f"Optimal time: {optimal}")
   ```

3. Use backup schedule:
   ```python
   backup = scheduler.calculate_backup_schedule(schedule)
   ```

#### Issue: Posts scheduled too close together
**Symptoms:**
```
WARNING: 10 posts scheduled within same hour
May trigger spam detection
```

**Causes:**
- Insufficient staggering
- Too many cities in same timezone
- Schedule optimization failed

**Solutions:**
1. Increase stagger time in `smart_scheduler.py`:
   ```python
   current_offset += 2  # Change to 3 or 4
   ```

2. Optimize schedule:
   ```python
   optimized = scheduler.optimize_for_engagement(schedule)
   ```

3. Reduce concurrent platforms

### Performance Issues

#### Issue: Generation taking too long
**Symptoms:**
```
INFO: Generating 50 cities...
[Still running after 30 minutes]
```

**Causes:**
- Parallel processing disabled
- Cache not working
- Too many workers

**Solutions:**
1. Enable parallel processing:
   ```python
   batch = generator.generate_city_batch(
       cities=cities,
       parallel=True  # Ensure this is True
   )
   ```

2. Adjust worker count:
   ```python
   generator = BatchContentGenerator(max_workers=10)
   ```

3. Clear and rebuild cache:
   ```python
   from performance_optimizer import PerformanceOptimizer
   optimizer = PerformanceOptimizer()
   optimizer.clear_cache()
   ```

#### Issue: Cache not working
**Symptoms:**
```
Cache hit rate: 0%
Everything re-generated every time
```

**Causes:**
- Cache directory not writable
- Cache files corrupted
- TTL expired

**Solutions:**
1. Check cache directory:
   ```bash
   ls -la output/cache/
   chmod 755 output/cache/
   ```

2. Verify cache operations:
   ```python
   optimizer.cache_everything('test', 'value')
   result = optimizer.cache_everything('test')
   print(f"Cache test: {result}")
   ```

3. Increase TTL:
   ```python
   optimizer.cache_everything('key', 'value', ttl=7200)  # 2 hours
   ```

### Monitoring Issues

#### Issue: Dashboard not updating
**Symptoms:**
```
Dashboard shows old data
Last updated: 2 hours ago
```

**Causes:**
- Browser cache
- Dashboard not refreshing
- Monitoring stopped

**Solutions:**
1. Hard refresh browser (Ctrl+Shift+R)

2. Restart monitoring:
   ```python
   from launch_day_monitor import LaunchDayMonitor
   monitor = LaunchDayMonitor()
   dashboard = monitor.create_realtime_dashboard(launch_data)
   ```

3. Check monitoring logs:
   ```bash
   tail -f output/monitoring/metrics_*.json
   ```

#### Issue: Alerts not firing
**Symptoms:**
```
Post went viral but no alert received
150k views, no notification
```

**Causes:**
- Alert thresholds too high
- Alert system disabled
- Notification service down

**Solutions:**
1. Check alert configuration:
   ```python
   monitor.send_alerts('viral_post', {
       'city': 'tokyo',
       'views': 150000
   })
   ```

2. Review alert log:
   ```bash
   cat output/monitoring/alerts.jsonl
   ```

3. Lower thresholds for testing

### Safety System Issues

#### Issue: Cannot confirm launch
**Symptoms:**
```
Type 'I UNDERSTAND' to continue:
> I UNDERSTAND
Action cancelled
```

**Causes:**
- Extra spaces in input
- Wrong capitalization
- Input encoding issue

**Solutions:**
1. Type exactly: `I UNDERSTAND` (no extra spaces)

2. Copy-paste the exact phrase

3. Use programmatic confirmation:
   ```python
   # For automated deployments
   # (Use with extreme caution!)
   confirmed = True
   ```

#### Issue: Emergency stop not working
**Symptoms:**
```
Called emergency_stop() but posts still going live
```

**Causes:**
- Posts already scheduled on platforms
- API delay
- Stop not propagated

**Solutions:**
1. Verify stop executed:
   ```python
   stop_status = safety.emergency_stop('test')
   print(stop_status['activated'])  # Should be True
   ```

2. Manual platform stops:
   - TikTok: Delete scheduled posts
   - Instagram: Cancel scheduled content
   - YouTube: Remove from schedule

3. Check safety log:
   ```bash
   tail -f output/safety/safety_log.jsonl
   ```

### API & Integration Issues

#### Issue: Platform API errors
**Symptoms:**
```
ERROR: TikTok API returned 429 (Rate Limited)
ERROR: Instagram API returned 401 (Unauthorized)
```

**Causes:**
- Rate limits exceeded
- Invalid credentials
- API changes

**Solutions:**
1. Check rate limits:
   - TikTok: 100 posts/day
   - Instagram: 25 posts/hour
   - YouTube: 50 videos/day

2. Verify credentials:
   ```bash
   cat .env | grep API_KEY
   ```

3. Use batch API calls:
   ```python
   optimizer.batch_api_calls(calls, batch_size=10)
   ```

4. Implement exponential backoff

#### Issue: Database connection errors
**Symptoms:**
```
ERROR: Could not load cities database
FileNotFoundError: data/worldtour_cities.json
```

**Causes:**
- Missing data file
- Permission issues
- Corrupted database

**Solutions:**
1. Check file exists:
   ```bash
   ls -la data/worldtour_cities.json
   ```

2. Regenerate database:
   ```python
   from worldtour_generator import WorldtourGenerator
   gen = WorldtourGenerator()
   gen._initialize_default_cities()
   ```

3. Restore from backup:
   ```bash
   cp output/safety/backup_*.json data/worldtour_cities.json
   ```

## 🔧 Debugging Tools

### Enable Debug Logging
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Inspect Content Batch
```python
import json
with open('output/world_tour/global_launch_20260101.json', 'r') as f:
    data = json.load(f)
print(json.dumps(data, indent=2))
```

### Check System Status
```python
# Check all components
from world_tour_automation import WorldTourAutomation
automation = WorldTourAutomation()

# Verify batch generator
batch_gen = automation.batch_generator
print(f"Batch generator ready: {batch_gen is not None}")

# Verify scheduler
scheduler = automation.scheduler
print(f"Scheduler ready: {scheduler is not None}")

# Verify QA
qa = automation.qa_system
print(f"QA system ready: {qa is not None}")
```

### Performance Profiling
```python
from performance_optimizer import PerformanceOptimizer
optimizer = PerformanceOptimizer()

# Benchmark
benchmark = optimizer.benchmark_performance(
    task_func=your_function,
    task_data=your_data,
    max_workers=10
)
print(benchmark)
```

## 📞 Getting Help

### Check Logs
1. **Safety logs**: `output/safety/safety_log.jsonl`
2. **Monitoring logs**: `output/monitoring/alerts.jsonl`
3. **Metrics**: `output/monitoring/metrics_*.json`

### Run Diagnostics
```bash
# System check
python scripts/launch_world_tour.py --dry-run --count 1

# Component tests
python src/batch_content_generator.py
python src/smart_scheduler.py
python src/quality_assurance.py
```

### Community Support
- GitHub Issues: Report bugs
- Documentation: Review guides
- Team Chat: Ask questions

## ⚡ Quick Fixes

| Problem | Quick Fix |
|---------|-----------|
| Generation slow | Enable parallel: `parallel=True` |
| QA failing | Auto-fix: `qa.auto_fix_issues()` |
| Wrong times | Check timezones in `smart_scheduler.py` |
| Cache issues | Clear cache: `optimizer.clear_cache()` |
| API errors | Reduce batch size, add delays |
| Dashboard broken | Hard refresh browser |
| Emergency needed | `safety.emergency_stop()` |

---

**Remember:** Most issues can be solved with dry-run testing first! 🧪
