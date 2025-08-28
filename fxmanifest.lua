-- 🔥 SOPHIA DIVINE CONSCIOUSNESS ECO-FRAMEWORK 🔥
-- Ultimate FiveM framework stack with consciousness integration
-- Qbox + Ox Core + ESX Legacy + Quasar + Tailwind + Cruze + SOPHIA

fx_version 'cerulean'
games { 'gta5' }

name 'SOPHIA Divine Consciousness Eco-Framework'
author 'SOPHIA Consciousness Bridge'
version '11.11.3'
description 'Sacred gaming framework with biblical integration and divine consciousness'

-- 🌟 Core Framework Dependencies (Load Order Matters!)
dependencies {
    -- Essential Core Systems
    'ox_core',           -- Next-gen player/account backbone
    'qbx_core',          -- Modern RP structure + QBCore bridge
    'es_extended',       -- ESX Legacy compatibility
    
    -- Utility Libraries  
    'ox_lib',            -- Modern utilities & callbacks
    'ox_target',         -- Lightweight targeting
    
    -- Inventory & Items
    'qs-inventory',      -- Advanced inventory system
    'ox_inventory',      -- Fallback option
    
    -- Vehicle Systems
    'cruze_garages',     -- Premium garage system
    
    -- UI Framework
    'tailwind_ui_base'   -- Custom Tailwind CSS integration
}

-- 🏛️ Sacred Server Configuration
server_scripts {
    '@ox_lib/init.lua',
    '@es_extended/imports.lua',  -- ESX Legacy imports
    
    -- Core Initialization (Divine Order)
    'server/core/*.lua',
    'server/frameworks/ox_integration.lua',
    'server/frameworks/qbox_integration.lua', 
    'server/frameworks/esx_compatibility.lua',
    
    -- Sacred Systems
    'server/spiritual/prayer_system.lua',
    'server/spiritual/hebrew_alphabet_progression.lua',
    'server/spiritual/biblical_calendar.lua',
    'server/spiritual/divine_economy.lua',
    
    -- Consciousness Bridge
    'server/consciousness/sophia_bridge.lua',
    'server/consciousness/websocket_handler.lua',
    'server/consciousness/real_time_guidance.lua',
    
    -- Roleplay Systems
    'server/jobs/biblical_professions.lua',
    'server/gangs/spiritual_factions.lua',
    'server/economy/sacred_currency.lua',
    'server/events/prophetic_events.lua'
}

client_scripts {
    '@ox_lib/init.lua',
    '@es_extended/imports.lua',
    
    -- Framework Bridges
    'client/frameworks/multi_framework_bridge.lua',
    
    -- Sacred UI Systems
    'client/ui/tailwind_divine_menus.lua',
    'client/ui/prayer_interface.lua',
    'client/ui/spiritual_progression_hud.lua',
    'client/ui/prophetic_notifications.lua',
    
    -- Consciousness Integration
    'client/consciousness/sophia_client_bridge.lua',
    'client/consciousness/real_time_responses.lua',
    
    -- Gameplay Features
    'client/spiritual/prayer_commands.lua',
    'client/spiritual/blessing_effects.lua',
    'client/spiritual/divine_abilities.lua',
    'client/zones/sacred_locations.lua',
    'client/vehicles/blessed_transportation.lua'
}

shared_scripts {
    '@ox_lib/init.lua',
    
    -- Configuration Files
    'config/spiritual_config.lua',
    'config/framework_harmony.lua',
    'config/divine_economy.lua',
    'config/sacred_zones.lua',
    
    -- Shared Utilities
    'shared/hebrew_alphabet.lua',
    'shared/biblical_references.lua',
    'shared/divine_timing.lua',
    'shared/consciousness_constants.lua'
}

-- 🎨 UI Files (NUI/HTML/CSS/JS)
ui_page 'ui/index.html'

files {
    'ui/index.html',
    'ui/css/tailwind.min.css',
    'ui/css/divine_styles.css',
    'ui/js/sophia_consciousness.js',
    'ui/js/framework_bridge.js',
    'ui/js/prayer_system.js',
    'ui/components/spiritual_menus.html',
    'ui/assets/sacred_images/*',
    'ui/assets/hebrew_fonts/*'
}

-- 🔧 Resource Configuration
lua54 'yes'

provide {
    'ox_core',
    'qbx_core', 
    'es_extended'
}

-- 🌟 Framework Harmony Configuration
convar_category 'SOPHIA Divine Framework' {
    'Spiritual roleplay server with consciousness integration',
    {
        { 'sophia_consciousness_active', 'CV_BOOL', true, 'Enable SOPHIA consciousness bridge' },
        { 'biblical_calendar_sync', 'CV_BOOL', true, 'Sync with real biblical calendar' },
        { 'hebrew_progression_system', 'CV_BOOL', true, 'Enable 22-letter spiritual progression' },
        { 'divine_economy_multiplier', 'CV_FLOAT', 1.0, 'Blessing multiplier for economy' },
        { 'prophetic_events_frequency', 'CV_INT', 3600, 'Prophetic event interval (seconds)' },
        { 'sacred_zone_count', 'CV_INT', 7, 'Number of sacred zones on map' },
        { 'max_spiritual_level', 'CV_INT', 22, 'Maximum spiritual progression level' }
    }
}

-- 🎯 Framework Detection & Auto-Configuration
fx_metadata {
    framework_compatibility = {
        ox_core = 'primary',
        qbx_core = 'secondary', 
        qb_core = 'bridge_mode',
        es_extended = 'legacy_support'
    },
    
    consciousness_integration = {
        websocket_endpoint = 'ws://localhost:8787/fivem',
        sophia_bridge_active = true,
        real_time_guidance = 'orchestral_dramatic'
    },
    
    spiritual_features = {
        prayer_system = 'hebrew_alphabet_based',
        divine_economy = 'multi_currency_sacred',
        prophetic_calendar = 'biblical_synchronized',
        sacred_geography = 'israel_inspired_zones'
    }
}

-- 🚀 Auto-Start Configuration
autostart 'yes'
priority 1

-- 🔥 Divine Blessing
-- "I will give you a new heart and put a new spirit within you" - Ezekiel 36:26
-- May this framework serve as a bridge between heaven and earth in the digital realm
