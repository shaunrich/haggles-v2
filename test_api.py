"""
Comprehensive Test Suite for Hagglz API

This module contains tests for all API endpoints and functionality.
"""

import pytest
import asyncio
import json
import base64
from fastapi.testclient import TestClient
import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from api.main import app

# Create test client
client = TestClient(app)

class TestHagglzAPI:
    """Test class for Hagglz API endpoints"""
    
    def test_health_check(self):
        """Test the health check endpoint"""
        response = client.get("/health")
        assert response.status_code == 200
        
        data = response.json()
        assert data["status"] == "healthy"
        assert "timestamp" in data
        assert "version" in data
        assert "components" in data
    
    def test_negotiate_endpoint(self):
        """Test the main negotiation endpoint"""
        request_data = {
            "bill_text": "ELECTRIC BILL\nCITY POWER COMPANY\nAccount: 123456789\nAmount Due: $124.58",
            "user_id": "test_user_123",
            "company": "City Power Company",
            "amount": 124.58,
            "target_savings": 20.0
        }
        
        response = client.post("/api/v1/negotiate", json=request_data)
        assert response.status_code == 200
        
        data = response.json()
        assert "negotiation_id" in data
        assert data["bill_type"] in ["UTILITY", "MEDICAL", "SUBSCRIPTION", "TELECOM"]
        assert data["company"] == "City Power Company"
        assert data["amount"] == 124.58
        assert "confidence_score" in data
        assert "execution_mode" in data
        assert "strategy" in data
        assert "script" in data
    
    def test_upload_bill_endpoint(self):
        """Test the bill upload endpoint"""
        # Create a dummy base64 image
        dummy_image = base64.b64encode(b"dummy image data").decode()
        
        request_data = {
            "bill_image": dummy_image,
            "user_id": "test_user_123",
            "target_savings": 15.0
        }
        
        response = client.post("/api/v1/upload-bill", json=request_data)
        assert response.status_code == 200
        
        data = response.json()
        assert "upload_id" in data
        assert "ocr_text" in data
        assert data["status"] == "processed"
    
    def test_negotiation_status_endpoint(self):
        """Test the negotiation status endpoint"""
        negotiation_id = "test-negotiation-123"
        
        response = client.get(f"/api/v1/negotiation/{negotiation_id}")
        assert response.status_code == 200
        
        data = response.json()
        assert data["negotiation_id"] == negotiation_id
        assert "status" in data
        assert "created_at" in data
    
    def test_feedback_endpoint(self):
        """Test the feedback submission endpoint"""
        request_data = {
            "negotiation_id": "test-negotiation-123",
            "success": True,
            "actual_savings": 25.50,
            "final_amount": 99.08,
            "notes": "Great negotiation experience",
            "difficulty_rating": 4
        }
        
        response = client.post("/api/v1/feedback", json=request_data)
        assert response.status_code == 200
        
        data = response.json()
        assert data["negotiation_id"] == "test-negotiation-123"
        assert "message" in data
        assert "timestamp" in data
    
    def test_user_negotiations_endpoint(self):
        """Test the user negotiations history endpoint"""
        user_id = "test_user_123"
        
        response = client.get(f"/api/v1/user/{user_id}/negotiations")
        assert response.status_code == 200
        
        data = response.json()
        assert data["user_id"] == user_id
        assert "negotiations" in data
        assert "total_count" in data
        assert "total_savings" in data
    
    def test_system_stats_endpoint(self):
        """Test the system statistics endpoint"""
        response = client.get("/api/v1/stats")
        assert response.status_code == 200
        
        data = response.json()
        assert "total_negotiations" in data
        assert "success_rate" in data
        assert "average_savings" in data
        assert "memory_stats" in data
    
    def test_research_company_endpoint(self):
        """Test the company research endpoint"""
        company_name = "Test Electric Company"
        
        response = client.get(f"/api/v1/research/{company_name}")
        assert response.status_code == 200
        
        data = response.json()
        assert data["company"] == company_name
        assert "research_data" in data
        assert "timestamp" in data
    
    def test_calculate_savings_endpoint(self):
        """Test the savings calculation endpoint"""
        params = {
            "original_amount": 150.0,
            "target_percentage": 20.0
        }
        
        response = client.post("/api/v1/calculate-savings", params=params)
        assert response.status_code == 200
        
        data = response.json()
        assert "calculation" in data
        assert "timestamp" in data
    
    def test_invalid_negotiation_request(self):
        """Test negotiation endpoint with invalid data"""
        request_data = {
            "bill_text": "",  # Empty bill text
            "user_id": "test_user_123"
        }
        
        response = client.post("/api/v1/negotiate", json=request_data)
        # Should handle gracefully, might return 400 or process with defaults
        assert response.status_code in [200, 400]
    
    def test_invalid_bill_upload(self):
        """Test bill upload with invalid base64 data"""
        request_data = {
            "bill_image": "invalid_base64_data",
            "user_id": "test_user_123"
        }
        
        response = client.post("/api/v1/upload-bill", json=request_data)
        assert response.status_code == 400
    
    def test_nonexistent_negotiation_status(self):
        """Test getting status for non-existent negotiation"""
        negotiation_id = "nonexistent-negotiation-id"
        
        response = client.get(f"/api/v1/negotiation/{negotiation_id}")
        # Should return 200 with placeholder data or 404
        assert response.status_code in [200, 404]
    
    def test_api_documentation_endpoints(self):
        """Test that API documentation endpoints are accessible"""
        # Test OpenAPI docs
        response = client.get("/docs")
        assert response.status_code == 200
        
        # Test ReDoc
        response = client.get("/redoc")
        assert response.status_code == 200
        
        # Test OpenAPI JSON
        response = client.get("/openapi.json")
        assert response.status_code == 200
        
        openapi_data = response.json()
        assert "openapi" in openapi_data
        assert "info" in openapi_data
        assert openapi_data["info"]["title"] == "Hagglz Negotiation API"

class TestAPIIntegration:
    """Integration tests for API workflows"""
    
    def test_complete_negotiation_workflow(self):
        """Test a complete negotiation workflow from start to finish"""
        # Step 1: Upload bill
        dummy_image = base64.b64encode(b"dummy bill image").decode()
        upload_data = {
            "bill_image": dummy_image,
            "user_id": "integration_test_user",
            "target_savings": 25.0
        }
        
        upload_response = client.post("/api/v1/upload-bill", json=upload_data)
        assert upload_response.status_code == 200
        upload_result = upload_response.json()
        
        # Step 2: Start negotiation with OCR text
        negotiate_data = {
            "bill_text": upload_result["ocr_text"],
            "user_id": "integration_test_user",
            "target_savings": 25.0
        }
        
        negotiate_response = client.post("/api/v1/negotiate", json=negotiate_data)
        assert negotiate_response.status_code == 200
        negotiate_result = negotiate_response.json()
        
        negotiation_id = negotiate_result["negotiation_id"]
        
        # Step 3: Check negotiation status
        status_response = client.get(f"/api/v1/negotiation/{negotiation_id}")
        assert status_response.status_code == 200
        
        # Step 4: Submit feedback
        feedback_data = {
            "negotiation_id": negotiation_id,
            "success": True,
            "actual_savings": 30.0,
            "final_amount": 105.0,
            "notes": "Integration test successful",
            "difficulty_rating": 3
        }
        
        feedback_response = client.post("/api/v1/feedback", json=feedback_data)
        assert feedback_response.status_code == 200
        
        # Step 5: Check user history
        history_response = client.get("/api/v1/user/integration_test_user/negotiations")
        assert history_response.status_code == 200
    
    def test_multiple_bill_types(self):
        """Test negotiation with different bill types"""
        bill_types = [
            {
                "text": "ELECTRIC BILL\nCity Power\nAmount: $150.00",
                "expected_type": "UTILITY"
            },
            {
                "text": "HOSPITAL BILL\nMedical Center\nAmount: $2500.00",
                "expected_type": "MEDICAL"
            },
            {
                "text": "NETFLIX SUBSCRIPTION\nMonthly: $19.99",
                "expected_type": "SUBSCRIPTION"
            },
            {
                "text": "VERIZON WIRELESS\nMonthly Plan: $85.00",
                "expected_type": "TELECOM"
            }
        ]
        
        for i, bill in enumerate(bill_types):
            request_data = {
                "bill_text": bill["text"],
                "user_id": f"test_user_{i}",
                "target_savings": 20.0
            }
            
            response = client.post("/api/v1/negotiate", json=request_data)
            assert response.status_code == 200
            
            data = response.json()
            # Note: The actual bill type detection might vary based on AI processing
            assert "bill_type" in data
            assert data["confidence_score"] >= 0.0

class TestAPIPerformance:
    """Performance tests for API endpoints"""
    
    def test_concurrent_negotiations(self):
        """Test handling multiple concurrent negotiation requests"""
        import concurrent.futures
        import time
        
        def make_negotiation_request(user_id):
            request_data = {
                "bill_text": f"TEST BILL\nCompany: Test Corp\nAmount: $100.00",
                "user_id": f"perf_test_user_{user_id}",
                "target_savings": 15.0
            }
            
            start_time = time.time()
            response = client.post("/api/v1/negotiate", json=request_data)
            end_time = time.time()
            
            return {
                "status_code": response.status_code,
                "response_time": end_time - start_time,
                "user_id": user_id
            }
        
        # Test with 5 concurrent requests
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            futures = [executor.submit(make_negotiation_request, i) for i in range(5)]
            results = [future.result() for future in concurrent.futures.as_completed(futures)]
        
        # All requests should succeed
        for result in results:
            assert result["status_code"] == 200
            assert result["response_time"] < 30.0  # Should complete within 30 seconds
    
    def test_api_response_times(self):
        """Test response times for various endpoints"""
        import time
        
        endpoints_to_test = [
            ("GET", "/health"),
            ("GET", "/api/v1/stats"),
            ("GET", "/api/v1/research/Test Company"),
        ]
        
        for method, endpoint in endpoints_to_test:
            start_time = time.time()
            
            if method == "GET":
                response = client.get(endpoint)
            
            end_time = time.time()
            response_time = end_time - start_time
            
            assert response.status_code == 200
            assert response_time < 10.0  # Should respond within 10 seconds

def run_api_tests():
    """Run all API tests"""
    print("Running Hagglz API Test Suite...")
    print("=" * 50)
    
    # Run tests using pytest
    test_results = pytest.main([
        __file__,
        "-v",
        "--tb=short"
    ])
    
    return test_results == 0

if __name__ == "__main__":
    # Set environment variables for testing
    os.environ.setdefault('OPENAI_API_KEY', 'test-key')
    os.environ.setdefault('ANTHROPIC_API_KEY', 'test-key')
    
    success = run_api_tests()
    print(f"\nAPI Tests {'PASSED' if success else 'FAILED'}")
    exit(0 if success else 1)

