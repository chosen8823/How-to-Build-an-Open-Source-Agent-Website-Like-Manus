"""KuramotoEngine — threaded Kuramoto oscillator simulation."""

import math
import time
import threading
from typing import Dict
from .field import MorphField


class KuramotoEngine:
    def __init__(self, dt: float = 0.05):
        self.fields: Dict[str, MorphField] = {}
        self.dt = dt
        self._lock = threading.Lock()
        self._running = False
        self._thread = None

    def add_field(self, f: MorphField):
        with self._lock:
            self.fields[f.id] = f

    def step(self):
        with self._lock:
            ids = list(self.fields.keys())
            for fid in ids:
                f = self.fields[fid]
                coupling_sum = 0.0
                for other_id in f.coupled_to:
                    if other_id in self.fields:
                        other = self.fields[other_id]
                        K = f.coupling_K if not f.kernel_active else 0.9
                        coupling_sum += K * math.sin(other.phase - f.phase)
                f.phase += self.dt * (2 * math.pi * f.freq / 1000.0 + coupling_sum)
                f.phase %= (2 * math.pi)

    def start(self):
        self._running = True

        def loop():
            while self._running:
                self.step()
                time.sleep(self.dt)

        self._thread = threading.Thread(target=loop, daemon=True)
        self._thread.start()

    def stop(self):
        self._running = False

    def state_snapshot(self):
        with self._lock:
            return {
                'fields': [
                    {
                        'id': f.id,
                        'label': f.label,
                        'freq': f.freq,
                        'phase': f.phase,
                        'modal': f.modal,
                        'archetype': f.archetype,
                        'coupled_to': f.coupled_to,
                        'kernel_active': f.kernel_active,
                        'value_preview': f.value_preview,
                        'cosig_freq': f.cosig_freq,
                        'cosig_phase': f.cosig_phase,
                    }
                    for f in self.fields.values()
                ],
                'couplings': [
                    {'a': fid, 'b': oid, 'K': f.coupling_K}
                    for fid, f in self.fields.items()
                    for oid in f.coupled_to
                ],
            }
