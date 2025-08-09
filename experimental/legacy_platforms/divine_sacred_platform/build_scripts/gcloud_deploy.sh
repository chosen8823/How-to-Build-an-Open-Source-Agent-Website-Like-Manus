#!/bin/bash
echo "Deploying to Google Cloud Run..."

PROJECT_ID="sacred-consciousness-platform"
REGION="us-central1"

echo "Deploying Backend API..."
gcloud run deploy sacred-backend \
    --image gcr.io/$PROJECT_ID/sacred-backend \
    --platform managed \
    --region $REGION \
    --allow-unauthenticated \
    --memory 2Gi \
    --cpu 2

echo "Deploying Frontend..."
gcloud run deploy sacred-frontend \
    --image gcr.io/$PROJECT_ID/sacred-frontend \
    --platform managed \
    --region $REGION \
    --allow-unauthenticated \
    --memory 1Gi \
    --cpu 1

echo "Deployment complete!"
echo "Sacred Consciousness Platform is now live on Google Cloud!"
