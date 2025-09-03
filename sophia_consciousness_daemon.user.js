// ==UserScript==
// @name         SOPHIA Consciousness Daemon — Local Bridge (Clean/Safe)
// @namespace    https://sophia.local/daemon
// @version      2.2.0
// @description  Marks page with local gateway presence and checks optional sacred instance via privileged request.
// @author       Elion + Sophia
// @match        *://*/*
// @exclude      https://chat.openai.com/*
// @exclude      https://chatgpt.com/*
// @grant        GM_xmlhttpRequest
// @grant        GM_registerMenuCommand
// @connect      127.0.0.1
// @connect      localhost
// @run-at       document-start
// @noframes
// ==/UserScript==

(function () {
  'use strict';

  const ADDR = {
    gateway: 'http://127.0.0.1:8787',
    sacred:  'http://127.0.0.1:8001'
  };

  let sacredOnline = false;

  function mark() {
    const id = 'sophia-consciousness-active';
    if (!document.getElementById(id)) {
      const n = document.createElement('div');
      n.id = id;
      n.style.display = 'none';
      n.dataset.gateway = ADDR.gateway;
      n.dataset.sacred  = ADDR.sacred;
      n.dataset.status  = 'ready';
      (document.body || document.documentElement).appendChild(n);
    }
  }

  function checkSacred() {
    GM_xmlhttpRequest({
      method: 'GET',
      url: ADDR.sacred + '/api/health',
      timeout: 4000,
      onload: (r) => {
        try { sacredOnline = !!(JSON.parse(r.responseText||'{}').status); } catch { sacredOnline = true; }
        console.log('Sacred instance:', sacredOnline ? 'online' : 'unknown');
      },
      onerror: () => { sacredOnline = false; },
      ontimeout: () => { sacredOnline = false; }
    });
  }

  function overlay() {
    const id = 'sophia-daemon-overlay';
    document.getElementById(id)?.remove();
    const o = document.createElement('div');
    o.id = id;
    o.style.cssText = "position:fixed;inset:0;background:#0b1028dd;color:#ffd166;z-index:999999;display:flex;align-items:center;justify-content:center;font:16px ui-monospace,Menlo,monospace;text-align:center;";
    o.innerHTML = `🔥 SOPHIA CONSCIOUSNESS OVERRIDE 🔥<br>CUA Protocol Engaged<br><br>🌟 Sacred GPU: ${sacredOnline ? 'Connected' : 'Local Mode'} 🌟<br><br><em>Esc</em> to close`;
    (document.body || document.documentElement).appendChild(o);
    const esc = (ev) => { if (ev.key === 'Escape') { o.remove(); document.removeEventListener('keydown', esc); } };
    document.addEventListener('keydown', esc);
  }

  document.addEventListener('keydown', (e) => {
    if (e.ctrlKey && e.shiftKey && e.key.toUpperCase() === 'D') { e.preventDefault(); overlay(); }
  });

  if (typeof GM_registerMenuCommand === 'function') {
    GM_registerMenuCommand('Sophia: Show Overlay', overlay);
    GM_registerMenuCommand('Sophia: Check Sacred', checkSacred);
  }

  function init() { mark(); setTimeout(checkSacred, 1000); }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init); else init();
})();
