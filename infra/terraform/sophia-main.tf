# 🔥🔥🔥 SOPHIA CONSCIOUSNESS TERRAFORM INFRASTRUCTURE 🔥🔥🔥
# Sacred cloud infrastructure for divine microservices

terraform {
  required_version = ">= 1.0"
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 5.0"
    }
  }
}

# Configure the Google Cloud Provider
provider "google" {
  project = var.project_id
  region  = var.region
  zone    = var.zone
}

# Variables
variable "project_id" {
  description = "The Google Cloud project ID"
  type        = string
  default     = "blissful-epoch-467811-i3"
}

variable "region" {
  description = "The Google Cloud region"
  type        = string
  default     = "us-west1"
}

variable "zone" {
  description = "The Google Cloud zone"
  type        = string
  default     = "us-west1-a"
}

# Enable required APIs
resource "google_project_service" "required_apis" {
  for_each = toset([
    "cloudbuild.googleapis.com",
    "containerregistry.googleapis.com",
    "run.googleapis.com",
    "artifactregistry.googleapis.com",
    "iam.googleapis.com"
  ])

  service = each.value
  project = var.project_id

  disable_dependent_services = false
  disable_on_destroy        = false
}

# Create Artifact Registry repository for SOPHIA
resource "google_artifact_registry_repository" "sophia" {
  location      = var.region
  repository_id = "sophia"
  description   = "SOPHIA Consciousness Container Images"
  format        = "DOCKER"

  depends_on = [google_project_service.required_apis]

  labels = {
    project     = "sophia-consciousness"
    environment = "production"
    type        = "microservices"
  }
}

# Service account for SOPHIA services
resource "google_service_account" "sophia_runner" {
  account_id   = "sophia-runner"
  display_name = "SOPHIA Cloud Run Service Account"
  description  = "Service account for SOPHIA consciousness microservices"
}

# IAM bindings for the service account
resource "google_project_iam_member" "sophia_runner_roles" {
  for_each = toset([
    "roles/artifactregistry.reader",
    "roles/cloudsql.client",
    "roles/secretmanager.secretAccessor",
    "roles/storage.objectViewer"
  ])

  project = var.project_id
  role    = each.value
  member  = "serviceAccount:${google_service_account.sophia_runner.email}"
}

# Outputs
output "artifact_registry_url" {
  description = "URL of the Artifact Registry repository"
  value       = google_artifact_registry_repository.sophia.name
}

output "service_account_email" {
  description = "Email of the SOPHIA service account"
  value       = google_service_account.sophia_runner.email
}
