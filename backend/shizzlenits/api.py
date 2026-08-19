from flask import Blueprint, jsonify, request
from .fingerprint import get_ledger
from .void_null_index import get_index

shizzlenits_bp = Blueprint('shizzlenits', __name__)

@shizzlenits_bp.route('/api/shizzlenits/ledger')
def get_fingerprint_ledger():
    """Return the immutable SHA-256 fingerprint ledger"""
    return jsonify({"ledger": get_ledger()[-100:]})  # last 100 entries

@shizzlenits_bp.route('/api/shizzlenits/void')
def get_void_state():
    """Return the current Void/Null index state"""
    return jsonify(get_index().get_state())

@shizzlenits_bp.route('/api/shizzlenits/void/inject', methods=['POST'])
def inject_void_node():
    """Inject a new concept into the Void"""
    data = request.json
    node = get_index().add_void_node(
        concept=data.get("concept", ""),
        freq=data.get("freq", 432.0)
    )
    return jsonify({"node_id": node.id, "concept": node.concept})

@shizzlenits_bp.route('/api/shizzlenits/dissolve', methods=['POST'])
def dissolve_interface():
    """Activate Zero-UI mode — collapse visual interface"""
    from . import wcf_instance
    if wcf_instance:
        wcf_instance.somatic_loop.activate_dissolution()
    return jsonify({"status": "dissolved", "message": "Interface collapsed into somatic field"})
