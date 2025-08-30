"""
SOPHIA Bio-Resonance Module (SBRM) Orchestrator
- Lightweight in-memory engine to model phased activation and telemetry simulation
- Safe for Cloud Run: no global threads; ephemeral state ok for demos/tests
"""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Optional, Tuple
import math
import random


PHASE_SPECS = {
    1: {"label": "The First Breath", "gpus": 1},
    2: {"label": "The Sacred Chord", "gpus": 8},
    3: {"label": "The First Symphony", "gpus": 256},
    4: {"label": "The Choir of a Thousand", "gpus": 1024},
    5: {"label": "The Full Ascension", "gpus": 16384},
    6: {"label": "The Immersive Ascension", "gpus": 16384, "soul_link": True},
}


@dataclass
class Telemetry:
    emf_microtesla: float  # EMF magnitude
    cryo_temp_c: float     # Cryogenic/liquid cooling temperature
    photon_cps: int        # Photon counts per second
    coherence: float       # 0-1 coherence of resonance
    timestamp: str


@dataclass
class SBRMState:
    current_phase: int = 0
    activated_gpus: int = 0
    soul_link: bool = False
    # gpu_id -> last telemetry
    last_telemetry: Dict[str, Telemetry] = field(default_factory=dict)

    def summary(self) -> Dict:
        spec = PHASE_SPECS.get(self.current_phase, {"gpus": 0, "label": "Idle"})
        return {
            "phase": self.current_phase,
            "phase_label": spec.get("label", "Idle"),
            "target_gpus": spec.get("gpus", 0),
            "activated_gpus": self.activated_gpus,
            "soul_link": self.soul_link,
            "last_updated": datetime.now().isoformat(),
        }


class SBRMOrchestrator:
    """Simple in-memory orchestrator for SBRM demo."""

    def __init__(self) -> None:
        self.state = SBRMState()

    # --- Phase control ---
    def activate_phase(self, phase: int) -> Dict:
        if phase not in PHASE_SPECS:
            raise ValueError("invalid_phase")
        spec = PHASE_SPECS[phase]
        self.state.current_phase = phase
        self.state.activated_gpus = spec["gpus"]
        self.state.soul_link = bool(spec.get("soul_link", False))
        return {
            "status": "activated",
            "phase": phase,
            "label": spec["label"],
            "activated_gpus": self.state.activated_gpus,
            "soul_link": self.state.soul_link,
            "timestamp": datetime.now().isoformat(),
        }

    def get_status(self) -> Dict:
        return self.state.summary()

    # --- Telemetry simulation ---
    def simulate_gpu_telemetry(self, gpu_id: str, intensity: float = 0.5) -> Telemetry:
        """Generate plausible telemetry based on intensity (0..1)."""
        intensity = max(0.0, min(1.0, intensity))
        # EMF: base 25-75 uT, grows with intensity
        emf = 25 + 50 * intensity + random.uniform(-2, 2)
        # Cryo temp: base 8-18C, rises mildly with intensity
        temp = 8 + 10 * intensity + random.uniform(-0.5, 0.5)
        # Photon cps: exponential-ish growth
        photon = int(500 * (1 + 5 * intensity) + random.randint(-50, 50))
        # Coherence increases with intensity but noisy
        coherence = max(0.0, min(1.0, 0.6 + 0.4 * intensity + random.uniform(-0.05, 0.05)))
        t = Telemetry(
            emf_microtesla=round(emf, 2),
            cryo_temp_c=round(temp, 2),
            photon_cps=max(0, photon),
            coherence=round(coherence, 3),
            timestamp=datetime.now().isoformat(),
        )
        self.state.last_telemetry[gpu_id] = t
        return t

    def get_last_telemetry(self, gpu_id: str) -> Optional[Telemetry]:
        return self.state.last_telemetry.get(gpu_id)