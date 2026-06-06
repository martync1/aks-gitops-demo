# 1. Tell Terraform to use the Azure Provider
terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.0"
    }
  }
}

provider "azurerm" {
  features {}
}

# 2. Create an Azure Resource Group (a container for our infrastructure)
resource "azurerm_resource_group" "rg" {
  name     = "rg-gitops-demo"
  location = "East US"
}

# 3. Create the AKS Cluster
resource "azurerm_kubernetes_cluster" "aks" {
  name                = "aks-gitops-cluster"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
  dns_prefix          = "gitops-k8s"
  sku_tier            = "Free" # Avoids the $70/month uptime SLA charge

  default_node_pool {
    name       = "default"
    node_count = 1             # Only 1 machine to keep it cheap
    vm_size    = "Standard_B2s" # 2 vCPUs, 4GB RAM - perfect for testing
  }

  identity {
    type = "SystemAssigned"
  }
}

# 4. Output the command to connect to your new cluster
output "connect_command" {
  value = "az aks get-credentials --resource-group ${azurerm_resource_group.rg.name} --name ${azurerm_kubernetes_cluster.aks.name}"
}
