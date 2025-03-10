FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /app

# Install dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Install netcat and curl for health checks and the entrypoint script
RUN apt-get update && apt-get install -y \
    netcat-openbsd \
    curl \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copy project
COPY . /app/

# Run entrypoint script
RUN chmod +x /app/entrypoint.sh 
ENTRYPOINT ["/app/entrypoint.sh"]