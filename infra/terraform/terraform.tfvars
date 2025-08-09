project_id         = "anchor1-soulphya"
region             = "us-central1"
location           = "us-central1"
service_name       = "botdl-backend"
artifact_repo_name = "app-repo"
cors_allow_origins = "https://app.anchor1llc.com,https://soulphya.io,https://botdl-backend-1021802765249.us-central1.run.app"

# Optional: Set secrets manually (otherwise auto-generated)
# secret_key = "your-super-secret-flask-key-64-chars-long"
# openai_api_key = "sk-..."
# anthropic_api_key = "sk-ant-..."

# Vertex AI settings
vertex_location = "us-central1"

# Database settings (optional for now)
db_tier = "db-f1-micro"
db_version = "POSTGRES_15"
db_name = "botdl"
db_user = "appuser"
