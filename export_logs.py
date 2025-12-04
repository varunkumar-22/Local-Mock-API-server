#!/usr/bin/env python3
"""
Export server logs to a file
"""

import requests
import json
import sys
from datetime import datetime


def export_logs(port=8000, output_file=None):
    """Export logs from server to file."""
    url = f"http://localhost:{port}/__logs"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        
        logs_data = response.json()
        
        if output_file is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_file = f"logs/exported_logs_{timestamp}.json"
        
        with open(output_file, 'w') as f:
            json.dump(logs_data, f, indent=2)
        
        print(f"✓ Exported {logs_data['count']} logs to {output_file}")
        
    except requests.exceptions.ConnectionError:
        print(f"✗ Could not connect to server on port {port}")
        sys.exit(1)
    except Exception as e:
        print(f"✗ Error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8000
    output = sys.argv[2] if len(sys.argv) > 2 else None
    
    export_logs(port, output)
