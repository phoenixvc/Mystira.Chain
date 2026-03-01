# Mystira Chain Dockerfile
# Multi-stage build for Mystira gRPC service (Python)
# Migrated from infra/docker/chain/ per ADR-0019

# Build stage
FROM python:3.14-slim AS builder

WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Production stage
FROM python:3.14-slim AS production

WORKDIR /app

# Create non-root user with specific IDs for K8s security context
RUN groupadd -g 10000 chain && \
    useradd -u 10000 -g chain -s /bin/sh chain

# Install runtime dependencies and grpc_health_probe
RUN apt-get update && apt-get install -y --no-install-recommends \
    tini \
    curl \
    && rm -rf /var/lib/apt/lists/* \
    # Install grpc_health_probe for Kubernetes health checks
    && curl -fsSL https://github.com/grpc-ecosystem/grpc-health-probe/releases/download/v0.4.25/grpc_health_probe-linux-amd64 \
       -o /usr/local/bin/grpc_health_probe \
    && chmod +x /usr/local/bin/grpc_health_probe

# Copy Python packages from builder
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages

# Copy application code (submodule context - copies from repo root)
COPY *.py ./
COPY story.proto ./

# Create data directory
RUN mkdir -p /data && chown -R chain:chain /data /app

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV CHAIN_DATA_DIR=/data

# Switch to non-root user
USER chain

# Expose gRPC port
EXPOSE 50051

# Health check using grpc_health_probe (gRPC native health checking)
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD grpc_health_probe -addr=:50051 || exit 1

# Use tini as init
ENTRYPOINT ["/usr/bin/tini", "--"]

# Start the gRPC server
CMD ["python", "server.py"]
