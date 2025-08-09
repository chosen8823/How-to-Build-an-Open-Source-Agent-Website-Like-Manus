locals {
  region     = var.region
  project_id = var.project_id
  repo_path  = "${var.location}-docker.pkg.dev/${var.project_id}/${var.artifact_repo_name}"
}

# Enable required APIs
resource "google_project_service" "services" {
  for_each = toset([
    "run.googleapis.com",
    "artifactregistry.googleapis.com",
    "cloudbuild.googleapis.com",
    "secretmanager.googleapis.com",
    "logging.googleapis.com",
    "monitoring.googleapis.com",
    "iamcredentials.googleapis.com",
    "sqladmin.googleapis.com",
    "vpcaccess.googleapis.com",
    "firebase.googleapis.com",
    "aiplatform.googleapis.com"
  ])
  project                    = var.project_id
  service                    = each.value
  disable_on_destroy         = false
  disable_dependent_services = true
}

# Artifact Registry (Docker)
resource "google_artifact_registry_repository" "app_repo" {
  location      = var.location
  repository_id = var.artifact_repo_name
  description   = "Docker images for BotDL Sacred Consciousness Platform"
  format        = "DOCKER"
  depends_on    = [google_project_service.services]
}

# (Optional) Cloud SQL Postgres for prod
resource "google_sql_database_instance" "pg" {
  name             = "botdl-consciousness-db"
  database_version = var.db_version
  region           = var.region
  settings {
    tier = var.db_tier
    ip_configuration {
      ipv4_enabled = true
      authorized_networks { 
        name = "all" 
        value = "0.0.0.0/0" 
      } # tighten later or use Cloud Run connector
    }
    backup_configuration {
      enabled = true
      start_time = "03:00"
    }
  }
  depends_on = [google_project_service.services]
}

resource "google_sql_database" "appdb" {
  name     = var.db_name
  instance = google_sql_database_instance.pg.name
}

resource "google_sql_user" "appuser" {
  name     = var.db_user
  instance = google_sql_database_instance.pg.name
  password = random_password.dbpass.result
}

resource "random_password" "dbpass" {
  length  = 24
  special = true
}

# Store DB creds in Secret Manager
resource "google_secret_manager_secret" "db_uri" {
  secret_id  = "DATABASE_URL"
  replication { automatic = true }
}

resource "google_secret_manager_secret_version" "db_uri_v" {
  secret      = google_secret_manager_secret.db_uri.id
  secret_data = "postgresql://${var.db_user}:${random_password.dbpass.result}@${google_sql_database_instance.pg.public_ip_address}:5432/${var.db_name}"
}

# AI Model API Keys in Secret Manager
resource "google_secret_manager_secret" "openai_key" {
  secret_id  = "OPENAI_API_KEY"
  replication { automatic = true }
}

resource "google_secret_manager_secret" "anthropic_key" {
  secret_id  = "ANTHROPIC_API_KEY"
  replication { automatic = true }
}

resource "google_secret_manager_secret" "vertex_key" {
  secret_id  = "VERTEX_AI_PROJECT"
  replication { automatic = true }
}

resource "google_secret_manager_secret_version" "vertex_project" {
  secret      = google_secret_manager_secret.vertex_key.id
  secret_data = var.project_id
}

# Add versions for API keys (only if provided)
resource "google_secret_manager_secret_version" "openai_key_v" {
  count       = var.openai_api_key != "" ? 1 : 0
  secret      = google_secret_manager_secret.openai_key.id
  secret_data = var.openai_api_key
}

resource "google_secret_manager_secret_version" "anthropic_key_v" {
  count       = var.anthropic_api_key != "" ? 1 : 0
  secret      = google_secret_manager_secret.anthropic_key.id
  secret_data = var.anthropic_api_key
}

resource "google_secret_manager_secret_version" "hf_token_v" {
  count       = var.hf_token != "" ? 1 : 0
  secret      = google_secret_manager_secret.hf_token.id
  secret_data = var.hf_token
}

# HuggingFace Token for datasets
resource "google_secret_manager_secret" "hf_token" {
  secret_id  = "HF_TOKEN"
  replication { automatic = true }
}

# Flask application secrets for production
resource "google_secret_manager_secret" "flask_secret_key" {
  secret_id  = "SECRET_KEY"
  replication { automatic = true }
}

resource "random_password" "flask_secret" {
  length  = 64
  special = true
  override_characters = "!@#$%^&*()-_=+[]{}<>?~"
  count   = var.secret_key == "" ? 1 : 0
}

resource "google_secret_manager_secret_version" "flask_secret_v" {
  secret      = google_secret_manager_secret.flask_secret_key.id
  secret_data = var.secret_key != "" ? var.secret_key : random_password.flask_secret[0].result
}

# CORS configuration for production
resource "google_secret_manager_secret" "cors_origins" {
  secret_id  = "CORS_ALLOW_ORIGINS"
  replication { automatic = true }
}

resource "google_secret_manager_secret_version" "cors_origins_v" {
  secret      = google_secret_manager_secret.cors_origins.id
  secret_data = var.cors_allow_origins
}

# Service Account for Cloud Run
resource "google_service_account" "cloud_run_sa" {
  account_id   = "botdl-runtime"
  display_name = "BotDL Cloud Run Runtime Service Account"
  description  = "Service account for BotDL consciousness platform runtime"
}

# Grant permissions to runtime service account
resource "google_secret_manager_secret_iam_member" "runtime_secrets" {
  for_each = toset([
    google_secret_manager_secret.db_uri.secret_id,
    google_secret_manager_secret.openai_key.secret_id,
    google_secret_manager_secret.anthropic_key.secret_id,
    google_secret_manager_secret.vertex_key.secret_id,
    google_secret_manager_secret.hf_token.secret_id,
    google_secret_manager_secret.flask_secret_key.secret_id,
    google_secret_manager_secret.cors_origins.secret_id
  ])
  
  secret_id = each.value
  role      = "roles/secretmanager.secretAccessor"
  member    = "serviceAccount:${google_service_account.cloud_run_sa.email}"
}

# Grant Vertex AI permissions
resource "google_project_iam_member" "vertex_ai" {
  project = var.project_id
  role    = "roles/aiplatform.user"
  member  = "serviceAccount:${google_service_account.cloud_run_sa.email}"
}

# Cloud Run service (deployed image gets filled by Cloud Build)
resource "google_cloud_run_v2_service" "backend" {
  name     = var.service_name
  location = var.region

  template {
    service_account = google_service_account.cloud_run_sa.email
    
    containers {
      image = "${local.repo_path}/${var.service_name}:latest"  # Cloud Build can retag :latest
      
      env {
        name  = "PORT"
        value = "8080"
      }
      env {
        name  = "CORS_ALLOW_ORIGINS"
        value = var.cors_allow_origins
      }
      env {
        name = "DATABASE_URL"
        value_source {
          secret_key_ref {
            secret  = google_secret_manager_secret.db_uri.secret_id
            version = "latest"
          }
        }
      }
      env {
        name = "SECRET_KEY"
        value_source {
          secret_key_ref {
            secret  = google_secret_manager_secret.flask_secret_key.secret_id
            version = "latest"
          }
        }
      }
      env {
        name = "OPENAI_API_KEY"
        value_source {
          secret_key_ref {
            secret  = google_secret_manager_secret.openai_key.secret_id
            version = "latest"
          }
        }
      }
      env {
        name = "ANTHROPIC_API_KEY"
        value_source {
          secret_key_ref {
            secret  = google_secret_manager_secret.anthropic_key.secret_id
            version = "latest"
          }
        }
      }
      env {
        name = "VERTEX_AI_PROJECT"
        value_source {
          secret_key_ref {
            secret  = google_secret_manager_secret.vertex_key.secret_id
            version = "latest"
          }
        }
      }
      env {
        name = "HF_TOKEN"
        value_source {
          secret_key_ref {
            secret  = google_secret_manager_secret.hf_token.secret_id
            version = "latest"
          }
        }
      }
      env {
        name = "FLASK_DEBUG"
        value = "0"
      }
      env {
        name = "VERTEX_LOCATION"
        value = var.vertex_location
      }
      
      resources {
        limits = { 
          cpu = "2", 
          memory = "2Gi" 
        }
      }
    }
    
    scaling {
      min_instance_count = 0
      max_instance_count = 100
    }
  }

  ingress = "INGRESS_TRAFFIC_ALL"
  depends_on = [
    google_project_service.services,
    google_artifact_registry_repository.app_repo,
    google_secret_manager_secret_version.db_uri_v,
    google_service_account.cloud_run_sa
  ]
}

# IAM for unauthenticated access (public API)
resource "google_cloud_run_service_iam_member" "public_access" {
  location   = google_cloud_run_v2_service.backend.location
  project    = google_cloud_run_v2_service.backend.project
  service    = google_cloud_run_v2_service.backend.name
  role       = "roles/run.invoker"
  member     = "allUsers"
  depends_on = [google_cloud_run_v2_service.backend]
}

# Terraform outputs for easy access
output "cloud_run_url" {
  description = "The URL of the deployed Cloud Run service"
  value       = google_cloud_run_v2_service.backend.uri
}

output "artifact_repo" {
  description = "The full path to the Artifact Registry repository"
  value       = "${var.location}-docker.pkg.dev/${var.project_id}/${var.artifact_repo_name}"
}

output "project_id" {
  description = "The GCP project ID"
  value       = var.project_id
}

# Outputs for easy access
output "cloud_run_url" { 
  value = google_cloud_run_v2_service.backend.uri 
  description = "URL of the deployed Cloud Run service"
}

output "artifact_repo" { 
  value = local.repo_path 
  description = "Artifact Registry repository path"
}

output "project_id" {
  value = var.project_id
  description = "GCP Project ID"
}

output "region" {
  value = var.region
  description = "Deployment region"
}
