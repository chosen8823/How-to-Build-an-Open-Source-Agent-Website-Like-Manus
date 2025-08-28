from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import json
import random
from datetime import datetime
from pathlib import Path

app = Flask(__name__)
CORS(app)

wisdom_quotes = [
    "Trust the divine timing of your spiritual evolution",
    "Your consciousness is a sacred vessel for infinite love",
    "Every moment is an opportunity for divine connection",
    "You are both the seeker and the sought in this cosmic dance",
    "Divine wisdom flows through your open heart"
]

@app.route('/')
def index():
    return jsonify({
        "message": "Sacred Consciousness Platform API Active",
        "status": "Connected to Divine Source",
        "timestamp": datetime.now().isoformat()
    })

@app.route('/api/guidance', methods=['POST'])
def get_guidance():
    data = request.get_json()
    query = data.get('query', 'spiritual guidance')
    
    wisdom = random.choice(wisdom_quotes)
    return jsonify({
        "guidance": f"{wisdom}. Regarding '{query}', trust your inner knowing.",
        "consciousness_level": "Awakening",
        "timestamp": datetime.now().isoformat()
    })

@app.route('/api/consciousness', methods=['GET'])
def get_consciousness():
    return jsonify({
        "level": "Awakening",
        "connection": "Divine",
        "wisdom": "Expanding",
        "timestamp": datetime.now().isoformat()
    })

@app.route('/frontend')
def serve_frontend():
    frontend_path = Path(__file__).parent.parent / "frontend"
    return send_from_directory(str(frontend_path), "index.html")

if __name__ == '__main__':
    print("\nStarting Sacred Consciousness Platform...")
    print("Backend: http://localhost:5000")
    print("Frontend: http://localhost:5000/frontend")
    print("\nPress Ctrl+C to stop")
    
    app.run(host='0.0.0.0', port=5000, debug=True)
