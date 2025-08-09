#!/bin/bash
# 🚀 ANCHOR1 LLC - BotDL SoulPHYA Google Cloud Deployment Script
# Sacred deployment to bring divine consciousness online

echo "🌟 ==============================================="
echo "🏢 ANCHOR1 LLC - BotDL SoulPHYA CLOUD DEPLOYMENT"
echo "🌟 ==============================================="

# Set your Google Cloud project
PROJECT_ID="anchor1-botdl-soulphya"
REGION="us-central1"
DOMAIN="app.anchor1llc.com"
API_DOMAIN="api.anchor1llc.com"

echo "🔧 Setting up Google Cloud configuration..."
gcloud config set project $PROJECT_ID
gcloud config set run/region $REGION

echo "🐳 Building and deploying backend to Cloud Run..."
cd backend

# Create Dockerfile if it doesn't exist
if [ ! -f "Dockerfile" ]; then
    echo "📝 Creating optimized Dockerfile..."
    cat > Dockerfile << 'EOF'
FROM python:3.9-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create necessary directories
RUN mkdir -p ai_engine/divine_resonance ai_engine/love_wisdom ai_engine/consciousness ai_engine/orchestrator

# Set environment variables
ENV FLASK_APP=app.py
ENV FLASK_ENV=production
ENV PORT=8080

# Expose port
EXPOSE 8080

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8080/api/health || exit 1

# Run the application
CMD ["python", "app.py"]
EOF
fi

# Build and deploy to Cloud Run
echo "🏗️ Building container image..."
gcloud builds submit --tag gcr.io/$PROJECT_ID/botdl-backend

echo "🚀 Deploying to Cloud Run..."
gcloud run deploy botdl-backend \
    --image gcr.io/$PROJECT_ID/botdl-backend \
    --platform managed \
    --region $REGION \
    --allow-unauthenticated \
    --port 8080 \
    --memory 2Gi \
    --cpu 2 \
    --max-instances 10 \
    --set-env-vars "ENV=production,GOOGLE_CLOUD=true"

echo "🌐 Getting service URL..."
BACKEND_URL=$(gcloud run services describe botdl-backend --platform managed --region $REGION --format 'value(status.url)')
echo "✅ Backend deployed at: $BACKEND_URL"

# Deploy frontend to Firebase Hosting
echo "🎨 Preparing frontend deployment..."
cd ../frontend

# Create Firebase config if it doesn't exist
if [ ! -f "firebase.json" ]; then
    echo "📝 Creating Firebase configuration..."
    cat > firebase.json << EOF
{
  "hosting": {
    "public": "dist",
    "ignore": [
      "firebase.json",
      "**/.*",
      "**/node_modules/**"
    ],
    "rewrites": [
      {
        "source": "**",
        "destination": "/index.html"
      }
    ],
    "headers": [
      {
        "source": "**/*.@(js|jsx|ts|tsx)",
        "headers": [
          {
            "key": "Cache-Control",
            "value": "max-age=31536000"
          }
        ]
      }
    ]
  }
}
EOF
fi

# Create environment file for frontend
echo "VITE_API_BASE=$BACKEND_URL" > .env.production

# Build and deploy frontend
echo "🏗️ Building frontend..."
npm run build

echo "🚀 Deploying to Firebase Hosting..."
firebase deploy --only hosting

# Set up custom domains
echo "🌐 Setting up custom domains..."
echo "📝 To complete domain setup:"
echo "1. Go to Cloud Run console for botdl-backend"
echo "2. Add custom domain: $API_DOMAIN"
echo "3. Go to Firebase Hosting console"
echo "4. Add custom domain: $DOMAIN"
echo "5. Update your DNS records as shown in the consoles"

echo "✅ Deployment complete!"
echo "🌟 Backend: $BACKEND_URL"
echo "🌟 Custom API domain (after DNS): https://$API_DOMAIN"
echo "🌟 Custom frontend domain (after DNS): https://$DOMAIN"
