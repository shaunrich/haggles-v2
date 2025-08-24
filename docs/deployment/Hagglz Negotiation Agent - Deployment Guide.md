# Hagglz Negotiation Agent - Deployment Guide

This guide provides comprehensive instructions for deploying the Hagglz AI negotiation agent system to LangGraph Platform.

## Prerequisites

### 1. Required API Keys

Before deployment, ensure you have the following API keys:

- **OpenAI API Key**: Required for GPT models used in utility, subscription, and telecom agents
- **Anthropic API Key**: Required for Claude models used in medical bill negotiations
- **LangSmith API Key** (Optional): For monitoring and tracing

### 2. Required Software

- Python 3.11+
- Docker (for containerised deployment)
- LangGraph CLI (`pip install langgraph-cli`)
- Git (for version control)

## Quick Start Deployment

### 1. Environment Setup

First, set your API keys as environment variables:

```bash
export OPENAI_API_KEY="your_openai_api_key_here"
export ANTHROPIC_API_KEY="your_anthropic_api_key_here"
export LANGCHAIN_API_KEY="your_langsmith_api_key_here"  # Optional
export LANGCHAIN_TRACING_V2="true"  # Optional
export LANGCHAIN_PROJECT="hagglz-production"  # Optional
```

### 2. Create Environment File

Generate an environment file template:

```bash
python deploy.py --create-env
```

This creates `.env.production` with all required variables. Copy it to `.env` and fill in your actual API keys.

### 3. Validate Configuration

Before deployment, validate your setup:

```bash
python deploy.py --validate-only
```

### 4. Deploy to LangGraph Platform

Run the full deployment process:

```bash
python deploy.py --name hagglz-production
```

## Deployment Options

### Standard Deployment

```bash
# Full deployment with all validation steps
python deploy.py --name my-hagglz-deployment
```

### Skip Tests (Faster Deployment)

```bash
# Skip pre-deployment tests for faster deployment
python deploy.py --name my-hagglz-deployment --skip-tests
```

### Skip Docker Build

```bash
# Skip Docker image build if already built
python deploy.py --name my-hagglz-deployment --skip-docker
```

### Validation Only

```bash
# Only run validation without deploying
python deploy.py --validate-only
```

## Local Development Setup

### Using Docker Compose

For local development and testing:

```bash
# Create data directories
mkdir -p data logs

# Start all services
docker-compose up -d

# View logs
docker-compose logs -f hagglz-agent

# Stop services
docker-compose down
```

### Direct Python Execution

For development without Docker:

```bash
# Install dependencies
pip install -r requirements.txt

# Start the API server
python run_api.py
```

## Configuration Files

### langgraph.yaml

The main configuration file for LangGraph Platform deployment. Key sections:

- **graphs**: Defines all agent workflows
- **api**: FastAPI application configuration
- **env_vars**: Required environment variables
- **resources**: Memory and CPU allocation
- **scaling**: Auto-scaling configuration

### Dockerfile

Multi-stage Docker build for optimised production deployment:

- **Builder stage**: Installs dependencies
- **Production stage**: Minimal runtime image
- **Security**: Non-root user execution
- **Health checks**: Built-in health monitoring

### docker-compose.yml

Local development environment with:

- **Main application**: Hagglz agent system
- **Redis**: Caching and session management
- **Nginx**: Reverse proxy (optional)
- **Persistent volumes**: Data and logs

## Environment Variables

### Required Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `OPENAI_API_KEY` | OpenAI API key for GPT models | `sk-...` |
| `ANTHROPIC_API_KEY` | Anthropic API key for Claude models | `sk-ant-...` |

### Optional Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `LANGCHAIN_API_KEY` | LangSmith API key for tracing | None |
| `LANGCHAIN_TRACING_V2` | Enable LangSmith tracing | `false` |
| `LANGCHAIN_PROJECT` | LangSmith project name | `hagglz-development` |
| `LOG_LEVEL` | Logging level | `INFO` |
| `DEBUG` | Debug mode | `false` |

## Monitoring and Health Checks

### Health Check Endpoint

The system provides a health check endpoint at `/health`:

```bash
curl http://your-deployment-url/health
```

Response:
```json
{
  "status": "healthy",
  "timestamp": "2024-01-01T12:00:00Z",
  "version": "1.0.0",
  "components": {
    "orchestrator": "active",
    "memory_system": "active",
    "negotiation_tools": "active"
  }
}
```

### API Documentation

Once deployed, access the interactive API documentation:

- **Swagger UI**: `http://your-deployment-url/docs`
- **ReDoc**: `http://your-deployment-url/redoc`
- **OpenAPI JSON**: `http://your-deployment-url/openapi.json`

## Troubleshooting

### Common Issues

1. **Missing API Keys**
   ```
   Error: Missing required environment variables: ['OPENAI_API_KEY']
   ```
   Solution: Set all required environment variables before deployment.

2. **Docker Build Failures**
   ```
   Error: Docker image build failed
   ```
   Solution: Ensure Docker is running and you have sufficient disk space.

3. **LangGraph CLI Not Found**
   ```
   Error: LangGraph CLI not found
   ```
   Solution: Install the LangGraph CLI: `pip install langgraph-cli`

4. **Configuration Validation Errors**
   ```
   Error: Missing required section in config: graphs
   ```
   Solution: Ensure `langgraph.yaml` is properly formatted and complete.

### Debugging Steps

1. **Validate Environment**:
   ```bash
   python deploy.py --validate-only
   ```

2. **Check Logs**:
   ```bash
   # Docker Compose
   docker-compose logs -f hagglz-agent
   
   # Direct execution
   python run_api.py
   ```

3. **Test API Locally**:
   ```bash
   python test_api_simple.py
   ```

4. **Verify Dependencies**:
   ```bash
   pip check
   ```

## Scaling and Performance

### Resource Configuration

The default configuration allocates:
- **Memory**: 2Gi limit, 1Gi reservation
- **CPU**: 1000m limit, 500m reservation
- **Scaling**: 1-5 instances based on CPU utilisation

### Performance Optimisation

1. **Increase Resources**: Modify `langgraph.yaml` resource limits
2. **Enable Caching**: Use Redis for response caching
3. **Load Balancing**: Deploy multiple instances
4. **Database Optimisation**: Tune ChromaDB settings

## Security Considerations

### API Security

- **CORS**: Configured for cross-origin requests
- **Rate Limiting**: Implement rate limiting for production
- **Authentication**: Add API key authentication for production use
- **HTTPS**: Use HTTPS in production environments

### Container Security

- **Non-root User**: Application runs as non-root user
- **Minimal Image**: Production image includes only necessary components
- **Security Scanning**: Regularly scan images for vulnerabilities

## Support and Maintenance

### Regular Maintenance

1. **Update Dependencies**: Regularly update Python packages
2. **Monitor Performance**: Track API response times and error rates
3. **Backup Data**: Regular backups of vector database
4. **Security Updates**: Keep base images and dependencies updated

### Getting Help

For deployment issues or questions:

1. Check this deployment guide
2. Review the troubleshooting section
3. Check application logs
4. Validate configuration files
5. Test with minimal configuration

## Version History

- **v1.0.0**: Initial release with full agent system
  - Master orchestrator with routing
  - Specialised agents for different bill types
  - Vector-based memory system
  - Comprehensive API with documentation
  - Docker containerisation
  - LangGraph Platform deployment configuration

