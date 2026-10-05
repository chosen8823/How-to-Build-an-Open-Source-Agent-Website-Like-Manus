"""Adapter helpers for converting trace features into oscillator observations."""
from __future__ import annotations
from math import pi
from typing import Mapping
from .kuramoto import MultiDomainKuramotoEngine


def normalized_cycle_to_phase(position: float) -> float:
    """Map cycle position [0,1) to radians."""
    return (float(position) % 1.0) * 2.0 * pi - pi


def ingest_audio_state(engine: MultiDomainKuramotoEngine, state: Mapping) -> dict:
    """Accept semantic audio-state/DOM telemetry.

    Expected optional fields:
      phase: radians
      cycle_position: normalized [0,1)
      dominant_hz: oscillator natural frequency
      rms: amplitude proxy
      confidence: estimator confidence
    """
    phase = state.get("phase")
    if phase is None and "cycle_position" in state:
        phase = normalized_cycle_to_phase(state["cycle_position"])
    if phase is None:
        raise ValueError("audio state needs phase or cycle_position")
    return engine.observe(
        "audio", phase,
        omega=state.get("dominant_hz"),
        amplitude=state.get("rms"),
        confidence=state.get("confidence"),
    )


def ingest_domain(engine: MultiDomainKuramotoEngine, name: str, state: Mapping) -> dict:
    phase = state.get("phase")
    if phase is None and "cycle_position" in state:
        phase = normalized_cycle_to_phase(state["cycle_position"])
    if phase is None:
        raise ValueError(f"{name} state needs phase or cycle_position")
    return engine.observe(name, phase,
                          omega=state.get("omega"),
                          amplitude=state.get("amplitude"),
                          confidence=state.get("confidence"))
