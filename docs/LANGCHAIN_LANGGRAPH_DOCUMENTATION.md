# LangChain, LangGraph & LangGraph Platform - Latest Documentation

## 🦜🔗 **LangChain Framework Overview**

### **Core Components**
LangChain is a framework for developing applications powered by large language models (LLMs) that simplifies every stage of the LLM application lifecycle.

#### **Essential Components**
- **Models**: LLM interfaces (OpenAI, Anthropic, local models)
- **Prompts**: Template management and prompt engineering
- **Chains**: Sequential LLM operations and workflows
- **Agents**: AI systems that can use tools to accomplish tasks
- **Memory**: Persistent state and conversation history
- **Tools**: External integrations and function calling

### **Agent Framework**
Agents enable AI systems to perform a series of actions to accomplish high-level tasks using LLMs as reasoning engines.

#### **Agent Types**
- **ReAct Agents**: Reason and act with tool usage
- **Plan-and-Execute**: Plan steps then execute sub-tasks
- **Tool-Calling Agents**: Use function calling for tool execution
- **Custom Agents**: Build specialized agents for specific domains

#### **Agent Architecture**
```python
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate

# Create agent with tools
agent = create_tool_calling_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools)

# Execute agent
response = agent_executor.invoke({"input": "What is the weather today?"})
```

### **Core Concepts**
- **Runnable Interface**: Common abstraction for building chains and agents
- **State Management**: Persistent state across agent interactions
- **Tool Integration**: External API and function calling capabilities
- **Memory Systems**: Long-term and short-term memory for conversations

---

## 🚀 **LangGraph Framework**

### **Overview**
LangGraph is a low-level orchestration framework for building, managing, and deploying long-running, stateful agents and workflows.

### **Key Features**
- **Stateful Workflows**: Persistent state across execution steps
- **Graph-Based Modeling**: Steps modeled as nodes and edges
- **Durable Execution**: Reliable long-running processes
- **Human-in-the-Loop**: Interactive workflow capabilities
- **Production Deployment**: Enterprise-ready hosting solutions

### **Core Concepts**

#### **State Management**
```python
from typing import TypedDict, List
from langgraph.graph import StateGraph, END

class AgentState(TypedDict):
    input: str
    output: List[str]
    intermediate_steps: List[tuple]

def agent_node(state: AgentState):
    # Process state and return updates
    return {"output": ["Agent response"], "intermediate_steps": []}

# Build workflow
workflow = StateGraph(AgentState)
workflow.add_node("agent", agent_node)
workflow.set_entry_point("agent")
workflow.add_edge("agent", END)
app = workflow.compile()
```

#### **Conditional Workflows**
```python
def should_continue(state):
    return "continue" if state["messages"][-1].tool_calls else "end"

workflow.add_conditional_edges(
    "agent",
    should_continue,
    {
        "continue": "action",
        "end": END,
    }
)
```

### **Workflow Patterns**
- **Sequential**: Linear step-by-step execution
- **Conditional**: Branching based on state
- **Recursive**: Looping workflows with state persistence
- **Parallel**: Concurrent execution of independent steps

---

## ☁️ **LangGraph Platform**

### **Deployment Options**

#### **1. Cloud SaaS (Recommended for Production)**
- **Management**: Fully managed by LangChain
- **CI/CD**: Automatic deployment from GitHub
- **Scaling**: Up to 10 replicas, 500 requests/second
- **Features**: Automatic backups, high availability
- **Pricing**: Plus plan with usage-based billing

#### **2. Self-Hosted Data Plane**
- **Control**: LangChain manages control plane, you manage data
- **Infrastructure**: Your cloud (Kubernetes, ECS)
- **Requirements**: Enterprise license
- **Benefits**: Data residency, custom scaling

#### **3. Self-Hosted Control Plane**
- **Control**: Fully self-hosted
- **Infrastructure**: Your Kubernetes cluster
- **Requirements**: Enterprise license
- **Benefits**: Complete control, custom resources

#### **4. Standalone Container**
- **Control**: Self-managed infrastructure
- **Infrastructure**: Your Docker environment
- **Requirements**: Developer license
- **Benefits**: Maximum flexibility, lowest cost

### **Deployment Types**

#### **Development**
- **Resources**: 1 CPU, 1 GB RAM
- **Scaling**: Up to 1 container
- **Database**: 10 GB disk, no backups
- **Use Case**: Testing, development, internal use

#### **Production**
- **Resources**: 2 CPU, 2 GB RAM
- **Scaling**: Up to 10 containers
- **Database**: Autoscaling disk, automatic backups
- **Use Case**: Customer-facing applications, production workloads

### **Configuration Requirements**

#### **langgraph.json**
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
  }
}
```

#### **Environment Variables**
```bash
# Required for deployment
OPENAI_API_KEY=your_openai_api_key_here
ANTHROPIC_API_KEY=your_anthropic_api_key_here

# Optional for enhanced functionality
LANGSMITH_API_KEY=your_langsmith_key_here
LANGSMITH_WORKSPACE_ID=your_workspace_id_here
```

### **Deployment Process**

#### **1. Repository Setup**
- Connect GitHub repository to LangGraph Platform
- Ensure `langgraph.json` is in root directory
- Set required environment variables

#### **2. Automatic Deployment**
- Platform detects configuration changes
- Builds Docker image automatically
- Deploys to selected environment
- Provides deployment URL and monitoring

#### **3. CI/CD Pipeline**
- Automatic builds on push to main branch
- Environment-specific deployments
- Rollback capabilities
- Health monitoring and alerts

---

## 🛠️ **Implementation Best Practices**

### **Agent Design Patterns**

#### **1. Stateful Agents**
```python
class NegotiationState(TypedDict):
    user_input: str
    bill_type: str
    negotiation_strategy: str
    conversation_history: List[dict]
    current_step: str
    confidence_score: float

def create_negotiation_agent():
    workflow = StateGraph(NegotiationState)
    
    # Add nodes for each step
    workflow.add_node("classify_bill", classify_bill_type)
    workflow.add_node("select_strategy", select_negotiation_strategy)
    workflow.add_node("execute_negotiation", execute_negotiation)
    
    # Define workflow
    workflow.set_entry_point("classify_bill")
    workflow.add_edge("classify_bill", "select_strategy")
    workflow.add_edge("select_strategy", "execute_negotiation")
    
    return workflow.compile()
```

#### **2. Tool Integration**
```python
from langchain_core.tools import tool

@tool
def research_bill_company(company_name: str) -> str:
    """Research company information for bill negotiation."""
    # Implementation for company research
    return f"Company research results for {company_name}"

@tool
def calculate_savings_potential(bill_amount: float, bill_type: str) -> str:
    """Calculate potential savings based on bill type and amount."""
    # Implementation for savings calculation
    return f"Potential savings: ${bill_amount * 0.15:.2f}"
```

### **Memory and Persistence**

#### **1. Vector Memory**
```python
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings

class NegotiationMemory:
    def __init__(self):
        self.embeddings = OpenAIEmbeddings()
        self.vectorstore = Chroma(
            collection_name="negotiation_strategies",
            embedding_function=self.embeddings
        )
    
    def store_strategy(self, strategy: str, metadata: dict):
        """Store negotiation strategy in vector memory."""
        self.vectorstore.add_texts([strategy], metadatas=[metadata])
    
    def retrieve_similar_strategies(self, query: str, k: int = 5):
        """Retrieve similar negotiation strategies."""
        return self.vectorstore.similarity_search(query, k=k)
```

#### **2. Conversation Memory**
```python
from langchain.memory import ConversationBufferMemory

class NegotiationAgent:
    def __init__(self):
        self.memory = ConversationBufferMemory(
            memory_key="conversation_history",
            return_messages=True
        )
    
    def add_to_memory(self, user_input: str, agent_response: str):
        """Add conversation turn to memory."""
        self.memory.chat_memory.add_user_message(user_input)
        self.memory.chat_memory.add_ai_message(agent_response)
```

### **Error Handling and Resilience**

#### **1. Graceful Degradation**
```python
def safe_tool_execution(tool_func, *args, **kwargs):
    """Execute tool with error handling and fallback."""
    try:
        return tool_func(*args, **kwargs)
    except Exception as e:
        logger.warning(f"Tool execution failed: {e}")
        return f"Unable to execute {tool_func.__name__}: {str(e)}"
```

#### **2. Retry Logic**
```python
from tenacity import retry, stop_after_attempt, wait_exponential

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
def reliable_api_call(api_func, *args, **kwargs):
    """Execute API call with exponential backoff retry."""
    return api_func(*args, **kwargs)
```

---

## 📊 **Monitoring and Observability**

### **LangSmith Integration**
```python
import os
from langsmith import Client

# Configure LangSmith
os.environ["LANGSMITH_API_KEY"] = "your_api_key"
os.environ["LANGSMITH_PROJECT"] = "hagglz-negotiation"

# LangSmith client for tracing
langsmith_client = Client()

# Trace agent execution
with langsmith_client.trace(
    project_name="hagglz-negotiation",
    tags=["negotiation", "bill-reduction"]
) as tracer:
    result = agent_executor.invoke({"input": user_input})
    tracer.add_metadata({"bill_type": bill_type, "confidence": confidence_score})
```

### **Custom Metrics**
```python
from dataclasses import dataclass
from datetime import datetime
import time

@dataclass
class NegotiationMetrics:
    start_time: datetime
    end_time: datetime = None
    bill_type: str = None
    initial_amount: float = None
    final_amount: float = None
    negotiation_steps: int = 0
    success: bool = False
    
    @property
    def duration(self) -> float:
        if self.end_time:
            return (self.end_time - self.start_time).total_seconds()
        return time.time() - self.start_time.timestamp()
    
    @property
    def savings_amount(self) -> float:
        if self.initial_amount and self.final_amount:
            return self.initial_amount - self.final_amount
        return 0.0
    
    @property
    def savings_percentage(self) -> float:
        if self.initial_amount and self.savings_amount > 0:
            return (self.savings_amount / self.initial_amount) * 100
        return 0.0
```

---

## 🔒 **Security and Compliance**

### **API Key Management**
```python
from langchain_core.runnables import RunnableConfig
import os

def get_secure_config() -> RunnableConfig:
    """Get secure configuration with proper API key handling."""
    return RunnableConfig(
        configurable={
            "openai_api_key": os.getenv("OPENAI_API_KEY"),
            "anthropic_api_key": os.getenv("ANTHROPIC_API_KEY"),
        },
        tags=["secure", "production"]
    )
```

### **Data Privacy**
```python
import hashlib
from typing import Optional

def anonymize_user_data(user_input: str, salt: str = "hagglz_salt") -> str:
    """Anonymize user data for logging and monitoring."""
    if not user_input:
        return ""
    
    # Hash sensitive information
    hashed = hashlib.sha256((user_input + salt).encode()).hexdigest()
    return f"user_{hashed[:8]}"

def sanitize_for_logging(data: dict) -> dict:
    """Remove sensitive information from data before logging."""
    sensitive_fields = ["credit_card", "ssn", "phone", "email"]
    sanitized = data.copy()
    
    for field in sensitive_fields:
        if field in sanitized:
            sanitized[field] = "[REDACTED]"
    
    return sanitized
```

---

## 🚀 **Performance Optimization**

### **Async Execution**
```python
import asyncio
from langchain_core.runnables import RunnableConfig

async def execute_negotiation_async(user_input: str, config: RunnableConfig):
    """Execute negotiation workflow asynchronously."""
    try:
        result = await agent_executor.ainvoke(
            {"input": user_input}, 
            config=config
        )
        return result
    except Exception as e:
        logger.error(f"Async execution failed: {e}")
        raise

# Batch processing
async def process_multiple_negotiations(requests: List[str]):
    """Process multiple negotiation requests concurrently."""
    tasks = [
        execute_negotiation_async(req, get_secure_config())
        for req in requests
    ]
    return await asyncio.gather(*tasks, return_exceptions=True)
```

### **Caching Strategies**
```python
from functools import lru_cache
import redis
import json

redis_client = redis.Redis(host='localhost', port=6379, db=0)

@lru_cache(maxsize=1000)
def cached_company_research(company_name: str) -> dict:
    """Cache company research results."""
    cache_key = f"company_research:{company_name.lower()}"
    
    # Check Redis cache first
    cached = redis_client.get(cache_key)
    if cached:
        return json.loads(cached)
    
    # Perform research and cache
    research_result = perform_company_research(company_name)
    redis_client.setex(cache_key, 3600, json.dumps(research_result))  # 1 hour TTL
    
    return research_result
```

---

## 📚 **Additional Resources**

### **Official Documentation**
- [LangChain Documentation](https://python.langchain.com/)
- [LangGraph Documentation](https://langchain-ai.github.io/langgraph/)
- [LangGraph Platform Guide](https://langchain-ai.github.io/langgraph/)

### **Community Resources**
- [LangChain Academy](https://academy.langchain.com/)
- [LangChain Discord](https://discord.gg/langchain)
- [GitHub Repositories](https://github.com/langchain-ai)

### **Best Practices**
- Use typed state management for complex workflows
- Implement proper error handling and fallbacks
- Monitor performance with LangSmith tracing
- Design agents with clear separation of concerns
- Test thoroughly before production deployment

---

*This documentation is based on the latest LangChain, LangGraph, and LangGraph Platform releases. For the most up-to-date information, always refer to the official documentation.*
