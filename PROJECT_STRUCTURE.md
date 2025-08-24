# Hagglz Project Structure

## 📁 Repository Organization

```
haggles-v2/
├── 📁 src/                           # Source code
│   └── 📁 hagglz/                    # Main package
│       ├── 📁 api/                   # FastAPI application
│       │   ├── __init__.py
│       │   ├── main.py               # Main API application
│       │   └── run_api.py            # API server startup
│       ├── 📁 core/                  # Core system components
│       │   ├── __init__.py
│       │   ├── orchestrator.py       # Master orchestrator
│       │   └── router_agent.py       # Bill classification & routing
│       ├── 📁 agents/                # Specialised negotiation agents
│       │   ├── __init__.py
│       │   ├── utility_agent.py      # Utility bill negotiations
│       │   ├── medical_agent.py      # Medical bill negotiations
│       │   ├── subscription_agent.py # Subscription negotiations
│       │   └── telecom_agent.py      # Telecom bill negotiations
│       ├── 📁 memory/                # Memory and learning system
│       │   ├── __init__.py
│       │   └── vector_store.py       # ChromaDB integration
│       └── 📁 tools/                 # Negotiation support tools
│           ├── __init__.py
│           └── negotiation_tools.py   # Research, calculation tools
├── 📁 tests/                         # Test suite
│   ├── __init__.py
│   ├── 📁 unit/                      # Unit tests
│   │   ├── __init__.py
│   │   ├── test_api.py               # API endpoint tests
│   │   └── test_api_simple.py        # Simple API tests
│   ├── 📁 integration/               # Integration tests
│   │   ├── __init__.py
│   │   └── test_integration.py       # Integration workflow tests
│   └── 📁 system/                    # System tests
│       ├── __init__.py
│       └── test_system.py            # End-to-end system tests
├── 📁 docs/                          # Documentation
│   ├── 📁 guides/                    # User and developer guides
│   │   ├── Hagglz AI Negotiation Agent - Complete System Overview.md
│   │   └── Hagglz AI Negotiation Agent.md
│   ├── 📁 deployment/                # Deployment documentation
│   │   └── Hagglz Negotiation Agent - Deployment Guide.md
│   └── Hagglz Negotiation Agent - System Status Report.md
├── 📁 config/                        # Configuration files
│   ├── langgraph.yaml                # LangGraph Platform config
│   ├── Dockerfile                    # Container configuration
│   └── docker-compose.yml            # Local development setup
├── 📁 scripts/                       # Utility scripts
│   └── deploy.py                     # Deployment automation
├── 📁 .git/                          # Git repository (hidden)
├── 📄 .gitignore                     # Git exclusions
├── 📄 requirements.txt                # Python dependencies
├── 📄 README.md                       # Main project documentation
├── 📄 LICENSE                         # MIT License
├── 📄 PROJECT_STRUCTURE.md            # This file
└── 📄 todo.md                         # Development tasks
```

## 🏗️ Architecture Overview

### **Source Code (`src/hagglz/`)**
- **API Layer**: FastAPI application with REST endpoints
- **Core System**: Orchestration and routing logic
- **Specialist Agents**: Domain-specific negotiation strategies
- **Memory System**: Vector-based learning and storage
- **Tools**: Research, calculation, and script generation

### **Testing (`tests/`)**
- **Unit Tests**: Individual component testing
- **Integration Tests**: Workflow and API testing
- **System Tests**: End-to-end functionality testing

### **Documentation (`docs/`)**
- **Guides**: User and developer documentation
- **Deployment**: Infrastructure and deployment guides
- **Status Reports**: System health and progress tracking

### **Configuration (`config/`)**
- **LangGraph**: Platform deployment configuration
- **Docker**: Containerization and orchestration
- **Infrastructure**: Development and production setup

### **Scripts (`scripts/`)**
- **Deployment**: Automated deployment processes
- **Utilities**: Development and maintenance tools

## 🔄 Import Structure

### **Main Package Imports**
```python
from hagglz import MasterOrchestrator, RouterAgent
from hagglz.api import app
from hagglz.agents import UtilityNegotiationAgent
from hagglz.memory import NegotiationMemory
from hagglz.tools import NegotiationTools
```

### **Internal Package Imports**
```python
# Within the package
from .core.orchestrator import MasterOrchestrator
from .agents.utility_agent import UtilityNegotiationAgent
from .memory.vector_store import NegotiationMemory
```

## 🚀 Development Workflow

### **Adding New Features**
1. Create feature branch from `main`
2. Implement in appropriate package under `src/hagglz/`
3. Add corresponding tests in `tests/`
4. Update documentation in `docs/`
5. Submit pull request

### **Testing Strategy**
1. **Unit Tests**: Test individual components in isolation
2. **Integration Tests**: Test component interactions
3. **System Tests**: Test complete workflows
4. **Performance Tests**: Test under load and stress

### **Deployment Process**
1. Update configuration in `config/`
2. Modify deployment scripts in `scripts/`
3. Update documentation in `docs/deployment/`
4. Test locally with Docker
5. Deploy to LangGraph Platform

## 📋 File Naming Conventions

- **Python Files**: `snake_case.py`
- **Directories**: `snake_case/`
- **Configuration**: `kebab-case.yaml`
- **Documentation**: `Title Case.md`
- **Constants**: `UPPER_SNAKE_CASE`

## 🔧 Package Dependencies

### **Core Dependencies**
- `src/hagglz/core/` → No internal dependencies
- `src/hagglz/agents/` → Depends on `core/`
- `src/hagglz/api/` → Depends on `core/`, `agents/`, `memory/`, `tools/`
- `src/hagglz/memory/` → No internal dependencies
- `src/hagglz/tools/` → No internal dependencies

### **External Dependencies**
- **LangGraph**: Agent workflow framework
- **FastAPI**: Web API framework
- **ChromaDB**: Vector database
- **OpenAI/Anthropic**: AI model providers

## 📊 Code Quality Standards

- **Type Hints**: All functions and methods
- **Docstrings**: Comprehensive documentation
- **Error Handling**: Graceful error management
- **Testing**: Minimum 80% coverage
- **Linting**: PEP 8 compliance
- **Security**: Input validation and sanitization

---

*This structure provides a clean, maintainable, and scalable foundation for the Hagglz AI Negotiation Agent system.*
