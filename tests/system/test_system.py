"""
Comprehensive Test Script for Hagglz Agent System

This script tests all components of the Hagglz negotiation system including
individual agents and the master orchestrator.
"""

import sys
import os
import logging
from typing import Dict, Any

# Add the project root to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def test_router_agent():
    """Test the router agent functionality"""
    print("\n" + "="*50)
    print("TESTING ROUTER AGENT")
    print("="*50)
    
    try:
        from agents.router_agent import RouterAgent
        
        router = RouterAgent()
        
        test_bills = [
            {
                'name': 'Electric Bill',
                'text': 'ELECTRIC BILL\nCITY POWER COMPANY\nAccount: 123456789\nAmount Due: $124.58'
            },
            {
                'name': 'Medical Bill', 
                'text': 'HOSPITAL BILL\nCITY MEDICAL CENTER\nEmergency Room Visit\nAmount Due: $2,450.00'
            },
            {
                'name': 'Netflix Subscription',
                'text': 'NETFLIX PREMIUM\nMonthly Subscription\nAmount: $19.99'
            },
            {
                'name': 'Verizon Mobile',
                'text': 'VERIZON WIRELESS\nUnlimited Plan\nMonthly Charge: $85.00'
            }
        ]
        
        for bill in test_bills:
            print(f"\nTesting: {bill['name']}")
            result = router.process_bill(bill['text'])
            print(f"  Classified as: {result.get('bill_type', 'Unknown')}")
            print(f"  Company: {result.get('company', 'Unknown')}")
            print(f"  Amount: ${result.get('amount', 0)}")
        
        print("\n✅ Router Agent Test: PASSED")
        return True
        
    except Exception as e:
        print(f"\n❌ Router Agent Test: FAILED - {str(e)}")
        return False

def test_utility_agent():
    """Test the utility negotiation agent"""
    print("\n" + "="*50)
    print("TESTING UTILITY AGENT")
    print("="*50)
    
    try:
        from agents.utility_agent import UtilityNegotiationAgent
        
        agent = UtilityNegotiationAgent()
        workflow = agent.build_graph()
        
        test_state = {
            'bill_type': 'UTILITY',
            'ocr_text': 'ELECTRIC BILL\nCITY POWER\nAmount Due: $124.58',
            'company': 'City Power',
            'amount': 124.58,
            'conversation_history': []
        }
        
        print("Processing utility bill...")
        result = workflow.invoke(test_state)
        
        print(f"  Confidence Score: {result.get('confidence_score', 0)}")
        print(f"  Has Strategy: {'negotiation_strategy' in result}")
        print(f"  Has Script: {'script' in result}")
        print(f"  Target Savings: {result.get('target_savings', {})}")
        
        print("\n✅ Utility Agent Test: PASSED")
        return True
        
    except Exception as e:
        print(f"\n❌ Utility Agent Test: FAILED - {str(e)}")
        return False

def test_medical_agent():
    """Test the medical negotiation agent"""
    print("\n" + "="*50)
    print("TESTING MEDICAL AGENT")
    print("="*50)
    
    try:
        from agents.medical_agent import MedicalNegotiationAgent
        
        agent = MedicalNegotiationAgent()
        workflow = agent.build_graph()
        
        test_state = {
            'bill_type': 'MEDICAL',
            'ocr_text': 'HOSPITAL BILL\nCITY MEDICAL CENTER\nEmergency Room Visit\nAmount Due: $2,450.00',
            'company': 'City Medical Center',
            'amount': 2450.00,
            'conversation_history': []
        }
        
        print("Processing medical bill...")
        result = workflow.invoke(test_state)
        
        print(f"  Confidence Score: {result.get('confidence_score', 0)}")
        print(f"  Errors Found: {result.get('has_errors', False)}")
        print(f"  Has Strategy: {'negotiation_strategy' in result}")
        print(f"  Has Script: {'script' in result}")
        print(f"  Target Savings: {result.get('target_savings', {})}")
        
        print("\n✅ Medical Agent Test: PASSED")
        return True
        
    except Exception as e:
        print(f"\n❌ Medical Agent Test: FAILED - {str(e)}")
        return False

def test_subscription_agent():
    """Test the subscription negotiation agent"""
    print("\n" + "="*50)
    print("TESTING SUBSCRIPTION AGENT")
    print("="*50)
    
    try:
        from agents.subscription_agent import SubscriptionNegotiationAgent
        
        agent = SubscriptionNegotiationAgent()
        workflow = agent.build_graph()
        
        test_state = {
            'bill_type': 'SUBSCRIPTION',
            'ocr_text': 'NETFLIX PREMIUM\nMonthly Subscription\nAmount: $19.99',
            'company': 'Netflix',
            'amount': 19.99,
            'conversation_history': []
        }
        
        print("Processing subscription bill...")
        result = workflow.invoke(test_state)
        
        print(f"  Confidence Score: {result.get('confidence_score', 0)}")
        print(f"  Subscription Type: {result.get('subscription_type', 'Unknown')}")
        print(f"  Has Strategy: {'negotiation_strategy' in result}")
        print(f"  Has Script: {'script' in result}")
        print(f"  Target Savings: {result.get('target_savings', {})}")
        
        print("\n✅ Subscription Agent Test: PASSED")
        return True
        
    except Exception as e:
        print(f"\n❌ Subscription Agent Test: FAILED - {str(e)}")
        return False

def test_telecom_agent():
    """Test the telecom negotiation agent"""
    print("\n" + "="*50)
    print("TESTING TELECOM AGENT")
    print("="*50)
    
    try:
        from agents.telecom_agent import TelecomNegotiationAgent
        
        agent = TelecomNegotiationAgent()
        workflow = agent.build_graph()
        
        test_state = {
            'bill_type': 'TELECOM',
            'ocr_text': 'VERIZON WIRELESS\nUnlimited Plan\nMonthly Charge: $85.00',
            'company': 'Verizon Wireless',
            'amount': 85.00,
            'conversation_history': []
        }
        
        print("Processing telecom bill...")
        result = workflow.invoke(test_state)
        
        print(f"  Confidence Score: {result.get('confidence_score', 0)}")
        print(f"  Telecom Type: {result.get('telecom_type', 'Unknown')}")
        print(f"  Has Strategy: {'negotiation_strategy' in result}")
        print(f"  Has Script: {'script' in result}")
        print(f"  Target Savings: {result.get('target_savings', {})}")
        
        print("\n✅ Telecom Agent Test: PASSED")
        return True
        
    except Exception as e:
        print(f"\n❌ Telecom Agent Test: FAILED - {str(e)}")
        return False

def test_master_orchestrator():
    """Test the master orchestrator"""
    print("\n" + "="*50)
    print("TESTING MASTER ORCHESTRATOR")
    print("="*50)
    
    try:
        from orchestrator import MasterOrchestrator
        
        orchestrator = MasterOrchestrator()
        
        test_bills = [
            {
                'name': 'High Amount Electric Bill (should be high confidence)',
                'data': {
                    'text': 'ELECTRIC BILL\nCITY POWER COMPANY\nAccount: 123456789\nAmount Due: $324.58',
                    'user_id': 'test_user_1'
                }
            },
            {
                'name': 'Medical Bill (medium confidence expected)',
                'data': {
                    'text': 'HOSPITAL BILL\nCITY MEDICAL CENTER\nEmergency Room Visit\nAmount Due: $1,250.00',
                    'user_id': 'test_user_2'
                }
            },
            {
                'name': 'Small Subscription (might be low confidence)',
                'data': {
                    'text': 'BASIC STREAMING\nAmount: $5.99',
                    'user_id': 'test_user_3'
                }
            }
        ]
        
        for bill in test_bills:
            print(f"\nTesting: {bill['name']}")
            result = orchestrator.process_bill(bill['data'])
            
            print(f"  Processing Status: {result.get('processing_status', 'Unknown')}")
            print(f"  Bill Type: {result.get('bill_type', 'Unknown')}")
            print(f"  Confidence Score: {result.get('confidence_score', 0)}")
            print(f"  Execution Mode: {result.get('execution_mode', 'Unknown')}")
            
            if result.get('processing_errors'):
                print(f"  Errors: {result['processing_errors']}")
        
        print("\n✅ Master Orchestrator Test: PASSED")
        return True
        
    except Exception as e:
        print(f"\n❌ Master Orchestrator Test: FAILED - {str(e)}")
        return False

def run_all_tests():
    """Run all system tests"""
    print("HAGGLZ AGENT SYSTEM - COMPREHENSIVE TESTING")
    print("="*60)
    
    tests = [
        ("Router Agent", test_router_agent),
        ("Utility Agent", test_utility_agent),
        ("Medical Agent", test_medical_agent),
        ("Subscription Agent", test_subscription_agent),
        ("Telecom Agent", test_telecom_agent),
        ("Master Orchestrator", test_master_orchestrator)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            success = test_func()
            results.append((test_name, success))
        except Exception as e:
            print(f"\n❌ {test_name} Test: FAILED - {str(e)}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    
    passed = 0
    total = len(results)
    
    for test_name, success in results:
        status = "✅ PASSED" if success else "❌ FAILED"
        print(f"{test_name}: {status}")
        if success:
            passed += 1
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 ALL TESTS PASSED! System is ready for deployment.")
    else:
        print("⚠️  Some tests failed. Please review and fix issues before deployment.")
    
    return passed == total

if __name__ == "__main__":
    # Set environment variables for testing (using placeholder values)
    os.environ.setdefault('OPENAI_API_KEY', 'test-key')
    os.environ.setdefault('ANTHROPIC_API_KEY', 'test-key')
    
    success = run_all_tests()
    sys.exit(0 if success else 1)

