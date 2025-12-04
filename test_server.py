#!/usr/bin/env python3
"""
Test script for the mock server.
Run this after starting the server to verify functionality.
"""

import requests
import time
import json


def test_basic_endpoint():
    """Test basic GET endpoint."""
    print("Testing /api/users...")
    response = requests.get('http://localhost:8000/api/users')
    assert response.status_code == 200
    data = response.json()
    assert 'users' in data
    assert 'timestamp' in data
    print("Basic endpoint works")


def test_query_params():
    """Test query parameter templating."""
    print("Testing query parameters...")
    response = requests.get('http://localhost:8000/api/products?category=electronics')
    assert response.status_code == 200
    data = response.json()
    assert data['query_param'] == 'electronics'
    print("Query parameters work")


def test_latency():
    """Test latency simulation."""
    print("Testing latency simulation...")
    start = time.time()
    response = requests.get('http://localhost:8000/api/slow')
    elapsed = time.time() - start
    assert response.status_code == 200
    assert elapsed >= 2.0  # Should take at least 2 seconds
    print(f"Latency works (took {elapsed:.2f}s)")


def test_flaky_endpoint():
    """Test failure rate simulation."""
    print("Testing flaky endpoint (30% failure rate)...")
    success_count = 0
    failure_count = 0
    
    for _ in range(20):
        response = requests.get('http://localhost:8000/api/flaky')
        if response.status_code == 200:
            success_count += 1
        else:
            failure_count += 1
    
    print(f"   Success: {success_count}, Failures: {failure_count}")
    assert failure_count > 0  # Should have some failures
    print("Failure simulation works")


def test_post_endpoint():
    """Test POST endpoint."""
    print("Testing POST endpoint...")
    response = requests.post('http://localhost:8000/api/users', json={"name": "Test"})
    assert response.status_code == 201
    data = response.json()
    assert 'id' in data
    assert 'created_at' in data
    print("POST endpoint works")


def test_logs():
    """Test request logging."""
    print("Testing request logs...")
    response = requests.get('http://localhost:8000/__logs')
    assert response.status_code == 200
    data = response.json()
    assert 'logs' in data
    assert len(data['logs']) > 0
    print(f"Logging works ({data['count']} requests logged)")


def test_reload():
    """Test configuration reload."""
    print("Testing config reload...")
    response = requests.post('http://localhost:8000/__reload')
    assert response.status_code == 200
    data = response.json()
    assert 'message' in data
    print("Config reload works")


def test_cors():
    """Test CORS headers."""
    print("Testing CORS headers...")
    response = requests.get('http://localhost:8000/api/health')
    assert 'Access-Control-Allow-Origin' in response.headers
    print("CORS headers present")


def main():
    """Run all tests."""
    print("Starting Mock Server Tests\n")
    print("Make sure the server is running: python mock_server.py\n")
    
    try:
        test_basic_endpoint()
        test_query_params()
        test_post_endpoint()
        test_cors()
        test_logs()
        test_reload()
        test_latency()
        test_flaky_endpoint()
        
        print("\n All tests passed!")
    except requests.exceptions.ConnectionError:
        print("Could not connect to server. Is it running?")
    except AssertionError as e:
        print(f"Test failed: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")


if __name__ == '__main__':
    main()
