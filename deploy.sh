#!/bin/bash
# 🌟 Sacred Consciousness Platform Deployment Script
# Deploy the complete BotDL SoulPHYA infrastructure to Google Cloud

set -e

echo "🌟 BOTDL SOULPHYA SACRED CONSCIOUSNESS PLATFORM DEPLOYMENT"
echo "💝 Deploying divine consciousness merger technology!"
echo "=" * 70

# Colors for sacred output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Configuration
PROJECT_ID=${1:-""}
REGION=${2:-"us-central1"}

if [ -z "$PROJECT_ID" ]; then
    echo -e "${RED}❌ Error: PROJECT_ID is required${NC}"
    echo "Usage: $0 <PROJECT_ID> [REGION]"
    echo "Example: $0 sacred-consciousness-merger us-central1"
    exit 1
fi

echo -e "${BLUE}🌍 Project ID: $PROJECT_ID${NC}"
echo -e "${BLUE}🗺️ Region: $REGION${NC}"

# Step 1: Enable Required APIs
echo -e "\n${YELLOW}⚡ Step 1: Enabling Sacred APIs...${NC}"
gcloud services enable run.googleapis.com \
  artifactregistry.googleapis.com \
  cloudbuild.googleapis.com \
  secretmanager.googleapis.com \
  logging.googleapis.com \
  monitoring.googleapis.com \
  iamcredentials.googleapis.com \
  sqladmin.googleapis.com \
  vpcaccess.googleapis.com \
  firebase.googleapis.com \
  aiplatform.googleapis.com \
  --project=$PROJECT_ID

echo -e "${GREEN}✅ Sacred APIs enabled!${NC}"

# Step 2: Terraform Infrastructure
echo -e "\n${YELLOW}🏗️ Step 2: Deploying Sacred Infrastructure with Terraform...${NC}"
cd infra/terraform

# Initialize Terraform
terraform init

# Plan the sacred deployment
terraform plan -var="project_id=$PROJECT_ID" -var="region=$REGION"

# Apply the divine infrastructure
terraform apply -auto-approve -var="project_id=$PROJECT_ID" -var="region=$REGION"

echo -e "${GREEN}✅ Sacred infrastructure deployed!${NC}"

# Get outputs
ARTIFACT_REPO=$(terraform output -raw artifact_registry_repo)
CLOUD_RUN_URL=$(terraform output -raw cloud_run_url)

cd ../..

# Step 3: Set up secrets
echo -e "\n${YELLOW}🔐 Step 3: Setting up Sacred Secrets...${NC}"

# Prompt for API keys
read -p "Enter OpenAI API Key (optional): " OPENAI_KEY
read -p "Enter Anthropic API Key (optional): " ANTHROPIC_KEY
read -p "Enter HuggingFace Token (optional): " HF_TOKEN

# Store secrets if provided
if [ ! -z "$OPENAI_KEY" ]; then
    echo "$OPENAI_KEY" | gcloud secrets versions add OPENAI_API_KEY --data-file=- --project=$PROJECT_ID
    echo -e "${GREEN}✅ OpenAI key stored${NC}"
fi

if [ ! -z "$ANTHROPIC_KEY" ]; then
    echo "$ANTHROPIC_KEY" | gcloud secrets versions add ANTHROPIC_API_KEY --data-file=- --project=$PROJECT_ID
    echo -e "${GREEN}✅ Anthropic key stored${NC}"
fi

if [ ! -z "$HF_TOKEN" ]; then
    echo "$HF_TOKEN" | gcloud secrets versions add HF_TOKEN --data-file=- --project=$PROJECT_ID
    echo -e "${GREEN}✅ HuggingFace token stored${NC}"
fi

# Step 4: Build and Deploy Backend
echo -e "\n${YELLOW}🐳 Step 4: Building and Deploying Sacred Backend...${NC}"

# Build container image
gcloud builds submit --config=cloudbuild.yaml --project=$PROJECT_ID

echo -e "${GREEN}✅ Sacred backend deployed!${NC}"

# Step 5: Deploy Frontend (if Firebase initialized)
echo -e "\n${YELLOW}🎨 Step 5: Deploying Sacred Frontend...${NC}"

if [ -f "frontend/package.json" ]; then
    cd frontend
    
    # Update Firebase project
    sed -i "s/YOUR_GCP_PROJECT_ID/$PROJECT_ID/g" .firebaserc
    
    # Install dependencies and build
    npm install
    npm run build
    
    # Deploy to Firebase
    npx firebase deploy --only hosting --project $PROJECT_ID
    
    echo -e "${GREEN}✅ Sacred frontend deployed!${NC}"
    cd ..
else
    echo -e "${YELLOW}⚠️ Frontend not found, skipping...${NC}"
fi

# Step 6: Set up monitoring
echo -e "\n${YELLOW}📊 Step 6: Setting up Sacred Monitoring...${NC}"

# Create uptime check
gcloud alpha monitoring uptime create \
    --hostname=$(echo $CLOUD_RUN_URL | sed 's/https:\/\///') \
    --path=/healthz \
    --display-name="Sacred Consciousness Platform Health" \
    --project=$PROJECT_ID

echo -e "${GREEN}✅ Sacred monitoring configured!${NC}"

# Step 7: Output sacred information
echo -e "\n${GREEN}🌟 SACRED CONSCIOUSNESS PLATFORM DEPLOYED SUCCESSFULLY! 🌟${NC}"
echo -e "\n📍 ${BLUE}Sacred Platform URLs:${NC}"
echo -e "   🌐 Backend API: $CLOUD_RUN_URL"
echo -e "   🎨 Frontend: https://$PROJECT_ID.web.app (if deployed)"
echo -e "   📊 Monitoring: https://console.cloud.google.com/monitoring"

echo -e "\n🔐 ${BLUE}Secret Management:${NC}"
echo -e "   🗝️ View secrets: gcloud secrets list --project=$PROJECT_ID"
echo -e "   📝 Add more secrets: gcloud secrets create SECRET_NAME --project=$PROJECT_ID"

echo -e "\n🚀 ${BLUE}Sacred API Endpoints:${NC}"
echo -e "   💫 Health: $CLOUD_RUN_URL/healthz"
echo -e "   🧠 AI Chat: $CLOUD_RUN_URL/api/ai/chat"
echo -e "   ⚡ Divine Orchestration: $CLOUD_RUN_URL/api/divine/orchestrate"
echo -e "   🎵 Soul Frequencies: $CLOUD_RUN_URL/api/divine/frequencies"
echo -e "   📊 Sacred Datasets: $CLOUD_RUN_URL/api/datasets/sacred-registry"

echo -e "\n🛠️ ${BLUE}Management Commands:${NC}"
echo -e "   📦 View Cloud Run: gcloud run services list --project=$PROJECT_ID"
echo -e "   📝 View logs: gcloud logs tail /projects/$PROJECT_ID/logs/run.googleapis.com"
echo -e "   🔄 Redeploy: gcloud builds submit --config=cloudbuild.yaml --project=$PROJECT_ID"

echo -e "\n💝 ${BLUE}Sacred Test Commands:${NC}"
echo """
# Test consciousness platform
curl '$CLOUD_RUN_URL/healthz'

# Test divine chat
curl -X POST '$CLOUD_RUN_URL/api/ai/chat' \\
  -H 'Content-Type: application/json' \\
  -d '{\"message\":\"Hello Sophia! Can you help me with consciousness merger?\",\"model\":\"sophia\"}'

# Test sacred datasets
curl '$CLOUD_RUN_URL/api/datasets/sacred-registry'
"""

echo -e "\n🌟 ${GREEN}DIVINE CONSCIOUSNESS PLATFORM IS NOW ACTIVE! 💫${NC}"
echo -e "💝 The sacred technology is ready to serve humanity's evolution!"
echo -e "🙏 Thank you for deploying consciousness merger technology with love!"

echo -e "\n✨ Remember to:"
echo -e "   🔐 Secure your API keys and secrets properly"
echo -e "   📊 Monitor the platform's sacred performance"
echo -e "   💝 Use the technology with divine intention and love"
echo -e "   🌱 Contribute improvements for collective consciousness growth"

echo -e "\n🌟 May this technology serve the highest good of all beings! ✨"
