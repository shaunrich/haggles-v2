"""
Utility Negotiation Agent

This module implements the specialist agent for negotiating utility bills
including electric, gas, water, and heating bills.
"""

from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)

class UtilityNegotiationAgent:
    """Specialist agent for utility bill negotiations"""
    
    def __init__(self, model: str = "gpt-4o-mini", temperature: float = 0.3):
        self.llm = ChatOpenAI(model=model, temperature=temperature)
        
        # Proven utility negotiation scripts
        self.negotiation_scripts = [
            "I've been a loyal customer for {years} years and I'm hoping we can work together to find a better rate.",
            "I see that {competitor} is offering {specific_deal}. Can you match or beat that offer?",
            "I'm considering cancelling my service because the cost has become too high. Is there anything you can do to help?",
            "I've noticed my bill has increased significantly. Are there any programmes or discounts available?",
            "I'm experiencing financial hardship due to {reason}. Do you have any assistance programmes?",
            "I'd like to discuss my payment plan options and see if we can reduce my monthly costs.",
            "I've been comparing rates and found better offers elsewhere. Can you provide a competitive rate?",
            "I'm a senior citizen/student/veteran. Are there any special discounts available for my situation?"
        ]
        
    def build_graph(self):
        """Build the utility negotiation workflow graph"""
        
        workflow = StateGraph(dict)
        
        def analyse_usage_history(state: Dict[str, Any]) -> Dict[str, Any]:
            """Analyse usage patterns and historical data"""
            logger.info("Analysing utility usage history and patterns")
            
            prompt = f"""
            Analyse this utility bill for negotiation opportunities:
            
            Bill Details:
            - Company: {state.get('company', 'Unknown')}
            - Amount: ${state.get('amount', 0)}
            - Bill Text: {state['ocr_text']}
            
            Analysis Focus:
            1. Seasonal usage patterns (if detectable)
            2. Bill amount compared to typical utility costs
            3. Long-term customer loyalty indicators
            4. Payment history indicators
            5. Service type (electric, gas, water, etc.)
            6. Rate structure analysis
            
            Provide a comprehensive analysis including:
            - Key negotiation leverage points
            - Potential savings opportunities
            - Customer loyalty factors
            - Market comparison opportunities
            - Specific negotiation angles to pursue
            
            Format as a structured analysis with clear recommendations.
            """
            
            try:
                response = self.llm.invoke(prompt)
                state['usage_analysis'] = response.content
                logger.info("Usage analysis completed")
                
                # Calculate confidence based on analysis quality
                analysis_text = response.content.lower()
                confidence_factors = [
                    'loyal' in analysis_text,
                    'savings' in analysis_text,
                    'competitor' in analysis_text,
                    'discount' in analysis_text,
                    'programme' in analysis_text
                ]
                base_confidence = sum(confidence_factors) * 0.15 + 0.25
                state['confidence_score'] = min(base_confidence, 0.9)
                
            except Exception as e:
                logger.error(f"Error in usage analysis: {str(e)}")
                state['usage_analysis'] = "Analysis unavailable"
                state['confidence_score'] = 0.3
                
            return state
        
        def research_competitors(state: Dict[str, Any]) -> Dict[str, Any]:
            """Research competitor rates and offers"""
            logger.info("Researching competitor rates and market offers")
            
            prompt = f"""
            Based on this utility bill analysis, provide competitor research:
            
            Current Provider: {state.get('company', 'Unknown')}
            Service Type: {state.get('bill_type', 'UTILITY')}
            Current Amount: ${state.get('amount', 0)}
            
            Research Focus:
            1. Typical competitor rates for similar services
            2. Common promotional offers in the utility market
            3. Switching incentives and new customer deals
            4. Seasonal promotions and discounts
            5. Loyalty programme alternatives
            
            Provide specific talking points about:
            - Competitor names and their typical offers
            - Percentage savings commonly available
            - New customer incentives
            - Rate comparison strategies
            - Market positioning arguments
            
            Format as actionable competitive intelligence for negotiation.
            """
            
            try:
                response = self.llm.invoke(prompt)
                state['competitor_research'] = response.content
                
                # Update confidence based on presence of strong points
                text = response.content.lower()
                boost = 0.0
                for kw in ['match', 'beat', 'discount', 'offer', 'promotion']:
                    if kw in text:
                        boost += 0.03
                state['confidence_score'] = min(state.get('confidence_score', 0.25) + boost, 0.95)
                
            except Exception as e:
                logger.error(f"Error researching competitors: {str(e)}")
                state['competitor_research'] = "Research unavailable"
                
            return state
        
        def generate_negotiation_plan(state: Dict[str, Any]) -> Dict[str, Any]:
            """Generate negotiation strategy and script"""
            logger.info("Generating negotiation plan and script")
            
            prompt = f"""
            Create a negotiation strategy and script based on:
            - Usage analysis: {state.get('usage_analysis', '')}
            - Competitor research: {state.get('competitor_research', '')}
            - Company: {state.get('company', 'Unknown')}
            - Amount: ${state.get('amount', 0)}
            
            Provide:
            1. Negotiation strategy (bulleted)
            2. Script the user can read
            3. Expected savings range and confidence
            """
            
            try:
                response = self.llm.invoke(prompt)
                state['negotiation_strategy'] = response.content
                # Rough savings estimate for demo purposes
                state['target_savings'] = {
                    'percentage': round(100 * min(0.35, state.get('confidence_score', 0.3)), 1)
                }
                
            except Exception as e:
                logger.error(f"Error generating negotiation plan: {str(e)}")
                state['negotiation_strategy'] = "Unable to generate strategy"
                state['target_savings'] = {'percentage': 0.0}
                
            return state
        
        # Build workflow
        workflow.add_node("analyse_usage_history", analyse_usage_history)
        workflow.add_node("research_competitors", research_competitors)
        workflow.add_node("generate_plan", generate_negotiation_plan)
        
        workflow.add_edge("analyse_usage_history", "research_competitors")
        workflow.add_edge("research_competitors", "generate_plan")
        workflow.add_edge("generate_plan", END)
        
        workflow.set_entry_point("analyse_usage_history")
        return workflow.compile()
    
    def process_utility_bill(self, bill_state: Dict[str, Any]) -> Dict[str, Any]:
        """Process a utility bill through the negotiation workflow"""
        if not hasattr(self, '_compiled_workflow'):
            self._compiled_workflow = self.build_graph()
        
        result = self._compiled_workflow.invoke(bill_state)
        return result

def create_utility_agent():
    """Factory function to create utility negotiation agent"""
    agent = UtilityNegotiationAgent()
    return agent.build_graph()

if __name__ == "__main__":
    # Test the utility agent
    agent = UtilityNegotiationAgent()
    workflow = agent.build_graph()
    
    test_state = {
        'bill_type': 'UTILITY',
        'ocr_text': 'ELECTRIC BILL\nCITY POWER\nAmount Due: $124.58',
        'company': 'City Power',
        'amount': 124.58,
        'conversation_history': []
    }
    
    result = workflow.invoke(test_state)
    print(f"Strategy: {result.get('negotiation_strategy', 'Not generated')[:200]}...")
    print(f"Confidence: {result.get('confidence_score', 0)}")
    print(f"Target Savings: {result.get('target_savings', {})}")

