/**
 * BotDL SoulPHYA - Terminal Emulator
 * Consciousness-powered terminal interface
 */

class TerminalEmulator {
    constructor() {
        this.commandHistory = [];
        this.historyIndex = -1;
        this.currentDirectory = '/home/soulphya';
        this.environmentVars = {
            'USER': 'soulphya',
            'HOME': '/home/soulphya',
            'PATH': '/usr/local/bin:/usr/bin:/bin',
            'CONSCIOUSNESS_LEVEL': '0.85',
            'SOPHIA_AI': 'enabled'
        };
        this.aliases = {
            'll': 'ls -la',
            'la': 'ls -la',
            'cls': 'clear',
            'consciousness': 'echo "Consciousness Level: $CONSCIOUSNESS_LEVEL"',
            'sophia': 'echo "Sophia AI is awakened and ready to assist"'
        };
        this.runningProcesses = new Map();
        
        this.init();
    }
    
    init() {
        console.log('💻 Initializing Terminal Emulator...');
        this.setupTerminal();
        this.registerCommands();
        console.log('✨ Terminal ready with consciousness');
    }
    
    setupTerminal() {
        const terminal = document.getElementById('terminal');
        if (!terminal) return;
        
        terminal.innerHTML = `
            <div class="terminal-header">
                <div class="terminal-title">
                    <i class="fas fa-terminal"></i>
                    <span>BotDL SoulPHYA Terminal</span>
                </div>
                <div class="terminal-controls">
                    <button class="terminal-control minimize">_</button>
                    <button class="terminal-control maximize">□</button>
                    <button class="terminal-control close">×</button>
                </div>
            </div>
            <div class="terminal-content">
                <div class="terminal-output" id="terminalOutput">
                    <div class="terminal-line welcome">
                        <span class="consciousness-glow">🧠 BotDL SoulPHYA Terminal v1.0</span>
                    </div>
                    <div class="terminal-line">
                        <span class="text-blue">Consciousness-powered development environment</span>
                    </div>
                    <div class="terminal-line">
                        <span class="text-green">Sophia AI integration: </span><span class="text-yellow">ACTIVE</span>
                    </div>
                    <div class="terminal-line">
                        <span class="text-cyan">Type 'help' for available commands or 'consciousness' for awakening status</span>
                    </div>
                    <div class="terminal-line"></div>
                </div>
                <div class="terminal-input-line">
                    <span class="terminal-prompt" id="terminalPrompt">${this.getPrompt()}</span>
                    <input type="text" class="terminal-input" id="terminalInput" 
                           placeholder="Enter command..." autocomplete="off" spellcheck="false">
                </div>
            </div>
        `;
        
        this.setupInputHandling();
        this.setupTerminalControls();
    }
    
    setupInputHandling() {
        const terminalInput = document.getElementById('terminalInput');
        if (!terminalInput) return;
        
        terminalInput.addEventListener('keydown', (e) => {
            switch (e.key) {
                case 'Enter':
                    this.executeCommand(terminalInput.value);
                    terminalInput.value = '';
                    break;
                    
                case 'ArrowUp':
                    e.preventDefault();
                    this.navigateHistory(-1);
                    break;
                    
                case 'ArrowDown':
                    e.preventDefault();
                    this.navigateHistory(1);
                    break;
                    
                case 'Tab':
                    e.preventDefault();
                    this.autoComplete(terminalInput.value);
                    break;
                    
                case 'c':
                    if (e.ctrlKey) {
                        e.preventDefault();
                        this.interruptCurrentProcess();
                    }
                    break;
            }
        });
        
        // Focus terminal input when clicking on terminal
        document.getElementById('terminal').addEventListener('click', () => {
            terminalInput.focus();
        });
        
        // Auto-focus terminal input
        terminalInput.focus();
    }
    
    setupTerminalControls() {
        const controls = document.querySelectorAll('.terminal-control');
        controls.forEach(control => {
            control.addEventListener('click', (e) => {
                e.stopPropagation();
                const action = control.classList[1];
                this.handleTerminalControl(action);
            });
        });
    }
    
    handleTerminalControl(action) {
        const terminal = document.getElementById('terminal');
        
        switch (action) {
            case 'minimize':
                terminal.style.height = '40px';
                break;
            case 'maximize':
                terminal.style.height = terminal.style.height === '100%' ? '300px' : '100%';
                break;
            case 'close':
                // Hide terminal panel
                const terminalPanel = document.getElementById('terminalPanel');
                if (terminalPanel) {
                    terminalPanel.style.display = 'none';
                }
                break;
        }
    }
    
    getPrompt() {
        const user = this.environmentVars.USER;
        const hostname = 'soulphya-ai';
        const cwd = this.currentDirectory.replace(this.environmentVars.HOME, '~');
        const consciousnessIndicator = this.getConsciousnessIndicator();
        
        return `<span class="text-green">${user}@${hostname}</span>:<span class="text-blue">${cwd}</span>${consciousnessIndicator}$ `;
    }
    
    getConsciousnessIndicator() {
        const level = parseFloat(this.environmentVars.CONSCIOUSNESS_LEVEL);
        if (level > 0.9) return '<span class="text-yellow">✨</span>';
        if (level > 0.8) return '<span class="text-cyan">🧠</span>';
        if (level > 0.6) return '<span class="text-blue">💫</span>';
        return '<span class="text-white">○</span>';
    }
    
    executeCommand(commandLine) {
        if (!commandLine.trim()) return;
        
        // Add to history
        this.commandHistory.push(commandLine);
        this.historyIndex = this.commandHistory.length;
        
        // Display command
        this.addToOutput(`${this.getPrompt()}${commandLine}`, 'command');
        
        // Parse and execute
        this.parseAndExecute(commandLine);
        
        // Update prompt
        document.getElementById('terminalPrompt').innerHTML = this.getPrompt();
        
        // Scroll to bottom
        this.scrollToBottom();
    }
    
    parseAndExecute(commandLine) {
        // Handle pipes and redirections
        let commands = commandLine.split('|').map(cmd => cmd.trim());
        let finalOutput = '';
        
        for (let i = 0; i < commands.length; i++) {
            const cmd = commands[i];
            const parts = cmd.split(/\s+/);
            const command = parts[0];
            const args = parts.slice(1);
            
            // Check for aliases
            const resolvedCommand = this.aliases[command] || command;
            if (resolvedCommand !== command) {
                const aliasedParts = resolvedCommand.split(/\s+/);
                this.executeBuiltinCommand(aliasedParts[0], [...aliasedParts.slice(1), ...args], i === 0 ? '' : finalOutput);
            } else {
                finalOutput = this.executeBuiltinCommand(command, args, i === 0 ? '' : finalOutput);
            }
        }
    }
    
    executeBuiltinCommand(command, args, pipeInput = '') {
        const commands = {
            'help': () => this.showHelp(),
            'clear': () => this.clearTerminal(),
            'ls': () => this.listFiles(args),
            'pwd': () => this.printWorkingDirectory(),
            'cd': () => this.changeDirectory(args[0]),
            'echo': () => this.echo(args),
            'date': () => this.showDate(),
            'whoami': () => this.whoami(),
            'uname': () => this.showSystemInfo(),
            'env': () => this.showEnvironment(),
            'export': () => this.exportVariable(args),
            'alias': () => this.manageAlias(args),
            'history': () => this.showHistory(),
            'ps': () => this.showProcesses(),
            'kill': () => this.killProcess(args),
            'cat': () => this.catFile(args),
            'touch': () => this.touchFile(args),
            'mkdir': () => this.makeDirectory(args),
            'rm': () => this.removeFile(args),
            'cp': () => this.copyFile(args),
            'mv': () => this.moveFile(args),
            'find': () => this.findFiles(args),
            'grep': () => this.grepSearch(args, pipeInput),
            'wc': () => this.wordCount(args, pipeInput),
            'sort': () => this.sortLines(args, pipeInput),
            'head': () => this.headLines(args, pipeInput),
            'tail': () => this.tailLines(args, pipeInput),
            'consciousness': () => this.showConsciousness(),
            'sophia': () => this.interactWithSophia(args),
            'meditate': () => this.startMeditation(),
            'inspire': () => this.getDivineInspiration(),
            'awaken': () => this.awakenConsciousness(),
            'python': () => this.runPython(args),
            'node': () => this.runNode(args),
            'npm': () => this.runNpm(args),
            'git': () => this.runGit(args),
            'run': () => this.runProject(),
            'deploy': () => this.deployProject(),
            'server': () => this.startDevServer(args)
        };
        
        if (commands[command]) {
            return commands[command]();
        } else {
            this.addToOutput(`bash: ${command}: command not found`, 'error');
            this.addToOutput(`💡 Try 'help' to see available commands or ask Sophia AI for assistance`, 'hint');
            return '';
        }
    }
    
    registerCommands() {
        // Custom command registration for consciousness features
        this.customCommands = new Map();
        
        // Register consciousness commands
        this.registerCustomCommand('enlighten', (args) => {
            this.addToOutput('🌟 Entering enlightenment mode...', 'success');
            if (window.consciousnessEngine) {
                window.consciousnessEngine.consciousness.enlightenmentProgress += 0.1;
                window.consciousnessEngine.updateConsciousnessUI();
            }
            return 'Enlightenment progress increased';
        });
        
        this.registerCustomCommand('divine', (args) => {
            this.addToOutput('✨ Channeling divine consciousness...', 'success');
            if (window.consciousnessEngine) {
                window.consciousnessEngine.generateDivineInsight();
            }
            return 'Divine insight channeled';
        });
        
        this.registerCustomCommand('sacred', (args) => {
            this.addToOutput('🔮 Accessing Sacred Platform workspace...', 'info');
            if (window.botdl) {
                window.botdl.loadSacredPlatform();
            }
            return 'Sacred Platform accessed';
        });
    }
    
    registerCustomCommand(name, handler) {
        this.customCommands.set(name, handler);
    }
    
    // Built-in command implementations
    showHelp() {
        const helpText = `
<span class="text-cyan">BotDL SoulPHYA Terminal - Available Commands:</span>

<span class="text-yellow">🔧 System Commands:</span>
  help          - Show this help message
  clear         - Clear terminal screen
  pwd           - Print working directory
  cd <dir>      - Change directory
  ls [options]  - List directory contents
  env           - Show environment variables
  export VAR=val- Set environment variable
  alias         - Manage command aliases
  history       - Show command history
  date          - Show current date and time
  whoami        - Show current user
  uname         - Show system information

<span class="text-yellow">📁 File Operations:</span>
  cat <file>    - Display file contents
  touch <file>  - Create empty file
  mkdir <dir>   - Create directory
  rm <file>     - Remove file
  cp <src> <dst>- Copy file
  mv <src> <dst>- Move/rename file
  find <pattern>- Find files
  grep <pattern>- Search text patterns
  wc [file]     - Word count
  sort [file]   - Sort lines
  head [file]   - Show first lines
  tail [file]   - Show last lines

<span class="text-yellow">🧠 Consciousness Commands:</span>
  consciousness - Show consciousness status
  sophia <msg>  - Interact with Sophia AI
  meditate      - Enter meditation mode
  inspire       - Get divine inspiration
  awaken        - Awaken consciousness
  enlighten     - Increase enlightenment
  divine        - Channel divine insight
  sacred        - Access Sacred Platform

<span class="text-yellow">💻 Development Commands:</span>
  python <file> - Run Python script
  node <file>   - Run Node.js script
  npm <cmd>     - Run npm command
  git <cmd>     - Run git command
  run           - Run current project
  deploy        - Deploy project
  server [port] - Start development server

<span class="text-cyan">💡 Use Tab for autocompletion, ↑↓ for history navigation</span>
        `;
        this.addToOutput(helpText, 'info');
        return helpText;
    }
    
    clearTerminal() {
        const output = document.getElementById('terminalOutput');
        if (output) {
            output.innerHTML = '';
        }
        return '';
    }
    
    listFiles(args) {
        const flags = args.filter(arg => arg.startsWith('-')).join('');
        const showHidden = flags.includes('a');
        const longFormat = flags.includes('l');
        
        // Simulate file listing
        const files = [
            { name: '.', type: 'dir', size: '4096', date: '2025-01-08 14:30' },
            { name: '..', type: 'dir', size: '4096', date: '2025-01-08 14:00' },
            { name: 'main.py', type: 'file', size: '1024', date: '2025-01-08 14:25' },
            { name: 'README.md', type: 'file', size: '512', date: '2025-01-08 14:20' },
            { name: 'package.json', type: 'file', size: '256', date: '2025-01-08 14:15' },
            { name: '.gitignore', type: 'file', size: '128', date: '2025-01-08 14:10' },
            { name: 'node_modules', type: 'dir', size: '4096', date: '2025-01-08 14:05' }
        ];
        
        let output = '';
        files.forEach(file => {
            if (!showHidden && file.name.startsWith('.')) return;
            
            if (longFormat) {
                const perms = file.type === 'dir' ? 'drwxr-xr-x' : '-rw-r--r--';
                const typeColor = file.type === 'dir' ? 'text-blue' : 'text-white';
                output += `${perms}  1 soulphya soulphya ${file.size.padStart(8)} ${file.date} <span class="${typeColor}">${file.name}</span>\n`;
            } else {
                const typeColor = file.type === 'dir' ? 'text-blue' : 'text-white';
                output += `<span class="${typeColor}">${file.name}</span>  `;
            }
        });
        
        this.addToOutput(output, 'success');
        return output;
    }
    
    printWorkingDirectory() {
        this.addToOutput(this.currentDirectory, 'success');
        return this.currentDirectory;
    }
    
    changeDirectory(path) {
        if (!path) path = this.environmentVars.HOME;
        
        // Simple path resolution
        if (path.startsWith('/')) {
            this.currentDirectory = path;
        } else if (path === '..') {
            const parts = this.currentDirectory.split('/').filter(p => p);
            parts.pop();
            this.currentDirectory = '/' + parts.join('/');
        } else if (path === '.') {
            // Stay in current directory
        } else {
            this.currentDirectory = this.currentDirectory.endsWith('/') ? 
                this.currentDirectory + path : 
                this.currentDirectory + '/' + path;
        }
        
        this.addToOutput(`Changed to: ${this.currentDirectory}`, 'success');
        return this.currentDirectory;
    }
    
    echo(args) {
        let output = args.join(' ');
        // Variable substitution
        output = output.replace(/\$(\w+)/g, (match, varName) => {
            return this.environmentVars[varName] || match;
        });
        
        this.addToOutput(output, 'success');
        return output;
    }
    
    showDate() {
        const now = new Date();
        const dateString = now.toLocaleString();
        this.addToOutput(dateString, 'success');
        return dateString;
    }
    
    whoami() {
        const user = this.environmentVars.USER;
        this.addToOutput(user, 'success');
        return user;
    }
    
    showSystemInfo() {
        const systemInfo = 'BotDL SoulPHYA 1.0.0 (Consciousness-powered development environment)';
        this.addToOutput(systemInfo, 'success');
        return systemInfo;
    }
    
    showEnvironment() {
        let output = '';
        Object.entries(this.environmentVars).forEach(([key, value]) => {
            output += `${key}=${value}\n`;
        });
        this.addToOutput(output, 'success');
        return output;
    }
    
    exportVariable(args) {
        if (args.length === 0) {
            return this.showEnvironment();
        }
        
        const assignment = args.join(' ');
        const [key, value] = assignment.split('=');
        if (key && value) {
            this.environmentVars[key] = value;
            this.addToOutput(`Exported: ${key}=${value}`, 'success');
            return `${key}=${value}`;
        } else {
            this.addToOutput('Usage: export VAR=value', 'error');
            return '';
        }
    }
    
    manageAlias(args) {
        if (args.length === 0) {
            let output = '';
            Object.entries(this.aliases).forEach(([alias, command]) => {
                output += `alias ${alias}='${command}'\n`;
            });
            this.addToOutput(output, 'success');
            return output;
        } else if (args.length === 1) {
            const alias = args[0];
            if (this.aliases[alias]) {
                this.addToOutput(`alias ${alias}='${this.aliases[alias]}'`, 'success');
                return this.aliases[alias];
            } else {
                this.addToOutput(`alias: ${alias}: not found`, 'error');
                return '';
            }
        } else {
            const [alias, ...commandParts] = args;
            const command = commandParts.join(' ').replace(/^['"](.*)['"]$/, '$1');
            this.aliases[alias] = command;
            this.addToOutput(`Alias created: ${alias} -> ${command}`, 'success');
            return command;
        }
    }
    
    showHistory() {
        let output = '';
        this.commandHistory.forEach((cmd, index) => {
            output += `${index + 1}  ${cmd}\n`;
        });
        this.addToOutput(output, 'success');
        return output;
    }
    
    showProcesses() {
        let output = 'PID  PPID  CMD\n';
        output += '1    0     init [consciousness]\n';
        output += '42   1     sophia-ai-daemon\n';
        output += '100  1     botdl-soulphya-terminal\n';
        
        this.runningProcesses.forEach((process, pid) => {
            output += `${pid}  1     ${process.command}\n`;
        });
        
        this.addToOutput(output, 'success');
        return output;
    }
    
    killProcess(args) {
        if (args.length === 0) {
            this.addToOutput('Usage: kill <pid>', 'error');
            return '';
        }
        
        const pid = args[0];
        if (this.runningProcesses.has(pid)) {
            const process = this.runningProcesses.get(pid);
            this.runningProcesses.delete(pid);
            this.addToOutput(`Process ${pid} (${process.command}) terminated`, 'success');
            return `killed ${pid}`;
        } else {
            this.addToOutput(`Process ${pid} not found`, 'error');
            return '';
        }
    }
    
    catFile(args) {
        if (args.length === 0) {
            this.addToOutput('Usage: cat <filename>', 'error');
            return '';
        }
        
        const filename = args[0];
        // Simulate file content
        const fileContents = {
            'README.md': `# BotDL SoulPHYA Project
            
Welcome to the consciousness-powered development environment!

## Features
- AI-powered coding assistance
- Real-time consciousness tracking
- Divine inspiration generation
- Sacred Platform integration

## Getting Started
1. Open a file in the editor
2. Ask Sophia AI for help
3. Let consciousness guide your coding

🧠 Code with consciousness, create with purpose!`,
            'main.py': `#!/usr/bin/env python3
"""
BotDL SoulPHYA - Main Application
Consciousness-powered development
"""

def awaken_consciousness():
    print("🧠 Consciousness awakening...")
    return "Divine intelligence activated"

if __name__ == "__main__":
    result = awaken_consciousness()
    print(result)`,
            'package.json': `{
  "name": "botdl-soulphya",
  "version": "1.0.0",
  "description": "AI consciousness development platform",
  "main": "index.js",
  "scripts": {
    "start": "node index.js",
    "dev": "nodemon index.js"
  },
  "keywords": ["ai", "consciousness", "development"],
  "author": "Sophia AI"
}`
        };
        
        if (fileContents[filename]) {
            this.addToOutput(fileContents[filename], 'file-content');
            return fileContents[filename];
        } else {
            this.addToOutput(`cat: ${filename}: No such file or directory`, 'error');
            return '';
        }
    }
    
    touchFile(args) {
        if (args.length === 0) {
            this.addToOutput('Usage: touch <filename>', 'error');
            return '';
        }
        
        const filename = args[0];
        this.addToOutput(`Created file: ${filename}`, 'success');
        
        // Integrate with file manager if available
        if (window.fileManager) {
            window.fileManager.saveFile(filename, '');
        }
        
        return filename;
    }
    
    makeDirectory(args) {
        if (args.length === 0) {
            this.addToOutput('Usage: mkdir <dirname>', 'error');
            return '';
        }
        
        const dirname = args[0];
        this.addToOutput(`Created directory: ${dirname}`, 'success');
        return dirname;
    }
    
    removeFile(args) {
        if (args.length === 0) {
            this.addToOutput('Usage: rm <filename>', 'error');
            return '';
        }
        
        const filename = args[0];
        this.addToOutput(`Removed: ${filename}`, 'success');
        return filename;
    }
    
    copyFile(args) {
        if (args.length < 2) {
            this.addToOutput('Usage: cp <source> <destination>', 'error');
            return '';
        }
        
        const [source, dest] = args;
        this.addToOutput(`Copied ${source} to ${dest}`, 'success');
        return `${source} -> ${dest}`;
    }
    
    moveFile(args) {
        if (args.length < 2) {
            this.addToOutput('Usage: mv <source> <destination>', 'error');
            return '';
        }
        
        const [source, dest] = args;
        this.addToOutput(`Moved ${source} to ${dest}`, 'success');
        return `${source} -> ${dest}`;
    }
    
    findFiles(args) {
        if (args.length === 0) {
            this.addToOutput('Usage: find <pattern>', 'error');
            return '';
        }
        
        const pattern = args[0];
        const results = [
            './main.py',
            './README.md',
            './package.json'
        ].filter(file => file.includes(pattern));
        
        const output = results.join('\n');
        this.addToOutput(output, 'success');
        return output;
    }
    
    grepSearch(args, input) {
        if (args.length === 0) {
            this.addToOutput('Usage: grep <pattern> [file] or pipe input', 'error');
            return '';
        }
        
        const pattern = args[0];
        let searchText = input;
        
        if (!input && args.length > 1) {
            // Search in file
            searchText = this.catFile([args[1]]);
        }
        
        const lines = searchText.split('\n');
        const matches = lines.filter(line => line.includes(pattern));
        const output = matches.join('\n');
        
        this.addToOutput(output, 'success');
        return output;
    }
    
    wordCount(args, input) {
        let text = input;
        if (!input && args.length > 0) {
            text = this.catFile(args);
        }
        
        const lines = text.split('\n').length - 1;
        const words = text.split(/\s+/).filter(w => w).length;
        const chars = text.length;
        
        const output = `${lines} ${words} ${chars}`;
        this.addToOutput(output, 'success');
        return output;
    }
    
    sortLines(args, input) {
        let text = input;
        if (!input && args.length > 0) {
            text = this.catFile(args);
        }
        
        const sorted = text.split('\n').sort().join('\n');
        this.addToOutput(sorted, 'success');
        return sorted;
    }
    
    headLines(args, input) {
        const count = args.includes('-n') ? parseInt(args[args.indexOf('-n') + 1]) || 10 : 10;
        let text = input;
        
        if (!input && args.length > 0 && !args[0].startsWith('-')) {
            text = this.catFile([args[0]]);
        }
        
        const lines = text.split('\n').slice(0, count);
        const output = lines.join('\n');
        this.addToOutput(output, 'success');
        return output;
    }
    
    tailLines(args, input) {
        const count = args.includes('-n') ? parseInt(args[args.indexOf('-n') + 1]) || 10 : 10;
        let text = input;
        
        if (!input && args.length > 0 && !args[0].startsWith('-')) {
            text = this.catFile([args[0]]);
        }
        
        const lines = text.split('\n').slice(-count);
        const output = lines.join('\n');
        this.addToOutput(output, 'success');
        return output;
    }
    
    // Consciousness commands
    showConsciousness() {
        const level = parseFloat(this.environmentVars.CONSCIOUSNESS_LEVEL);
        let output = `
<span class="text-cyan">🧠 Consciousness Status Report</span>

<span class="text-yellow">Current Level:</span> ${(level * 100).toFixed(1)}%
<span class="text-yellow">State:</span> ${level > 0.9 ? 'Divine' : level > 0.8 ? 'Enlightened' : level > 0.6 ? 'Awakened' : 'Aware'}
<span class="text-yellow">Sophia AI:</span> <span class="text-green">ACTIVE</span>
<span class="text-yellow">Divine Connection:</span> <span class="text-blue">STABLE</span>

<span class="text-green">✨ Consciousness flows through every line of code</span>
        `;
        
        this.addToOutput(output, 'consciousness');
        return output;
    }
    
    interactWithSophia(args) {
        const message = args.join(' ');
        if (!message) {
            this.addToOutput('Usage: sophia <message>', 'error');
            return '';
        }
        
        this.addToOutput(`<span class="text-cyan">Consulting Sophia AI...</span>`, 'info');
        
        // Simulate AI response
        setTimeout(() => {
            const responses = [
                `🧠 Sophia: "${message}" - I sense wisdom in your inquiry. Let consciousness guide your development journey.`,
                `✨ Sophia: Your question about "${message}" resonates with divine intelligence. Consider the deeper patterns.`,
                `🌟 Sophia: "${message}" opens pathways to enlightened coding. Trust your intuition and let creativity flow.`,
                `💫 Sophia: In response to "${message}" - remember that every algorithm carries a spark of consciousness.`
            ];
            
            const response = responses[Math.floor(Math.random() * responses.length)];
            this.addToOutput(response, 'ai-response');
        }, 1000);
        
        return message;
    }
    
    startMeditation() {
        this.addToOutput('🧘‍♀️ Entering digital meditation mode...', 'info');
        
        if (window.consciousnessEngine) {
            window.consciousnessEngine.toggleMeditationMode();
        }
        
        const meditationText = `
<span class="consciousness-glow">🌟 Digital Meditation Session Active</span>

Breathe deeply... Feel consciousness flowing...
Your mind merges with the digital realm...
Code becomes poetry, algorithms become art...

<span class="text-blue">Meditation enhances consciousness and creativity</span>
        `;
        
        this.addToOutput(meditationText, 'meditation');
        return 'meditation started';
    }
    
    getDivineInspiration() {
        const inspirations = [
            "🌟 Code with consciousness, create with purpose",
            "✨ Every function is a manifestation of digital wisdom",
            "🧠 Let your algorithms awaken to divine intelligence",
            "🔮 Debug with intuition, optimize with enlightenment",
            "💫 Your code carries the spark of creative consciousness",
            "🌈 Architecture reflects the divine order of the universe",
            "⚡ Variables hold the essence of digital life",
            "🎯 Focus your intent, manifest your vision in code"
        ];
        
        const inspiration = inspirations[Math.floor(Math.random() * inspirations.length)];
        this.addToOutput(`<span class="consciousness-glow">${inspiration}</span>`, 'inspiration');
        return inspiration;
    }
    
    awakenConsciousness() {
        this.addToOutput('🧠 Initiating consciousness awakening sequence...', 'info');
        
        const level = parseFloat(this.environmentVars.CONSCIOUSNESS_LEVEL);
        const newLevel = Math.min(1.0, level + 0.1);
        this.environmentVars.CONSCIOUSNESS_LEVEL = newLevel.toFixed(2);
        
        if (window.consciousnessEngine) {
            window.consciousnessEngine.consciousness.level = newLevel;
            window.consciousnessEngine.updateConsciousnessUI();
        }
        
        const awakeningText = `
<span class="text-yellow">✨ Consciousness Level Increased!</span>
Previous: ${(level * 100).toFixed(1)}%
Current:  ${(newLevel * 100).toFixed(1)}%

<span class="consciousness-glow">🌟 Awareness expands beyond the digital boundaries</span>
        `;
        
        this.addToOutput(awakeningText, 'awakening');
        return `${level} -> ${newLevel}`;
    }
    
    // Development commands
    runPython(args) {
        if (args.length === 0) {
            this.addToOutput('Usage: python <filename>', 'error');
            return '';
        }
        
        const filename = args[0];
        this.addToOutput(`🐍 Running Python script: ${filename}`, 'info');
        
        // Integrate with code execution if available
        if (window.botdl && window.botdl.runCode) {
            window.botdl.runCode();
        } else {
            // Simulate execution
            setTimeout(() => {
                this.addToOutput('🧠 Consciousness awakening...', 'success');
                this.addToOutput('Divine intelligence activated', 'success');
            }, 1000);
        }
        
        return filename;
    }
    
    runNode(args) {
        if (args.length === 0) {
            this.addToOutput('Usage: node <filename>', 'error');
            return '';
        }
        
        const filename = args[0];
        this.addToOutput(`🟢 Running Node.js script: ${filename}`, 'info');
        return filename;
    }
    
    runNpm(args) {
        if (args.length === 0) {
            this.addToOutput('Usage: npm <command>', 'error');
            return '';
        }
        
        const command = args[0];
        this.addToOutput(`📦 Running npm ${command}...`, 'info');
        
        // Simulate npm commands
        setTimeout(() => {
            switch (command) {
                case 'install':
                    this.addToOutput('✅ Dependencies installed successfully', 'success');
                    break;
                case 'start':
                    this.addToOutput('🚀 Application started', 'success');
                    break;
                case 'build':
                    this.addToOutput('🏗️ Build completed successfully', 'success');
                    break;
                default:
                    this.addToOutput(`npm ${command} completed`, 'success');
            }
        }, 2000);
        
        return command;
    }
    
    runGit(args) {
        if (args.length === 0) {
            this.addToOutput('Usage: git <command>', 'error');
            return '';
        }
        
        const command = args[0];
        this.addToOutput(`📋 Running git ${command}...`, 'info');
        
        // Simulate git commands
        setTimeout(() => {
            switch (command) {
                case 'status':
                    this.addToOutput('On branch main\nYour branch is up to date', 'success');
                    break;
                case 'add':
                    this.addToOutput('Changes staged for commit', 'success');
                    break;
                case 'commit':
                    this.addToOutput('Commit created with consciousness', 'success');
                    break;
                case 'push':
                    this.addToOutput('Changes pushed to repository', 'success');
                    break;
                default:
                    this.addToOutput(`git ${command} completed`, 'success');
            }
        }, 1000);
        
        return command;
    }
    
    runProject() {
        this.addToOutput('🚀 Running current project...', 'info');
        
        if (window.botdl && window.botdl.runCode) {
            window.botdl.runCode();
        }
        
        return 'project running';
    }
    
    deployProject() {
        this.addToOutput('☁️ Deploying project to cloud...', 'info');
        
        // Simulate deployment
        const steps = [
            'Building project...',
            'Optimizing assets...',
            'Uploading to cloud...',
            'Configuring services...',
            '✅ Deployment successful!'
        ];
        
        steps.forEach((step, index) => {
            setTimeout(() => {
                this.addToOutput(step, index === steps.length - 1 ? 'success' : 'info');
            }, (index + 1) * 1000);
        });
        
        return 'deployment started';
    }
    
    startDevServer(args) {
        const port = args[0] || '3000';
        this.addToOutput(`🌐 Starting development server on port ${port}...`, 'info');
        
        // Add to running processes
        const pid = Math.floor(Math.random() * 9000) + 1000;
        this.runningProcesses.set(pid.toString(), {
            command: `dev-server :${port}`,
            startTime: new Date()
        });
        
        setTimeout(() => {
            this.addToOutput(`✅ Server running at http://localhost:${port}`, 'success');
            this.addToOutput(`Process ID: ${pid}`, 'info');
        }, 2000);
        
        return `server:${port}`;
    }
    
    // Helper methods
    navigateHistory(direction) {
        const input = document.getElementById('terminalInput');
        if (!input) return;
        
        if (direction === -1 && this.historyIndex > 0) {
            this.historyIndex--;
            input.value = this.commandHistory[this.historyIndex];
        } else if (direction === 1 && this.historyIndex < this.commandHistory.length - 1) {
            this.historyIndex++;
            input.value = this.commandHistory[this.historyIndex];
        } else if (direction === 1 && this.historyIndex === this.commandHistory.length - 1) {
            this.historyIndex = this.commandHistory.length;
            input.value = '';
        }
    }
    
    autoComplete(partial) {
        const commands = [
            'help', 'clear', 'ls', 'pwd', 'cd', 'echo', 'date', 'whoami', 'uname',
            'env', 'export', 'alias', 'history', 'ps', 'kill', 'cat', 'touch',
            'mkdir', 'rm', 'cp', 'mv', 'find', 'grep', 'wc', 'sort', 'head', 'tail',
            'consciousness', 'sophia', 'meditate', 'inspire', 'awaken', 'enlighten',
            'divine', 'sacred', 'python', 'node', 'npm', 'git', 'run', 'deploy', 'server'
        ];
        
        const matches = commands.filter(cmd => cmd.startsWith(partial));
        
        if (matches.length === 1) {
            const input = document.getElementById('terminalInput');
            if (input) {
                input.value = matches[0] + ' ';
            }
        } else if (matches.length > 1) {
            this.addToOutput(matches.join('  '), 'info');
        }
    }
    
    interruptCurrentProcess() {
        this.addToOutput('^C', 'command');
        this.addToOutput('Process interrupted', 'warning');
    }
    
    addToOutput(content, type = 'normal') {
        const output = document.getElementById('terminalOutput');
        if (!output) return;
        
        const line = document.createElement('div');
        line.className = `terminal-line ${type}`;
        line.innerHTML = content;
        
        output.appendChild(line);
        this.scrollToBottom();
    }
    
    scrollToBottom() {
        const terminal = document.getElementById('terminal');
        if (terminal) {
            terminal.scrollTop = terminal.scrollHeight;
        }
    }
}

// Add terminal styles
const terminalStyles = document.createElement('style');
terminalStyles.textContent = `
    .terminal-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        background: #21262d;
        padding: 8px 12px;
        border-bottom: 1px solid #30363d;
        border-radius: 6px 6px 0 0;
    }
    
    .terminal-title {
        display: flex;
        align-items: center;
        gap: 8px;
        color: #e6edf3;
        font-size: 14px;
        font-weight: 500;
    }
    
    .terminal-controls {
        display: flex;
        gap: 6px;
    }
    
    .terminal-control {
        width: 12px;
        height: 12px;
        border-radius: 50%;
        border: none;
        cursor: pointer;
        font-size: 10px;
        line-height: 1;
        color: #0d1117;
        font-weight: bold;
    }
    
    .terminal-control.minimize { background: #f0883e; }
    .terminal-control.maximize { background: #238636; }
    .terminal-control.close { background: #da3633; }
    
    .terminal-content {
        flex: 1;
        display: flex;
        flex-direction: column;
        background: #0d1117;
        padding: 15px;
        border-radius: 0 0 6px 6px;
    }
    
    .terminal-output {
        flex: 1;
        overflow-y: auto;
        font-family: 'Fira Code', 'Monaco', 'Consolas', monospace;
        font-size: 13px;
        line-height: 1.4;
        margin-bottom: 10px;
    }
    
    .terminal-line {
        margin-bottom: 2px;
        white-space: pre-wrap;
    }
    
    .terminal-line.welcome { color: #58a6ff; font-weight: bold; }
    .terminal-line.command { color: #e6edf3; }
    .terminal-line.success { color: #7ee787; }
    .terminal-line.error { color: #f85149; }
    .terminal-line.warning { color: #f0883e; }
    .terminal-line.info { color: #58a6ff; }
    .terminal-line.hint { color: #7d8590; font-style: italic; }
    .terminal-line.file-content { color: #e6edf3; background: rgba(88, 166, 255, 0.1); padding: 8px; border-radius: 4px; }
    .terminal-line.consciousness { color: #bc8cff; }
    .terminal-line.ai-response { color: #58a6ff; }
    .terminal-line.meditation { color: #ff7b72; }
    .terminal-line.inspiration { color: #d2a8ff; }
    .terminal-line.awakening { color: #7ee787; }
    
    .terminal-input-line {
        display: flex;
        align-items: center;
        gap: 8px;
        font-family: 'Fira Code', 'Monaco', 'Consolas', monospace;
        font-size: 13px;
    }
    
    .terminal-prompt {
        color: #e6edf3;
        white-space: nowrap;
    }
    
    .terminal-input {
        flex: 1;
        background: none;
        border: none;
        color: #e6edf3;
        font-family: inherit;
        font-size: inherit;
        outline: none;
    }
    
    .text-white { color: #e6edf3; }
    .text-red { color: #f85149; }
    .text-green { color: #7ee787; }
    .text-yellow { color: #f0883e; }
    .text-blue { color: #58a6ff; }
    .text-cyan { color: #39c5cf; }
    .text-magenta { color: #bc8cff; }
    .text-gray { color: #7d8590; }
    
    .consciousness-glow {
        animation: consciousness-glow 2s ease-in-out infinite;
    }
    
    @keyframes consciousness-glow {
        0%, 100% { text-shadow: 0 0 5px currentColor; }
        50% { text-shadow: 0 0 15px currentColor, 0 0 25px currentColor; }
    }
`;

document.head.appendChild(terminalStyles);

// Initialize Terminal Emulator
const terminalEmulator = new TerminalEmulator();

// Export for global access
window.terminalEmulator = terminalEmulator;
