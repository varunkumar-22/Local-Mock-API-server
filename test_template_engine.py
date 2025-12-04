#!/usr/bin/env python3
"""
Tests for template engine {{variables}}
"""

import sys
import os
import re

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'server'))

from mock_server import TemplateEngine, MockServerConfig


def test_timestamp_template():
    """Test {{timestamp}} template."""
    print("Testing {{timestamp}} template...")
    
    config = MockServerConfig('config/config.json')
    result = TemplateEngine.render("{{timestamp}}", {}, config)
    
    # Check if it's a valid ISO timestamp format
    assert re.match(r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}', result), \
        "Timestamp should be in ISO format"
    
    print("✓ Timestamp template works")


def test_uuid_template():
    """Test {{uuid}} template."""
    print("Testing {{uuid}} template...")
    
    config = MockServerConfig('config/config.json')
    result = TemplateEngine.render("{{uuid}}", {}, config)
    
    # Check if it's a valid UUID format
    assert re.match(r'[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}', result), \
        "UUID should be in valid format"
    
    print("✓ UUID template works")


def test_random_int_template():
    """Test {{random_int}} template."""
    print("Testing {{random_int}} template...")
    
    config = MockServerConfig('config/config.json')
    result = TemplateEngine.render("{{random_int}}", {}, config)
    
    # Check if it's a valid integer
    assert result.isdigit(), "Random int should be a number"
    
    print("✓ Random int template works")


def test_query_param_template():
    """Test {{query.param}} template."""
    print("Testing {{query.param}} template...")
    
    config = MockServerConfig('config/config.json')
    query_params = {'name': ['Alice'], 'age': ['25']}
    
    result = TemplateEngine.render("Hello {{query.name}}, age {{query.age}}", query_params, config)
    
    assert result == "Hello Alice, age 25", f"Expected 'Hello Alice, age 25', got '{result}'"
    
    print("✓ Query param template works")


def test_database_template():
    """Test {{database}} template."""
    print("Testing {{database}} template...")
    
    config = MockServerConfig('config/config.json')
    result = TemplateEngine.render("{{database}}", {}, config)
    
    assert isinstance(result, list), "Database should return a list"
    assert len(result) > 0, "Database should not be empty"
    
    print(f"✓ Database template works ({len(result)} records)")


if __name__ == '__main__':
    test_timestamp_template()
    test_uuid_template()
    test_random_int_template()
    test_query_param_template()
    test_database_template()
    print("\n✅ All template tests passed!")
