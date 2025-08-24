"""
Hagglz Agents Package

Specialised negotiation agents for different bill types.
"""

from .utility_agent import UtilityNegotiationAgent
from .medical_agent import MedicalNegotiationAgent
from .subscription_agent import SubscriptionNegotiationAgent
from .telecom_agent import TelecomNegotiationAgent

__all__ = [
    "UtilityNegotiationAgent",
    "MedicalNegotiationAgent",
    "SubscriptionNegotiationAgent",
    "TelecomNegotiationAgent"
]
