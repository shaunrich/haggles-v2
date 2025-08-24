# LangGraph Platform Deployment Guide

## 🚀 **Deploying Hagglz to LangGraph Platform**

This guide covers deploying the Hagglz AI Negotiation Agent to LangGraph Platform for automatic deployment from your GitHub repository.

## 📋 **Prerequisites**

### **1. LangGraph Platform Access**
- ✅ LangGraph Platform account (Cloud SaaS)
- ✅ Valid license key (if using Enterprise features)
- ✅ GitHub repository connected

### **2. Repository Requirements**
- ✅ Clean folder structure (completed)
- ✅ `langgraph.json` configuration file (completed)
- ✅ All import paths updated (completed)
- ✅ Environment variables documented

### **3. Required Environment Variables**
```bash
# Required for deployment
OPENAI_API_KEY=your_openai_api_key_here
ANTHROPIC_API_KEY=your_anthropic_api_key_here

# Optional for enhanced functionality
LANGCHAIN_API_KEY=your_langsmith_api_key_here
LANGCHAIN_TRACING_V2=true
LANGCHAIN_PROJECT=hagglz-production
```

## 🔧 **Configuration Files**

### **⚠️ Important: Package Configuration Fix**
The repository name `haggles-v2` contains a hyphen, which causes deployment issues with LangGraph Platform. This has been resolved by adding proper Python package configuration files:

- **`pyproject.toml`**: Modern Python packaging configuration
- **`setup.py`**: Traditional Python packaging configuration
- **`langgraph.json`**: Updated with Wolfi Linux distribution for security

These files make the project a proper Python package, allowing LangGraph Platform to deploy successfully.

### **1. langgraph.json (Root Directory)**
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

**Note**: The `image_distro: "wolfi"` setting enables enhanced security with Wolfi Linux distribution.

### **2. requirements.txt (Root Directory)**
```txt
# Core LangChain and LangGraph dependencies
langchain>=0.1.0
langgraph>=0.1.0
langchain-openai>=0.1.0
langchain-anthropic>=0.1.0
langchain-community>=0.1.0

# FastAPI and web framework
fastapi>=0.104.0
uvicorn[standard]>=0.24.0
python-multipart>=0.0.6

# Data validation and serialization
pydantic>=2.0.0
pydantic-settings>=2.0.0

# Vector database and embeddings
chromadb>=0.4.0
openai>=1.0.0

# Environment and configuration
python-dotenv>=1.0.0
pyyaml>=6.0
```

## 🌐 **LangGraph Platform Setup**

### **1. Connect GitHub Repository**
1. **Access LangGraph Platform**: Navigate to your LangGraph Platform dashboard
2. **Create New Deployment**: Click "New Deployment" or "Connect Repository"
3. **Select GitHub**: Choose GitHub as your source
4. **Repository Selection**: Select `shaunrich/haggles-v2`
5. **Branch Selection**: Choose `main` branch

### **2. Configure Deployment Settings**
```yaml
# Deployment Configuration
Name: hagglz-negotiation-agent
Type: Production  # or Development for testing
Build on Push: true  # Automatic deployment on commits
Custom URL: (optional) your-custom-domain.com

# Resource Configuration
CPU: 2 (Production) or 1 (Development)
Memory: 2GB (Production) or 1GB (Development)
Scaling: Up to 10 containers (Production) or 1 (Development)
```

### **3. Environment Variables Setup**
In the LangGraph Platform dashboard:
1. **Navigate to Secrets**: Go to your deployment's secrets section
2. **Add Required Secrets**:
   ```
   OPENAI_API_KEY: your_actual_openai_key
   ANTHROPIC_API_KEY: your_actual_anthropic_key
   ```
3. **Add Optional Secrets**:
   ```
   LANGCHAIN_API_KEY: your_langsmith_key
   LANGCHAIN_TRACING_V2: true
   LANGCHAIN_PROJECT: hagglz-production
   ```

## 🚀 **Deployment Process**

### **1. Initial Deployment**
1. **Repository Connection**: Platform connects to your GitHub repo
2. **Configuration Detection**: Platform reads `langgraph.json`
3. **Dependency Installation**: Platform installs from `requirements.txt`
4. **Graph Compilation**: Platform compiles all defined graphs
5. **API Server Build**: Platform builds the FastAPI server
6. **Health Check**: Platform verifies deployment health
7. **Deployment Complete**: Your agent is now live!

### **2. Automatic Deployments**
- **Build on Push**: Every commit to `main` triggers automatic rebuild
- **Rolling Updates**: Zero-downtime deployments
- **Health Monitoring**: Automatic rollback on failures

## 📊 **Deployment Types**

### **Development Deployment**
```yaml
Type: Development
Resources: 1 CPU, 1GB RAM
Scaling: Up to 1 container
Database: 10GB disk, no backups
Cost: Lower (preemptible infrastructure)
Use Case: Testing, development, internal use
```

### **Production Deployment**
```yaml
Type: Production
Resources: 2 CPU, 2GB RAM
Scaling: Up to 10 containers
Database: Autoscaling disk, automatic backups
Cost: Higher (durable infrastructure)
Use Case: Customer-facing applications
```

## 🔍 **Post-Deployment Verification**

### **1. Health Check Endpoints**
```bash
# Basic health check
curl https://your-deployment-url/ok

# API documentation
curl https://your-deployment-url/docs

# Health status
curl https://your-deployment-url/health
```

### **2. Graph Verification**
```bash
# Test master orchestrator
curl -X POST https://your-deployment-url/runs \
  -H "Content-Type: application/json" \
  -H "X-Api-Key: your_langsmith_key" \
  -d '{"graph": "master_orchestrator", "input": {"bill_data": {"text": "TEST BILL"}}}'
```

### **3. API Endpoint Testing**
```bash
# Test health endpoint
curl https://your-deployment-url/health

# Test negotiation endpoint
curl -X POST https://your-deployment-url/negotiate \
  -H "Content-Type: application/json" \
  -d '{"bill_text": "ELECTRIC BILL", "user_id": "test"}'
```

## 🛠️ **Troubleshooting**

### **Common Issues**

#### **1. Package Name Hyphen Error**
```bash
# ❌ Error: Package name 'haggles-v2' contains a hyphen
ValueError: Package name 'haggles-v2' contains a hyphen. 
Rename the directory to use it as flat-layout package.

# ✅ Solution: Added proper Python package configuration
# - pyproject.toml (modern packaging)
# - setup.py (traditional packaging)
# - langgraph.json with image_distro: "wolfi"
```

#### **2. Import Path Errors**
```python
# ❌ Old import style
from agents.utility_agent import UtilityNegotiationAgent

# ✅ New import style
from ..agents.utility_agent import UtilityNegotiationAgent
```

#### **2. Configuration File Issues**
```json
# ❌ Missing required fields
{
  "graphs": {}
}

# ✅ Complete configuration
{
  "dependencies": ["."],
  "graphs": {
    "master_orchestrator": "./src/hagglz/core/orchestrator.py:MasterOrchestrator"
  },
  "http": {
    "app": "./src/hagglz/api/main.py:app"
  }
}
```

#### **3. Environment Variable Issues**
```bash
# ❌ Missing required variables
OPENAI_API_KEY=  # Empty value

# ✅ Properly set variables
OPENAI_API_KEY=sk-your-actual-key-here
```

### **Debugging Steps**
1. **Check Build Logs**: Review deployment build logs in platform
2. **Verify Configuration**: Ensure `langgraph.json` is valid JSON
3. **Test Locally**: Run `langgraph dev` to test locally first
4. **Check Dependencies**: Verify all packages in `requirements.txt`
5. **Import Validation**: Ensure all import paths are correct

## 📈 **Monitoring & Scaling**

### **1. Performance Metrics**
- **Request Count**: Total API requests
- **Response Time**: Average response latency
- **Error Rate**: Percentage of failed requests
- **Resource Usage**: CPU and memory utilization

### **2. Scaling Configuration**
```yaml
# Automatic scaling
Min Instances: 1
Max Instances: 10 (Production) or 1 (Development)
Target CPU: 70%
Scaling Policy: Horizontal Pod Autoscaler
```

### **3. Health Monitoring**
- **Liveness Probe**: `/ok` endpoint
- **Readiness Probe**: `/health` endpoint
- **Metrics Endpoint**: `/metrics` (Prometheus format)
- **Documentation**: `/docs` (Swagger UI)

## 🔒 **Security Considerations**

### **1. API Key Management**
- ✅ Store API keys as platform secrets
- ✅ Never commit keys to repository
- ✅ Rotate keys regularly
- ✅ Use least-privilege access

### **2. Network Security**
- **HTTPS Only**: All endpoints use TLS encryption
- **CORS Configuration**: Configure allowed origins
- **Rate Limiting**: Implement request throttling
- **Authentication**: Use LangSmith API keys

### **3. Data Privacy**
- **Vector Database**: ChromaDB data stays in your deployment
- **No Data Sharing**: LangChain doesn't access your data
- **Compliance**: Meets enterprise security requirements

## 📞 **Support & Resources**

### **1. LangGraph Platform Support**
- **Documentation**: [LangGraph Platform Docs](https://langchain-ai.github.io/langgraph/)
- **Community**: [LangChain Discord](https://discord.gg/langchain)
- **Support**: support@langchain.dev

### **2. Deployment Status**
- **Platform Dashboard**: Monitor deployment health
- **Build Logs**: Review deployment process
- **Metrics**: Track performance and usage
- **Alerts**: Configure notification thresholds

## 🎯 **Next Steps After Deployment**

1. **Test All Endpoints**: Verify all API endpoints work correctly
2. **Monitor Performance**: Watch response times and error rates
3. **Set Up Alerts**: Configure monitoring and alerting
4. **Scale as Needed**: Adjust resources based on usage
5. **Iterate & Improve**: Collect feedback and enhance the system

---

**🎉 Congratulations! Your Hagglz AI Negotiation Agent is now deployed on LangGraph Platform!**

The system will automatically deploy updates whenever you push to the `main` branch, providing a seamless CI/CD pipeline for your AI agents.
