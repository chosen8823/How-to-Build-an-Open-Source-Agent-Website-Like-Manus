variable "project_id"   { type = string }
variable "region"       { type = string  default = "us-central1" }
variable "location"     { type = string  default = "us-central1" } # for Artifact Registry
variable "service_name" { type = string  default = "botdl-backend" }
variable "artifact_repo_name" { type = string default = "app-repo" }

# CORS configuration
variable "cors_allow_origins" {
  type    = string
  default = "https://app.anchor1llc.com,https://soulphya.io"
}

# Cloud SQL (can skip if not needed yet)
variable "db_tier"      { type = string  default = "db-f1-micro" }
variable "db_version"   { type = string  default = "POSTGRES_15" }
variable "db_name"      { type = string  default = "botdl" }
variable "db_user"      { type = string  default = "appuser" }

# Secrets (optionally set via tfvars; fall back to random)
variable "secret_key" {
  type      = string
  sensitive = true
  default   = ""
}

# AI Model API Keys (with proper sensitivity)
variable "openai_api_key" {
  type      = string
  sensitive = true
  default   = ""
}
variable "anthropic_api_key" {
  type      = string
  sensitive = true
  default   = ""
}
variable "hf_token" {
  type      = string
  sensitive = true
  default   = ""
}
variable "vertex_location" {
  type    = string
  default = "us-central1"
}
