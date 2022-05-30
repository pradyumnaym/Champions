variable "PREFIX" {
  type = string
}

variable "LOCATION" {
  type = string
}

variable "REGISTRY_SERVER_URL" {
  type = string
}

variable "REGISTRY_SERVER_USERNAME" {
  type = string
}

variable "REGISTRY_SERVER_PASSWORD" {
  type      = string
  sensitive = true
}

variable "APPINSIGHTS_INSTRUMENTATIONKEY" {
  type      = string
  sensitive = true
}
variable "APPLICATIONINSIGHTS_CONNECTION_STRING" {
  type      = string
  sensitive = true
}

variable "DB_CONNECTION_STRING" {
  type      = string
  sensitive = true
}
