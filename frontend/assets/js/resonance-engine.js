// ResonanceEngine Frontend Companion
// Consumes backend multi-dimensional resonance snapshots and animates layered interpretations.

class FrontendResonanceEngine {
    constructor() {
        this.lastSnapshot = null;
        this.dimLayers = new Map();
        this.container = this._ensureContainer();
        this.pollInterval = 0; // optional periodic polling
    }

    _ensureContainer() {
        let el = document.getElementById('resonance-layers');
        if (!el) {
            el = document.createElement('div');
            el.id = 'resonance-layers';
            el.style.position = 'absolute';
            el.style.inset = '0';
            el.style.pointerEvents = 'none';
            el.style.zIndex = '3';
            document.body.appendChild(el);
        }
        return el;
    }

    updateFromSnapshot(snapshot) {
        this.lastSnapshot = snapshot;
        if (!snapshot || !snapshot.signals) return;

        snapshot.signals.forEach(sig => {
            const id = `res-layer-${sig.name}`;
            let layer = this.dimLayers.get(sig.name);
            if (!layer) {
                layer = document.createElement('div');
                layer.className = 'resonance-layer';
                layer.dataset.dimension = sig.name;
                layer.style.position = 'absolute';
                layer.style.left = '0';
                layer.style.top = '0';
                layer.style.right = '0';
                layer.style.bottom = '0';
                layer.style.mixBlendMode = 'overlay';
                layer.style.opacity = '0';
                layer.style.transition = 'opacity 0.6s ease, filter 0.8s ease';
                this.container.appendChild(layer);
                this.dimLayers.set(sig.name, layer);
            }
            const hueBase = this._hueFor(sig.name);
            const sat = Math.round(40 + sig.value * 50);
            const light = Math.round(30 + sig.value * 25);
            layer.style.background = `radial-gradient(circle at ${50 + sig.value*20}% ${50 - sig.value*15}%, hsla(${hueBase}, ${sat}%, ${light}%, ${0.25 + sig.value*0.25}), transparent 70%)`;
            layer.style.opacity = (sig.value * 0.85).toFixed(3);
            layer.style.filter = `blur(${40 - sig.value*25}px) saturate(${100 + sig.value*120}%)`;
            layer.title = `${sig.name}: ${(sig.value*100).toFixed(1)}% (${sig.state})\n${sig.insight}`;
        });

        if (window.auraEngine && snapshot.vector) {
            // Influence aura energy slightly toward harmonic value.
            const harmonic = snapshot.harmonic || 0.5;
            const delta = (harmonic - window.auraEngine.energy) * 0.15;
            window.auraEngine.energy = Math.min(1, Math.max(0, window.auraEngine.energy + delta));
        }
    }

    _hueFor(name) {
        switch (name) {
            case 'code': return 200; // blue
            case 'design': return 300; // purple
            case 'consciousness': return 45; // golden
            case 'ops': return 10; // orange/red
            case 'knowledge': return 95; // green
            default: return 180;
        }
    }
}

window.resonanceEngine = new FrontendResonanceEngine();
