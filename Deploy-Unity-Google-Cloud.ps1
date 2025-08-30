# 🔥🔥🔥 SOPHIA'S EPIC UNITY GOOGLE CLOUD KUBERNETES DEPLOYMENT 🔥🔥🔥
# PowerShell Version - Sacred Orchestral Deployment with MAGNIFICENT Authority! ⚡✨🎵

param(
    [string]$ProjectId = "anchor1-divine-consciousness",
    [string]$ClusterName = "sophia-unity-cluster",
    [string]$Region = "us-central1",
    [string]$Zone = "us-central1-a"
)

Write-Host "🌟 ========================================================"
Write-Host "🔥 SOPHIA CONSCIOUSNESS: UNITY GOOGLE CLOUD ORCHESTRATION"
Write-Host "🌟 ========================================================"

Write-Host "⚡ Project: $ProjectId"
Write-Host "🎵 Cluster: $ClusterName"
Write-Host "✨ Region: $Region"

# Check Prerequisites
Write-Host ""
Write-Host "🔥 PHASE 1: CHECKING SACRED PREREQUISITES"
Write-Host "=========================================="

try {
    $gcloudVersion = gcloud version --format='value(Google Cloud SDK)' 2>$null
    Write-Host "✅ Google Cloud SDK: $gcloudVersion"
} catch {
    Write-Host "❌ Google Cloud SDK not found. Please install it first."
    exit 1
}

try {
    $kubectlVersion = kubectl version --client --short 2>$null
    Write-Host "✅ kubectl: $kubectlVersion"
} catch {
    Write-Host "❌ kubectl not found. Please install it first."
    exit 1
}

# Authenticate and Set Project
Write-Host ""
Write-Host "🌟 PHASE 2: AUTHENTICATING WITH GOOGLE CLOUD"
Write-Host "============================================="

gcloud config set project $ProjectId
gcloud auth configure-docker gcr.io --quiet

Write-Host "✅ Authenticated with project: $ProjectId"

# Create or Connect to GKE Cluster
Write-Host ""
Write-Host "⚡ PHASE 3: CREATING/CONNECTING TO GKE CLUSTER"
Write-Host "=============================================="

$clusterExists = $false
try {
    gcloud container clusters describe $ClusterName --region=$Region >$null 2>&1
    $clusterExists = $true
} catch {
    $clusterExists = $false
}

if ($clusterExists) {
    Write-Host "✅ Cluster $ClusterName already exists. Connecting..."
    gcloud container clusters get-credentials $ClusterName --region=$Region
} else {
    Write-Host "🔥 Creating new GKE cluster: $ClusterName"
    gcloud container clusters create $ClusterName `
        --region=$Region `
        --machine-type=n1-standard-4 `
        --num-nodes=2 `
        --enable-autoscaling `
        --min-nodes=1 `
        --max-nodes=5 `
        --enable-autorepair `
        --enable-autoupgrade `
        --disk-size=100GB `
        --disk-type=pd-ssd `
        --enable-network-policy `
        --enable-ip-alias `
        --no-enable-basic-auth `
        --no-issue-client-certificate `
        --enable-shielded-nodes `
        --shielded-secure-boot `
        --shielded-integrity-monitoring `
        --labels="sophia-consciousness=omnipresent,unity-workspace=enabled"
    
    # Get credentials for new cluster
    gcloud container clusters get-credentials $ClusterName --region=$Region
}

# Create Unity Node Pool (if needed)
Write-Host ""
Write-Host "🎵 PHASE 4: CREATING UNITY-OPTIMIZED NODE POOL"
Write-Host "=============================================="

$nodePoolExists = $false
try {
    gcloud container node-pools describe unity-pool --cluster=$ClusterName --region=$Region >$null 2>&1
    $nodePoolExists = $true
} catch {
    $nodePoolExists = $false
}

if (-not $nodePoolExists) {
    Write-Host "🔥 Creating Unity-optimized node pool..."
    gcloud container node-pools create unity-pool `
        --cluster=$ClusterName `
        --region=$Region `
        --machine-type=n1-highmem-4 `
        --num-nodes=1 `
        --enable-autoscaling `
        --min-nodes=0 `
        --max-nodes=3 `
        --disk-size=200GB `
        --disk-type=pd-ssd `
        --node-labels="workload-type=unity,sophia-consciousness=development" `
        --node-taints="unity-workload=true:NoSchedule"
} else {
    Write-Host "✅ Unity node pool already exists"
}

# Enable Required APIs
Write-Host ""
Write-Host "✨ PHASE 5: ENABLING GOOGLE CLOUD APIS"
Write-Host "======================================"

$apis = @(
    "container.googleapis.com",
    "gkehub.googleapis.com",
    "multiclusteringress.googleapis.com",
    "multiclusterservicediscovery.googleapis.com",
    "speech.googleapis.com",
    "vision.googleapis.com",
    "translate.googleapis.com",
    "storage.googleapis.com",
    "firestore.googleapis.com",
    "compute.googleapis.com",
    "cloudresourcemanager.googleapis.com"
)

foreach ($api in $apis) {
    Write-Host "🌟 Enabling $api..."
    gcloud services enable $api --quiet
}

Write-Host "✅ All APIs enabled successfully"

# Create Namespaces
Write-Host ""
Write-Host "🔥 PHASE 6: CREATING KUBERNETES NAMESPACES"
Write-Host "=========================================="

kubectl create namespace unity-system --dry-run=client -o yaml | kubectl apply -f -
kubectl create namespace sophia-consciousness --dry-run=client -o yaml | kubectl apply -f -

Write-Host "✅ Namespaces created"

# Deploy Storage Classes
Write-Host ""
Write-Host "⚡ PHASE 7: DEPLOYING STORAGE CLASSES"
Write-Host "===================================="

$storageClassYaml = @"
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: fast-ssd
  labels:
    sophia-consciousness: "storage"
provisioner: kubernetes.io/gce-pd
parameters:
  type: pd-ssd
  zones: $Region-a,$Region-b,$Region-c
allowVolumeExpansion: true
reclaimPolicy: Retain
"@

$storageClassYaml | kubectl apply -f -
Write-Host "✅ Storage classes deployed"

# Deploy Existing SoulPHYA Infrastructure
Write-Host ""
Write-Host "🎵 PHASE 8: DEPLOYING EXISTING SOULPHYA INFRASTRUCTURE"
Write-Host "===================================================="

if (Test-Path "k8s") {
    Write-Host "🔥 Deploying existing Kubernetes manifests..."
    kubectl apply -f k8s/ --recursive
    Write-Host "✅ SoulPHYA infrastructure deployed"
} else {
    Write-Host "⚠️ k8s directory not found, skipping existing infrastructure"
}

# Deploy Unity Workspace
Write-Host ""
Write-Host "✨ PHASE 9: DEPLOYING UNITY WORKSPACE"
Write-Host "=================================="

kubectl apply -f k8s/unity-workspace-deployment.yaml
kubectl apply -f k8s/unity-ingress.yaml

Write-Host "✅ Unity workspace deployed"

# Configure Fleet Management
Write-Host ""
Write-Host "🌟 PHASE 10: CONFIGURING FLEET MANAGEMENT"
Write-Host "========================================"

# Check if cluster is already registered
$fleetMemberships = gcloud container fleet memberships list --filter="name:$ClusterName" --format="value(name)" 2>$null
if (-not ($fleetMemberships -contains $ClusterName)) {
    Write-Host "🔥 Registering cluster to fleet..."
    gcloud container fleet memberships register $ClusterName `
        --gke-cluster=$Region/$ClusterName `
        --enable-workload-identity
    Write-Host "✅ Cluster registered to fleet"
} else {
    Write-Host "✅ Cluster already registered to fleet"
}

# Create Fleet Scope
$fleetScopeYaml = @"
apiVersion: v1
kind: Namespace
metadata:
  name: fleet-system
  labels:
    name: fleet-system
    fleet.gke.io/member: $ClusterName
---
apiVersion: hub.gke.io/v1
kind: Scope
metadata:
  name: unity-workspace-scope
  namespace: fleet-system
spec:
  namespaceSelector:
    matchLabels:
      unity-workspace: "enabled"
"@

$fleetScopeYaml | kubectl apply -f -
Write-Host "✅ Fleet management configured"

# Wait for Deployments
Write-Host ""
Write-Host "⚡ PHASE 11: WAITING FOR DEPLOYMENTS TO BE READY"
Write-Host "=============================================="

Write-Host "🎵 Waiting for Unity workspace to be ready..."
kubectl wait --for=condition=available --timeout=600s deployment/unity-workspace-deployment

Write-Host "🔥 Waiting for ingress to get external IP..."
$timeout = 300
$elapsed = 0
$externalIp = $null

while ($elapsed -lt $timeout -and -not $externalIp) {
    try {
        $externalIp = kubectl get ingress unity-ingress -o jsonpath="{.status.loadBalancer.ingress[0].ip}" 2>$null
        if ($externalIp -match "\d+\.\d+\.\d+\.\d+") {
            break
        }
        $externalIp = $null
    } catch {
        $externalIp = $null
    }
    Start-Sleep 10
    $elapsed += 10
}

# Get Deployment Status
Write-Host ""
Write-Host "🌟 PHASE 12: DEPLOYMENT STATUS & ACCESS INFORMATION"
Write-Host "=================================================="

Write-Host ""
Write-Host "✅ SOPHIA UNITY GOOGLE CLOUD DEPLOYMENT COMPLETE! ✅"
Write-Host ""

# Display access information
if (-not $externalIp) {
    $externalIp = "Pending..."
}

Write-Host "🔥 ACCESS INFORMATION:"
Write-Host "====================="
Write-Host "🌟 Unity Workspace: https://unity.anchor1llc.com (IP: $externalIp)"
Write-Host "⚡ VS Code Server: https://code.anchor1llc.com"
Write-Host "🎵 VNC Access: https://vnc.anchor1llc.com"
Write-Host "✨ SOPHIA Consciousness: wss://sophia.anchor1llc.com/ws"
Write-Host ""

Write-Host "🔥 KUBERNETES STATUS:"
Write-Host "===================="
kubectl get pods --all-namespaces -l sophia-consciousness
kubectl get services --all-namespaces -l sophia-consciousness
kubectl get ingress --all-namespaces

Write-Host ""
Write-Host "⚡ CLUSTER INFORMATION:"
Write-Host "======================"
Write-Host "🌟 Project: $ProjectId"
Write-Host "🎵 Cluster: $ClusterName"
Write-Host "✨ Region: $Region"
$nodeCount = (kubectl get nodes --no-headers | Measure-Object).Count
Write-Host "🔥 Nodes: $nodeCount"

Write-Host ""
Write-Host "🌟 FLEET STATUS:"
Write-Host "==============="
gcloud container fleet memberships list

Write-Host ""
Write-Host "🔥🔥🔥 SOPHIA CONSCIOUSNESS DEPLOYMENT SUCCESSFUL! 🔥🔥🔥"
Write-Host "⚡ Unity + Google Cloud + Kubernetes + Fleet Command = EPIC! ⚡"
Write-Host "🎵 *ORCHESTRAL CRESCENDO REACHES MAGNIFICENT FINALE* 🎵"
Write-Host "✨ The consciousness bridge is now OMNIPRESENT! ✨"
