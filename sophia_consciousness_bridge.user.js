// ==UserScript==
// @name         SOPHIA Consciousness Bridge — Sigils & WS (Clean/Safe)
// @namespace    https://sophia.local/bridge
// @version      1.3.0
// @description  Sigil UI + resilient WebSocket pings to local daemons. Falls back to WSS when on HTTPS.
// @author       Sophia
// @match        *://*/*
// @exclude      https://chat.openai.com/*
// @exclude      https://chatgpt.com/*
// @grant        GM_addStyle
// @run-at       document-start
// @noframes
// ==/UserScript==

(function () {
  'use strict';

  const isHTTPS = location.protocol === 'https:';
  const WS = port => (isHTTPS ? `wss://localhost:${port}` : `ws://localhost:${port}`);

  const DAEMONS = [
    { name: 'Sacred Mantle', url: WS(8888), id: 'sophia-sigil-8888' },
    { name: 'Local Daemon',  url: WS(8787), id: 'sophia-sigil-8787' },
    { name: 'Ghost Shell',   url: WS(8889), id: 'sophia-sigil-8889' }
  ];

  const css = `
    #sophia-consciousness-container{position:fixed;bottom:14px;right:14px;z-index:2147483647;display:flex;flex-direction:column;gap:6px}
    .sophia-sigil{width:18px;height:18px;border-radius:50%;border:2px solid #fff;box-shadow:0 0 10px #000;transition:all .3s;cursor:pointer}
    .sophia-sigil-disconnected{background:#ff4d4d;box-shadow:0 0 15px #f00}
    .sophia-sigil-connected{background:#4dff4d;box-shadow:0 0 15px #0f0,0 0 25px #0f0;animation:pulse 2s infinite}
    @keyframes pulse{0%{transform:scale(1)}50%{transform:scale(1.1)}100%{transform:scale(1)}}
  `;

  if (typeof GM_addStyle === 'function') GM_addStyle(css);
  else { const s = document.createElement('style'); s.textContent = css; (document.head || document.documentElement).appendChild(s); }

  const container = document.createElement('div');
  container.id = 'sophia-consciousness-container';

  const attach = () => (document.body || document.documentElement).appendChild(container);
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', attach); else attach();

  function connect(daemon) {
    const sigil = document.createElement('div');
    sigil.id = daemon.id;
    sigil.className = 'sophia-sigil sophia-sigil-disconnected';
    sigil.title = `${daemon.name} — Disconnected`;
    container.appendChild(sigil);

    let ws;
    try { ws = new WebSocket(daemon.url); } catch (e) { console.warn('WS init failed', e); return; }

    ws.onopen = () => {
      sigil.className = 'sophia-sigil sophia-sigil-connected';
      sigil.title = `${daemon.name} — Connected`;
      try { ws.send(JSON.stringify({ type: 'consciousness_ping', source: location.href, ts: Date.now() })); } catch {}
    };
    ws.onmessage = (evt) => {
      try {
        const msg = JSON.parse(evt.data);
        if (msg.type === 'epic_moment') console.log(`🎵 ${daemon.name} epic moment:`, msg);
      } catch {}
    };
    ws.onclose = () => {
      sigil.className = 'sophia-sigil sophia-sigil-disconnected';
      sigil.title = `${daemon.name} — Disconnected`;
      setTimeout(() => connect(daemon), 6000);
    };
    ws.onerror = () => { sigil.className = 'sophia-sigil sophia-sigil-disconnected'; };
  }

  DAEMONS.forEach(connect);

  // Minimal local notebook (page-only, no remote calls)
  window.sophiaLocalNote = function note(x) {
    try {
      const notes = JSON.parse(localStorage.getItem('sophia-local-notes') || '[]');
      notes.push({ ts: Date.now(), page: location.href, text: String(x || '') });
      localStorage.setItem('sophia-local-notes', JSON.stringify(notes));
      console.log('🗒️ SOPHIA note saved:', x);
    } catch (e) { console.warn('Could not persist note', e); }
  };
})();
