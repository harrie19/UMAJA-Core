#!/usr/bin/env python3
"""
Enhanced AI Reviewer with Security Hardening
Prevents token exposure and implements comprehensive security scanning
"""

import os
import re
import sys
import json
from github import Github
from typing import Dict, List, Any

# Security: NEVER log tokens, even partially
def validate_token(token_name: str) -> str:
    """Validate token exists without logging"""
    token = os.getenv(token_name)
    if not token:
        raise ValueError(f"{token_name} not configured")
    print(f"✅ {token_name}: validated")
    return token

# Restricted paths requiring human review
RESTRICTED_PATHS = [
    r'^\.github/workflows/.*',
    r'.*secrets.*',
    r'.*\.key$',
    r'.*\.pem$',
    r'^railway\.json$',
    r'^\.env.*',
    r'^package-lock\.json$',
]

# Dangerous code patterns
DANGEROUS_PATTERNS = [
    (r'eval\(', 'Code injection via eval()'),
    (r'exec\(', 'Code execution via exec()'),
    (r'__import__\(', 'Dynamic import'),
    (r'os\.system\(', 'Shell command execution'),
    (r'subprocess\.', 'Subprocess execution'),
    (r'password\s*=\s*["\']', 'Hardcoded password'),
    (r'api[_-]?key\s*=\s*["\']', 'Hardcoded API key'),
    (r'token\s*=\s*["\'][^"\']{20,}["\']', 'Hardcoded token'),
    (r'RAILWAY_TOKEN\s*=', 'Railway token in code'),
    (r'GH_PAT\s*=', 'GitHub PAT in code'),
]

def should_auto_approve(pr) -> tuple[bool, List[str]]:
    """
    Enhanced approval logic with comprehensive security checks
    Returns: (should_approve, reasons)
    """
    reasons = []
    
    # 1. Size check
    if pr.changed_files > 10:
        reasons.append(f"❌ Too many files changed: {pr.changed_files} (max 10)")
        return False, reasons
    
    reasons.append(f"✅ File count acceptable: {pr.changed_files}/10")
    
    # 2. Restricted path check
    files = pr.get_files()
    for file in files:
        for pattern in RESTRICTED_PATHS:
            if re.match(pattern, file.filename, re.IGNORECASE):
                reasons.append(f"❌ Restricted path: {file.filename}")
                return False, reasons
    
    reasons.append(f"✅ No restricted paths modified")
    
    # 3. Content security scan
    security_issues = []
    for file in files:
        if file.patch:
            for pattern, description in DANGEROUS_PATTERNS:
                matches = re.finditer(pattern, file.patch, re.IGNORECASE)
                for match in matches:
                    security_issues.append(f"{file.filename}: {description} at line {match.start()}")
    
    if security_issues:
        reasons.append(f"❌ Security issues detected:")
        reasons.extend([f"   - {issue}" for issue in security_issues])
        return False, reasons
    
    reasons.append(f"✅ No dangerous patterns found")
    
    # 4. Dependency file check
    dependency_files = ['package.json', 'requirements.txt', 'Gemfile', 'go.mod', 'Cargo.toml']
    modified_files = [f.filename for f in files]
    
    has_deps = any(df in modified_files for df in dependency_files)
    if not has_deps:
        reasons.append(f"ℹ️ Not a dependency update (acceptable)")
    else:
        reasons.append(f"✅ Dependency file update detected")
    
    # 5. Check tests passing
    commit = pr.get_commits().reversed[0]
    statuses = commit.get_combined_status()
    
    if statuses.state != 'success':
        reasons.append(f"❌ Checks not passing: {statuses.state}")
        return False, reasons
    
    reasons.append(f"✅ All checks passing")
    
    # 6. No file deletions
    deletions = [f for f in files if f.status == 'removed']
    if deletions:
        reasons.append(f"❌ File deletions detected: {len(deletions)} files")
        return False, reasons
    
    reasons.append(f"✅ No file deletions")
    
    # 7. Draft PR check
    if pr.draft:
        reasons.append(f"❌ PR is still in draft mode")
        return False, reasons
    
    reasons.append(f"✅ PR is ready for review")
    
    # All checks passed!
    return True, reasons

def main():
    """Main execution"""
    try:
        # Validate environment (without logging tokens)
        gh_token = validate_token('GH_PAT')
        pr_number = int(os.getenv('PR_NUMBER'))
        repo_name = os.getenv('GITHUB_REPOSITORY')
        
        print(f"\n🤖 Reviewing PR #{pr_number} in {repo_name}")
        
        # Connect to GitHub
        g = Github(gh_token)
        repo = g.get_repo(repo_name)
        pr = repo.get_pull(pr_number)
        
        # Run approval logic
        should_approve, reasons = should_auto_approve(pr)
        
        # Post review comment
        comment_body = "## 🤖 Automated Security Review\n\n"
        comment_body += "\n".join(reasons)
        
        if should_approve:
            comment_body += "\n\n✅ **Recommendation:** APPROVE\n"
            comment_body += "This PR passes all automated security and quality checks."
            print(f"::set-output name=should_approve::true")
        else:
            comment_body += "\n\n⚠️ **Recommendation:** MANUAL REVIEW REQUIRED\n"
            comment_body += "This PR requires human review due to security concerns or policy violations."
            print(f"::set-output name=should_approve::false")
        
        # Post comment
        pr.create_issue_comment(comment_body)
        print(f"\n✅ Review posted to PR #{pr_number}")
        
    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()
