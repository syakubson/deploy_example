#!/bin/bash
set -e

echo "Starting Qwen3 service entrypoint..."

# Download model from S3 if not already present
echo "Checking for model files..."
python /app/download_model.py

# Start FastAPI service with Uvicorn
echo "Starting FastAPI service on port 8000..."
exec uvicorn app:app --host 0.0.0.0 --port 8000

