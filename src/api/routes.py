"""API routes for the Campus AI Chat Platform."""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Optional
from src.inference.engine import model_engine
from src.utils.queue import request_queue
from src.utils.logger import logger
import time


router = APIRouter()


class ChatRequest(BaseModel):
    """Chat request model."""
    prompt: str = Field(..., min_length=1, max_length=4096)
    max_tokens: Optional[int] = Field(None, ge=1, le=1024)
    temperature: Optional[float] = Field(None, ge=0.0, le=2.0)
    top_p: Optional[float] = Field(None, ge=0.0, le=1.0)


class ChatResponse(BaseModel):
    """Chat response model."""
    response: str
    prompt_length: int
    response_length: int
    generation_time: float


@router.get("/health")
async def health_check():
    """
    Health check endpoint.
    
    Returns:
        dict: Health status
    """
    return {
        "status": "healthy",
        "model_loaded": model_engine.model_loaded
    }


@router.get("/status")
async def get_status():
    """
    Get server and model status.
    
    Returns:
        dict: Server status information
    """
    model_info = model_engine.get_model_info()
    queue_status = request_queue.get_status()
    
    return {
        "status": "running",
        "model": model_info,
        "queue": queue_status,
        "current_users": queue_status["active_requests"],
        "max_users": queue_status["max_concurrent"]
    }


@router.post("/api/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Generate a chat response from the AI model.
    
    Args:
        request: Chat request with prompt and generation parameters
        
    Returns:
        ChatResponse: Generated response with metadata
    """
    if not model_engine.model_loaded:
        raise HTTPException(
            status_code=503, 
            detail="Model not loaded. Server is starting up."
        )
    
    try:
        # Log request (just metadata, not full prompt for privacy)
        logger.info(f"Chat request received (prompt_length={len(request.prompt)})")
        
        # Generate response
        start_time = time.time()
        response_text = model_engine.generate(
            prompt=request.prompt,
            max_tokens=request.max_tokens,
            temperature=request.temperature,
            top_p=request.top_p
        )
        generation_time = time.time() - start_time
        
        # Log completion
        logger.info(f"Response generated in {generation_time:.2f}s")
        
        return ChatResponse(
            response=response_text,
            prompt_length=len(request.prompt),
            response_length=len(response_text),
            generation_time=generation_time
        )
        
    except Exception as e:
        logger.error(f"Error processing chat request: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
