terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.90"
    }
  }
  backend "azurerm" {
    key = "ephemeral.tfstate"
  }
}

provider "azurerm" {
  features {}
}

variable "location" { default = "eastus2" }
variable "env" { default = "dev" }

# --- Remote State (Read Permanent Stack) ---
data "terraform_remote_state" "permanent" {
  backend = "azurerm"
  config = {
    resource_group_name  = "rg-rag-tfstate" # MUST MATCH BOOTSTRAP
    storage_account_name = "sttfstatehv3yil" # UPDATED
    container_name       = "tfstate"
    key                  = "permanent.tfstate"
  }
}

locals {
  rg_name       = data.terraform_remote_state.permanent.outputs.resource_group_name
  app_subnet_id = data.terraform_remote_state.permanent.outputs.app_subnet_id
  acr_server    = data.terraform_remote_state.permanent.outputs.acr_login_server
  acr_user      = data.terraform_remote_state.permanent.outputs.acr_admin_username
  acr_pass      = data.terraform_remote_state.permanent.outputs.acr_admin_password
  sa_name       = data.terraform_remote_state.permanent.outputs.storage_account_name
  sa_key        = data.terraform_remote_state.permanent.outputs.storage_account_key
  pg_host       = data.terraform_remote_state.permanent.outputs.postgres_fqdn
  api_key       = data.terraform_remote_state.permanent.outputs.api_key
  kv_id         = data.terraform_remote_state.permanent.outputs.key_vault_id
}

data "azurerm_key_vault_secret" "openai_key" {
  name         = "OpenAI-API-Key"
  key_vault_id = local.kv_id
}

# --- Log Analytics Workspace ---
resource "azurerm_log_analytics_workspace" "law" {
  name                = "law-rag-${var.env}"
  location            = var.location
  resource_group_name = local.rg_name
  sku                 = "PerGB2018"
  retention_in_days   = 30
}

# --- Container Apps Environment ---
resource "azurerm_container_app_environment" "aca_env" {
  name                       = "aca-env-rag-${var.env}"
  location                   = var.location
  resource_group_name        = local.rg_name
  log_analytics_workspace_id = azurerm_log_analytics_workspace.law.id
  infrastructure_subnet_id   = local.app_subnet_id
}

# --- Storage Mount (Qdrant) ---
resource "azurerm_container_app_environment_storage" "qdrant_storage" {
  name                         = "qdrant-mount"
  container_app_environment_id = azurerm_container_app_environment.aca_env.id
  account_name                 = local.sa_name
  access_key                   = local.sa_key
  share_name                   = "qdrantdata"
  access_mode                  = "ReadWrite"
}

# --- Container App: Qdrant ---
resource "azurerm_container_app" "qdrant" {
  name                         = "ca-qdrant-${var.env}"
  container_app_environment_id = azurerm_container_app_environment.aca_env.id
  resource_group_name          = local.rg_name
  revision_mode                = "Single"

  template {
    container {
      name   = "qdrant"
      image  = "qdrant/qdrant:v1.12.1"
      cpu    = 0.5
      memory = "1Gi"
      
      volume_mounts {
        name = "qdrant-data"
        path = "/qdrant/storage"
      }
    }
    volume {
      name         = "qdrant-data"
      storage_name = azurerm_container_app_environment_storage.qdrant_storage.name
      storage_type = "AzureFile"
    }
  }
  
  ingress {
    external_enabled = false
    target_port      = 6333
    transport        = "tcp"
    traffic_weight {
      percentage = 100
      latest_revision = true
    }
  }
}

# --- Container App: Backend ---
resource "azurerm_container_app" "backend" {
  name                         = "ca-backend-${var.env}"
  container_app_environment_id = azurerm_container_app_environment.aca_env.id
  resource_group_name          = local.rg_name
  revision_mode                = "Single"

  registry {
    server               = local.acr_server
    username             = local.acr_user
    password_secret_name = "acr-password"
  }

  secret {
    name  = "acr-password"
    value = local.acr_pass
  }

  secret {
    name  = "rag-api-key"
    value = local.api_key
  }

  secret {
    name  = "openai-api-key"
    value = data.azurerm_key_vault_secret.openai_key.value
  }

  template {
    min_replicas = 0
    max_replicas = 1

    container {
      name   = "backend"
      image  = "${local.acr_server}/backend:latest"
      cpu    = 0.5
      memory = "1Gi"
      
      env {
        name  = "POSTGRES_HOST"
        value = local.pg_host
      }
      env {
        name  = "QDRANT_HOST"
        value = azurerm_container_app.qdrant.name # Internal DNS
      }
      env {
        name        = "API_KEY"
        secret_name = "rag-api-key"
      }
      env {
        name        = "OPENAI_API_KEY"
        secret_name = "openai-api-key"
      }
      # Secrets should be pulled from KeyVault or passed as secrets.
      # Simplified here for brevity.
    }
  }

  ingress {
    external_enabled = true
    target_port      = 8000
    traffic_weight {
      percentage = 100
      latest_revision = true
    }
  }
}

# --- Container App: Frontend ---
resource "azurerm_container_app" "frontend" {
  name                         = "ca-frontend-${var.env}"
  container_app_environment_id = azurerm_container_app_environment.aca_env.id
  resource_group_name          = local.rg_name
  revision_mode                = "Single"

  registry {
    server               = local.acr_server
    username             = local.acr_user
    password_secret_name = "acr-password"
  }

  secret {
    name  = "acr-password"
    value = local.acr_pass
  }

  secret {
    name  = "rag-api-key"
    value = local.api_key
  }

  template {
    min_replicas = 0
    max_replicas = 1

    container {
      name   = "frontend"
      image  = "${local.acr_server}/frontend:latest"
      cpu    = 0.5
      memory = "1Gi"
      
      env {
        name  = "VITE_API_URL"
        value = "https://${azurerm_container_app.backend.ingress[0].fqdn}/api/v1"
      }
      env {
        name        = "VITE_API_KEY"
        secret_name = "rag-api-key"
      }
    }
  }

  ingress {
    external_enabled = true
    target_port      = 3000
    traffic_weight {
      percentage = 100
      latest_revision = true
    }
  }
}
