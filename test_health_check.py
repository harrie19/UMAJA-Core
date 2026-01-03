#!/usr/bin/env python3
"""
Simple test script to check if UMAJA-Core services are accessible
Created: 2026-01-03
"""

import urllib.request
import urllib.error
import sys
from datetime import datetime

def check_url(url, description):
    """
    Check if a URL is accessible and responding
    
    Args:
        url: The URL to check
        description: A description of what this URL is
    
    Returns:
        bool: True if accessible, False otherwise
    """
    print(f"\n{'='*60}")
    print(f"Testing: {description}")
    print(f"URL: {url}")
    print(f"{'='*60}")
    
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'UMAJA-Core-Health-Check/1.0'})
        with urllib.request.urlopen(req, timeout=10) as response:
            status_code = response.getcode()
            content_length = len(response.read())
            
            print(f"✓ Status Code: {status_code}")
            print(f"✓ Content Length: {content_length} bytes")
            print(f"✓ {description} is ACCESSIBLE")
            return True
            
    except urllib.error.HTTPError as e:
        print(f"✗ HTTP Error: {e.code} - {e.reason}")
        print(f"✗ {description} returned an error")
        return False
        
    except urllib.error.URLError as e:
        print(f"✗ URL Error: {e.reason}")
        print(f"✗ {description} is NOT ACCESSIBLE")
        return False
        
    except Exception as e:
        print(f"✗ Unexpected Error: {str(e)}")
        print(f"✗ {description} check FAILED")
        return False

def main():
    """Main test function"""
    print("\n" + "="*60)
    print("UMAJA-Core Health Check Script")
    print(f"Timestamp: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')} UTC")
    print("="*60)
    
    # Define URLs to check
    tests = [
        {
            'url': 'https://umaja-core-production.up.railway.app/health',
            'description': 'Railway Production Health Endpoint'
        },
        {
            'url': 'https://harrie19.github.io/UMAJA-Core/',
            'description': 'GitHub Pages Site'
        }
    ]
    
    # Run all tests
    results = []
    for test in tests:
        result = check_url(test['url'], test['description'])
        results.append(result)
    
    # Summary
    print(f"\n{'='*60}")
    print("SUMMARY")
    print(f"{'='*60}")
    passed = sum(results)
    total = len(results)
    print(f"Tests Passed: {passed}/{total}")
    
    for i, test in enumerate(tests):
        status = "✓ PASS" if results[i] else "✗ FAIL"
        print(f"{status} - {test['description']}")
    
    print(f"{'='*60}\n")
    
    # Exit with appropriate code
    if all(results):
        print("All checks passed! ✓")
        sys.exit(0)
    else:
        print("Some checks failed! ✗")
        sys.exit(1)

if __name__ == "__main__":
    main()
