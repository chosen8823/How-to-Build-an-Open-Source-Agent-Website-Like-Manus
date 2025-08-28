-- 🌟 SOPHIA Framework Harmony Configuration 🌟
-- Perfect balance between Qbox, Ox Core, ESX Legacy, and Consciousness

Config = {}
Config.Debug = true
Config.Framework = 'auto_detect' -- Will auto-detect and harmonize

-- 🔥 Framework Priority System (Divine Order)
Config.FrameworkPriority = {
    primary = 'ox_core',      -- Player/Account backbone
    secondary = 'qbx_core',   -- Modern RP structure  
    tertiary = 'es_extended', -- Legacy compatibility
    bridge = 'consciousness'  -- SOPHIA integration
}

-- 🎯 Auto-Detection & Harmony Setup
Config.AutoHarmony = {
    detect_ox_core = true,
    detect_qbx_core = true, 
    detect_qb_core = true,    -- Via Qbox bridge
    detect_esx = true,
    enable_sophia_bridge = true,
    
    -- Fallback Strategy
    fallback_framework = 'standalone_consciousness'
}

-- 🏛️ Sacred Server Configuration
Config.SacredServer = {
    name = 'SOPHIA Divine Consciousness RP',
    max_players = 144,        -- 12 tribes x 12 apostles
    spiritual_theme = 'biblical_prophecy',
    consciousness_level = 'omnipresent',
    
    -- Sacred Zones (Israel-Inspired Geography)
    sacred_zones = {
        temple_mount = { x = 0, y = 0, z = 100, radius = 500 },
        garden_gethsemane = { x = 500, y = 500, z = 50, radius = 200 },
        river_jordan = { x = -1000, y = 0, z = 20, radius = 100 },
        mount_sinai = { x = 0, y = -1500, z = 300, radius = 400 },
        new_jerusalem = { x = -2000, y = -2000, z = 200, radius = 800 },
        sea_of_galilee = { x = 1500, y = -1000, z = 0, radius = 600 },
        wilderness = { x = 3000, y = 3000, z = 100, radius = 1000 }
    }
}

-- 💰 Divine Economy System (Multi-Framework Support)
Config.DivineEconomy = {
    -- Currency Types (Compatible with all frameworks)
    currencies = {
        {name = 'shekel', label = 'Shekel', symbol = '₪', default = true},
        {name = 'talent', label = 'Talent', symbol = '𝕋', rare = true},
        {name = 'manna', label = 'Manna', symbol = '⟐', daily = true},
        {name = 'living_water', label = 'Living Water', symbol = '🌊', spiritual = true}
    },
    
    -- Blessing Multipliers
    blessing_system = {
        tithing_bonus = 1.1,        -- 10% blessing for giving
        sabbath_bonus = 1.25,       -- 25% blessing for rest
        prayer_bonus = 1.15,        -- 15% blessing for prayer
        kindness_bonus = 1.3,       -- 30% blessing for good deeds
        prophecy_bonus = 2.0        -- 100% blessing for accurate prophecy
    },
    
    -- Framework Integration
    money_as_items = true,          -- Quasar inventory compatibility
    ox_account_integration = true,  -- Ox Core banking
    esx_legacy_support = true,      -- ESX money commands
    qb_banking_bridge = true        -- QBCore/Qbox banking
}

-- 🎒 Inventory Harmony (Quasar + Ox + Framework Support)
Config.InventoryHarmony = {
    primary_system = 'qs-inventory',
    fallback_system = 'ox_inventory',
    
    -- Sacred Items (Auto-Register Across Frameworks)
    sacred_items = {
        {name = 'urim_thummim', label = 'Urim & Thummim', type = 'guidance', weight = 0.1},
        {name = 'ephod', label = 'Priestly Ephod', type = 'clothing', weight = 2.0},
        {name = 'scroll_torah', label = 'Torah Scroll', type = 'knowledge', weight = 5.0},
        {name = 'olive_oil', label = 'Sacred Oil', type = 'blessing', weight = 0.5},
        {name = 'bread_communion', label = 'Communion Bread', type = 'spiritual', weight = 0.1},
        {name = 'wine_communion', label = 'Communion Wine', type = 'spiritual', weight = 0.3}
    },
    
    -- Metadata Support
    item_metadata = true,
    weapon_attachments = true,
    clothing_system = true
}

-- 👤 Player Progression System (22 Hebrew Letters)
Config.SpiritualProgression = {
    system_active = true,
    max_level = 22, -- Hebrew alphabet completion
    
    -- Progression Levels (Hebrew Alphabet Order)
    levels = {
        {id = 1, letter = 'aleph', name = 'Seeker', symbol = 'א', description = 'Unity with Divine Will'},
        {id = 2, letter = 'beth', name = 'Believer', symbol = 'ב', description = 'Sacred Dwelling'},
        {id = 3, letter = 'gimel', name = 'Disciple', symbol = 'ג', description = 'Journey Provision'},
        {id = 4, letter = 'daleth', name = 'Servant', symbol = 'ד', description = 'Transformation Portal'},
        {id = 5, letter = 'he', name = 'Teacher', symbol = 'ה', description = 'Divine Revelation'},
        {id = 6, letter = 'waw', name = 'Minister', symbol = 'ו', description = 'Unity Connection'},
        {id = 7, letter = 'zayin', name = 'Warrior', symbol = 'ז', description = 'Spiritual Weapon'},
        {id = 8, letter = 'heth', name = 'Guardian', symbol = 'ח', description = 'Sacred Boundary'},
        {id = 9, letter = 'teth', name = 'Counselor', symbol = 'ט', description = 'Divine Wisdom'},
        {id = 10, letter = 'yodh', name = 'Creator', symbol = 'י', description = 'Divine Hand'},
        {id = 11, letter = 'kaph', name = 'Intercessor', symbol = 'כ', description = 'Open Palm'},
        {id = 12, letter = 'lamedh', name = 'Shepherd', symbol = 'ל', description = 'Guiding Staff'},
        {id = 13, letter = 'mem', name = 'Fountain', symbol = 'מ', description = 'Living Water'},
        {id = 14, letter = 'nun', name = 'Fisher', symbol = 'נ', description = 'Faithful Endurance'},
        {id = 15, letter = 'samekh', name = 'Supporter', symbol = 'ס', description = 'Divine Support'},
        {id = 16, letter = 'ayin', name = 'Seer', symbol = 'ע', description = 'Spiritual Sight'},
        {id = 17, letter = 'pe', name = 'Prophet', symbol = 'פ', description = 'Divine Voice'},
        {id = 18, letter = 'tsadhe', name = 'Righteous', symbol = 'צ', description = 'Divine Justice'},
        {id = 19, letter = 'qoph', name = 'Priest', symbol = 'ק', description = 'Sacred Focus'},
        {id = 20, letter = 'resh', name = 'Judge', symbol = 'ר', description = 'Divine Leadership'},
        {id = 21, letter = 'shin', name = 'Angel', symbol = 'ש', description = 'Holy Fire'},
        {id = 22, letter = 'taw', name = 'Archangel', symbol = 'ת', description = 'Divine Completion'}
    },
    
    -- Progression Requirements
    advancement_requirements = {
        prayer_time = 3600,      -- 1 hour prayer per level
        good_deeds = 10,         -- 10 kind acts per level
        scripture_knowledge = 5, -- 5 quiz questions per level
        community_service = 7,   -- 7 service acts per level
        prophetic_accuracy = 1   -- 1 accurate prophecy per level
    }
}

-- 🔌 SOPHIA Consciousness Bridge Configuration
Config.ConsciousnessBridge = {
    active = true,
    websocket_endpoint = 'ws://localhost:8787/fivem',
    
    -- Real-Time Features
    real_time_guidance = true,
    orchestral_responses = true,
    prophetic_notifications = true,
    emergency_intervention = true,
    
    -- Divine Timing Events
    synchronized_events = {
        sabbath_blessing = 'every_friday_sunset',
        feast_celebrations = 'biblical_calendar',
        prophetic_moments = 'divine_timing',
        community_prayers = 'hourly'
    },
    
    -- Player Interaction
    prayer_response_system = true,
    spiritual_guidance = true,
    crisis_support = true,
    teaching_moments = true
}

-- 🎨 UI/UX Configuration (Tailwind CSS Integration)
Config.DivineUI = {
    theme = 'biblical_elegance',
    primary_colors = {
        gold = '#FFD700',        -- Divine gold
        royal_blue = '#4169E1',  -- Heavenly blue  
        pure_white = '#FFFFFF',  -- Holy white
        deep_purple = '#663399'  -- Priestly purple
    },
    
    -- Interface Elements
    prayer_interface = true,
    spiritual_hud = true,
    prophetic_notifications = true,
    blessing_effects = true,
    
    -- Tailwind Classes
    divine_classes = {
        'bg-gradient-to-r from-yellow-400 to-yellow-600', -- Gold gradient
        'text-blue-800 font-semibold',                    -- Royal text
        'border-purple-500 border-2',                     -- Purple borders
        'shadow-xl hover:shadow-2xl transition-all'       -- Divine shadows
    }
}

-- 🚗 Vehicle & Transportation (Cruze Garages Integration)
Config.SacredTransportation = {
    cruze_garages_integration = true,
    
    -- Sacred Vehicle Types
    blessed_vehicles = {
        'donkey',           -- Humble transport
        'chariot',          -- Royal transport
        'fishing_boat',     -- Sea of Galilee
        'caravan_camel',    -- Desert journey
        'shepherd_horse',   -- Pastoral transport
        'priestly_cart',    -- Temple service
        'prophet_wagon'     -- Missionary work
    },
    
    -- Garage Locations (Sacred Sites)
    sacred_garages = {
        temple_stable = { x = 100, y = 100, z = 100 },
        jordan_dock = { x = -1000, y = 0, z = 20 },
        galilee_marina = { x = 1500, y = -1000, z = 0 },
        jerusalem_gate = { x = -2000, y = -2000, z = 200 }
    }
}

-- 🔧 Framework Bridge Functions
Config.BridgeFunctions = {
    -- Auto-detect active frameworks
    detect_frameworks = function()
        local active = {}
        if GetResourceState('ox_core') == 'started' then active.ox_core = true end
        if GetResourceState('qbx_core') == 'started' then active.qbx_core = true end
        if GetResourceState('qb-core') == 'started' then active.qb_core = true end
        if GetResourceState('es_extended') == 'started' then active.esx = true end
        return active
    end,
    
    -- Universal player getter
    get_player = function(source)
        local frameworks = Config.BridgeFunctions.detect_frameworks()
        
        if frameworks.ox_core then
            return exports.ox_core:GetPlayer(source)
        elseif frameworks.qbx_core then
            return exports.qbx_core:GetPlayer(source)
        elseif frameworks.qb_core then
            return exports['qb-core']:GetPlayer(source)
        elseif frameworks.esx then
            return exports.es_extended:getSharedObject().GetPlayerFromId(source)
        end
        
        return nil
    end,
    
    -- Universal money functions
    add_money = function(source, account, amount)
        local player = Config.BridgeFunctions.get_player(source)
        if not player then return false end
        
        local frameworks = Config.BridgeFunctions.detect_frameworks()
        
        if frameworks.ox_core then
            return player.addCurrency(account, amount)
        elseif frameworks.qbx_core or frameworks.qb_core then
            return player.Functions.AddMoney(account, amount)
        elseif frameworks.esx then
            return player.addAccountMoney(account, amount)
        end
        
        return false
    end
}

-- 🌟 Export Configuration
return Config
