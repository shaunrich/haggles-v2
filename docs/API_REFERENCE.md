# Hagglz AI Negotiation Agent - API Reference

## 🌐 **API Overview**

The Hagglz AI Negotiation Agent provides a comprehensive REST API for bill negotiation services. The API is built with FastAPI and offers endpoints for bill classification, negotiation strategy generation, and agent execution.

---

## 🔑 **Authentication**

### **API Key Authentication**
All API endpoints require authentication using a LangSmith API key.

```bash
# Header format
X-Api-Key: your_langsmith_api_key_here
```

### **Environment Setup**
```bash
export LANGSMITH_API_KEY="your_api_key_here"
export LANGSMITH_WORKSPACE_ID="your_workspace_id_here"
```

---

## 📋 **Base URL**

```
Production: https://your-deployment-url.langgraph.ai
Local: http://localhost:8000
```

---

## 🚀 **Core Endpoints**

### **1. Health Check**

#### **GET /health**
Check system health and status.

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2025-01-24T10:30:00Z",
  "version": "2.0.0",
  "components": {
    "orchestrator": "operational",
    "memory": "operational",
    "agents": "operational"
  }
}
```

---

### **2. Bill Classification**

#### **POST /classify-bill**
Classify a bill and determine the appropriate negotiation strategy.

**Request Body:**
```json
{
  "bill_description": "Monthly electricity bill from EDF Energy",
  "bill_amount": 89.50,
  "bill_type": "utility",
  "company_name": "EDF Energy",
  "due_date": "2025-02-15",
  "user_context": {
    "location": "London, UK",
    "payment_history": "good",
    "negotiation_experience": "beginner"
  }
}
```

**Response:**
```json
{
  "bill_classification": {
    "primary_type": "utility",
    "confidence": 0.95,
    "sub_type": "electricity",
    "negotiation_complexity": "medium"
  },
  "recommended_agent": "utility_agent",
  "estimated_savings_potential": {
    "min": 15.0,
    "max": 25.0,
    "currency": "GBP"
  },
  "next_steps": [
    "Research company policies",
    "Prepare negotiation script",
    "Execute negotiation strategy"
  ]
}
```

---

### **3. Negotiation Strategy Generation**

#### **POST /generate-strategy**
Generate a comprehensive negotiation strategy for a specific bill.

**Request Body:**
```json
{
  "bill_type": "utility",
  "company_name": "EDF Energy",
  "bill_amount": 89.50,
  "user_context": {
    "location": "London, UK",
    "payment_history": "good",
    "negotiation_experience": "beginner",
    "preferred_approach": "polite but firm"
  },
  "constraints": {
    "max_time": 30,
    "preferred_outcome": "reduction",
    "avoid_approaches": ["aggressive", "confrontational"]
  }
}
```

**Response:**
```json
{
  "strategy": {
    "approach": "relationship_building",
    "key_points": [
      "Highlight good payment history",
      "Mention loyalty as customer",
      "Request goodwill adjustment"
    ],
    "script": {
      "opening": "Hello, I'm calling about my monthly electricity bill...",
      "main_points": [
        "I've been a loyal customer for X years",
        "My payment history has been excellent",
        "I'm experiencing some financial challenges"
      ],
      "closing": "Is there anything you can do to help reduce this bill?"
    },
    "confidence_score": 0.87,
    "estimated_success_rate": 0.75
  },
  "supporting_materials": {
    "company_policies": "EDF offers loyalty discounts for long-term customers",
    "competitor_rates": "British Gas offers 15% lower rates for new customers",
    "negotiation_tips": [
      "Call during business hours",
      "Be polite and patient",
      "Have account details ready"
    ]
  }
}
```

---

### **4. Agent Execution**

#### **POST /execute-negotiation**
Execute a negotiation using the specified agent.

**Request Body:**
```json
{
  "agent_type": "utility_agent",
  "bill_context": {
    "bill_type": "utility",
    "company_name": "EDF Energy",
    "bill_amount": 89.50,
    "due_date": "2025-02-15"
  },
  "user_preferences": {
    "communication_style": "professional",
    "risk_tolerance": "medium",
    "time_constraints": 30
  },
  "execution_mode": "confidence_based"
}
```

**Response:**
```json
{
  "execution_id": "neg_12345",
  "status": "in_progress",
  "agent_actions": [
    {
      "step": 1,
      "action": "research_company",
      "description": "Researching EDF Energy policies and current offers",
      "status": "completed",
      "result": "Found loyalty discount program available"
    },
    {
      "step": 2,
      "action": "generate_script",
      "description": "Creating personalized negotiation script",
      "status": "completed",
      "result": "Script generated with 87% confidence"
    }
  ],
  "current_step": "execute_negotiation",
  "estimated_completion": "2025-01-24T11:00:00Z",
  "confidence_score": 0.87
}
```

---

### **5. Strategy Memory Management**

#### **GET /strategies**
Retrieve stored negotiation strategies.

**Query Parameters:**
- `bill_type` (optional): Filter by bill type
- `company_name` (optional): Filter by company
- `success_rate_min` (optional): Minimum success rate
- `limit` (optional): Maximum results (default: 50)

**Response:**
```json
{
  "strategies": [
    {
      "id": "strat_001",
      "bill_type": "utility",
      "company_name": "EDF Energy",
      "strategy_summary": "Loyalty-based approach with payment history emphasis",
      "success_rate": 0.82,
      "usage_count": 15,
      "last_used": "2025-01-20T14:30:00Z",
      "tags": ["loyalty", "payment_history", "good_customer"]
    }
  ],
  "total_count": 150,
  "page": 1,
  "per_page": 50
}
```

#### **POST /strategies**
Store a new negotiation strategy.

**Request Body:**
```json
{
  "bill_type": "utility",
  "company_name": "EDF Energy",
  "strategy": {
    "approach": "loyalty_based",
    "key_points": ["payment_history", "customer_loyalty"],
    "script": "Custom negotiation script...",
    "success_indicators": ["discount_offered", "payment_plan_agreed"]
  },
  "outcome": {
    "success": true,
    "savings_amount": 22.50,
    "savings_percentage": 25.1,
    "notes": "Successfully negotiated 25% reduction"
  },
  "tags": ["loyalty", "payment_history", "successful"]
}
```

---

## 🧠 **Agent-Specific Endpoints**

### **Utility Agent**

#### **POST /agents/utility/negotiate**
Execute utility bill negotiation.

**Request Body:**
```json
{
  "bill_details": {
    "service_type": "electricity",
    "provider": "EDF Energy",
    "amount": 89.50,
    "usage_period": "monthly"
  },
  "user_profile": {
    "location": "London, UK",
    "payment_history": "excellent",
    "contract_duration": "3 years"
  }
}
```

### **Medical Agent**

#### **POST /agents/medical/negotiate**
Execute medical bill negotiation.

**Request Body:**
```json
{
  "bill_details": {
    "service_type": "consultation",
    "provider": "NHS Trust",
    "amount": 150.00,
    "procedure_date": "2025-01-15"
  },
  "user_profile": {
    "insurance_status": "uninsured",
    "financial_hardship": true,
    "payment_ability": "limited"
  }
}
```

### **Subscription Agent**

#### **POST /agents/subscription/negotiate**
Execute subscription service negotiation.

**Request Body:**
```json
{
  "bill_details": {
    "service_type": "streaming",
    "provider": "Netflix",
    "amount": 15.99,
    "subscription_tier": "premium"
  },
  "user_profile": {
    "usage_pattern": "moderate",
    "loyalty_duration": "2 years",
    "cancellation_threat": false
  }
}
```

### **Telecom Agent**

#### **POST /agents/telecom/negotiate**
Execute telecom bill negotiation.

**Request Body:**
```json
{
  "bill_details": {
    "service_type": "mobile",
    "provider": "Vodafone",
    "amount": 45.00,
    "plan_type": "unlimited_data"
  },
  "user_profile": {
    "contract_status": "month_to_month",
    "data_usage": "high",
    "competitor_offers": ["Three", "EE"]
  }
}
```

---

## 📊 **Analytics & Monitoring**

### **GET /analytics/performance**
Get system performance metrics.

**Response:**
```json
{
  "overall_metrics": {
    "total_negotiations": 1250,
    "success_rate": 0.78,
    "average_savings": 18.50,
    "total_savings": 23125.00
  },
  "agent_performance": {
    "utility_agent": {
      "success_rate": 0.82,
      "average_savings": 22.30,
      "total_negotiations": 450
    },
    "medical_agent": {
      "success_rate": 0.71,
      "average_savings": 45.20,
      "total_negotiations": 200
    }
  },
  "time_period": {
    "start": "2025-01-01T00:00:00Z",
    "end": "2025-01-24T23:59:59Z"
  }
}
```

### **GET /analytics/strategies**
Get strategy effectiveness analytics.

**Response:**
```json
{
  "top_strategies": [
    {
      "strategy_id": "strat_001",
      "approach": "loyalty_based",
      "success_rate": 0.85,
      "usage_count": 45,
      "average_savings": 25.30
    }
  ],
  "strategy_evolution": {
    "trends": [
      "Loyalty-based approaches showing 15% improvement",
      "Payment history emphasis increasing success rates"
    ]
  }
}
```

---

## 🔧 **System Management**

### **GET /system/status**
Get detailed system status.

**Response:**
```json
{
  "system_status": "operational",
  "components": {
    "orchestrator": {
      "status": "healthy",
      "uptime": "99.8%",
      "last_check": "2025-01-24T10:30:00Z"
    },
    "memory_system": {
      "status": "healthy",
      "storage_usage": "45%",
      "vector_count": 1250
    },
    "agents": {
      "utility_agent": "healthy",
      "medical_agent": "healthy",
      "subscription_agent": "healthy",
      "telecom_agent": "healthy"
    }
  },
  "performance_metrics": {
    "average_response_time": "2.3s",
    "requests_per_minute": 45,
    "error_rate": "0.02%"
  }
}
```

### **POST /system/maintenance**
Trigger system maintenance mode.

**Request Body:**
```json
{
  "maintenance_type": "scheduled",
  "duration_minutes": 30,
  "reason": "Database optimization",
  "affected_services": ["strategy_generation", "analytics"]
}
```

---

## 📝 **Error Handling**

### **Error Response Format**
```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid bill amount provided",
    "details": {
      "field": "bill_amount",
      "value": -50.00,
      "constraint": "Amount must be positive"
    },
    "timestamp": "2025-01-24T10:30:00Z",
    "request_id": "req_12345"
  }
}
```

### **Common Error Codes**
- `VALIDATION_ERROR`: Invalid input data
- `AUTHENTICATION_ERROR`: Invalid or missing API key
- `AGENT_UNAVAILABLE`: Requested agent is not available
- `STRATEGY_NOT_FOUND`: Requested strategy does not exist
- `SYSTEM_ERROR`: Internal system error
- `RATE_LIMIT_EXCEEDED`: Too many requests

---

## 📚 **Data Models**

### **Bill Classification Request**
```typescript
interface BillClassificationRequest {
  bill_description: string;
  bill_amount: number;
  bill_type?: string;
  company_name?: string;
  due_date?: string;
  user_context?: {
    location?: string;
    payment_history?: 'excellent' | 'good' | 'fair' | 'poor';
    negotiation_experience?: 'beginner' | 'intermediate' | 'expert';
  };
}
```

### **Negotiation Strategy Response**
```typescript
interface NegotiationStrategy {
  approach: string;
  key_points: string[];
  script: {
    opening: string;
    main_points: string[];
    closing: string;
  };
  confidence_score: number;
  estimated_success_rate: number;
}
```

### **Agent Execution Request**
```typescript
interface AgentExecutionRequest {
  agent_type: 'utility_agent' | 'medical_agent' | 'subscription_agent' | 'telecom_agent';
  bill_context: {
    bill_type: string;
    company_name: string;
    bill_amount: number;
    due_date?: string;
  };
  user_preferences: {
    communication_style?: string;
    risk_tolerance?: 'low' | 'medium' | 'high';
    time_constraints?: number;
  };
  execution_mode: 'confidence_based' | 'aggressive' | 'conservative';
}
```

---

## 🚀 **Rate Limiting**

### **Limits**
- **Standard**: 100 requests per minute
- **Premium**: 500 requests per minute
- **Enterprise**: 1000 requests per minute

### **Headers**
```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1643025600
```

---

## 📖 **Examples**

### **Complete Negotiation Flow**
```bash
# 1. Classify bill
curl -X POST "https://api.hagglz.ai/classify-bill" \
  -H "X-Api-Key: your_api_key" \
  -H "Content-Type: application/json" \
  -d '{
    "bill_description": "Monthly electricity bill",
    "bill_amount": 89.50,
    "company_name": "EDF Energy"
  }'

# 2. Generate strategy
curl -X POST "https://api.hagglz.ai/generate-strategy" \
  -H "X-Api-Key: your_api_key" \
  -H "Content-Type: application/json" \
  -d '{
    "bill_type": "utility",
    "company_name": "EDF Energy",
    "bill_amount": 89.50
  }'

# 3. Execute negotiation
curl -X POST "https://api.hagglz.ai/execute-negotiation" \
  -H "X-Api-Key: your_api_key" \
  -H "Content-Type: application/json" \
  -d '{
    "agent_type": "utility_agent",
    "bill_context": {
      "bill_type": "utility",
      "company_name": "EDF Energy",
      "bill_amount": 89.50
    }
  }'
```

---

## 🔗 **SDK & Libraries**

### **Python SDK**
```python
from hagglz_sdk import HagglzClient

client = HagglzClient(api_key="your_api_key")

# Classify bill
classification = client.classify_bill(
    bill_description="Monthly electricity bill",
    bill_amount=89.50,
    company_name="EDF Energy"
)

# Generate strategy
strategy = client.generate_strategy(
    bill_type="utility",
    company_name="EDF Energy",
    bill_amount=89.50
)

# Execute negotiation
execution = client.execute_negotiation(
    agent_type="utility_agent",
    bill_context={
        "bill_type": "utility",
        "company_name": "EDF Energy",
        "bill_amount": 89.50
    }
)
```

### **JavaScript SDK**
```javascript
import { HagglzClient } from '@hagglz/sdk';

const client = new HagglzClient({ apiKey: 'your_api_key' });

// Classify bill
const classification = await client.classifyBill({
  billDescription: 'Monthly electricity bill',
  billAmount: 89.50,
  companyName: 'EDF Energy'
});

// Generate strategy
const strategy = await client.generateStrategy({
  billType: 'utility',
  companyName: 'EDF Energy',
  billAmount: 89.50
});
```

---

*For additional support and examples, please refer to the [Knowledge Base Index](KNOWLEDGE_BASE_INDEX.md) or contact the development team.*
