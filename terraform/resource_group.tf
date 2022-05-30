resource "azurerm_resource_group" "main" {
  name     = "${var.PREFIX}-champions"
  location = var.LOCATION
}
