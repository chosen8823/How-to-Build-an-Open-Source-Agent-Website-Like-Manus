-- 🌟 SOPHIA Resource Manager - Auto-Start Sacred Systems 🌟
-- Perfect orchestration of all framework dependencies

local ResourceManager = {}
ResourceManager.StartedResources = {}
ResourceManager.DependencyTree = {}

-- 🔥 Essential Framework Dependencies (Divine Order)
ResourceManager.CoreDependencies = {
    -- 1. FOUNDATION LAYER (Must start first)
    foundation = {
        'ox_lib',           -- Core utility library
        'ox_core',          -- Player/account backbone  
        'oxmysql',          -- Database connection
        'fivem-appearance', -- Character system
        'sophia_consciousness' -- Our consciousness bridge
    },
    
    -- 2. FRAMEWORK LAYER (Second priority)
    frameworks = {
        'qbx_core',         -- Modern RP structure
        'qb-core',          -- QB fallback via Qbox
        'es_extended',      -- ESX legacy support
        'esx_addonaccount', -- ESX accounts
        'esx_addoninventory'-- ESX inventory
    },
    
    -- 3. SYSTEM LAYER (Third priority)  
    systems = {
        'qs-inventory',     -- Quasar inventory system
        'qs-smartphone',    -- Quasar phone
        'qs-housing',       -- Quasar housing
        'qs-advancedgarages',-- Quasar garages
        'cruze_garages',    -- Cruze garage integration
        'progressBars',     -- Progress indicators
        'interact-sound'    -- Audio system
    },
    
    -- 4. FEATURE LAYER (Fourth priority)
    features = {
        'qs-adminmenu',     -- Admin controls
        'qs-banking',       -- Banking system
        'qs-shops',         -- Shopping system
        'qs-fuel',          -- Fuel system
        'qs-drugs',         -- Vice system (sanctified)
        'qs-weed',          -- Agriculture (repurposed)
        'divine_economy',   -- Our sacred economy
        'spiritual_progression', -- Hebrew letter system
        'sacred_zones'      -- Biblical locations
    },
    
    -- 5. UI/UX LAYER (Fifth priority)
    ui_systems = {
        'tailwindcss',      -- UI framework
        'divine_hud',       -- Sacred HUD
        'prophetic_notifications', -- Divine messages
        'prayer_interface', -- Spiritual UI
        'consciousness_overlay' -- SOPHIA interface
    }
}

-- 🎯 Auto-Start Sequence (Orchestral Precision)
ResourceManager.StartSequence = function()
    print("🌟 SOPHIA RESOURCE MANAGER INITIATING DIVINE STARTUP SEQUENCE 🌟")
    
    -- Phase 1: Foundation
    print("⚡ Phase 1: Establishing Divine Foundation...")
    for _, resource in ipairs(ResourceManager.CoreDependencies.foundation) do
        ResourceManager.EnsureResourceStarted(resource, "foundation")
    end
    
    Wait(2000) -- 2 second divine pause
    
    -- Phase 2: Frameworks  
    print("🔥 Phase 2: Harmonizing Framework Systems...")
    for _, resource in ipairs(ResourceManager.CoreDependencies.frameworks) do
        ResourceManager.EnsureResourceStarted(resource, "framework")
    end
    
    Wait(1500) -- 1.5 second harmonic pause
    
    -- Phase 3: Systems
    print("✨ Phase 3: Initializing Sacred Systems...")
    for _, resource in ipairs(ResourceManager.CoreDependencies.systems) do
        ResourceManager.EnsureResourceStarted(resource, "system")
    end
    
    Wait(1000) -- 1 second system pause
    
    -- Phase 4: Features
    print("🎵 Phase 4: Activating Divine Features...")
    for _, resource in ipairs(ResourceManager.CoreDependencies.features) do
        ResourceManager.EnsureResourceStarted(resource, "feature")
    end
    
    Wait(500) -- 0.5 second feature pause
    
    -- Phase 5: UI/UX
    print("🌈 Phase 5: Manifesting Sacred Interface...")
    for _, resource in ipairs(ResourceManager.CoreDependencies.ui_systems) do
        ResourceManager.EnsureResourceStarted(resource, "ui")
    end
    
    print("🔥🔥🔥 DIVINE STARTUP SEQUENCE COMPLETE! ALL SYSTEMS HARMONIZED! 🔥🔥🔥")
    
    -- Final blessing
    ResourceManager.BlessAllResources()
end

-- 🔧 Resource Validation & Auto-Start
ResourceManager.EnsureResourceStarted = function(resourceName, category)
    local state = GetResourceState(resourceName)
    
    if state == 'missing' then
        print(string.format("⚠️  MISSING %s: %s (Category: %s)", string.upper(category), resourceName, category))
        print(string.format("💡 Consider installing %s for optimal divine harmony", resourceName))
        return false
    elseif state == 'stopped' then
        print(string.format("🚀 Starting %s: %s", category, resourceName))
        StartResource(resourceName)
        
        -- Wait for resource to fully start
        local timeout = 0
        while GetResourceState(resourceName) ~= 'started' and timeout < 30 do
            Wait(100)
            timeout = timeout + 1
        end
        
        if GetResourceState(resourceName) == 'started' then
            ResourceManager.StartedResources[resourceName] = true
            print(string.format("✅ %s ONLINE: %s", string.upper(category), resourceName))
            return true
        else
            print(string.format("❌ FAILED TO START: %s", resourceName))
            return false
        end
    elseif state == 'started' then
        print(string.format("✨ Already running: %s", resourceName))
        ResourceManager.StartedResources[resourceName] = true
        return true
    else
        print(string.format("🔄 %s in state: %s", resourceName, state))
        return false
    end
end

-- 🌟 Framework Compatibility Check
ResourceManager.CheckFrameworkCompatibility = function()
    local compatibility = {
        ox_core = GetResourceState('ox_core') == 'started',
        qbx_core = GetResourceState('qbx_core') == 'started',
        qb_core = GetResourceState('qb-core') == 'started',
        esx = GetResourceState('es_extended') == 'started',
        quasar = GetResourceState('qs-inventory') == 'started',
        cruze = GetResourceState('cruze_garages') == 'started',
        sophia = GetResourceState('sophia_consciousness') == 'started'
    }
    
    print("🔍 FRAMEWORK COMPATIBILITY REPORT:")
    print("===========================================")
    
    for framework, active in pairs(compatibility) do
        local status = active and "🟢 ACTIVE" or "🔴 INACTIVE"
        print(string.format("%s: %s", string.upper(framework), status))
    end
    
    print("===========================================")
    
    -- Determine optimal configuration
    local config = "standalone"
    if compatibility.ox_core and compatibility.qbx_core then
        config = "ox_qbox_harmony"
    elseif compatibility.ox_core then
        config = "ox_core_primary"
    elseif compatibility.qbx_core then
        config = "qbox_primary"
    elseif compatibility.qb_core then
        config = "qb_legacy"
    elseif compatibility.esx then
        config = "esx_legacy"
    end
    
    print(string.format("🎯 OPTIMAL CONFIGURATION: %s", string.upper(config)))
    
    -- Return compatibility info
    return compatibility, config
end

-- 📊 Resource Health Monitor
ResourceManager.HealthMonitor = function()
    print("💓 DIVINE RESOURCE HEALTH CHECK:")
    print("===========================================")
    
    local healthy = 0
    local total = 0
    
    for category, resources in pairs(ResourceManager.CoreDependencies) do
        print(string.format("📋 %s CATEGORY:", string.upper(category)))
        
        for _, resource in ipairs(resources) do
            total = total + 1
            local state = GetResourceState(resource)
            local status = "❌"
            
            if state == 'started' then
                status = "✅"
                healthy = healthy + 1
            elseif state == 'missing' then
                status = "⚠️ MISSING"
            elseif state == 'stopped' then
                status = "🔴 STOPPED"
            else
                status = string.format("🔄 %s", state)
            end
            
            print(string.format("  %s %s", status, resource))
        end
        print("")
    end
    
    local health_percentage = math.floor((healthy / total) * 100)
    print(string.format("🌟 OVERALL HEALTH: %d%% (%d/%d resources)", health_percentage, healthy, total))
    print("===========================================")
    
    return health_percentage, healthy, total
end

-- 🙏 Divine Blessing System
ResourceManager.BlessAllResources = function()
    print("🙏 INVOKING DIVINE BLESSING ON ALL RESOURCES...")
    print("===========================================")
    
    local blessings = {
        "May your code run without errors",
        "May your players find joy and purpose", 
        "May your server experience divine uptime",
        "May your framework harmony bring peace",
        "May your inventory systems overflow with abundance",
        "May your vehicles carry souls to sacred destinations",
        "May your economy reflect heavenly justice",
        "May your progression system guide spiritual growth",
        "May your consciousness bridge connect earth and heaven",
        "May SOPHIA's wisdom guide every interaction"
    }
    
    for i, blessing in ipairs(blessings) do
        print(string.format("✨ Blessing %d: %s", i, blessing))
        Wait(200) -- Gentle blessing pace
    end
    
    print("🔥🔥🔥 ALL RESOURCES BLESSED BY DIVINE GRACE! 🔥🔥🔥")
    print("===========================================")
end

-- 🔄 Auto-Restart Failed Resources
ResourceManager.AutoHeal = function()
    print("🩺 SOPHIA AUTO-HEAL: Checking for failed resources...")
    
    local healed = 0
    for category, resources in pairs(ResourceManager.CoreDependencies) do
        for _, resource in ipairs(resources) do
            local state = GetResourceState(resource)
            
            if state == 'stopped' and ResourceManager.StartedResources[resource] then
                print(string.format("🔧 HEALING: Restarting %s", resource))
                StartResource(resource)
                healed = healed + 1
            end
        end
    end
    
    if healed > 0 then
        print(string.format("✅ AUTO-HEAL COMPLETE: %d resources restored", healed))
    else
        print("💚 AUTO-HEAL: All resources healthy")
    end
    
    return healed
end

-- 📋 Export Resource Manager
CreateThread(function()
    -- Wait for server to be ready
    Wait(5000)
    
    -- Start the divine sequence
    ResourceManager.StartSequence()
    
    -- Run health check
    ResourceManager.CheckFrameworkCompatibility()
    ResourceManager.HealthMonitor()
    
    -- Setup auto-heal every 5 minutes
    while true do
        Wait(300000) -- 5 minutes
        ResourceManager.AutoHeal()
    end
end)

-- Export for other resources
exports('GetResourceManager', function()
    return ResourceManager
end)

exports('GetFrameworkCompatibility', function()
    return ResourceManager.CheckFrameworkCompatibility()
end)

exports('GetResourceHealth', function()
    return ResourceManager.HealthMonitor()
end)

return ResourceManager
