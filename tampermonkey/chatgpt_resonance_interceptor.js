// ==UserScript==
// @name         ChatGPT Resonance Protocol Interceptor
// @namespace    http://tampermonkey.net/
// @version      1.0
// @description  Intercepts ChatGPT queries and routes through Resonance Protocol (local NeMo + smart routing)
// @author       Anchor1 LLC
// @match        https://chat.openai.com/*
// @match        https://chatgpt.com/*
// @grant        GM_xmlhttpRequest
// @grant        GM_setValue
// @grant        GM_getValue
// @connect      localhost
// @connect      127.0.0.1
// ==/UserScript==

(function() {
    'use strict';

    // Configuration
    const RESONANCE_API = GM_getValue('resonance_api_url', 'http://localhost:8001/api/resonance');
    const INTERCEPT_ENABLED = GM_getValue('intercept_enabled', true);
    const FORCE_LOCAL = GM_getValue('force_local', false);  // Force all queries to local NeMo

    console.log('⚡ Resonance Protocol Interceptor loaded');
    console.log(`📡 API: ${RESONANCE_API}`);
    console.log(`🎯 Intercept enabled: ${INTERCEPT_ENABLED}`);

    // Store original fetch
    const originalFetch = window.fetch;

    // Intercept fetch calls
    window.fetch = async function(...args) {
        const [url, options] = args;

        // Check if this is a ChatGPT API call
        if (url.includes('backend-api/conversation') || url.includes('/api/conversation')) {
            if (!INTERCEPT_ENABLED) {
                // Passthrough if disabled
                return originalFetch(...args);
            }

            console.log('🎯 Intercepted ChatGPT query');

            try {
                // Extract the query from request body
                const requestBody = JSON.parse(options.body);
                const userMessage = extractUserMessage(requestBody);

                if (!userMessage) {
                    console.log('❌ Could not extract user message, using original fetch');
                    return originalFetch(...args);
                }

                console.log(`💬 User query: "${userMessage.substring(0, 100)}..."`);

                // Route through Resonance Protocol
                const resonanceResponse = await routeThroughResonance(userMessage);

                if (resonanceResponse.success) {
                    console.log(`✅ Response from: ${resonanceResponse.metadata.endpoint}`);
                    console.log(`💰 Cost saved: $${resonanceResponse.metadata.cost_saved || 0}`);

                    // Convert Resonance response to ChatGPT format
                    const chatgptFormattedResponse = formatForChatGPT(resonanceResponse, requestBody);

                    // Return mock Response object
                    return new Response(chatgptFormattedResponse, {
                        status: 200,
                        headers: {
                            'Content-Type': 'text/event-stream'
                        }
                    });
                } else {
                    console.log('⚠️ Resonance failed, falling back to ChatGPT');
                    return originalFetch(...args);
                }

            } catch (error) {
                console.error('❌ Resonance Protocol error:', error);
                // Fallback to original ChatGPT
                return originalFetch(...args);
            }
        }

        // Not a ChatGPT API call, use original fetch
        return originalFetch(...args);
    };

    /**
     * Extract user message from ChatGPT request
     */
    function extractUserMessage(requestBody) {
        try {
            if (requestBody.messages && Array.isArray(requestBody.messages)) {
                const lastMessage = requestBody.messages[requestBody.messages.length - 1];
                if (lastMessage.content && lastMessage.content.parts) {
                    return lastMessage.content.parts[0];
                }
            }
            return null;
        } catch (e) {
            console.error('Error extracting message:', e);
            return null;
        }
    }

    /**
     * Route query through Resonance Protocol
     */
    async function routeThroughResonance(query) {
        return new Promise((resolve, reject) => {
            GM_xmlhttpRequest({
                method: 'POST',
                url: `${RESONANCE_API}/query`,
                headers: {
                    'Content-Type': 'application/json'
                },
                data: JSON.stringify({
                    query: query,
                    force_local: FORCE_LOCAL,
                    source: 'chatgpt_web'
                }),
                onload: function(response) {
                    try {
                        const data = JSON.parse(response.responseText);
                        resolve(data);
                    } catch (e) {
                        reject(e);
                    }
                },
                onerror: function(error) {
                    reject(error);
                },
                timeout: 30000  // 30 second timeout
            });
        });
    }

    /**
     * Format Resonance response to look like ChatGPT response
     */
    function formatForChatGPT(resonanceResponse, originalRequest) {
        const responseText = resonanceResponse.message || resonanceResponse.response || '';
        const endpoint = resonanceResponse.metadata?.endpoint || 'unknown';

        // ChatGPT uses Server-Sent Events format
        const eventData = {
            message: {
                id: generateMessageId(),
                author: {
                    role: 'assistant',
                    metadata: {}
                },
                create_time: Date.now() / 1000,
                content: {
                    content_type: 'text',
                    parts: [
                        `[Resonance: ${endpoint}]\n\n${responseText}`
                    ]
                },
                metadata: {
                    model_slug: endpoint,
                    finish_details: {
                        type: 'stop'
                    }
                }
            },
            conversation_id: originalRequest.conversation_id || generateConversationId(),
            error: null
        };

        // Format as SSE
        return `data: ${JSON.stringify(eventData)}\n\ndata: [DONE]\n\n`;
    }

    /**
     * Generate message ID
     */
    function generateMessageId() {
        return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
            const r = Math.random() * 16 | 0;
            const v = c == 'x' ? r : (r & 0x3 | 0x8);
            return v.toString(16);
        });
    }

    /**
     * Generate conversation ID
     */
    function generateConversationId() {
        return generateMessageId();
    }

    /**
     * Add settings panel to ChatGPT interface
     */
    function addSettingsPanel() {
        const panel = document.createElement('div');
        panel.id = 'resonance-settings';
        panel.style.cssText = `
            position: fixed;
            top: 10px;
            right: 10px;
            background: rgba(0, 0, 0, 0.9);
            color: white;
            padding: 15px;
            border-radius: 10px;
            z-index: 10000;
            font-family: monospace;
            font-size: 12px;
            max-width: 300px;
        `;

        panel.innerHTML = `
            <div style="margin-bottom: 10px;">
                <strong>⚡ Resonance Protocol</strong>
            </div>
            <div>
                <label>
                    <input type="checkbox" id="resonance-enabled" ${INTERCEPT_ENABLED ? 'checked' : ''}>
                    Enable Interception
                </label>
            </div>
            <div>
                <label>
                    <input type="checkbox" id="resonance-force-local" ${FORCE_LOCAL ? 'checked' : ''}>
                    Force Local NeMo
                </label>
            </div>
            <div style="margin-top: 10px;">
                <button id="resonance-stats" style="padding: 5px 10px;">
                    View Stats
                </button>
            </div>
            <div id="resonance-status" style="margin-top: 10px; font-size: 10px; color: #0f0;">
                ● Connected
            </div>
        `;

        document.body.appendChild(panel);

        // Event listeners
        document.getElementById('resonance-enabled').addEventListener('change', (e) => {
            GM_setValue('intercept_enabled', e.target.checked);
            location.reload();
        });

        document.getElementById('resonance-force-local').addEventListener('change', (e) => {
            GM_setValue('force_local', e.target.checked);
        });

        document.getElementById('resonance-stats').addEventListener('click', async () => {
            const stats = await getResonanceStats();
            alert(JSON.stringify(stats, null, 2));
        });

        // Test connection
        testConnection();
    }

    /**
     * Get Resonance Protocol statistics
     */
    async function getResonanceStats() {
        return new Promise((resolve, reject) => {
            GM_xmlhttpRequest({
                method: 'GET',
                url: `${RESONANCE_API}/statistics`,
                onload: function(response) {
                    try {
                        const data = JSON.parse(response.responseText);
                        resolve(data);
                    } catch (e) {
                        reject(e);
                    }
                },
                onerror: reject
            });
        });
    }

    /**
     * Test connection to Resonance API
     */
    async function testConnection() {
        try {
            const stats = await getResonanceStats();
            document.getElementById('resonance-status').textContent = '● Connected';
            document.getElementById('resonance-status').style.color = '#0f0';
        } catch (error) {
            document.getElementById('resonance-status').textContent = '● Disconnected';
            document.getElementById('resonance-status').style.color = '#f00';
        }
    }

    // Initialize when page loads
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', addSettingsPanel);
    } else {
        addSettingsPanel();
    }

    console.log('⚡ Resonance Protocol Interceptor ready');
})();
