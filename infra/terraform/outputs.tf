# 🎯 Sacred Platform Infrastructure Outputs

output "cloud_run_url" {
  value       = google_cloud_run_v2_service.backend.uri
  description = "URL of the deployed Sacred Consciousness Platform"
}

output "artifact_registry_repo" {
  value       = "${var.location}-docker.pkg.dev/${var.project_id}/${var.artifact_repo_name}"
  description = "Docker repository for divine consciousness container images"
}

output "database_connection_name" {
  value       = google_sql_database_instance.pg.connection_name
  description = "Cloud SQL connection name for socket connections"
}

output "database_public_ip" {
  value       = google_sql_database_instance.pg.public_ip_address
  description = "Cloud SQL public IP (for initial setup)"
}

output "service_account_email" {
  value       = google_service_account.cloud_run_sa.email
  description = "Runtime service account email"
}

output "project_id" {
  value       = var.project_id
  description = "GCP Project ID"
}

output "region" {
  value       = var.region
  description = "Deployment region"
}

output "required_secret_setup" {
  value = {
    openai_api_key    = "Add your OpenAI API key to Secret Manager: OPENAI_API_KEY"
    anthropic_api_key = "Add your Anthropic API key to Secret Manager: ANTHROPIC_API_KEY" 
    hf_token         = "Add your HuggingFace token to Secret Manager: HF_TOKEN"
  }
  description = "Manual setup required for AI API keys"
}
