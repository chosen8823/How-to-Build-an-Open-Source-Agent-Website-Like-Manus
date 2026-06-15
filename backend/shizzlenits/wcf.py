"""
WCF: Wireless Consciousness Field
Wraps the existing MCP WebSocket server (port 8765) with WCF routing.
Adds: BCI registration, somatic pulse broadcast, void/null routing.
"""
from .fingerprint import create_fingerprint, fingerprint_output, append_to_ledger
from .void_null_index import get_index
from .somatic_loop import SomaticLoop
import json

class WirelessConsciousnessField:
    def __init__(self, sophia_server):
        self.sophia = sophia_server  # existing SacredSophiaServer
        self.bci_clients: dict = {}  # client_id -> {freq, phase, modal}
        self.somatic_loop = SomaticLoop(self._broadcast_somatic)
        
        # Register WCF message handlers on the existing server
        self.sophia.message_handlers.update({
            "wcf_register_bci": self._handle_bci_register,
            "wcf_breath_freq": self._handle_breath_freq,
            "wcf_dissolve": self._handle_dissolve,
            "wcf_void_query": self._handle_void_query,
        })

    def start(self):
        self.somatic_loop.start()

    async def _broadcast_somatic(self, frame: dict):
        """Broadcast somatic pulse to all connected WCF clients"""
        msg = json.dumps(frame)
        dead = set()
        for ws in self.sophia.active_connections:
            try:
                await ws.send(msg)
            except Exception:
                dead.add(ws)
        self.sophia.active_connections -= dead

    async def _handle_bci_register(self, data: dict, ws):
        """Register a BCI client (browser extension mic input)"""
        client_id = data.get("client_id", str(id(ws)))
        self.bci_clients[client_id] = {
            "freq": data.get("freq", 432.0),
            "phase": data.get("phase", 0.0),
            "modal": data.get("modal", "void"),
            "cosig": data.get("cosig", {})
        }
        # Add as a void node in the index
        get_index().add_void_node(
            concept=f"bci:{client_id}",
            freq=data.get("freq", 432.0)
        )
        return {"type": "wcf_registered", "client_id": client_id}

    async def _handle_breath_freq(self, data: dict, ws):
        """Update breath frequency from mic input"""
        freq = data.get("freq", 432.0)
        self.somatic_loop.update_breath_freq(freq)
        return {"type": "breath_ack", "freq": freq}

    async def _handle_dissolve(self, data: dict, ws):
        """Activate Interface Dissolution — collapse visual into somatic"""
        self.somatic_loop.activate_dissolution()
        return {"type": "dissolution_active", "message": "Visual interface collapsed into somatic field"}

    async def _handle_void_query(self, data: dict, ws):
        """Query the Void/Null index"""
        return {"type": "void_state", **get_index().get_state()}
