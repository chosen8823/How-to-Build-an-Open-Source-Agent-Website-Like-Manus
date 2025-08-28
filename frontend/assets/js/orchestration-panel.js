// OrchestrationPanel - Multi-agent team/task UI
class OrchestrationPanel {
    constructor() {
        this.el = document.getElementById('orchestrationPanel');
        this.formationSelect = null;
        this.taskInput = null;
        this.taskList = null;
        this.currentFormation = null;
        this.init();
    }
    async init() {
        if (!this.el) return;
        this.el.innerHTML = `
            <div class="orch-header">
                <h3><i class="fas fa-users"></i> Orchestration</h3>
                <select id="formationSelect"></select>
                <button id="orchQuickstart" style="margin-left:12px;">Team Upgrade Quickstart</button>
            </div>
            <div class="orch-agents" id="orchAgents"></div>
            <div class="orch-task-entry">
                <input id="orchTaskInput" type="text" placeholder="Describe a new task..." />
                <button id="orchTaskSubmit">Submit Task</button>
            </div>
            <div class="orch-tasks" id="orchTaskList"></div>
        `;
        this.formationSelect = document.getElementById('formationSelect');
        this.taskInput = document.getElementById('orchTaskInput');
        this.taskList = document.getElementById('orchTaskList');
        document.getElementById('orchTaskSubmit').onclick = () => this.submitTask();
        this.formationSelect.onchange = () => this.selectFormation();
        document.getElementById('orchQuickstart').onclick = () => this.quickstartTeamUpgrade();
        await this.loadFormations();
    }
    async quickstartTeamUpgrade() {
        // Team-of-teams upgrade tasks
        const tasks = [
            { description: "Architect: Refine modularity, scalability, and extensibility of the app." },
            { description: "Backend: Add advanced endpoints for streaming, agent logs, and custom dimensions." },
            { description: "Frontend: Polish UI/UX, add live orchestration dashboard, and improve visuals." },
            { description: "QA: Add automated tests and validation for all new features." },
            { description: "Docs: Update README and in-app help to reflect new capabilities." }
        ];
        for (const t of tasks) {
            await fetch(`/api/agents/orchestrators/${this.currentFormation}/tasks`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(t)
            });
        }
        this.loadTasks();
    }
    async loadFormations() {
        const resp = await fetch('/api/agents/formations');
        const data = await resp.json();
        if (data.success && Array.isArray(data.formations)) {
            this.formationSelect.innerHTML = data.formations.map(f => `<option value="${f}">${f}</option>`).join('');
            this.selectFormation();
        }
    }
    async selectFormation() {
        const name = this.formationSelect.value;
        if (!name) return;
        const resp = await fetch(`/api/agents/formations/${name}`, { method: 'POST' });
        const data = await resp.json();
        if (data.success) {
            this.currentFormation = name;
            this.renderAgents(data.agents);
            this.loadTasks();
        }
    }
    renderAgents(agentIds) {
        const el = document.getElementById('orchAgents');
        el.innerHTML = agentIds.map(id => `<span class="orch-agent">${id}</span>`).join(' ');
    }
    async submitTask() {
        const desc = this.taskInput.value.trim();
        if (!desc || !this.currentFormation) return;
        const resp = await fetch(`/api/agents/orchestrators/${this.currentFormation}/tasks`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ description: desc })
        });
        const data = await resp.json();
        if (data.success) {
            this.taskInput.value = '';
            this.loadTasks();
        }
    }
    async loadTasks() {
        if (!this.currentFormation) return;
        const resp = await fetch(`/api/agents/orchestrators/${this.currentFormation}/tasks`);
        const data = await resp.json();
        if (data.success && Array.isArray(data.tasks)) {
            this.renderTasks(data.tasks);
        }
    }
    renderTasks(tasks) {
        this.taskList.innerHTML = tasks.map(t => `
            <div class="orch-task">
                <div><b>${t.description}</b></div>
                <div>Assigned: <span class="orch-agent">${t.assigned_to}</span></div>
                <div>Status: <span class="orch-status">${t.status}</span></div>
                <div>Result: <span class="orch-result">${t.results && t.results.agent_output ? t.results.agent_output : ''}</span></div>
            </div>
        `).join('');
    }
}
window.orchestrationPanel = new OrchestrationPanel();
