#!/usr/bin/env python3
"""
Hagglz API Server Startup Script

This script starts the Hagglz negotiation API server with proper configuration.
"""

import os
import sys
import uvicorn
import logging
from pathlib import Path

# Add current directory to Python path
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

def setup_environment():
    """Set up environment variables and configuration"""
    # Set default environment variables if not already set
    env_vars = {
        'OPENAI_API_KEY': 'your-openai-api-key-here',
        'ANTHROPIC_API_KEY': 'your-anthropic-api-key-here',
        'LANGCHAIN_API_KEY': 'your-langsmith-api-key-here',
        'LANGCHAIN_TRACING_V2': 'true',
        'LANGCHAIN_PROJECT': 'hagglz-development'
    }
    
    for key, default_value in env_vars.items():
        if key not in os.environ:
            os.environ[key] = default_value
            logger.info(f"Set default environment variable: {key}")

def main():
    """Main function to start the API server"""
    logger.info("Starting Hagglz Negotiation API Server...")
    
    # Setup environment
    setup_environment()
    
    # Configuration
    config = {
        "app": "api.main:app",
        "host": "0.0.0.0",
        "port": 8000,
        "reload": True,
        "log_level": "info",
        "access_log": True
    }
    
    logger.info(f"Server configuration: {config}")
    logger.info("API will be available at:")
    logger.info("  - Main API: http://localhost:8000")
    logger.info("  - API Docs: http://localhost:8000/docs")
    logger.info("  - ReDoc: http://localhost:8000/redoc")
    logger.info("  - Health Check: http://localhost:8000/health")
    
    try:
        # Start the server
        uvicorn.run(**config)
    except KeyboardInterrupt:
        logger.info("Server shutdown requested by user")
    except Exception as e:
        logger.error(f"Error starting server: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()

