# Dockerfile
FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y netcat-openbsd gcc libpq-dev

# Install Redis tools (optional, for debugging)
RUN apt-get install -y redis-tools

# Install dependencies
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy project files
COPY . .

# Run Django commands (run via docker-compose command)
CMD ["daphne", "chatapp.asgi:application"]
