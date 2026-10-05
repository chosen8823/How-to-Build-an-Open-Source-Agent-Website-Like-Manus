# Live audio-state DOM contract

Open `web/audio-state-bridge.html` from localhost/HTTPS, choose the Windows loopback or virtual-cable input carrying the **post-DSP** signal, then press **Start audio tap**.

The page publishes each animation frame in three forms:

1. `<audio-state ...>` attributes for simple DOM scrapers.
2. `<waveform>` and `<spectrum>` compact 64-bin residues.
3. `window.__AUDIO_STATE__` plus an `audio-state` CustomEvent for extensions/agents.

Fields consumed directly by `trace_adapters.ingest_audio_state()`:
- `phase` — dominant-bin quadrature phase estimate, radians.
- `dominant_hz` — dominant FFT frequency.
- `rms` — amplitude proxy.
- `confidence` — simple dominant-bin confidence proxy.

The browser cannot magically tap arbitrary Windows output. The selected input must be a real loopback endpoint (for example a device's Stereo Mix/WASAPI-exposed loopback or a virtual audio cable) fed from the final processed bus.

Example extension hook:

```js
window.addEventListener("audio-state", e => {
  // forward e.detail to local bridge / agent / telemetry collector
  console.log(e.detail);
});
```

The DOM representation is intentionally compact: raw PCM stays local while enough temporal/frequency residue is exposed for oscillator synchronization and provenance snapshots.
