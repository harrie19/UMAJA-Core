#!/usr/bin/env python3
"""
UMAJA-Core Backend URL Verification Script
Tests the configured backend URL and CORS settings
"""

import requests
import sys
import json
from urllib.parse import urlparse

# Backend URL to test (should match docs/index.html line 324)
BACKEND_URL = "https://web-production-6ec45.up.railway.app"
FRONTEND_ORIGIN = "https://harrie19.github.io"

def test_health_endpoint():
    """Test the /health endpoint"""
    print(f"\n🔍 Testing backend health endpoint...")
    print(f"URL: {BACKEND_URL}/health")
    
    try:
        response = requests.get(
            f"{BACKEND_URL}/health",
            timeout=10,
            headers={
                "Origin": FRONTEND_ORIGIN,
                "User-Agent": "UMAJA-Core-Verification/1.0"
            }
        )
        
        print(f"✅ Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Response: {json.dumps(data, indent=2)}")
            
            # Check CORS headers
            cors_header = response.headers.get('Access-Control-Allow-Origin', 'NOT SET')
            print(f"\n🔒 CORS Header: {cors_header}")
            
            if cors_header == '*' or cors_header == FRONTEND_ORIGIN:
                print(f"✅ CORS properly configured for {FRONTEND_ORIGIN}")
            else:
                print(f"⚠️  CORS may not allow {FRONTEND_ORIGIN}")
            
            return True
        else:
            print(f"❌ Unexpected status code: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except requests.exceptions.ConnectionError:
        print(f"❌ Connection Error: Cannot reach {BACKEND_URL}")
        print(f"   Possible causes:")
        print(f"   1. Backend not deployed")
        print(f"   2. Wrong URL (verify at https://railway.app/dashboard)")
        print(f"   3. Network/firewall issue")
        return False
    except requests.exceptions.Timeout:
        print(f"❌ Timeout: Backend took too long to respond")
        return False
    except Exception as e:
        print(f"❌ Error: {type(e).__name__}: {e}")
        return False

def test_daily_smile_endpoint():
    """Test the /api/daily-smile endpoint"""
    print(f"\n🔍 Testing daily smile endpoint...")
    print(f"URL: {BACKEND_URL}/api/daily-smile")
    
    try:
        response = requests.get(
            f"{BACKEND_URL}/api/daily-smile",
            timeout=10,
            headers={
                "Origin": FRONTEND_ORIGIN,
                "User-Agent": "UMAJA-Core-Verification/1.0"
            }
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Daily smile endpoint working!")
            print(f"   Archetype: {data.get('archetype', 'unknown')}")
            print(f"   Content preview: {data.get('content', '')[:100]}...")
            return True
        else:
            print(f"⚠️  Status: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"⚠️  Could not test daily smile: {type(e).__name__}")
        return False

def test_worldtour_endpoint():
    """Test the /worldtour/status endpoint"""
    print(f"\n🔍 Testing World Tour endpoint...")
    print(f"URL: {BACKEND_URL}/worldtour/status")
    
    try:
        response = requests.get(
            f"{BACKEND_URL}/worldtour/status",
            timeout=10,
            headers={
                "Origin": FRONTEND_ORIGIN,
                "User-Agent": "UMAJA-Core-Verification/1.0"
            }
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ World Tour endpoint working!")
            if 'stats' in data:
                stats = data['stats']
                print(f"   Visited: {stats.get('visited_cities', 0)}/{stats.get('total_cities', 0)} cities")
                print(f"   Completion: {stats.get('completion_percentage', 0):.1f}%")
            return True
        else:
            print(f"⚠️  Status: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"⚠️  Could not test World Tour: {type(e).__name__}")
        return False

def main():
    """Run all verification tests"""
    print("=" * 60)
    print("UMAJA-Core Backend URL Verification")
    print("=" * 60)
    print(f"\n🎯 Backend URL: {BACKEND_URL}")
    print(f"🌐 Frontend Origin: {FRONTEND_ORIGIN}")
    print(f"📋 Testing connection and CORS configuration...")
    
    # Test health endpoint (critical)
    health_ok = test_health_endpoint()
    
    if not health_ok:
        print("\n" + "=" * 60)
        print("❌ BACKEND NOT ACCESSIBLE")
        print("=" * 60)
        print("\n📝 ACTION REQUIRED:")
        print("1. Verify Railway deployment is active")
        print("2. Check the actual URL at: https://railway.app/dashboard")
        print("3. If URL is different, update docs/index.html line 324")
        print("4. Ensure CORS allows: https://harrie19.github.io")
        print("\n💡 Expected URL format: https://web-production-6ec45.up.railway.app")
        print("⚠️  Previous wrong URL: https://web-production-6ec45.up.railway.app")
        sys.exit(1)
    
    # Test other endpoints (non-critical)
    test_daily_smile_endpoint()
    test_worldtour_endpoint()
    
    print("\n" + "=" * 60)
    print("✅ VERIFICATION COMPLETE - BACKEND ACCESSIBLE")
    print("=" * 60)
    print("\n✨ Dashboard should show:")
    print("   • Green 'Connected' status indicator")
    print("   • Backend version information")
    print("   • Working 'Get Daily Smile' button")
    print("   • World Tour status data")
    sys.exit(0)

if __name__ == "__main__":
    main()
