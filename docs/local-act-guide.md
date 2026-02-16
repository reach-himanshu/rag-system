# Local CI with `act`

Run GitHub Actions locally using Docker. This catches Linux-specific errors (case sensitivity) and tests workflows before pushing!

## 1. Installation
Run in PowerShell (Admin):
```powershell
choco install act-cli
# OR
winget install nektos.act
```

## 2. Secrets Configuration
Create a file named `.secrets` in the project root. **DO NOT COMMIT THIS FILE.**

```dotenv
# Azure Service Principal (From your initial setup)
AZURE_CREDENTIALS='{"clientId": "...", "clientSecret": "...", "subscriptionId": "...", "tenantId": "..."}'
AZURE_SUBSCRIPTION_ID=...

# Terraform State (From bootstrap output)
TF_STATE_STORAGE_ACCOUNT=sttfstatehv3yil

# OpenAI (For tests)
OPENAI_API_KEY=sk-...
```

## 3. Usage

### Run All Checks (Lint + Test)
```bash
act push -j lint -j test-backend -j test-frontend --secret-file .secrets
```

### Run Specific Job
```bash
act -j test-backend --secret-file .secrets
```

### Debugging
If `act` fails with "Docker not found", ensure Docker Desktop is running!
