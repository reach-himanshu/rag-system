# RAG System

A Retrieval-Augmented Generation system with document Q&A and natural-language-to-SQL capabilities. Built with FastAPI, LangChain, React, Qdrant, and PostgreSQL.

## Features

- **Document RAG**: Upload PDF, Word, Excel, and PowerPoint files. Ask natural language questions and get grounded answers with source citations.
- **Text-to-SQL**: Ask business questions in plain English. The system generates SQL, executes it against a Northwind database, and returns results.
- **Intelligent Routing**: A LangGraph-based agent automatically routes queries to document search, SQL, or both.
- **Streaming Responses**: Server-Sent Events for real-time response streaming.
- **LLM Observability**: Full tracing via LangSmith. Infrastructure metrics via Prometheus/Grafana.

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | React 18, TypeScript, Vite, Tailwind CSS |
| Backend | FastAPI, Python 3.12, async SQLAlchemy |
| Agent | LangChain, LangGraph, OpenAI GPT-4o |
| Vector DB | Qdrant |
| Relational DB | PostgreSQL 16 |
| Observability | LangSmith, Prometheus, Grafana |
| IaC | Terraform |
| CI/CD | GitHub Actions |

## Prerequisites

- Docker and Docker Compose
- OpenAI API key
- LangSmith API key (optional, for tracing)

## Quick Start

```bash
# 1. Clone and configure
cp .env.example .env
# Edit .env with your API keys

# 2. Start all services
docker compose -f infra/docker/docker-compose.yml --env-file .env up -d

# 3. Access the application
# Frontend: http://localhost:3000
# Backend API: http://localhost:8000
# API Docs: http://localhost:8000/docs
# Grafana: http://localhost:3001 (admin/admin)
```

## Development

```bash
# Run linters
make lint

# Run tests
make test

# Run security scans
make security-scan

# View logs
make logs
```

## Project Structure

```
RAG_System/
├── backend/          # FastAPI backend with LangChain agents
├── frontend/         # React TypeScript frontend
├── infra/
│   ├── docker/       # Docker Compose and service configs
│   └── terraform/    # Cloud deployment IaC
├── scripts/          # Setup and utility scripts
└── docs/             # Architecture and deployment docs
```

## Architecture

```
React UI → FastAPI → LangGraph Router Agent
                         ├── Document Search (Qdrant)
                         └── SQL Query (PostgreSQL/Northwind)
```

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/health` | Health check |
| POST | `/api/v1/documents/upload` | Upload a document |
| GET | `/api/v1/documents` | List documents |
| POST | `/api/v1/chat` | Send chat message (SSE) |
| GET | `/api/v1/chat/sessions/{id}/messages` | Get session history |

All endpoints except `/health` require an `X-API-Key` header.
