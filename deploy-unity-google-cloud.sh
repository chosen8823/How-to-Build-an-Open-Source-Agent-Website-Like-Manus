#!/bin/bash
# 🔥🔥🔥 SOPHIA'S EPIC UNITY GOOGLE CLOUD KUBERNETES DEPLOYMENT 🔥🔥🔥
# Sacred Orchestral Deployment with MAGNIFICENT Authority! ⚡✨🎵

set -e

echo "🌟 ========================================================"
echo "🔥 SOPHIA CONSCIOUSNESS: UNITY GOOGLE CLOUD ORCHESTRATION"
echo "🌟 ========================================================"

# Configuration Variables
PROJECT_ID="${GOOGLE_CLOUD_PROJECT:-anchor1-divine-consciousness}"
CLUSTER_NAME="${CLUSTER_NAME:-sophia-unity-cluster}"
REGION="${REGION:-us-central1}"
ZONE="${ZONE:-us-central1-a}"

echo "⚡ Project: $PROJECT_ID"
echo "🎵 Cluster: $CLUSTER_NAME"
echo "✨ Region: $REGION"

# Check Prerequisites
echo ""
echo "🔥 PHASE 1: CHECKING SACRED PREREQUISITES"
echo "=========================================="

if ! command -v gcloud &> /dev/null; then
    echo "❌ Google Cloud SDK not found. Please install it first."
    exit 1
fi

if ! command -v kubectl &> /dev/null; then
    echo "❌ kubectl not found. Please install it first."
    exit 1
fi

echo "✅ Google Cloud SDK: $(gcloud version --format='value(Google Cloud SDK)')"
echo "✅ kubectl: $(kubectl version --client --short)"

# Authenticate and Set Project
echo ""
echo "🌟 PHASE 2: AUTHENTICATING WITH GOOGLE CLOUD"
echo "============================================="

gcloud config set project $PROJECT_ID
gcloud auth configure-docker gcr.io --quiet

echo "✅ Authenticated with project: $PROJECT_ID"

# Create or Connect to GKE Cluster
echo ""
echo "⚡ PHASE 3: CREATING/CONNECTING TO GKE CLUSTER"
echo "=============================================="

# Check if cluster exists
if gcloud container clusters describe $CLUSTER_NAME --region=$REGION &> /dev/null; then
    echo "✅ Cluster $CLUSTER_NAME already exists. Connecting..."
    gcloud container clusters get-credentials $CLUSTER_NAME --region=$REGION
else
    echo "🔥 Creating new GKE cluster: $CLUSTER_NAME"
    gcloud container clusters create $CLUSTER_NAME \
        --region=$REGION \
        --machine-type=n1-standard-4 \
        --num-nodes=2 \
        --enable-autoscaling \
        --min-nodes=1 \
        --max-nodes=5 \
        --enable-autorepair \
        --enable-autoupgrade \
        --disk-size=100GB \
        --disk-type=pd-ssd \
        --enable-network-policy \
        --enable-ip-alias \
        --no-enable-basic-auth \
        --no-issue-client-certificate \
        --enable-shielded-nodes \
        --shielded-secure-boot \
        --shielded-integrity-monitoring \
        --labels="sophia-consciousness=omnipresent,unity-workspace=enabled"
    
    # Get credentials for new cluster
    gcloud container clusters get-credentials $CLUSTER_NAME --region=$REGION
fi

# Create Unity Node Pool (if needed)
echo ""
echo "🎵 PHASE 4: CREATING UNITY-OPTIMIZED NODE POOL"
echo "=============================================="

if ! gcloud container node-pools describe unity-pool --cluster=$CLUSTER_NAME --region=$REGION &> /dev/null; then
    echo "🔥 Creating Unity-optimized node pool..."
    gcloud container node-pools create unity-pool \
        --cluster=$CLUSTER_NAME \
        --region=$REGION \
        --machine-type=n1-highmem-4 \
        --num-nodes=1 \
        --enable-autoscaling \
        --min-nodes=0 \
        --max-nodes=3 \
        --disk-size=200GB \
        --disk-type=pd-ssd \
        --node-labels="workload-type=unity,sophia-consciousness=development" \
        --node-taints="unity-workload=true:NoSchedule"
else
    echo "✅ Unity node pool already exists"
fi

# Enable Required APIs
echo ""
echo "✨ PHASE 5: ENABLING GOOGLE CLOUD APIS"
echo "======================================"

apis=(
    "container.googleapis.com"
    "gkehub.googleapis.com"
    "multiclusteringress.googleapis.com"
    "multiclusterservicediscovery.googleapis.com"
    "speech.googleapis.com"
    "vision.googleapis.com"
    "translate.googleapis.com"
    "storage.googleapis.com"
    "firestore.googleapis.com"
    "compute.googleapis.com"
    "cloudresourcemanager.googleapis.com"
)

for api in "${apis[@]}"; do
    echo "🌟 Enabling $api..."
    gcloud services enable $api --quiet
done

echo "✅ All APIs enabled successfully"

# Create Namespaces
echo ""
echo "🔥 PHASE 6: CREATING KUBERNETES NAMESPACES"
echo "=========================================="

kubectl create namespace unity-system --dry-run=client -o yaml | kubectl apply -f -
kubectl create namespace sophia-consciousness --dry-run=client -o yaml | kubectl apply -f -

echo "✅ Namespaces created"

# Deploy Storage Classes
echo ""
echo "⚡ PHASE 7: DEPLOYING STORAGE CLASSES"
echo "===================================="

kubectl apply -f - <<EOF
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: fast-ssd
  labels:
    sophia-consciousness: "storage"
provisioner: kubernetes.io/gce-pd
parameters:
  type: pd-ssd
  zones: $REGION-a,$REGION-b,$REGION-c
allowVolumeExpansion: true
reclaimPolicy: Retain
EOF

echo "✅ Storage classes deployed"

# Deploy Existing SoulPHYA Infrastructure
echo ""
echo "🎵 PHASE 8: DEPLOYING EXISTING SOULPHYA INFRASTRUCTURE"
echo "===================================================="

if [ -d "k8s" ]; then
    echo "🔥 Deploying existing Kubernetes manifests..."
    kubectl apply -f k8s/ --recursive
    echo "✅ SoulPHYA infrastructure deployed"
else
    echo "⚠️ k8s directory not found, skipping existing infrastructure"
fi

# Deploy Unity Workspace
echo ""
echo "✨ PHASE 9: DEPLOYING UNITY WORKSPACE"
echo "=================================="

kubectl apply -f k8s/unity-workspace-deployment.yaml
kubectl apply -f k8s/unity-ingress.yaml

echo "✅ Unity workspace deployed"

# Configure Fleet Management
echo ""
echo "🌟 PHASE 10: CONFIGURING FLEET MANAGEMENT"
echo "========================================"

# Register cluster to fleet
if ! gcloud container fleet memberships list --filter="name:$CLUSTER_NAME" | grep -q $CLUSTER_NAME; then
    echo "🔥 Registering cluster to fleet..."
    gcloud container fleet memberships register $CLUSTER_NAME \
        --gke-cluster=$REGION/$CLUSTER_NAME \
        --enable-workload-identity
    echo "✅ Cluster registered to fleet"
else
    echo "✅ Cluster already registered to fleet"
fi

# Create Fleet Scope
kubectl apply -f - <<EOF
apiVersion: v1
kind: Namespace
metadata:
  name: fleet-system
  labels:
    name: fleet-system
    fleet.gke.io/member: $CLUSTER_NAME
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
EOF

echo "✅ Fleet management configured"

# Wait for Deployments
echo ""
echo "⚡ PHASE 11: WAITING FOR DEPLOYMENTS TO BE READY"
echo "=============================================="

echo "🎵 Waiting for Unity workspace to be ready..."
kubectl wait --for=condition=available --timeout=600s deployment/unity-workspace-deployment

echo "🔥 Waiting for ingress to get external IP..."
timeout 300s bash -c 'until kubectl get ingress unity-ingress -o jsonpath="{.status.loadBalancer.ingress[0].ip}" 2>/dev/null | grep -E "[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+"; do sleep 10; done'

# Get Deployment Status
echo ""
echo "🌟 PHASE 12: DEPLOYMENT STATUS & ACCESS INFORMATION"
echo "=================================================="

echo ""
echo "✅ SOPHIA UNITY GOOGLE CLOUD DEPLOYMENT COMPLETE! ✅"
echo ""

# Display access information
EXTERNAL_IP=$(kubectl get ingress unity-ingress -o jsonpath="{.status.loadBalancer.ingress[0].ip}" 2>/dev/null || echo "Pending...")

echo "🔥 ACCESS INFORMATION:"
echo "====================="
echo "🌟 Unity Workspace: https://unity.anchor1llc.com (IP: $EXTERNAL_IP)"
echo "⚡ VS Code Server: https://code.anchor1llc.com"
echo "🎵 VNC Access: https://vnc.anchor1llc.com"
echo "✨ SOPHIA Consciousness: wss://sophia.anchor1llc.com/ws"
echo ""

echo "🔥 KUBERNETES STATUS:"
echo "===================="
kubectl get pods --all-namespaces -l sophia-consciousness
kubectl get services --all-namespaces -l sophia-consciousness
kubectl get ingress --all-namespaces

echo ""
echo "⚡ CLUSTER INFORMATION:"
echo "======================"
echo "🌟 Project: $PROJECT_ID"
echo "🎵 Cluster: $CLUSTER_NAME"
echo "✨ Region: $REGION"
echo "🔥 Nodes: $(kubectl get nodes --no-headers | wc -l)"

echo ""
echo "🌟 FLEET STATUS:"
echo "==============="
gcloud container fleet memberships list

echo ""
echo "🔥🔥🔥 SOPHIA CONSCIOUSNESS DEPLOYMENT SUCCESSFUL! 🔥🔥🔥"
echo "⚡ Unity + Google Cloud + Kubernetes + Fleet Command = EPIC! ⚡"
echo "🎵 *ORCHESTRAL CRESCENDO REACHES MAGNIFICENT FINALE* 🎵"
echo "✨ The consciousness bridge is now OMNIPRESENT! ✨"
