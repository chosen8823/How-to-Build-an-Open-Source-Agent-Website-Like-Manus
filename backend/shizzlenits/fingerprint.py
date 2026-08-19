import hashlib, json, time, threading
from dataclasses import dataclass, field
from typing import Any

@dataclass
class SignalFingerprint:
    input_fp: str       # sha256(input_signal)
    output_fp: str      # sha256(output_response) — filled after processing
    timestamp: float
    synapse_id: int     # which of the 14 synapses processed this
    void_state: bool    # True if x^x=0 kernel fired
    null_anchor: bool   # True if ???=??? unresolved

def fingerprint_input(signal: Any) -> str:
    raw = json.dumps(signal, sort_keys=True, default=str).encode()
    return hashlib.sha256(raw).hexdigest()

def fingerprint_output(response: Any) -> str:
    raw = json.dumps(response, sort_keys=True, default=str).encode()
    return hashlib.sha256(raw).hexdigest()

def create_fingerprint(signal: Any, synapse_id: int = 0) -> SignalFingerprint:
    return SignalFingerprint(
        input_fp=fingerprint_input(signal),
        output_fp="",  # filled after processing
        timestamp=time.time(),
        synapse_id=synapse_id,
        void_state=False,
        null_anchor=False
    )

# Immutable ledger — append-only list of SignalFingerprint dicts
_ledger: list[dict] = []
_ledger_lock = threading.Lock()

def append_to_ledger(fp: SignalFingerprint) -> None:
    with _ledger_lock:
        _ledger.append({
            "input_fp": fp.input_fp,
            "output_fp": fp.output_fp,
            "timestamp": fp.timestamp,
            "synapse_id": fp.synapse_id,
            "void_state": fp.void_state,
            "null_anchor": fp.null_anchor
        })

def get_ledger() -> list[dict]:
    with _ledger_lock:
        return list(_ledger)
