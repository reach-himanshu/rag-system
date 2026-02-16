#!/bin/bash
set -e

echo "=== RAG System Setup ==="

# Copy env file if not exists
if [ ! -f .env ]; then
    echo "Creating .env from .env.example..."
    cp .env.example .env
    echo "Please edit .env with your API keys before starting services."
    exit 1
fi

# Install pre-commit hooks
echo "Installing pre-commit hooks..."
pip install pre-commit
pre-commit install

# Build and start containers
echo "Building Docker images..."
docker compose -f infra/docker/docker-compose.yml --env-file .env build

echo "Starting services..."
docker compose -f infra/docker/docker-compose.yml --env-file .env up -d

# Wait for postgres to be ready
echo "Waiting for PostgreSQL..."
sleep 5

echo ""
echo "=== Setup Complete ==="
echo "Frontend: http://localhost:3000"
echo "Backend:  http://localhost:8000"
echo "API Docs: http://localhost:8000/docs"
echo "Grafana:  http://localhost:3001 (admin/admin)"
