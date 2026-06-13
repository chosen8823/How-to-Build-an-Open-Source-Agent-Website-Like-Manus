/* SoulPHYA Field — Background Service Worker
   Maintains persistent WebSocket to MCP server. */

let ws = null;
let pending = [];
let wsUrl = 'ws://localhost:8765';

// Load configured WebSocket URL from storage
chrome.storage.local.get(['soulphya_settings'], (r) => {
  if (r.soulphya_settings && r.soulphya_settings.wsUrl) {
    wsUrl = r.soulphya_settings.wsUrl;
  }
  connect();
});

// React to runtime settings changes
chrome.storage.onChanged.addListener((changes, areaName) => {
  if (areaName === 'local' && changes.soulphya_settings) {
    const newSettings = changes.soulphya_settings.newValue;
    if (newSettings && newSettings.wsUrl && newSettings.wsUrl !== wsUrl) {
      wsUrl = newSettings.wsUrl;
      if (ws) { ws.close(); }
    }
  }
});

function connect() {
  try {
    ws = new WebSocket(wsUrl);

    ws.onopen = () => {
      console.log('[SoulPHYA] WebSocket connected to MCP server');
      pending.forEach(m => ws.send(m));
      pending = [];
    };

    ws.onmessage = (e) => {
      try {
        chrome.runtime.sendMessage({
          type: 'mcp_event',
          data: JSON.parse(e.data)
        }, () => {
          if (chrome.runtime.lastError) { /* no listener — ignored */ }
        });
      } catch (_) { /* popup closed */ }
    };

    ws.onclose = () => {
      console.log('[SoulPHYA] WebSocket closed, reconnecting in 3s…');
      setTimeout(connect, 3000);
    };

    ws.onerror = () => ws.close();
  } catch (e) {
    console.error('[SoulPHYA] WebSocket error:', e);
    setTimeout(connect, 5000);
  }
}

chrome.runtime.onMessage.addListener((msg) => {
  if (msg.type === 'mcp_send') {
    const p = JSON.stringify(msg.data);
    if (ws?.readyState === WebSocket.OPEN) ws.send(p);
    else pending.push(p);
  }
});
