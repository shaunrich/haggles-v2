# Hagglz AI Negotiation Agent

A comprehensive AI-powered negotiation system built with LangGraph Platform that specialises in bill negotiation across multiple categories including utilities, medical bills, subscriptions, and telecommunications.

## Features

- **Multi-Agent Architecture**: Specialised agents for different bill types
- **Intelligent Routing**: Automatic bill classification and routing to appropriate specialists
- **Confidence-Based Execution**: Automated, supervised, or human-handoff modes based on confidence scores
- **Memory System**: Vector-based storage of successful negotiation strategies
- **RESTful API**: FastAPI-based interface for integration
- **LangGraph Platform**: Cloud deployment and monitoring

## Architecture

### Core Components

1. **Router Agent**: Classifies bills and routes to appropriate specialists
2. **Specialist Agents**:
   - Utility Agent: Electric, gas, water bills
   - Medical Agent: Healthcare, dental, medical bills  
   - Subscription Agent: Streaming, software services
   - Telecom Agent: Phone, internet, cable bills
3. **Master Orchestrator**: Coordinates workflow and confidence evaluation
4. **Memory System**: ChromaDB vector store for negotiation history
5. **Tools**: Research, calculation, and script generation utilities

### Confidence Thresholds

- **>0.8**: Automatic execution
- **0.5-0.8**: Supervised execution
- **<0.5**: Human handoff required

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd hagglz-agent
```

2. Set up virtual environment:
```bash
python3.11 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure environment variables:
```bash
cp .env.example .env
# Edit .env with your API keys and configuration
```

## Usage

### Local Development

1. Start the API server:
```bash
uvicorn api.main:app --reload --host 0.0.0.0 --port 8000
```

2. Access the API documentation:
```
http://localhost:8000/docs
```

### LangGraph Platform Deployment

1. Install LangGraph CLI:
```bash
pip install langgraph-cli
```

2. Deploy to LangGraph Cloud:
```bash
langgraph deploy --config langgraph.yaml
```

## API Endpoints

- `POST /api/v1/negotiate`: Start a new negotiation
- `GET /api/v1/negotiation/{negotiation_id}`: Get negotiation status
- `POST /api/v1/feedback`: Provide feedback on negotiation results

## Testing

Run the test suite:
```bash
pytest tests/
```

## Monitoring

The system includes comprehensive monitoring through:
- LangSmith tracing
- Custom metrics tracking
- Performance monitoring
- Success rate analytics

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## Licence

[Add your licence information here]

