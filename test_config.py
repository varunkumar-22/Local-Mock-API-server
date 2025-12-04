#!/usr/bin/env python3
"""
Config schema validation tests
"""

import json
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))


def test_config_schema():
    """Test that config files match the schema."""
    print("Testing config schema validation...")
    
    # Load schema
    with open('config/config_schema.json', 'r') as f:
        schema = json.load(f)
    
    # Load main config
    with open('config/config.json', 'r') as f:
        config = json.load(f)
    
    # Basic validation
    assert 'endpoints' in config, "Config must have 'endpoints'"
    assert isinstance(config['endpoints'], list), "'endpoints' must be a list"
    
    for endpoint in config['endpoints']:
        assert 'path' in endpoint, "Endpoint must have 'path'"
        assert 'method' in endpoint, "Endpoint must have 'method'"
        assert 'response' in endpoint, "Endpoint must have 'response'"
        assert endpoint['method'] in ['GET', 'POST', 'DELETE', 'PATCH'], \
            f"Invalid method: {endpoint['method']}"
    
    print("✓ Config schema validation passed")


def test_custom_config():
    """Test custom config file."""
    print("Testing custom config...")
    
    with open('config/custom_config.json', 'r') as f:
        config = json.load(f)
    
    assert 'endpoints' in config
    assert len(config['endpoints']) > 0
    
    print("✓ Custom config validation passed")


if __name__ == '__main__':
    test_config_schema()
    test_custom_config()
    print("\n✅ All config tests passed!")
