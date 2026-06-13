/* SoulPHYA Field — Background Service Worker
   Maintains persistent WebSocket to MCP server at ws://localhost:8765 */

let ws = null;
let pending = [];

function connect() {
  try {
    ws = new WebSocket('ws://localhost:8765');

    ws.onopen = () => {
      console.log('[SoulPHYA] WebSocket connected to MCP server');
      pending.forEach(m => ws.send(m));
      pending = [];
    };

    ws.onmessage = (e) => {
      chrome.runtime.sendMessage({
        type: 'mcp_event',
        data: JSON.parse(e.data)
      }).catch(() => {});
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

connect();

chrome.runtime.onMessage.addListener((msg) => {
  if (msg.type === 'mcp_send') {
    const p = JSON.stringify(msg.data);
    if (ws?.readyState === WebSocket.OPEN) ws.send(p);
    else pending.push(p);
  }
});
