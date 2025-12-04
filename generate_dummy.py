#!/usr/bin/env python3
"""
Generate dummy endpoint configurations
"""

import json
import sys


def generate_dummy_config(num_endpoints=5):
    """Generate a dummy config with specified number of endpoints."""
    config = {
        "port": 8000,
        "cors": True,
        "endpoints": []
    }
    
    for i in range(1, num_endpoints + 1):
        endpoint = {
            "path": f"/api/dummy{i}",
            "method": "GET",
            "response": {
                "id": i,
                "message": f"Dummy endpoint {i}",
                "timestamp": "{{timestamp}}",
                "request_id": "{{uuid}}"
            },
            "status": 200,
            "latency_ms": 50,
            "failure_rate": 0.0
        }
        config["endpoints"].append(endpoint)
    
    return config


def main():
    """Main entry point."""
    num = int(sys.argv[1]) if len(sys.argv) > 1 else 5
    output_file = sys.argv[2] if len(sys.argv) > 2 else "config/dummy_config.json"
    
    config = generate_dummy_config(num)
    
    with open(output_file, 'w') as f:
        json.dump(config, f, indent=2)
    
    print(f"✓ Generated {num} dummy endpoints in {output_file}")


if __name__ == '__main__':
    main()
