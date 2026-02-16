terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.90"
    }
    random = {
      source = "hashicorp/random"
    }
  }
  backend "azurerm" {
    # To be filled via -backend-config or init
    key = "permanent.tfstate"
  }
}

resource "random_string" "suffix" {
  length  = 6
  special = false
  upper   = false
}

provider "azurerm" {
  features {}
}

variable "location" {
  default = "eastus2"
}

variable "env" {
  default = "dev"
}

variable "subscription_id" {
    type = string
    description = "Azure Subscription ID"
}

# --- Resource Group ---
resource "azurerm_resource_group" "rg" {
  name     = "rg-rag-${var.env}"
  location = var.location
}

# --- Networking ---
resource "azurerm_virtual_network" "vnet" {
  name                = "vnet-rag-${var.env}"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
  address_space       = ["10.0.0.0/16"]
}

resource "azurerm_subnet" "app_subnet" {
  name                 = "snet-app"
  resource_group_name  = azurerm_resource_group.rg.name
  virtual_network_name = azurerm_virtual_network.vnet.name
  address_prefixes     = ["10.0.1.0/24"]
  
  delegation {
    name = "aca-delegation"
    service_delegation {
      name    = "Microsoft.App/environments"
      actions = ["Microsoft.Network/virtualNetworks/subnets/action"]
    }
  }
}

resource "azurerm_subnet" "db_subnet" {
  name                 = "snet-db"
  resource_group_name  = azurerm_resource_group.rg.name
  virtual_network_name = azurerm_virtual_network.vnet.name
  address_prefixes     = ["10.0.2.0/24"]
  service_endpoints    = ["Microsoft.Storage"]
  
  delegation {
    name = "pg-delegation"
    service_delegation {
      name    = "Microsoft.DBforPostgreSQL/flexibleServers"
      actions = ["Microsoft.Network/virtualNetworks/subnets/join/action"]
    }
  }
}

# --- DNS Zone for Postgres ---
resource "azurerm_private_dns_zone" "pg_dns" {
  name                = "rag.postgres.database.azure.com"
  resource_group_name = azurerm_resource_group.rg.name
}

resource "azurerm_private_dns_zone_virtual_network_link" "pg_dns_link" {
  name                  = "pg-dns-link"
  private_dns_zone_name = azurerm_private_dns_zone.pg_dns.name
  virtual_network_id    = azurerm_virtual_network.vnet.id
  resource_group_name   = azurerm_resource_group.rg.name
}

# --- PostgreSQL Flexible Server ---
resource "random_password" "pg_password" {
  length           = 16
  special          = true
  override_special = "!#$%&*()-_=+[]{}<>:?"
}

resource "azurerm_postgresql_flexible_server" "pg" {
  name                   = "psql-rag-${var.env}-${random_string.suffix.result}"
  resource_group_name    = azurerm_resource_group.rg.name
  location               = azurerm_resource_group.rg.location
  version                = "16"
  delegated_subnet_id    = azurerm_subnet.db_subnet.id
  private_dns_zone_id    = azurerm_private_dns_zone.pg_dns.id
  administrator_login    = "pgadmin"
  administrator_password = random_password.pg_password.result
  sku_name               = "B_Standard_B1ms" # Burstable, cheapest for dev
  storage_mb             = 32768
  public_network_access_enabled = false

  depends_on = [azurerm_private_dns_zone_virtual_network_link.pg_dns_link]
}

resource "azurerm_postgresql_flexible_server_database" "rag_db" {
  name      = "rag_system"
  server_id = azurerm_postgresql_flexible_server.pg.id
  collation = "en_US.utf8"
  charset   = "utf8"
}

resource "azurerm_postgresql_flexible_server_database" "northwind_db" {
  name      = "northwind"
  server_id = azurerm_postgresql_flexible_server.pg.id
  collation = "en_US.utf8"
  charset   = "utf8"
}

# --- Azure Container Registry ---
resource "azurerm_container_registry" "acr" {
  name                = "acrrag${var.env}${random_string.suffix.result}" # Unique name
  resource_group_name = azurerm_resource_group.rg.name
  location            = azurerm_resource_group.rg.location
  sku                 = "Basic"
  admin_enabled       = true # Simplify pull for now, or use Managed Identity
}

# --- Storage Account (for Qdrant & File Shares) ---
resource "azurerm_storage_account" "sa" {
  name                     = "strag${var.env}${random_string.suffix.result}"
  resource_group_name      = azurerm_resource_group.rg.name
  location                 = azurerm_resource_group.rg.location
  account_tier             = "Standard"
  account_replication_type = "LRS"
}

resource "azurerm_storage_share" "qdrant_share" {
  name                 = "qdrantdata"
  storage_account_name = azurerm_storage_account.sa.name
  quota                = 5
}

# --- Key Vault ---
data "azurerm_client_config" "current" {}

resource "azurerm_key_vault" "kv" {
  name                        = "kv-rag-${var.env}-${random_string.suffix.result}"
  location                    = azurerm_resource_group.rg.location
  resource_group_name         = azurerm_resource_group.rg.name
  enabled_for_disk_encryption = true
  tenant_id                   = data.azurerm_client_config.current.tenant_id
  soft_delete_retention_days  = 7
  purge_protection_enabled    = false

  sku_name = "standard"

  access_policy {
    tenant_id = data.azurerm_client_config.current.tenant_id
    object_id = data.azurerm_client_config.current.object_id

    key_permissions = [
      "Get",
    ]

    secret_permissions = [
      "Get", "List", "Set", "Delete", "Purge", "Recover"
    ]

    storage_permissions = [
      "Get",
    ]
  }
}

# --- Store Secrets in Key Vault ---
resource "azurerm_key_vault_secret" "pg_pass" {
  name         = "Postgres-Admin-Password"
  value        = random_password.pg_password.result
  key_vault_id = azurerm_key_vault.kv.id
}

resource "azurerm_key_vault_secret" "pg_host" {
  name         = "Postgres-Host"
  value        = azurerm_postgresql_flexible_server.pg.fqdn
  key_vault_id = azurerm_key_vault.kv.id
}

# --- Outputs ---
output "resource_group_name" {
  value = azurerm_resource_group.rg.name
}

output "acr_login_server" {
  value = azurerm_container_registry.acr.login_server
}

output "acr_admin_username" {
  value = azurerm_container_registry.acr.admin_username
}

output "acr_admin_password" {
  value = azurerm_container_registry.acr.admin_password
  sensitive = true
}

output "app_subnet_id" {
  value = azurerm_subnet.app_subnet.id
}

output "storage_account_name" {
  value = azurerm_storage_account.sa.name
}

output "storage_account_key" {
  value = azurerm_storage_account.sa.primary_access_key
  sensitive = true
}

output "key_vault_id" {
  value = azurerm_key_vault.kv.id
}

output "key_vault_uri" {
    value = azurerm_key_vault.kv.vault_uri
}

output "postgres_fqdn" {
  value = azurerm_postgresql_flexible_server.pg.fqdn
}
