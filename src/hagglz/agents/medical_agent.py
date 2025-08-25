"""
Medical Negotiation Agent

This module implements the specialist agent for negotiating medical bills
including healthcare, dental, and hospital bills using Claude AI.
"""

from langgraph.graph import StateGraph, END
from langchain_anthropic import ChatAnthropic
from typing import Dict, Any
import logging
import re

logger = logging.getLogger(__name__)

class MedicalNegotiationAgent:
    """Specialist agent for medical bill negotiations"""
    
    def __init__(self, model: str = "claude-3-opus-20240229", temperature: float = 0.2):
        # Use Claude for medical bills as per specification
        self.llm = ChatAnthropic(model=model, temperature=temperature)
        
        # Proven medical negotiation scripts
        self.medical_scripts = [
            "Is this negotiable? I'd like to discuss payment options for this medical bill.",
            "I want to offer you a settlement amount to close out this account. What's the minimum you would accept?",
            "I'm experiencing financial hardship. Are there assistance programmes or charity care available?",
            "I'd like to request an itemised bill to review all charges before making payment.",
            "I believe there may be billing errors. Can we review the charges together?",
            "I don't have insurance coverage for this. Do you offer uninsured patient discounts?",
            "Can we set up a payment plan that works with my budget?",
            "I've received multiple bills for the same service. Can you help clarify the charges?"
        ]
        
        # Common medical billing errors to check for
        self.common_errors = [
            "Duplicate charges for the same service",
            "Incorrect CPT (procedure) codes",
            "Services billed but not received",
            "Insurance processing errors",
            "Incorrect patient information",
            "Upcoding (billing for more expensive procedures)",
            "Unbundling (separate billing for bundled services)",
            "Balance billing issues"
        ]
        
    def build_graph(self):
        """Build the medical negotiation workflow graph"""
        
        workflow = StateGraph(dict)
        
        def check_billing_errors(state: Dict[str, Any]) -> Dict[str, Any]:
            """Check for common medical billing errors"""
            logger.info("Checking medical bill for errors and discrepancies")
            
            prompt = f"""
            Analyse this medical bill for potential billing errors and discrepancies:
            
            Bill Details:
            - Provider: {state.get('company', 'Unknown')}
            - Amount: ${state.get('amount', 0)}
            - Bill Text: {state['ocr_text']}
            
            Please identify:
            1. Potential coding errors (CPT codes)
            2. Duplicate or unnecessary charges
            3. Insurance processing issues
            4. Mismatched patient or service information
            
            Provide a summary and suggested next steps.
            """
            
            try:
                response = self.llm.invoke(prompt)
                state['error_analysis'] = response.content
            except Exception as e:
                logger.error(f"Error checking billing errors: {str(e)}")
                state['error_analysis'] = "Analysis unavailable"
            
            return state
        
        def assess_financial_hardship(state: Dict[str, Any]) -> Dict[str, Any]:
            """Assess financial hardship and assistance options"""
            logger.info("Assessing financial hardship and assistance programmes")
            
            prompt = f"""
            Assess financial assistance options for this medical bill:
            
            Bill Amount: ${state.get('amount', 0)}
            Provider: {state.get('company', 'Unknown')}
            
            Financial Assistance Assessment:
            1. Typical charity care programmes offered by medical providers
            2. Income-based assistance eligibility
            3. Uninsured patient discounts
            4. Payment plan options
            5. Settlement negotiation possibilities
            
            Provide guidance on:
            - What financial assistance programmes to ask about
            - Typical discount percentages available
            - Documentation that might be needed
            - Best approaches for requesting assistance
            - Alternative payment arrangements
            
            Focus on practical, actionable advice for financial relief options.
            """
            
            try:
                response = self.llm.invoke(prompt)
                state['financial_assistance'] = response.content
                logger.info("Financial assistance assessment completed")
                
            except Exception as e:
                logger.error(f"Error in financial assessment: {str(e)}")
                state['financial_assistance'] = "Financial assistance assessment unavailable"
                
            return state
        
        def generate_medical_strategy(state: Dict[str, Any]) -> Dict[str, Any]:
            """Create medical bill negotiation strategy"""
            logger.info("Generating medical negotiation strategy")
            
            has_errors = state.get('has_errors', False)
            amount = state.get('amount', 0)
            
            prompt = f"""
            Create a comprehensive medical bill negotiation strategy:
            
            Bill Information:
            - Provider: {state.get('company', 'Unknown')}
            - Amount: ${amount}
            - Errors Found: {has_errors}
            
            Error Analysis: {state.get('error_analysis', 'Not available')}
            Financial Options: {state.get('financial_assistance', 'Not available')}
            
            Strategy Development:
            1. Primary negotiation approach based on situation
            2. Specific talking points and arguments
            3. Target outcome (discount percentage, payment plan, etc.)
            4. Documentation to request
            5. Escalation path if initial contact fails
            
            Medical Bill Negotiation Approaches:
            - Error-based: Challenge specific billing errors
            - Financial hardship: Request charity care or assistance
            - Uninsured discount: Request standard uninsured rates
            - Settlement offer: Propose lump sum payment for discount
            - Payment plan: Request manageable monthly payments
            
            Consider these factors:
            - Medical bills often have 30-70% negotiation success rates
            - Providers prefer payment to collections
            - Many hospitals have charity care requirements
            - Uninsured patients often qualify for significant discounts
            
            Provide a detailed, step-by-step negotiation strategy.
            """
            
            try:
                response = self.llm.invoke(prompt)
                state['negotiation_strategy'] = response.content
                
                # Calculate confidence based on strategy factors
                base_confidence = 0.4  # Medical bills generally have good negotiation potential
                
                if has_errors:
                    base_confidence += 0.2  # Errors provide strong leverage
                if amount > 1000:
                    base_confidence += 0.1  # Higher amounts often more negotiable
                if 'charity' in response.content.lower():
                    base_confidence += 0.1  # Charity care options available
                if 'uninsured' in response.content.lower():
                    base_confidence += 0.1  # Uninsured discounts available
                
                state['confidence_score'] = min(base_confidence, 0.9)
                logger.info(f"Medical strategy generated with confidence: {state['confidence_score']}")
                
            except Exception as e:
                logger.error(f"Error generating medical strategy: {str(e)}")
                state['negotiation_strategy'] = "Strategy generation failed"
                state['confidence_score'] = 0.3
                
            return state
        
        def create_medical_script(state: Dict[str, Any]) -> Dict[str, Any]:
            """Generate medical negotiation script"""
            logger.info("Creating medical negotiation script")
            
            has_errors = state.get('has_errors', False)
            strategy_text = state.get('negotiation_strategy', '').lower()
            
            # Select appropriate scripts based on strategy
            selected_scripts = []
            
            if has_errors:
                selected_scripts.extend([self.medical_scripts[0], self.medical_scripts[3], self.medical_scripts[4]])
            if 'hardship' in strategy_text or 'charity' in strategy_text:
                selected_scripts.append(self.medical_scripts[2])
            if 'settlement' in strategy_text:
                selected_scripts.append(self.medical_scripts[1])
            if 'uninsured' in strategy_text:
                selected_scripts.append(self.medical_scripts[5])
            if 'payment plan' in strategy_text:
                selected_scripts.append(self.medical_scripts[6])
            
            # Default scripts if none selected
            if not selected_scripts:
                selected_scripts = self.medical_scripts[:3]
            
            prompt = f"""
            Create a complete medical bill negotiation script:
            
            Provider: {state.get('company', 'Unknown')}
            Amount: ${state.get('amount', 0)}
            Errors Found: {state.get('has_errors', False)}
            Strategy: {state.get('negotiation_strategy', 'Not available')}
            
            Use these proven medical negotiation approaches:
            {chr(10).join(selected_scripts)}
            
            Create a complete dialogue including:
            1. Professional opening and identification
            2. Clear statement of purpose
            3. Specific requests based on situation:
               - Error corrections if applicable
               - Financial assistance requests
               - Settlement offers
               - Payment plan requests
            4. Documentation requests (itemised bill, charity care applications)
            5. Professional closing with next steps
            
            Medical Bill Script Guidelines:
            - Be respectful and professional
            - Request itemised bills for review
            - Ask about financial assistance programmes
            - Be prepared to provide financial documentation
            - Know your rights regarding billing practices
            - Request supervisor if needed
            
            Make the script specific to this medical bill situation.
            """
            
            try:
                response = self.llm.invoke(prompt)
                state['script'] = response.content
                logger.info("Medical negotiation script created")
                
            except Exception as e:
                logger.error(f"Error creating medical script: {str(e)}")
                state['script'] = "Script generation failed"
                
            return state
        
        def calculate_medical_savings(state: Dict[str, Any]) -> Dict[str, Any]:
            """Calculate potential savings for medical bills"""
            logger.info("Calculating medical bill savings potential")
            
            current_amount = state.get('amount', 0)
            has_errors = state.get('has_errors', False)
            
            # Medical bill savings scenarios (typically higher than other bills)
            if has_errors:
                savings_scenarios = {
                    'conservative': 0.20,  # 20% - error corrections
                    'moderate': 0.40,      # 40% - errors + negotiation
                    'aggressive': 0.60     # 60% - significant errors
                }
            else:
                savings_scenarios = {
                    'conservative': 0.15,  # 15% - basic negotiation
                    'moderate': 0.30,      # 30% - financial hardship
                    'aggressive': 0.50     # 50% - charity care/settlement
                }
            
            savings_analysis = {}
            for scenario, percentage in savings_scenarios.items():
                savings_amount = current_amount * percentage
                savings_analysis[scenario] = {
                    'savings_amount': round(savings_amount, 2),
                    'final_amount': round(current_amount - savings_amount, 2),
                    'percentage': percentage * 100
                }
            
            state['savings_potential'] = savings_analysis
            
            # Set target savings based on confidence and errors
            confidence = state.get('confidence_score', 0.5)
            if confidence > 0.8 or has_errors:
                state['target_savings'] = savings_analysis['aggressive']
            elif confidence > 0.6:
                state['target_savings'] = savings_analysis['moderate']
            else:
                state['target_savings'] = savings_analysis['conservative']
            
            logger.info(f"Medical savings potential calculated: {state['target_savings']}")
            return state
        
        # Add nodes to workflow
        workflow.add_node("check_errors", check_billing_errors)
        workflow.add_node("assess_hardship", assess_financial_hardship)
        workflow.add_node("generate_strategy", generate_medical_strategy)
        workflow.add_node("create_script", create_medical_script)
        workflow.add_node("calculate_savings", calculate_medical_savings)
        
        # Define edges
        workflow.add_edge("check_errors", "assess_hardship")
        workflow.add_edge("assess_hardship", "generate_strategy")
        workflow.add_edge("generate_strategy", "create_script")
        workflow.add_edge("create_script", "calculate_savings")
        workflow.add_edge("calculate_savings", END)
        
        workflow.set_entry_point("check_errors")
        
        return workflow.compile()
    
    def process_medical_bill(self, bill_state: Dict[str, Any]) -> Dict[str, Any]:
        """Process a medical bill through the negotiation workflow"""
        if not hasattr(self, '_compiled_workflow'):
            self._compiled_workflow = self.build_graph()
        
        result = self._compiled_workflow.invoke(bill_state)
        return result

def create_medical_agent():
    """Factory function to create medical negotiation agent"""
    agent = MedicalNegotiationAgent()
    return agent.build_graph()

if __name__ == "__main__":
    # Test the medical agent
    agent = MedicalNegotiationAgent()
    workflow = agent.build_graph()
    
    test_state = {
        'bill_type': 'MEDICAL',
        'ocr_text': 'HOSPITAL BILL\nCITY MEDICAL CENTER\nEmergency Room Visit\nAmount Due: $2,450.00',
        'company': 'City Medical Center',
        'amount': 2450.00,
        'conversation_history': []
    }
    
    result = workflow.invoke(test_state)
    print(f"Errors Found: {result.get('has_errors', False)}")
    print(f"Strategy: {result.get('negotiation_strategy', 'Not generated')[:200]}...")
    print(f"Confidence: {result.get('confidence_score', 0)}")
    print(f"Target Savings: {result.get('target_savings', {})}")

