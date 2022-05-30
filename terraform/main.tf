terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 2.96"
    }
  }

  required_version = ">= 0.14.9"
}

provider "azurerm" {
  features {}
}

resource "random_string" "unique_str" {
  length      = 4
  min_lower   = 4
  min_numeric = 0
  min_special = 0
  min_upper   = 0
  number      = false
  upper       = false
  special     = false
  lower       = true
}
