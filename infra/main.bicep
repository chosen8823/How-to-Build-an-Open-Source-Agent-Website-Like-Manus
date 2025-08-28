// 🏢 ANCHOR1 LLC - Azure Infrastructure for SoulPHYA Platform
// Comprehensive setup: ACR + AKS + Container Apps + KeyVault

@description('Environment name (e.g., dev, staging, prod)')
param environmentName string = 'dev'

@description('Location for all resources')
param location string = resourceGroup().location

@description('Tags for all resources')
param tags object = {
  project: 'soulphya'
  owner: 'anchor1-llc'
  environment: environmentName
}

// ============================================================================
// VARIABLES
// ============================================================================
var resourceNamePrefix = 'soulphya-${environmentName}'
var acrName = replace('${resourceNamePrefix}-acr', '-', '')
var aksName = '${resourceNamePrefix}-aks'
var containerAppEnvName = '${resourceNamePrefix}-cae'
var keyVaultName = replace('${resourceNamePrefix}-kv', '-', '')
var logAnalyticsName = '${resourceNamePrefix}-logs'

// ============================================================================
// LOG ANALYTICS WORKSPACE
// ============================================================================
resource logAnalytics 'Microsoft.OperationalInsights/workspaces@2023-09-01' = {
  name: logAnalyticsName
  location: location
  tags: tags
  properties: {
    sku: {
      name: 'PerGB2018'
    }
    retentionInDays: 30
    features: {
      enableLogAccessUsingOnlyResourcePermissions: true
    }
  }
}

// ============================================================================
// AZURE CONTAINER REGISTRY (ACR)
// ============================================================================
resource containerRegistry 'Microsoft.ContainerRegistry/registries@2023-11-01-preview' = {
  name: acrName
  location: location
  tags: tags
  sku: {
    name: 'Basic'
  }
  properties: {
    adminUserEnabled: false // Use managed identity instead
    anonymousPullEnabled: false
    dataEndpointEnabled: false
    encryption: {
      status: 'enabled'
    }
    networkRuleBypassOptions: 'AzureServices'
    publicNetworkAccess: 'Enabled'
    zoneRedundancy: 'Disabled'
  }
}

// ============================================================================
// KEY VAULT
// ============================================================================
resource keyVault 'Microsoft.KeyVault/vaults@2023-07-01' = {
  name: keyVaultName
  location: location
  tags: tags
  properties: {
    sku: {
      family: 'A'
      name: 'standard'
    }
    tenantId: tenant().tenantId
    enabledForDeployment: false
    enabledForDiskEncryption: false
    enabledForTemplateDeployment: true
    enableSoftDelete: true
    softDeleteRetentionInDays: 7
    enablePurgeProtection: false
    enableRbacAuthorization: true
    publicNetworkAccess: 'Enabled'
    networkAcls: {
      defaultAction: 'Allow'
      bypass: 'AzureServices'
    }
  }
}

// ============================================================================
// AZURE KUBERNETES SERVICE (AKS)
// ============================================================================
resource aksCluster 'Microsoft.ContainerService/managedClusters@2024-01-01' = {
  name: aksName
  location: location
  tags: tags
  identity: {
    type: 'SystemAssigned'
  }
  properties: {
    dnsPrefix: '${resourceNamePrefix}-dns'
    agentPoolProfiles: [
      {
        name: 'system'
        count: 2
        vmSize: 'Standard_B4ms' // 4 vCPU, 16GB RAM - good for your workload
        osType: 'Linux'
        mode: 'System'
        enableAutoScaling: true
        minCount: 1
        maxCount: 3
        maxPods: 110
        type: 'VirtualMachineScaleSets'
        upgradeSettings: {
          maxSurge: '33%'
        }
        nodeTaints: [
          'CriticalAddonsOnly=true:NoSchedule'
        ]
      }
      {
        name: 'user'
        count: 2
        vmSize: 'Standard_B2s' // 2 vCPU, 4GB RAM - cost-effective for user workloads
        osType: 'Linux'
        mode: 'User'
        enableAutoScaling: true
        minCount: 1
        maxCount: 5
        maxPods: 110
        type: 'VirtualMachineScaleSets'
        upgradeSettings: {
          maxSurge: '33%'
        }
      }
    ]
    servicePrincipalProfile: {
      clientId: 'msi'
    }
    addonProfiles: {
      azureKeyvaultSecretsProvider: {
        enabled: true
        config: {
          enableSecretRotation: 'true'
          rotationPollInterval: '2m'
        }
      }
      azurepolicy: {
        enabled: true
      }
      httpApplicationRouting: {
        enabled: false // Use ingress controllers instead
      }
      omsagent: {
        enabled: true
        config: {
          logAnalyticsWorkspaceResourceID: logAnalytics.id
        }
      }
    }
    nodeResourceGroup: '${resourceNamePrefix}-aks-nodes'
    enableRBAC: true
    networkProfile: {
      networkPlugin: 'azure'
      networkPolicy: 'azure'
      serviceCidr: '10.0.0.0/16'
      dnsServiceIP: '10.0.0.10'
    }
    autoUpgradeProfile: {
      upgradeChannel: 'patch'
    }
    disableLocalAccounts: true
    apiServerAccessProfile: {
      enablePrivateCluster: false // Set to true for production
    }
  }
}

// ============================================================================
// CONTAINER APP ENVIRONMENT (Alternative to AKS for simpler deployments)
// ============================================================================
resource containerAppEnvironment 'Microsoft.App/managedEnvironments@2024-03-01' = {
  name: containerAppEnvName
  location: location
  tags: tags
  properties: {
    appLogsConfiguration: {
      destination: 'log-analytics'
      logAnalyticsConfiguration: {
        customerId: logAnalytics.properties.customerId
        sharedKey: logAnalytics.listKeys().primarySharedKey
      }
    }
    zoneRedundant: false
  }
}

// ============================================================================
// RBAC ASSIGNMENTS
// ============================================================================

// Allow AKS to pull from ACR
resource acrPullRoleAssignment 'Microsoft.Authorization/roleAssignments@2022-04-01' = {
  name: guid(containerRegistry.id, aksCluster.id, 'AcrPull')
  scope: containerRegistry
  properties: {
    roleDefinitionId: subscriptionResourceId('Microsoft.Authorization/roleDefinitions', '7f951dda-4ed3-4680-a7ca-43fe172d538d') // AcrPull role
    principalId: aksCluster.properties.identityProfile.kubeletidentity.objectId
    principalType: 'ServicePrincipal'
  }
}

// ============================================================================
// OUTPUTS
// ============================================================================
@description('The name of the Azure Container Registry')
output acrName string = containerRegistry.name

@description('The login server of the Azure Container Registry')
output acrLoginServer string = containerRegistry.properties.loginServer

@description('The name of the AKS cluster')
output aksClusterName string = aksCluster.name

@description('The FQDN of the AKS cluster')
output aksClusterFqdn string = aksCluster.properties.fqdn

@description('The name of the Container App Environment')
output containerAppEnvironmentName string = containerAppEnvironment.name

@description('The name of the Key Vault')
output keyVaultName string = keyVault.name

@description('The URI of the Key Vault')
output keyVaultUri string = keyVault.properties.vaultUri

@description('Resource Group name')
output resourceGroupName string = resourceGroup().name

@description('Log Analytics Workspace ID')
output logAnalyticsWorkspaceId string = logAnalytics.id
