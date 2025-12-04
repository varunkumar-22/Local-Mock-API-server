#!/usr/bin/env python3
"""
Tests for GET/POST/filters endpoints
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

try:
    import requests
    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False
    print("Warning: 'requests' library not installed. Install with: pip install requests")


def test_all_endpoints():
    """Test all configured endpoints."""
    if not REQUESTS_AVAILABLE:
        print("Skipping endpoint tests - requests library not available")
        return
    
    base_url = "http://localhost:8000"
    
    tests = [
        ("GET /api/games", f"{base_url}/api/games"),
        ("GET /api/games/new-releases", f"{base_url}/api/games/new-releases"),
        ("GET /api/games/highest-rated", f"{base_url}/api/games/highest-rated"),
        ("GET /api/games/search", f"{base_url}/api/games/search?title=Minecraft"),
        ("GET /api/games/genre", f"{base_url}/api/games/genre?genre=RPG"),
        ("GET /api/health", f"{base_url}/api/health"),
    ]
    
    print("Testing endpoints...")
    for name, url in tests:
        try:
            response = requests.get(url, timeout=5)
            status = "✓" if response.status_code == 200 else "✗"
            print(f"{status} {name} - Status: {response.status_code}")
        except requests.exceptions.ConnectionError:
            print(f"✗ {name} - Server not running")
        except Exception as e:
            print(f"✗ {name} - Error: {e}")


if __name__ == '__main__':
    if not REQUESTS_AVAILABLE:
        print("Please install requests: pip install requests")
        sys.exit(1)
    
    test_all_endpoints()
