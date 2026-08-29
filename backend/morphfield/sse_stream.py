"""SSE stream + REST endpoint for Kuramoto field state."""

from flask import Blueprint, Response, stream_with_context, jsonify
import json
import time

morphfield_bp = Blueprint('morphfield', __name__)
_engine = None


def set_engine(engine):
    global _engine
    _engine = engine


@morphfield_bp.route('/api/fields/stream')
def field_stream():
    def generate():
        while True:
            if _engine:
                snapshot = _engine.state_snapshot()
                yield f"data: {json.dumps(snapshot)}\n\n"
            time.sleep(0.1)

    return Response(
        stream_with_context(generate()),
        mimetype='text/event-stream',
        headers={'Cache-Control': 'no-cache', 'X-Accel-Buffering': 'no'},
    )


@morphfield_bp.route('/api/fields/state')
def field_state():
    if _engine:
        return jsonify(_engine.state_snapshot())
    return jsonify({'fields': [], 'couplings': []})
