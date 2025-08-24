"""
Hagglz AI Negotiation Agent

AI-powered bill negotiation system with specialised agents for different bill types.
"""

__version__ = "2.0.0"
__author__ = "Hagglz Team"
__description__ = "AI-powered bill negotiation system with specialised agents"

from hagglz.core.orchestrator import MasterOrchestrator
from hagglz.core.router_agent import RouterAgent

__all__ = [
    "MasterOrchestrator",
    "RouterAgent",
    "__version__",
    "__author__",
    "__description__"
]
