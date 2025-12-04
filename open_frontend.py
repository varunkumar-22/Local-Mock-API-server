#!/usr/bin/env python3
"""
Open the frontend testing interface in the default browser
"""

import webbrowser
import time
import sys

def main():
    url = "http://localhost:8000"
    
    print("Opening frontend testing interface...")
    print(f"URL: {url}")
    print("\nMake sure the server is running with: python main.py")
    
    # Wait a moment for server to be ready
    time.sleep(1)
    
    # Open browser
    try:
        webbrowser.open(url)
        print("✓ Browser opened successfully")
    except Exception as e:
        print(f"✗ Could not open browser: {e}")
        print(f"Please manually navigate to: {url}")
        sys.exit(1)

if __name__ == '__main__':
    main()
