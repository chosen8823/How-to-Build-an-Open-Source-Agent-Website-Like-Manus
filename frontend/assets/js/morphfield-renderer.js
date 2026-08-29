/* Morphfield Canvas Renderer
   Connects to GET /api/fields/stream (SSE) and renders the Kuramoto field
   as radial-gradient blobs with coupling edges on a Canvas2D surface. */

(function () {
  'use strict';

  const canvas = document.getElementById('morphfield-canvas');
  if (!canvas) return;
  const ctx = canvas.getContext('2d');

  let fieldState = { fields: [], couplings: [] };
  let selectedFieldId = null;

  // ── Resize ──
  function resize() {
    const rect = canvas.parentElement.getBoundingClientRect();
    canvas.width  = rect.width  * devicePixelRatio;
    canvas.height = rect.height * devicePixelRatio;
    ctx.setTransform(devicePixelRatio, 0, 0, devicePixelRatio, 0, 0);
  }
  resize();
  window.addEventListener('resize', resize);

  // ── SSE connection ──
  function connectSSE() {
    try {
      const es = new EventSource('/api/fields/stream');
      es.onmessage = (e) => {
        try { fieldState = JSON.parse(e.data); } catch (_) {}
      };
      es.onerror = () => {
        es.close();
        setTimeout(connectSSE, 3000);
      };
    } catch (_) {
      setTimeout(connectSSE, 5000);
    }
  }
  connectSSE();

  // ── Click handler ──
  canvas.addEventListener('click', (e) => {
    const rect = canvas.getBoundingClientRect();
    const mx = e.clientX - rect.left;
    const my = e.clientY - rect.top;
    const W = rect.width;
    const H = rect.height;

    for (const f of fieldState.fields) {
      const fx = Math.cos(f.phase) * 0.35 * W + W / 2;
      const fy = Math.sin(f.phase * 1.618) * 0.35 * H + H / 2;
      const r  = 40 + Math.sin(f.phase) * 20;
      const dx = mx - fx;
      const dy = my - fy;
      if (dx * dx + dy * dy < r * r) {
        selectedFieldId = f.id;
        // Attempt to load value_preview into Monaco if available
        if (window.editor && f.value_preview) {
          window.editor.setValue(f.value_preview);
        }
        break;
      }
    }
  });

  // ── Update carrier element ──
  function updateCarrier(f) {
    const el = document.getElementById('soulphya-carrier');
    if (!el) return;
    el.dataset.cosigFreq  = (f.cosig_freq || f.freq).toFixed(2);
    el.dataset.cosigPhase = (f.cosig_phase || f.phase).toFixed(4);
    el.dataset.cosigModal = f.modal || 'void';
  }

  // ── Render loop ──
  function draw() {
    const W = canvas.clientWidth;
    const H = canvas.clientHeight;
    ctx.clearRect(0, 0, W, H);

    // Background
    ctx.fillStyle = '#0a0a0f';
    ctx.fillRect(0, 0, W, H);

    const positions = {};

    // Compute positions
    fieldState.fields.forEach((f) => {
      const x = Math.cos(f.phase) * 0.35 * W + W / 2;
      const y = Math.sin(f.phase * 1.618) * 0.35 * H + H / 2;
      positions[f.id] = { x, y };
    });

    // Draw coupling edges as bezier curves
    fieldState.couplings.forEach((c) => {
      const a = positions[c.a];
      const b = positions[c.b];
      if (!a || !b) return;
      ctx.beginPath();
      const mx = (a.x + b.x) / 2;
      const my = (a.y + b.y) / 2 - 20;
      ctx.moveTo(a.x, a.y);
      ctx.quadraticCurveTo(mx, my, b.x, b.y);
      ctx.strokeStyle = 'rgba(139, 92, 246, ' + Math.min(c.K, 0.5) + ')';
      ctx.lineWidth = 1;
      ctx.stroke();
    });

    // Draw field blobs
    fieldState.fields.forEach((f) => {
      const pos = positions[f.id];
      if (!pos) return;
      const radius = 40 + Math.sin(f.phase) * 20;
      const hue = f.freq % 360;

      const grad = ctx.createRadialGradient(pos.x, pos.y, 0, pos.x, pos.y, radius);
      grad.addColorStop(0, 'hsla(' + hue + ', 70%, 60%, 0.6)');
      grad.addColorStop(1, 'hsla(' + hue + ', 70%, 60%, 0.0)');

      ctx.beginPath();
      ctx.arc(pos.x, pos.y, radius, 0, Math.PI * 2);
      ctx.fillStyle = grad;
      ctx.fill();

      // Highlight selected
      if (f.id === selectedFieldId) {
        ctx.strokeStyle = 'rgba(255,255,255,0.6)';
        ctx.lineWidth = 2;
        ctx.stroke();
        updateCarrier(f);
      }

      // Label
      ctx.fillStyle = 'rgba(255,255,255,0.7)';
      ctx.font = '10px monospace';
      ctx.textAlign = 'center';
      ctx.fillText(f.label || f.id, pos.x, pos.y - radius - 6);
      ctx.fillText((f.cosig_freq || f.freq).toFixed(0) + ' Hz', pos.x, pos.y - radius + 5);
    });

    requestAnimationFrame(draw);
  }
  requestAnimationFrame(draw);
})();
