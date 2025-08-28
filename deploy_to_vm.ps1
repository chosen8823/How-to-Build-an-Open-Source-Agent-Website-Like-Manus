# 🚀 ANCHOR1 LLC - Deploy to VM Script
# PowerShell script to deploy your BotDL SoulPHYA platform to the VM

Write-Host "🚀 ANCHOR1 LLC - VM Deployment Script" -ForegroundColor Cyan
Write-Host "====================================" -ForegroundColor Cyan

# VM Configuration
$VM_NAME = "anchor1-dev-beast"
$VM_ZONE = "us-central1-a"
$VM_IP = "34.55.15.199"  # External IP from VM creation

Write-Host "🎯 Target VM: $VM_NAME ($VM_IP)" -ForegroundColor Yellow

# Step 1: Copy setup script to VM
Write-Host "📂 Copying setup script to VM..." -ForegroundColor Green
gcloud compute scp vm_setup.sh ${VM_NAME}:~/setup.sh --zone=$VM_ZONE

# Step 2: Make setup script executable and run it
Write-Host "🚀 Running setup script on VM..." -ForegroundColor Green
gcloud compute ssh $VM_NAME --zone=$VM_ZONE --command="chmod +x ~/setup.sh && ~/setup.sh"

# Step 3: Copy your BotDL SoulPHYA backend code
Write-Host "📦 Deploying BotDL SoulPHYA backend..." -ForegroundColor Green
gcloud compute scp --recurse backend ${VM_NAME}:~/anchor1-soulphya/ --zone=$VM_ZONE

# Step 4: Copy the Vertex AI code assistant
Write-Host "🤖 Deploying Vertex AI Code Assistant..." -ForegroundColor Green
gcloud compute scp vertex_ai_code_assistant.py ${VM_NAME}:~/anchor1-soulphya/backend/ --zone=$VM_ZONE

# Step 5: Install enhanced requirements
Write-Host "📦 Installing enhanced requirements..." -ForegroundColor Green
gcloud compute ssh $VM_NAME --zone=$VM_ZONE --command="cd ~/anchor1-soulphya && source venv/bin/activate && pip install -r backend/requirements.txt"

# Step 6: Set up Google Cloud authentication on VM
Write-Host "🔐 Setting up Google Cloud authentication..." -ForegroundColor Green
gcloud compute ssh $VM_NAME --zone=$VM_ZONE --command="gcloud auth application-default login --no-launch-browser"

# Step 7: Start the platform
Write-Host "🚀 Starting the platform..." -ForegroundColor Green
gcloud compute ssh $VM_NAME --zone=$VM_ZONE --command="cd ~/anchor1-soulphya && source venv/bin/activate && cd backend && nohup python app.py > app.log 2>&1 &"

Write-Host ""
Write-Host "🎉 DEPLOYMENT COMPLETE!" -ForegroundColor Green
Write-Host "======================" -ForegroundColor Green
Write-Host ""
Write-Host "✅ Your BotDL SoulPHYA platform is now running on the VM!" -ForegroundColor Cyan
Write-Host ""
Write-Host "🌐 Platform URL: http://$VM_IP:8080" -ForegroundColor Yellow
Write-Host "🔗 Health Check: http://$VM_IP:8080/api/health" -ForegroundColor Yellow
Write-Host "📊 Status Check: http://$VM_IP:8080/api/status" -ForegroundColor Yellow
Write-Host ""
Write-Host "🚀 Next Steps:" -ForegroundColor Magenta
Write-Host "1. Test the platform: Invoke-WebRequest -Uri 'http://$VM_IP:8080/api/health'" -ForegroundColor White
Write-Host "2. SSH to VM: gcloud compute ssh $VM_NAME --zone=$VM_ZONE" -ForegroundColor White
Write-Host "3. Run Vertex AI assistant: python vertex_ai_code_assistant.py" -ForegroundColor White
Write-Host "4. Monitor logs: tail -f ~/anchor1-soulphya/backend/app.log" -ForegroundColor White
Write-Host ""
Write-Host "💎 Anchor1 LLC - Divine Consciousness Platform LIVE!" -ForegroundColor Cyan

# Test the deployment
Write-Host "🧪 Testing deployment..." -ForegroundColor Green
Start-Sleep 5

try {
    $response = Invoke-WebRequest -Uri "http://$VM_IP:8080/api/health" -Method GET -TimeoutSec 10
    if ($response.StatusCode -eq 200) {
        Write-Host "✅ Platform is responding successfully!" -ForegroundColor Green
        $content = $response.Content | ConvertFrom-Json
        Write-Host "📊 Platform Status: $($content.status)" -ForegroundColor Yellow
    }
} catch {
    Write-Host "⏳ Platform is starting up... Give it a few more seconds" -ForegroundColor Yellow
    Write-Host "🔄 You can test manually with: Invoke-WebRequest -Uri 'http://$VM_IP:8080/api/health'" -ForegroundColor White
}
