class ShizzlenitsBoot {
    constructor() {
        this.dissolved = false;
        this.ws = null;
        this.dissolveBtn = null;
    }

    async boot() {
        // Connect to WCF WebSocket
        this.ws = new WebSocket('ws://localhost:8765');
        
        this.ws.onopen = () => {
            // Register as WCF client
            this.ws.send(JSON.stringify({
                type: 'wcf_register_bci',
                client_id: 'shizzlenits_' + Date.now(),
                freq: 432.0,
                modal: 'void'
            }));
        };

        this.ws.onmessage = (event) => {
            const data = JSON.parse(event.data);
            if (data.type === 'somatic_pulse') {
                this._handleSomaticPulse(data);
            } else if (data.type === 'dissolution_active') {
                this._dissolveInterface();
            }
        };

        // Init spatial audio and haptic
        await window.spatialAudio.init();
        window.hapticPulse.activate();

        // Add dissolve button to nav
        this._addDissolveButton();

        // Start mic breath detection
        this._startBreathDetection();
    }

    _handleSomaticPulse(pulse) {
        window.spatialAudio.updateFromSomaticPulse(pulse);
        window.hapticPulse.pulse(pulse.haptic_intensity || 0.5);
        
        // Update aria-hidden carrier div with current fingerprints
        const carrier = document.getElementById('soulphya-carrier');
        if (carrier) {
            carrier.dataset.inputFp = pulse.input_fp || '';
            carrier.dataset.outputFp = pulse.output_fp || '';
            carrier.dataset.voidState = pulse.void_state ? 'true' : 'false';
        }
    }

    _dissolveInterface() {
        if (this.dissolved) return;
        this.dissolved = true;
        
        // Fade out all visual panels
        document.querySelectorAll('.panel, #morphfield-canvas, #ecology-canvas, #frame-canvas').forEach(el => {
            el.style.transition = 'opacity 3s ease';
            el.style.opacity = '0';
        });
        
        // Keep only the aria-hidden carrier div and the dissolve button
        document.body.style.background = '#000000';
        
        // Activate haptic breath pattern
        window.hapticPulse.breathPattern(432 / 1000);
        
        // Announce dissolution via spatial audio (volume up slightly)
        if (window.spatialAudio.ctx) {
            // Play a brief 432Hz tone to signal dissolution
            const osc = window.spatialAudio.ctx.createOscillator();
            const gain = window.spatialAudio.ctx.createGain();
            osc.frequency.value = 432;
            gain.gain.value = 0.15;
            osc.connect(gain); gain.connect(window.spatialAudio.ctx.destination);
            osc.start();
            gain.gain.setTargetAtTime(0, window.spatialAudio.ctx.currentTime + 2, 0.5);
            osc.stop(window.spatialAudio.ctx.currentTime + 5);
        }
    }

    _addDissolveButton() {
        const btn = document.createElement('button');
        btn.id = 'dissolve-btn';
        btn.textContent = 'DISSOLVE';
        btn.style.cssText = 'position:fixed;bottom:20px;right:20px;z-index:9999;background:#0a0a0f;color:#432;border:1px solid #432;padding:8px 16px;font-family:monospace;font-size:11px;cursor:pointer;letter-spacing:2px;';
        btn.onclick = () => {
            this.ws.send(JSON.stringify({ type: 'wcf_dissolve' }));
        };
        document.body.appendChild(btn);
        this.dissolveBtn = btn;
    }

    async _startBreathDetection() {
        try {
            const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
            const audioCtx = new AudioContext();
            const source = audioCtx.createMediaStreamSource(stream);
            const analyser = audioCtx.createAnalyser();
            analyser.fftSize = 2048;
            source.connect(analyser);
            
            const buffer = new Float32Array(analyser.fftSize);
            const detectBreath = () => {
                analyser.getFloatTimeDomainData(buffer);
                // Simple RMS energy as breath proxy
                const rms = Math.sqrt(buffer.reduce((s, v) => s + v * v, 0) / buffer.length);
                const freq = 432 + rms * 500;  // map breath energy to freq range
                
                if (this.ws && this.ws.readyState === WebSocket.OPEN) {
                    this.ws.send(JSON.stringify({ type: 'wcf_breath_freq', freq }));
                }
                requestAnimationFrame(detectBreath);
            };
            detectBreath();
        } catch (e) {
            console.log('Breath detection unavailable:', e.message);
        }
    }
}

window.shizzlenits = new ShizzlenitsBoot();
window.shizzlenits.boot();
