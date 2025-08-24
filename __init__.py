"""
Memory Module for Hagglz Agent

This module provides vector-based memory capabilities for storing and retrieving
negotiation strategies, successful outcomes, and company intelligence.
"""

from .vector_store import NegotiationMemory, create_negotiation_memory

__all__ = ['NegotiationMemory', 'create_negotiation_memory']

