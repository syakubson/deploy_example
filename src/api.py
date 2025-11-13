"""
FastAPI service endpoints for Qwen3 text generation.
"""

import time
from contextlib import asynccontextmanager
from typing import Optional

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from .model_manager import model_manager


class GenerateRequest(BaseModel):
    """Request model for text generation."""

    message: str
    max_new_tokens: Optional[int] = 32768


class GenerateResponse(BaseModel):
    """Response model for text generation."""

    thinking: str
    content: str
    processing_time: float


class HealthResponse(BaseModel):
    """Response model for health check."""

    status: str
    model_loaded: bool


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Load model on startup, cleanup on shutdown."""
    # Startup
    model_manager.load_model()
    yield
    # Shutdown
    print("Shutting down service")


# Create FastAPI app
app = FastAPI(
    title="Qwen3 Text Generation Service",
    description="FastAPI service with Qwen3-0.6B model for text generation",
    version="1.0.0",
    lifespan=lifespan,
)


@app.post("/generate", response_model=GenerateResponse)
async def generate(request: GenerateRequest):
    """
    Generate text based on input message.
    Returns both thinking process and final content.
    """
    if not model_manager.is_model_loaded():
        raise HTTPException(status_code=503, detail="Model not loaded")

    try:
        start_time = time.time()
        thinking, content = model_manager.generate_text(request.message, request.max_new_tokens)
        processing_time = time.time() - start_time

        return GenerateResponse(thinking=thinking, content=content, processing_time=processing_time)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Generation failed: {str(e)}")


@app.get("/health", response_model=HealthResponse)
async def health():
    """Health check endpoint to verify service status."""
    return HealthResponse(
        status="healthy" if model_manager.is_model_loaded() else "unhealthy",
        model_loaded=model_manager.is_model_loaded(),
    )
