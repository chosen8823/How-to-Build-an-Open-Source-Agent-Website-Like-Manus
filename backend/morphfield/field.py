"""MorphField — dataclass representing a single oscillator in the Kuramoto field."""

from dataclasses import dataclass, field
from typing import List
import time
import uuid


@dataclass
class MorphField:
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    label: str = ''
    freq: float = 432.0            # natural frequency (Hz)
    phase: float = 0.0             # current phase (radians)
    modal: str = 'text'            # text | audio | visual | spatial | void
    archetype: str = 'sophia'      # sophia | aeon | gate | memory | user
    coupling_K: float = 0.3        # Kuramoto coupling strength
    coupled_to: List[str] = field(default_factory=list)   # field IDs
    last_hydrated: float = field(default_factory=time.time)
    value_preview: str = ''
    cosig_freq: float = 432.0
    cosig_phase: float = 0.0
    kernel_active: bool = False
    unresolved_state: str = '???'
