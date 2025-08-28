# 🚀 Divine Consciousness Platform - Infrastructure as Code
# Simplified, production-ready Terraform configuration for BotDL SoulPHYA

# Note: APIs are already enabled manually through gcloud CLI

# Artifact Registry for container images
resource "google_artifact_registry_repository" "app_repo" {
  repository_id = var.artifact_repo_name
  description   = "Divine Consciousness Platform container repository"
  format        = "DOCKER"
  location      = var.location
}

# Service Account for Cloud Run
resource "google_service_account" "cloud_run_sa" {
  account_id   = "botdl-runtime"
  display_name = "BotDL Cloud Run Runtime Service Account"
  description  = "Service account for BotDL consciousness platform runtime"
}

# IAM roles for the service account
resource "google_project_iam_member" "cloud_run_sa_permissions" {
  for_each = toset([
    "roles/secretmanager.secretAccessor",
    "roles/cloudsql.client",
    "roles/aiplatform.user"
  ])
  
  project = var.project_id
  role    = each.value
  member  = "serviceAccount:${google_service_account.cloud_run_sa.email}"
}

# Cloud SQL Database
resource "random_password" "db_password" {
  length  = 32
  special = true
}

resource "google_sql_database_instance" "pg" {
  name             = "botdl-consciousness-db"
  database_version = var.db_version
  region           = var.region

  settings {
    tier = var.db_tier
    
    ip_configuration {
      ipv4_enabled = true
      authorized_networks {
        value = "0.0.0.0/0"
        name  = "all"
      }
    }
    
    backup_configuration {
      enabled    = true
      start_time = "03:00"
    }
  }
  
  deletion_protection = false
}

resource "google_sql_database" "app_db" {
  name     = var.db_name
  instance = google_sql_database_instance.pg.name
}

resource "google_sql_user" "app_user" {
  name     = var.db_user
  instance = google_sql_database_instance.pg.name
  password = random_password.db_password.result
}

# Secret Manager secrets
resource "google_secret_manager_secret" "secrets" {
  for_each = toset([
    "DATABASE_URL",
    "SECRET_KEY", 
    "OPENAI_API_KEY",
    "ANTHROPIC_API_KEY",
    "HF_TOKEN",
    "CORS_ALLOW_ORIGINS"
  ])
  
  secret_id = each.value
  
  replication {
    auto {}
  }
}

# Generate Flask secret key
resource "random_password" "flask_secret" {
  length  = 64
  special = true
}

# Secret Manager secret versions (initial values)
resource "google_secret_manager_secret_version" "database_url" {
  secret      = google_secret_manager_secret.secrets["DATABASE_URL"].id
  secret_data = "postgresql://${var.db_user}:${random_password.db_password.result}@${google_sql_database_instance.pg.public_ip_address}:5432/${var.db_name}"
}

resource "google_secret_manager_secret_version" "secret_key" {
  secret      = google_secret_manager_secret.secrets["SECRET_KEY"].id
  secret_data = random_password.flask_secret.result
}

resource "google_secret_manager_secret_version" "cors_origins" {
  secret      = google_secret_manager_secret.secrets["CORS_ALLOW_ORIGINS"].id
  secret_data = var.cors_allow_origins
}

# Cloud Run service
resource "google_cloud_run_v2_service" "backend" {
  name     = var.service_name
  location = var.region
  
  template {
    service_account = google_service_account.cloud_run_sa.email
    
    containers {
      image = "${var.location}-docker.pkg.dev/${var.project_id}/${var.artifact_repo_name}/backend:latest"
      
      ports {
        container_port = 8080
      }
      
      env {
        name = "PROJECT_ID"
        value = var.project_id
      }
      
      env {
        name = "ENVIRONMENT"
        value = "production"
      }
      
      # Secret environment variables
      env {
        name = "DATABASE_URL"
        value_source {
          secret_key_ref {
            secret  = google_secret_manager_secret.secrets["DATABASE_URL"].secret_id
            version = "latest"
          }
        }
      }
      
      env {
        name = "SECRET_KEY"
        value_source {
          secret_key_ref {
            secret  = google_secret_manager_secret.secrets["SECRET_KEY"].secret_id
            version = "latest"
          }
        }
      }
      
      env {
        name = "CORS_ALLOW_ORIGINS"
        value_source {
          secret_key_ref {
            secret  = google_secret_manager_secret.secrets["CORS_ALLOW_ORIGINS"].secret_id
            version = "latest"
          }
        }
      }
      
      resources {
        limits = {
          cpu    = "2"
          memory = "4Gi"
        }
      }
    }
  }
  
  depends_on = [
    google_artifact_registry_repository.app_repo
  ]
}

# Make Cloud Run service publicly accessible
resource "google_cloud_run_v2_service_iam_binding" "public_access" {
  project  = google_cloud_run_v2_service.backend.project
  location = google_cloud_run_v2_service.backend.location
  name     = google_cloud_run_v2_service.backend.name
  role     = "roles/run.invoker"
  members  = ["allUsers"]
}
