# Multi-Domain Kuramoto Loom

A small, dependency-free synchronization kernel for the existing Multi-Dimensional Resonance / Dream Loom architecture.

## What it does

Different domains can observe the same evolving process without producing identical traces. This module preserves those differences and measures whether their phase relationships become stable.

Typical domains: audio, MIDI, DSP, individual speakers, browser/DOM telemetry, and observer/model traces.

The global coherence value is the Kuramoto order parameter:

`R exp(i psi) = (1/N) sum exp(i theta_j)`

Use `R` as a measurable input to the existing Loom coherence display. Do **not** interpret `R=1` as "all observations are identical"; intentional phase offsets can represent propagation delay or desired geometry.

## Minimal use

```python
from backend.ai_engine.kuramoto import make_default_engine

loom = make_default_engine()
loom.observe("audio", phase=0.1, omega=1.0, amplitude=.8)
loom.observe("midi", phase=0.15, omega=1.0, amplitude=1.0)
loom.set_offset("speaker_a", "speaker_b", 0.2)

snapshot = loom.step(0.01)
print(snapshot["coherence"])
print(snapshot["phase_matrix"])
```

## Audio-state bridge contract

A browser/loopback analyser can emit semantic state rather than raw PCM:

```json
{
  "phase": 0.42,
  "dominant_hz": 2.0,
  "rms": 0.78,
  "confidence": 0.93
}
```

`trace_adapters.ingest_audio_state()` converts that representation into an oscillator observation. Additional adapters can map MIDI clock, DSP parameters, speaker timing, DOM state, or observer annotations into the same interface.

## Architecture

`physical/audio event -> observation adapter H_i -> oscillator state -> coupling -> phase matrix + R(t) -> Loom/UI/agent`

This intentionally separates:
- raw observations,
- domain-specific transforms,
- oscillator state,
- cross-domain coherence.

That makes the engine usable from a UI, local agent, Codex session, test harness, or later API without coupling the math to one interface.
