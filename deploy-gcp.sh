#!/bin/bash
# 🏢 ANCHOR1 LLC - Google Cloud Platform Deployment Script
# Complete GCP setup for BotDL SoulPHYA Divine Consciousness Platform

set -e

# Configuration
PROJECT_ID="anchor1-divine-consciousness"
REGION="us-central1"
SERVICE_NAME="anchor1-soulphya-platform"
IMAGE_NAME="soulphya-platform"
DATABASE_INSTANCE="soulphya-db"

echo "🏢 ANCHOR1 LLC - Deploying BotDL SoulPHYA to Google Cloud Platform"
echo "=================================================================="

# 1. Set up Google Cloud Project
echo "🔧 Setting up Google Cloud Project..."
gcloud config set project $PROJECT_ID
gcloud services enable run.googleapis.com
gcloud services enable cloudbuild.googleapis.com
gcloud services enable sqladmin.googleapis.com
gcloud services enable secretmanager.googleapis.com
gcloud services enable compute.googleapis.com

# 2. Build and push Docker image
echo "🐳 Building and pushing Docker image..."
gcloud builds submit --tag gcr.io/$PROJECT_ID/$IMAGE_NAME .

# 3. Create Cloud SQL Database
echo "🗃️ Setting up Cloud SQL database..."
if ! gcloud sql instances describe $DATABASE_INSTANCE --region=$REGION 2>/dev/null; then
    gcloud sql instances create $DATABASE_INSTANCE \
        --database-version=POSTGRES_15 \
        --tier=db-f1-micro \
        --region=$REGION \
        --root-password=divine_consciousness_root
    
    gcloud sql databases create soulphya --instance=$DATABASE_INSTANCE
    gcloud sql users create anchor1 --instance=$DATABASE_INSTANCE --password=divine_consciousness
fi

# 4. Create Redis instance
echo "🔴 Setting up Redis cache..."
if ! gcloud redis instances describe soulphya-redis --region=$REGION 2>/dev/null; then
    gcloud redis instances create soulphya-redis \
        --size=1 \
        --region=$REGION \
        --redis-version=redis_7_0
fi

# 5. Store secrets
echo "🔐 Setting up secrets..."
DATABASE_URL="postgresql://anchor1:divine_consciousness@/soulphya?host=/cloudsql/$PROJECT_ID:$REGION:$DATABASE_INSTANCE"
REDIS_HOST=$(gcloud redis instances describe soulphya-redis --region=$REGION --format="value(host)")
REDIS_URL="redis://$REDIS_HOST:6379/0"

echo -n "$DATABASE_URL" | gcloud secrets create database-url --data-file=-
echo -n "$REDIS_URL" | gcloud secrets create redis-url --data-file=-

# 6. Create service account and key
echo "🔑 Setting up service account..."
SERVICE_ACCOUNT="soulphya-service@$PROJECT_ID.iam.gserviceaccount.com"
if ! gcloud iam service-accounts describe $SERVICE_ACCOUNT 2>/dev/null; then
    gcloud iam service-accounts create soulphya-service \
        --display-name="BotDL SoulPHYA Service Account"
    
    gcloud projects add-iam-policy-binding $PROJECT_ID \
        --member="serviceAccount:$SERVICE_ACCOUNT" \
        --role="roles/cloudsql.client"
    
    gcloud projects add-iam-policy-binding $PROJECT_ID \
        --member="serviceAccount:$SERVICE_ACCOUNT" \
        --role="roles/redis.editor"
    
    gcloud iam service-accounts keys create key.json \
        --iam-account=$SERVICE_ACCOUNT
    
    gcloud secrets create google-cloud-key --data-file=key.json
    rm key.json
fi

# 7. Deploy to Cloud Run
echo "🚀 Deploying to Cloud Run..."
gcloud run deploy $SERVICE_NAME \
    --image gcr.io/$PROJECT_ID/$IMAGE_NAME \
    --platform managed \
    --region $REGION \
    --allow-unauthenticated \
    --port 8001 \
    --memory 4Gi \
    --cpu 2 \
    --max-instances 100 \
    --min-instances 1 \
    --set-env-vars="FLASK_ENV=production,GOOGLE_CLOUD_PROJECT=$PROJECT_ID" \
    --set-secrets="DATABASE_URL=database-url:latest,REDIS_URL=redis-url:latest,GOOGLE_APPLICATION_CREDENTIALS=/var/secrets/google/key.json=google-cloud-key:latest" \
    --add-cloudsql-instances $PROJECT_ID:$REGION:$DATABASE_INSTANCE \
    --service-account $SERVICE_ACCOUNT

# 8. Set up custom domain (optional)
echo "🌐 Setting up custom domain..."
DOMAIN="platform.anchor1llc.com"
gcloud run domain-mappings create --service $SERVICE_NAME --domain $DOMAIN --region $REGION

# 9. Configure monitoring
echo "📊 Setting up monitoring..."
gcloud logging sinks create soulphya-logs \
    bigquery.googleapis.com/projects/$PROJECT_ID/datasets/soulphya_logs \
    --log-filter="resource.type=cloud_run_revision AND resource.labels.service_name=$SERVICE_NAME"

# Get the deployed URL
SERVICE_URL=$(gcloud run services describe $SERVICE_NAME --region=$REGION --format="value(status.url)")

echo ""
echo "🎉 DEPLOYMENT COMPLETE!"
echo "=================================================================="
echo "🏢 Anchor1 LLC BotDL SoulPHYA Platform is now live!"
echo "🌐 Service URL: $SERVICE_URL"
echo "🌐 Custom Domain: https://$DOMAIN (if configured)"
echo "📊 Monitoring: https://console.cloud.google.com/run/detail/$REGION/$SERVICE_NAME"
echo "🗃️ Database: $PROJECT_ID:$REGION:$DATABASE_INSTANCE"
echo "🔴 Redis: soulphya-redis"
echo ""
echo "✅ All systems are operational and ready for enterprise use!"
echo "⚡🌟💎 ANCHOR1 LLC DIVINE CONSCIOUSNESS PLATFORM ACTIVE 💎🌟⚡"
