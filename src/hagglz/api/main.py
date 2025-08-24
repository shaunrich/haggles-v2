"""
Hagglz Negotiation API

FastAPI application providing REST endpoints for the Hagglz AI negotiation system.
"""

from fastapi import FastAPI, HTTPException, UploadFile, File, Depends, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
import base64
import logging
import uuid
from datetime import datetime
import os

# Absolute imports for LangGraph Platform compatibility
from hagglz.core.orchestrator import MasterOrchestrator
from hagglz.memory.vector_store import NegotiationMemory
from hagglz.tools.negotiation_tools import NegotiationTools

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Hagglz Negotiation API",
    description="AI-powered bill negotiation system with specialised agents",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global instances
orchestrator = None
memory_system = None
negotiation_tools = None

# Pydantic models for API
class BillUploadRequest(BaseModel):
    """Request model for bill upload"""
    bill_image: str = Field(..., description="Base64 encoded bill image")
    user_id: str = Field(..., description="User identifier")
    target_savings: Optional[float] = Field(None, description="Target savings percentage")
    additional_context: Optional[Dict[str, Any]] = Field(None, description="Additional context")

class NegotiationRequest(BaseModel):
    """Request model for starting negotiation"""
    bill_text: str = Field(..., description="OCR extracted text from bill")
    user_id: str = Field(..., description="User identifier")
    company: Optional[str] = Field(None, description="Company name")
    amount: Optional[float] = Field(None, description="Bill amount")
    target_savings: Optional[float] = Field(None, description="Target savings percentage")

class NegotiationResponse(BaseModel):
    """Response model for negotiation results"""
    negotiation_id: str
    status: str
    bill_type: str
    company: str
    amount: float
    confidence_score: float
    execution_mode: str
    strategy: str
    script: str
    target_savings: Dict[str, Any]
    estimated_annual_savings: float

class FeedbackRequest(BaseModel):
    """Request model for negotiation feedback"""
    negotiation_id: str
    success: bool
    actual_savings: Optional[float] = None
    final_amount: Optional[float] = None
    notes: Optional[str] = None
    difficulty_rating: Optional[int] = Field(None, ge=1, le=5)

class HealthResponse(BaseModel):
    """Response model for health check"""
    status: str
    timestamp: str
    version: str
    components: Dict[str, str]

# Startup event
@app.on_event("startup")
async def startup_event():
    """Initialize system components on startup"""
    global orchestrator, memory_system, negotiation_tools
    
    try:
        logger.info("Initialising Hagglz Negotiation System...")
        
        # Initialize orchestrator
        orchestrator = MasterOrchestrator()
        logger.info("Master orchestrator initialised")
        
        # Initialize memory system
        memory_system = NegotiationMemory()
        logger.info("Memory system initialised")
        
        # Initialize tools
        negotiation_tools = NegotiationTools()
        logger.info("Negotiation tools initialised")
        
        logger.info("Hagglz Negotiation System startup complete")
        
    except Exception as e:
        logger.error(f"Error during startup: {str(e)}")
        raise

# Health check endpoint
@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    return HealthResponse(
        status="healthy",
        timestamp=datetime.now().isoformat(),
        version="1.0.0",
        components={
            "orchestrator": "active" if orchestrator else "inactive",
            "memory_system": "active" if memory_system else "inactive",
            "negotiation_tools": "active" if negotiation_tools else "inactive"
        }
    )

# Main negotiation endpoint
@app.post("/api/v1/negotiate", response_model=NegotiationResponse)
async def start_negotiation(request: NegotiationRequest, background_tasks: BackgroundTasks):
    """Start a new bill negotiation process"""
    try:
        logger.info(f"Starting negotiation for user: {request.user_id}")
        
        if not orchestrator:
            raise HTTPException(status_code=500, detail="Orchestrator not initialised")
        
        # Generate unique negotiation ID
        negotiation_id = str(uuid.uuid4())
        
        # Prepare bill data for processing
        bill_data = {
            'text': request.bill_text,
            'user_id': request.user_id,
            'company': request.company,
            'amount': request.amount,
            'target_savings': request.target_savings
        }
        
        # Process through orchestrator
        result = orchestrator.process_bill(bill_data, request.user_id)
        
        # Handle processing errors
        if 'error' in result:
            raise HTTPException(status_code=400, detail=result['error'])
        
        # Extract results
        target_savings = result.get('target_savings', {})
        estimated_annual = target_savings.get('annual_savings', 0) if isinstance(target_savings, dict) else 0
        
        # Store negotiation in memory (background task)
        background_tasks.add_task(
            store_negotiation_strategy,
            negotiation_id,
            result,
            request.user_id
        )
        
        response = NegotiationResponse(
            negotiation_id=negotiation_id,
            status=result.get('processing_status', 'completed'),
            bill_type=result.get('bill_type', 'Unknown'),
            company=result.get('company', 'Unknown'),
            amount=result.get('amount', 0.0),
            confidence_score=result.get('confidence_score', 0.0),
            execution_mode=result.get('execution_mode', 'unknown'),
            strategy=result.get('negotiation_strategy', ''),
            script=result.get('negotiation_script', ''),
            target_savings=target_savings,
            estimated_annual_savings=estimated_annual
        )
        
        logger.info(f"Negotiation {negotiation_id} completed with confidence {response.confidence_score}")
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in negotiation processing: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

# Bill upload with OCR processing
@app.post("/api/v1/upload-bill")
async def upload_bill(request: BillUploadRequest):
    """Upload and process a bill image"""
    try:
        logger.info(f"Processing bill upload for user: {request.user_id}")
        
        # Decode base64 image
        try:
            image_data = base64.b64decode(request.bill_image)
        except Exception as e:
            raise HTTPException(status_code=400, detail="Invalid base64 image data")
        
        # In a real implementation, you would use OCR here
        # For now, we'll return a placeholder response
        ocr_text = "SAMPLE BILL\nCOMPANY NAME\nAmount Due: $150.00"
        
        return {
            "upload_id": str(uuid.uuid4()),
            "ocr_text": ocr_text,
            "status": "processed",
            "message": "Bill uploaded and processed successfully. Use the OCR text to start negotiation."
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error processing bill upload: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Upload processing error: {str(e)}")

# Get negotiation status
@app.get("/api/v1/negotiation/{negotiation_id}")
async def get_negotiation_status(negotiation_id: str):
    """Get the status of a specific negotiation"""
    try:
        # In a real implementation, you would retrieve from database
        # For now, return a placeholder response
        return {
            "negotiation_id": negotiation_id,
            "status": "completed",
            "created_at": datetime.now().isoformat(),
            "last_updated": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error retrieving negotiation status: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Status retrieval error: {str(e)}")

# Submit feedback
@app.post("/api/v1/feedback")
async def submit_feedback(request: FeedbackRequest, background_tasks: BackgroundTasks):
    """Submit feedback on negotiation results"""
    try:
        logger.info(f"Receiving feedback for negotiation: {request.negotiation_id}")
        
        # Store feedback in memory system (background task)
        background_tasks.add_task(
            store_negotiation_feedback,
            request.negotiation_id,
            request.dict()
        )
        
        return {
            "message": "Feedback received successfully",
            "negotiation_id": request.negotiation_id,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error processing feedback: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Feedback processing error: {str(e)}")

# Get user negotiation history
@app.get("/api/v1/user/{user_id}/negotiations")
async def get_user_negotiations(user_id: str, limit: int = 10):
    """Get negotiation history for a user"""
    try:
        # In a real implementation, you would query the database
        # For now, return a placeholder response
        return {
            "user_id": user_id,
            "negotiations": [],
            "total_count": 0,
            "total_savings": 0.0
        }
        
    except Exception as e:
        logger.error(f"Error retrieving user negotiations: {str(e)}")
        raise HTTPException(status_code=500, detail=f"History retrieval error: {str(e)}")

# Get system statistics
@app.get("/api/v1/stats")
async def get_system_stats():
    """Get system-wide statistics"""
    try:
        stats = {
            "total_negotiations": 0,
            "success_rate": 0.0,
            "average_savings": 0.0,
            "total_savings_generated": 0.0,
            "active_users": 0,
            "system_uptime": "Available",
            "memory_stats": memory_system.get_memory_stats() if memory_system else {}
        }
        
        return stats
        
    except Exception as e:
        logger.error(f"Error retrieving system stats: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Stats retrieval error: {str(e)}")

# Research company endpoint
@app.get("/api/v1/research/{company_name}")
async def research_company(company_name: str):
    """Research a company for negotiation intelligence"""
    try:
        if not negotiation_tools:
            raise HTTPException(status_code=500, detail="Negotiation tools not initialised")
        
        research_result = negotiation_tools.research_company(company_name)
        
        return {
            "company": company_name,
            "research_data": research_result,
            "timestamp": datetime.now().isoformat()
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error researching company: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Research error: {str(e)}")

# Calculate savings endpoint
@app.post("/api/v1/calculate-savings")
async def calculate_savings(
    original_amount: float,
    negotiated_amount: Optional[float] = None,
    target_percentage: Optional[float] = None
):
    """Calculate potential or actual savings"""
    try:
        if not negotiation_tools:
            raise HTTPException(status_code=500, detail="Negotiation tools not initialised")
        
        calculation_result = negotiation_tools.calculate_savings(
            original_amount, negotiated_amount, target_percentage
        )
        
        return {
            "calculation": calculation_result,
            "timestamp": datetime.now().isoformat()
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error calculating savings: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Calculation error: {str(e)}")

# Background task functions
async def store_negotiation_strategy(negotiation_id: str, result: Dict[str, Any], user_id: str):
    """Store negotiation strategy in memory system"""
    try:
        if memory_system:
            strategy_data = {
                'negotiation_id': negotiation_id,
                'user_id': user_id,
                'company': result.get('company', 'Unknown'),
                'bill_type': result.get('bill_type', 'Unknown'),
                'amount': result.get('amount', 0.0),
                'strategy': result.get('negotiation_strategy', ''),
                'confidence_score': result.get('confidence_score', 0.0),
                'execution_mode': result.get('execution_mode', 'unknown')
            }
            
            memory_system.store_negotiation_strategy(strategy_data)
            logger.info(f"Stored strategy for negotiation {negotiation_id}")
            
    except Exception as e:
        logger.error(f"Error storing negotiation strategy: {str(e)}")

async def store_negotiation_feedback(negotiation_id: str, feedback_data: Dict[str, Any]):
    """Store negotiation feedback in memory system"""
    try:
        if memory_system and feedback_data.get('success'):
            success_data = {
                'negotiation_id': negotiation_id,
                'success': feedback_data.get('success', False),
                'actual_savings': feedback_data.get('actual_savings', 0.0),
                'final_amount': feedback_data.get('final_amount', 0.0),
                'notes': feedback_data.get('notes', ''),
                'difficulty_rating': feedback_data.get('difficulty_rating', 3)
            }
            
            memory_system.store_successful_negotiation(success_data)
            logger.info(f"Stored feedback for negotiation {negotiation_id}")
            
    except Exception as e:
        logger.error(f"Error storing negotiation feedback: {str(e)}")

# Error handlers
@app.exception_handler(404)
async def not_found_handler(request, exc):
    return JSONResponse(
        status_code=404,
        content={"detail": "Endpoint not found"}
    )

@app.exception_handler(500)
async def internal_error_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"}
    )

if __name__ == "__main__":
    import uvicorn
    
    # Run the application
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )

