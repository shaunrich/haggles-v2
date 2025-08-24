"""
Negotiation Tools

This module implements various tools for supporting the negotiation process
including research, calculation, and script generation utilities.
"""

from langchain.tools import Tool
from langchain_openai import ChatOpenAI
from typing import Dict, Any, List, Optional
import logging
import requests
import json
from datetime import datetime
import re

logger = logging.getLogger(__name__)

class NegotiationTools:
    """Collection of tools for negotiation support"""
    
    def __init__(self):
        self.llm = ChatOpenAI(model="gpt-4-turbo-preview", temperature=0.3)
        
    def create_negotiation_tools(self) -> List[Tool]:
        """Create and return all negotiation tools"""
        tools = []
        
        # Research Tool
        research_tool = Tool(
            name="research_company",
            func=self.research_company,
            description="Research company policies, negotiation history, and competitor rates"
        )
        tools.append(research_tool)
        
        # Calculator Tool
        calculator_tool = Tool(
            name="calculate_savings",
            func=self.calculate_savings,
            description="Calculate potential savings, ROI, and financial impact"
        )
        tools.append(calculator_tool)
        
        # Script Generator Tool
        script_tool = Tool(
            name="generate_script",
            func=self.generate_negotiation_script,
            description="Generate customised negotiation scripts based on context"
        )
        tools.append(script_tool)
        
        # Competitor Analysis Tool
        competitor_tool = Tool(
            name="analyse_competitors",
            func=self.analyse_competitors,
            description="Analyse competitor offerings and market rates"
        )
        tools.append(competitor_tool)
        
        # Success Probability Tool
        probability_tool = Tool(
            name="calculate_success_probability",
            func=self.calculate_success_probability,
            description="Calculate probability of negotiation success based on factors"
        )
        tools.append(probability_tool)
        
        # Timing Optimiser Tool
        timing_tool = Tool(
            name="optimise_timing",
            func=self.optimise_negotiation_timing,
            description="Determine optimal timing for negotiation attempts"
        )
        tools.append(timing_tool)
        
        return tools
    
    def research_company(self, company_name: str) -> str:
        """Research company policies and negotiation potential"""
        try:
            logger.info(f"Researching company: {company_name}")
            
            prompt = f"""
            Research and provide intelligence about negotiating with {company_name}:
            
            Please provide information about:
            1. Company's general negotiation policies
            2. Known customer retention strategies
            3. Typical discount ranges offered
            4. Best departments/contacts for negotiations
            5. Seasonal patterns or promotional periods
            6. Customer service reputation and approach
            7. Competitive positioning in the market
            
            Format the response as actionable intelligence for negotiation planning.
            Focus on practical insights that can improve negotiation success.
            """
            
            response = self.llm.invoke(prompt)
            
            # Structure the response
            research_data = {
                'company': company_name,
                'research_date': datetime.now().isoformat(),
                'intelligence': response.content,
                'confidence': 'medium',  # Could be enhanced with real data sources
                'sources': 'AI analysis based on general knowledge'
            }
            
            return json.dumps(research_data, indent=2)
            
        except Exception as e:
            logger.error(f"Error researching company {company_name}: {str(e)}")
            return json.dumps({'error': str(e), 'company': company_name})
    
    def calculate_savings(self, original_amount: float, negotiated_amount: float = None, 
                         target_percentage: float = None) -> str:
        """Calculate potential savings and financial impact"""
        try:
            logger.info(f"Calculating savings for amount: ${original_amount}")
            
            calculations = {
                'original_amount': original_amount,
                'calculation_date': datetime.now().isoformat()
            }
            
            # If negotiated amount is provided, calculate actual savings
            if negotiated_amount is not None:
                savings_amount = original_amount - negotiated_amount
                savings_percentage = (savings_amount / original_amount) * 100
                
                calculations.update({
                    'negotiated_amount': negotiated_amount,
                    'savings_amount': round(savings_amount, 2),
                    'savings_percentage': round(savings_percentage, 2),
                    'monthly_savings': round(savings_amount, 2),
                    'annual_savings': round(savings_amount * 12, 2),
                    'roi_calculation': 'Immediate return on negotiation effort'
                })
            
            # If target percentage is provided, calculate target amounts
            if target_percentage is not None:
                target_savings = original_amount * (target_percentage / 100)
                target_final = original_amount - target_savings
                
                calculations.update({
                    'target_percentage': target_percentage,
                    'target_savings_amount': round(target_savings, 2),
                    'target_final_amount': round(target_final, 2),
                    'target_annual_savings': round(target_savings * 12, 2)
                })
            
            # Calculate scenario analysis
            scenarios = {}
            for scenario, percentage in [('conservative', 10), ('moderate', 20), ('aggressive', 30)]:
                scenario_savings = original_amount * (percentage / 100)
                scenarios[scenario] = {
                    'percentage': percentage,
                    'monthly_savings': round(scenario_savings, 2),
                    'annual_savings': round(scenario_savings * 12, 2),
                    'final_amount': round(original_amount - scenario_savings, 2)
                }
            
            calculations['scenarios'] = scenarios
            
            return json.dumps(calculations, indent=2)
            
        except Exception as e:
            logger.error(f"Error calculating savings: {str(e)}")
            return json.dumps({'error': str(e)})
    
    def generate_negotiation_script(self, context: Dict[str, Any]) -> str:
        """Generate customised negotiation script"""
        try:
            logger.info(f"Generating script for {context.get('company', 'Unknown')}")
            
            prompt = f"""
            Generate a comprehensive negotiation script based on this context:
            
            Company: {context.get('company', 'Unknown')}
            Bill Type: {context.get('bill_type', 'Unknown')}
            Amount: ${context.get('amount', 0)}
            Strategy: {context.get('strategy', 'General negotiation')}
            Customer History: {context.get('customer_history', 'Unknown')}
            Leverage Points: {context.get('leverage_points', [])}
            
            Create a complete script including:
            1. Professional opening and account verification
            2. Clear statement of purpose
            3. Specific negotiation requests
            4. Leverage points and supporting arguments
            5. Responses to common objections
            6. Escalation tactics if needed
            7. Professional closing with next steps
            
            Make the script conversational, polite but firm, and specific to this situation.
            Include placeholders for personalisation (e.g., [years as customer], [competitor name]).
            """
            
            response = self.llm.invoke(prompt)
            
            script_data = {
                'company': context.get('company', 'Unknown'),
                'bill_type': context.get('bill_type', 'Unknown'),
                'script': response.content,
                'generated_date': datetime.now().isoformat(),
                'customisation_notes': [
                    'Replace [years as customer] with actual tenure',
                    'Insert specific competitor names and offers',
                    'Adjust tone based on company culture',
                    'Personalise based on account history'
                ]
            }
            
            return json.dumps(script_data, indent=2)
            
        except Exception as e:
            logger.error(f"Error generating script: {str(e)}")
            return json.dumps({'error': str(e)})
    
    def analyse_competitors(self, company: str, service_type: str) -> str:
        """Analyse competitor offerings and market rates"""
        try:
            logger.info(f"Analysing competitors for {company} in {service_type}")
            
            prompt = f"""
            Analyse the competitive landscape for {company} in the {service_type} market:
            
            Provide analysis of:
            1. Main competitors and their positioning
            2. Typical pricing strategies in this market
            3. New customer promotions commonly offered
            4. Switching incentives and bonuses
            5. Market trends affecting pricing
            6. Seasonal patterns in offers
            7. Specific competitive advantages to leverage
            
            Focus on actionable competitive intelligence for negotiation.
            Include specific talking points about competitor offers.
            """
            
            response = self.llm.invoke(prompt)
            
            analysis_data = {
                'target_company': company,
                'service_type': service_type,
                'analysis': response.content,
                'analysis_date': datetime.now().isoformat(),
                'market_position': 'Competitive analysis based on general market knowledge',
                'negotiation_leverage': 'Use competitor offers as leverage points'
            }
            
            return json.dumps(analysis_data, indent=2)
            
        except Exception as e:
            logger.error(f"Error analysing competitors: {str(e)}")
            return json.dumps({'error': str(e)})
    
    def calculate_success_probability(self, factors: Dict[str, Any]) -> str:
        """Calculate probability of negotiation success"""
        try:
            logger.info("Calculating negotiation success probability")
            
            # Base probability factors
            base_probability = 0.5  # 50% base
            
            # Adjust based on various factors
            adjustments = []
            
            # Bill type factor
            bill_type = factors.get('bill_type', '').upper()
            if bill_type == 'UTILITY':
                base_probability += 0.1
                adjustments.append("Utility bills generally negotiable (+10%)")
            elif bill_type == 'MEDICAL':
                base_probability += 0.2
                adjustments.append("Medical bills highly negotiable (+20%)")
            elif bill_type == 'TELECOM':
                base_probability += 0.15
                adjustments.append("Telecom services very negotiable (+15%)")
            elif bill_type == 'SUBSCRIPTION':
                base_probability += 0.1
                adjustments.append("Subscriptions moderately negotiable (+10%)")
            
            # Amount factor
            amount = factors.get('amount', 0)
            if amount > 500:
                base_probability += 0.1
                adjustments.append("High amount increases leverage (+10%)")
            elif amount > 1000:
                base_probability += 0.05
                adjustments.append("Very high amount provides strong leverage (+5%)")
            
            # Customer tenure factor
            tenure = factors.get('customer_tenure_years', 0)
            if tenure > 2:
                base_probability += 0.1
                adjustments.append("Long-term customer loyalty (+10%)")
            elif tenure > 5:
                base_probability += 0.05
                adjustments.append("Very long-term customer (+5%)")
            
            # Payment history factor
            payment_history = factors.get('payment_history', 'unknown')
            if payment_history == 'excellent':
                base_probability += 0.1
                adjustments.append("Excellent payment history (+10%)")
            elif payment_history == 'good':
                base_probability += 0.05
                adjustments.append("Good payment history (+5%)")
            
            # Competition factor
            has_competitor_offers = factors.get('has_competitor_offers', False)
            if has_competitor_offers:
                base_probability += 0.15
                adjustments.append("Competitor offers provide leverage (+15%)")
            
            # Timing factor
            timing = factors.get('timing', 'normal')
            if timing == 'end_of_quarter':
                base_probability += 0.1
                adjustments.append("End of quarter timing (+10%)")
            elif timing == 'contract_renewal':
                base_probability += 0.15
                adjustments.append("Contract renewal timing (+15%)")
            
            # Cap at 95%
            final_probability = min(base_probability, 0.95)
            
            probability_data = {
                'base_probability': 0.5,
                'adjustments': adjustments,
                'final_probability': round(final_probability, 3),
                'percentage': round(final_probability * 100, 1),
                'confidence_level': 'high' if final_probability > 0.7 else 'medium' if final_probability > 0.5 else 'low',
                'calculation_date': datetime.now().isoformat(),
                'factors_considered': list(factors.keys())
            }
            
            return json.dumps(probability_data, indent=2)
            
        except Exception as e:
            logger.error(f"Error calculating success probability: {str(e)}")
            return json.dumps({'error': str(e)})
    
    def optimise_negotiation_timing(self, context: Dict[str, Any]) -> str:
        """Determine optimal timing for negotiation"""
        try:
            logger.info("Optimising negotiation timing")
            
            company = context.get('company', 'Unknown')
            bill_type = context.get('bill_type', 'Unknown')
            
            prompt = f"""
            Determine the optimal timing for negotiating with {company} for a {bill_type} bill:
            
            Consider:
            1. Company's fiscal calendar and quarter-end pressures
            2. Industry seasonal patterns
            3. Customer service availability and workload
            4. Promotional cycles and new customer offers
            5. Contract renewal periods
            6. Economic factors affecting the industry
            
            Provide specific recommendations for:
            - Best time of day to call
            - Best day of week
            - Best time of month/quarter
            - Seasonal considerations
            - What to avoid (busy periods, holidays, etc.)
            
            Include reasoning for each recommendation.
            """
            
            response = self.llm.invoke(prompt)
            
            timing_data = {
                'company': company,
                'bill_type': bill_type,
                'timing_analysis': response.content,
                'analysis_date': datetime.now().isoformat(),
                'urgency_level': context.get('urgency', 'normal'),
                'current_timing_score': self._calculate_current_timing_score()
            }
            
            return json.dumps(timing_data, indent=2)
            
        except Exception as e:
            logger.error(f"Error optimising timing: {str(e)}")
            return json.dumps({'error': str(e)})
    
    def _calculate_current_timing_score(self) -> str:
        """Calculate a timing score for the current moment"""
        now = datetime.now()
        
        # Simple scoring based on current time
        score_factors = []
        
        # Day of week (Tuesday-Thursday are generally better)
        if now.weekday() in [1, 2, 3]:  # Tue, Wed, Thu
            score_factors.append("Good day of week")
        
        # Time of day (10 AM - 4 PM generally better)
        if 10 <= now.hour <= 16:
            score_factors.append("Good time of day")
        
        # Not end of month (companies may be busier)
        if now.day < 25:
            score_factors.append("Not end-of-month rush")
        
        return f"Current timing factors: {', '.join(score_factors) if score_factors else 'Standard timing'}"

# Factory function
def create_negotiation_tools() -> List[Tool]:
    """Factory function to create negotiation tools"""
    tools_manager = NegotiationTools()
    return tools_manager.create_negotiation_tools()

if __name__ == "__main__":
    # Test the tools
    tools_manager = NegotiationTools()
    tools = tools_manager.create_negotiation_tools()
    
    print(f"Created {len(tools)} negotiation tools:")
    for tool in tools:
        print(f"- {tool.name}: {tool.description}")
    
    # Test calculator
    savings_result = tools_manager.calculate_savings(150.0, target_percentage=20)
    print(f"\nSavings calculation result: {savings_result}")
    
    # Test success probability
    test_factors = {
        'bill_type': 'UTILITY',
        'amount': 200.0,
        'customer_tenure_years': 3,
        'payment_history': 'excellent',
        'has_competitor_offers': True
    }
    
    probability_result = tools_manager.calculate_success_probability(test_factors)
    print(f"\nSuccess probability result: {probability_result}")

