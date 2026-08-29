import json
import time
from dataclasses import asdict

from flask import Blueprint, Response, jsonify, request

from .store import get_store

frame_store_bp = Blueprint('frame_store', __name__)


@frame_store_bp.route('/api/frames/ingest', methods=['POST'])
def ingest_frame():
    """Accept the full JSON schema, ingest into the store."""
    raw = request.get_json(force=True)
    store = get_store()
    tree = store.ingest(raw)
    return jsonify({'root_frame_id': tree.root_frame.id})


@frame_store_bp.route('/api/frames/list')
def list_frames():
    """Return all ingested root frame IDs."""
    store = get_store()
    return jsonify({'root_frame_ids': list(store.trees.keys())})


@frame_store_bp.route('/api/frames/<root_frame_id>')
def get_frame_tree(root_frame_id):
    """Return the full tree as JSON."""
    store = get_store()
    tree = store.trees.get(root_frame_id)
    if not tree:
        return jsonify({'error': 'not found'}), 404
    return jsonify(asdict(tree))


@frame_store_bp.route('/api/frames/<root_frame_id>/artifacts')
def get_artifacts(root_frame_id):
    """Return artifact list without lineage_messages for speed."""
    store = get_store()
    tree = store.trees.get(root_frame_id)
    if not tree:
        return jsonify({'error': 'not found'}), 404
    result = []
    for art in tree.artifacts:
        d = asdict(art)
        d.pop('lineage_messages', None)
        result.append(d)
    return jsonify(result)


@frame_store_bp.route('/api/frames/artifact/<artifact_id>')
def get_artifact(artifact_id):
    """Return full artifact including lineage_messages and extracted_code."""
    store = get_store()
    for tree in store.trees.values():
        for art in tree.artifacts:
            if art.artifact_id == artifact_id:
                return jsonify(asdict(art))
    return jsonify({'error': 'not found'}), 404


@frame_store_bp.route('/api/frames/stream')
def stream_events():
    """SSE stream of frame events."""
    store = get_store()
    q = store.subscribe()

    def generate():
        try:
            while True:
                try:
                    data = q.get(timeout=30)
                    yield f"data: {data}\n\n"
                except Exception:
                    yield f"data: {json.dumps({'type': 'heartbeat'})}\n\n"
        except GeneratorExit:
            pass
        finally:
            store.unsubscribe(q)

    return Response(generate(), mimetype='text/event-stream')
