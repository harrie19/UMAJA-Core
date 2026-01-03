#!/usr/bin/env python3
"""
UMAJA Reality Agent - Proactive System Monitor
Philosophy: Reality Glasses (Verify, Don't Assume)
"""

import re
import json
import logging
from pathlib import Path
from datetime import datetime, timezone
from typing import Dict, List, Any

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class RealityGlassesSensor:
    """
    Active verification sensors - Reality Glasses in code
    Philosophy: Check facts, don't guess
    """
    
    def __init__(self, repo_root: Path = None):
        self.repo_root = repo_root or Path(__file__).parent.parent
        logger.info(f"🥽 Reality Glasses initialized at {self.repo_root}")
    
    def check_backend_url(self) -> Dict[str, Any]:
        """
        Reality Check #1: Backend URL Configuration
        Verifies docs/config.js has correct Railway URL
        
        Philosophy: READ the file, don't ASSUME it's correct
        """
        logger.info("🔍 Checking backend URL configuration...")
        
        config_file = self.repo_root / "docs" / "config.js"
        
        if not config_file.exists():
            return {
                'status': 'ERROR',
                'message': 'config.js not found',
                'confidence': 1.0,
                'evidence': f'File missing: {config_file}'
            }
        
        try:
            content = config_file.read_text()
            
            # Look for production URL
            production_match = re.search(
                r"production:\s*['\"]https?://([^'\"]+)['\"]",
                content
            )
            
            if not production_match:
                return {
                    'status': 'ERROR',
                    'message': 'No production URL found',
                    'confidence': 1.0,
                    'evidence': 'production: field not found in config'
                }
            
            url = production_match.group(1)
            
            # Expected URL patterns
            expected_patterns = [
                'umaja-core-production.up.railway.app',
                'umaja.*railway.app'
            ]
            
            is_correct = any(
                re.search(pattern, url, re.IGNORECASE) 
                for pattern in expected_patterns
            )
            
            if is_correct:
                return {
                    'status': 'OK',
                    'message': 'Backend URL configured correctly',
                    'url': url,
                    'confidence': 1.0,
                    'evidence': f'Found: {url}'
                }
            else:
                return {
                    'status': 'WARNING',
                    'message': 'Backend URL may be incorrect',
                    'url': url,
                    'expected': 'umaja-core-production.up.railway.app',
                    'confidence': 0.8,
                    'evidence': f'Found: {url}, expected pattern not matched'
                }
        
        except Exception as e:
            return {
                'status': 'ERROR',
                'message': f'Error reading config: {str(e)}',
                'confidence': 1.0,
                'evidence': str(e)
            }
    
    def scan_for_bugs(self) -> Dict[str, Any]:
        """
        Reality Check #2: Bug Scanning
        Searches for common issues via regex patterns
        
        Philosophy: Find problems BEFORE they cause issues
        """
        logger.info("🔍 Scanning for bugs...")
        
        patterns = {
            'naive_datetime': {
                'pattern': r'datetime\.now\(\)(?!\s*[\.\(])',
                'severity': 'HIGH',
                'message': 'Naive datetime (missing timezone)'
            },
            'todo_comments': {
                'pattern': r'#\s*TODO|#\s*FIXME|#\s*XXX',
                'severity': 'LOW',
                'message': 'TODO comment'
            },
            'bare_except': {
                'pattern': r'except\s*:',
                'severity': 'MEDIUM',
                'message': 'Bare except (catches all exceptions)'
            },
            'hardcoded_password': {
                'pattern': r"password\s*=\s*['\"][^'\"]+['\"]",
                'severity': 'CRITICAL',
                'message': 'Hardcoded password detected'
            }
        }
        
        findings = []
        
        # Scan Python files
        for py_file in self.repo_root.rglob("*.py"):
            # Skip virtual environments
            if 'venv' in str(py_file) or '.venv' in str(py_file):
                continue
            
            try:
                content = py_file.read_text()
                
                for bug_type, config in patterns.items():
                    matches = re.finditer(config['pattern'], content, re.IGNORECASE)
                    
                    for match in matches:
                        # Get line number
                        line_num = content[:match.start()].count('\n') + 1
                        
                        findings.append({
                            'type': bug_type,
                            'severity': config['severity'],
                            'message': config['message'],
                            'file': str(py_file.relative_to(self.repo_root)),
                            'line': line_num,
                            'snippet': match.group(0)[:50]
                        })
            
            except Exception as e:
                logger.warning(f"Error scanning {py_file}: {e}")
        
        # Categorize by severity
        by_severity = {
            'CRITICAL': [f for f in findings if f['severity'] == 'CRITICAL'],
            'HIGH': [f for f in findings if f['severity'] == 'HIGH'],
            'MEDIUM': [f for f in findings if f['severity'] == 'MEDIUM'],
            'LOW': [f for f in findings if f['severity'] == 'LOW']
        }
        
        return {
            'status': 'CRITICAL' if by_severity['CRITICAL'] else 
                     'WARNING' if (by_severity['HIGH'] or by_severity['MEDIUM']) else 'OK',
            'total_findings': len(findings),
            'by_severity': {k: len(v) for k, v in by_severity.items()},
            'findings': findings[:20],  # Top 20
            'confidence': 0.95
        }
    
    def check_test_status(self) -> Dict[str, Any]:
        """
        Reality Check #3: Test Suite Status
        Checks if pytest is available and counts tests
        """
        logger.info("🔍 Checking test status...")
        
        # Check if pytest is available
        try:
            import pytest
            pytest_available = True
        except ImportError:
            pytest_available = False
        
        # Count test files
        test_files = list(self.repo_root.glob("test*.py")) + \
                    list(self.repo_root.glob("tests/**/*.py"))
        
        return {
            'status': 'OK' if pytest_available else 'WARNING',
            'pytest_available': pytest_available,
            'test_files_count': len(test_files),
            'test_files': [str(f.relative_to(self.repo_root)) for f in test_files[:10]],
            'confidence': 1.0,
            'message': 'Pytest available' if pytest_available else 'Pytest not installed'
        }
    
    def check_deployment_files(self) -> Dict[str, Any]:
        """
        Reality Check #4: Deployment Files Validation
        Verifies required deployment files exist
        """
        logger.info("🔍 Checking deployment files...")
        
        required_files = [
            'railway.json',
            'Procfile',
            'requirements.txt',
            'wsgi.py',
            '.env.example'
        ]
        
        results = {}
        missing = []
        
        for filename in required_files:
            file_path = self.repo_root / filename
            exists = file_path.exists()
            results[filename] = exists
            
            if not exists:
                missing.append(filename)
        
        return {
            'status': 'ERROR' if missing else 'OK',
            'all_present': len(missing) == 0,
            'missing_files': missing,
            'present_files': [f for f, exists in results.items() if exists],
            'confidence': 1.0,
            'message': 'All deployment files present' if not missing else f'{len(missing)} files missing'
        }


class UMAJARealityAgent:
    """
    Main Reality Agent orchestrator
    Philosophy: Proactive monitoring, not reactive firefighting
    """
    
    def __init__(self):
        self.sensor = RealityGlassesSensor()
        self.results_dir = Path(__file__).parent.parent / "data" / "reality_checks"
        self.results_dir.mkdir(parents=True, exist_ok=True)
    
    def _determine_overall_status(self, statuses: List[str]) -> str:
        """Determine overall status from check statuses"""
        if 'ERROR' in statuses or 'CRITICAL' in statuses:
            return 'CRITICAL'
        elif 'WARNING' in statuses:
            return 'WARNING'
        else:
            return 'HEALTHY'
    
    def run_all_checks(self) -> Dict[str, Any]:
        """Run all reality checks and generate report"""
        logger.info("🥽 Starting Reality Agent checks...")
        
        timestamp = datetime.now(timezone.utc)
        
        checks = {
            'backend_url': self.sensor.check_backend_url(),
            'bug_scan': self.sensor.scan_for_bugs(),
            'test_status': self.sensor.check_test_status(),
            'deployment_files': self.sensor.check_deployment_files()
        }
        
        # Determine overall status
        statuses = [check['status'] for check in checks.values()]
        overall_status = self._determine_overall_status(statuses)
        
        report = {
            'timestamp': timestamp.isoformat(),
            'overall_status': overall_status,
            'checks': checks,
            'summary': {
                'total_checks': len(checks),
                'passed': sum(1 for c in checks.values() if c['status'] == 'OK'),
                'warnings': sum(1 for c in checks.values() if c['status'] == 'WARNING'),
                'errors': sum(1 for c in checks.values() if c['status'] in ['ERROR', 'CRITICAL'])
            }
        }
        
        # Save reports
        self._save_json_report(report, timestamp)
        self._save_markdown_report(report, timestamp)
        
        return report
    
    def _save_json_report(self, report: Dict, timestamp: datetime):
        """Save JSON report"""
        filename = f"reality_check_{timestamp.strftime('%Y%m%d_%H%M%S')}.json"
        filepath = self.results_dir / filename
        
        with open(filepath, 'w') as f:
            json.dump(report, f, indent=2)
        
        logger.info(f"📄 JSON report saved: {filepath}")
    
    def _save_markdown_report(self, report: Dict, timestamp: datetime):
        """Save human-readable Markdown report"""
        filename = f"reality_check_{timestamp.strftime('%Y%m%d_%H%M%S')}.md"
        filepath = self.results_dir / filename
        
        md = f"""# 🥽 Reality Check Report

**Timestamp:** {timestamp.strftime('%Y-%m-%d %H:%M:%S UTC')}  
**Overall Status:** {report['overall_status']}

## Summary

- Total Checks: {report['summary']['total_checks']}
- ✅ Passed: {report['summary']['passed']}
- ⚠️ Warnings: {report['summary']['warnings']}
- ❌ Errors: {report['summary']['errors']}

---

## Checks Detail

See JSON report for full details.

---

*Generated by UMAJA Reality Agent - Reality Glasses Philosophy*
"""
        
        with open(filepath, 'w') as f:
            f.write(md)
        
        logger.info(f"📄 Markdown report saved: {filepath}")


def main():
    """CLI entry point"""
    print("🥽 UMAJA Reality Agent v1.0")
    print("=" * 60)
    
    agent = UMAJARealityAgent()
    report = agent.run_all_checks()
    
    print()
    print("📊 Reality Check Complete!")
    print(f"Overall Status: {report['overall_status']}")
    print()
    
    exit_code = 0 if report['overall_status'] in ['HEALTHY', 'WARNING'] else 1
    return exit_code


if __name__ == '__main__':
    exit(main())
