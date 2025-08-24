"""
Vector Store for Negotiation Memory

This module implements the vector-based memory system for storing and retrieving
successful negotiation strategies and historical data.
"""

from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from typing import Dict, Any, List, Optional
import logging
import os
import json
from datetime import datetime

logger = logging.getLogger(__name__)

class NegotiationMemory:
    """Vector-based memory system for negotiation strategies"""
    
    def __init__(self, persist_directory: str = "./chroma_db"):
        """Initialize the negotiation memory system"""
        self.persist_directory = persist_directory
        self.embeddings = OpenAIEmbeddings()
        
        # Ensure the persist directory exists
        os.makedirs(persist_directory, exist_ok=True)
        
        # Initialize vector stores for different types of data
        self.strategy_store = Chroma(
            collection_name="negotiation_strategies",
            embedding_function=self.embeddings,
            persist_directory=os.path.join(persist_directory, "strategies")
        )
        
        self.success_store = Chroma(
            collection_name="successful_negotiations",
            embedding_function=self.embeddings,
            persist_directory=os.path.join(persist_directory, "successes")
        )
        
        self.company_store = Chroma(
            collection_name="company_profiles",
            embedding_function=self.embeddings,
            persist_directory=os.path.join(persist_directory, "companies")
        )
        
        logger.info("Negotiation memory system initialized")
    
    def store_negotiation_strategy(self, strategy_data: Dict[str, Any]) -> str:
        """Store a negotiation strategy in the vector store"""
        try:
            # Create a comprehensive text representation
            strategy_text = self._create_strategy_text(strategy_data)
            
            # Create metadata
            metadata = {
                'company': strategy_data.get('company', 'Unknown'),
                'bill_type': strategy_data.get('bill_type', 'Unknown'),
                'amount': strategy_data.get('amount', 0.0),
                'confidence_score': strategy_data.get('confidence_score', 0.0),
                'timestamp': datetime.now().isoformat(),
                'strategy_type': strategy_data.get('strategy_type', 'general')
            }
            
            # Store in vector database
            doc_ids = self.strategy_store.add_texts(
                texts=[strategy_text],
                metadatas=[metadata]
            )
            
            logger.info(f"Stored negotiation strategy for {metadata['company']}")
            return doc_ids[0] if doc_ids else None
            
        except Exception as e:
            logger.error(f"Error storing negotiation strategy: {str(e)}")
            return None
    
    def store_successful_negotiation(self, success_data: Dict[str, Any]) -> str:
        """Store a successful negotiation outcome"""
        try:
            # Create text representation of the success
            success_text = self._create_success_text(success_data)
            
            # Create metadata
            metadata = {
                'company': success_data.get('company', 'Unknown'),
                'bill_type': success_data.get('bill_type', 'Unknown'),
                'original_amount': success_data.get('original_amount', 0.0),
                'final_amount': success_data.get('final_amount', 0.0),
                'savings_amount': success_data.get('savings_amount', 0.0),
                'savings_percentage': success_data.get('savings_percentage', 0.0),
                'negotiation_duration': success_data.get('negotiation_duration', 0),
                'success_factors': json.dumps(success_data.get('success_factors', [])),
                'timestamp': datetime.now().isoformat()
            }
            
            # Store in vector database
            doc_ids = self.success_store.add_texts(
                texts=[success_text],
                metadatas=[metadata]
            )
            
            logger.info(f"Stored successful negotiation: {metadata['savings_percentage']}% savings")
            return doc_ids[0] if doc_ids else None
            
        except Exception as e:
            logger.error(f"Error storing successful negotiation: {str(e)}")
            return None
    
    def store_company_profile(self, company_data: Dict[str, Any]) -> str:
        """Store company-specific negotiation intelligence"""
        try:
            # Create text representation
            company_text = self._create_company_text(company_data)
            
            # Create metadata
            metadata = {
                'company_name': company_data.get('company_name', 'Unknown'),
                'industry': company_data.get('industry', 'Unknown'),
                'negotiation_difficulty': company_data.get('negotiation_difficulty', 'medium'),
                'average_savings': company_data.get('average_savings', 0.0),
                'best_approaches': json.dumps(company_data.get('best_approaches', [])),
                'contact_preferences': json.dumps(company_data.get('contact_preferences', {})),
                'timestamp': datetime.now().isoformat()
            }
            
            # Store in vector database
            doc_ids = self.company_store.add_texts(
                texts=[company_text],
                metadatas=[metadata]
            )
            
            logger.info(f"Stored company profile for {metadata['company_name']}")
            return doc_ids[0] if doc_ids else None
            
        except Exception as e:
            logger.error(f"Error storing company profile: {str(e)}")
            return None
    
    def retrieve_similar_strategies(self, query: str, bill_type: str = None, k: int = 5) -> List[Dict[str, Any]]:
        """Retrieve similar negotiation strategies"""
        try:
            # Build search filter
            search_filter = {}
            if bill_type:
                search_filter['bill_type'] = bill_type
            
            # Perform similarity search
            if search_filter:
                results = self.strategy_store.similarity_search(
                    query, k=k, filter=search_filter
                )
            else:
                results = self.strategy_store.similarity_search(query, k=k)
            
            # Format results
            formatted_results = []
            for doc in results:
                formatted_results.append({
                    'content': doc.page_content,
                    'metadata': doc.metadata,
                    'relevance': 'high'  # Could implement scoring
                })
            
            logger.info(f"Retrieved {len(formatted_results)} similar strategies")
            return formatted_results
            
        except Exception as e:
            logger.error(f"Error retrieving similar strategies: {str(e)}")
            return []
    
    def retrieve_successful_negotiations(self, company: str = None, bill_type: str = None, k: int = 5) -> List[Dict[str, Any]]:
        """Retrieve successful negotiations for learning"""
        try:
            # Build query
            query_parts = []
            if company:
                query_parts.append(f"company: {company}")
            if bill_type:
                query_parts.append(f"bill type: {bill_type}")
            
            query = " ".join(query_parts) if query_parts else "successful negotiation"
            
            # Build search filter
            search_filter = {}
            if company:
                search_filter['company'] = company
            if bill_type:
                search_filter['bill_type'] = bill_type
            
            # Perform search
            if search_filter:
                results = self.success_store.similarity_search(
                    query, k=k, filter=search_filter
                )
            else:
                results = self.success_store.similarity_search(query, k=k)
            
            # Format results
            formatted_results = []
            for doc in results:
                formatted_results.append({
                    'content': doc.page_content,
                    'metadata': doc.metadata,
                    'savings_percentage': doc.metadata.get('savings_percentage', 0.0)
                })
            
            logger.info(f"Retrieved {len(formatted_results)} successful negotiations")
            return formatted_results
            
        except Exception as e:
            logger.error(f"Error retrieving successful negotiations: {str(e)}")
            return []
    
    def get_company_intelligence(self, company_name: str) -> Optional[Dict[str, Any]]:
        """Get company-specific negotiation intelligence"""
        try:
            query = f"company profile: {company_name}"
            results = self.company_store.similarity_search(query, k=1)
            
            if results:
                doc = results[0]
                return {
                    'content': doc.page_content,
                    'metadata': doc.metadata,
                    'company_name': doc.metadata.get('company_name', company_name),
                    'best_approaches': json.loads(doc.metadata.get('best_approaches', '[]')),
                    'average_savings': doc.metadata.get('average_savings', 0.0),
                    'negotiation_difficulty': doc.metadata.get('negotiation_difficulty', 'medium')
                }
            
            return None
            
        except Exception as e:
            logger.error(f"Error retrieving company intelligence: {str(e)}")
            return None
    
    def _create_strategy_text(self, strategy_data: Dict[str, Any]) -> str:
        """Create a text representation of a negotiation strategy"""
        parts = [
            f"Negotiation Strategy for {strategy_data.get('company', 'Unknown')}",
            f"Bill Type: {strategy_data.get('bill_type', 'Unknown')}",
            f"Amount: ${strategy_data.get('amount', 0.0)}",
            f"Strategy: {strategy_data.get('strategy', '')}",
            f"Key Points: {strategy_data.get('key_points', '')}",
            f"Expected Outcome: {strategy_data.get('expected_outcome', '')}",
            f"Confidence Score: {strategy_data.get('confidence_score', 0.0)}"
        ]
        return "\n".join(parts)
    
    def _create_success_text(self, success_data: Dict[str, Any]) -> str:
        """Create a text representation of a successful negotiation"""
        parts = [
            f"Successful Negotiation with {success_data.get('company', 'Unknown')}",
            f"Bill Type: {success_data.get('bill_type', 'Unknown')}",
            f"Original Amount: ${success_data.get('original_amount', 0.0)}",
            f"Final Amount: ${success_data.get('final_amount', 0.0)}",
            f"Savings: {success_data.get('savings_percentage', 0.0)}%",
            f"Approach Used: {success_data.get('approach_used', '')}",
            f"Key Success Factors: {', '.join(success_data.get('success_factors', []))}",
            f"Negotiation Notes: {success_data.get('notes', '')}"
        ]
        return "\n".join(parts)
    
    def _create_company_text(self, company_data: Dict[str, Any]) -> str:
        """Create a text representation of company profile"""
        parts = [
            f"Company Profile: {company_data.get('company_name', 'Unknown')}",
            f"Industry: {company_data.get('industry', 'Unknown')}",
            f"Negotiation Difficulty: {company_data.get('negotiation_difficulty', 'medium')}",
            f"Average Savings Achieved: {company_data.get('average_savings', 0.0)}%",
            f"Best Approaches: {', '.join(company_data.get('best_approaches', []))}",
            f"Preferred Contact Methods: {company_data.get('contact_preferences', {})}",
            f"Special Notes: {company_data.get('special_notes', '')}",
            f"Success Rate: {company_data.get('success_rate', 0.0)}%"
        ]
        return "\n".join(parts)
    
    def get_memory_stats(self) -> Dict[str, Any]:
        """Get statistics about the memory system"""
        try:
            # This is a simplified version - ChromaDB doesn't have direct count methods
            # In a production system, you'd implement proper counting
            return {
                'strategies_stored': 'Available',
                'successes_stored': 'Available', 
                'companies_profiled': 'Available',
                'memory_status': 'Active'
            }
        except Exception as e:
            logger.error(f"Error getting memory stats: {str(e)}")
            return {'error': str(e)}

# Factory function
def create_negotiation_memory(persist_directory: str = "./chroma_db") -> NegotiationMemory:
    """Factory function to create negotiation memory system"""
    return NegotiationMemory(persist_directory)

if __name__ == "__main__":
    # Test the memory system
    memory = NegotiationMemory()
    
    # Test storing a strategy
    test_strategy = {
        'company': 'Test Electric Company',
        'bill_type': 'UTILITY',
        'amount': 150.0,
        'strategy': 'Loyalty-based approach with competitor comparison',
        'key_points': 'Long-term customer, competitor offers better rates',
        'confidence_score': 0.8
    }
    
    strategy_id = memory.store_negotiation_strategy(test_strategy)
    print(f"Stored strategy with ID: {strategy_id}")
    
    # Test retrieval
    similar = memory.retrieve_similar_strategies("electric bill negotiation", "UTILITY", k=3)
    print(f"Found {len(similar)} similar strategies")
    
    # Test memory stats
    stats = memory.get_memory_stats()
    print(f"Memory stats: {stats}")

