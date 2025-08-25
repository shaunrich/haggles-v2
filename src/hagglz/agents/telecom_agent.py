"""
Telecom Negotiation Agent

This module implements the specialist agent for negotiating telecom bills
including phone, internet, cable, and mobile service bills.
"""

from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)

class TelecomNegotiationAgent:
    """Specialist agent for telecom bill negotiations"""
    
    def __init__(self, model: str = "gpt-4o-mini", temperature: float = 0.3):
        self.llm = ChatOpenAI(model=model, temperature=temperature)
        
        # Proven telecom negotiation scripts
        self.telecom_scripts = [
            "I've been a loyal customer for {years} years and I'm considering switching to {competitor}. Can you offer me a better rate?",
            "I see {competitor} is offering {specific_offer}. Can you match or beat that deal?",
            "My promotional rate has expired and my bill has increased significantly. Can we discuss options to reduce it?",
            "I'm only using {usage_amount} of my plan. Do you have a more suitable plan for my usage?",
            "I'm bundling services with you but I think I'm overpaying. Can we review my package?",
            "I'm experiencing financial hardship. Are there any assistance programmes or reduced-rate plans available?",
            "I'm ready to cancel my service today unless we can work out a better deal.",
            "I don't need all these features I'm paying for. Can we customise a plan that better fits my needs?"
        ]
        
        # Telecom service types and their characteristics
        self.telecom_types = {
            'mobile': {
                'negotiation_potential': 0.8,
                'common_tactics': ['competitor_comparison', 'usage_analysis', 'loyalty_discount'],
                'typical_savings': 0.25,
                'key_factors': ['data_usage', 'call_minutes', 'contract_status']
            },
            'internet': {
                'negotiation_potential': 0.9,
                'common_tactics': ['speed_downgrade', 'competitor_offers', 'bundle_analysis'],
                'typical_savings': 0.30,
                'key_factors': ['speed_requirements', 'data_caps', 'promotional_expiry']
            },
            'cable': {
                'negotiation_potential': 0.9,
                'common_tactics': ['cord_cutting_threat', 'channel_reduction', 'streaming_alternatives'],
                'typical_savings': 0.35,
                'key_factors': ['channel_usage', 'streaming_services', 'contract_terms']
            },
            'landline': {
                'negotiation_potential': 0.7,
                'common_tactics': ['necessity_question', 'basic_plan', 'bundle_removal'],
                'typical_savings': 0.40,
                'key_factors': ['actual_usage', 'mobile_alternative', 'emergency_needs']
            },
            'bundle': {
                'negotiation_potential': 0.8,
                'common_tactics': ['service_separation', 'competitor_bundles', 'usage_optimisation'],
                'typical_savings': 0.25,
                'key_factors': ['individual_service_costs', 'usage_patterns', 'contract_flexibility']
            }
        }
        
    def build_graph(self):
        """Build the telecom negotiation workflow graph"""
        
        workflow = StateGraph(dict)
        
        def identify_telecom_services(state: Dict[str, Any]) -> Dict[str, Any]:
            """Identify telecom services and plan details"""
            logger.info("Identifying telecom services and plan characteristics")
            
            prompt = f"""
            Analyse this telecom bill to identify services and plan details:
            
            Bill Details:
            - Provider: {state.get('company', 'Unknown')}
            - Amount: ${state.get('amount', 0)}
            - Bill Text: {state['ocr_text']}
            
            Identify:
            1. Service types (mobile, internet, cable TV, landline, bundle)
            2. Plan details (data limits, speeds, channels, minutes)
            3. Contract status (month-to-month, contract term)
            4. Promotional rates and expiry dates
            5. Add-on services and fees
            6. Usage patterns if mentioned
            
            Service Categories:
            - Mobile: Cell phone plans, data plans
            - Internet: Broadband, fibre, DSL
            - Cable: TV packages, premium channels
            - Landline: Home phone service
            - Bundle: Combined services package
            
            Provide detailed analysis of:
            - Primary service type
            - Plan specifications
            - Contract terms
            - Promotional pricing status
            - Additional fees and services
            """
            
            try:
                response = self.llm.invoke(prompt)
                state['service_analysis'] = response.content
                
                # Determine primary service type
                analysis_text = response.content.lower()
                detected_type = 'bundle'  # default assumption
                
                # Check for specific service indicators
                if 'mobile' in analysis_text or 'cell' in analysis_text:
                    detected_type = 'mobile'
                elif 'internet' in analysis_text and 'cable' not in analysis_text:
                    detected_type = 'internet'
                elif 'cable' in analysis_text or 'tv' in analysis_text:
                    detected_type = 'cable'
                elif 'landline' in analysis_text or 'home phone' in analysis_text:
                    detected_type = 'landline'
                elif 'bundle' in analysis_text or ('internet' in analysis_text and 'tv' in analysis_text):
                    detected_type = 'bundle'
                
                state['telecom_type'] = detected_type
                state['type_info'] = self.telecom_types.get(detected_type, self.telecom_types['bundle'])
                
                logger.info(f"Telecom type identified: {detected_type}")
                
            except Exception as e:
                logger.error(f"Error identifying telecom services: {str(e)}")
                state['service_analysis'] = "Analysis unavailable"
                state['telecom_type'] = 'bundle'
                state['type_info'] = self.telecom_types['bundle']
                
            return state
        
        def analyse_usage_and_needs(state: Dict[str, Any]) -> Dict[str, Any]:
            """Analyse usage patterns and actual needs"""
            logger.info("Analysing telecom usage patterns and needs")
            
            telecom_type = state.get('telecom_type', 'bundle')
            type_info = state.get('type_info', {})
            
            prompt = f"""
            Analyse usage patterns and needs for this telecom service:
            
            Service Type: {telecom_type}
            Provider: {state.get('company', 'Unknown')}
            Current Cost: ${state.get('amount', 0)}
            Service Details: {state.get('service_analysis', 'Not available')}
            
            Key Analysis Areas for {telecom_type}:
            {type_info.get('key_factors', [])}
            
            Usage Analysis:
            1. Current plan vs actual needs assessment
            2. Overprovisioned services identification
            3. Underutilised features and add-ons
            4. Seasonal or changing usage patterns
            5. Alternative service options
            
            Consider:
            - Are you paying for more than you use?
            - Which features are essential vs nice-to-have?
            - How do your needs compare to plan offerings?
            - Are there more cost-effective alternatives?
            - What usage trends might affect future needs?
            
            Provide insights for:
            - Plan optimisation opportunities
            - Service reduction possibilities
            - Usage-based negotiation arguments
            - Alternative plan recommendations
            """
            
            try:
                response = self.llm.invoke(prompt)
                state['usage_analysis'] = response.content
                logger.info("Usage analysis completed")
                
            except Exception as e:
                logger.error(f"Error in usage analysis: {str(e)}")
                state['usage_analysis'] = "Usage analysis unavailable"
                
            return state
        
        def research_competitor_offers(state: Dict[str, Any]) -> Dict[str, Any]:
            """Research competitor offers and market rates"""
            logger.info("Researching telecom competitor offers and market rates")
            
            telecom_type = state.get('telecom_type', 'bundle')
            current_amount = state.get('amount', 0)
            
            prompt = f"""
            Research competitive landscape for this telecom service:
            
            Current Service: {telecom_type}
            Provider: {state.get('company', 'Unknown')}
            Current Cost: ${current_amount}
            
            Research Focus:
            1. Major competitor pricing for similar services
            2. New customer promotional offers
            3. Switching incentives and bonuses
            4. Alternative service providers
            5. Market rate comparisons
            
            For {telecom_type} services, research:
            - Competitor names and their typical pricing
            - Promotional rates for new customers
            - Service quality and speed comparisons
            - Contract terms and flexibility
            - Switching costs and benefits
            
            Provide specific competitive intelligence including:
            - Competitor names and offers
            - Price comparisons for similar services
            - New customer incentives
            - Service quality differences
            - Negotiation leverage points based on competition
            
            Focus on actionable competitive information for negotiation.
            """
            
            try:
                response = self.llm.invoke(prompt)
                state['competitor_research'] = response.content
                logger.info("Competitor research completed")
                
            except Exception as e:
                logger.error(f"Error researching competitors: {str(e)}")
                state['competitor_research'] = "Competitor research unavailable"
                
            return state
        
        def generate_telecom_strategy(state: Dict[str, Any]) -> Dict[str, Any]:
            """Generate telecom negotiation strategy"""
            logger.info("Generating telecom negotiation strategy")
            
            telecom_type = state.get('telecom_type', 'bundle')
            type_info = state.get('type_info', {})
            negotiation_potential = type_info.get('negotiation_potential', 0.8)
            
            prompt = f"""
            Create a comprehensive telecom negotiation strategy:
            
            Service Details:
            - Type: {telecom_type}
            - Provider: {state.get('company', 'Unknown')}
            - Amount: ${state.get('amount', 0)}
            - Negotiation Potential: {negotiation_potential}
            
            Analysis Results:
            - Service Analysis: {state.get('service_analysis', 'Not available')}
            - Usage Analysis: {state.get('usage_analysis', 'Not available')}
            - Competitor Research: {state.get('competitor_research', 'Not available')}
            
            Strategy Development:
            1. Primary negotiation approach
            2. Specific discount targets
            3. Plan modification opportunities
            4. Competitive leverage points
            5. Escalation tactics
            
            Common Telecom Negotiation Tactics:
            {type_info.get('common_tactics', [])}
            
            Telecom-Specific Approaches:
            - Retention department: Ask for cancellation/retention team
            - Competitor matching: Reference specific competitor offers
            - Plan optimisation: Right-size services to actual usage
            - Promotional recovery: Request new customer rates
            - Bundle analysis: Evaluate individual vs bundled pricing
            - Contract leverage: Use contract end dates for negotiation
            
            Telecom Industry Insights:
            - High customer acquisition costs make retention valuable
            - Promotional rates are often renewable with negotiation
            - Retention departments have more authority than regular support
            - Competitor switching is common and expected
            - Usage-based arguments are particularly effective
            
            Provide a detailed, step-by-step negotiation strategy.
            """
            
            try:
                response = self.llm.invoke(prompt)
                state['negotiation_strategy'] = response.content
                
                # Calculate confidence based on telecom type and factors
                base_confidence = negotiation_potential * 0.8
                
                strategy_text = response.content.lower()
                confidence_factors = [
                    'competitor' in strategy_text,
                    'retention' in strategy_text,
                    'promotional' in strategy_text,
                    'usage' in strategy_text,
                    'cancel' in strategy_text
                ]
                
                strategy_bonus = sum(confidence_factors) * 0.04
                state['confidence_score'] = min(base_confidence + strategy_bonus, 0.95)
                
                logger.info(f"Telecom strategy generated with confidence: {state['confidence_score']}")
                
            except Exception as e:
                logger.error(f"Error generating telecom strategy: {str(e)}")
                state['negotiation_strategy'] = "Strategy generation failed"
                state['confidence_score'] = 0.5
                
            return state
        
        def create_telecom_script(state: Dict[str, Any]) -> Dict[str, Any]:
            """Generate telecom negotiation script"""
            logger.info("Creating telecom negotiation script")
            
            strategy_text = state.get('negotiation_strategy', '').lower()
            telecom_type = state.get('telecom_type', 'bundle')
            
            # Select appropriate scripts based on strategy
            selected_scripts = []
            
            if 'competitor' in strategy_text:
                selected_scripts.extend([self.telecom_scripts[0], self.telecom_scripts[1]])
            if 'promotional' in strategy_text:
                selected_scripts.append(self.telecom_scripts[2])
            if 'usage' in strategy_text:
                selected_scripts.extend([self.telecom_scripts[3], self.telecom_scripts[7]])
            if 'bundle' in strategy_text:
                selected_scripts.append(self.telecom_scripts[4])
            if 'cancel' in strategy_text:
                selected_scripts.append(self.telecom_scripts[6])
            
            # Default scripts if none selected
            if not selected_scripts:
                selected_scripts = self.telecom_scripts[:3]
            
            prompt = f"""
            Create a complete telecom negotiation script:
            
            Service: {state.get('company', 'Unknown')}
            Type: {telecom_type}
            Amount: ${state.get('amount', 0)}
            Strategy: {state.get('negotiation_strategy', 'Not available')}
            
            Use these proven telecom negotiation approaches:
            {chr(10).join(selected_scripts)}
            
            Create a complete dialogue including:
            1. Account verification and service identification
            2. Clear statement of intent (retention/cost reduction)
            3. Specific requests:
               - Rate reductions or promotional pricing
               - Plan modifications or downgrades
               - Competitor price matching
               - Contract term adjustments
            4. Leverage points:
               - Competitor offers
               - Loyalty history
               - Cancellation consideration
               - Usage optimisation
            5. Escalation requests (retention department)
            6. Clear next steps and follow-up
            
            Telecom Negotiation Best Practices:
            - Ask for retention/cancellation department immediately
            - Have specific competitor offers ready to reference
            - Be prepared to actually cancel if needed
            - Request supervisor if first agent can't help
            - Ask about unadvertised promotions
            - Get any agreements in writing
            - Confirm effective dates and terms
            
            Make the script specific to {telecom_type} services and this provider.
            """
            
            try:
                response = self.llm.invoke(prompt)
                state['script'] = response.content
                logger.info("Telecom negotiation script created")
                
            except Exception as e:
                logger.error(f"Error creating telecom script: {str(e)}")
                state['script'] = "Script generation failed"
                
            return state
        
        def calculate_telecom_savings(state: Dict[str, Any]) -> Dict[str, Any]:
            """Calculate potential savings for telecom services"""
            logger.info("Calculating telecom savings potential")
            
            current_amount = state.get('amount', 0)
            type_info = state.get('type_info', {})
            typical_savings = type_info.get('typical_savings', 0.25)
            
            # Telecom savings scenarios (generally high potential)
            savings_scenarios = {
                'conservative': typical_savings * 0.7,    # 70% of typical
                'moderate': typical_savings,              # Typical savings
                'aggressive': typical_savings * 1.3      # 130% of typical
            }
            
            savings_analysis = {}
            for scenario, percentage in savings_scenarios.items():
                monthly_savings = current_amount * percentage
                annual_savings = monthly_savings * 12
                savings_analysis[scenario] = {
                    'monthly_savings': round(monthly_savings, 2),
                    'annual_savings': round(annual_savings, 2),
                    'percentage': round(percentage * 100, 1)
                }
            
            state['savings_potential'] = savings_analysis
            
            # Set target savings based on confidence and service type
            confidence = state.get('confidence_score', 0.5)
            negotiation_potential = type_info.get('negotiation_potential', 0.8)
            
            if confidence > 0.8 and negotiation_potential > 0.8:
                state['target_savings'] = savings_analysis['aggressive']
            elif confidence > 0.6:
                state['target_savings'] = savings_analysis['moderate']
            else:
                state['target_savings'] = savings_analysis['conservative']
            
            logger.info(f"Telecom savings potential calculated: {state['target_savings']}")
            return state
        
        # Add nodes to workflow
        workflow.add_node("identify_services", identify_telecom_services)
        workflow.add_node("analyse_usage", analyse_usage_and_needs)
        workflow.add_node("research_competitors", research_competitor_offers)
        workflow.add_node("generate_strategy", generate_telecom_strategy)
        workflow.add_node("create_script", create_telecom_script)
        workflow.add_node("calculate_savings", calculate_telecom_savings)
        
        # Define edges
        workflow.add_edge("identify_services", "analyse_usage")
        workflow.add_edge("analyse_usage", "research_competitors")
        workflow.add_edge("research_competitors", "generate_strategy")
        workflow.add_edge("generate_strategy", "create_script")
        workflow.add_edge("create_script", "calculate_savings")
        workflow.add_edge("calculate_savings", END)
        
        workflow.set_entry_point("identify_services")
        
        return workflow.compile()
    
    def process_telecom_bill(self, bill_state: Dict[str, Any]) -> Dict[str, Any]:
        """Process a telecom bill through the negotiation workflow"""
        if not hasattr(self, '_compiled_workflow'):
            self._compiled_workflow = self.build_graph()
        
        result = self._compiled_workflow.invoke(bill_state)
        return result

def create_telecom_agent():
    """Factory function to create telecom negotiation agent"""
    agent = TelecomNegotiationAgent()
    return agent.build_graph()

if __name__ == "__main__":
    # Test the telecom agent
    agent = TelecomNegotiationAgent()
    workflow = agent.build_graph()
    
    test_state = {
        'bill_type': 'TELECOM',
        'ocr_text': 'VERIZON WIRELESS\nUnlimited Plan\nMonthly Charge: $85.00',
        'company': 'Verizon Wireless',
        'amount': 85.00,
        'conversation_history': []
    }
    
    result = workflow.invoke(test_state)
    print(f"Telecom Type: {result.get('telecom_type', 'Unknown')}")
    print(f"Strategy: {result.get('negotiation_strategy', 'Not generated')[:200]}...")
    print(f"Confidence: {result.get('confidence_score', 0)}")
    print(f"Target Savings: {result.get('target_savings', {})}")

