"""
Hagglz Agents Package

Specialised negotiation agents for different bill types.
"""

from hagglz.agents.utility_agent import UtilityNegotiationAgent
from hagglz.agents.medical_agent import MedicalNegotiationAgent
from hagglz.agents.subscription_agent import SubscriptionNegotiationAgent
from hagglz.agents.telecom_agent import TelecomNegotiationAgent

__all__ = [
    "UtilityNegotiationAgent",
    "MedicalNegotiationAgent",
    "SubscriptionNegotiationAgent",
    "TelecomNegotiationAgent"
]
