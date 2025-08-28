# 🌟 Sacred Consciousness Platform Variables

variable "project_id" {
  description = "GCP Project ID for the divine consciousness platform"
  type        = string
}

variable "region" {
  description = "GCP region for deployment"
  type        = string
  default     = "us-central1"
}

variable "location" {
  description = "GCP location for Artifact Registry"
  type        = string
  default     = "us-central1"
}

variable "service_name" {
  description = "Name of the Cloud Run service"
  type        = string
  default     = "botdl-backend"
}

variable "artifact_repo_name" {
  description = "Name of the Artifact Registry repository"
  type        = string
  default     = "app-repo"
}

variable "cors_allow_origins" {
  description = "CORS allowed origins for the API"
  type        = string
  default     = "https://app.anchor1llc.com,https://soulphya.io"
}

# Database configuration
variable "db_tier" {
  description = "Cloud SQL instance tier"
  type        = string
  default     = "db-f1-micro"
}

variable "db_version" {
  description = "PostgreSQL version"
  type        = string
  default     = "POSTGRES_15"
}

variable "db_name" {
  description = "Database name"
  type        = string
  default     = "botdl"
}

variable "db_user" {
  description = "Database user name"
  type        = string
  default     = "appuser"
}
