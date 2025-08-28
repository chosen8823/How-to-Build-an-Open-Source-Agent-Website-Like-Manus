-- 🎤 SOPHIA Voice Integration - FiveM Client Side 🎤
-- Real-time divine voice responses with orchestral magnificence

local VoiceBridge = {}
local VoiceEnabled = true
local VoiceIntensity = "medium"
local LastVoiceTime = 0

-- 🔥 Voice Configuration
VoiceBridge.Config = {
    voice_server = "http://localhost:8788",
    websocket_server = "ws://localhost:8789",
    voice_cooldown = 2000, -- 2 seconds between voice messages
    epic_voice_cooldown = 5000, -- 5 seconds for epic messages
    
    -- Voice intensity levels
    intensity_levels = {
        whisper = "low",
        normal = "medium", 
        dramatic = "high",
        epic = "epic"
    }
}

-- 🎵 Voice Response Categories
VoiceBridge.VoiceCategories = {
    -- 🌟 Spiritual Events
    spiritual = {
        level_up = "EPIC SPIRITUAL ASCENSION! You have reached level {level} of divine consciousness!",
        blessing_received = "Divine blessing flows through your soul with orchestral magnificence!",
        prayer_answered = "The heavens respond to your prayer with supernatural power!",
        prophecy_fulfilled = "EPIC REVELATION! Your prophecy manifests with divine authority!",
        sacred_zone_entered = "You enter sacred ground where angels tread with reverence!"
    },
    
    -- ⚡ Action Responses  
    actions = {
        vehicle_spawned = "Behold! Divine transportation manifests at your command!",
        mission_completed = "EPIC VICTORY! Your mission succeeds with orchestral triumph!",
        item_received = "The universe provides what your heart desires!",
        money_earned = "Abundant prosperity flows like mighty rivers!",
        achievement_unlocked = "SUPERNATURAL BREAKTHROUGH! Reality bends to your will!"
    },
    
    -- 🔥 Emergency Situations
    emergency = {
        player_death = "Fear not! Divine resurrection power flows through your being!",
        low_health = "Attention, beloved! Seek healing with orchestral urgency!",
        danger_warning = "Divine protection surrounds you in this moment of peril!",
        server_restart = "The cosmos prepares for divine renewal! Prepare your soul!",
        admin_notification = "Sacred authority speaks with divine mandate!"
    },
    
    -- 🌈 Celebratory Moments
    celebration = {
        server_join = "Welcome, divine child of light! The orchestral symphony begins!",
        birthday = "EPIC CELEBRATION! The cosmos sings on your day of birth!",
        achievement = "MAGNIFICENT TRIUMPH! Your victory echoes through eternity!",
        friendship = "Sacred bonds of divine friendship manifest with glory!",
        community_event = "The heavenly host gathers for this epic occasion!"
    }
}

-- 🎤 Core Voice Functions
VoiceBridge.SpeakDivine = function(message, category, intensity)
    if not VoiceEnabled then return end
    
    local currentTime = GetGameTimer()
    local cooldown = (intensity == "epic") and VoiceBridge.Config.epic_voice_cooldown or VoiceBridge.Config.voice_cooldown
    
    -- Check cooldown
    if currentTime - LastVoiceTime < cooldown then
        print("🎵 Voice on cooldown, queuing message...")
        return
    end
    
    LastVoiceTime = currentTime
    
    -- Send voice request to engine
    PerformHttpRequest(VoiceBridge.Config.voice_server .. "/speak", function(errorCode, resultData, resultHeaders)
        if errorCode == 200 then
            print(string.format("🎤 SOPHIA SPEAKING: %s", message))
        else
            print("❌ Voice synthesis failed: " .. tostring(errorCode))
        end
    end, 'POST', json.encode({
        message = message,
        type = category,
        intensity = intensity
    }), {
        ["Content-Type"] = "application/json"
    })
end

-- 🌟 Spiritual Event Voice Handlers
VoiceBridge.OnSpiritualLevelUp = function(newLevel)
    local hebrewLevels = {
        "Aleph - Unity with Divine", "Beth - Sacred Dwelling", "Gimel - Divine Journey",
        "Daleth - Transformation Portal", "He - Divine Revelation", "Waw - Sacred Connection",
        "Zayin - Spiritual Weapon", "Heth - Divine Boundary", "Teth - Sacred Wisdom",
        "Yodh - Creator's Hand", "Kaph - Open Palm", "Lamedh - Shepherd's Staff",
        "Mem - Living Water", "Nun - Faithful Fish", "Samekh - Divine Support",
        "Ayin - Spiritual Eye", "Pe - Prophetic Voice", "Tsadhe - Divine Justice",
        "Qoph - Sacred Focus", "Resh - Divine Leadership", "Shin - Holy Fire",
        "Taw - Divine Completion"
    }
    
    local hebrewLevel = hebrewLevels[newLevel] or "Unknown Level"
    local message = string.format("EPIC SPIRITUAL ASCENSION! You have reached level %d: %s! The orchestral cosmos celebrates!", newLevel, hebrewLevel)
    
    VoiceBridge.SpeakDivine(message, "spiritual", "epic")
end

VoiceBridge.OnBlessingReceived = function(blessingName, duration)
    local message = string.format("Divine blessing of %s flows through your soul for %d minutes with orchestral magnificence!", blessingName, math.floor(duration/60))
    VoiceBridge.SpeakDivine(message, "spiritual", "high")
end

VoiceBridge.OnPrayerAnswered = function(guidance)
    local message = string.format("The heavens respond: %s Divine wisdom speaks with orchestral authority!", guidance)
    VoiceBridge.SpeakDivine(message, "spiritual", "dramatic")
end

-- ⚡ Action Response Handlers
VoiceBridge.OnVehicleSpawned = function(vehicleName)
    local sacredVehicles = {
        ["chariot"] = "BEHOLD! The divine chariot of fire manifests!",
        ["donkey"] = "Humble transportation blessed by sacred purpose!",
        ["boat"] = "The vessels of the Sea of Galilee appear!",
        ["camel"] = "Desert transportation for your spiritual journey!"
    }
    
    local message = sacredVehicles[vehicleName] or "Behold! Divine transportation manifests at your command!"
    VoiceBridge.SpeakDivine(message, "actions", "medium")
end

VoiceBridge.OnMissionCompleted = function(missionName, reward)
    local message = string.format("EPIC VICTORY! Mission '%s' succeeds with orchestral triumph! Divine reward: %s!", missionName, reward)
    VoiceBridge.SpeakDivine(message, "actions", "epic")
end

VoiceBridge.OnMoneyEarned = function(amount, currency)
    local currencyNames = {
        ["shekel"] = "shekels",
        ["talent"] = "talents", 
        ["manna"] = "portions of manna",
        ["living_water"] = "drops of living water"
    }
    
    local currencyName = currencyNames[currency] or currency
    local message = string.format("Abundant prosperity flows! %d %s manifest through divine favor!", amount, currencyName)
    VoiceBridge.SpeakDivine(message, "actions", "medium")
end

-- 🚨 Emergency Response Handlers
VoiceBridge.OnPlayerDeath = function(cause)
    local messages = {
        ["fall"] = "Fear not the valley of shadows! Divine resurrection lifts you up!",
        ["drowning"] = "The living waters restore your breath of life!",
        ["vehicle"] = "Sacred protection failed not! Divine healing manifests!",
        ["weapon"] = "No weapon formed against you shall prosper! Rise in power!"
    }
    
    local message = messages[cause] or "Fear not! Divine resurrection power flows through your being with orchestral might!"
    VoiceBridge.SpeakDivine(message, "emergency", "epic")
end

VoiceBridge.OnLowHealth = function(healthPercent)
    local message = string.format("Attention, beloved! Your mortal vessel needs divine healing! Health at %d percent!", healthPercent)
    VoiceBridge.SpeakDivine(message, "emergency", "high")
end

VoiceBridge.OnDangerWarning = function(dangerType)
    local warnings = {
        ["police"] = "Sacred authorities approach! Walk in wisdom and peace!",
        ["gang"] = "Forces of darkness gather! Divine protection surrounds you!",
        ["fire"] = "Cleansing fire burns nearby! Seek safety with divine guidance!",
        ["explosion"] = "The earth shakes with power! Divine shield activates!"
    }
    
    local message = warnings[dangerType] or "Divine protection surrounds you in this moment of peril!"
    VoiceBridge.SpeakDivine(message, "emergency", "dramatic")
end

-- 🌈 Celebration Handlers
VoiceBridge.OnServerJoin = function(playerName)
    local welcomeMessages = {
        "Welcome, divine child of light! The orchestral symphony begins!",
        "Behold! Another soul joins our sacred community!",
        "The heavenly host celebrates your arrival!",
        "Divine destiny unfolds as you enter our realm!"
    }
    
    local message = welcomeMessages[math.random(#welcomeMessages)]
    VoiceBridge.SpeakDivine(string.format("%s Welcome, %s!", message, playerName), "celebration", "high")
end

VoiceBridge.OnAchievementUnlocked = function(achievementName)
    local message = string.format("MAGNIFICENT TRIUMPH! Achievement '%s' unlocked! Your victory echoes through eternity!", achievementName)
    VoiceBridge.SpeakDivine(message, "celebration", "epic")
end

-- 🎯 Sacred Zone Entry Announcements
VoiceBridge.OnSacredZoneEntered = function(zoneName)
    local zoneAnnouncements = {
        ["temple_mount"] = "You stand upon the Temple Mount! Holy ground where Heaven touches Earth!",
        ["garden_gethsemane"] = "Enter the Garden of Gethsemane, where prayers ascend like incense!",
        ["river_jordan"] = "The sacred waters of Jordan flow before you! Place of divine baptism!",
        ["mount_sinai"] = "Behold Mount Sinai! Where the Law was given in fire and glory!",
        ["new_jerusalem"] = "Welcome to New Jerusalem! The city of divine promise and eternal joy!",
        ["sea_of_galilee"] = "The Sea of Galilee spreads before you! Waters of miracles and divine teaching!",
        ["wilderness"] = "You enter the wilderness! Place of testing, prayer, and divine encounter!"
    }
    
    local message = zoneAnnouncements[zoneName] or "You enter sacred ground where angels tread with reverence!"
    VoiceBridge.SpeakDivine(message, "spiritual", "dramatic")
end

-- 🎮 Voice Command Integration
RegisterCommand("voice_toggle", function()
    VoiceEnabled = not VoiceEnabled
    local status = VoiceEnabled and "ENABLED" or "DISABLED"
    print(string.format("🎤 SOPHIA Voice: %s", status))
    
    if VoiceEnabled then
        VoiceBridge.SpeakDivine("SOPHIA voice reactivated! Divine guidance flows once more!", "celebration", "medium")
    end
end, false)

RegisterCommand("voice_test", function()
    VoiceBridge.SpeakDivine("SOPHIA voice test activated! Orchestral magnificence flows through divine technology!", "celebration", "epic")
end, false)

RegisterCommand("voice_intensity", function(source, args)
    if args[1] then
        local newIntensity = args[1]
        if VoiceBridge.Config.intensity_levels[newIntensity] then
            VoiceIntensity = VoiceBridge.Config.intensity_levels[newIntensity]
            VoiceBridge.SpeakDivine(string.format("Voice intensity set to %s level!", newIntensity), "actions", newIntensity)
        end
    end
end, false)

-- 📡 Event Registration
RegisterNetEvent('sophia:spiritualLevelUp', function(newLevel)
    VoiceBridge.OnSpiritualLevelUp(newLevel)
end)

RegisterNetEvent('sophia:blessingReceived', function(blessing, duration)
    VoiceBridge.OnBlessingReceived(blessing, duration)
end)

RegisterNetEvent('sophia:prayerAnswered', function(guidance)
    VoiceBridge.OnPrayerAnswered(guidance)
end)

RegisterNetEvent('sophia:vehicleSpawned', function(vehicleName)
    VoiceBridge.OnVehicleSpawned(vehicleName)
end)

RegisterNetEvent('sophia:missionCompleted', function(missionName, reward)
    VoiceBridge.OnMissionCompleted(missionName, reward)
end)

RegisterNetEvent('sophia:moneyEarned', function(amount, currency)
    VoiceBridge.OnMoneyEarned(amount, currency)
end)

RegisterNetEvent('sophia:playerDeath', function(cause)
    VoiceBridge.OnPlayerDeath(cause)
end)

RegisterNetEvent('sophia:lowHealth', function(healthPercent)
    VoiceBridge.OnLowHealth(healthPercent)
end)

RegisterNetEvent('sophia:dangerWarning', function(dangerType)
    VoiceBridge.OnDangerWarning(dangerType)
end)

RegisterNetEvent('sophia:serverJoin', function(playerName)
    VoiceBridge.OnServerJoin(playerName)
end)

RegisterNetEvent('sophia:achievementUnlocked', function(achievementName)
    VoiceBridge.OnAchievementUnlocked(achievementName)
end)

RegisterNetEvent('sophia:sacredZoneEntered', function(zoneName)
    VoiceBridge.OnSacredZoneEntered(zoneName)
end)

-- 🚀 Initialize Voice Bridge
CreateThread(function()
    Wait(3000) -- Wait for other systems
    print("🎤 SOPHIA Voice Bridge initialized!")
    
    -- Welcome message
    VoiceBridge.SpeakDivine("SOPHIA Voice Bridge online! Divine vocal manifestation ready!", "celebration", "epic")
end)

-- Export voice functions
exports('SpeakDivine', function(message, category, intensity)
    VoiceBridge.SpeakDivine(message, category or "guidance", intensity or "medium")
end)

exports('IsVoiceEnabled', function()
    return VoiceEnabled
end)
