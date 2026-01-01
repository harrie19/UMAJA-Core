#!/usr/bin/env python3
"""
UMAJA Deployment Verification Script

Tests that both backend and frontend deployments are working correctly.
Run this locally to verify deployments before/after changes.

Philosophy: "Let deeds, not words, be your adorning" - Bahá'u'lláh
We verify through action, not assumption.
"""

import sys
import os
import requests
import json
from datetime import datetime
from typing import Dict, Tuple, Optional

# Color codes for terminal output
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    END = '\033[0m'

# Deployment URLs - can be overridden via environment variables
BACKEND_URL = os.environ.get("UMAJA_BACKEND_URL", "https://umaja-core-production.up.railway.app")
FRONTEND_URL = os.environ.get("UMAJA_FRONTEND_URL", "https://harrie19.github.io/UMAJA-Core/")

def print_header(text: str) -> None:
    """Print a colored header"""
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'=' * 60}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.CYAN}{text}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}{'=' * 60}{Colors.END}\n")

def print_success(text: str) -> None:
    """Print success message"""
    print(f"{Colors.GREEN}✅ {text}{Colors.END}")

def print_error(text: str) -> None:
    """Print error message"""
    print(f"{Colors.RED}❌ {text}{Colors.END}")

def print_warning(text: str) -> None:
    """Print warning message"""
    print(f"{Colors.YELLOW}⚠️  {text}{Colors.END}")

def print_info(text: str) -> None:
    """Print info message"""
    print(f"{Colors.BLUE}ℹ️  {text}{Colors.END}")

def check_backend_health() -> Tuple[bool, Optional[Dict]]:
    """
    Check if backend /health endpoint is responding
    
    Returns:
        Tuple of (success: bool, health_data: dict or None)
    """
    print_info(f"Checking backend health: {BACKEND_URL}/health")
    print_info("(Waiting up to 15 seconds for cold start...)")
    
    try:
        response = requests.get(
            f"{BACKEND_URL}/health",
            timeout=15
        )
        
        if response.status_code == 200:
            health_data = response.json()
            print_success(f"Backend is healthy! (HTTP {response.status_code})")
            print(f"  Version: {health_data.get('version', 'unknown')}")
            print(f"  Mission: {health_data.get('mission', 'unknown')}")
            print(f"  Timestamp: {health_data.get('timestamp', 'unknown')}")
            
            # Check individual health checks
            checks = health_data.get('checks', {})
            for check_name, check_status in checks.items():
                if check_status == 'ok' or check_status is True:
                    print(f"  ✓ {check_name}: OK")
                else:
                    print(f"  ✗ {check_name}: {check_status}")
            
            return True, health_data
        else:
            print_error(f"Backend health check failed (HTTP {response.status_code})")
            print(f"  Response: {response.text[:200]}")
            return False, None
            
    except requests.exceptions.Timeout:
        print_error("Backend health check timed out (>15 seconds)")
        print_warning("This could indicate:")
        print("    - Backend is down")
        print("    - Cold start is taking too long")
        print("    - Network connectivity issues")
        return False, None
        
    except requests.exceptions.ConnectionError:
        print_error("Could not connect to backend")
        print_warning("This could indicate:")
        print("    - Backend is not deployed")
        print("    - DNS resolution failed")
        print("    - Network is unreachable")
        return False, None
        
    except Exception as e:
        print_error(f"Unexpected error checking backend: {str(e)}")
        return False, None

def test_daily_smile_endpoint() -> bool:
    """
    Test /api/daily-smile endpoint
    
    Returns:
        bool: True if endpoint works correctly
    """
    print_info(f"Testing daily smile endpoint: {BACKEND_URL}/api/daily-smile")
    
    try:
        response = requests.get(
            f"{BACKEND_URL}/api/daily-smile",
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            print_success("Daily smile endpoint working!")
            print(f"  Archetype: {data.get('archetype', 'unknown')}")
            print(f"  Content: \"{data.get('content', 'unknown')[:80]}...\"")
            print(f"  Mission: {data.get('mission', 'unknown')}")
            return True
        else:
            print_error(f"Daily smile endpoint failed (HTTP {response.status_code})")
            print(f"  Response: {response.text[:200]}")
            return False
            
    except Exception as e:
        print_error(f"Error testing daily smile endpoint: {str(e)}")
        return False

def test_generate_endpoint() -> bool:
    """
    Test /api/smile/<archetype> endpoints
    
    Returns:
        bool: True if all archetypes work
    """
    print_info("Testing archetype-specific endpoints...")
    
    archetypes = ["professor", "worrier", "enthusiast"]
    all_passed = True
    
    for archetype in archetypes:
        try:
            response = requests.get(
                f"{BACKEND_URL}/api/smile/{archetype}",
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                print(f"  ✓ {archetype}: OK")
            else:
                print(f"  ✗ {archetype}: Failed (HTTP {response.status_code})")
                all_passed = False
                
        except Exception as e:
            print(f"  ✗ {archetype}: Error - {str(e)}")
            all_passed = False
    
    if all_passed:
        print_success("All archetype endpoints working!")
    else:
        print_error("Some archetype endpoints failed")
    
    return all_passed

def check_frontend() -> bool:
    """
    Check if frontend is accessible
    
    Returns:
        bool: True if frontend loads successfully
    """
    print_info(f"Checking frontend: {FRONTEND_URL}")
    
    try:
        response = requests.get(
            FRONTEND_URL,
            timeout=10
        )
        
        if response.status_code == 200:
            html = response.text
            
            # Check for expected content
            if "UMAJA" in html:
                print_success("Frontend is accessible!")
                print("  ✓ Contains UMAJA branding")
                
                # Check for other expected elements
                checks = {
                    "dashboard": "dashboard" in html.lower() or "status" in html.lower(),
                    "backend_url": BACKEND_URL in html or "railway" in html.lower(),
                }
                
                for check_name, check_result in checks.items():
                    if check_result:
                        print(f"  ✓ {check_name}: Found")
                    else:
                        print(f"  ⚠ {check_name}: Not found (may be OK)")
                
                return True
            else:
                print_warning("Frontend loaded but missing UMAJA content")
                return False
        else:
            print_error(f"Frontend check failed (HTTP {response.status_code})")
            return False
            
    except requests.exceptions.Timeout:
        print_error("Frontend request timed out")
        return False
        
    except requests.exceptions.ConnectionError:
        print_error("Could not connect to frontend")
        return False
        
    except Exception as e:
        print_error(f"Error checking frontend: {str(e)}")
        return False

def print_summary(backend_ok: bool, api_ok: bool, frontend_ok: bool) -> None:
    """Print verification summary"""
    print_header("📊 VERIFICATION SUMMARY")
    
    print(f"Backend Health:     {'✅ PASS' if backend_ok else '❌ FAIL'}")
    print(f"API Endpoints:      {'✅ PASS' if api_ok else '❌ FAIL'}")
    print(f"Frontend:           {'✅ PASS' if frontend_ok else '❌ FAIL'}")
    print()
    
    if backend_ok and api_ok and frontend_ok:
        print(f"{Colors.BOLD}{Colors.GREEN}")
        print("🎉 " + "=" * 56 + " 🎉")
        print("   UMAJA IS LIVE!")
        print("   Serving 8 billion people with Truth, Unity, and Service")
        print("🎉 " + "=" * 56 + " 🎉")
        print(Colors.END)
        print()
        print("✨ All systems operational ✨")
        print()
        print("Quick Links:")
        print(f"  🌐 Dashboard: {FRONTEND_URL}")
        print(f"  🔌 API: {BACKEND_URL}")
        print(f"  💚 Health: {BACKEND_URL}/health")
        print(f"  😊 Smile: {BACKEND_URL}/api/daily-smile")
        
    else:
        print(f"{Colors.BOLD}{Colors.RED}")
        print("⚠️  DEPLOYMENT ISSUES DETECTED")
        print(Colors.END)
        print()
        print("Troubleshooting tips:")
        
        if not backend_ok:
            print(f"{Colors.YELLOW}Backend Issues:{Colors.END}")
            print("  1. Check Railway deployment status")
            print("  2. Review backend logs for errors")
            print("  3. Verify environment variables are set")
            print("  4. Check if backend is sleeping (cold start)")
            print()
        
        if not api_ok:
            print(f"{Colors.YELLOW}API Issues:{Colors.END}")
            print("  1. Test endpoints manually with curl")
            print("  2. Check for recent code changes")
            print("  3. Verify API routes are registered")
            print("  4. Check CORS configuration")
            print()
        
        if not frontend_ok:
            print(f"{Colors.YELLOW}Frontend Issues:{Colors.END}")
            print("  1. Check GitHub Pages deployment status")
            print("  2. Verify docs/index.html exists")
            print("  3. Check GitHub Actions workflow")
            print("  4. Clear browser cache and retry")
            print()

def main() -> int:
    """
    Main verification function
    
    Returns:
        int: Exit code (0 = success, 1 = failure)
    """
    print_header("🌍 UMAJA DEPLOYMENT VERIFICATION")
    print(f"Timestamp: {datetime.utcnow().isoformat()}Z")
    print(f"Mission: Bringing smiles to 8 billion people")
    print(f"Philosophy: Bahá'í principles of Truth, Unity, Service")
    
    # Run checks
    backend_ok, health_data = check_backend_health()
    print()
    
    api_ok = False
    if backend_ok:
        daily_smile_ok = test_daily_smile_endpoint()
        print()
        generate_ok = test_generate_endpoint()
        print()
        api_ok = daily_smile_ok and generate_ok
    else:
        print_warning("Skipping API tests (backend unhealthy)")
        print()
    
    frontend_ok = check_frontend()
    print()
    
    # Print summary
    print_summary(backend_ok, api_ok, frontend_ok)
    
    # Return exit code
    if backend_ok and api_ok and frontend_ok:
        return 0
    else:
        return 1

if __name__ == "__main__":
    try:
        exit_code = main()
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}Verification interrupted by user{Colors.END}")
        sys.exit(1)
    except Exception as e:
        print(f"\n{Colors.RED}Unexpected error: {str(e)}{Colors.END}")
        sys.exit(1)
