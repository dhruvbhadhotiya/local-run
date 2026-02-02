"""Main server application for the Campus AI Chat Platform."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
import uvicorn

from src.api.routes import router
from src.api.streaming_routes import router as streaming_router
from src.inference.engine import model_engine
from src.utils.config import settings
from src.utils.logger import logger


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan context manager for startup and shutdown events.
    
    Args:
        app: FastAPI application instance
    """
    # Startup
    logger.info("=" * 60)
    logger.info("Campus AI Chat Platform - Starting Up")
    logger.info("=" * 60)
    logger.info(f"Server: {settings.host}:{settings.port}")
    logger.info(f"Model: {settings.hf_model}")
    logger.info("Loading model... This may take a few minutes.")
    
    # Load model
    success = model_engine.load_model()
    
    if success:
        logger.info("✓ Model loaded successfully!")
        logger.info(f"Ready to accept connections at http://{settings.host}:{settings.port}")
    else:
        logger.warning("✗ Model failed to load. Server will start but won't accept chat requests.")
        logger.warning("Please check model path and configuration.")
    
    logger.info("=" * 60)
    
    yield
    
    # Shutdown
    logger.info("Shutting down server...")
    logger.info("Goodbye!")


# Create FastAPI application
app = FastAPI(
    title="Campus AI Chat Platform",
    description="Local AI chat platform for educational use",
    version="1.0.0",
    lifespan=lifespan
)

# Add CORS middleware for local network access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins on local network
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(router)
app.include_router(streaming_router)

# Mount static files for frontend (will be added in Phase 3)
# app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")


def main():
    """Run the server."""
    uvicorn.run(
        "server:app",
        host=settings.host,
        port=settings.port,
        log_level=settings.log_level.lower(),
        reload=False  # Disable reload in production
    )


if __name__ == "__main__":
    main()
