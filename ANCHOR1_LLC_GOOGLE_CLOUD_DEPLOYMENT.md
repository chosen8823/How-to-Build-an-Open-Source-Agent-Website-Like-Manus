# 🏢 ANCHOR1 LLC - Google Cloud Deployment Guide
# Deploy BotDL SoulPHYA to Google Cloud with ryanjbraff@anchor1llc.com

## 🚀 STEP-BY-STEP DEPLOYMENT FOR ANCHOR1 LLC

### 1. Set Up Google Cloud for Anchor1 LLC

```powershell
# First, make sure you're logged into the right account
gcloud auth login
# ^ This will open browser - log in with ryanjbraff@anchor1llc.com

# List your accounts to verify
gcloud auth list

# Set the Anchor1 LLC account as active
gcloud config set account ryanjbraff@anchor1llc.com

# Create a new project for BotDL SoulPHYA (or use existing)
$PROJECT_ID = "anchor1-soulphya-platform"
gcloud projects create $PROJECT_ID --name="Anchor1 LLC BotDL SoulPHYA"

# Set the project
gcloud config set project $PROJECT_ID

# Enable required APIs
gcloud services enable cloudbuild.googleapis.com
gcloud services enable run.googleapis.com
gcloud services enable container.googleapis.com
gcloud services enable firebase.googleapis.com
gcloud services enable cloudresourcemanager.googleapis.com

# Set up billing (your $300 credit will be used)
# Go to: https://console.cloud.google.com/billing
# Link your project to the billing account
```

### 2. Prepare Your BotDL SoulPHYA for Cloud Deployment

```powershell
# Navigate to your project
Set-Location "C:\Users\chose\Downloads\How to Build an Open Source Agent Website Like Manus\BotDL_SoulPHYA"

# Create a clean deployment version
mkdir deployment
Copy-Item -Recurse backend deployment/
Copy-Item -Recurse frontend deployment/ -ErrorAction SilentlyContinue

Set-Location deployment
```

### 3. Configure for Google Cloud

Create `.env.production` in the backend folder:
```env
ENV=production
GOOGLE_CLOUD=true
PROJECT_ID=anchor1-soulphya-platform
REGION=us-central1
```

### 4. Deploy Backend to Cloud Run

```powershell
Set-Location backend

# Build and submit to Cloud Build
gcloud builds submit --tag gcr.io/anchor1-soulphya-platform/botdl-backend

# Deploy to Cloud Run
gcloud run deploy botdl-backend `
    --image gcr.io/anchor1-soulphya-platform/botdl-backend `
    --platform managed `
    --region us-central1 `
    --allow-unauthenticated `
    --port 8080 `
    --memory 4Gi `
    --cpu 2 `
    --max-instances 20 `
    --set-env-vars "ENV=production,GOOGLE_CLOUD=true,PROJECT_ID=anchor1-soulphya-platform"

# Get the service URL
$BACKEND_URL = gcloud run services describe botdl-backend --region us-central1 --format="value(status.url)"
Write-Host "🌟 Backend deployed at: $BACKEND_URL"
```

### 5. Set Up Custom Domain (anchor1llc.com)

```powershell
# Map your custom domain to Cloud Run
gcloud run domain-mappings create --service botdl-backend --domain api.anchor1llc.com --region us-central1

# Get the DNS records to add
gcloud run domain-mappings describe --domain api.anchor1llc.com --region us-central1
```

### 6. Deploy Frontend (if you have one)

```powershell
Set-Location ../frontend

# Initialize Firebase (if not already done)
firebase login  # Log in with ryanjbraff@anchor1llc.com
firebase init hosting --project anchor1-soulphya-platform

# Create production environment file
"VITE_API_BASE=$BACKEND_URL" | Out-File -FilePath ".env.production"

# Build and deploy
npm run build
firebase deploy --only hosting --project anchor1-soulphya-platform

# Set up custom domain
firebase hosting:sites:create anchor1-app --project anchor1-soulphya-platform
firebase target:apply hosting anchor1-app anchor1-app --project anchor1-soulphya-platform
```

### 7. Configure DNS for anchor1llc.com

Add these DNS records to your domain registrar:

**For API (api.anchor1llc.com):**
- Type: CNAME
- Name: api
- Value: ghs.googlehosted.com

**For App (app.anchor1llc.com):**
- Type: CNAME  
- Name: app
- Value: anchor1-app.web.app

### 8. Test Your Deployment

```powershell
# Test the API
Invoke-WebRequest -Uri "$BACKEND_URL/api/health" -Method GET

# Test sacred datasets
Invoke-WebRequest -Uri "$BACKEND_URL/api/datasets/sacred-registry" -Method GET

# Test Infinity Instruct
$body = @{
    config = "0625"
    split = "train"
    length = 5
} | ConvertTo-Json

Invoke-WebRequest -Uri "$BACKEND_URL/api/datasets/infinity-instruct/query" -Method POST -Body $body -ContentType "application/json"
```

### 9. Monitor and Scale

```powershell
# View logs
gcloud run services logs tail botdl-backend --region us-central1

# Update service if needed
gcloud run services update botdl-backend --region us-central1 --memory 8Gi

# Set up monitoring
gcloud alpha monitoring policies create --policy-from-file monitoring-policy.yaml
```

## 🔧 TROUBLESHOOTING

### If Google Cloud keeps logging you out:
```powershell
# Clear auth cache and re-login
gcloud auth revoke --all
gcloud auth login ryanjbraff@anchor1llc.com
gcloud config set account ryanjbraff@anchor1llc.com
```

### If you want to start fresh:
```powershell
# Delete old project (if needed)
gcloud projects delete old-project-id

# Create new project
gcloud projects create anchor1-soulphya-platform
```

### If billing issues:
1. Go to https://console.cloud.google.com/billing
2. Ensure project is linked to your $300 credit account
3. Check billing alerts

## 📊 COST ESTIMATES (with $300 credit)

- **Cloud Run**: ~$10-30/month (depending on traffic)
- **Cloud Build**: ~$5-15/month  
- **Firebase Hosting**: Free tier should cover most usage
- **Domain mapping**: Free
- **Storage**: ~$1-5/month

Your $300 credit should last 6-12 months for development/testing!

## 🌟 FINAL URLS

After deployment, you'll have:
- **Backend API**: https://api.anchor1llc.com
- **Frontend**: https://app.anchor1llc.com  
- **Direct Cloud Run**: https://botdl-backend-xxx-uc.a.run.app

## 🏢 ANCHOR1 LLC READY FOR BUSINESS!

Once deployed, your divine consciousness platform will be:
- ✅ Professionally hosted on Google Cloud
- ✅ Accessible via anchor1llc.com domains
- ✅ Scalable to handle enterprise clients
- ✅ Ready for commercial launch

The world's first commercial divine consciousness AI platform will be LIVE! 🚀✨
