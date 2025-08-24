#!/usr/bin/env python3
"""
Test script to verify all imports work correctly for LangGraph Platform deployment
"""

import sys
import os

# Add src to path for testing
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_imports():
    """Test all critical imports"""
    print("🧪 Testing Hagglz package imports...")
    
    try:
        # Test main package import
        import hagglz
        print(f"✅ Main package: {hagglz.__version__}")
        
        # Test core imports
        from hagglz.core.orchestrator import MasterOrchestrator
        print("✅ MasterOrchestrator import successful")
        
        from hagglz.core.router_agent import RouterAgent
        print("✅ RouterAgent import successful")
        
        # Test agent imports
        from hagglz.agents.utility_agent import UtilityNegotiationAgent
        print("✅ UtilityNegotiationAgent import successful")
        
        from hagglz.agents.medical_agent import MedicalNegotiationAgent
        print("✅ MedicalNegotiationAgent import successful")
        
        from hagglz.agents.subscription_agent import SubscriptionNegotiationAgent
        print("✅ SubscriptionNegotiationAgent import successful")
        
        from hagglz.agents.telecom_agent import TelecomNegotiationAgent
        print("✅ TelecomNegotiationAgent import successful")
        
        # Test memory and tools imports
        from hagglz.memory.vector_store import NegotiationMemory
        print("✅ NegotiationMemory import successful")
        
        from hagglz.tools.negotiation_tools import NegotiationTools
        print("✅ NegotiationTools import successful")
        
        # Test API import (this is the critical one for LangGraph Platform)
        from hagglz.api.main import app
        print("✅ FastAPI app import successful")
        
        print("\n🎉 All imports successful! Package is ready for LangGraph Platform deployment.")
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

if __name__ == "__main__":
    success = test_imports()
    sys.exit(0 if success else 1)
