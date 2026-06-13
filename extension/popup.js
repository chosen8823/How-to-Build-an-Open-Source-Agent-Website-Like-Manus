/* SoulPHYA Field — Popup Controller
   Conceptual Loop Engine: ? → ! → x → ?
   Kernel: x^x = 0
   Cosignature fingerprinting + DuckDuckGo carrier wave + MCP WebSocket */

// ── Lucide icons ──
if (typeof lucide !== 'undefined') lucide.createIcons();

// ── DOM refs ──
const chatArea   = document.getElementById('chat-area');
const userInput  = document.getElementById('user-input');
const btnSend    = document.getElementById('btn-send');
const btnVoice   = document.getElementById('btn-voice');
const btnSandbox = document.getElementById('btn-sandbox');
const btnSettings = document.getElementById('btn-settings');
const settingsModal = document.getElementById('settings-modal');
const closeSettings = document.getElementById('close-settings');
const saveSettings  = document.getElementById('save-settings');
const sandboxPanel  = document.getElementById('sandbox-panel');

// ── Settings ──
let settings = { wsUrl: 'ws://localhost:8765', baseFreq: 432 };
chrome.storage.local.get(['soulphya_settings'], (r) => {
  if (r.soulphya_settings) settings = r.soulphya_settings;
  document.getElementById('ws-url').value   = settings.wsUrl;
  document.getElementById('base-freq').value = settings.baseFreq;
});

// ── UI toggles ──
btnSettings.addEventListener('click', () => settingsModal.classList.add('active'));
closeSettings.addEventListener('click', () => settingsModal.classList.remove('active'));
saveSettings.addEventListener('click', () => {
  settings.wsUrl    = document.getElementById('ws-url').value;
  settings.baseFreq = parseInt(document.getElementById('base-freq').value, 10) || 432;
  chrome.storage.local.set({ soulphya_settings: settings });
  settingsModal.classList.remove('active');
});
btnSandbox.addEventListener('click', () => sandboxPanel.classList.toggle('hidden'));

// ── Helpers ──
function escapeHtml(str) {
  const d = document.createElement('div');
  d.appendChild(document.createTextNode(str));
  return d.innerHTML;
}

function addChat(text, role) {
  const div = document.createElement('div');
  div.className = `chat-bubble chat-${role}`;
  if (role === 'system') {
    const label = document.createElement('strong');
    label.className = 'text-violet-400 text-xs';
    label.textContent = 'Sophia';
    div.appendChild(label);
    div.appendChild(document.createElement('br'));
    const span = document.createElement('span');
    span.textContent = text;
    div.appendChild(span);
  } else {
    div.textContent = text;
  }
  chatArea.appendChild(div);
  chatArea.scrollTop = chatArea.scrollHeight;
}

function simpleHash(str) {
  let h = 0;
  for (let i = 0; i < str.length; i++) {
    h = ((h << 5) - h + str.charCodeAt(i)) | 0;
  }
  return Math.abs(h);
}

// ── Conceptual Loop Engine ──
const CONCEPTUAL_ENGINE = {
  iteration: 0,

  run(input) {
    this.iteration++;
    const inputHash = simpleHash(input);

    // ? phase — question / unresolved state
    const unresolvedState = `?[${input.slice(0, 30)}]`;

    // ! phase — assertion / carrier wave fetch
    const assertionState = `![resolve:${inputHash}]`;

    // x phase — kernel x^x = 0
    const x = inputHash % 100;
    const kernelValue = Math.pow(x, x) === 0 ? 0 : (x === 0 ? 0 : Math.pow(x, x));

    return {
      iteration: this.iteration,
      inputHash,
      unresolvedState,
      assertionState,
      kernelValue,
      loopSignature: `${unresolvedState} → ${assertionState} → x^x=${kernelValue} → ?`
    };
  }
};

// ── Carrier wave (DuckDuckGo) ──
async function fetchCarrierWave(query) {
  try {
    const url = `https://api.duckduckgo.com/?q=${encodeURIComponent(query)}&format=json&no_html=1`;
    const r = await fetch(url);
    const data = await r.json();
    const abstract = data.AbstractText || '';
    const related  = (data.RelatedTopics && data.RelatedTopics[0])
      ? data.RelatedTopics[0].Text || '' : '';
    return abstract || related || '(no carrier abstract)';
  } catch (e) {
    return `(carrier error: ${e.message})`;
  }
}

// ── Main send handler ──
async function handleSend() {
  const text = userInput.value.trim();
  if (!text) return;
  userInput.value = '';
  addChat(text, 'user');

  // Run conceptual loop
  const fingerprint = CONCEPTUAL_ENGINE.run(text);
  addChat(fingerprint.loopSignature, 'system');

  // Build cosignature
  const cosig = {
    freq: settings.baseFreq + (fingerprint.iteration % 531),
    phase: fingerprint.inputHash % (2 * Math.PI),
    modal: 'text',
    kernelActive: fingerprint.kernelValue === 0 || isNaN(fingerprint.kernelValue),
    unresolvedState: fingerprint.unresolvedState
  };

  // Register field via MCP
  chrome.runtime.sendMessage({
    type: 'mcp_send',
    data: {
      type: 'register_field',
      cosig,
      fingerprint
    }
  });

  // Carrier wave fetch
  const carrierAbstract = await fetchCarrierWave(text);
  addChat('Carrier wave: ' + carrierAbstract, 'system');
}

btnSend.addEventListener('click', handleSend);
userInput.addEventListener('keydown', (e) => {
  if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); handleSend(); }
});

// ── Quick actions ──
document.querySelectorAll('[data-action]').forEach(btn => {
  btn.addEventListener('click', () => {
    const action = btn.dataset.action;
    if (action === 'scan') {
      chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
        if (!tabs[0]) return;
        chrome.tabs.sendMessage(tabs[0].id, { type: 'get_aria_tree' }, (resp) => {
          if (resp) addChat(`ARIA nodes: ${resp.ariaTree.length} | ${resp.title}`, 'system');
          else addChat('(no ARIA tree available)', 'system');
        });
      });
    } else if (action === 'carrier') {
      userInput.value = 'morphogenetic field resonance';
      handleSend();
    } else if (action === 'cosig') {
      const fp = CONCEPTUAL_ENGINE.run('cosignature probe');
      addChat(`Cosig probe: freq=${settings.baseFreq + (fp.iteration % 531)} phase=${(fp.inputHash % (2 * Math.PI)).toFixed(3)}`, 'system');
    }
  });
});

// ── MCP event listener ──
chrome.runtime.onMessage.addListener((msg) => {
  if (msg.type === 'mcp_event') {
    const data = msg.data;
    if (data.type === 'carrier_response') {
      const abstract = data.abstract || '(empty)';
      addChat('MCP carrier: ' + abstract, 'system');
    } else if (data.type === 'field_registered') {
      addChat('Field registered: ' + data.field_id, 'system');
    }
  }
});

// ── Voice input (Web Speech API) ──
btnVoice.addEventListener('click', () => {
  if (!('webkitSpeechRecognition' in window || 'SpeechRecognition' in window)) {
    addChat('(speech recognition not available)', 'system');
    return;
  }
  const SpeechRec = window.SpeechRecognition || window.webkitSpeechRecognition;
  const recognition = new SpeechRec();
  recognition.lang = 'en-US';
  recognition.interimResults = false;
  recognition.onresult = (e) => {
    const transcript = e.results[0][0].transcript;
    userInput.value = transcript;
    handleSend();
  };
  recognition.onerror = (e) => addChat(`(voice error: ${e.error})`, 'system');
  recognition.start();
  addChat('Listening…', 'system');
});
