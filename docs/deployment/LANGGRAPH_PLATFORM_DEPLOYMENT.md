# LangGraph Platform Deployment Guide

## Overview
This guide covers deploying the Hagglz AI Negotiation Agent to LangGraph Platform, including configuration, deployment process, and troubleshooting.

## Prerequisites
- LangGraph CLI installed and authenticated
- GitHub repository with proper Python package structure
- Environment variables configured (API keys, etc.)

## Configuration

### 1. langgraph.json
The main configuration file for LangGraph Platform deployment:

```json
{
  "dependencies": ["."],
  "graphs": {
    "master_orchestrator": "./src/hagglz/core/orchestrator.py:MasterOrchestrator",
    "utility_agent": "./src/hagglz/agents/utility_agent.py:UtilityNegotiationAgent",
    "medical_agent": "./src/hagglz/agents/medical_agent.py:MedicalNegotiationAgent",
    "subscription_agent": "./src/hagglz/agents/subscription_agent.py:SubscriptionNegotiationAgent",
    "telecom_agent": "./src/hagglz/agents/telecom_agent.py:TelecomNegotiationAgent"
  },
  "http": {
    "app": "./src/hagglz/api/main.py:app"
  },
  "image_distro": "wolfi"
}
```

### 2. Package Configuration
- **pyproject.toml**: Modern Python packaging configuration
- **setup.py**: Traditional Python packaging alternative
- **Package Name**: `hagglz-negotiation-agent` (no hyphens in package name)

## Deployment Process

### 1. Initial Setup
```bash
# Install LangGraph CLI
pip install langgraph-cli

# Authenticate with LangGraph Platform
langgraph auth login
```

### 2. Deploy to Platform
```bash
# Deploy to LangGraph Cloud
langgraph deploy

# Or specify a specific deployment
langgraph deploy --name hagglz-negotiation-agent
```

## Troubleshooting

### Common Issues and Solutions

#### 1. Package Name Hyphen Error
**Error**: `ValueError: Package name 'haggles-v2' contains a hyphen. Rename the directory to use it as flat-layout package.`

**Solution**: 
- Repository name can contain hyphens (`haggles-v2`)
- Package name in `pyproject.toml` and `setup.py` must NOT contain hyphens (`hagglz-negotiation-agent`)
- Use proper Python package structure with `src/` layout

#### 2. Relative Import Failures
**Error**: `ImportError: attempted relative import with no known parent package`

**Root Cause**: Relative imports (`from ..core.orchestrator import MasterOrchestrator`) fail in containerized environments like LangGraph Platform.

**Solution**: Convert all relative imports to absolute imports:
```python
# ❌ Before (Relative imports - FAILS)
from ..core.orchestrator import MasterOrchestrator
from ..memory.vector_store import NegotiationMemory

# ✅ After (Absolute imports - WORKS)
from hagglz.core.orchestrator import MasterOrchestrator
from hagglz.memory.vector_store import NegotiationMemory
```

**Files Fixed**:
- `src/hagglz/__init__.py`
- `src/hagglz/core/__init__.py`
- `src/hagglz/core/orchestrator.py`
- `src/hagglz/agents/__init__.py`
- `src/hagglz/api/__init__.py`
- `src/hagglz/api/main.py`
- `src/hagglz/memory/__init__.py`
- `src/hagglz/tools/__init__.py`

#### 3. Module Import Path Issues
**Error**: `ImportError: Failed to import app module '/deps/haggles-v2/src/hagglz/api/main.py'`

**Solution**: Ensure all import paths use absolute package references and the package structure is properly defined.

## Verification

### 1. Local Testing
Test imports locally before deployment:
```bash
cd src
python -c "import hagglz; print('Package import successful')"
```

### 2. Deployment Status
Check deployment status in LangGraph Platform dashboard or via CLI:
```bash
langgraph deployments list
```

## Monitoring and Scaling

### 1. Health Checks
- Monitor `/health` endpoint
- Check application logs in LangGraph Platform
- Set up alerts for failed deployments

### 2. Performance
- Monitor response times
- Track resource usage
- Scale based on demand

## Security Considerations

### 1. Environment Variables
- Never commit API keys to repository
- Use LangGraph Platform secrets management
- Secure sensitive configuration

### 2. Container Security
- Use Wolfi Linux (`"image_distro": "wolfi"`)
- Regular security updates
- Access control and authentication

## Best Practices

### 1. Package Structure
- Use `src/` layout for Python packages
- Proper `__init__.py` files in all directories
- Clear separation of concerns

### 2. Import Strategy
- Always use absolute imports for production
- Avoid relative imports in containerized environments
- Test imports locally before deployment

### 3. Configuration Management
- Version control configuration files
- Environment-specific settings
- Documentation of all configuration options

## Support and Resources

- [LangGraph Platform Documentation](https://docs.langchain.com/langgraph-platform/)
- [LangGraph CLI Reference](https://docs.langchain.com/langgraph-platform/deploy/cli)
- [Python Packaging Best Practices](https://packaging.python.org/guides/)
- [Container Deployment Guidelines](https://docs.langchain.com/langgraph-platform/deploy/container)
