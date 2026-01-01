#!/usr/bin/env python3
"""
UMAJA-Core Deployment Health Check
Validates all endpoints and generates deployment report
"""
import requests
import sys
import json
from datetime import datetime
from typing import Dict, List, Tuple

class DeploymentHealthCheck:
    """Comprehensive deployment health checker"""
    
    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip('/')
        self.results = []
        self.passed = 0
        self.failed = 0
        
    def log(self, message: str, level: str = "INFO"):
        """Log a message with timestamp"""
        timestamp = datetime.utcnow().isoformat()
        print(f"[{timestamp}] [{level}] {message}")
        
    def check_endpoint(self, path: str, method: str = "GET", 
                      expected_status: int = 200,
                      check_json: bool = True,
                      required_fields: List[str] = None) -> Tuple[bool, str]:
        """
        Check a single endpoint
        Returns (success, message)
        """
        url = f"{self.base_url}{path}"
        self.log(f"Checking {method} {url}")
        
        try:
            if method == "GET":
                response = requests.get(url, timeout=10)
            elif method == "POST":
                response = requests.post(url, timeout=10)
            else:
                return False, f"Unsupported method: {method}"
            
            # Check status code
            if response.status_code != expected_status:
                return False, f"Expected status {expected_status}, got {response.status_code}"
            
            # Check JSON response
            if check_json:
                try:
                    data = response.json()
                    
                    # Check required fields
                    if required_fields:
                        missing = [f for f in required_fields if f not in data]
                        if missing:
                            return False, f"Missing required fields: {', '.join(missing)}"
                    
                    return True, f"OK - Response: {json.dumps(data, indent=2)[:200]}..."
                    
                except json.JSONDecodeError:
                    return False, "Response is not valid JSON"
            
            return True, "OK"
            
        except requests.exceptions.Timeout:
            return False, "Request timeout (10s)"
        except requests.exceptions.ConnectionError:
            return False, "Connection failed - service may be down"
        except Exception as e:
            return False, f"Error: {str(e)}"
    
    def run_checks(self) -> Dict:
        """Run all health checks"""
        self.log("=" * 80)
        self.log("UMAJA-Core Deployment Health Check")
        self.log("=" * 80)
        self.log(f"Target: {self.base_url}")
        self.log("")
        
        # Define all checks
        checks = [
            {
                "name": "Root Endpoint",
                "path": "/",
                "required_fields": ["service", "version", "mission", "endpoints"]
            },
            {
                "name": "Health Check",
                "path": "/health",
                "required_fields": ["status", "service", "version", "timestamp", "checks"]
            },
            {
                "name": "Version Info",
                "path": "/version",
                "required_fields": ["version", "service", "mission"]
            },
            {
                "name": "Deployment Info",
                "path": "/deployment-info",
                "required_fields": ["environment", "version", "timestamp"]
            },
            {
                "name": "Daily Smile API",
                "path": "/api/daily-smile",
                "required_fields": ["content", "archetype", "mission"]
            },
            {
                "name": "Smile by Archetype - Professor",
                "path": "/api/smile/professor",
                "required_fields": ["content", "archetype"]
            },
            {
                "name": "Smile by Archetype - Worrier",
                "path": "/api/smile/worrier",
                "required_fields": ["content", "archetype"]
            },
            {
                "name": "Smile by Archetype - Enthusiast",
                "path": "/api/smile/enthusiast",
                "required_fields": ["content", "archetype"]
            },
            {
                "name": "404 Error Handling",
                "path": "/nonexistent-endpoint",
                "expected_status": 404,
                "required_fields": ["error", "message"]
            }
        ]
        
        # Run all checks
        for check in checks:
            name = check["name"]
            path = check["path"]
            expected_status = check.get("expected_status", 200)
            required_fields = check.get("required_fields", [])
            
            success, message = self.check_endpoint(
                path, 
                expected_status=expected_status,
                required_fields=required_fields
            )
            
            if success:
                self.passed += 1
                self.log(f"✅ PASS: {name}", "PASS")
                self.results.append({
                    "name": name,
                    "status": "PASS",
                    "path": path,
                    "message": message
                })
            else:
                self.failed += 1
                self.log(f"❌ FAIL: {name} - {message}", "FAIL")
                self.results.append({
                    "name": name,
                    "status": "FAIL",
                    "path": path,
                    "message": message
                })
            
            self.log("")
        
        # Generate report
        return self.generate_report()
    
    def generate_report(self) -> Dict:
        """Generate final deployment report"""
        total = self.passed + self.failed
        success_rate = (self.passed / total * 100) if total > 0 else 0
        
        report = {
            "timestamp": datetime.utcnow().isoformat(),
            "target": self.base_url,
            "summary": {
                "total_checks": total,
                "passed": self.passed,
                "failed": self.failed,
                "success_rate": f"{success_rate:.1f}%"
            },
            "results": self.results,
            "deployment_status": "HEALTHY" if self.failed == 0 else "UNHEALTHY"
        }
        
        self.log("=" * 80)
        self.log("DEPLOYMENT HEALTH CHECK REPORT")
        self.log("=" * 80)
        self.log(f"Total Checks: {total}")
        self.log(f"Passed: {self.passed} ✅")
        self.log(f"Failed: {self.failed} ❌")
        self.log(f"Success Rate: {success_rate:.1f}%")
        self.log(f"Overall Status: {report['deployment_status']}")
        self.log("=" * 80)
        
        return report
    
    def save_report(self, filename: str = "deployment_report.json"):
        """Save report to file"""
        report = self.generate_report()
        
        with open(filename, 'w') as f:
            json.dump(report, f, indent=2)
        
        self.log(f"Report saved to {filename}")

def main():
    """Main entry point"""
    if len(sys.argv) < 2:
        print("Usage: python deployment_health_check.py <base_url>")
        print("Example: python deployment_health_check.py https://umaja-core.railway.app")
        print("         python deployment_health_check.py http://localhost:5000")
        sys.exit(1)
    
    base_url = sys.argv[1]
    checker = DeploymentHealthCheck(base_url)
    report = checker.run_checks()
    
    # Save report
    checker.save_report()
    
    # Exit with appropriate code
    if report["deployment_status"] == "HEALTHY":
        print("\n🎉 Deployment is HEALTHY! All checks passed. 🌟")
        sys.exit(0)
    else:
        print(f"\n⚠️  Deployment has issues: {checker.failed} check(s) failed.")
        sys.exit(1)

if __name__ == "__main__":
    main()
