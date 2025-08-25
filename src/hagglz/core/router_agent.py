"""
Router Agent for Bill Classification

This module implements the router agent that analyses bills and determines
the appropriate specialist agent for negotiation.
"""

from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI
from typing import TypedDict, Literal, List, Dict, Any
import logging

logger = logging.getLogger(__name__)

class BillState(TypedDict, total=False):
    """State structure for bill processing"""
    bill_type: str
    ocr_text: str
    company: str
    amount: float
    negotiation_strategy: str
    conversation_history: List[Dict[str, Any]]
    confidence_score: float
    errors: str
    script: str

class RouterAgent:
    """Router agent for classifying bills and routing to specialists"""
    
    def __init__(self, model: str = "gpt-3.5-turbo", temperature: float = 0):
        self.llm = ChatOpenAI(model=model, temperature=temperature)
        self.workflow = None
        
    def create_router_graph(self):
        """Creates the router workflow graph"""
        workflow = StateGraph(BillState)
        
        def route_bill(state: BillState) -> BillState:
            """Routes bill to appropriate specialist agent"""
            logger.info("Routing bill for classification")
            
            prompt = f"""
            Analyse this bill and determine the specialist agent category.
            
            Bill Data: {state['ocr_text']}
            
            Categories:
            - UTILITY: Electric, gas, water, heating bills
            - MEDICAL: Healthcare, dental, medical, hospital bills
            - SUBSCRIPTION: Streaming services, software subscriptions, memberships
            - TELECOM: Phone, internet, cable, mobile bills
            
            Instructions:
            1. Read the bill text carefully
            2. Identify key indicators (company name, service type, billing categories)
            3. Return ONLY the category name (UTILITY, MEDICAL, SUBSCRIPTION, or TELECOM)
            4. If unclear, default to the most likely category based on available information
            
            Return only the category name.
            """
            
            try:
                response = self.llm.invoke(prompt)
                bill_type = response.content.strip().upper()
                
                # Validate the response
                valid_types = ['UTILITY', 'MEDICAL', 'SUBSCRIPTION', 'TELECOM']
                if bill_type not in valid_types:
                    logger.warning(f"Invalid bill type returned: {bill_type}, defaulting to UTILITY")
                    bill_type = 'UTILITY'
                
                state['bill_type'] = bill_type
                logger.info(f"Bill classified as: {bill_type}")
                
            except Exception as e:
                logger.error(f"Error in bill routing: {str(e)}")
                state['bill_type'] = 'UTILITY'  # Default fallback
                
            return state
        
        def extract_bill_details(state: BillState) -> BillState:
            """Extracts key details from the bill"""
            logger.info("Extracting bill details")
            
            prompt = f"""
            Extract key information from this bill:
            
            Bill Text: {state['ocr_text']}
            
            Please extract:
            1. Company/Service Provider Name
            2. Total Amount Due (numerical value only)
            3. Any account numbers or reference numbers
            4. Due date if available
            5. Service period if available
            
            Format your response as:
            Company: [company name]
            Amount: [numerical amount]
            Account: [account number if available]
            Due Date: [due date if available]
            Service Period: [service period if available]
            """
            
            try:
                response = self.llm.invoke(prompt)
                details = response.content
                
                # Parse company name
                for line in details.split('\n'):
                    if line.startswith('Company:'):
                        state['company'] = line.replace('Company:', '').strip()
                    elif line.startswith('Amount:'):
                        try:
                            amount_str = line.replace('Amount:', '').strip()
                            # Extract numerical value
                            import re
                            amount_match = re.search(r'[\d,]+\.?\d*', amount_str)
                            if amount_match:
                                state['amount'] = float(amount_match.group().replace(',', ''))
                        except (ValueError, AttributeError):
                            state['amount'] = 0.0
                
                logger.info(f"Extracted details - Company: {state.get('company', 'Unknown')}, Amount: {state.get('amount', 0)}")
                
            except Exception as e:
                logger.error(f"Error extracting bill details: {str(e)}")
                state['company'] = 'Unknown'
                state['amount'] = 0.0
                
            return state
        
        # Add nodes to workflow
        workflow.add_node("route", route_bill)
        workflow.add_node("extract", extract_bill_details)
        
        # Define edges
        workflow.add_edge("route", "extract")
        workflow.add_edge("extract", END)
        workflow.set_entry_point("route")
        
        self.workflow = workflow.compile()
        return self.workflow
    
    def process_bill(self, ocr_text: str) -> BillState:
        """Process a bill through the router"""
        if not self.workflow:
            self.create_router_graph()
            
        initial_state = BillState(
            bill_type="",
            ocr_text=ocr_text,
            company="",
            amount=0.0,
            negotiation_strategy="",
            conversation_history=[],
            confidence_score=0.0,
            errors="",
            script=""
        )
        
        result = self.workflow.invoke(initial_state)
        return result

def create_router_graph():
    """Factory function to create router graph"""
    router = RouterAgent()
    return router.create_router_graph()

if __name__ == "__main__":
    # Test the router agent
    router = RouterAgent()
    router.create_router_graph()
    
    test_bill = """
    ELECTRIC BILL
    CITY POWER COMPANY
    Account: 123456789
    Amount Due: $124.58
    Due Date: 2024-01-15
    Service Period: Dec 1-31, 2023
    """
    
    result = router.process_bill(test_bill)
    print(f"Bill Type: {result['bill_type']}")
    print(f"Company: {result['company']}")
    print(f"Amount: ${result['amount']}")

