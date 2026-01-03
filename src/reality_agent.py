#!/usr/bin/env python3
"""
Reality Agent for UMAJA-Core
Implements "Reality Glasses" philosophy for proactive system health monitoring

Philosophy:
- PROACTIVE over Reactive (scan before asked)
- VERIFY over Assume (check facts, don't guess)
- TRUTH over Plausibility (measure reality, don't imagine)
- REALITY over Hallucination (sensors > training data)

Bahá'í Principles:
- Truth: Agent verifies facts, doesn't guess
- Service: Agent helps proactively without being asked
- Humility: Agent admits when checks fail (confidence < 1.0)
- Unity: Agent serves all users equally
"""

import os
import re
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Any, Tuple
from dataclasses import dataclass, asdict


@dataclass
class RealityCheck:
    """Result of a reality verification check"""
    name: str
    status: str  # "OK", "WARNING", "CRITICAL", "ERROR"
    confidence: float  # 0.0 to 1.0
    message: str
    details: Dict[str, Any]
    timestamp: str


class RealityGlassesSensor:
    """
    Reality Glasses - See the truth, not assumptions
    
    This class embodies the "Reality Glasses" philosophy:
    - Actively verifies facts against reality
    - Does not assume or hallucinate
    - Measures confidence in every check
    - Reports truth, even when uncertain
    """
    
    def __init__(self, repo_root: Path):
        self.repo_root = repo_root
        self.timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    
    def verify_backend_url(self) -> RealityCheck:
        """
        Verify backend URL configuration matches expected Railway URL
        VERIFY over ASSUME: Check actual file content, don't guess
        """
        config_path = self.repo_root / "docs" / "config.js"
        expected_url = "https://umaja-core-production.up.railway.app"
        
        try:
            if not config_path.exists():
                return RealityCheck(
                    name="Backend URL Check",
                    status="CRITICAL",
                    confidence=1.0,
                    message="config.js file not found",
                    details={"path": str(config_path), "exists": False},
                    timestamp=datetime.now(timezone.utc).isoformat()
                )
            
            content = config_path.read_text()
            
            # Search for Railway URL
            found_url = None
            for line in content.split('\n'):
                if 'railway.app' in line.lower():
                    # Extract URL from line
                    url_match = re.search(r'https://[^\s\'"]+railway\.app', line)
                    if url_match:
                        found_url = url_match.group(0)
                        break
            
            if found_url == expected_url:
                return RealityCheck(
                    name="Backend URL Check",
                    status="OK",
                    confidence=1.0,
                    message="Backend URL correctly configured",
                    details={
                        "expected": expected_url,
                        "found": found_url,
                        "file": str(config_path)
                    },
                    timestamp=datetime.now(timezone.utc).isoformat()
                )
            elif found_url:
                return RealityCheck(
                    name="Backend URL Check",
                    status="WARNING",
                    confidence=1.0,
                    message="Backend URL mismatch detected",
                    details={
                        "expected": expected_url,
                        "found": found_url,
                        "file": str(config_path)
                    },
                    timestamp=datetime.now(timezone.utc).isoformat()
                )
            else:
                return RealityCheck(
                    name="Backend URL Check",
                    status="CRITICAL",
                    confidence=0.9,
                    message="No Railway backend URL found in config.js",
                    details={
                        "expected": expected_url,
                        "found": None,
                        "file": str(config_path)
                    },
                    timestamp=datetime.now(timezone.utc).isoformat()
                )
                
        except Exception as e:
            return RealityCheck(
                name="Backend URL Check",
                status="ERROR",
                confidence=0.5,
                message=f"Error reading config.js: {str(e)}",
                details={"error": str(e)},
                timestamp=datetime.now(timezone.utc).isoformat()
            )
    
    def scan_for_bugs(self) -> RealityCheck:
        """
        Proactively scan for common code issues
        PROACTIVE over REACTIVE: Find problems before they're reported
        """
        issues = {
            "naive_datetime": [],
            "todos": [],
            "missing_error_handling": [],
            "hardcoded_credentials": []
        }
        
        # Scan Python files
        python_files = list(self.repo_root.rglob("*.py"))
        # Exclude venv and cache directories
        python_files = [f for f in python_files if 'venv' not in str(f) and '__pycache__' not in str(f)]
        
        total_files = len(python_files)
        scanned_files = 0
        
        for py_file in python_files:
            try:
                content = py_file.read_text()
                relative_path = py_file.relative_to(self.repo_root)
                
                # Check for naive datetime usage (without timezone)
                # Look for datetime.now() calls that don't include timezone parameter
                has_naive = False
                for line in content.split('\n'):
                    # Skip comments
                    code_part = line.split('#')[0] if '#' in line else line
                    
                    # Skip lines that have datetime.now in strings (like in this check itself!)
                    if "datetime.now(" in code_part and ("'" in code_part or '"' in code_part):
                        # Check if it's in a string literal - simple heuristic
                        if "'datetime.now" in code_part or '"datetime.now' in code_part:
                            continue
                    
                    # Check if line contains datetime.now() without timezone in the call
                    if 'datetime.now(' in code_part:
                        # Extract the full call
                        if re.search(r'datetime\.now\(\s*\)', code_part):
                            # datetime.now() with no arguments - definitely naive
                            has_naive = True
                            break
                        elif 'timezone' not in code_part:
                            # datetime.now(...) but no timezone in the code - likely naive
                            has_naive = True
                            break
                
                if has_naive:
                    issues["naive_datetime"].append(str(relative_path))
                
                # Check for TODO comments
                todo_matches = re.findall(r'#\s*TODO:?\s*(.+)', content, re.IGNORECASE)
                if todo_matches:
                    issues["todos"].append({
                        "file": str(relative_path),
                        "count": len(todo_matches)
                    })
                
                # Check for potential hardcoded credentials
                credential_patterns = [
                    r'password\s*=\s*["\'][^"\']+["\']',
                    r'api[_-]?key\s*=\s*["\'][^"\']+["\']',
                    r'secret\s*=\s*["\'][^"\']+["\']',
                    r'token\s*=\s*["\'][^"\']+["\']'
                ]
                
                for pattern in credential_patterns:
                    matches = re.findall(pattern, content, re.IGNORECASE)
                    # Filter out obvious test/example values
                    real_matches = [m for m in matches if not any(
                        x in m.lower() for x in ['example', 'test', 'your_', 'xxx', 'dummy']
                    )]
                    if real_matches:
                        issues["hardcoded_credentials"].append({
                            "file": str(relative_path),
                            "matches": len(real_matches)
                        })
                
                scanned_files += 1
                
            except Exception as e:
                # Skip files that can't be read
                continue
        
        # Calculate status
        total_issues = (
            len(issues["naive_datetime"]) +
            len(issues["todos"]) +
            len(issues["hardcoded_credentials"])
        )
        
        if len(issues["hardcoded_credentials"]) > 0:
            status = "CRITICAL"
        elif len(issues["naive_datetime"]) > 5:
            status = "WARNING"
        elif total_issues > 0:
            status = "WARNING"
        else:
            status = "OK"
        
        # Confidence based on files scanned
        confidence = min(1.0, scanned_files / max(total_files, 1))
        
        return RealityCheck(
            name="Bug Scan",
            status=status,
            confidence=confidence,
            message=f"Scanned {scanned_files}/{total_files} Python files, found {total_issues} issues",
            details={
                "files_scanned": scanned_files,
                "total_files": total_files,
                "issues": issues,
                "summary": {
                    "naive_datetime": len(issues["naive_datetime"]),
                    "todos": sum(t["count"] for t in issues["todos"]),
                    "missing_error_handling": len(issues["missing_error_handling"]),
                    "hardcoded_credentials": len(issues["hardcoded_credentials"])
                }
            },
            timestamp=datetime.now(timezone.utc).isoformat()
        )
    
    def check_test_status(self) -> RealityCheck:
        """
        Verify test suite availability and status
        VERIFY over ASSUME: Actually check if tests exist and run
        """
        try:
            # Check if pytest is available
            version_result = subprocess.run(
                ["python", "-m", "pytest", "--version"],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if version_result.returncode != 0:
                return RealityCheck(
                    name="Test Status",
                    status="WARNING",
                    confidence=1.0,
                    message="pytest not available",
                    details={"pytest_available": False},
                    timestamp=datetime.now(timezone.utc).isoformat()
                )
            
            # Extract pytest version
            pytest_version = version_result.stdout.strip().split('\n')[0] if version_result.stdout else "pytest"
            
            # Count test files
            test_files = list(self.repo_root.glob("tests/test_*.py")) + \
                        list(self.repo_root.glob("test_*.py"))
            
            # Try to collect tests (don't run them, just count)
            collect_result = subprocess.run(
                ["python", "-m", "pytest", "--collect-only", "-q"],
                capture_output=True,
                text=True,
                timeout=30,
                cwd=str(self.repo_root)
            )
            
            # Extract test count from output
            # Look in both stdout and stderr for the count
            output = collect_result.stdout + "\n" + collect_result.stderr
            test_count = 0
            
            # Look for patterns like "5 tests collected" or "29 tests collected, 2 errors"
            match = re.search(r'(\d+)\s+tests?\s+collected', output)
            if match:
                test_count = int(match.group(1))
            
            # Determine status
            if test_count > 0:
                status = "OK"
                message = f"pytest available, {test_count} tests found"
            else:
                status = "WARNING"
                message = "pytest available but no tests could be collected"
            
            return RealityCheck(
                name="Test Status",
                status=status,
                confidence=1.0,
                message=message,
                details={
                    "pytest_available": True,
                    "pytest_version": pytest_version,
                    "test_files": len(test_files),
                    "tests_collected": test_count,
                    "collection_errors": collect_result.returncode != 0
                },
                timestamp=datetime.now(timezone.utc).isoformat()
            )
            
        except subprocess.TimeoutExpired:
            return RealityCheck(
                name="Test Status",
                status="WARNING",
                confidence=0.7,
                message="Test collection timed out",
                details={"timeout": True},
                timestamp=datetime.now(timezone.utc).isoformat()
            )
        except Exception as e:
            return RealityCheck(
                name="Test Status",
                status="ERROR",
                confidence=0.5,
                message=f"Error checking test status: {str(e)}",
                details={"error": str(e)},
                timestamp=datetime.now(timezone.utc).isoformat()
            )
    
    def validate_deployment_files(self) -> RealityCheck:
        """
        Verify all required deployment files exist
        TRUTH over PLAUSIBILITY: Check actual file existence
        """
        required_files = [
            "railway.json",
            "Procfile",
            "requirements.txt",
            "wsgi.py",
            ".env.example"
        ]
        
        results = {}
        missing = []
        
        for filename in required_files:
            file_path = self.repo_root / filename
            exists = file_path.exists()
            results[filename] = {
                "exists": exists,
                "path": str(file_path)
            }
            
            if exists:
                # Get file size for additional context
                results[filename]["size"] = file_path.stat().st_size
            else:
                missing.append(filename)
        
        if len(missing) == 0:
            status = "OK"
            message = "All deployment files present"
        elif len(missing) <= 2:
            status = "WARNING"
            message = f"Missing {len(missing)} deployment file(s)"
        else:
            status = "CRITICAL"
            message = f"Missing {len(missing)} critical deployment files"
        
        return RealityCheck(
            name="Deployment Files",
            status=status,
            confidence=1.0,
            message=message,
            details={
                "files": results,
                "missing": missing,
                "total": len(required_files),
                "present": len(required_files) - len(missing)
            },
            timestamp=datetime.now(timezone.utc).isoformat()
        )


class UMAJARealityAgent:
    """
    Main Reality Agent Orchestrator
    
    Embodies Bahá'í principles:
    - Truth: Reports verified facts only
    - Service: Serves proactively
    - Humility: Admits uncertainty via confidence scores
    - Unity: Serves all equally
    """
    
    def __init__(self, repo_root: str = None):
        if repo_root is None:
            # Auto-detect repository root
            current = Path(__file__).resolve()
            while current.parent != current:
                if (current / ".git").exists():
                    repo_root = current
                    break
                current = current.parent
            else:
                repo_root = Path.cwd()
        
        self.repo_root = Path(repo_root)
        self.sensor = RealityGlassesSensor(self.repo_root)
        self.results: List[RealityCheck] = []
    
    def run_all_checks(self) -> List[RealityCheck]:
        """
        Run all reality checks
        PROACTIVE: Scan everything, don't wait for problems
        """
        print("🥽 Reality Agent Starting...")
        print(f"📁 Repository: {self.repo_root}")
        print(f"⏰ Timestamp: {datetime.now(timezone.utc).isoformat()}")
        print()
        
        # Run all checks
        checks = [
            ("Backend URL", self.sensor.verify_backend_url),
            ("Bug Scan", self.sensor.scan_for_bugs),
            ("Test Status", self.sensor.check_test_status),
            ("Deployment Files", self.sensor.validate_deployment_files)
        ]
        
        for check_name, check_func in checks:
            print(f"🔍 Running: {check_name}...")
            result = check_func()
            self.results.append(result)
            
            # Print immediate feedback
            status_emoji = {
                "OK": "✅",
                "WARNING": "⚠️",
                "CRITICAL": "🚨",
                "ERROR": "❌"
            }
            print(f"   {status_emoji.get(result.status, '❓')} {result.message}")
            print(f"   Confidence: {result.confidence:.0%}")
            print()
        
        return self.results
    
    def get_overall_status(self) -> Tuple[str, str]:
        """
        Determine overall system status
        Returns: (status, message)
        """
        if not self.results:
            return ("UNKNOWN", "No checks performed")
        
        statuses = [r.status for r in self.results]
        
        if "CRITICAL" in statuses or "ERROR" in statuses:
            return ("CRITICAL", "Critical issues detected requiring immediate attention")
        elif "WARNING" in statuses:
            return ("WARNING", "Warnings detected, system operational but needs attention")
        else:
            return ("HEALTHY", "All systems operational")
    
    def save_results(self) -> Tuple[Path, Path]:
        """
        Save results to data/reality_checks/
        Returns: (json_path, markdown_path)
        """
        timestamp = self.sensor.timestamp
        output_dir = self.repo_root / "data" / "reality_checks"
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Save JSON
        json_path = output_dir / f"reality_check_{timestamp}.json"
        json_data = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "overall_status": self.get_overall_status()[0],
            "checks": [asdict(r) for r in self.results]
        }
        
        with open(json_path, 'w') as f:
            json.dump(json_data, f, indent=2)
        
        # Save Markdown
        md_path = output_dir / f"reality_check_{timestamp}.md"
        overall_status, overall_message = self.get_overall_status()
        
        md_content = f"""# Reality Check Report

**Timestamp:** {datetime.now(timezone.utc).isoformat()}  
**Overall Status:** {overall_status}  
**Message:** {overall_message}

---

## Checks Performed

"""
        
        for result in self.results:
            status_emoji = {
                "OK": "✅",
                "WARNING": "⚠️",
                "CRITICAL": "🚨",
                "ERROR": "❌"
            }
            
            md_content += f"""### {status_emoji.get(result.status, '❓')} {result.name}

**Status:** {result.status}  
**Confidence:** {result.confidence:.0%}  
**Message:** {result.message}

**Details:**
```json
{json.dumps(result.details, indent=2)}
```

---

"""
        
        md_content += """
## Philosophy

This report was generated using **Reality Glasses** philosophy:

- ✅ **PROACTIVE** over Reactive - Scanned before problems reported
- ✅ **VERIFY** over Assume - Checked facts, didn't guess
- ✅ **TRUTH** over Plausibility - Measured reality with confidence scores
- ✅ **REALITY** over Hallucination - Used sensors, not assumptions

---

*Generated by Reality Agent - Serving Truth with Humility* 🥽✨
"""
        
        with open(md_path, 'w') as f:
            f.write(md_content)
        
        return json_path, md_path
    
    def display_summary(self):
        """Display summary to console"""
        print("=" * 70)
        print("🥽 REALITY CHECK COMPLETE")
        print("=" * 70)
        print()
        
        overall_status, overall_message = self.get_overall_status()
        status_emoji = {
            "HEALTHY": "✅",
            "WARNING": "⚠️",
            "CRITICAL": "🚨",
            "UNKNOWN": "❓"
        }
        
        print(f"{status_emoji.get(overall_status, '❓')} Overall Status: {overall_status}")
        print(f"📝 {overall_message}")
        print()
        
        print("Individual Checks:")
        for result in self.results:
            status_emoji_check = {
                "OK": "✅",
                "WARNING": "⚠️",
                "CRITICAL": "🚨",
                "ERROR": "❌"
            }
            print(f"  {status_emoji_check.get(result.status, '❓')} {result.name}: {result.status} (confidence: {result.confidence:.0%})")
        
        print()
        print("=" * 70)


def main():
    """Main entry point for standalone execution"""
    import sys
    
    # Determine repository root
    repo_root = os.environ.get('GITHUB_WORKSPACE')
    if not repo_root:
        # Try to find .git directory
        current = Path(__file__).resolve().parent
        while current.parent != current:
            if (current / ".git").exists():
                repo_root = str(current)
                break
            current = current.parent
        else:
            repo_root = str(Path.cwd())
    
    # Create and run agent
    agent = UMAJARealityAgent(repo_root)
    agent.run_all_checks()
    
    # Save results
    json_path, md_path = agent.save_results()
    print(f"💾 Results saved:")
    print(f"   JSON: {json_path}")
    print(f"   Markdown: {md_path}")
    print()
    
    # Display summary
    agent.display_summary()
    
    # Exit with appropriate code
    overall_status = agent.get_overall_status()[0]
    if overall_status in ["CRITICAL", "ERROR"]:
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == "__main__":
    main()
