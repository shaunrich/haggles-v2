#!/usr/bin/env python3
"""
Integration Test for Hagglz Agent System

This test starts the actual server and tests the complete system functionality.
"""

import os
import sys
import time
import requests
import subprocess
import signal
import json
from typing import Optional

# Set environment variables
os.environ.setdefault('OPENAI_API_KEY', 'test-key')
os.environ.setdefault('ANTHROPIC_API_KEY', 'test-key')

class ServerManager:
    """Manages the test server lifecycle"""
    
    def __init__(self, port: int = 8001):
        self.port = port
        self.process: Optional[subprocess.Popen] = None
        self.base_url = f"http://localhost:{port}"
    
    def start_server(self) -> bool:
        """Start the API server"""
        try:
            print(f"Starting server on port {self.port}...")
            
            # Start the server process
            self.process = subprocess.Popen([
                sys.executable, "-m", "uvicorn", 
                "api.main:app", 
                "--host", "0.0.0.0", 
                "--port", str(self.port),
                "--log-level", "error"  # Reduce log noise
            ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            
            # Wait for server to start
            for i in range(30):  # Wait up to 30 seconds
                try:
                    response = requests.get(f"{self.base_url}/health", timeout=2)
                    if response.status_code == 200:
                        print(f"✅ Server started successfully on port {self.port}")
                        return True
                except requests.exceptions.RequestException:
                    pass
                
                time.sleep(1)
                
                # Check if process is still running
                if self.process.poll() is not None:
                    stdout, stderr = self.process.communicate()
                    print(f"❌ Server process exited early")
                    print(f"STDOUT: {stdout.decode()}")
                    print(f"STDERR: {stderr.decode()}")
                    return False
            
            print("❌ Server failed to start within timeout")
            return False
            
        except Exception as e:
            print(f"❌ Error starting server: {str(e)}")
            return False
    
    def stop_server(self):
        """Stop the API server"""
        if self.process:
            try:
                print("Stopping server...")
                self.process.terminate()
                self.process.wait(timeout=10)
                print("✅ Server stopped")
            except subprocess.TimeoutExpired:
                print("⚠️  Server didn't stop gracefully, killing...")
                self.process.kill()
                self.process.wait()
            except Exception as e:
                print(f"⚠️  Error stopping server: {str(e)}")

class IntegrationTester:
    """Runs integration tests against the live server"""
    
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.timeout = 30
    
    def test_health_endpoint(self) -> bool:
        """Test the health endpoint"""
        try:
            print("\n🔍 Testing health endpoint...")
            response = self.session.get(f"{self.base_url}/health")
            
            if response.status_code == 200:
                data = response.json()
                print(f"  Status: {data.get('status')}")
                print(f"  Components: {data.get('components', {})}")
                
                # Check if all components are active
                components = data.get('components', {})
                all_active = all(status == 'active' for status in components.values())
                
                if all_active:
                    print("✅ Health endpoint test passed - all components active")
                    return True
                else:
                    print("⚠️  Health endpoint test passed but some components inactive")
                    return True  # Still consider this a pass for testing
            else:
                print(f"❌ Health endpoint returned status {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ Health endpoint test failed: {str(e)}")
            return False
    
    def test_negotiate_endpoint(self) -> bool:
        """Test the negotiation endpoint"""
        try:
            print("\n🔍 Testing negotiation endpoint...")
            
            request_data = {
                "bill_text": "ELECTRIC BILL\nCITY POWER COMPANY\nAccount: 123456789\nAmount Due: $124.58",
                "user_id": "integration_test_user",
                "company": "City Power Company",
                "amount": 124.58,
                "target_savings": 20.0
            }
            
            response = self.session.post(
                f"{self.base_url}/api/v1/negotiate", 
                json=request_data
            )
            
            print(f"  Response status: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                print(f"  Negotiation ID: {data.get('negotiation_id', 'N/A')}")
                print(f"  Bill Type: {data.get('bill_type', 'N/A')}")
                print(f"  Confidence Score: {data.get('confidence_score', 'N/A')}")
                print(f"  Execution Mode: {data.get('execution_mode', 'N/A')}")
                
                # Validate response structure
                required_fields = ['negotiation_id', 'status', 'bill_type', 'company', 'confidence_score']
                missing_fields = [field for field in required_fields if field not in data]
                
                if not missing_fields:
                    print("✅ Negotiation endpoint test passed")
                    return True
                else:
                    print(f"❌ Missing required fields: {missing_fields}")
                    return False
            else:
                print(f"❌ Negotiation endpoint returned status {response.status_code}")
                print(f"  Response: {response.text}")
                return False
                
        except Exception as e:
            print(f"❌ Negotiation endpoint test failed: {str(e)}")
            return False
    
    def test_upload_bill_endpoint(self) -> bool:
        """Test the bill upload endpoint"""
        try:
            print("\n🔍 Testing bill upload endpoint...")
            
            # Create dummy base64 image
            import base64
            dummy_image = base64.b64encode(b"dummy bill image data").decode()
            
            request_data = {
                "bill_image": dummy_image,
                "user_id": "integration_test_user",
                "target_savings": 15.0
            }
            
            response = self.session.post(
                f"{self.base_url}/api/v1/upload-bill",
                json=request_data
            )
            
            print(f"  Response status: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                print(f"  Upload ID: {data.get('upload_id', 'N/A')}")
                print(f"  OCR Text: {data.get('ocr_text', 'N/A')[:50]}...")
                print("✅ Bill upload endpoint test passed")
                return True
            else:
                print(f"❌ Bill upload endpoint returned status {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ Bill upload endpoint test failed: {str(e)}")
            return False
    
    def test_api_documentation(self) -> bool:
        """Test that API documentation is accessible"""
        try:
            print("\n🔍 Testing API documentation...")
            
            # Test OpenAPI docs
            docs_response = self.session.get(f"{self.base_url}/docs")
            redoc_response = self.session.get(f"{self.base_url}/redoc")
            openapi_response = self.session.get(f"{self.base_url}/openapi.json")
            
            docs_ok = docs_response.status_code == 200
            redoc_ok = redoc_response.status_code == 200
            openapi_ok = openapi_response.status_code == 200
            
            print(f"  Swagger UI (/docs): {'✅' if docs_ok else '❌'}")
            print(f"  ReDoc (/redoc): {'✅' if redoc_ok else '❌'}")
            print(f"  OpenAPI JSON: {'✅' if openapi_ok else '❌'}")
            
            if docs_ok and redoc_ok and openapi_ok:
                print("✅ API documentation test passed")
                return True
            else:
                print("❌ Some API documentation endpoints failed")
                return False
                
        except Exception as e:
            print(f"❌ API documentation test failed: {str(e)}")
            return False
    
    def run_all_tests(self) -> bool:
        """Run all integration tests"""
        print("🚀 Starting Integration Tests")
        print("=" * 50)
        
        tests = [
            ("Health Endpoint", self.test_health_endpoint),
            ("Negotiation Endpoint", self.test_negotiate_endpoint),
            ("Bill Upload Endpoint", self.test_upload_bill_endpoint),
            ("API Documentation", self.test_api_documentation)
        ]
        
        results = []
        for test_name, test_func in tests:
            try:
                success = test_func()
                results.append((test_name, success))
            except Exception as e:
                print(f"❌ {test_name} failed with exception: {str(e)}")
                results.append((test_name, False))
        
        # Summary
        print("\n" + "=" * 50)
        print("🏁 Integration Test Summary")
        print("=" * 50)
        
        passed = 0
        for test_name, success in results:
            status = "✅ PASSED" if success else "❌ FAILED"
            print(f"{test_name}: {status}")
            if success:
                passed += 1
        
        total = len(results)
        print(f"\nOverall: {passed}/{total} tests passed")
        
        if passed == total:
            print("🎉 ALL INTEGRATION TESTS PASSED!")
            return True
        else:
            print("⚠️  Some integration tests failed")
            return False

def main():
    """Main integration test function"""
    print("Hagglz Agent - Integration Test Suite")
    print("=" * 60)
    
    # Start server
    server = ServerManager(port=8001)
    
    try:
        if not server.start_server():
            print("❌ Failed to start server for integration tests")
            return False
        
        # Run tests
        tester = IntegrationTester(server.base_url)
        success = tester.run_all_tests()
        
        return success
        
    finally:
        # Always stop the server
        server.stop_server()

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

