class SpatialAudioLayer {
    constructor() {
        this.ctx = null;
        this.listener = null;
        this.oscillators = new Map();  // field_id -> OscillatorNode
        this.panners = new Map();      // field_id -> PannerNode
        this.active = false;
    }

    async init() {
        this.ctx = new (window.AudioContext || window.webkitAudioContext)();
        this.listener = this.ctx.listener;
        this.active = true;
    }

    updateFromSomaticPulse(pulse) {
        if (!this.active || !this.ctx) return;
        
        const freq = pulse.audio_freq || 432;
        const pan = pulse.audio_pan || 0;
        const intensity = pulse.haptic_intensity || 0.5;
        
        // Update or create oscillator for this pulse
        if (!this.oscillators.has('main')) {
            const osc = this.ctx.createOscillator();
            const panner = this.ctx.createPanner();
            const gain = this.ctx.createGain();
            
            osc.type = 'sine';
            osc.frequency.value = freq;
            panner.panningModel = 'HRTF';
            panner.positionX.value = pan;
            gain.gain.value = 0.05;  // subtle ambient tone
            
            osc.connect(panner);
            panner.connect(gain);
            gain.connect(this.ctx.destination);
            osc.start();
            
            this.oscillators.set('main', osc);
            this.panners.set('main', panner);
        } else {
            const osc = this.oscillators.get('main');
            const panner = this.panners.get('main');
            osc.frequency.setTargetAtTime(freq, this.ctx.currentTime, 0.1);
            panner.positionX.setTargetAtTime(pan, this.ctx.currentTime, 0.05);
        }
    }

    // Spatial audio gradient: semantic attractors have positions in 3D space
    positionAttractor(id, x, y, z, freq) {
        if (!this.active || !this.ctx) return;
        if (!this.oscillators.has(id)) {
            const osc = this.ctx.createOscillator();
            const panner = this.ctx.createPanner();
            const gain = this.ctx.createGain();
            osc.type = 'sine';
            osc.frequency.value = freq;
            panner.panningModel = 'HRTF';
            panner.positionX.value = x;
            panner.positionY.value = y;
            panner.positionZ.value = z;
            gain.gain.value = 0.02;
            osc.connect(panner); panner.connect(gain); gain.connect(this.ctx.destination);
            osc.start();
            this.oscillators.set(id, osc);
            this.panners.set(id, panner);
        }
    }
}

window.spatialAudio = new SpatialAudioLayer();
