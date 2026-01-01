#!/usr/bin/env python3
"""
Smart Merge Strategy with Mergeable State Retry Logic
"""

import os
import re
import sys
import time
from typing import Tuple
from github import Github

def can_merge(pr, max_retries=5, wait_seconds=10) -> Tuple[bool, str]:
    """
    Check if PR is mergeable with retry logic for UNKNOWN state
    Returns: (can_merge, reason)
    """
    for attempt in range(max_retries):
        # Refresh PR state from API
        pr.update()
        
        if pr.mergeable is True:
            return True, "PR is mergeable"
        
        elif pr.mergeable is False:
            # Check why it's not mergeable
            if pr.mergeable_state == 'dirty':
                return False, "PR has merge conflicts"
            elif pr.mergeable_state == 'blocked':
                return False, "PR is blocked by required checks or reviews"
            else:
                return False, f"PR not mergeable: {pr.mergeable_state}"
        
        else:  # mergeable is None (UNKNOWN state)
            print(f"⏳ PR #{pr.number} mergeable state unknown, retrying in {wait_seconds}s... (attempt {attempt+1}/{max_retries})")
            time.sleep(wait_seconds)
    
    # Failed after all retries
    return False, f"Mergeable state unknown after {max_retries} attempts - manual review required"

def choose_merge_strategy(pr) -> str:
    """Choose optimal merge strategy based on PR characteristics"""
    
    commits = pr.commits
    files = pr.changed_files
    
    # Strategy 1: Squash for small, messy commits
    if commits <= 3 and files <= 5:
        return 'squash'
    
    # Strategy 2: Rebase for clean, linear history
    if commits <= 10 and files <= 20:
        # Check if commits follow conventional format
        commit_list = list(pr.get_commits())
        if all(is_conventional_commit(c) for c in commit_list):
            return 'rebase'
    
    # Strategy 3: Merge for large feature branches
    if commits > 10 or files > 20:
        return 'merge'
    
    # Default: squash
    return 'squash'

def is_conventional_commit(commit) -> bool:
    """Check if commit follows conventional commits spec"""
    message = commit.commit.message.split('\n')[0]
    patterns = [
        r'^feat(\(.+\))?:',
        r'^fix(\(.+\))?:',
        r'^docs(\(.+\))?:',
        r'^style(\(.+\))?:',
        r'^refactor(\(.+\))?:',
        r'^test(\(.+\))?:',
        r'^chore(\(.+\))?:',
    ]
    return any(re.match(p, message) for p in patterns)

def main():
    """Execute smart merge"""
    try:
        # Get environment
        gh_token = os.getenv('GH_PAT')
        pr_number = int(os.getenv('PR_NUMBER'))
        repo_name = os.getenv('GITHUB_REPOSITORY')
        
        # Connect
        g = Github(gh_token)
        
        # Check API rate limits
        rate_limit = g.get_rate_limit()
        remaining = rate_limit.core.remaining
        print(f"📊 API Rate Limit: {remaining}/{rate_limit.core.limit} remaining")
        
        if remaining < 50:
            print(f"⚠️ WARNING: Low API rate limit for merge operation")
            if remaining < 5:
                print(f"❌ CRITICAL: API rate limit too low, postponing merge")
                sys.exit(1)
        
        repo = g.get_repo(repo_name)
        pr = repo.get_pull(pr_number)
        
        print(f"\n🔄 Smart Merge for PR #{pr_number}")
        
        # Check if mergeable
        mergeable, reason = can_merge(pr)
        if not mergeable:
            print(f"❌ Cannot merge: {reason}")
            sys.exit(1)
        
        # Choose strategy
        strategy = choose_merge_strategy(pr)
        print(f"📋 Strategy: {strategy.upper()}")
        print(f"   Commits: {pr.commits}, Files: {pr.changed_files}")
        
        # Execute merge
        if strategy == 'squash':
            pr.merge(merge_method='squash', commit_title=pr.title)
        elif strategy == 'rebase':
            pr.merge(merge_method='rebase')
        else:
            pr.merge(merge_method='merge')
        
        print(f"✅ PR #{pr_number} merged using {strategy}")
        
    except Exception as e:
        print(f"❌ Merge failed: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()
