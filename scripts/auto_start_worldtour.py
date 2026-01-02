#!/usr/bin/env python3
"""
Auto-start script for UMAJA World Tour
Automatically initiates the tour and visits the first 5 cities
"""
import requests
import time
import sys

BACKEND_URL = "https://umaja-core-production.up.railway.app"
# Fallback to local if Railway not available
LOCAL_URL = "http://localhost:5000"

def check_backend():
    """Check if backend is available"""
    for url in [BACKEND_URL, LOCAL_URL]:
        try:
            response = requests.get(f"{url}/health", timeout=5)
            if response.status_code == 200:
                print(f"✅ Backend available at {url}")
                return url
        except:
            continue
    return None

def start_worldtour(base_url):
    """Start the World Tour"""
    try:
        print("\n🌍 Starting UMAJA World Tour...")
        response = requests.post(f"{base_url}/worldtour/start", timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ World Tour Started!")
            print(f"   Next City: {data['next_city']['name']}, {data['next_city']['country']}")
            print(f"   Total Cities: {data['stats']['total_cities']}")
            return data['next_city']['id']
        else:
            print(f"❌ Failed to start tour: {response.status_code}")
            return None
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

def visit_city(base_url, city_id):
    """Visit a specific city"""
    try:
        print(f"\n🎭 Visiting {city_id}...")
        response = requests.post(
            f"{base_url}/worldtour/visit/{city_id}",
            json={"personality": "john_cleese", "content_type": "city_review"},
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Visited {data['city']['name']}!")
            if 'content' in data and 'topic' in data['content']:
                print(f"   Content: {data['content']['topic'][:100]}...")
            return True
        else:
            print(f"❌ Failed to visit {city_id}: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error visiting {city_id}: {e}")
        return False

def get_status(base_url):
    """Get current tour status"""
    try:
        response = requests.get(f"{base_url}/worldtour/status", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"\n📊 Tour Status:")
            print(f"   Visited: {data['stats']['visited_cities']}/{data['stats']['total_cities']}")
            print(f"   Progress: {data['stats']['completion_percentage']:.1f}%")
            return data
        return None
    except Exception as e:
        print(f"❌ Error getting status: {e}")
        return None

def main():
    print("="*60)
    print("🌍 UMAJA WORLD TOUR AUTO-START")
    print("="*60)
    
    # Check backend
    base_url = check_backend()
    if not base_url:
        print("❌ Backend not available. Please start the backend first.")
        sys.exit(1)
    
    # Start tour
    first_city = start_worldtour(base_url)
    if not first_city:
        print("❌ Could not start World Tour")
        sys.exit(1)
    
    # Visit first 5 cities
    print(f"\n🎬 Auto-visiting first 5 cities...")
    cities_to_visit = ["new_york", "london", "tokyo", "paris", "sydney"]
    
    for city in cities_to_visit:
        visit_city(base_url, city)
        time.sleep(2)  # Wait between requests
    
    # Show final status
    get_status(base_url)
    
    print("\n" + "="*60)
    print("🎉 WORLD TOUR LAUNCHED SUCCESSFULLY!")
    print("="*60)
    print(f"\n🌐 Dashboard: https://harrie19.github.io/UMAJA-Core/")
    print(f"🚂 API: {base_url}")
    print("\nUMAJA is now touring the world! 🌍✈️🎭\n")

if __name__ == "__main__":
    main()
