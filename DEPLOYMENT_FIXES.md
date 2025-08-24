# Deployment Fixes for Hagglz Negotiation Agent

## Issues Identified

The deployment was failing with two main errors:

1. **Lifespan Conflict**: `ValueError: Cannot merge lifespans with on_startup or on_shutdown`
2. **Import Path Issues**: Module resolution problems due to incorrect import paths

## Fixes Applied

### 1. Fixed FastAPI Lifespan Compatibility

**Problem**: The application was using the deprecated `@app.on_event("startup")` decorator, which is incompatible with LangGraph Platform's lifespan management.

**Solution**: Replaced the deprecated startup event with a modern `lifespan` context manager.

**Files Modified**:
- `src/hagglz/api/main.py`

**Changes**:
```python
# Before (deprecated)
@app.on_event("startup")
async def startup_event():
    # ... startup logic

# After (modern approach)
@asynccontextmanager
async def lifespan(app: FastAPI):
    # ... startup logic
    yield
    # ... shutdown logic

app = FastAPI(
    # ... other config
    lifespan=lifespan
)
```

### 2. Fixed Import Path Issues

**Problem**: Absolute imports (`from hagglz.core.orchestrator import MasterOrchestrator`) were not resolving correctly in the deployment environment.

**Solution**: Updated all imports to use relative imports for better module resolution.

**Files Modified**:
- `src/hagglz/api/main.py`
- `src/hagglz/core/orchestrator.py`
- `src/hagglz/__init__.py`

**Changes**:
```python
# Before (absolute imports)
from hagglz.core.orchestrator import MasterOrchestrator

# After (relative imports)
from ..core.orchestrator import MasterOrchestrator
```

### 3. Updated Docker Configuration

**Problem**: The Dockerfile was using incorrect import paths and Python path configuration.

**Solution**: Updated the Dockerfile to use the correct module paths and Python path.

**Files Modified**:
- `config/Dockerfile`

**Changes**:
```dockerfile
# Updated Python path
ENV PYTHONPATH="/app/src:$PYTHONPATH"

# Updated command to use correct import path
CMD ["python", "-m", "uvicorn", "hagglz.api.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "1"]
```

### 4. Updated LangGraph Configuration

**Problem**: The LangGraph configuration was pointing to incorrect file paths.

**Solution**: Updated all paths to reflect the correct source directory structure.

**Files Modified**:
- `config/langgraph.yaml`

**Changes**:
```yaml
# Updated graph paths
graphs:
  - name: "master_orchestrator"
    path: "./src/hagglz/core/orchestrator.py"
    
# Updated API path
api:
  path: "./src/hagglz/api/main.py"
```

### 5. Updated Dependencies

**Problem**: Some dependencies had version conflicts or were missing.

**Solution**: Updated requirements.txt with compatible versions and added missing dependencies.

**Files Modified**:
- `requirements.txt`

**Changes**:
```txt
# Updated versions for compatibility
langchain-community>=0.4.0
uvicorn[standard]>=0.24.0
openai>=1.0.0
```

## Testing

After applying the fixes, all imports were tested successfully:

```bash
✓ MasterOrchestrator imported successfully
✓ NegotiationMemory imported successfully
✓ NegotiationTools imported successfully
✓ FastAPI app imported successfully
```

## Deployment Notes

1. **Environment Variables**: Ensure all required environment variables are set:
   - `OPENAI_API_KEY`
   - `ANTHROPIC_API_KEY`
   - `LANGCHAIN_API_KEY` (optional)

2. **Python Path**: The application now correctly sets `PYTHONPATH=/app/src` in the container.

3. **Module Structure**: All modules use relative imports for better compatibility with LangGraph Platform.

4. **Health Check**: The application includes a `/health` endpoint for monitoring.

## Next Steps

1. **Deploy**: The application should now deploy successfully on LangGraph Platform.
2. **Monitor**: Watch the logs for any remaining issues.
3. **Test**: Verify all endpoints are working correctly after deployment.
4. **Scale**: The configuration supports auto-scaling from 1 to 5 instances.

## Troubleshooting

If deployment still fails:

1. Check the LangGraph Platform logs for specific error messages
2. Verify all environment variables are set correctly
3. Ensure the container has sufficient resources (2GB RAM, 1 CPU)
4. Check that the health check endpoint is responding correctly

## Files Modified Summary

- `src/hagglz/api/main.py` - Fixed lifespan and imports
- `src/hagglz/core/orchestrator.py` - Fixed imports
- `src/hagglz/__init__.py` - Fixed imports
- `config/Dockerfile` - Fixed paths and commands
- `config/langgraph.yaml` - Updated file paths
- `requirements.txt` - Updated dependencies
