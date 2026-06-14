class FrameRenderer {
    constructor(canvas) {
        this.canvas = canvas;
        this.ctx = canvas.getContext('2d');
        this.trees = {};       // root_frame_id -> parsed tree
        this.positions = {};   // frame_id -> {x, y}
        this.artifactPos = {}; // artifact_id -> {x, y, parentX, parentY}
        this.t = 0;
        this.selected = null;  // selected frame_id or artifact_id
        this.sse = null;
        this._init();
    }

    async _init() {
        // Load all existing trees
        try {
            const resp = await fetch('/api/frames/list');
            const ids = await resp.json();
            for (const id of ids.root_frame_ids) {
                await this._loadTree(id);
            }
        } catch (e) {
            console.warn('Frame store not available:', e);
        }
        // Connect SSE
        try {
            this.sse = new EventSource('/api/frames/stream');
            this.sse.onmessage = (e) => {
                const ev = JSON.parse(e.data);
                if (ev.type === 'tree_ingested') this._loadTree(ev.root_frame_id);
            };
        } catch (e) {
            console.warn('SSE not available:', e);
        }
        this._layout();
        this._loop();
        this.canvas.addEventListener('click', (e) => this._onClick(e));
    }

    async _loadTree(rootId) {
        const resp = await fetch(`/api/frames/${rootId}`);
        const tree = await resp.json();
        this.trees[rootId] = tree;
        this._layout();
    }

    _layout() {
        // Radial layout: root frame at center, child frames orbit at radius 180px
        // Artifacts orbit their parent frame at radius 60px
        const W = this.canvas.width, H = this.canvas.height;
        const cx = W / 2, cy = H / 2;

        let treeIdx = 0;
        for (const [rootId, tree] of Object.entries(this.trees)) {
            const rootAngle = (treeIdx / Object.keys(this.trees).length) * Math.PI * 2;
            const rootX = cx + Math.cos(rootAngle) * 200 * treeIdx;
            const rootY = cy + Math.sin(rootAngle) * 200 * treeIdx;
            this.positions[tree.root_frame.id] = {x: rootX, y: rootY, frame: tree.root_frame};

            // Group artifacts by frame_id
            const byFrame = {};
            for (const art of tree.artifacts) {
                if (!byFrame[art.frame_id]) byFrame[art.frame_id] = [];
                byFrame[art.frame_id].push(art);
            }

            // Root frame's own artifacts
            const rootArts = byFrame[tree.root_frame.id] || [];
            rootArts.forEach((art, i) => {
                const a = (i / Math.max(rootArts.length, 1)) * Math.PI * 2;
                this.artifactPos[art.artifact_id] = {
                    x: rootX + Math.cos(a) * 60,
                    y: rootY + Math.sin(a) * 60,
                    parentX: rootX, parentY: rootY,
                    art
                };
            });

            // Child frames (inferred from artifacts with different frame_ids)
            const childFrameIds = [...new Set(tree.artifacts.map(a => a.frame_id).filter(id => id !== tree.root_frame.id))];
            childFrameIds.forEach((fid, fi) => {
                const angle = (fi / Math.max(childFrameIds.length, 1)) * Math.PI * 2;
                const fx = rootX + Math.cos(angle) * 180;
                const fy = rootY + Math.sin(angle) * 180;
                const agentName = tree.artifacts.find(a => a.frame_id === fid)?.agent_name || 'AGENT';
                this.positions[fid] = {x: fx, y: fy, frame: {id: fid, agent_name: agentName, status: 'completed'}};

                const arts = byFrame[fid] || [];
                arts.forEach((art, i) => {
                    const a = (i / Math.max(arts.length, 1)) * Math.PI * 2;
                    this.artifactPos[art.artifact_id] = {
                        x: fx + Math.cos(a) * 50,
                        y: fy + Math.sin(a) * 50,
                        parentX: fx, parentY: fy,
                        art
                    };
                });
            });
            treeIdx++;
        }
    }

    _draw() {
        const ctx = this.ctx;
        const W = this.canvas.width, H = this.canvas.height;
        ctx.clearRect(0, 0, W, H);
        ctx.fillStyle = '#050508';
        ctx.fillRect(0, 0, W, H);

        // Draw edges: root -> child frames
        for (const [fid, pos] of Object.entries(this.positions)) {
            if (pos.frame?.parent_frame_id && this.positions[pos.frame.parent_frame_id]) {
                const parent = this.positions[pos.frame.parent_frame_id];
                ctx.beginPath();
                ctx.moveTo(parent.x, parent.y);
                ctx.lineTo(pos.x, pos.y);
                ctx.strokeStyle = 'rgba(100,200,255,0.2)';
                ctx.lineWidth = 1;
                ctx.stroke();
            }
        }

        // Draw lines from root to child frames that were inferred from artifacts
        const rootIds = Object.keys(this.trees);
        for (const rootId of rootIds) {
            const rootPos = this.positions[rootId];
            if (!rootPos) continue;
            for (const [fid, pos] of Object.entries(this.positions)) {
                if (fid !== rootId && !pos.frame?.parent_frame_id) {
                    // Inferred child frame -- draw connector to root
                    ctx.beginPath();
                    ctx.moveTo(rootPos.x, rootPos.y);
                    ctx.lineTo(pos.x, pos.y);
                    ctx.strokeStyle = 'rgba(100,200,255,0.2)';
                    ctx.lineWidth = 1;
                    ctx.stroke();
                }
            }
        }

        // Draw artifact satellite edges
        for (const [aid, apos] of Object.entries(this.artifactPos)) {
            ctx.beginPath();
            ctx.moveTo(apos.parentX, apos.parentY);
            ctx.lineTo(apos.x, apos.y);
            ctx.strokeStyle = 'rgba(180,255,180,0.15)';
            ctx.lineWidth = 0.5;
            ctx.stroke();
        }

        // Draw frame nodes
        for (const [fid, pos] of Object.entries(this.positions)) {
            const pulse = Math.sin(this.t * 0.02 + fid.charCodeAt(0) * 0.1) * 5;
            const r = 22 + pulse;
            const isSelected = this.selected === fid;

            ctx.beginPath();
            ctx.arc(pos.x, pos.y, r, 0, Math.PI * 2);
            ctx.fillStyle = isSelected ? 'rgba(100,200,255,0.9)' : 'rgba(60,120,200,0.7)';
            ctx.fill();
            ctx.strokeStyle = isSelected ? '#fff' : 'rgba(100,200,255,0.4)';
            ctx.lineWidth = isSelected ? 2 : 1;
            ctx.stroke();

            // Agent name label
            ctx.fillStyle = '#eef';
            ctx.font = '10px monospace';
            ctx.textAlign = 'center';
            ctx.fillText(pos.frame?.agent_name || fid.slice(0, 8), pos.x, pos.y + r + 14);
            ctx.fillText(pos.frame?.status || '', pos.x, pos.y + r + 26);
        }

        // Draw artifact satellites
        for (const [aid, apos] of Object.entries(this.artifactPos)) {
            const isSelected = this.selected === aid;
            // Color by content_type
            const ct = apos.art.content_type;
            let color = 'rgba(180,255,180,0.7)';
            if (ct === 'image/png') color = 'rgba(255,200,100,0.8)';
            else if (ct === 'chemical/x-pdb') color = 'rgba(255,100,200,0.8)';
            else if (ct === 'text/csv') color = 'rgba(100,255,200,0.8)';

            ctx.beginPath();
            ctx.arc(apos.x, apos.y, isSelected ? 10 : 7, 0, Math.PI * 2);
            ctx.fillStyle = color;
            ctx.fill();

            // Filename label (truncated)
            ctx.fillStyle = 'rgba(220,220,220,0.7)';
            ctx.font = '9px monospace';
            ctx.textAlign = 'center';
            const label = apos.art.filename.length > 18 ? apos.art.filename.slice(0, 15) + '...' : apos.art.filename;
            ctx.fillText(label, apos.x, apos.y + 18);
        }

        this.t++;
    }

    _loop() {
        this._draw();
        requestAnimationFrame(() => this._loop());
    }

    async _onClick(e) {
        const rect = this.canvas.getBoundingClientRect();
        const mx = e.clientX - rect.left;
        const my = e.clientY - rect.top;

        // Check artifact satellites first (smaller, on top)
        for (const [aid, apos] of Object.entries(this.artifactPos)) {
            const dx = mx - apos.x, dy = my - apos.y;
            if (Math.sqrt(dx * dx + dy * dy) < 12) {
                this.selected = aid;
                await this._showArtifact(aid);
                return;
            }
        }

        // Check frame nodes
        for (const [fid, pos] of Object.entries(this.positions)) {
            const dx = mx - pos.x, dy = my - pos.y;
            if (Math.sqrt(dx * dx + dy * dy) < 30) {
                this.selected = fid;
                this._showThoughtStream(fid);
                return;
            }
        }
    }

    async _showArtifact(artifactId) {
        const resp = await fetch(`/api/frames/artifact/${artifactId}`);
        const art = await resp.json();
        const panel = document.getElementById('thought-stream-panel');
        panel.style.display = 'block';

        let html = `<h3 style="color:#aef;margin:0 0 8px">${this._escapeHtml(art.filename)}</h3>`;
        html += `<div style="color:#888;font-size:10px;margin-bottom:12px">${this._escapeHtml(art.content_type)} &middot; ${this._escapeHtml(art.agent_name)} &middot; ${this._escapeHtml(art.storage_path)}</div>`;

        // Show extracted code
        if (art.extracted_code) {
            html += `<div style="color:#8f8;margin-bottom:6px;font-size:11px">EXTRACTED CODE:</div>`;
            html += `<pre style="background:#0a0a18;padding:8px;border-radius:4px;overflow-x:auto;font-size:10px;color:#cfc;max-height:200px;overflow-y:auto">${this._escapeHtml(art.extracted_code.slice(0, 2000))}</pre>`;
        }

        // Show lineage messages (thought stream)
        html += `<div style="color:#8af;margin:12px 0 6px;font-size:11px">THOUGHT STREAM (${art.lineage_messages.length} messages):</div>`;
        for (const msg of art.lineage_messages) {
            const role = msg.role;
            const color = role === 'assistant' ? '#aef' : '#fa8';
            const content = Array.isArray(msg.content)
                ? msg.content.filter(c => c.type === 'text').map(c => c.text).join('\n')
                : msg.content;
            if (content) {
                html += `<div style="margin-bottom:8px"><span style="color:${color};font-size:10px">[${this._escapeHtml(role.toUpperCase())}]</span><div style="color:#ccc;font-size:10px;margin-top:2px;white-space:pre-wrap">${this._escapeHtml(content.slice(0, 500))}</div></div>`;
            }
        }

        // Show environment snapshot
        if (art.environment_snapshot?.packages?.length) {
            html += `<div style="color:#8af;margin:12px 0 6px;font-size:11px">ENVIRONMENT: ${this._escapeHtml(art.environment_snapshot.environment_name)} (Python ${this._escapeHtml(art.environment_snapshot.python_version)})</div>`;
            html += `<div style="color:#888;font-size:9px">${art.environment_snapshot.packages.map(p => `${this._escapeHtml(p.name)}==${this._escapeHtml(p.version)}`).join(', ')}</div>`;
        }

        panel.innerHTML = html;
    }

    _showThoughtStream(frameId) {
        const panel = document.getElementById('thought-stream-panel');
        panel.style.display = 'block';
        const pos = this.positions[frameId];
        if (!pos) return;

        let html = `<h3 style="color:#aef;margin:0 0 8px">${this._escapeHtml(pos.frame?.agent_name || frameId)}</h3>`;
        html += `<div style="color:#888;font-size:10px;margin-bottom:12px">Status: ${this._escapeHtml(pos.frame?.status || 'unknown')}</div>`;

        // Show input/output if root frame
        for (const [rootId, tree] of Object.entries(this.trees)) {
            if (tree.root_frame.id === frameId) {
                html += `<div style="color:#8f8;font-size:11px;margin-bottom:6px">INPUT:</div>`;
                html += `<div style="color:#ccc;font-size:10px;white-space:pre-wrap;margin-bottom:12px">${this._escapeHtml(JSON.stringify(tree.root_frame.input_data, null, 2).slice(0, 500))}</div>`;
                break;
            }
        }

        // Count artifacts for this frame
        let artCount = 0;
        for (const [aid, apos] of Object.entries(this.artifactPos)) {
            if (apos.art.frame_id === frameId) artCount++;
        }
        html += `<div style="color:#fa8;font-size:11px">${artCount} artifacts &mdash; click a satellite dot to inspect</div>`;

        panel.innerHTML = html;
    }

    _escapeHtml(str) {
        if (!str) return '';
        return String(str)
            .replace(/&/g, '&amp;')
            .replace(/</g, '&lt;')
            .replace(/>/g, '&gt;')
            .replace(/"/g, '&quot;');
    }
}

// Initialize on DOM ready
document.addEventListener('DOMContentLoaded', () => {
    const canvas = document.getElementById('frame-canvas');
    if (canvas) {
        canvas.width = canvas.offsetWidth;
        canvas.height = canvas.offsetHeight;
        window._frameRenderer = new FrameRenderer(canvas);
    }
});
