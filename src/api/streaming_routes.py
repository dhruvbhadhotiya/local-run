"""Streaming API routes using Server-Sent Events."""

from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field
from typing import Optional
import asyncio
import time

from src.inference.engine import model_engine
from src.inference.streaming import stream_generate
from src.utils.queue import request_queue
from src.utils.logger import logger


router = APIRouter()


class StreamChatRequest(BaseModel):
    """Streaming chat request model."""
    prompt: str = Field(..., min_length=1, max_length=4096)
    max_tokens: Optional[int] = Field(None, ge=1, le=1024)
    temperature: Optional[float] = Field(None, ge=0.0, le=2.0)
    top_p: Optional[float] = Field(None, ge=0.0, le=1.0)


async def generate_sse_stream(prompt: str, max_tokens: int, temperature: float, top_p: float):
    """
    Generate Server-Sent Events stream for chat responses.
    
    Args:
        prompt: User input prompt
        max_tokens: Maximum tokens to generate
        temperature: Sampling temperature
        top_p: Nucleus sampling parameter
        
    Yields:
        SSE formatted messages
    """
    try:
        # Acquire a slot in the queue
        if not await request_queue.acquire():
            yield f"event: error\ndata: Maximum concurrent users reached. Please try again later.\n\n"
            return
        
        try:
            # Send start event
            yield f"event: start\ndata: Generation started\n\n"
            
            start_time = time.time()
            token_count = 0
            
            # Stream tokens from model
            async for token in stream_generate(
                model=model_engine.model,
                prompt=prompt,
                max_tokens=max_tokens,
                temperature=temperature,
                top_p=top_p
            ):
                token_count += 1
                # Send token as SSE message
                # Escape newlines in token for SSE format
                escaped_token = token.replace('\n', '\\n').replace('\r', '\\r')
                yield f"data: {escaped_token}\n\n"
                
                # Small delay to prevent overwhelming the client
                await asyncio.sleep(0.01)
            
            # Send completion event
            generation_time = time.time() - start_time
            yield f"event: done\ndata: {{\"token_count\": {token_count}, \"generation_time\": {generation_time:.2f}}}\n\n"
            
        finally:
            # Always release the slot
            await request_queue.release()
            
    except Exception as e:
        logger.error(f"Error in SSE stream: {str(e)}")
        yield f"event: error\ndata: {str(e)}\n\n"


@router.post("/api/chat/stream")
async def stream_chat(request: StreamChatRequest):
    """
    Stream chat responses using Server-Sent Events.
    
    Args:
        request: Streaming chat request with prompt and parameters
        
    Returns:
        StreamingResponse: SSE stream of generated tokens
    """
    if not model_engine.model_loaded:
        raise HTTPException(
            status_code=503,
            detail="Model not loaded. Server is starting up."
        )
    
    logger.info(f"Streaming chat request received (prompt_length={len(request.prompt)})")
    
    # Use defaults from settings if not provided
    max_tokens = request.max_tokens or model_engine.get_model_info()["max_tokens"]
    temperature = request.temperature or model_engine.get_model_info()["temperature"]
    top_p = request.top_p or model_engine.get_model_info()["top_p"]
    
    return StreamingResponse(
        generate_sse_stream(request.prompt, max_tokens, temperature, top_p),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no"
        }
    )
