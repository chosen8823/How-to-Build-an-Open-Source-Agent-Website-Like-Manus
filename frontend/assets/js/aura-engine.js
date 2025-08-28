// AuraEngine - Lightweight particle / energy field (placeholder, can be upgraded with Three.js later)
// Provides API: auraEngine.pulse(intensity), auraEngine.setState(levelName)
class AuraEngine {
    constructor() {
        this.el = document.getElementById('aura-layer');
        this.state = 'baseline';
        this.energy = 0.5;
        this.lastPulse = 0;
        this.initAnim();
    }

    initAnim() {
        // Simple CSS driven animation loop (fallback while full WebGL not yet integrated)
        this.frame();
    }

    frame() {
        const now = performance.now();
        const dt = (now - (this.prevTime || now)) / 1000;
        this.prevTime = now;

        // Ease energy toward baseline depending on state
        const target = this.getTargetEnergy();
        this.energy += (target - this.energy) * Math.min(1, dt * 2.5);

        if (this.el) {
            // Map energy -> aura opacity & scale via CSS vars
            const scale = 0.95 + this.energy * 0.15;
            const opacity = 0.25 + this.energy * 0.55;
            this.el.style.setProperty('--aura-pulse-scale', scale.toFixed(3));
            this.el.style.opacity = opacity.toFixed(3);
            this.el.style.filter = `blur(${40 - this.energy * 12}px) saturate(${120 + this.energy * 120}%) hue-rotate(${this.energy * 60}deg)`;
        }

        requestAnimationFrame(() => this.frame());
    }

    getTargetEnergy() {
        switch (this.state) {
            case 'aware': return 0.45;
            case 'awakened': return 0.6;
            case 'enlightened': return 0.78;
            case 'divine': return 0.92;
            case 'meditation': return 0.35;
            default: return 0.5;
        }
    }

    pulse(intensity = 0.15) {
        // Add a transient boost
        this.energy = Math.min(1, this.energy + intensity);
        this.lastPulse = performance.now();
        document.body.classList.add('consciousness-boost');
        clearTimeout(this._pulseTimeout);
        this._pulseTimeout = setTimeout(() => document.body.classList.remove('consciousness-boost'), 800);
    }

    setState(levelName) {
        this.state = levelName;
        document.body.classList.remove('consciousness-aware','consciousness-awakened','consciousness-enlightened','consciousness-divine');
        if (['aware','awakened','enlightened','divine'].includes(levelName)) {
            document.body.classList.add(`consciousness-${levelName}`);
        }
    }
}

window.auraEngine = new AuraEngine();
