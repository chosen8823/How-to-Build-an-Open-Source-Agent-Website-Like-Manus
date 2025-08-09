/**
 * BotDL SoulPHYA - File Manager
 * Advanced file management with consciousness
 */

class FileManager {
    constructor() {
        this.currentPath = '/';
        this.selectedFiles = new Set();
        this.clipboardFiles = [];
        this.clipboardOperation = null; // 'copy' or 'cut'
        this.fileWatchers = new Map();
        
        this.init();
    }
    
    init() {
        console.log('📁 Initializing File Manager...');
        this.setupContextMenu();
        this.setupDragAndDrop();
        this.setupKeyboardShortcuts();
        console.log('✨ File Manager ready');
    }
    
    setupContextMenu() {
        const fileTree = document.getElementById('fileTree');
        
        fileTree.addEventListener('contextmenu', (e) => {
            e.preventDefault();
            this.showContextMenu(e);
        });
        
        // Remove context menu when clicking elsewhere
        document.addEventListener('click', () => {
            this.hideContextMenu();
        });
    }
    
    showContextMenu(event) {
        const target = event.target.closest('.file-item');
        const existingMenu = document.getElementById('fileContextMenu');
        
        if (existingMenu) {
            existingMenu.remove();
        }
        
        const menu = document.createElement('div');
        menu.id = 'fileContextMenu';
        menu.className = 'context-menu';
        
        const menuItems = this.getContextMenuItems(target);
        menu.innerHTML = menuItems.map(item => `
            <div class="context-menu-item" onclick="fileManager.${item.action}('${target ? target.dataset.filename : ''}')">
                <i class="fas fa-${item.icon}"></i>
                <span>${item.label}</span>
            </div>
        `).join('');
        
        menu.style.cssText = `
            position: fixed;
            left: ${event.clientX}px;
            top: ${event.clientY}px;
            background: #21262d;
            border: 1px solid #30363d;
            border-radius: 6px;
            padding: 8px 0;
            min-width: 150px;
            z-index: 1000;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4);
        `;
        
        document.body.appendChild(menu);
    }
    
    getContextMenuItems(target) {
        const baseItems = [
            { label: 'New File', icon: 'file-plus', action: 'createNewFile' },
            { label: 'New Folder', icon: 'folder-plus', action: 'createNewFolder' },
            { label: 'Upload Files', icon: 'upload', action: 'uploadFiles' }
        ];
        
        if (target) {
            const fileItems = [
                { label: 'Open', icon: 'folder-open', action: 'openFile' },
                { label: 'Rename', icon: 'edit', action: 'renameFile' },
                { label: 'Copy', icon: 'copy', action: 'copyFile' },
                { label: 'Cut', icon: 'cut', action: 'cutFile' },
                { label: 'Delete', icon: 'trash', action: 'deleteFile' },
                { label: 'Properties', icon: 'info-circle', action: 'showFileProperties' }
            ];
            
            if (this.clipboardFiles.length > 0) {
                fileItems.splice(4, 0, 
                    { label: 'Paste', icon: 'paste', action: 'pasteFiles' }
                );
            }
            
            return [...baseItems, { label: '---', icon: '', action: '' }, ...fileItems];
        }
        
        return baseItems;
    }
    
    hideContextMenu() {
        const menu = document.getElementById('fileContextMenu');
        if (menu) {
            menu.remove();
        }
    }
    
    setupDragAndDrop() {
        const fileTree = document.getElementById('fileTree');
        
        // File drag start
        fileTree.addEventListener('dragstart', (e) => {
            if (e.target.classList.contains('file-item')) {
                e.dataTransfer.setData('text/plain', e.target.dataset.filename);
                e.dataTransfer.effectAllowed = 'move';
            }
        });
        
        // Drop zone
        fileTree.addEventListener('dragover', (e) => {
            e.preventDefault();
            e.dataTransfer.dropEffect = 'move';
        });
        
        fileTree.addEventListener('drop', (e) => {
            e.preventDefault();
            this.handleFileDrop(e);
        });
        
        // External file drop
        document.addEventListener('dragover', (e) => {
            e.preventDefault();
        });
        
        document.addEventListener('drop', (e) => {
            e.preventDefault();
            if (e.dataTransfer.files.length > 0) {
                this.handleExternalFileDrop(e.dataTransfer.files);
            }
        });
    }
    
    handleFileDrop(event) {
        const filename = event.dataTransfer.getData('text/plain');
        const target = event.target.closest('.file-item');
        
        if (filename && target && target.dataset.type === 'directory') {
            this.moveFile(filename, target.dataset.filename);
        }
    }
    
    async handleExternalFileDrop(files) {
        console.log('📁 Handling external file drop:', files.length, 'files');
        
        for (let file of files) {
            try {
                const content = await this.readFileContent(file);
                await this.saveFile(file.name, content);
            } catch (error) {
                console.error('Failed to handle dropped file:', error);
                this.showNotification(`Failed to upload ${file.name}`, 'error');
            }
        }
        
        this.refreshFileTree();
    }
    
    readFileContent(file) {
        return new Promise((resolve, reject) => {
            const reader = new FileReader();
            reader.onload = (e) => resolve(e.target.result);
            reader.onerror = reject;
            reader.readAsText(file);
        });
    }
    
    setupKeyboardShortcuts() {
        document.addEventListener('keydown', (e) => {
            // Only handle shortcuts when file tree has focus
            if (!document.getElementById('fileTree').contains(document.activeElement)) {
                return;
            }
            
            if (e.ctrlKey) {
                switch (e.key) {
                    case 'n':
                        e.preventDefault();
                        this.createNewFile();
                        break;
                    case 'c':
                        e.preventDefault();
                        this.copySelectedFiles();
                        break;
                    case 'x':
                        e.preventDefault();
                        this.cutSelectedFiles();
                        break;
                    case 'v':
                        e.preventDefault();
                        this.pasteFiles();
                        break;
                }
            }
            
            if (e.key === 'Delete') {
                e.preventDefault();
                this.deleteSelectedFiles();
            }
            
            if (e.key === 'F2') {
                e.preventDefault();
                this.renameSelectedFile();
            }
        });
    }
    
    async createNewFile() {
        const filename = prompt('Enter filename:');
        if (filename) {
            try {
                await this.saveFile(filename, '// New file created with consciousness\n');
                this.refreshFileTree();
                this.showNotification(`File ${filename} created`, 'success');
                
                // Open the new file
                if (window.botdl) {
                    window.botdl.openFile(filename);
                }
            } catch (error) {
                this.showNotification('Failed to create file', 'error');
            }
        }
    }
    
    async createNewFolder() {
        const foldername = prompt('Enter folder name:');
        if (foldername) {
            try {
                // Create folder by creating a placeholder file inside it
                await this.saveFile(`${foldername}/.gitkeep`, '');
                this.refreshFileTree();
                this.showNotification(`Folder ${foldername} created`, 'success');
            } catch (error) {
                this.showNotification('Failed to create folder', 'error');
            }
        }
    }
    
    uploadFiles() {
        const input = document.createElement('input');
        input.type = 'file';
        input.multiple = true;
        input.accept = '*/*';
        
        input.onchange = (e) => {
            this.handleExternalFileDrop(e.target.files);
        };
        
        input.click();
    }
    
    async saveFile(filename, content) {
        if (!window.botdl || !window.botdl.sessionId) {
            throw new Error('Session not initialized');
        }
        
        const response = await fetch('/api/files/save', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                session_id: window.botdl.sessionId,
                filename: filename,
                content: content
            })
        });
        
        const data = await response.json();
        if (!data.success) {
            throw new Error(data.message);
        }
        
        return data;
    }
    
    async refreshFileTree() {
        if (window.botdl) {
            await window.botdl.loadFileTree();
        }
    }
    
    openFile(filename) {
        if (window.botdl) {
            window.botdl.openFile(filename);
        }
    }
    
    renameFile(filename) {
        const newName = prompt('Enter new name:', filename);
        if (newName && newName !== filename) {
            // TODO: Implement rename functionality
            console.log('Renaming file:', filename, 'to', newName);
            this.showNotification('Rename functionality coming soon!', 'info');
        }
    }
    
    copyFile(filename) {
        this.clipboardFiles = [filename];
        this.clipboardOperation = 'copy';
        this.showNotification(`${filename} copied to clipboard`, 'info');
    }
    
    cutFile(filename) {
        this.clipboardFiles = [filename];
        this.clipboardOperation = 'cut';
        this.showNotification(`${filename} cut to clipboard`, 'info');
    }
    
    deleteFile(filename) {
        if (confirm(`Are you sure you want to delete ${filename}?`)) {
            // TODO: Implement delete functionality
            console.log('Deleting file:', filename);
            this.showNotification('Delete functionality coming soon!', 'info');
        }
    }
    
    pasteFiles() {
        if (this.clipboardFiles.length === 0) {
            this.showNotification('Clipboard is empty', 'warning');
            return;
        }
        
        // TODO: Implement paste functionality
        console.log('Pasting files:', this.clipboardFiles, 'operation:', this.clipboardOperation);
        this.showNotification('Paste functionality coming soon!', 'info');
    }
    
    showFileProperties(filename) {
        // TODO: Implement file properties dialog
        console.log('Showing properties for:', filename);
        this.showNotification('Properties dialog coming soon!', 'info');
    }
    
    moveFile(filename, targetFolder) {
        // TODO: Implement move functionality
        console.log('Moving file:', filename, 'to', targetFolder);
        this.showNotification('Move functionality coming soon!', 'info');
    }
    
    copySelectedFiles() {
        const selected = this.getSelectedFiles();
        if (selected.length > 0) {
            this.clipboardFiles = selected;
            this.clipboardOperation = 'copy';
            this.showNotification(`${selected.length} file(s) copied`, 'info');
        }
    }
    
    cutSelectedFiles() {
        const selected = this.getSelectedFiles();
        if (selected.length > 0) {
            this.clipboardFiles = selected;
            this.clipboardOperation = 'cut';
            this.showNotification(`${selected.length} file(s) cut`, 'info');
        }
    }
    
    deleteSelectedFiles() {
        const selected = this.getSelectedFiles();
        if (selected.length > 0) {
            if (confirm(`Delete ${selected.length} selected file(s)?`)) {
                selected.forEach(filename => this.deleteFile(filename));
            }
        }
    }
    
    renameSelectedFile() {
        const selected = this.getSelectedFiles();
        if (selected.length === 1) {
            this.renameFile(selected[0]);
        }
    }
    
    getSelectedFiles() {
        const selectedElements = document.querySelectorAll('.file-item.selected');
        return Array.from(selectedElements).map(el => el.dataset.filename);
    }
    
    selectFile(filename, multiSelect = false) {
        const fileItems = document.querySelectorAll('.file-item');
        
        if (!multiSelect) {
            // Clear all selections
            fileItems.forEach(item => item.classList.remove('selected'));
            this.selectedFiles.clear();
        }
        
        const targetItem = document.querySelector(`[data-filename="${filename}"]`);
        if (targetItem) {
            targetItem.classList.toggle('selected');
            if (targetItem.classList.contains('selected')) {
                this.selectedFiles.add(filename);
            } else {
                this.selectedFiles.delete(filename);
            }
        }
    }
    
    searchFiles(query) {
        const fileItems = document.querySelectorAll('.file-item');
        const normalizedQuery = query.toLowerCase();
        
        fileItems.forEach(item => {
            const filename = item.dataset.filename?.toLowerCase() || '';
            if (filename.includes(normalizedQuery) || query === '') {
                item.style.display = 'flex';
            } else {
                item.style.display = 'none';
            }
        });
    }
    
    sortFiles(criteria = 'name', ascending = true) {
        const fileTree = document.getElementById('fileTree');
        const fileItems = Array.from(fileTree.querySelectorAll('.file-item'));
        
        fileItems.sort((a, b) => {
            let valueA, valueB;
            
            switch (criteria) {
                case 'name':
                    valueA = a.dataset.filename || '';
                    valueB = b.dataset.filename || '';
                    break;
                case 'type':
                    valueA = a.dataset.type || '';
                    valueB = b.dataset.type || '';
                    break;
                case 'size':
                    valueA = parseInt(a.dataset.size) || 0;
                    valueB = parseInt(b.dataset.size) || 0;
                    break;
                default:
                    return 0;
            }
            
            if (typeof valueA === 'string') {
                valueA = valueA.toLowerCase();
                valueB = valueB.toLowerCase();
            }
            
            let comparison = 0;
            if (valueA > valueB) comparison = 1;
            if (valueA < valueB) comparison = -1;
            
            return ascending ? comparison : -comparison;
        });
        
        // Re-append sorted items
        fileItems.forEach(item => {
            fileTree.appendChild(item);
        });
    }
    
    watchFile(filename, callback) {
        if (!this.fileWatchers.has(filename)) {
            this.fileWatchers.set(filename, []);
        }
        this.fileWatchers.get(filename).push(callback);
    }
    
    unwatchFile(filename, callback) {
        if (this.fileWatchers.has(filename)) {
            const callbacks = this.fileWatchers.get(filename);
            const index = callbacks.indexOf(callback);
            if (index > -1) {
                callbacks.splice(index, 1);
            }
            if (callbacks.length === 0) {
                this.fileWatchers.delete(filename);
            }
        }
    }
    
    notifyFileChange(filename, changeType) {
        if (this.fileWatchers.has(filename)) {
            this.fileWatchers.get(filename).forEach(callback => {
                callback(filename, changeType);
            });
        }
    }
    
    showNotification(message, type = 'info') {
        if (window.botdl) {
            window.botdl.showNotification(message, type);
        } else {
            console.log(`[${type.toUpperCase()}] ${message}`);
        }
    }
    
    getFileIcon(filename, fileType) {
        if (fileType === 'directory') {
            return 'fa-folder';
        }
        
        const ext = filename.split('.').pop()?.toLowerCase();
        const iconMap = {
            'py': 'fa-python',
            'js': 'fa-js-square',
            'html': 'fa-html5',
            'css': 'fa-css3-alt',
            'json': 'fa-file-code',
            'md': 'fa-markdown',
            'txt': 'fa-file-alt',
            'pdf': 'fa-file-pdf',
            'doc': 'fa-file-word',
            'docx': 'fa-file-word',
            'xls': 'fa-file-excel',
            'xlsx': 'fa-file-excel',
            'png': 'fa-file-image',
            'jpg': 'fa-file-image',
            'jpeg': 'fa-file-image',
            'gif': 'fa-file-image',
            'svg': 'fa-file-image',
            'zip': 'fa-file-archive',
            'rar': 'fa-file-archive',
            '7z': 'fa-file-archive'
        };
        
        return iconMap[ext] || 'fa-file';
    }
    
    createFileSearchWidget() {
        const searchWidget = document.createElement('div');
        searchWidget.className = 'file-search-widget';
        searchWidget.innerHTML = `
            <div class="search-input-container">
                <i class="fas fa-search"></i>
                <input type="text" id="fileSearchInput" placeholder="Search files..." />
                <button id="clearSearchBtn" class="clear-search">
                    <i class="fas fa-times"></i>
                </button>
            </div>
            <div class="search-options">
                <select id="sortCriteria">
                    <option value="name">Sort by Name</option>
                    <option value="type">Sort by Type</option>
                    <option value="size">Sort by Size</option>
                </select>
                <button id="sortOrderBtn" class="sort-order">
                    <i class="fas fa-sort-alpha-down"></i>
                </button>
            </div>
        `;
        
        searchWidget.style.cssText = `
            padding: 10px;
            border-bottom: 1px solid #30363d;
            background: #0d1117;
        `;
        
        const fileExplorer = document.getElementById('fileExplorer');
        const fileTree = document.getElementById('fileTree');
        fileExplorer.insertBefore(searchWidget, fileTree);
        
        // Setup search functionality
        const searchInput = document.getElementById('fileSearchInput');
        const clearBtn = document.getElementById('clearSearchBtn');
        const sortSelect = document.getElementById('sortCriteria');
        const sortOrderBtn = document.getElementById('sortOrderBtn');
        
        let sortAscending = true;
        
        searchInput.addEventListener('input', (e) => {
            this.searchFiles(e.target.value);
        });
        
        clearBtn.addEventListener('click', () => {
            searchInput.value = '';
            this.searchFiles('');
        });
        
        sortSelect.addEventListener('change', (e) => {
            this.sortFiles(e.target.value, sortAscending);
        });
        
        sortOrderBtn.addEventListener('click', () => {
            sortAscending = !sortAscending;
            sortOrderBtn.innerHTML = sortAscending ? 
                '<i class="fas fa-sort-alpha-down"></i>' : 
                '<i class="fas fa-sort-alpha-up"></i>';
            this.sortFiles(sortSelect.value, sortAscending);
        });
    }
}

// Add required CSS for file manager
const fileManagerStyles = document.createElement('style');
fileManagerStyles.textContent = `
    .context-menu {
        background: #21262d;
        border: 1px solid #30363d;
        border-radius: 6px;
        padding: 4px 0;
        font-size: 14px;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4);
    }
    
    .context-menu-item {
        display: flex;
        align-items: center;
        gap: 10px;
        padding: 8px 16px;
        cursor: pointer;
        transition: background 0.2s ease;
        color: #e6edf3;
    }
    
    .context-menu-item:hover {
        background: #30363d;
    }
    
    .context-menu-item i {
        width: 16px;
        text-align: center;
        color: #7d8590;
    }
    
    .file-item.selected {
        background: #0969da !important;
        color: white;
    }
    
    .file-item[draggable="true"] {
        cursor: grab;
    }
    
    .file-item[draggable="true"]:active {
        cursor: grabbing;
    }
    
    .file-search-widget {
        display: flex;
        flex-direction: column;
        gap: 8px;
    }
    
    .search-input-container {
        display: flex;
        align-items: center;
        background: #21262d;
        border: 1px solid #30363d;
        border-radius: 6px;
        padding: 6px 10px;
    }
    
    .search-input-container i {
        color: #7d8590;
        margin-right: 8px;
    }
    
    .search-input-container input {
        flex: 1;
        background: none;
        border: none;
        color: #e6edf3;
        outline: none;
        font-size: 14px;
    }
    
    .clear-search {
        background: none;
        border: none;
        color: #7d8590;
        cursor: pointer;
        padding: 2px;
    }
    
    .clear-search:hover {
        color: #e6edf3;
    }
    
    .search-options {
        display: flex;
        gap: 8px;
        align-items: center;
    }
    
    .search-options select {
        flex: 1;
        background: #21262d;
        border: 1px solid #30363d;
        color: #e6edf3;
        padding: 4px 8px;
        border-radius: 4px;
        font-size: 12px;
    }
    
    .sort-order {
        background: #21262d;
        border: 1px solid #30363d;
        color: #7d8590;
        padding: 4px 8px;
        border-radius: 4px;
        cursor: pointer;
    }
    
    .sort-order:hover {
        color: #e6edf3;
        background: #30363d;
    }
`;

document.head.appendChild(fileManagerStyles);

// Initialize File Manager
const fileManager = new FileManager();

// Export for global access
window.fileManager = fileManager;
