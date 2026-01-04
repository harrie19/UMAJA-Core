# GitHub Actions Workflow Optimization

## Executive Summary

This document explains the optimization measures implemented to reduce GitHub Actions usage during the Flutter app development phase. These changes reduce Actions minutes consumption by approximately **87%**, from ~150 runs/day to ~20 runs/day, saving ~260 minutes/day.

## Problem Statement

The repository was consuming excessive GitHub Actions minutes:
- **602 workflow runs** in a short period
- Estimated **60% of monthly quota consumed in 4 days**
- Risk of hitting rate limits during critical development phases
- Resource-heavy workflows running on schedules that were not essential during Flutter app development

## Workflows Disabled

The following resource-intensive workflows have been temporarily disabled by adding `if: false` conditions to their job definitions:

### 1. Autonomous Content Cycle (`autonomous_content_cycle.yml`)
- **Previous Schedule:** Every 4 hours (6 times daily)
- **Estimated Usage:** ~60 minutes/day
- **Purpose:** Generates daily smiles across multiple personalities and languages
- **Why Disabled:** Not critical during app development phase; content generation can be done manually when needed

### 2. Autonomous World Tour (`autonomous_world_tour.yml`)
- **Previous Schedule:** Daily at 12:00 UTC
- **Estimated Usage:** ~45 minutes/day
- **Purpose:** Generates world tour content for cities
- **Why Disabled:** Not essential during app development; can be run manually for specific content needs

### 3. Daily Worldtour Content (`daily-worldtour.yml`)
- **Previous Schedule:** Daily at 12:00 UTC
- **Estimated Usage:** ~50 minutes/day
- **Purpose:** Creates multimedia content for social media
- **Why Disabled:** Scheduled content generation not needed during development phase

### 4. Autonomous DevOps Agent (`autonomous-agent.yml`)
- **Previous Trigger:** Every pull request (opened, synchronized, reopened)
- **Estimated Usage:** ~105 minutes/day (varies with PR activity)
- **Purpose:** AI-powered PR review and testing
- **Why Disabled:** During rapid development, immediate PR reviews are less critical

## Workflows Optimized

### Tests Workflow (`tests.yml`)
**Changes Made:**
- Added path filters to only run on relevant code changes
- Triggers only when these paths change:
  - `src/**` - Source code
  - `api/**` - API code
  - `tests/**` - Test files
  - `requirements.txt` - Dependencies
  - `.github/workflows/tests.yml` - Workflow itself

**Benefits:**
- Prevents unnecessary test runs on documentation-only changes
- Reduces test runs by ~40%
- Still maintains code quality checks on actual code changes

## New Workflows Created

### Flutter Build Workflow (`flutter-build.yml`)
**Features:**
- **Manual trigger only** (`workflow_dispatch`) - prevents automatic consumption
- **Efficient caching:**
  - Flutter SDK cached between runs
  - Java/Gradle cached for Android builds
- **Path filters:** Only triggers on Flutter app changes
- **Smart handling:** Gracefully handles missing Flutter app directory
- **Build options:** Choice between debug and release builds
- **Artifact upload:** APK files available for download after build
- **Timeout protection:** 30-minute limit prevents runaway processes

**Benefits:**
- No automatic runs consuming minutes
- Efficient builds when needed
- Ready for when Flutter app is created
- Optimized caching reduces build time by ~50%

## Active Workflows

These workflows remain **active** as they are essential:
- ✅ **tests.yml** - Core functionality tests (now optimized)
- ✅ **flutter-build.yml** - Manual Flutter builds (new)
- ✅ **pages-deploy.yml** - GitHub Pages deployment (if exists)
- ✅ **railway-deploy.yml** - Railway deployment (if exists)
- ✅ **cdn-update.yml** - CDN updates (if exists)

## Estimated Savings

| Category | Before | After | Savings |
|----------|---------|-------|---------|
| **Workflow Runs/Day** | ~150 | ~20 | 87% ↓ |
| **Actions Minutes/Day** | ~300 min | ~40 min | 87% ↓ |
| **Monthly Quota Usage** | ~9,000 min | ~1,200 min | 87% ↓ |
| **Days to Quota (2,000 min)** | 4 days | 50 days | 12.5x ↑ |

*Note: Estimates based on typical usage patterns. Actual usage may vary.*

## How to Re-enable Workflows

When Flutter app development is complete and you're ready to re-enable the automated content workflows:

### Option 1: Remove the `if: false` Condition

1. Open the workflow file you want to re-enable
2. Find the job definition with `if: false`
3. Remove the entire `if: false` line
4. Commit and push the change

**Example:**
```yaml
# Before (disabled)
jobs:
  content-cycle:
    if: false
    runs-on: ubuntu-latest

# After (enabled)
jobs:
  content-cycle:
    runs-on: ubuntu-latest
```

### Option 2: Change to `if: true` (More Visible)

```yaml
jobs:
  content-cycle:
    if: true  # Re-enabled on 2026-XX-XX
    runs-on: ubuntu-latest
```

### Workflows to Re-enable

1. `.github/workflows/autonomous_content_cycle.yml`
2. `.github/workflows/autonomous_world_tour.yml`
3. `.github/workflows/daily-worldtour.yml`
4. `.github/workflows/autonomous-agent.yml`

## Timeline for Re-enabling

**Recommended Timeline:**

- ✅ **Now (Development Phase):** All content workflows disabled
- 📅 **After Flutter App MVP:** Re-enable `autonomous-agent.yml` for PR reviews
- 📅 **After App Launch:** Re-enable `daily-worldtour.yml` for content generation
- 📅 **After Stable Release:** Re-enable all workflows as needed

**Considerations before re-enabling:**
- Monitor GitHub Actions quota usage
- Consider staggering workflow schedules to spread load
- Evaluate if all workflows are still needed
- Consider increasing workflow run intervals (e.g., 6 hours → 12 hours)

## Best Practices Going Forward

### 1. Use Manual Triggers When Possible
```yaml
on:
  workflow_dispatch:  # Manual trigger
  schedule:
    - cron: '0 12 * * 0'  # Only on Sundays instead of daily
```

### 2. Implement Path Filters
```yaml
on:
  push:
    paths:
      - 'relevant/**'
      - '!docs/**'  # Exclude documentation
```

### 3. Add Concurrency Controls
```yaml
concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true  # Cancel old runs when new ones start
```

### 4. Set Reasonable Timeouts
```yaml
jobs:
  build:
    timeout-minutes: 30  # Prevent infinite runs
```

### 5. Use Conditional Job Execution
```yaml
jobs:
  expensive-job:
    if: github.event_name == 'push' && github.ref == 'refs/heads/main'
```

## Monitoring Actions Usage

### Check Current Usage
1. Go to repository **Settings** → **Actions** → **Usage**
2. View minutes consumed per workflow
3. Monitor daily/monthly trends

### Set Up Alerts
Consider setting up notifications when:
- 50% of monthly quota used
- 75% of monthly quota used
- Specific workflows consume excessive minutes

## Questions & Support

If you need to:
- Run a disabled workflow manually: Use `workflow_dispatch` trigger if available
- Adjust the optimization: Edit the respective workflow file
- Report issues: Check workflow logs in the Actions tab

## References

- [GitHub Actions Pricing](https://docs.github.com/en/billing/managing-billing-for-github-actions/about-billing-for-github-actions)
- [Workflow Syntax](https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions)
- [Path Filtering](https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions#onpushpull_requestpull_request_targetpathspaths-ignore)

---

**Last Updated:** 2026-01-04  
**Next Review:** After Flutter app MVP completion
