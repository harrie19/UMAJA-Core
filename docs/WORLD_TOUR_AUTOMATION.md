# World Tour Automation - Complete Guide

## 🌍 Overview

The UMAJA World Tour Automation Suite enables one-command generation and deployment of content for 50 cities × 8 languages × 3 platforms = 1200 posts.

## 🚀 Quick Start

### Basic Launch
```bash
# Dry run (test mode - no actual posting)
python scripts/launch_world_tour.py --dry-run

# Full global launch
python scripts/launch_world_tour.py --go-live

# Launch with monitoring
python scripts/launch_world_tour.py --go-live --monitor
```

### Custom Launch
```bash
# Specific cities
python scripts/launch_world_tour.py --cities "new_york,london,tokyo" --dry-run

# Specific languages
python scripts/launch_world_tour.py --languages "en,es,fr" --dry-run

# Specific platforms
python scripts/launch_world_tour.py --platforms "tiktok,instagram" --dry-run

# Custom date
python scripts/launch_world_tour.py --date "2026-01-01" --dry-run

# Limited count for testing
python scripts/launch_world_tour.py --count 5 --dry-run
```

## 📦 Components

### 1. World Tour Automation (Orchestrator)
**File:** `src/world_tour_automation.py`

Main orchestrator that coordinates all components.

```python
from world_tour_automation import WorldTourAutomation

automation = WorldTourAutomation()

# Generate content for global launch
launch_data = automation.generate_global_launch(
    launch_date=datetime(2026, 1, 1),
    cities=['new_york', 'london', 'tokyo'],
    languages=['en', 'es'],
    platforms=['tiktok', 'instagram']
)

# Schedule posts optimally
schedule = automation.schedule_optimal_posts(
    content_batch=launch_data['content_batch'],
    launch_date=datetime(2026, 1, 1)
)

# Monitor launch day
monitoring = automation.monitor_launch_day(launch_data)
```

**Key Features:**
- One-command content generation
- Automatic scheduling
- QA integration
- Launch monitoring

### 2. Batch Content Generator
**File:** `src/batch_content_generator.py`

Mass-produces content with parallel processing.

```python
from batch_content_generator import BatchContentGenerator

generator = BatchContentGenerator(max_workers=10)

# Generate for multiple cities
batch = generator.generate_city_batch(
    cities=['new_york', 'london', 'tokyo'],
    languages=['en', 'es'],
    platforms=['tiktok', 'instagram'],
    parallel=True
)

# Generate variations for A/B testing
variations = generator.generate_with_variations('new_york', count=3)
```

**Key Features:**
- Parallel processing (10× faster)
- Multiple personality variations
- Language translations
- Platform adaptation
- Quality scoring

### 3. Smart Scheduler
**File:** `src/smart_scheduler.py`

Timezone-aware intelligent scheduling.

```python
from smart_scheduler import SmartScheduler

scheduler = SmartScheduler()

# Calculate optimal posting time
optimal_time = scheduler.calculate_optimal_time(
    city='tokyo',
    platform='tiktok'
)

# Create global schedule
schedule = scheduler.create_global_schedule(content_batch)

# Handle failures automatically
retry_schedule = scheduler.handle_failures_automatically(failed_posts)
```

**Key Features:**
- Timezone-aware scheduling
- Platform-specific peak times
- 24/7 rolling schedule
- Automatic retry on failure
- Backup schedules

### 4. Quality Assurance
**File:** `src/quality_assurance.py`

Ensures every post is perfect before going live.

```python
from quality_assurance import QualityAssurance

qa = QualityAssurance()

# Validate content batch
results = qa.validate_content_batch(content_batch)

# Cultural safety check
safety = qa.cultural_safety_check(content, 'ar')

# Auto-fix issues
fixed_batch = qa.auto_fix_issues(content_batch, results['issues'])
```

**Key Features:**
- Text length validation
- Cultural sensitivity checks
- Hashtag validation
- Automatic fixes
- Detailed reporting

### 5. Launch Day Monitor
**File:** `src/launch_day_monitor.py`

Real-time monitoring and dashboards.

```python
from launch_day_monitor import LaunchDayMonitor

monitor = LaunchDayMonitor()

# Create dashboard
dashboard_url = monitor.create_realtime_dashboard(launch_data)

# Track metrics
metrics = monitor.track_metrics(launch_data)

# Send alerts
monitor.send_alerts('viral_post', {
    'city': 'tokyo',
    'views': 150000
})
```

**Key Features:**
- Real-time HTML dashboard
- Live metrics tracking
- Engagement monitoring
- Alert system
- Progress reports

### 6. Compilation Generator
**File:** `src/compilation_generator.py`

Auto-creates highlight reels and recaps.

```python
from compilation_generator import CompilationGenerator

compiler = CompilationGenerator()

# Create launch day recap
recap = compiler.create_launch_day_recap('2026-01-01', content_batch)

# Create top moments
top_moments = compiler.create_top_moments(days=7, content_batch)
```

**Key Features:**
- Launch day recaps
- Top 10 compilations
- Language-specific compilations
- Platform-optimized output

### 7. Performance Optimizer
**File:** `src/performance_optimizer.py`

Makes generation 10× faster.

```python
from performance_optimizer import PerformanceOptimizer

optimizer = PerformanceOptimizer()

# Parallel processing
results = optimizer.parallel_processing(tasks, task_func, max_workers=10)

# Caching
optimizer.cache_everything('key', 'value')
cached = optimizer.cache_everything('key')

# Batch API calls
results = optimizer.batch_api_calls(api_calls, batch_size=10)
```

**Key Features:**
- Parallel processing
- Intelligent caching
- API batching
- Performance benchmarking

### 8. Safety System
**File:** `src/safety_system.py`

Prevents disasters with safety checks.

```python
from safety_system import SafetySystem

safety = SafetySystem()

# Require confirmation
confirmed = safety.require_confirmation('global_launch', details)

# Dry run mode
simulation = safety.dry_run_mode('action', data)

# Emergency stop
safety.emergency_stop('reason')

# Rollback
safety.rollback_capability('launch_id')
```

**Key Features:**
- Confirmation prompts
- Dry run mode
- Emergency stop button
- Rollback capability
- Safety validation

## 🔄 Workflow

### Standard Launch Process

1. **Preparation**
   ```bash
   # Test with dry run first
   python scripts/launch_world_tour.py --date "2026-01-01" --dry-run
   ```

2. **Review**
   - Check simulation results
   - Verify content quality
   - Confirm scheduling

3. **Launch**
   ```bash
   # Execute actual launch
   python scripts/launch_world_tour.py --date "2026-01-01" --go-live
   ```

4. **Monitor**
   ```bash
   # Launch with monitoring
   python scripts/launch_world_tour.py --date "2026-01-01" --go-live --monitor
   ```

5. **Track & Respond**
   - Monitor dashboard
   - Track engagement
   - Respond to comments

## 📊 Output Files

### Content & Schedule
- `output/world_tour/global_launch_YYYYMMDD.json` - Complete launch data
- `output/world_tour/*.json` - Individual content files

### Monitoring
- `output/monitoring/launch_dashboard.html` - Live dashboard
- `output/monitoring/metrics_*.json` - Metrics snapshots
- `output/monitoring/alerts.jsonl` - Alert log

### Safety
- `output/safety/safety_log.jsonl` - Safety action log
- `output/safety/dry_run_*.json` - Dry run results
- `output/safety/backup_*.json` - Launch backups

### Compilations
- `output/compilations/recap_*.json` - Launch recaps
- `output/compilations/top_moments_*.json` - Top content

### Cache
- `output/cache/*.json` - Cached content

## 🎯 Best Practices

### Testing
1. **Always dry-run first**
   ```bash
   python scripts/launch_world_tour.py --dry-run
   ```

2. **Test with small batch**
   ```bash
   python scripts/launch_world_tour.py --count 5 --dry-run
   ```

3. **Verify one city/language/platform**
   ```bash
   python scripts/launch_world_tour.py --cities "new_york" --languages "en" --platforms "tiktok" --dry-run
   ```

### Safety
1. **Backups are automatic** - Check `output/safety/backup_*.json`
2. **Emergency stop available** - Run safety.emergency_stop()
3. **Rollback possible** - Use safety.rollback_capability()

### Performance
1. **Use caching** - Speeds up re-runs
2. **Parallel processing** - Enabled by default
3. **Clear cache periodically** - `optimizer.clear_cache()`

### Monitoring
1. **Always monitor launches** - Use `--monitor` flag
2. **Check dashboard regularly** - Open generated HTML
3. **Respond to alerts** - Set up notification system

## 🔧 Configuration

### Environment Variables
```bash
# Optional configuration
export UMAJA_MAX_WORKERS=10
export UMAJA_CACHE_TTL=3600
export UMAJA_OUTPUT_DIR="output"
```

### Cities
Default: All 50+ cities in `data/worldtour_cities.json`

### Languages
Default: `['en', 'es', 'fr', 'de', 'ja', 'zh', 'ar', 'pt']`

### Platforms
Default: `['tiktok', 'instagram', 'youtube']`

## 📈 Metrics & Analytics

### Key Metrics
- **Total Reach**: Combined views across platforms
- **Engagement Rate**: Likes + comments + shares / views
- **Viral Posts**: Posts with >100k views
- **Sentiment**: Positive vs negative comments
- **Share Velocity**: Shares per hour

### Accessing Metrics
```python
from launch_day_monitor import LaunchDayMonitor

monitor = LaunchDayMonitor()
metrics = monitor.track_metrics(launch_data)

print(f"Total Reach: {metrics['total_reach']}")
print(f"Viral Posts: {metrics['viral_posts']}")
```

## 🚨 Troubleshooting

See `docs/TROUBLESHOOTING.md` for common issues and solutions.

## 🔐 Safety Guidelines

See `docs/SAFETY_GUIDELINES.md` for best practices and safety protocols.

## 📋 Launch Day Checklist

See `docs/LAUNCH_DAY_CHECKLIST.md` for step-by-step launch guide.

## 🤝 Support

For issues or questions:
1. Check documentation
2. Review troubleshooting guide
3. Open GitHub issue
4. Contact team

## 📝 License

MIT License - See LICENSE file for details

---

**Remember:** Test with `--dry-run` first! 🧪
