# Base image with Python 3.11
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY src/app.py .
COPY src/download_model.py .
COPY scripts/entrypoint.sh .

# Make entrypoint script executable
RUN chmod +x entrypoint.sh

# Expose port for FastAPI service
EXPOSE 8000

# Set environment variable for model path
ENV MODEL_PATH=/app/model

# Run entrypoint script
ENTRYPOINT ["/app/entrypoint.sh"]

