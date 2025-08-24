#!/usr/bin/env python3
"""
Simple API Test Script

Quick test to verify the API can be imported and basic functionality works.
"""

import sys
import os
import json

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_api_import():
    """Test that the API can be imported"""
    try:
        from fastapi.testclient import TestClient
        from api.main import app
        
        client = TestClient(app)
        print("✅ API import successful")
        return client
    except Exception as e:
        print(f"❌ API import failed: {str(e)}")
        return None

def test_health_endpoint(client):
    """Test the health endpoint"""
    try:
        response = client.get("/health")
        print(f"Health endpoint status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"Health response: {json.dumps(data, indent=2)}")
            print("✅ Health endpoint test passed")
            return True
        else:
            print("❌ Health endpoint test failed")
            return False
    except Exception as e:
        print(f"❌ Health endpoint error: {str(e)}")
        return False

def test_negotiate_endpoint(client):
    """Test the negotiate endpoint"""
    try:
        request_data = {
            "bill_text": "TEST ELECTRIC BILL\nCITY POWER COMPANY\nAmount Due: $124.58",
            "user_id": "test_user_123",
            "company": "City Power Company",
            "amount": 124.58,
            "target_savings": 20.0
        }
        
        response = client.post("/api/v1/negotiate", json=request_data)
        print(f"Negotiate endpoint status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"Negotiate response keys: {list(data.keys())}")
            print("✅ Negotiate endpoint test passed")
            return True
        else:
            print(f"❌ Negotiate endpoint test failed: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Negotiate endpoint error: {str(e)}")
        return False

def main():
    """Run simple API tests"""
    print("Hagglz API - Simple Test Suite")
    print("=" * 40)
    
    # Set environment variables
    os.environ.setdefault('OPENAI_API_KEY', 'test-key')
    os.environ.setdefault('ANTHROPIC_API_KEY', 'test-key')
    
    # Test API import
    client = test_api_import()
    if not client:
        print("Cannot proceed with tests - API import failed")
        return False
    
    # Test health endpoint
    health_ok = test_health_endpoint(client)
    
    # Test negotiate endpoint
    negotiate_ok = test_negotiate_endpoint(client)
    
    # Summary
    print("\n" + "=" * 40)
    print("Test Summary:")
    print(f"Health endpoint: {'✅ PASSED' if health_ok else '❌ FAILED'}")
    print(f"Negotiate endpoint: {'✅ PASSED' if negotiate_ok else '❌ FAILED'}")
    
    all_passed = health_ok and negotiate_ok
    print(f"\nOverall: {'✅ ALL TESTS PASSED' if all_passed else '❌ SOME TESTS FAILED'}")
    
    return all_passed

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

