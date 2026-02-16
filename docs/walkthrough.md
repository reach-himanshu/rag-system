# RAG System Walkthrough

## 🚀 Getting Started

### 1. Requirements
- Docker or Podman Desktop
- OpenAI API Key

### 2. Startup
Run the following command to start the full stack (Frontend, Backend, Database, Vector DB, Monitoring):

```bash
# Start everything in background
podman-compose -f infra/docker/docker-compose.yml up -d
```

### 3. Access Points
- **Frontend (Chat UI)**: [http://localhost:3000](http://localhost:3000)
- **Backend API Docs**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **Grafana (Monitoring)**: [http://localhost:3001](http://localhost:3001) (User: `admin`, Pass: `admin`)

## 📚 Using the System

### Uploading Documents (RAG)
1. Go to the API Docs: [http://localhost:8000/docs](http://localhost:8000/docs)
2. Find `POST /api/v1/documents/upload`.
3. Click **Try it out**.
4. Upload a PDF (e.g., `Python-for-Data-Analysis.pdf`).
5. Execute.

### Chatting
Go to [http://localhost:3000](http://localhost:3000).

- **Ask General Questions**: "What is Python?" (General Chat 🤖)
- **Ask Document Questions**: "Tell me about IPython from the document?" (RAG 📄)
  - *Note: The system aggressively checks documents for technical terms.*
- **Ask Data Questions**: "How many products do we have?" (SQL 🛢️)

## 🛠️ Troubleshooting

- **"Connection Refused"**: Ensure all containers are running (`podman ps`).
- **"Database raguser does not exist"**: This is a benign healthcheck warning during startup; it resolves itself.
- **"Bot Icon vs Page Icon"**: The system uses icons to indicate the source. If it shows a Bot icon but cites the document in the text, it successfully used the RAG pipeline.

### Monitoring Verification
To check if logs and metrics are working:
1.  **Backend Metrics**: Visit [http://localhost:8000/metrics](http://localhost:8000/metrics) to see raw Prometheus metrics.
2.  **Prometheus Targets**: Visit [http://localhost:9090/targets](http://localhost:9090/targets) and check if `rag-backend` is **UP**.
3.  **Grafana**: Visit [http://localhost:3001](http://localhost:3001), log in (admin/admin), add Prometheus data source, and explore `http_requests_total`.

3.  **Grafana**: Visit [http://localhost:3001](http://localhost:3001), log in (admin/admin), add Prometheus data source, and explore `http_requests_total`.

## ☁️ Deploying to Azure

### Prerequisities
-   Azure CLI (`az login`)
-   Terraform
-   GitHub Repo

### 1. One-Time Setup (Foundation)
Run this manually to create the "State Backend" and "Image Registry".

**Step A: Bootstrap (State Storage)**
```bash
cd infra/terraform/bootstrap
az login
terraform init
terraform apply
# COPY the output 'storage_account_name' -> You need this!
```

**Step B: Permanent Stack (Database, Registry, KeyVault)**
```bash
cd ../permanent
# Edit main.tf or pass backend config
terraform init -backend-config="storage_account_name=<YOUR_STORAGE_ACCOUNT>" -backend-config="resource_group_name=rg-rag-tfstate" -backend-config="container_name=tfstate" -backend-config="key=permanent.tfstate"
terraform apply
# COPY the output 'acr_login_server' and 'acr_admin_password' -> You need these!
```

### 2. Connect GitHub Actions
Go to your GitHub Repo > Settings > Secrets and add:

-   `AZURE_CLIENT_ID`, `AZURE_TENANT_ID`, `AZURE_SUBSCRIPTION_ID` (Use `az ad sp create-for-rbac` to generate these).
-   `TF_STATE_STORAGE_ACCOUNT`: The name from Step A.
-   `ACR_NAME`: The name of the registry (e.g. `acrragdev`).

### 3. Deploy
Just **git push** to the `main` branch! The Action will:
1.  Build Docker images -> Push to ACR.
2.  Deploy `ephemeral` stack (Container Apps) using the new images.

## 🔄 Updates
The backend supports hot-reloading. If you edit code in `backend/app`, it updates instantly!
