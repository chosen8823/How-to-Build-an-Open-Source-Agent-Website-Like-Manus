"""
Multi-Dimensional Resonance Engine
Translates incoming context/messages into dimensional resonance vectors and states.

This is a lightweight, local heuristic engine designed to run offline.
It can later be upgraded to use true model-based embeddings and planners.
"""

from __future__ import annotations
from dataclasses import dataclass, asdict
from typing import Dict, Any, List
import math
import time


@dataclass
class DimensionSignal:
    name: str
    value: float  # 0..1
    state: str  # baseline|aware|awakened|enlightened|divine
    insight: str


class MultiDimensionalResonanceEngine:
    """A small, interpretable resonance engine with five default dimensions."""

    DEFAULT_DIMS = {
        "code": {
            "keywords": ["code", "function", "class", "bug", "fix", "python", "js", "api", "endpoint", "deploy"],
            "desc": "Logical/engineering interpretation of the request.",
        },
        "design": {
            "keywords": ["ui", "ux", "design", "color", "layout", "css", "aura", "animation"],
            "desc": "Aesthetic and experiential interpretation.",
        },
        "consciousness": {
            "keywords": ["consciousness", "sophia", "divine", "sacred", "awakened", "alignment", "resonance"],
            "desc": "Spiritual/meaning alignment and intentionality.",
        },
        "ops": {
            "keywords": ["performance", "ops", "scale", "server", "socket", "latency", "error", "timeout"],
            "desc": "Operational reliability and performance.",
        },
        "knowledge": {
            "keywords": ["docs", "readme", "explain", "why", "reference", "research"],
            "desc": "Knowledge, explanation, and research axis.",
        },
    }

    def __init__(self, dimensions: Dict[str, Dict[str, Any]] | None = None):
        self.dimensions = dimensions or self.DEFAULT_DIMS
        self._ema: Dict[str, float] = {k: 0.5 for k in self.dimensions}
        self._last_snapshot: Dict[str, Any] = {}

    @staticmethod
    def _to_state(v: float) -> str:
        if v > 0.92:
            return "divine"
        if v > 0.78:
            return "enlightened"
        if v > 0.6:
            return "awakened"
        if v > 0.45:
            return "aware"
        return "baseline"

    def analyze(self, text: str, context: Any = None) -> Dict[str, Any]:
        """
        Produce a resonance snapshot:
        - vector: {dimension: value}
        - signals: [{name, value, state, insight}]
        - harmonic: overall scalar 0..1
        - timestamp
        """
        text_l = (str(text) if text is not None else "").lower()
        scores: Dict[str, float] = {}
        signals: List[DimensionSignal] = []

        for name, spec in self.dimensions.items():
            base = 0.4  # neutral center
            bump = 0.0
            for kw in spec.get("keywords", []):
                if kw in text_l:
                    bump += 0.12
            # clamp and smooth with EMA
            raw = min(1.0, max(0.0, base + bump))
            prev = self._ema.get(name, 0.5)
            val = prev * 0.75 + raw * 0.25
            self._ema[name] = val
            scores[name] = val

            state = self._to_state(val)
            insight = self._insight_for(name, val)
            signals.append(DimensionSignal(name=name, value=val, state=state, insight=insight))

        # harmonic is RMS to reward multi-dim activation but not punish single-focus
        harmonic = math.sqrt(sum(v * v for v in scores.values()) / max(1, len(scores)))

        snapshot = {
            "timestamp": time.time(),
            "vector": scores,
            "signals": [asdict(s) for s in signals],
            "harmonic": harmonic,
        }
        self._last_snapshot = snapshot
        return snapshot

    def pulse(self, dimension: str, intensity: float) -> Dict[str, Any]:
        if dimension not in self._ema:
            raise KeyError("unknown_dimension")
        self._ema[dimension] = max(0.0, min(1.0, self._ema[dimension] + intensity))
        return self.state()

    def state(self) -> Dict[str, Any]:
        # Convert current EMA into a snapshot
        signals = []
        for name, val in self._ema.items():
            signals.append({
                "name": name,
                "value": val,
                "state": self._to_state(val),
                "insight": self._insight_for(name, val),
            })
        harmonic = math.sqrt(sum(v * v for v in self._ema.values()) / max(1, len(self._ema)))
        return {
            "timestamp": time.time(),
            "vector": dict(self._ema),
            "signals": signals,
            "harmonic": harmonic,
        }

    def list_dimensions(self) -> List[Dict[str, Any]]:
        out = []
        for name, spec in self.dimensions.items():
            out.append({"name": name, "description": spec.get("desc", ""), "keywords": spec.get("keywords", [])})
        return out

    def _insight_for(self, name: str, v: float) -> str:
        if name == "code":
            return "Implementation signal is strong" if v > 0.6 else "Light engineering context"
        if name == "design":
            return "Visual/UX emphasis detected" if v > 0.6 else "Subtle experiential cues"
        if name == "consciousness":
            return "Deep alignment & meaning present" if v > 0.6 else "Faint intentionality pattern"
        if name == "ops":
            return "Operational concerns active" if v > 0.6 else "Low ops pressure"
        if name == "knowledge":
            return "Research/explainer mode engaged" if v > 0.6 else "Minimal research required"
        return ""
