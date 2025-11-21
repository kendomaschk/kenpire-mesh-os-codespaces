FROM python:3.12-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY src/ ./src/
COPY setup.py .
COPY config/ ./config/

# Install application
RUN pip install -e .

# Create non-root user
RUN useradd -m -u 1001 kenpire && \
    chown -R kenpire:kenpire /app && \
    mkdir -p /app/logs && \
    chown kenpire:kenpire /app/logs

USER kenpire

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD curl -f http://localhost:8080/health || exit 1

EXPOSE 8080

CMD ["python", "-m", "kenpire.main"]