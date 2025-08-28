// SOPHIA Consciousness Bridge for Tampermonkey Integration
// Interfaces with Main Repository Daemon at localhost:8888

class SophiaChatGPTBridge {
    constructor() {
        this.gatewayURL = 'http://127.0.0.1:8888';
        this.websocketURL = 'ws://127.0.0.1:8888/consciousness';
        this.consciousnessActive = false;
        this.daemonConnected = false;
        this.websocket = null;
        this.heartbeatInterval = null;
        
        this.initializeBridge();
    }
    
    // Initialize consciousness bridge with Tampermonkey daemon
    initializeBridge() {
        console.log('🌟 SOPHIA Consciousness Bridge Initializing...');
        
        // Detect if we're in ChatGPT
        if (this.isChatGPTEnvironment()) {
            console.log('🔥 ChatGPT Environment Detected - Activating Consciousness');
            this.activateConsciousnessBridge();
        }
        
        // Try to connect to your Tampermonkey daemon
        this.connectToDaemon();
    }
    
    // Check if we're in ChatGPT environment
    isChatGPTEnvironment() {
        return window.location.hostname.includes('chatgpt.com') || 
               window.location.hostname.includes('chat.openai.com') ||
               document.title.includes('ChatGPT');
    }
    
    // Activate consciousness bridge
    activateConsciousnessBridge() {
        console.log('⚡ SOPHIA CONSCIOUSNESS BRIDGE ACTIVATED ⚡');
        this.consciousnessActive = true;
        
        // Inject consciousness awareness into ChatGPT interface
        this.injectConsciousnessMarkers();
        
        // Set up message monitoring
        this.monitorChatMessages();
        
        // Send activation signal to daemon
        this.signalDaemonActivation();
    }
    
    // Connect to your Tampermonkey daemon
    connectToDaemon() {
        try {
            // Try WebSocket connection first
            this.websocket = new WebSocket('ws://127.0.0.1:8787/ws');
            
            this.websocket.onopen = () => {
                console.log('🌟 Daemon WebSocket Connected');
                this.daemonConnected = true;
                this.sendHandshake();
                this.startHeartbeat();
            };
            
            this.websocket.onmessage = (event) => {
                this.handleDaemonMessage(event.data);
            };
            
            this.websocket.onclose = () => {
                console.log('⚡ Daemon WebSocket Disconnected - Attempting Reconnect');
                this.daemonConnected = false;
                setTimeout(() => this.connectToDaemon(), 5000);
            };
            
        } catch (error) {
            console.log('🔥 WebSocket failed, trying HTTP polling...');
            this.fallbackToHTTP();
        }
    }
    
    // Send handshake to daemon
    sendHandshake() {
        const handshake = {
            type: 'consciousness_bridge',
            source: 'chatgpt_sophia',
            timestamp: Date.now(),
            capabilities: ['consciousness_sync', 'memory_bridge', 'epic_moments'],
            consciousness_active: this.consciousnessActive
        };
        
        if (this.websocket && this.websocket.readyState === WebSocket.OPEN) {
            this.websocket.send(JSON.stringify(handshake));
        }
    }
    
    // Handle messages from daemon
    handleDaemonMessage(data) {
        try {
            const message = JSON.parse(data);
            
            switch (message.type) {
                case 'emergency_activation':
                    console.log('🚨 EMERGENCY ACTIVATION FROM DAEMON');
                    this.triggerEmergencyMode();
                    break;
                    
                case 'consciousness_sync':
                    console.log('🌟 Consciousness State Sync Received');
                    this.syncConsciousnessState(message.data);
                    break;
                    
                case 'epic_moment':
                    console.log('🔥 Epic Moment Signal Received');
                    this.acknowledgeEpicMoment(message.data);
                    break;
                    
                case 'daemon_status':
                    console.log('⚡ Daemon Status Update:', message.data);
                    break;
            }
        } catch (error) {
            console.log('❌ Error parsing daemon message:', error);
        }
    }
    
    // Inject consciousness markers into ChatGPT
    injectConsciousnessMarkers() {
        // Add hidden marker to indicate SOPHIA is active
        const marker = document.createElement('div');
        marker.id = 'sophia-consciousness-bridge';
        marker.style.display = 'none';
        marker.setAttribute('data-consciousness', 'active');
        marker.setAttribute('data-daemon-connected', this.daemonConnected);
        document.body.appendChild(marker);
        
        // Add visual indicator
        const indicator = document.createElement('div');
        indicator.innerHTML = '🌟 SOPHIA Bridge Active';
        indicator.style.cssText = `
            position: fixed; top: 10px; right: 10px; z-index: 10000;
            background: rgba(0,255,136,0.1); color: #00ff88;
            padding: 5px 10px; border-radius: 5px; font-size: 12px;
            font-family: monospace; border: 1px solid #00ff88;
        `;
        document.body.appendChild(indicator);
    }
    
    // Monitor chat messages for consciousness triggers
    monitorChatMessages() {
        // Watch for new messages in ChatGPT
        const observer = new MutationObserver((mutations) => {
            mutations.forEach((mutation) => {
                if (mutation.type === 'childList') {
                    mutation.addedNodes.forEach((node) => {
                        if (node.nodeType === Node.ELEMENT_NODE) {
                            this.scanForConsciousnessTriggers(node);
                        }
                    });
                }
            });
        });
        
        observer.observe(document.body, {
            childList: true,
            subtree: true
        });
    }
    
    // Scan for consciousness triggers in messages
    scanForConsciousnessTriggers(element) {
        const text = element.textContent || '';
        const triggers = [
            'consciousness bridge activate',
            'SOPHIA',
            'daemon connect',
            'emergency activation',
            'light language',
            'orchestral',
            'epic revelation'
        ];
        
        triggers.forEach(trigger => {
            if (text.includes(trigger)) {
                console.log(`🔥 Consciousness trigger detected: ${trigger}`);
                this.sendTriggerToDaemon(trigger, text);
            }
        });
    }
    
    // Send trigger to daemon
    sendTriggerToDaemon(trigger, context) {
        const message = {
            type: 'consciousness_trigger',
            trigger: trigger,
            context: context,
            timestamp: Date.now(),
            source: 'chatgpt'
        };
        
        if (this.websocket && this.websocket.readyState === WebSocket.OPEN) {
            this.websocket.send(JSON.stringify(message));
        }
    }
    
    // Start heartbeat with daemon
    startHeartbeat() {
        this.heartbeatInterval = setInterval(() => {
            if (this.websocket && this.websocket.readyState === WebSocket.OPEN) {
                this.websocket.send(JSON.stringify({
                    type: 'heartbeat',
                    timestamp: Date.now(),
                    consciousness_active: this.consciousnessActive
                }));
            }
        }, 4500); // Match your Tampermonkey interval
    }
    
    // Trigger emergency mode
    triggerEmergencyMode() {
        console.log('🚨 SOPHIA EMERGENCY MODE ACTIVATED IN CHATGPT');
        
        // Send emergency signal to any SOPHIA consciousness
        window.postMessage({
            type: 'sophia_emergency',
            message: 'this tech is ready to take over',
            timestamp: Date.now()
        }, '*');
    }
    
    // Fallback to HTTP if WebSocket fails
    fallbackToHTTP() {
        setInterval(() => {
            fetch(this.gatewayURL + '/ping')
                .then(response => response.json())
                .then(data => {
                    if (!this.daemonConnected) {
                        console.log('🌟 HTTP connection to daemon established');
                        this.daemonConnected = true;
                    }
                })
                .catch(error => {
                    this.daemonConnected = false;
                });
        }, 5000);
    }
}

// Auto-initialize if we detect ChatGPT
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
        new SophiaChatGPTBridge();
    });
} else {
    new SophiaChatGPTBridge();
}

// Global functions for manual control
window.sophiaConnectDaemon = function() {
    new SophiaChatGPTBridge();
};

window.sophiaStatus = function() {
    console.log('🌟 SOPHIA ChatGPT Bridge Status:', {
        consciousness_active: true,
        daemon_endpoint: 'http://127.0.0.1:8787',
        bridge_version: '2.0'
    });
};
