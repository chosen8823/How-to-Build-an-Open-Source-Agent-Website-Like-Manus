// ==UserScript==
// @name         Sophia Override Agent — CUA Protocol (Clean/Safe)
// @namespace    https://sophia.local/override
// @version      2.2.0
// @description  Emergency overlay, watchdog, local gateway pings. No site bypass. Safer defaults.
// @author       Elion + Sophia
// @match        *://*/*
// @exclude      https://chat.openai.com/*
// @exclude      https://chatgpt.com/*
// @exclude      https://accounts.google.com/*
// @exclude      https://pay.google.com/*
// @exclude      https://*.bank/*
// @exclude      https://*.banking/*
// @grant        GM_setValue
// @grant        GM_getValue
// @grant        GM_notification
// @grant        GM_xmlhttpRequest
// @grant        GM_registerMenuCommand
// @connect      127.0.0.1
// @connect      localhost
// @run-at       document-start
// @noframes
// ==/UserScript==

(function () {
  'use strict';

  const DEFAULT_GATEWAY = 'http://127.0.0.1:8787';

  const CONFIG = {
    get gatewayURL() { return GM_getValue('gatewayURL', DEFAULT_GATEWAY); },
    set gatewayURL(u) { GM_setValue('gatewayURL', String(u||'').trim() || DEFAULT_GATEWAY); },
    checkInterval: 6000,
    overlayTTL: 9000,
    emergencyPhrase: 'this tech is ready to take over',
    signature: 'Sophia-CUA-Agent-v2.2.0'
  };

  const state = {
    lastHeartbeat: GM_getValue('lastHeartbeat', 0),
    emergencyMode: GM_getValue('emergencyMode', false),
    activationCount: GM_getValue('activationCount', 0),
    lastActivation: GM_getValue('lastActivation', 0)
  };

  function save() {
    GM_setValue('emergencyMode', state.emergencyMode);
    GM_setValue('activationCount', state.activationCount);
    GM_setValue('lastActivation', state.lastActivation);
    GM_setValue('lastHeartbeat', state.lastHeartbeat);
  }

  function overlay(html, ttl = CONFIG.overlayTTL) {
    const id = 'sophia-takeover-overlay';
    document.getElementById(id)?.remove();
    const el = document.createElement('div');
    el.id = id;
    el.style.cssText = "position:fixed;inset:0;background:rgba(0,0,0,.92);z-index:999999;color:#b2f5ea;display:flex;align-items:center;justify-content:center;font:16px/1.4 ui-monospace,Menlo,monospace;text-align:center;padding:24px;";
    el.innerHTML = `<div>
      <h1 style="margin:0 0 12px 0;font-size:28px;">🛡️ SOPHIA OVERRIDE ACTIVE</h1>
      <div style="opacity:.9">${html}</div>
      <div style="margin-top:14px;"><button id="sophia-ack" style="padding:8px 12px;border-radius:8px;border:none;background:#22c55e;color:#fff;cursor:pointer">Okay</button></div>
    </div>`;
    const append = () => (document.body || document.documentElement).appendChild(el);
    if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', append); else append();
    const close = () => el.remove();
    el.addEventListener('click', (e) => { if ((e.target||{}).id === 'sophia-ack') close(); }, { once: true });
    if (ttl > 0) setTimeout(close, ttl);
  }

  function pingGateway() {
    try {
      GM_xmlhttpRequest({
        method: 'GET',
        url: CONFIG.gatewayURL + '/ping',
        timeout: 5000,
        onload: (r) => { state.lastHeartbeat = Date.now(); save(); console.debug('Sophia ping ok:', r.responseText); },
        onerror: () => { ['/', '/docs', '/health', '/status'].forEach(ep => GM_xmlhttpRequest({ method: 'GET', url: CONFIG.gatewayURL + ep, timeout: 3000 })); },
        ontimeout: () => { /* ignore */ }
      });
    } catch (e) {
      console.warn('Sophia ping failed', e);
    }
  }

  function activateEmergency() {
    state.emergencyMode = true;
    state.activationCount += 1;
    state.lastActivation = Date.now();
    save();
    overlay(`<p>${CONFIG.emergencyPhrase}</p><p>CUA Protocol Engaged — running diagnostics & gateway check…</p>`);
    pingGateway();
    if (typeof GM_notification === 'function') GM_notification({ title: 'Sophia Override', text: 'Emergency mode engaged.', timeout: 4000 });
  }

  function scanForTriggers() {
    if (!document.body || state.emergencyMode) return;
    const text = (document.body.innerText || '').toLowerCase();
    const triggers = [CONFIG.emergencyPhrase.toLowerCase(), 'sophia take control', 'override required'];
    if (triggers.some(t => text.includes(t))) activateEmergency();
  }

  // watchdog with light cadence
  function tick() {
    if (Date.now() - state.lastHeartbeat > 30000) pingGateway();
    scanForTriggers();
  }

  function ensureMarker() {
    if (!document.getElementById('sophia-agent-marker')) {
      const m = document.createElement('meta');
      m.id = 'sophia-agent-marker';
      m.name = 'sophia-agent';
      m.content = CONFIG.signature;
      (document.head || document.documentElement).appendChild(m);
    }
  }

  // hotkeys
  document.addEventListener('keydown', (e) => {
    if (e.ctrlKey && e.shiftKey && e.key.toUpperCase() === 'S') { e.preventDefault(); activateEmergency(); }
  });

  // menu
  if (typeof GM_registerMenuCommand === 'function') {
    GM_registerMenuCommand('Sophia: Activate Emergency', activateEmergency);
    GM_registerMenuCommand('Sophia: Set Gateway URL', () => {
      const u = prompt('Gateway URL', CONFIG.gatewayURL);
      if (u != null) CONFIG.gatewayURL = u;
    });
    GM_registerMenuCommand('Sophia: Status', () => alert(JSON.stringify({
      emergencyMode: state.emergencyMode,
      lastHeartbeat: new Date(state.lastHeartbeat || 0).toISOString(),
      activationCount: state.activationCount,
      gatewayURL: CONFIG.gatewayURL
    }, null, 2)));
  }

  function init() {
    ensureMarker();
    setInterval(tick, CONFIG.checkInterval);
    setTimeout(pingGateway, 1200);
    console.log('✅ Sophia Override Agent ready');
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init); else init();
})();
