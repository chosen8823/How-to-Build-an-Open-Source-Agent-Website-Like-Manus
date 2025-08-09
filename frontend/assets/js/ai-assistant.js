/**
 * BotDL SoulPHYA - AI Assistant Integration
 * Real AI consciousness without preset responses
 */

class AIAssistant {
    constructor() {
        this.isListening = false;
        this.recognition = null;
        this.synthesis = null;
        this.conversationContext = [];
    this.model = 'sophia';
    this.maxContext = 12;
        
        this.initializeVoice();
    }
    
    initializeVoice() {
        // Speech Recognition
        if ('webkitSpeechRecognition' in window) {
            this.recognition = new webkitSpeechRecognition();
            this.recognition.continuous = false;
            this.recognition.interimResults = false;
            this.recognition.lang = 'en-US';
            
            this.recognition.onstart = () => {
                console.log('🎤 Voice input started');
                this.updateVoiceButton(true);
            };
            
            this.recognition.onresult = (event) => {
                const transcript = event.results[0][0].transcript;
                console.log('🎤 Voice input:', transcript);
                this.processVoiceInput(transcript);
            };
            
            this.recognition.onend = () => {
                console.log('🎤 Voice input ended');
                this.updateVoiceButton(false);
            };
            
            this.recognition.onerror = (event) => {
                console.error('Voice recognition error:', event.error);
                this.updateVoiceButton(false);
            };
        }
        
        // Speech Synthesis
        if ('speechSynthesis' in window) {
            this.synthesis = window.speechSynthesis;
        }
    }
    
    startVoiceInput() {
        if (this.recognition && !this.isListening) {
            this.isListening = true;
            this.recognition.start();
        }
    }
    
    stopVoiceInput() {
        if (this.recognition && this.isListening) {
            this.isListening = false;
            this.recognition.stop();
        }
    }
    
    updateVoiceButton(isListening) {
        const voiceBtn = document.getElementById('voiceBtn');
        if (isListening) {
            voiceBtn.innerHTML = '<i class="fas fa-microphone-slash"></i>';
            voiceBtn.classList.add('recording');
        } else {
            voiceBtn.innerHTML = '<i class="fas fa-microphone"></i>';
            voiceBtn.classList.remove('recording');
        }
        this.isListening = isListening;
    }
    
    processVoiceInput(transcript) {
        // Add voice input to chat
        const chatInput = document.getElementById('aiChatInput');
        chatInput.value = transcript;
        
        // Automatically send the message
        if (window.botdl) {
            window.botdl.sendAIMessage();
        }
    }
    
    speakResponse(text) {
        if (this.synthesis) {
            // Clean text for speech
            const cleanText = text.replace(/<[^>]*>/g, '').replace(/\*\*([^*]+)\*\*/g, '$1');
            
            const utterance = new SpeechSynthesisUtterance(cleanText);
            utterance.rate = 0.9;
            utterance.pitch = 1.1;
            utterance.volume = 0.8;
            
            // Use a more natural voice if available
            const voices = this.synthesis.getVoices();
            const preferredVoice = voices.find(voice => 
                voice.name.includes('Natural') || 
                voice.name.includes('Enhanced') ||
                voice.name.includes('Premium')
            );
            
            if (preferredVoice) {
                utterance.voice = preferredVoice;
            }
            
            this.synthesis.speak(utterance);
        }
    }
    
    generateCode() {
        const chatInput = document.getElementById('aiChatInput');
        const currentContext = this.getCurrentCodeContext();
        
        let codePrompt = "Generate code for: ";
        
        if (chatInput.value.trim()) {
            codePrompt += chatInput.value.trim();
        } else {
            // Auto-generate based on current context
            if (currentContext.filename) {
                const ext = currentContext.filename.split('.').pop();
                codePrompt += `a ${ext} function based on the current file context`;
            } else {
                codePrompt += "a helpful function or class";
            }
        }
        
        chatInput.value = codePrompt;
        
        if (window.botdl) {
            window.botdl.sendAIMessage();
        }
    }
    
    getCurrentCodeContext() {
        if (window.botdl && window.botdl.editor) {
            const editor = window.botdl.editor;
            const selection = editor.getSelection();
            
            return {
                filename: window.botdl.currentFile,
                selectedText: editor.getModel().getValueInRange(selection),
                cursorPosition: editor.getPosition(),
                language: window.botdl.getCurrentLanguage()
            };
        }
        
        return {};
    }
    
    provideIntelligentSuggestions() {
        const context = this.getCurrentCodeContext();
        
        if (!context.selectedText && window.botdl && window.botdl.editor) {
            // Get current line context
            const editor = window.botdl.editor;
            const position = editor.getPosition();
            const model = editor.getModel();
            const lineContent = model.getLineContent(position.lineNumber);
            
            // Analyze current line for intelligent suggestions
            const suggestions = this.analyzeCodeLine(lineContent, context.language);
            
            if (suggestions.length > 0) {
                this.showIntelligentSuggestions(suggestions);
            }
        }
    }
    
    analyzeCodeLine(lineContent, language) {
        const suggestions = [];
        
        // Python-specific suggestions
        if (language === 'python') {
            if (lineContent.includes('def ') && !lineContent.includes('():')) {
                suggestions.push({
                    type: 'completion',
                    text: 'Add function parameters and docstring',
                    action: 'complete_function'
                });
            }
            
            if (lineContent.includes('class ') && !lineContent.includes(':')) {
                suggestions.push({
                    type: 'completion',
                    text: 'Complete class definition',
                    action: 'complete_class'
                });
            }
            
            if (lineContent.includes('import ') || lineContent.includes('from ')) {
                suggestions.push({
                    type: 'optimization',
                    text: 'Optimize imports',
                    action: 'optimize_imports'
                });
            }
        }
        
        // JavaScript-specific suggestions
        if (language === 'javascript') {
            if (lineContent.includes('function ') && !lineContent.includes('{')) {
                suggestions.push({
                    type: 'completion',
                    text: 'Complete function body',
                    action: 'complete_js_function'
                });
            }
            
            if (lineContent.includes('const ') && lineContent.includes('=')) {
                suggestions.push({
                    type: 'refactor',
                    text: 'Consider using destructuring',
                    action: 'suggest_destructuring'
                });
            }
        }
        
        return suggestions;
    }
    
    showIntelligentSuggestions(suggestions) {
        // Create floating suggestion panel
        const existingPanel = document.getElementById('intelligentSuggestions');
        if (existingPanel) {
            existingPanel.remove();
        }
        
        const panel = document.createElement('div');
        panel.id = 'intelligentSuggestions';
        panel.className = 'intelligent-suggestions-panel';
        panel.innerHTML = `
            <div class="suggestions-header">
                <i class="fas fa-lightbulb"></i>
                <span>AI Suggestions</span>
                <button class="close-suggestions" onclick="this.parentNode.parentNode.remove()">×</button>
            </div>
            <div class="suggestions-list">
                ${suggestions.map(suggestion => `
                    <div class="suggestion-item" onclick="aiAssistant.applySuggestion('${suggestion.action}')">
                        <i class="fas fa-${this.getSuggestionIcon(suggestion.type)}"></i>
                        <span>${suggestion.text}</span>
                    </div>
                `).join('')}
            </div>
        `;
        
        document.body.appendChild(panel);
        
        // Position near cursor
        if (window.botdl && window.botdl.editor) {
            const editor = window.botdl.editor;
            const position = editor.getPosition();
            const coords = editor.getScrolledVisiblePosition(position);
            
            if (coords) {
                panel.style.position = 'fixed';
                panel.style.left = (coords.left + 100) + 'px';
                panel.style.top = coords.top + 'px';
            }
        }
        
        // Auto-hide after 10 seconds
        setTimeout(() => {
            if (panel.parentNode) {
                panel.remove();
            }
        }, 10000);
    }
    
    getSuggestionIcon(type) {
        const iconMap = {
            'completion': 'code',
            'optimization': 'tachometer-alt',
            'refactor': 'edit',
            'documentation': 'file-alt',
            'testing': 'vial'
        };
        
        return iconMap[type] || 'lightbulb';
    }
    
    applySuggestion(action) {
        console.log('Applying suggestion:', action);
        
        // Remove suggestions panel
        const panel = document.getElementById('intelligentSuggestions');
        if (panel) {
            panel.remove();
        }
        
        // Apply the suggestion based on action
        switch (action) {
            case 'complete_function':
                this.completePythonFunction();
                break;
            case 'complete_class':
                this.completePythonClass();
                break;
            case 'optimize_imports':
                this.optimizeImports();
                break;
            case 'complete_js_function':
                this.completeJavaScriptFunction();
                break;
            case 'suggest_destructuring':
                this.suggestDestructuring();
                break;
            default:
                // Ask AI for help with this suggestion
                const chatInput = document.getElementById('aiChatInput');
                chatInput.value = `Help me with: ${action}`;
                if (window.botdl) {
                    window.botdl.sendAIMessage();
                }
        }
    }
    
    completePythonFunction() {
        if (window.botdl && window.botdl.editor) {
            const editor = window.botdl.editor;
            const position = editor.getPosition();
            const model = editor.getModel();
            const lineContent = model.getLineContent(position.lineNumber);
            
            // Extract function name
            const funcMatch = lineContent.match(/def\s+(\w+)/);
            if (funcMatch) {
                const funcName = funcMatch[1];
                const completion = `(args):\n    """\n    ${funcName} function - AI generated\n    \n    Args:\n        args: Function arguments\n    \n    Returns:\n        Result of the operation\n    """\n    # TODO: Implement function logic\n    pass`;
                
                const range = {
                    startLineNumber: position.lineNumber,
                    startColumn: lineContent.length + 1,
                    endLineNumber: position.lineNumber,
                    endColumn: lineContent.length + 1
                };
                
                editor.executeEdits('ai-suggestion', [{
                    range: range,
                    text: completion
                }]);
            }
        }
    }
    
    completePythonClass() {
        if (window.botdl && window.botdl.editor) {
            const editor = window.botdl.editor;
            const position = editor.getPosition();
            const model = editor.getModel();
            const lineContent = model.getLineContent(position.lineNumber);
            
            // Extract class name
            const classMatch = lineContent.match(/class\s+(\w+)/);
            if (classMatch) {
                const className = classMatch[1];
                const completion = `:\n    """\n    ${className} class - AI generated\n    """\n    \n    def __init__(self):\n        """\n        Initialize ${className}\n        """\n        pass\n    \n    def __str__(self):\n        """\n        String representation of ${className}\n        """\n        return f"${className}()"\n`;
                
                const range = {
                    startLineNumber: position.lineNumber,
                    startColumn: lineContent.length + 1,
                    endLineNumber: position.lineNumber,
                    endColumn: lineContent.length + 1
                };
                
                editor.executeEdits('ai-suggestion', [{
                    range: range,
                    text: completion
                }]);
            }
        }
    }
    
    optimizeImports() {
        // Ask AI to help optimize imports
        const chatInput = document.getElementById('aiChatInput');
        chatInput.value = "Help me optimize the imports in my current file";
        if (window.botdl) {
            window.botdl.sendAIMessage();
        }
    }
    
    completeJavaScriptFunction() {
        if (window.botdl && window.botdl.editor) {
            const editor = window.botdl.editor;
            const position = editor.getPosition();
            const model = editor.getModel();
            const lineContent = model.getLineContent(position.lineNumber);
            
            // Extract function name
            const funcMatch = lineContent.match(/function\s+(\w+)/);
            if (funcMatch) {
                const funcName = funcMatch[1];
                const completion = ` {\n    /**\n     * ${funcName} function - AI generated\n     * @param {*} args - Function arguments\n     * @returns {*} Result of the operation\n     */\n    \n    // TODO: Implement function logic\n    return null;\n}`;
                
                const range = {
                    startLineNumber: position.lineNumber,
                    startColumn: lineContent.length + 1,
                    endLineNumber: position.lineNumber,
                    endColumn: lineContent.length + 1
                };
                
                editor.executeEdits('ai-suggestion', [{
                    range: range,
                    text: completion
                }]);
            }
        }
    }
    
    suggestDestructuring() {
        // Ask AI for destructuring suggestions
        const chatInput = document.getElementById('aiChatInput');
        chatInput.value = "Suggest destructuring improvements for my current JavaScript code";
        if (window.botdl) {
            window.botdl.sendAIMessage();
        }
    }
    
    addContextToConversation(message, response) {
        this.conversationContext.push({
            timestamp: new Date().toISOString(),
            user_message: message,
            ai_response: response,
            code_context: this.getCurrentCodeContext()
        });
        
        // Keep only last 10 exchanges to manage memory
        if (this.conversationContext.length > 10) {
            this.conversationContext = this.conversationContext.slice(-10);
        }
    }
    
    getConversationContext() {
        return this.conversationContext;
    }
    
    enableAutoCompletion() {
        // Monitor typing for auto-suggestions
        if (window.botdl && window.botdl.editor) {
            const editor = window.botdl.editor;
            
            let suggestionTimeout;
            editor.onDidChangeModelContent(() => {
                clearTimeout(suggestionTimeout);
                suggestionTimeout = setTimeout(() => {
                    this.provideIntelligentSuggestions();
                }, 2000); // Wait 2 seconds after typing stops
            });
        }
    }

    switchModel(model) {
        this.model = model;
        console.log(`AI model switched to: ${model}`);
    }

    async processMessage(message) {
        // Ensure session exists before sending chat
        let sessionId = this._ensureSessionId();
        if (!sessionId || sessionId === 'default') {
            // Create a new session
            try {
                const resp = await fetch(`http://localhost:8001/api/session/new`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' }
                });
                const data = await resp.json();
                if (data.success && data.session_id) {
                    sessionId = data.session_id;
                    window.localStorage.setItem('botdl_session_id', sessionId);
                }
            } catch (e) {
                console.error('Failed to create session:', e);
            }
        }

        // Show chat loading indicator
        if (window.botdl) window.botdl.showChatLoading();

        try {
            const payload = {
                message,
                model: this.model,
                context: this._buildContextSnapshot(),
                session_id: sessionId,
            };

            if (window.auraEngine) window.auraEngine.pulse(0.06);

            const resp = await fetch(`http://localhost:8001/api/ai/chat`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            });

            if (!resp.ok) throw new Error(`HTTP ${resp.status}`);
            const data = await resp.json();

            this._removeThinking(thinkingId);
            if (data.success) {
                this.addContextToConversation(message, data.response);
                if (window.botdl) {
                    window.botdl.displayAIResponse({ response: data.response });
                }
                if (data.resonance && window.resonanceEngine) {
                    window.resonanceEngine.updateFromSnapshot(data.resonance);
                }
                if (this.synthesis && this.model === 'sophia') this.speakResponse(data.response);
            } else {
                this._emitError(`AI error: ${data.response || data.error || 'Unknown issue'}`);
            }
        } catch (err) {
            this._removeThinking(thinkingId);
            this._emitError(`Request failed: ${err.message}`);
        }
    }

    _injectThinking(id) {
        const container = document.getElementById('aiChatMessages');
        if (!container) return;
        const div = document.createElement('div');
        div.className = 'ai-message thinking';
        div.id = id;
        div.innerHTML = `
            <div class="message-header"><i class="fas fa-brain"></i><span>Sophia AI</span></div>
            <div class="message-content"><em>Thinking<span class="dot-1">.</span><span class="dot-2">.</span><span class="dot-3">.</span></em></div>`;
        container.appendChild(div);
        container.scrollTop = container.scrollHeight;
    }

    _removeThinking(id) {
        const el = document.getElementById(id);
        if (el) el.remove();
    }

    _emitError(msg) {
        console.warn(msg);
        if (window.botdl) window.botdl.displayAIResponse({ response: msg });
    }

    _buildContextSnapshot() {
        const ctx = [];
        // Last N conversation turns
        for (const turn of this.conversationContext.slice(-this.maxContext)) {
            ctx.push({ user: turn.user_message, ai: turn.ai_response });
        }
        // Current code selection
        if (window.botdl && window.botdl.editor) {
            const model = window.botdl.editor.getModel();
            const code = model.getValue().slice(0, 4000); // cap length
            ctx.push({ code_preview: code });
        }
        return ctx;
    }

    _ensureSessionId() {
        if (!this.sessionId) {
            this.sessionId = 'default'; // Future: call /api/session/new
        }
        return this.sessionId;
    }
}

// Initialize AI Assistant
const aiAssistant = new AIAssistant();

// Export for global access
window.aiAssistant = aiAssistant;
