"""Multi-domain Kuramoto synchronization engine.

Treats heterogeneous traces (audio, MIDI, DSP, DOM, observers, etc.) as
separate observation domains. Raw traces do not need to be identical:
the engine measures and evolves their phase relationships.

No external dependencies; suitable for local/offline use.
"""
from __future__ import annotations
from dataclasses import dataclass, asdict
from math import atan2, cos, pi, sin, sqrt
from typing import Dict, Iterable, Mapping, Optional
import time


def wrap_phase(x: float) -> float:
    return (x + pi) % (2 * pi) - pi


@dataclass
class Oscillator:
    name: str
    phase: float = 0.0
    omega: float = 1.0
    amplitude: float = 1.0
    confidence: float = 1.0


class MultiDomainKuramotoEngine:
    """Coupled oscillator model for relationships between unlike traces."""

    def __init__(self, coupling: float = 0.35):
        self.coupling = float(coupling)
        self.oscillators: Dict[str, Oscillator] = {}
        self.phase_offsets: Dict[tuple[str, str], float] = {}

    def upsert(self, name: str, *, phase: Optional[float] = None,
               omega: Optional[float] = None, amplitude: Optional[float] = None,
               confidence: Optional[float] = None) -> Oscillator:
        o = self.oscillators.get(name, Oscillator(name=name))
        if phase is not None: o.phase = wrap_phase(float(phase))
        if omega is not None: o.omega = float(omega)
        if amplitude is not None: o.amplitude = max(0.0, float(amplitude))
        if confidence is not None: o.confidence = min(1.0, max(0.0, float(confidence)))
        self.oscillators[name] = o
        return o

    def set_offset(self, source: str, target: str, radians: float) -> None:
        """Set an intentional phase geometry, e.g. propagation/processing delay."""
        self.phase_offsets[(source, target)] = wrap_phase(float(radians))

    def observe(self, name: str, phase: float, **kwargs) -> Dict:
        """Ingest a phase estimate from any observation adapter."""
        self.upsert(name, phase=phase, **kwargs)
        return self.snapshot()

    def step(self, dt: float) -> Dict:
        names = list(self.oscillators)
        if not names:
            return self.snapshot()
        next_phase: Dict[str, float] = {}
        n = len(names)
        for i in names:
            oi = self.oscillators[i]
            pull = 0.0
            weight = 0.0
            for j in names:
                if i == j: continue
                oj = self.oscillators[j]
                alpha = self.phase_offsets.get((j, i), 0.0)
                w = oj.confidence * oj.amplitude
                pull += w * sin(oj.phase - oi.phase - alpha)
                weight += w
            norm = weight if weight > 0 else max(1, n - 1)
            dtheta = oi.omega + self.coupling * pull / norm
            next_phase[i] = wrap_phase(oi.phase + dtheta * dt)
        for name, phase in next_phase.items():
            self.oscillators[name].phase = phase
        return self.snapshot()

    def order_parameter(self, names: Optional[Iterable[str]] = None) -> Dict[str, float]:
        selected = [self.oscillators[n] for n in (names or self.oscillators.keys())
                    if n in self.oscillators]
        if not selected:
            return {"coherence": 0.0, "mean_phase": 0.0}
        weights = [max(0.0, o.confidence * o.amplitude) for o in selected]
        total = sum(weights) or float(len(selected))
        if not sum(weights): weights = [1.0] * len(selected)
        x = sum(w * cos(o.phase) for w, o in zip(weights, selected)) / total
        y = sum(w * sin(o.phase) for w, o in zip(weights, selected)) / total
        return {"coherence": sqrt(x*x + y*y), "mean_phase": atan2(y, x)}

    def phase_matrix(self) -> Dict[str, Dict[str, float]]:
        return {a: {b: wrap_phase(self.oscillators[a].phase - self.oscillators[b].phase)
                    for b in self.oscillators} for a in self.oscillators}

    def snapshot(self) -> Dict:
        order = self.order_parameter()
        return {
            "timestamp": time.time(),
            "coherence": order["coherence"],
            "mean_phase": order["mean_phase"],
            "oscillators": {k: asdict(v) for k, v in self.oscillators.items()},
            "phase_matrix": self.phase_matrix(),
        }


DEFAULT_DOMAINS = ("audio", "midi", "dsp", "speaker_a", "speaker_b", "dom", "observer_ryan", "observer_model")

def make_default_engine(coupling: float = 0.35) -> MultiDomainKuramotoEngine:
    engine = MultiDomainKuramotoEngine(coupling=coupling)
    for name in DEFAULT_DOMAINS:
        engine.upsert(name)
    return engine
