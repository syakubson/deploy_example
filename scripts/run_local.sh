#!/bin/bash
# Script to run the service locally with the local model

export MODEL_PATH=./Qwen3-0.6B
export PYTHONPATH=.

echo "Starting Qwen3 service locally..."
echo "Model path: $MODEL_PATH"
echo ""
echo "The service will be available at:"
echo "  - Gradio UI: http://localhost:8000"
echo "  - API Docs: http://localhost:8000/docs"
echo "  - Health: http://localhost:8000/health"
echo ""

uvicorn src.app:app --host 0.0.0.0 --port 8000
