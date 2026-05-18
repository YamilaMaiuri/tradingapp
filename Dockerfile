FROM --platform=linux/amd64 python:3.11-slim

WORKDIR /app

# Copy requirements first for better caching
COPY requirements_api.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements_api.txt

# Copy application code
COPY api_server.py .

# Expose port
EXPOSE 8080

# Run with gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "--workers", "2", "--timeout", "120", "--access-logfile", "-", "--error-logfile", "-", "api_server:app"]

# Made with Bob
