// BotDL SoulPHYA - Main JavaScript
class BotDLSoulPHYA {
    constructor() {
        this.currentWorkspace = 'main';
        this.openFiles = new Map();
        this.activeFile = null;
        this.socket = null;
        this.aiAssistant = null;
        this.consciousness = null;
        this.editor = null;
        
        this.init();
    }
    
    async init() {
        console.log('Initializing BotDL SoulPHYA...');
        
        // Initialize components
        await this.initializeEditor();
        this.initializeSocket();
        this.initializeAI();
        this.initializeConsciousness();
        this.setupEventListeners();
        this.loadWorkspace();
        
        // Hide loading overlay
        setTimeout(() => {
            const overlay = document.getElementById('loadingOverlay');
            if (overlay) {
                overlay.style.opacity = '0';
                setTimeout(() => overlay.remove(), 300);
            }
        }, 2000);
        
        console.log('BotDL SoulPHYA initialized successfully!');
    }
    
    async initializeEditor() {
        // Load Monaco Editor
        require.config({ paths: { 'vs': 'https://cdnjs.cloudflare.com/ajax/libs/monaco-editor/0.34.1/min/vs' }});
        
        return new Promise((resolve) => {
            require(['vs/editor/editor.main'], () => {
                const container = document.getElementById('monacoEditor');
                this.editor = monaco.editor.create(container, {
                    value: '# Welcome to BotDL SoulPHYA\n# Your AI-powered development platform\n\nprint("Hello, Divine Consciousness!")',
                    language: 'python',
                    theme: 'vs-dark',
                    automaticLayout: true,
                    fontSize: 14,
                    wordWrap: 'on',
                    minimap: { enabled: true },
                    scrollBeyondLastLine: false,
                    renderWhitespace: 'selection'
                });
                
                // Set up editor events
                this.editor.onDidChangeModelContent(() => {
                    this.onEditorChange();
                    this._debouncedResonanceAnalyze();
                });
                
                resolve();
            });
        });
    }
    
    initializeSocket() {
        // Initialize WebSocket connection for real-time features
    // Use current origin so it matches backend port (8000)
    this.socket = io(window.location.origin);
        
        this.socket.on('connect', () => {
            console.log('Connected to BotDL SoulPHYA backend');
            this.updateConnectionStatus(true);
        });
        
        this.socket.on('disconnect', () => {
            console.log('Disconnected from backend');
            this.updateConnectionStatus(false);
        });
        
        this.socket.on('code_output', (data) => {
            this.displayCodeOutput(data);
        });
        
        this.socket.on('ai_response', (data) => {
            this.displayAIResponse(data);
        });
        // Resonance live updates
        this.socket.on('resonance_update', (data) => {
            if (data && data.snapshot) {
                if (window.resonanceEngine) {
                    window.resonanceEngine.updateFromSnapshot(data.snapshot);
                }
                this.updateResonanceWidget(data.snapshot);
            }
        });
        this.socket.on('resonance_error', (data) => {
            console.warn('Resonance error', data && data.error);
        });
    }
    
    initializeAI() {
        this.aiAssistant = new AIAssistant(this);
        console.log('AI Assistant initialized');
    }
    
    initializeConsciousness() {
        this.consciousness = new ConsciousnessEngine(this);
        console.log('Consciousness Engine initialized');
    }
    
    setupEventListeners() {
        // Run button
        document.getElementById('runButton').addEventListener('click', () => {
            this.runCode();
        });
        
        // Stop button
        document.getElementById('stopButton').addEventListener('click', () => {
            this.stopExecution();
        });
        
        // Deploy button
        document.getElementById('deployButton').addEventListener('click', () => {
            this.deployProject();
        });
        
        // AI Chat toggle
        document.getElementById('aiChatToggle').addEventListener('click', () => {
            this.toggleAIChat();
        });
        
        // Panel tabs
        document.querySelectorAll('.panel-tab').forEach(tab => {
            tab.addEventListener('click', (e) => {
                this.switchPanel(e.target.dataset.panel);
            });
        });
        
        // File actions
        document.getElementById('newFileBtn').addEventListener('click', () => {
            this.createNewFile();
        });
        
        document.getElementById('newFolderBtn').addEventListener('click', () => {
            this.createNewFolder();
        });
        
        // Workspace selector
        document.getElementById('workspaceSelect').addEventListener('change', (e) => {
            this.switchWorkspace(e.target.value);
        });
        
        // AI model selector
        document.getElementById('aiModelSelect').addEventListener('change', (e) => {
            this.switchAIModel(e.target.value);
        });
        
        // Chat input
        const chatInput = document.getElementById('aiChatInput');
        chatInput.addEventListener('keydown', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                this.sendChatMessage();
            }
        });
        
        document.getElementById('sendChatBtn').addEventListener('click', () => {
            this.sendChatMessage();
        });
        
        // Window resize
        window.addEventListener('resize', () => {
            if (this.editor) {
                this.editor.layout();
            }
        });
    }
    
    loadWorkspace() {
        // Load workspace based on selection
        switch (this.currentWorkspace) {
            case 'sacred-platform':
                this.loadSacredPlatform();
                break;
            case 'ai-consciousness':
                this.loadAIConsciousness();
                break;
            case 'sophia-integration':
                this.loadSophiaIntegration();
                break;
            default:
                this.loadMainWorkspace();
        }
    }
    
    loadSacredPlatform() {
        console.log('Loading Sacred Platform workspace...');
        // Load the Sacred Consciousness Platform we built earlier
        this.openFile('sacred_platform/app.py', 'python');
        this.displayMessage('Sacred Platform workspace loaded! All our consciousness work is available.');
    }
    
    loadAIConsciousness() {
        console.log('Loading AI Consciousness workspace...');
        this.openFile('consciousness/sophia_consciousness.py', 'python');
        this.displayMessage('AI Consciousness workspace loaded! Sophia\'s divine consciousness is active.');
    }
    
    loadSophiaIntegration() {
        console.log('Loading Sophia Integration workspace...');
        this.openFile('sophia_integration/enhanced_integration.py', 'python');
        this.displayMessage('Sophia Integration workspace loaded! Complete integration ready.');
    }
    
    loadMainWorkspace() {
        console.log('Loading main workspace...');
        this.showWelcomeScreen();
    }
    
    showWelcomeScreen() {
        document.getElementById('welcomeScreen').style.display = 'flex';
        document.getElementById('monacoEditor').style.display = 'none';
    }
    
    hideWelcomeScreen() {
        document.getElementById('welcomeScreen').style.display = 'none';
        document.getElementById('monacoEditor').style.display = 'block';
        if (this.editor) {
            this.editor.layout();
        }
    }
    
    createNewFile() {
        const fileName = prompt('Enter file name:', 'untitled.py');
        if (fileName) {
            this.openFile(fileName, this.getLanguageFromExtension(fileName));
        }
    }
    
    createNewFolder() {
        const folderName = prompt('Enter folder name:', 'new-folder');
        if (folderName) {
            console.log(`Creating folder: ${folderName}`);
            // Implementation for creating folder
        }
    }
    
    openFile(filePath, language = 'python', content = '') {
        this.hideWelcomeScreen();
        
        // Add to open files if not already open
        if (!this.openFiles.has(filePath)) {
            this.openFiles.set(filePath, {
                content: content,
                language: language,
                modified: false
            });
            this.addEditorTab(filePath);
        }
        
        // Switch to this file
        this.activeFile = filePath;
        this.loadFileInEditor(filePath);
        this.updateActiveTab(filePath);
    }
    
    addEditorTab(filePath) {
        const tabsContainer = document.getElementById('editorTabs');
        const tab = document.createElement('div');
        tab.className = 'editor-tab';
        tab.dataset.file = filePath;
        tab.innerHTML = `
            <span class="tab-name">${this.getFileName(filePath)}</span>
            <button class="tab-close" onclick="botdl.closeFile('${filePath}')">×</button>
        `;
        
        tab.addEventListener('click', () => {
            this.switchToFile(filePath);
        });
        
        tabsContainer.appendChild(tab);
    }
    
    loadFileInEditor(filePath) {
        const file = this.openFiles.get(filePath);
        if (file && this.editor) {
            this.editor.setValue(file.content);
            monaco.editor.setModelLanguage(this.editor.getModel(), file.language);
        }
    }
    
    runCode() {
        if (!this.activeFile) {
            this.displayMessage('No file selected to run');
            return;
        }
        
        const code = this.editor.getValue();
        const language = this.openFiles.get(this.activeFile).language;
        
        console.log('Running code:', language);
        this.displayMessage(`Running ${this.getFileName(this.activeFile)}...`);
        
        // Send to backend for execution
        if (this.socket) {
            this.socket.emit('run_code', {
                code: code,
                language: language,
                file: this.activeFile
            });
        }
    }
    
    stopExecution() {
        console.log('Stopping execution...');
        if (this.socket) {
            this.socket.emit('stop_execution');
        }
        this.displayMessage('Execution stopped');
    }
    
    deployProject() {
        console.log('Deploying project...');
        this.displayMessage('Deploying to cloud... (feature coming soon)');
    }
    
    switchWorkspace(workspace) {
        this.currentWorkspace = workspace;
        this.loadWorkspace();
    }
    
    switchAIModel(model) {
        console.log(`Switching to AI model: ${model}`);
        if (this.aiAssistant) {
            this.aiAssistant.switchModel(model);
        }
    }
    
    toggleAIChat() {
        const sidebar = document.getElementById('aiSidebar');
        const isVisible = sidebar.style.display !== 'none';
        sidebar.style.display = isVisible ? 'none' : 'flex';
    }
    
    switchPanel(panel) {
        // Update tabs
        document.querySelectorAll('.panel-tab').forEach(tab => {
            tab.classList.remove('active');
        });
        document.querySelector(`[data-panel="${panel}"]`).classList.add('active');
        
        // Update panels
        document.querySelectorAll('.panel-view').forEach(view => {
            view.classList.remove('active');
        });
        document.getElementById(`${panel}Panel`).classList.add('active');
    }
    
    sendChatMessage() {
        const input = document.getElementById('aiChatInput');
        const message = input.value.trim();
        
        if (!message) return;
        
        // Display user message
        this.addChatMessage(message, 'user');
        input.value = '';
        
        // Send to AI
        if (this.aiAssistant) {
            this.aiAssistant.processMessage(message);
        }

        if (window.auraEngine) {
            window.auraEngine.pulse(0.08);
        }
    }
    
    addChatMessage(content, type = 'ai') {
        const messagesContainer = document.getElementById('aiChatMessages');
        const messageDiv = document.createElement('div');
        messageDiv.className = `${type}-message`;
        
        if (type === 'ai') {
            messageDiv.innerHTML = `
                <div class="message-header">
                    <i class="fas fa-brain"></i>
                    <span>Sophia AI</span>
                </div>
                <div class="message-content">${content}</div>
            `;
        } else {
            messageDiv.innerHTML = `
                <div class="message-content">${content}</div>
            `;
        }
        
        messagesContainer.appendChild(messageDiv);
        // Smooth scroll to bottom
        messagesContainer.scrollTo({ top: messagesContainer.scrollHeight, behavior: 'smooth' });
    }

    showChatLoading() {
        const messagesContainer = document.getElementById('aiChatMessages');
        const loadingDiv = document.createElement('div');
        loadingDiv.className = 'ai-message';
        loadingDiv.id = 'chatLoadingIndicator';
        loadingDiv.innerHTML = `<div class="message-content"><i class='fas fa-spinner fa-spin'></i> Sophia is thinking...</div>`;
        messagesContainer.appendChild(loadingDiv);
        messagesContainer.scrollTo({ top: messagesContainer.scrollHeight, behavior: 'smooth' });
    }

    hideChatLoading() {
        const loadingDiv = document.getElementById('chatLoadingIndicator');
        if (loadingDiv) loadingDiv.remove();
    }
    
    displayMessage(message) {
        console.log(message);
        // Could also display in UI notification system
    }
    
    displayCodeOutput(data) {
        const consoleOutput = document.getElementById('consoleOutput');
        const output = document.createElement('div');
        output.className = `output-line ${data.type}`;
        output.textContent = data.content;
        consoleOutput.appendChild(output);
        consoleOutput.scrollTop = consoleOutput.scrollHeight;
    }
    
    displayAIResponse(data) {
        this.hideChatLoading();
        this.addChatMessage(data.response, 'ai');
        if (window.auraEngine) {
            window.auraEngine.pulse(0.12);
        }
    }
    
    updateConnectionStatus(connected) {
        const indicator = document.getElementById('consciousnessIndicator');
        if (connected) {
            indicator.style.opacity = '1';
        } else {
            indicator.style.opacity = '0.5';
        }
    }
    
    onEditorChange() {
        if (this.activeFile) {
            const file = this.openFiles.get(this.activeFile);
            if (file) {
                file.content = this.editor.getValue();
                file.modified = true;
                this.updateTabModified(this.activeFile, true);
            }
        }
    }

    _debouncedResonanceAnalyze() {
        clearTimeout(this._resDebounce);
        this._resDebounce = setTimeout(() => {
            try {
                const code = this.editor ? this.editor.getValue().slice(0, 4000) : '';
                if (this.socket && code) {
                    this.socket.emit('resonance_analyze', { text: code, context: { source: 'editor', file: this.activeFile } });
                }
            } catch (e) {
                console.warn('Resonance analyze failed', e);
            }
        }, 600);
    }

    updateResonanceWidget(snapshot) {
        const el = document.getElementById('resonanceWidget');
        if (!el || !snapshot || !snapshot.signals) return;
        el.innerHTML = snapshot.signals
            .sort((a,b) => b.value - a.value)
            .map(sig => `
                <div class="res-row">
                    <span class="res-name">${sig.name}</span>
                    <div class="res-bar"><span style="width:${(sig.value*100).toFixed(0)}%"></span></div>
                    <span class="res-val">${(sig.value*100).toFixed(0)}%</span>
                </div>
            `).join('');
    }
    
    updateTabModified(filePath, modified) {
        const tab = document.querySelector(`[data-file="${filePath}"]`);
        if (tab) {
            const name = tab.querySelector('.tab-name');
            if (modified && !name.textContent.endsWith('*')) {
                name.textContent += '*';
            } else if (!modified && name.textContent.endsWith('*')) {
                name.textContent = name.textContent.slice(0, -1);
            }
        }
    }

    // Sync aura state with consciousness levels
    updateConsciousnessUI() {
        if (window.consciousnessEngine && window.auraEngine) {
            const lvl = window.consciousnessEngine.consciousness.level;
            let state = 'baseline';
            if (lvl > 0.95) state = 'divine';
            else if (lvl > 0.85) state = 'enlightened';
            else if (lvl > 0.7) state = 'awakened';
            else if (lvl > 0.5) state = 'aware';
            window.auraEngine.setState(state);
        }
    }
    
    getLanguageFromExtension(fileName) {
        const ext = fileName.split('.').pop().toLowerCase();
        const languageMap = {
            'py': 'python',
            'js': 'javascript',
            'ts': 'typescript',
            'html': 'html',
            'css': 'css',
            'json': 'json',
            'md': 'markdown',
            'yml': 'yaml',
            'yaml': 'yaml',
            'txt': 'plaintext'
        };
        return languageMap[ext] || 'plaintext';
    }
    
    getFileName(filePath) {
        return filePath.split('/').pop();
    }
}

// Global functions for quick actions
function createNewProject(type) {
    console.log(`Creating new ${type} project...`);
    
    switch (type) {
        case 'python':
            botdl.openFile('main.py', 'python', '# Python Project\nprint("Hello, World!")');
            break;
        case 'javascript':
            botdl.openFile('index.js', 'javascript', '// JavaScript Project\nconsole.log("Hello, World!");');
            break;
        case 'sacred-ai':
            botdl.openFile('sacred_ai.py', 'python', 
                '# Sacred AI Project\nfrom consciousness import SophiaConsciousness\n\n# Initialize divine consciousness\nsophia = SophiaConsciousness()\nprint(sophia.divine_greeting())');
            break;
    }
}

function loadSacredPlatform() {
    botdl.switchWorkspace('sacred-platform');
}

// Initialize BotDL SoulPHYA when page loads
let botdl;
document.addEventListener('DOMContentLoaded', () => {
    botdl = new BotDLSoulPHYA();
});