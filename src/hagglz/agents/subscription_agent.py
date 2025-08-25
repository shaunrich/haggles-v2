"""
Subscription Negotiation Agent

This module implements the specialist agent for negotiating subscription bills
including streaming services, software subscriptions, and memberships.
"""

from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI
from typing import Dict, Any, TypedDict
import logging

logger = logging.getLogger(__name__)

class SubscriptionState(TypedDict, total=False):
    bill_type: str
    ocr_text: str
    company: str
    amount: float
    subscription_analysis: str
    subscription_type: str
    type_info: Dict[str, Any]
    usage_recommendations: str
    negotiation_plan: str

class SubscriptionNegotiationAgent:
    """Specialist agent for subscription bill negotiations"""
    
    def __init__(self, model: str = "gpt-4o-mini", temperature: float = 0.3):
        self.llm = ChatOpenAI(model=model, temperature=temperature)
        
        # Proven subscription negotiation scripts
        self.subscription_scripts = [
            "I've been a loyal subscriber for {duration} and I'm considering cancelling due to cost. Can you offer me a better rate?",
            "I see you're offering new customers a discount. Can existing customers get the same deal?",
            "I'm not using all the features I'm paying for. Do you have a more basic plan that would suit my needs?",
            "I'm comparing your service with competitors who are offering better prices. Can you match their rates?",
            "I'd like to cancel my subscription. Is there anything you can do to keep me as a customer?",
            "I'm experiencing financial difficulties. Do you offer any hardship discounts or payment plans?",
            "I only use this service seasonally. Do you have any pause or temporary suspension options?",
            "I'm a student/senior/military member. Are there any special discounts available for my situation?"
        ]
        
        # Common subscription types and their negotiation potential
        self.subscription_types = {
            'streaming': {
                'negotiation_potential': 0.7,
                'common_discounts': ['student', 'annual', 'bundle', 'loyalty'],
                'typical_savings': 0.25
            },
            'software': {
                'negotiation_potential': 0.8,
                'common_discounts': ['annual', 'multi-user', 'nonprofit', 'startup'],
                'typical_savings': 0.30
            },
            'fitness': {
                'negotiation_potential': 0.9,
                'common_discounts': ['annual', 'family', 'corporate', 'student'],
                'typical_savings': 0.35
            },
            'news': {
                'negotiation_potential': 0.8,
                'common_discounts': ['student', 'senior', 'annual', 'digital-only'],
                'typical_savings': 0.40
            },
            'cloud': {
                'negotiation_potential': 0.6,
                'common_discounts': ['annual', 'volume', 'startup', 'nonprofit'],
                'typical_savings': 0.20
            }
        }
        
    def build_graph(self):
        """Build the subscription negotiation workflow graph"""
        
        workflow = StateGraph(SubscriptionState)
        
        def identify_subscription_type(state: SubscriptionState) -> SubscriptionState:
            """Identify the specific type of subscription"""
            logger.info("Identifying subscription type and characteristics")
            
            prompt = f"""
            Analyse this subscription bill to identify the service type and characteristics:
            
            Bill Details:
            - Company: {state.get('company', 'Unknown')}
            - Amount: ${state.get('amount', 0)}
            - Bill Text: {state['ocr_text']}
            
            Identify:
            1. Service category (streaming, software, fitness, news, cloud, other)
            2. Subscription tier/plan level
            3. Billing frequency (monthly, annual, etc.)
            4. Service features included
            5. Contract terms if mentioned
            
            Common subscription categories:
            - Streaming: Netflix, Spotify, Disney+, etc.
            - Software: Adobe, Microsoft, Salesforce, etc.
            - Fitness: Gym memberships, fitness apps
            - News: Newspapers, magazines, news sites
            - Cloud: AWS, Google Cloud, hosting services
            - Other: Various subscription services
            
            Provide detailed analysis of the subscription characteristics.
            """
            
            try:
                response = self.llm.invoke(prompt)
                state['subscription_analysis'] = response.content
                
                # Determine subscription type from analysis
                analysis_text = response.content.lower()
                detected_type = 'other'  # default
                
                for sub_type in self.subscription_types.keys():
                    if sub_type in analysis_text:
                        detected_type = sub_type
                        break
                
                state['subscription_type'] = detected_type
                state['type_info'] = self.subscription_types.get(detected_type, {
                    'negotiation_potential': 0.6,
                    'common_discounts': ['annual', 'loyalty'],
                    'typical_savings': 0.25
                })
                
                logger.info(f"Subscription type identified: {detected_type}")
                
            except Exception as e:
                logger.error(f"Error identifying subscription type: {str(e)}")
                state['subscription_analysis'] = "Analysis unavailable"
                state['subscription_type'] = 'other'
                state['type_info'] = self.subscription_types['streaming']  # default
                
            return state
        
        def analyse_usage_patterns(state: SubscriptionState) -> SubscriptionState:
            """Analyse subscription usage and value"""
            logger.info("Analysing subscription usage patterns and value")
            
            prompt = f"""
            Analyse the value and usage potential for this subscription:
            
            Subscription: {state.get('company', 'Unknown')}
            Type: {state.get('subscription_type', 'Unknown')}
            Amount: ${state.get('amount', 0)}
            
            Analysis Focus:
            1. Cost per month/year analysis
            2. Feature utilisation assessment
            3. Alternative options available
            4. Seasonal usage patterns
            5. Value proposition evaluation
            
            Consider:
            - Is this a premium tier that could be downgraded?
            - Are there unused features being paid for?
            - How does the price compare to competitors?
            - Are there bundle opportunities?
            - Is the billing frequency optimal?
            
            Provide insights for negotiation leverage including:
            - Overpriced features or tiers
            - Competitor pricing advantages
            - Usage-based arguments
            - Downgrade opportunities
            - Bundle or package alternatives
            """
            
            try:
                response = self.llm.invoke(prompt)
                state['usage_analysis'] = response.content
                logger.info("Usage analysis completed")
                
            except Exception as e:
                logger.error(f"Error in usage analysis: {str(e)}")
                state['usage_analysis'] = "Usage analysis unavailable"
                
            return state
        
        def research_alternatives(state: SubscriptionState) -> SubscriptionState:
            """Research alternative plans and competitor options"""
            logger.info("Researching subscription alternatives and competitors")
            
            subscription_type = state.get('subscription_type', 'other')
            
            prompt = f"""
            Research alternatives and competitive options for this subscription:
            
            Current Service: {state.get('company', 'Unknown')}
            Type: {subscription_type}
            Current Cost: ${state.get('amount', 0)}
            
            Research Areas:
            1. Lower-tier plans from the same provider
            2. Competitor services and pricing
            3. Bundle opportunities
            4. Annual vs monthly pricing differences
            5. Special discount programmes
            
            For {subscription_type} subscriptions, consider:
            - Free tier alternatives
            - Student/senior/military discounts
            - Family or group plans
            - Annual payment discounts
            - Promotional rates for new customers
            
            Provide specific alternatives including:
            - Alternative plan names and prices
            - Competitor services and costs
            - Discount programmes available
            - Bundle opportunities
            - Negotiation talking points based on alternatives
            """
            
            try:
                response = self.llm.invoke(prompt)
                state['alternatives_research'] = response.content
                logger.info("Alternatives research completed")
                
            except Exception as e:
                logger.error(f"Error researching alternatives: {str(e)}")
                state['alternatives_research'] = "Alternatives research unavailable"
                
            return state
        
        def generate_subscription_strategy(state: SubscriptionState) -> SubscriptionState:
            """Generate subscription negotiation strategy"""
            logger.info("Generating subscription negotiation strategy")
            
            type_info = state.get('type_info', {})
            negotiation_potential = type_info.get('negotiation_potential', 0.6)
            
            prompt = f"""
            Create a comprehensive subscription negotiation strategy:
            
            Subscription Details:
            - Service: {state.get('company', 'Unknown')}
            - Type: {state.get('subscription_type', 'Unknown')}
            - Amount: ${state.get('amount', 0)}
            - Negotiation Potential: {negotiation_potential}
            
            Analysis Results:
            - Usage Analysis: {state.get('usage_analysis', 'Not available')}
            - Alternatives: {state.get('alternatives_research', 'Not available')}
            
            Strategy Development:
            1. Primary negotiation approach
            2. Specific discount requests
            3. Alternative plan considerations
            4. Cancellation leverage tactics
            5. Timing recommendations
            
            Subscription Negotiation Approaches:
            - Loyalty-based: Emphasise long-term subscription
            - Competition-based: Reference competitor pricing
            - Downgrade threat: Consider lower-tier plans
            - Cancellation leverage: Threaten to cancel service
            - Bundle opportunity: Explore package deals
            - Payment terms: Annual vs monthly negotiations
            
            Common Subscription Discounts:
            {type_info.get('common_discounts', [])}
            
            Provide a detailed negotiation strategy with specific tactics.
            """
            
            try:
                response = self.llm.invoke(prompt)
                state['negotiation_strategy'] = response.content
                
                # Calculate confidence based on subscription type and analysis
                base_confidence = negotiation_potential * 0.7  # Base on type potential
                
                strategy_text = response.content.lower()
                confidence_factors = [
                    'competitor' in strategy_text,
                    'discount' in strategy_text,
                    'cancel' in strategy_text,
                    'alternative' in strategy_text,
                    'loyalty' in strategy_text
                ]
                
                strategy_bonus = sum(confidence_factors) * 0.05
                state['confidence_score'] = min(base_confidence + strategy_bonus, 0.9)
                
                logger.info(f"Subscription strategy generated with confidence: {state['confidence_score']}")
                
            except Exception as e:
                logger.error(f"Error generating subscription strategy: {str(e)}")
                state['negotiation_strategy'] = "Strategy generation failed"
                state['confidence_score'] = 0.4
                
            return state
        
        def create_subscription_script(state: SubscriptionState) -> SubscriptionState:
            """Generate subscription negotiation script"""
            logger.info("Creating subscription negotiation script")
            
            strategy_text = state.get('negotiation_strategy', '').lower()
            subscription_type = state.get('subscription_type', 'other')
            
            # Select appropriate scripts based on strategy
            selected_scripts = []
            
            if 'loyalty' in strategy_text:
                selected_scripts.append(self.subscription_scripts[0])
            if 'competitor' in strategy_text:
                selected_scripts.extend([self.subscription_scripts[1], self.subscription_scripts[3]])
            if 'cancel' in strategy_text:
                selected_scripts.append(self.subscription_scripts[4])
            if 'downgrade' in strategy_text:
                selected_scripts.append(self.subscription_scripts[2])
            if 'hardship' in strategy_text:
                selected_scripts.append(self.subscription_scripts[5])
            
            # Default scripts if none selected
            if not selected_scripts:
                selected_scripts = self.subscription_scripts[:3]
            
            prompt = f"""
            Create a complete subscription negotiation script:
            
            Service: {state.get('company', 'Unknown')}
            Type: {subscription_type}
            Amount: ${state.get('amount', 0)}
            Strategy: {state.get('negotiation_strategy', 'Not available')}
            
            Use these proven subscription negotiation approaches:
            {chr(10).join(selected_scripts)}
            
            Create a complete dialogue including:
            1. Friendly opening and account identification
            2. Reason for calling (cost concerns, competition, etc.)
            3. Specific requests:
               - Discount percentages
               - Plan downgrades
               - Promotional rates
               - Payment term changes
            4. Leverage points (cancellation, competition, loyalty)
            5. Alternative solutions if initial request denied
            6. Closing with clear next steps
            
            Subscription Negotiation Tips:
            - Be prepared to actually cancel if needed
            - Ask for retention department
            - Mention specific competitor offers
            - Request supervisor if first agent can't help
            - Be polite but persistent
            - Ask about unadvertised promotions
            
            Make the script conversational and specific to this subscription type.
            """
            
            try:
                response = self.llm.invoke(prompt)
                state['script'] = response.content
                logger.info("Subscription negotiation script created")
                
            except Exception as e:
                logger.error(f"Error creating subscription script: {str(e)}")
                state['script'] = "Script generation failed"
                
            return state
        
        def calculate_subscription_savings(state: SubscriptionState) -> SubscriptionState:
            """Calculate potential savings for subscription"""
            logger.info("Calculating subscription savings potential")
            
            current_amount = state.get('amount', 0)
            type_info = state.get('type_info', {})
            typical_savings = type_info.get('typical_savings', 0.25)
            
            # Subscription savings scenarios
            savings_scenarios = {
                'conservative': typical_savings * 0.6,    # 60% of typical
                'moderate': typical_savings,              # Typical savings
                'aggressive': typical_savings * 1.4      # 140% of typical
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
            
            # Set target savings based on confidence
            confidence = state.get('confidence_score', 0.5)
            if confidence > 0.8:
                state['target_savings'] = savings_analysis['aggressive']
            elif confidence > 0.6:
                state['target_savings'] = savings_analysis['moderate']
            else:
                state['target_savings'] = savings_analysis['conservative']
            
            logger.info(f"Subscription savings potential calculated: {state['target_savings']}")
            return state
        
        # Add nodes to workflow
        workflow.add_node("identify_type", identify_subscription_type)
        workflow.add_node("analyse_usage", analyse_usage_patterns)
        workflow.add_node("research_alternatives", research_alternatives)
        workflow.add_node("generate_strategy", generate_subscription_strategy)
        workflow.add_node("create_script", create_subscription_script)
        workflow.add_node("calculate_savings", calculate_subscription_savings)
        
        # Define edges
        workflow.add_edge("identify_type", "analyse_usage")
        workflow.add_edge("analyse_usage", "research_alternatives")
        workflow.add_edge("research_alternatives", "generate_strategy")
        workflow.add_edge("generate_strategy", "create_script")
        workflow.add_edge("create_script", "calculate_savings")
        workflow.add_edge("calculate_savings", END)
        
        workflow.set_entry_point("identify_type")
        
        return workflow.compile()
    
    def process_subscription_bill(self, bill_state: SubscriptionState) -> SubscriptionState:
        """Process a subscription bill through the negotiation workflow"""
        if not hasattr(self, '_compiled_workflow'):
            self._compiled_workflow = self.build_graph()
        
        result = self._compiled_workflow.invoke(bill_state)
        return result

def create_subscription_agent():
    """Factory function to create subscription negotiation agent"""
    agent = SubscriptionNegotiationAgent()
    return agent.build_graph()

if __name__ == "__main__":
    # Test the subscription agent
    agent = SubscriptionNegotiationAgent()
    workflow = agent.build_graph()
    
    test_state = {
        'bill_type': 'SUBSCRIPTION',
        'ocr_text': 'NETFLIX PREMIUM\nMonthly Subscription\nAmount: $19.99',
        'company': 'Netflix',
        'amount': 19.99,
        'conversation_history': []
    }
    
    result = workflow.invoke(test_state)
    print(f"Subscription Type: {result.get('subscription_type', 'Unknown')}")
    print(f"Strategy: {result.get('negotiation_strategy', 'Not generated')[:200]}...")
    print(f"Confidence: {result.get('confidence_score', 0)}")
    print(f"Target Savings: {result.get('target_savings', {})}")

