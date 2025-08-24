"""
Master Orchestrator for Hagglz Negotiation System

This module implements the main orchestrator that coordinates all specialist agents,
manages confidence-based routing, and controls the overall negotiation workflow.
"""

from langgraph.graph import StateGraph, END
from typing import Annotated, Sequence, Dict, Any, Literal
from langchain_core.messages import BaseMessage
import operator
import logging

# Import specialist agents
from agents.router_agent import RouterAgent
from agents.utility_agent import UtilityNegotiationAgent
from agents.medical_agent import MedicalNegotiationAgent
from agents.subscription_agent import SubscriptionNegotiationAgent
from agents.telecom_agent import TelecomNegotiationAgent

logger = logging.getLogger(__name__)

class NegotiationState(Dict[str, Any]):
    """Enhanced state structure for the negotiation workflow"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Ensure all required fields exist with defaults
        self.setdefault('messages', [])
        self.setdefault('bill_data', {})
        self.setdefault('agent_decision', '')
        self.setdefault('negotiation_result', {})
        self.setdefault('confidence_score', 0.0)
        self.setdefault('execution_mode', '')
        self.setdefault('error_messages', [])
        self.setdefault('processing_status', 'pending')

class MasterOrchestrator:
    """Master orchestrator for the Hagglz negotiation system"""
    
    def __init__(self):
        self.workflow = None
        
        # Confidence thresholds as per specification
        self.CONFIDENCE_THRESHOLD_AUTO = 0.8
        self.CONFIDENCE_THRESHOLD_SUPERVISED = 0.5
        
        # Initialize specialist agents
        self.router_agent = RouterAgent()
        self.utility_agent = UtilityNegotiationAgent()
        self.medical_agent = MedicalNegotiationAgent()
        self.subscription_agent = SubscriptionNegotiationAgent()
        self.telecom_agent = TelecomNegotiationAgent()
        
        # Compile agent workflows
        self._compile_agents()
        
    def _compile_agents(self):
        """Compile all specialist agent workflows"""
        try:
            self.router_workflow = self.router_agent.create_router_graph()
            self.utility_workflow = self.utility_agent.build_graph()
            self.medical_workflow = self.medical_agent.build_graph()
            self.subscription_workflow = self.subscription_agent.build_graph()
            self.telecom_workflow = self.telecom_agent.build_graph()
            logger.info("All specialist agents compiled successfully")
        except Exception as e:
            logger.error(f"Error compiling specialist agents: {str(e)}")
            raise
    
    def create_master_orchestrator(self):
        """Create the master orchestrator workflow"""
        workflow = StateGraph(NegotiationState)
        
        def route_negotiation(state: NegotiationState) -> NegotiationState:
            """Route bill to appropriate specialist agent"""
            logger.info("Starting bill routing process")
            
            try:
                # Extract OCR text from bill data
                ocr_text = state.get('bill_data', {}).get('text', '')
                if not ocr_text:
                    raise ValueError("No OCR text provided in bill data")
                
                # Use router agent to classify bill
                router_result = self.router_agent.process_bill(ocr_text)
                
                # Update state with routing results
                state['agent_decision'] = router_result.get('bill_type', 'UTILITY')
                state['bill_data'].update({
                    'company': router_result.get('company', 'Unknown'),
                    'amount': router_result.get('amount', 0.0),
                    'bill_type': router_result.get('bill_type', 'UTILITY')
                })
                
                state['processing_status'] = 'routed'
                logger.info(f"Bill routed to: {state['agent_decision']}")
                
            except Exception as e:
                logger.error(f"Error in bill routing: {str(e)}")
                state['error_messages'].append(f"Routing error: {str(e)}")
                state['agent_decision'] = 'UTILITY'  # Default fallback
                state['processing_status'] = 'routing_error'
            
            return state
        
        def execute_specialist_agent(state: NegotiationState) -> NegotiationState:
            """Execute the appropriate specialist agent"""
            logger.info(f"Executing specialist agent: {state['agent_decision']}")
            
            try:
                agent_type = state['agent_decision']
                
                # Select appropriate specialist agent
                agent_workflows = {
                    'UTILITY': self.utility_workflow,
                    'MEDICAL': self.medical_workflow,
                    'SUBSCRIPTION': self.subscription_workflow,
                    'TELECOM': self.telecom_workflow
                }
                
                selected_workflow = agent_workflows.get(agent_type)
                if not selected_workflow:
                    raise ValueError(f"Unknown agent type: {agent_type}")
                
                # Prepare state for specialist agent
                specialist_state = {
                    'bill_type': state['bill_data'].get('bill_type', agent_type),
                    'ocr_text': state['bill_data'].get('text', ''),
                    'company': state['bill_data'].get('company', 'Unknown'),
                    'amount': state['bill_data'].get('amount', 0.0),
                    'conversation_history': state.get('messages', [])
                }
                
                # Execute specialist workflow
                result = selected_workflow.invoke(specialist_state)
                
                # Update state with specialist results
                state['negotiation_result'] = result
                state['confidence_score'] = result.get('confidence_score', 0.5)
                state['processing_status'] = 'specialist_complete'
                
                logger.info(f"Specialist agent completed with confidence: {state['confidence_score']}")
                
            except Exception as e:
                logger.error(f"Error executing specialist agent: {str(e)}")
                state['error_messages'].append(f"Specialist execution error: {str(e)}")
                state['confidence_score'] = 0.0
                state['processing_status'] = 'specialist_error'
                state['negotiation_result'] = {
                    'error': str(e),
                    'strategy': 'Error occurred during processing',
                    'script': 'Unable to generate script due to error'
                }
            
            return state
        
        def evaluate_confidence(state: NegotiationState) -> str:
            """Evaluate confidence and determine execution mode"""
            confidence = state.get('confidence_score', 0.0)
            
            logger.info(f"Evaluating confidence score: {confidence}")
            
            # Apply confidence thresholds as per specification
            if confidence >= self.CONFIDENCE_THRESHOLD_AUTO:
                execution_mode = "auto_execute"
                logger.info("High confidence - auto execution mode")
            elif confidence >= self.CONFIDENCE_THRESHOLD_SUPERVISED:
                execution_mode = "supervised"
                logger.info("Medium confidence - supervised execution mode")
            else:
                execution_mode = "human_handoff"
                logger.info("Low confidence - human handoff required")
            
            state['execution_mode'] = execution_mode
            return execution_mode
        
        def auto_execute_negotiation(state: NegotiationState) -> NegotiationState:
            """Handle automatic execution of high-confidence negotiations"""
            logger.info("Processing auto-execution negotiation")
            
            state['processing_status'] = 'auto_ready'
            state['execution_instructions'] = {
                'mode': 'automatic',
                'confidence': state.get('confidence_score', 0.0),
                'strategy': state.get('negotiation_result', {}).get('negotiation_strategy', ''),
                'script': state.get('negotiation_result', {}).get('script', ''),
                'target_savings': state.get('negotiation_result', {}).get('target_savings', {}),
                'next_steps': [
                    'Execute negotiation script automatically',
                    'Monitor conversation progress',
                    'Apply fallback strategies if needed',
                    'Report results to user'
                ]
            }
            
            return state
        
        def supervised_execution(state: NegotiationState) -> NegotiationState:
            """Handle supervised execution of medium-confidence negotiations"""
            logger.info("Processing supervised execution negotiation")
            
            state['processing_status'] = 'supervised_ready'
            state['execution_instructions'] = {
                'mode': 'supervised',
                'confidence': state.get('confidence_score', 0.0),
                'strategy': state.get('negotiation_result', {}).get('negotiation_strategy', ''),
                'script': state.get('negotiation_result', {}).get('script', ''),
                'target_savings': state.get('negotiation_result', {}).get('target_savings', {}),
                'supervision_required': [
                    'Review negotiation strategy before execution',
                    'Monitor conversation in real-time',
                    'Approve key negotiation points',
                    'Intervene if conversation goes off-track'
                ],
                'next_steps': [
                    'Present strategy for human review',
                    'Execute with human oversight',
                    'Confirm key decisions during negotiation',
                    'Report results to user'
                ]
            }
            
            return state
        
        def human_handoff(state: NegotiationState) -> NegotiationState:
            """Handle human handoff for low-confidence negotiations"""
            logger.info("Processing human handoff")
            
            state['processing_status'] = 'human_handoff_ready'
            state['execution_instructions'] = {
                'mode': 'human_handoff',
                'confidence': state.get('confidence_score', 0.0),
                'reason': 'Low confidence score requires human intervention',
                'available_analysis': {
                    'strategy': state.get('negotiation_result', {}).get('negotiation_strategy', ''),
                    'script': state.get('negotiation_result', {}).get('script', ''),
                    'potential_savings': state.get('negotiation_result', {}).get('target_savings', {})
                },
                'recommendations': [
                    'Review AI-generated strategy and script',
                    'Conduct manual analysis of bill details',
                    'Research additional negotiation angles',
                    'Execute negotiation with human expertise',
                    'Use AI analysis as supporting information'
                ],
                'next_steps': [
                    'Human review of all analysis',
                    'Manual negotiation execution',
                    'Optional use of AI-generated talking points',
                    'Human-driven strategy adjustments'
                ]
            }
            
            return state
        
        def finalize_processing(state: NegotiationState) -> NegotiationState:
            """Finalize processing and prepare results"""
            logger.info("Finalizing negotiation processing")
            
            state['processing_status'] = 'complete'
            state['final_result'] = {
                'bill_type': state.get('agent_decision', 'Unknown'),
                'confidence_score': state.get('confidence_score', 0.0),
                'execution_mode': state.get('execution_mode', 'unknown'),
                'company': state.get('bill_data', {}).get('company', 'Unknown'),
                'amount': state.get('bill_data', {}).get('amount', 0.0),
                'negotiation_strategy': state.get('negotiation_result', {}).get('negotiation_strategy', ''),
                'negotiation_script': state.get('negotiation_result', {}).get('script', ''),
                'target_savings': state.get('negotiation_result', {}).get('target_savings', {}),
                'execution_instructions': state.get('execution_instructions', {}),
                'processing_errors': state.get('error_messages', [])
            }
            
            return state
        
        # Add nodes to workflow
        workflow.add_node("route", route_negotiation)
        workflow.add_node("execute", execute_specialist_agent)
        workflow.add_node("evaluate", lambda state: evaluate_confidence(state))
        workflow.add_node("auto_execute", auto_execute_negotiation)
        workflow.add_node("supervised", supervised_execution)
        workflow.add_node("human_handoff", human_handoff)
        workflow.add_node("finalize", finalize_processing)
        
        # Add edges
        workflow.add_edge("route", "execute")
        workflow.add_edge("execute", "evaluate")
        
        # Conditional routing based on confidence evaluation
        workflow.add_conditional_edges(
            "evaluate",
            evaluate_confidence,
            {
                "auto_execute": "auto_execute",
                "supervised": "supervised", 
                "human_handoff": "human_handoff"
            }
        )
        
        # All execution modes lead to finalization
        workflow.add_edge("auto_execute", "finalize")
        workflow.add_edge("supervised", "finalize")
        workflow.add_edge("human_handoff", "finalize")
        workflow.add_edge("finalize", END)
        
        workflow.set_entry_point("route")
        
        self.workflow = workflow.compile()
        return self.workflow
    
    def process_bill(self, bill_data: Dict[str, Any], user_id: str = None) -> Dict[str, Any]:
        """Process a bill through the complete negotiation workflow"""
        if not self.workflow:
            self.create_master_orchestrator()
        
        # Create initial state
        initial_state = NegotiationState(
            bill_data=bill_data,
            messages=[],
            user_id=user_id or 'anonymous'
        )
        
        try:
            # Execute the workflow
            result = self.workflow.invoke(initial_state)
            logger.info("Bill processing completed successfully")
            return result.get('final_result', {})
            
        except Exception as e:
            logger.error(f"Error processing bill: {str(e)}")
            return {
                'error': str(e),
                'processing_status': 'failed',
                'confidence_score': 0.0,
                'execution_mode': 'error'
            }

def create_master_orchestrator():
    """Factory function to create master orchestrator"""
    orchestrator = MasterOrchestrator()
    return orchestrator.create_master_orchestrator()

def calculate_confidence(negotiation_result: Dict[str, Any]) -> float:
    """Calculate confidence score for negotiation result"""
    # This function can be enhanced with more sophisticated confidence calculation
    base_confidence = negotiation_result.get('confidence_score', 0.5)
    
    # Adjust based on various factors
    adjustments = 0.0
    
    # Check for strategy quality indicators
    strategy = negotiation_result.get('negotiation_strategy', '').lower()
    if 'competitor' in strategy:
        adjustments += 0.05
    if 'error' in strategy or 'discount' in strategy:
        adjustments += 0.05
    if 'loyalty' in strategy:
        adjustments += 0.03
    
    # Check for script quality
    script = negotiation_result.get('script', '').lower()
    if len(script) > 500:  # Detailed script
        adjustments += 0.02
    
    final_confidence = min(base_confidence + adjustments, 0.95)
    return round(final_confidence, 3)

if __name__ == "__main__":
    # Test the master orchestrator
    orchestrator = MasterOrchestrator()
    workflow = orchestrator.create_master_orchestrator()
    
    test_bill_data = {
        'text': 'ELECTRIC BILL\nCITY POWER COMPANY\nAccount: 123456789\nAmount Due: $124.58',
        'user_id': 'test_user'
    }
    
    result = orchestrator.process_bill(test_bill_data)
    print(f"Processing Status: {result.get('processing_status', 'Unknown')}")
    print(f"Bill Type: {result.get('bill_type', 'Unknown')}")
    print(f"Confidence Score: {result.get('confidence_score', 0)}")
    print(f"Execution Mode: {result.get('execution_mode', 'Unknown')}")
    print(f"Target Savings: {result.get('target_savings', {})}")

