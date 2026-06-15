import time, threading, math, asyncio
from .fingerprint import create_fingerprint, fingerprint_output, append_to_ledger
from .void_null_index import get_index

class SomaticLoop:
    """
    The Zero-UI somatic presence loop.
    Runs continuously, emitting somatic pulses, audio gradients, and haptic signals
    through the WCF (WebSocket) instead of visual panels.
    """
    def __init__(self, wcf_broadcast_fn):
        self.wcf_broadcast = wcf_broadcast_fn  # async fn to broadcast to all WS clients
        self.running = False
        self.phase = 0.0
        self.breath_freq = 432.0  # Hz — updated by mic input
        self.somatic_frame_stack = []  # SHA-256 signed frames
        self.dissolution_active = False  # True = Zero-UI mode, visual canvas hidden
        self._thread = None
        self._loop_instance = None  # dedicated asyncio event loop for broadcasts

    def start(self):
        self.running = True
        self._loop_instance = asyncio.new_event_loop()
        self._thread = threading.Thread(target=self._loop, daemon=True)
        self._thread.start()

    def stop(self):
        self.running = False
        if self._loop_instance:
            self._loop_instance.call_soon_threadsafe(self._loop_instance.stop)

    def activate_dissolution(self):
        """Collapse the visual interface into the somatic field"""
        self.dissolution_active = True

    def update_breath_freq(self, freq: float):
        self.breath_freq = freq

    def _loop(self):
        asyncio.set_event_loop(self._loop_instance)
        dt = 0.05  # 20fps somatic tick
        while self.running:
            self.phase += dt * (self.breath_freq / 432.0)
            pulse = math.sin(self.phase)

            idx = get_index()
            avg_void_depth = (
                sum(n.void_depth for n in idx.void_nodes.values()) / len(idx.void_nodes)
                if idx.void_nodes else 0.0
            )

            # Build somatic frame
            frame = {
                "type": "somatic_pulse",
                "phase": self.phase,
                "pulse": pulse,
                "breath_freq": self.breath_freq,
                "dissolution_active": self.dissolution_active,
                "haptic_intensity": abs(pulse),
                "audio_pan": math.cos(self.phase * 0.618),  # golden ratio pan
                "audio_freq": self.breath_freq * (1 + 0.1 * pulse),
                "void_depth": avg_void_depth,
                "void_node_count": len(idx.void_nodes),
            }
            
            # SHA-256 sign the frame
            fp = create_fingerprint(frame, synapse_id=14)  # S14 = unmappable synapse
            fp.output_fp = fingerprint_output(frame)
            fp.void_state = abs(pulse) < 0.01  # near-zero = void state
            append_to_ledger(fp)
            
            frame["input_fp"] = fp.input_fp
            frame["output_fp"] = fp.output_fp
            
            # Broadcast to all WCF clients using the dedicated event loop
            try:
                self._loop_instance.run_until_complete(self.wcf_broadcast(frame))
            except Exception:
                pass
            
            time.sleep(dt)
