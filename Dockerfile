# Build stage
FROM python:3.11-slim as builder

WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir --user -r requirements.txt

# Production stage
FROM python:3.11-slim

WORKDIR /app

# Create non-root user for security
RUN useradd --create-home --shell /bin/bash appuser

# Copy installed packages from builder
COPY --from=builder /root/.local /home/appuser/.local

# Ensure scripts in .local are usable
ENV PATH=/home/appuser/.local/bin:$PATH

# Copy application code
COPY --chown=appuser:appuser *.py ./
COPY --chown=appuser:appuser story.proto ./

# Switch to non-root user
USER appuser

# Expose gRPC port
EXPOSE 50051

# Health check using grpc_health_probe (optional, for K8s)
# HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
#     CMD grpc_health_probe -addr=:50051 || exit 1

# Run the gRPC server
CMD ["python", "server.py"]
