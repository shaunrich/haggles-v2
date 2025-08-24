"""
Utility Negotiation Agent

This module implements the specialist agent for negotiating utility bills
including electric, gas, water, and heating bills.
"""

from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)

class UtilityNegotiationAgent:
    """Specialist agent for utility bill negotiations"""
    
    def __init__(self, model: str = "gpt-4-turbo-preview", temperature: float = 0.3):
        self.llm = ChatOpenAI(model=model, temperature=temperature)
        self.memory = ConversationBufferMemory()
        
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
                logger.info("Competitor research completed")
                
            except Exception as e:
                logger.error(f"Error in competitor research: {str(e)}")
                state['competitor_research'] = "Competitor research unavailable"
                
            return state
        
        def generate_negotiation_strategy(state: Dict[str, Any]) -> Dict[str, Any]:
            """Generate comprehensive negotiation strategy"""
            logger.info("Generating utility negotiation strategy")
            
            prompt = f"""
            Create a comprehensive utility negotiation strategy based on:
            
            Bill Information:
            - Company: {state.get('company', 'Unknown')}
            - Amount: ${state.get('amount', 0)}
            - Type: {state.get('bill_type', 'UTILITY')}
            
            Analysis: {state.get('usage_analysis', 'Not available')}
            Competitor Research: {state.get('competitor_research', 'Not available')}
            
            Create a strategy including:
            1. Primary negotiation angle (loyalty, competition, hardship, etc.)
            2. Specific talking points and arguments
            3. Target savings percentage (realistic range)
            4. Fallback positions if initial approach fails
            5. Timing recommendations for the call
            6. Key phrases and questions to use
            
            Proven Utility Negotiation Approaches:
            - Loyalty-based: Emphasise long-term customer relationship
            - Competition-based: Reference specific competitor offers
            - Hardship-based: Request assistance programmes
            - Rate analysis: Question rate increases and seek explanations
            - Bundle opportunities: Explore service combinations
            
            Provide a detailed, actionable negotiation strategy.
            """
            
            try:
                response = self.llm.invoke(prompt)
                state['negotiation_strategy'] = response.content
                logger.info("Negotiation strategy generated")
                
            except Exception as e:
                logger.error(f"Error generating strategy: {str(e)}")
                state['negotiation_strategy'] = "Strategy generation failed"
                
            return state
        
        def create_negotiation_script(state: Dict[str, Any]) -> Dict[str, Any]:
            """Generate specific negotiation script"""
            logger.info("Creating utility negotiation script")
            
            # Select appropriate script templates based on strategy
            strategy_text = state.get('negotiation_strategy', '').lower()
            
            selected_scripts = []
            if 'loyal' in strategy_text:
                selected_scripts.append(self.negotiation_scripts[0])
            if 'competitor' in strategy_text:
                selected_scripts.extend(self.negotiation_scripts[1:3])
            if 'hardship' in strategy_text:
                selected_scripts.append(self.negotiation_scripts[4])
            if 'discount' in strategy_text:
                selected_scripts.extend(self.negotiation_scripts[3:4])
            
            # Default scripts if none selected
            if not selected_scripts:
                selected_scripts = self.negotiation_scripts[:3]
            
            prompt = f"""
            Create a complete negotiation script for this utility bill:
            
            Company: {state.get('company', 'Unknown')}
            Amount: ${state.get('amount', 0)}
            Strategy: {state.get('negotiation_strategy', 'Not available')}
            
            Use these proven script templates:
            {chr(10).join(selected_scripts)}
            
            Create a complete dialogue including:
            1. Opening statement and introduction
            2. Main negotiation points (2-3 key arguments)
            3. Specific requests (discount percentage, payment plans, etc.)
            4. Responses to common objections
            5. Closing statements and next steps
            
            Make the script conversational, polite but firm, and specific to this situation.
            Include placeholder values that can be customised (e.g., [years as customer], [competitor name]).
            """
            
            try:
                response = self.llm.invoke(prompt)
                state['script'] = response.content
                logger.info("Negotiation script created")
                
                # Adjust confidence based on script quality
                script_quality_indicators = [
                    'opening' in response.content.lower(),
                    'discount' in response.content.lower(),
                    'competitor' in response.content.lower(),
                    'loyal' in response.content.lower()
                ]
                script_bonus = sum(script_quality_indicators) * 0.05
                state['confidence_score'] = min(state.get('confidence_score', 0.5) + script_bonus, 0.95)
                
            except Exception as e:
                logger.error(f"Error creating script: {str(e)}")
                state['script'] = "Script generation failed"
                
            return state
        
        def calculate_savings_potential(state: Dict[str, Any]) -> Dict[str, Any]:
            """Calculate potential savings and ROI"""
            logger.info("Calculating savings potential")
            
            current_amount = state.get('amount', 0)
            
            # Typical utility savings ranges
            savings_scenarios = {
                'conservative': 0.05,  # 5%
                'moderate': 0.15,      # 15%
                'aggressive': 0.25     # 25%
            }
            
            savings_analysis = {}
            for scenario, percentage in savings_scenarios.items():
                monthly_savings = current_amount * percentage
                annual_savings = monthly_savings * 12
                savings_analysis[scenario] = {
                    'monthly_savings': round(monthly_savings, 2),
                    'annual_savings': round(annual_savings, 2),
                    'percentage': percentage * 100
                }
            
            state['savings_potential'] = savings_analysis
            
            # Set target savings based on confidence
            confidence = state.get('confidence_score', 0.5)
            if confidence > 0.8:
                state['target_savings'] = savings_analysis['aggressive']
            elif confidence > 0.6:
                state['target_savings'] = savings_analysis['moderate']
            else:
                state['target_savings'] = savings_analysis['conservative']
            
            logger.info(f"Savings potential calculated: {state['target_savings']}")
            return state
        
        # Add nodes to workflow
        workflow.add_node("analyse_usage", analyse_usage_history)
        workflow.add_node("research_competitors", research_competitors)
        workflow.add_node("generate_strategy", generate_negotiation_strategy)
        workflow.add_node("create_script", create_negotiation_script)
        workflow.add_node("calculate_savings", calculate_savings_potential)
        
        # Define edges
        workflow.add_edge("analyse_usage", "research_competitors")
        workflow.add_edge("research_competitors", "generate_strategy")
        workflow.add_edge("generate_strategy", "create_script")
        workflow.add_edge("create_script", "calculate_savings")
        workflow.add_edge("calculate_savings", END)
        
        workflow.set_entry_point("analyse_usage")
        
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

