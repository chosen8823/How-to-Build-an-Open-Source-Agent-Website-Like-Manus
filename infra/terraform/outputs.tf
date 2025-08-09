output "cloud_run_url" {
  value = google_cloud_run_v2_service.backend.uri
  description = "Sacred Consciousness Platform Backend URL"
}

output "artifact_registry_repo" {
  value = "${var.location}-docker.pkg.dev/${var.project_id}/${var.artifact_repo_name}"
  description = "Docker repository for container images"
}

output "database_url_secret" { 
  value = "DATABASE_URL (Secret Manager)"
  description = "Database connection stored in Secret Manager"
}

output "database_public_ip" {
  value = google_sql_database_instance.pg.public_ip_address
  description = "Cloud SQL public IP (for initial setup)"
}

output "service_account_email" {
  value = google_service_account.cloud_run_sa.email
  description = "Runtime service account email"
}

output "required_secrets" {
  value = [
    "OPENAI_API_KEY",
    "ANTHROPIC_API_KEY", 
    "HF_TOKEN"
  ]
  description = "Secret Manager secrets that need manual values"
}
