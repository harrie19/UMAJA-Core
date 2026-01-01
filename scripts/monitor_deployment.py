#!/usr/bin/env python3
"""
UMAJA-Core Deployment Monitor
Continuous monitoring of deployment health and performance
"""
import requests
import sys
import time
import json
from datetime import datetime
from typing import Dict, Optional

class DeploymentMonitor:
    """Monitor deployment health and alert on failures"""
    
    def __init__(self, base_url: str, check_interval: int = 60, max_failures: int = 3):
        self.base_url = base_url.rstrip('/')
        self.check_interval = check_interval
        self.max_failures = max_failures
        self.consecutive_failures = 0
        self.total_checks = 0
        self.total_successes = 0
        self.total_failures = 0
        self.start_time = datetime.utcnow()
        self.metrics = []
        
    def log(self, message: str, level: str = "INFO"):
        """Log a message with timestamp"""
        timestamp = datetime.utcnow().isoformat()
        print(f"[{timestamp}] [{level}] {message}")
        
    def check_health(self) -> Dict:
        """Check deployment health endpoint"""
        url = f"{self.base_url}/health"
        
        try:
            start = time.time()
            response = requests.get(url, timeout=10)
            response_time = time.time() - start
            
            if response.status_code == 200:
                data = response.json()
                return {
                    "status": "healthy",
                    "response_time": response_time,
                    "data": data,
                    "error": None
                }
            else:
                return {
                    "status": "unhealthy",
                    "response_time": response_time,
                    "data": None,
                    "error": f"HTTP {response.status_code}"
                }
                
        except requests.exceptions.Timeout:
            return {
                "status": "unhealthy",
                "response_time": 10.0,
                "data": None,
                "error": "Request timeout (10s)"
            }
        except requests.exceptions.ConnectionError:
            return {
                "status": "unhealthy",
                "response_time": 0,
                "data": None,
                "error": "Connection failed"
            }
        except Exception as e:
            return {
                "status": "unhealthy",
                "response_time": 0,
                "data": None,
                "error": str(e)
            }
    
    def record_metric(self, check_result: Dict):
        """Record monitoring metrics"""
        metric = {
            "timestamp": datetime.utcnow().isoformat(),
            "status": check_result["status"],
            "response_time": check_result["response_time"],
            "error": check_result.get("error")
        }
        
        self.metrics.append(metric)
        
        # Keep only last 100 metrics
        if len(self.metrics) > 100:
            self.metrics = self.metrics[-100:]
    
    def calculate_uptime(self) -> float:
        """Calculate uptime percentage"""
        if self.total_checks == 0:
            return 100.0
        return (self.total_successes / self.total_checks) * 100
    
    def get_average_response_time(self) -> float:
        """Calculate average response time from recent metrics"""
        if not self.metrics:
            return 0.0
        
        valid_metrics = [m for m in self.metrics if m["status"] == "healthy"]
        if not valid_metrics:
            return 0.0
        
        total_time = sum(m["response_time"] for m in valid_metrics)
        return total_time / len(valid_metrics)
    
    def alert_failure(self, check_result: Dict):
        """Alert on deployment failure"""
        self.log("=" * 80, "ALERT")
        self.log("🚨 DEPLOYMENT ALERT - SERVICE UNHEALTHY", "ALERT")
        self.log("=" * 80, "ALERT")
        self.log(f"URL: {self.base_url}", "ALERT")
        self.log(f"Consecutive Failures: {self.consecutive_failures}/{self.max_failures}", "ALERT")
        self.log(f"Error: {check_result.get('error', 'Unknown')}", "ALERT")
        self.log(f"Total Uptime: {self.calculate_uptime():.2f}%", "ALERT")
        self.log("=" * 80, "ALERT")
    
    def print_status(self, check_result: Dict):
        """Print current status"""
        uptime = self.calculate_uptime()
        avg_response = self.get_average_response_time()
        runtime = (datetime.utcnow() - self.start_time).total_seconds()
        
        status_icon = "✅" if check_result["status"] == "healthy" else "❌"
        
        self.log(
            f"{status_icon} Status: {check_result['status'].upper()} | "
            f"Response: {check_result['response_time']:.3f}s | "
            f"Uptime: {uptime:.2f}% | "
            f"Avg Response: {avg_response:.3f}s | "
            f"Runtime: {runtime:.0f}s"
        )
        
        if check_result["error"]:
            self.log(f"   Error: {check_result['error']}", "ERROR")
    
    def generate_report(self) -> Dict:
        """Generate monitoring report"""
        runtime = (datetime.utcnow() - self.start_time).total_seconds()
        
        return {
            "timestamp": datetime.utcnow().isoformat(),
            "target": self.base_url,
            "monitoring_duration_seconds": runtime,
            "statistics": {
                "total_checks": self.total_checks,
                "successful_checks": self.total_successes,
                "failed_checks": self.total_failures,
                "uptime_percentage": self.calculate_uptime(),
                "average_response_time": self.get_average_response_time(),
                "consecutive_failures": self.consecutive_failures
            },
            "recent_metrics": self.metrics[-10:] if self.metrics else []
        }
    
    def save_metrics(self, filename: str = "deployment_metrics.json"):
        """Save metrics to file"""
        report = self.generate_report()
        
        with open(filename, 'w') as f:
            json.dump(report, f, indent=2)
        
        self.log(f"Metrics saved to {filename}")
    
    def monitor(self, duration: Optional[int] = None):
        """
        Start monitoring
        Args:
            duration: Optional duration in seconds. If None, runs indefinitely
        """
        self.log("=" * 80)
        self.log("UMAJA-Core Deployment Monitor Starting")
        self.log("=" * 80)
        self.log(f"Target: {self.base_url}")
        self.log(f"Check Interval: {self.check_interval}s")
        self.log(f"Max Consecutive Failures: {self.max_failures}")
        if duration:
            self.log(f"Duration: {duration}s")
        else:
            self.log("Duration: Continuous (Ctrl+C to stop)")
        self.log("=" * 80)
        self.log("")
        
        end_time = time.time() + duration if duration else None
        
        try:
            while True:
                # Check if we should stop
                if end_time and time.time() >= end_time:
                    break
                
                # Perform health check
                check_result = self.check_health()
                self.total_checks += 1
                
                # Record metrics
                self.record_metric(check_result)
                
                # Update statistics
                if check_result["status"] == "healthy":
                    self.total_successes += 1
                    self.consecutive_failures = 0
                else:
                    self.total_failures += 1
                    self.consecutive_failures += 1
                    
                    # Alert if too many consecutive failures
                    if self.consecutive_failures >= self.max_failures:
                        self.alert_failure(check_result)
                
                # Print status
                self.print_status(check_result)
                
                # Save metrics periodically (every 10 checks)
                if self.total_checks % 10 == 0:
                    self.save_metrics()
                
                # Wait for next check
                time.sleep(self.check_interval)
                
        except KeyboardInterrupt:
            self.log("\n" + "=" * 80)
            self.log("Monitoring stopped by user")
            self.log("=" * 80)
        
        # Final report
        self.print_final_report()
        self.save_metrics()
    
    def print_final_report(self):
        """Print final monitoring report"""
        report = self.generate_report()
        
        self.log("")
        self.log("=" * 80)
        self.log("FINAL MONITORING REPORT")
        self.log("=" * 80)
        self.log(f"Target: {self.base_url}")
        self.log(f"Monitoring Duration: {report['monitoring_duration_seconds']:.0f}s")
        self.log(f"Total Checks: {report['statistics']['total_checks']}")
        self.log(f"Successful: {report['statistics']['successful_checks']} ✅")
        self.log(f"Failed: {report['statistics']['failed_checks']} ❌")
        self.log(f"Uptime: {report['statistics']['uptime_percentage']:.2f}%")
        self.log(f"Avg Response Time: {report['statistics']['average_response_time']:.3f}s")
        self.log("=" * 80)

def main():
    """Main entry point"""
    if len(sys.argv) < 2:
        print("Usage: python monitor_deployment.py <base_url> [interval] [duration]")
        print("")
        print("Arguments:")
        print("  base_url  - Base URL of the deployment (required)")
        print("  interval  - Check interval in seconds (default: 60)")
        print("  duration  - Monitoring duration in seconds (default: infinite)")
        print("")
        print("Examples:")
        print("  python monitor_deployment.py https://umaja-core.railway.app")
        print("  python monitor_deployment.py http://localhost:5000 30")
        print("  python monitor_deployment.py https://umaja-core.railway.app 60 300")
        sys.exit(1)
    
    base_url = sys.argv[1]
    interval = int(sys.argv[2]) if len(sys.argv) > 2 else 60
    duration = int(sys.argv[3]) if len(sys.argv) > 3 else None
    
    monitor = DeploymentMonitor(base_url, check_interval=interval)
    monitor.monitor(duration=duration)

if __name__ == "__main__":
    main()
