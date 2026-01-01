#!/usr/bin/env python3
"""
UMAJA-Core Deployment Verification Script
Run locally to verify the deployment is live and working

Usage:
    python scripts/verify_deployment.py
"""

import sys
import requests
from datetime import datetime

# URLs to check
BACKEND_URL = "https://umaja-core.onrender.com"
FRONTEND_URL = "https://harrie19.github.io/UMAJA-Core/"

# Colors for terminal output
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
BOLD = '\033[1m'
RESET = '\033[0m'

def print_header():
    """Print fancy header"""
    print()
    print("=" * 70)
    print(f"{BOLD}{BLUE}🚀 UMAJA-Core Deployment Verification{RESET}")
    print("=" * 70)
    print()

def print_success(message):
    """Print success message"""
    print(f"{GREEN}✅ {message}{RESET}")

def print_error(message):
    """Print error message"""
    print(f"{RED}❌ {message}{RESET}")

def print_warning(message):
    """Print warning message"""
    print(f"{YELLOW}⚠️  {message}{RESET}")

def print_info(message):
    """Print info message"""
    print(f"{BLUE}ℹ️  {message}{RESET}")

def check_backend_health():
    """Check if backend is healthy"""
    print(f"\n{BOLD}1. Checking Backend Health...{RESET}")
    print(f"   URL: {BACKEND_URL}/health")
    
    try:
        response = requests.get(f"{BACKEND_URL}/health", timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            print_success(f"Backend is alive!")
            print(f"   Mission: {data.get('mission', 'N/A')}")
            print(f"   Status: {data.get('status', 'N/A')}")
            print(f"   Service: {data.get('service', 'N/A')}")
            return True
        else:
            print_error(f"Backend returned HTTP {response.status_code}")
            return False
    
    except requests.exceptions.Timeout:
        print_warning("Backend timed out (may be starting up on free tier)")
        print_info("Render free tier takes 1-2 minutes to wake from sleep")
        return False
    
    except Exception as e:
        print_error(f"Backend check failed: {e}")
        return False

def check_daily_smile():
    """Check if daily smile endpoint works"""
    print(f"\n{BOLD}2. Testing Daily Smile API...{RESET}")
    print(f"   URL: {BACKEND_URL}/api/daily-smile")
    
    try:
        response = requests.get(f"{BACKEND_URL}/api/daily-smile", timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            
            if data.get('success'):
                smile = data.get('smile', {})
                print_success("Daily Smile API works!")
                print(f"   Personality: {smile.get('personality', 'N/A')}")
                print(f"   Tone: {smile.get('tone', 'N/A')}")
                print(f"   Content: {smile.get('content', '')[:80]}...")
                return True
            else:
                print_error("API returned success=false")
                return False
        else:
            print_error(f"API returned HTTP {response.status_code}")
            return False
    
    except Exception as e:
        print_error(f"Daily smile check failed: {e}")
        return False

def check_generate_api():
    """Check if generate endpoint works"""
    print(f"\n{BOLD}3. Testing Custom Generate API...{RESET}")
    print(f"   URL: {BACKEND_URL}/api/generate")
    
    try:
        payload = {
            "archetype": "professor",
            "topic": "deployment test"
        }
        
        response = requests.post(
            f"{BACKEND_URL}/api/generate",
            json=payload,
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            
            if data.get('success'):
                print_success("Generate API works!")
                smile = data.get('smile', {})
                print(f"   Generated personality: {smile.get('personality', 'N/A')}")
                return True
            else:
                print_error("API returned success=false")
                return False
        else:
            print_error(f"API returned HTTP {response.status_code}")
            return False
    
    except Exception as e:
        print_error(f"Generate API check failed: {e}")
        return False

def check_frontend():
    """Check if frontend is accessible"""
    print(f"\n{BOLD}4. Checking Frontend...{RESET}")
    print(f"   URL: {FRONTEND_URL}")
    
    try:
        response = requests.get(FRONTEND_URL, timeout=10)
        
        if response.status_code == 200:
            # Check if it contains expected content
            if 'UMAJA-Core' in response.text and '8 Billion' in response.text:
                print_success("Frontend is live and contains expected content!")
                return True
            else:
                print_warning("Frontend loads but content may be incorrect")
                return True
        else:
            print_error(f"Frontend returned HTTP {response.status_code}")
            return False
    
    except Exception as e:
        print_error(f"Frontend check failed: {e}")
        print_info("Make sure GitHub Pages is enabled in repository settings")
        return False

def print_summary(results):
    """Print final summary"""
    print()
    print("=" * 70)
    print(f"{BOLD}📊 Verification Summary{RESET}")
    print("=" * 70)
    
    backend_health = results.get('backend_health', False)
    daily_smile = results.get('daily_smile', False)
    generate_api = results.get('generate_api', False)
    frontend = results.get('frontend', False)
    
    all_passed = backend_health and daily_smile and generate_api and frontend
    
    print(f"\n{'✅' if backend_health else '❌'} Backend Health: {'PASSED' if backend_health else 'FAILED'}")
    print(f"{'✅' if daily_smile else '❌'} Daily Smile API: {'PASSED' if daily_smile else 'FAILED'}")
    print(f"{'✅' if generate_api else '❌'} Generate API: {'PASSED' if generate_api else 'FAILED'}")
    print(f"{'✅' if frontend else '❌'} Frontend: {'PASSED' if frontend else 'FAILED'}")
    
    print()
    print("=" * 70)
    
    if all_passed:
        print(f"{BOLD}{GREEN}")
        print("🎉 UMAJA IS LIVE! 🎉")
        print(f"{RESET}")
        print("Backend: Live at", BACKEND_URL)
        print("Frontend: Live at", FRONTEND_URL)
        print()
        print("Mission: Bringing smiles to 8 billion people ✅")
        print()
        print("\"Let deeds, not words, be your adorning.\" - Bahá'u'lláh")
        print("=" * 70)
        return 0
    else:
        print(f"{BOLD}{YELLOW}")
        print("⚠️  Some checks failed")
        print(f"{RESET}")
        print()
        print("Troubleshooting:")
        
        if not backend_health:
            print("- Backend: Check Render dashboard, may be starting up")
        if not (daily_smile and generate_api):
            print("- APIs: Backend may be online but endpoints failing")
        if not frontend:
            print("- Frontend: Enable GitHub Pages in Settings → Pages")
        
        print()
        print("See docs/DEPLOYMENT_GUIDE.md for detailed troubleshooting")
        print("=" * 70)
        return 1

def main():
    """Main verification flow"""
    print_header()
    
    results = {
        'backend_health': check_backend_health(),
        'daily_smile': check_daily_smile(),
        'generate_api': check_generate_api(),
        'frontend': check_frontend()
    }
    
    return print_summary(results)

if __name__ == '__main__':
    sys.exit(main())
