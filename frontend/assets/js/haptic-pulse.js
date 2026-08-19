class HapticPulseLayer {
    constructor() {
        this.supported = 'vibrate' in navigator;
        this.active = false;
        this.lastPulse = 0;
        this.minInterval = 100;  // ms between pulses
    }

    activate() { this.active = true; }
    deactivate() { this.active = false; }

    pulse(intensity) {
        if (!this.active || !this.supported) return;
        const now = Date.now();
        if (now - this.lastPulse < this.minInterval) return;
        this.lastPulse = now;
        
        // intensity 0.0-1.0 -> vibration duration 10-200ms
        const duration = Math.round(10 + intensity * 190);
        navigator.vibrate(duration);
    }

    // Somatic pulse pattern: breath rhythm
    breathPattern(freq_hz) {
        if (!this.active || !this.supported) return;
        const period_ms = Math.round(1000 / freq_hz);
        // Inhale pulse, pause, exhale pulse
        navigator.vibrate([period_ms * 0.4, period_ms * 0.2, period_ms * 0.4]);
    }

    // Strong movement: sudden phase jump (lightning from atmosphere plan)
    lightning() {
        if (!this.supported) return;
        navigator.vibrate([50, 30, 50, 30, 200]);
    }
}

window.hapticPulse = new HapticPulseLayer();
