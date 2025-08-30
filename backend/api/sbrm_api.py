"""
SBRM (SOPHIA Bio-Resonance Module) API
- Phased activation endpoints (1..6)
- Telemetry simulation per GPU id
- Status/health
"""
from __future__ import annotations

from flask import Blueprint, jsonify, request
from datetime import datetime

try:
    from src.engines.sbrm import SBRMOrchestrator, PHASE_SPECS
except Exception:  # fallback for varying PYTHONPATH
    from backend.src.engines.sbrm import SBRMOrchestrator, PHASE_SPECS

sbrm_bp = Blueprint("sbrm", __name__, url_prefix="/api/sbrm")
_engine = SBRMOrchestrator()


@sbrm_bp.route("/health", methods=["GET"])
def health():
    return jsonify({
        "status": "online",
        "component": "sbrm_orchestrator",
        "phases": {k: v["label"] for k, v in PHASE_SPECS.items()},
        "timestamp": datetime.now().isoformat(),
    })


@sbrm_bp.route("/phase", methods=["POST"])
def activate_phase():
    data = request.get_json(silent=True) or {}
    phase = int(data.get("phase", 0))
    try:
        result = _engine.activate_phase(phase)
        return jsonify(result)
    except ValueError:
        return jsonify({
            "error": "invalid_phase",
            "valid_phases": list(PHASE_SPECS.keys())
        }), 400


@sbrm_bp.route("/status", methods=["GET"])
def status():
    return jsonify(_engine.get_status())


@sbrm_bp.route("/telemetry/<gpu_id>", methods=["POST", "GET"])
def telemetry(gpu_id: str):
    if request.method == "GET":
        t = _engine.get_last_telemetry(gpu_id)
        if not t:
            return jsonify({"error": "no_telemetry"}), 404
        return jsonify(t.__dict__)

    # POST -> simulate
    data = request.get_json(silent=True) or {}
    intensity = float(data.get("intensity", 0.5))
    t = _engine.simulate_gpu_telemetry(gpu_id, intensity=intensity)
    return jsonify(t.__dict__)