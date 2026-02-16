# Walkthrough: Phase 7 - Podman Deployment

The system is containerized and compatible with **Podman Desktop**.

## 🐳 Podman Setup

I have updated `docker-compose.yml` with `:Z` labels for SELinux compatibility.

### 1. Prerequisites
- **Podman Desktop** installed and running.
- **Podman Machine** started.

### 2. Configure Environment
Ensure your `.env` file has the API key:
```properties
OPENAI_API_KEY=sk-your-key-here
```

### 3. Start Services
I have installed `podman-compose` in the project's virtual environment. Run:

```powershell
# Activate venv if not already
.venv\Scripts\Activate.ps1

# Run with podman-compose
podman-compose -f infra/docker/docker-compose.yml up --build
```

### 4. Verify Deployment
- **Frontend**: http://localhost:3000
- **Backend Swagger**: http://localhost:8000/docs
- **Qdrant**: http://localhost:6333/dashboard
- **Grafana**: http://localhost:3001
