#!/usr/bin/env python3
"""
Hagglz Agent - LangGraph Platform Deployment Script

This script handles the deployment of the Hagglz negotiation agent system
to LangGraph Platform with proper configuration and validation.
"""

import os
import sys
import json
import subprocess
import argparse
import logging
from pathlib import Path
from typing import Dict, Any, Optional

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class LangGraphDeployer:
    """Handles deployment to LangGraph Platform"""
    
    def __init__(self, project_path: str = "."):
        self.project_path = Path(project_path).resolve()
        self.config_file = self.project_path / "langgraph.yaml"
        
    def validate_environment(self) -> bool:
        """Validate that all required environment variables are set"""
        logger.info("Validating environment variables...")
        
        required_vars = [
            'OPENAI_API_KEY',
            'ANTHROPIC_API_KEY'
        ]
        
        optional_vars = [
            'LANGCHAIN_API_KEY',
            'LANGCHAIN_TRACING_V2',
            'LANGCHAIN_PROJECT'
        ]
        
        missing_required = []
        for var in required_vars:
            if not os.getenv(var):
                missing_required.append(var)
        
        if missing_required:
            logger.error(f"Missing required environment variables: {missing_required}")
            logger.error("Please set these variables before deployment:")
            for var in missing_required:
                logger.error(f"  export {var}=your_api_key_here")
            return False
        
        logger.info("✅ All required environment variables are set")
        
        # Check optional variables
        for var in optional_vars:
            if os.getenv(var):
                logger.info(f"✅ Optional variable {var} is set")
            else:
                logger.info(f"ℹ️  Optional variable {var} is not set")
        
        return True
    
    def validate_configuration(self) -> bool:
        """Validate the langgraph.yaml configuration file"""
        logger.info("Validating LangGraph configuration...")
        
        if not self.config_file.exists():
            logger.error(f"Configuration file not found: {self.config_file}")
            return False
        
        try:
            import yaml
            with open(self.config_file, 'r') as f:
                config = yaml.safe_load(f)
            
            # Validate required sections
            required_sections = ['name', 'graphs', 'api', 'env_vars']
            for section in required_sections:
                if section not in config:
                    logger.error(f"Missing required section in config: {section}")
                    return False
            
            logger.info("✅ Configuration file is valid")
            return True
            
        except Exception as e:
            logger.error(f"Error validating configuration: {str(e)}")
            return False
    
    def validate_dependencies(self) -> bool:
        """Validate that all dependencies are properly specified"""
        logger.info("Validating dependencies...")
        
        requirements_file = self.project_path / "requirements.txt"
        if not requirements_file.exists():
            logger.error("requirements.txt file not found")
            return False
        
        try:
            with open(requirements_file, 'r') as f:
                requirements = f.read()
            
            # Check for essential dependencies
            essential_deps = [
                'langchain',
                'langgraph',
                'fastapi',
                'uvicorn',
                'pydantic'
            ]
            
            missing_deps = []
            for dep in essential_deps:
                if dep not in requirements:
                    missing_deps.append(dep)
            
            if missing_deps:
                logger.error(f"Missing essential dependencies: {missing_deps}")
                return False
            
            logger.info("✅ All essential dependencies are specified")
            return True
            
        except Exception as e:
            logger.error(f"Error validating dependencies: {str(e)}")
            return False
    
    def run_tests(self) -> bool:
        """Run tests before deployment"""
        logger.info("Running pre-deployment tests...")
        
        try:
            # Run the simple API test
            test_script = self.project_path / "test_api_simple.py"
            if test_script.exists():
                result = subprocess.run([
                    sys.executable, str(test_script)
                ], capture_output=True, text=True, cwd=self.project_path)
                
                if result.returncode == 0:
                    logger.info("✅ Pre-deployment tests passed")
                    return True
                else:
                    logger.error("❌ Pre-deployment tests failed")
                    logger.error(f"Test output: {result.stdout}")
                    logger.error(f"Test errors: {result.stderr}")
                    return False
            else:
                logger.warning("No test script found, skipping tests")
                return True
                
        except Exception as e:
            logger.error(f"Error running tests: {str(e)}")
            return False
    
    def build_docker_image(self) -> bool:
        """Build Docker image for deployment"""
        logger.info("Building Docker image...")
        
        try:
            dockerfile = self.project_path / "Dockerfile"
            if not dockerfile.exists():
                logger.error("Dockerfile not found")
                return False
            
            # Build the image
            cmd = [
                "docker", "build",
                "-t", "hagglz-negotiation-agent:latest",
                "-f", str(dockerfile),
                str(self.project_path)
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                logger.info("✅ Docker image built successfully")
                return True
            else:
                logger.error("❌ Docker image build failed")
                logger.error(f"Build output: {result.stdout}")
                logger.error(f"Build errors: {result.stderr}")
                return False
                
        except Exception as e:
            logger.error(f"Error building Docker image: {str(e)}")
            return False
    
    def deploy_to_langgraph(self, deployment_name: Optional[str] = None) -> bool:
        """Deploy to LangGraph Platform"""
        logger.info("Deploying to LangGraph Platform...")
        
        try:
            # Prepare deployment command
            cmd = ["langgraph", "deploy"]
            
            if deployment_name:
                cmd.extend(["--name", deployment_name])
            
            # Add configuration file
            cmd.extend(["--config", str(self.config_file)])
            
            # Add project path
            cmd.append(str(self.project_path))
            
            logger.info(f"Running deployment command: {' '.join(cmd)}")
            
            # Execute deployment
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                logger.info("✅ Deployment to LangGraph Platform successful")
                logger.info(f"Deployment output: {result.stdout}")
                return True
            else:
                logger.error("❌ Deployment to LangGraph Platform failed")
                logger.error(f"Deployment output: {result.stdout}")
                logger.error(f"Deployment errors: {result.stderr}")
                return False
                
        except FileNotFoundError:
            logger.error("LangGraph CLI not found. Please install it first:")
            logger.error("  pip install langgraph-cli")
            return False
        except Exception as e:
            logger.error(f"Error during deployment: {str(e)}")
            return False
    
    def create_env_file(self) -> bool:
        """Create .env file template for deployment"""
        logger.info("Creating environment file template...")
        
        env_file = self.project_path / ".env.production"
        
        env_template = """# Hagglz Negotiation Agent - Production Environment Variables
# Copy this file to .env and fill in your actual API keys

# Required API Keys
OPENAI_API_KEY=your_openai_api_key_here
ANTHROPIC_API_KEY=your_anthropic_api_key_here

# Optional LangChain Configuration
LANGCHAIN_API_KEY=your_langsmith_api_key_here
LANGCHAIN_TRACING_V2=true
LANGCHAIN_PROJECT=hagglz-production

# Application Configuration
ENVIRONMENT=production
LOG_LEVEL=INFO
DEBUG=false

# Database Configuration
CHROMA_DB_PATH=/app/data/chroma_db

# Security Configuration
SECRET_KEY=your_secret_key_here
CORS_ORIGINS=https://yourdomain.com

# Monitoring Configuration
ENABLE_METRICS=true
METRICS_PORT=9090
"""
        
        try:
            with open(env_file, 'w') as f:
                f.write(env_template)
            
            logger.info(f"✅ Environment template created: {env_file}")
            logger.info("Please copy this file to .env and fill in your actual API keys")
            return True
            
        except Exception as e:
            logger.error(f"Error creating environment file: {str(e)}")
            return False
    
    def full_deployment(self, deployment_name: Optional[str] = None, 
                       skip_tests: bool = False, skip_docker: bool = False) -> bool:
        """Run the complete deployment process"""
        logger.info("Starting full deployment process...")
        
        steps = [
            ("Environment Validation", self.validate_environment),
            ("Configuration Validation", self.validate_configuration),
            ("Dependencies Validation", self.validate_dependencies),
        ]
        
        if not skip_tests:
            steps.append(("Pre-deployment Tests", self.run_tests))
        
        if not skip_docker:
            steps.append(("Docker Image Build", self.build_docker_image))
        
        steps.append(("LangGraph Deployment", lambda: self.deploy_to_langgraph(deployment_name)))
        
        # Execute all steps
        for step_name, step_func in steps:
            logger.info(f"\n{'='*50}")
            logger.info(f"Step: {step_name}")
            logger.info(f"{'='*50}")
            
            if not step_func():
                logger.error(f"❌ Deployment failed at step: {step_name}")
                return False
        
        logger.info(f"\n{'='*50}")
        logger.info("🎉 DEPLOYMENT SUCCESSFUL!")
        logger.info(f"{'='*50}")
        logger.info("Your Hagglz Negotiation Agent is now deployed to LangGraph Platform")
        
        return True

def main():
    """Main deployment function"""
    parser = argparse.ArgumentParser(description="Deploy Hagglz Agent to LangGraph Platform")
    parser.add_argument("--name", help="Deployment name")
    parser.add_argument("--skip-tests", action="store_true", help="Skip pre-deployment tests")
    parser.add_argument("--skip-docker", action="store_true", help="Skip Docker image build")
    parser.add_argument("--create-env", action="store_true", help="Create environment file template")
    parser.add_argument("--validate-only", action="store_true", help="Only run validation steps")
    parser.add_argument("--project-path", default=".", help="Path to project directory")
    
    args = parser.parse_args()
    
    # Initialize deployer
    deployer = LangGraphDeployer(args.project_path)
    
    # Create environment file if requested
    if args.create_env:
        deployer.create_env_file()
        return
    
    # Run validation only if requested
    if args.validate_only:
        success = (
            deployer.validate_environment() and
            deployer.validate_configuration() and
            deployer.validate_dependencies()
        )
        sys.exit(0 if success else 1)
    
    # Run full deployment
    success = deployer.full_deployment(
        deployment_name=args.name,
        skip_tests=args.skip_tests,
        skip_docker=args.skip_docker
    )
    
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()

