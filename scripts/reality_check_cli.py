#!/usr/bin/env python3
"""
Reality Check CLI Tool for UMAJA
Runs reality checks from command line with various options
"""
import sys
import json
import argparse
import time
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from reality_agent import RealityAgent


def run_checks(check_name: str = None, format_type: str = "text", watch: bool = False, interval: int = 300) -> None:
    """Run reality checks"""
    
    agent = RealityAgent()
    
    while True:
        if check_name:
            # Run specific check
            check_methods = {
                "backend_url": agent.check_backend_url,
                "bug_scan": agent.scan_for_bugs,
                "test_status": agent.check_test_status,
                "deployment": agent.check_deployment_config
            }
            
            if check_name not in check_methods:
                print(f"Unknown check: {check_name}", file=sys.stderr)
                print(f"Available: {', '.join(check_methods.keys())}", file=sys.stderr)
                sys.exit(1)
            
            result = check_methods[check_name]()
            results = {"checks": [result.to_dict()]}
        else:
            # Run all checks
            results = agent.run_all_checks()
        
        # Output results
        if format_type == "json":
            print(json.dumps(results, indent=2))
        else:
            print_text_report(results)
        
        if not watch:
            break
        
        # Wait before next check
        print(f"\nWaiting {interval} seconds before next check...\n")
        time.sleep(interval)


def print_text_report(results: dict) -> None:
    """Print human-readable text report"""
    print("=" * 60)
    print("UMAJA Reality Check Report")
    print("=" * 60)
    print()
    
    checks = results.get("checks", [])
    summary = results.get("summary", {})
    
    # Print summary
    print(f"Total Checks: {summary.get('total_checks', len(checks))}")
    print(f"Passed: {summary.get('passed', 0)}")
    print(f"Warnings: {summary.get('warnings', 0)}")
    print(f"Failed: {summary.get('failed', 0)}")
    print(f"Overall Status: {summary.get('overall_status', 'UNKNOWN')}")
    print()
    
    # Print individual checks
    for check in checks:
        status = check.get("status", "UNKNOWN")
        status_icon = {
            "OK": "✓",
            "WARNING": "⚠",
            "CRITICAL": "✗",
            "ERROR": "✗"
        }.get(status, "?")
        
        print(f"{status_icon} {check.get('name', 'Unknown Check')}")
        print(f"  Status: {status}")
        print(f"  Confidence: {check.get('confidence', 0):.1%}")
        print(f"  Message: {check.get('message', 'No message')}")
        
        # Print important details
        details = check.get("details", {})
        if details:
            if "issues" in details:
                issues = details["issues"]
                if isinstance(issues, dict):
                    for issue_type, issue_list in issues.items():
                        if issue_list:
                            print(f"  - {issue_type}: {len(issue_list)}")
            elif "found" in details:
                print(f"  - Found: {details.get('found', 'N/A')}")
        
        print()
    
    print("=" * 60)


def main():
    parser = argparse.ArgumentParser(
        description="Reality Check CLI for UMAJA"
    )
    parser.add_argument(
        "--check",
        choices=["backend_url", "bug_scan", "test_status", "deployment"],
        help="Run specific check only"
    )
    parser.add_argument(
        "--format",
        choices=["text", "json"],
        default="text",
        help="Output format"
    )
    parser.add_argument(
        "--watch",
        action="store_true",
        help="Run checks continuously"
    )
    parser.add_argument(
        "--interval",
        type=int,
        default=300,
        help="Interval between checks in watch mode (seconds)"
    )
    
    args = parser.parse_args()
    
    try:
        run_checks(
            check_name=args.check,
            format_type=args.format,
            watch=args.watch,
            interval=args.interval
        )
    except KeyboardInterrupt:
        print("\nStopped by user", file=sys.stderr)
        sys.exit(0)
    except Exception as e:
        print(f"Error running checks: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
