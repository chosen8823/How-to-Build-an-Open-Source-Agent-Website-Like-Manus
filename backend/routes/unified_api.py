#!/usr/bin/env python3
"""
🌟 Unified API Routes
Flask endpoints for ChatGPT + Biorhythm + VRChat integration
"""

from flask import Blueprint, request, jsonify
from datetime import datetime
import logging
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from integrations.unified_platform import get_unified_platform

logger = logging.getLogger(__name__)

unified_bp = Blueprint('unified', __name__, url_prefix='/api/unified')

# Get unified platform instance
platform = get_unified_platform()


@unified_bp.route('/health', methods=['GET'])
def health():
    """Health check for unified platform"""
    status = platform.get_status()
    return jsonify({
        "ok": True,
        "status": status,
        "timestamp": datetime.now().isoformat()
    })


@unified_bp.route('/chatgpt/set-token', methods=['POST'])
def set_chatgpt_token():
    """
    Set ChatGPT access token

    Request body:
    {
        "access_token": "your_chatgpt_access_token"
    }
    """
    data = request.get_json()
    access_token = data.get('access_token')

    if not access_token:
        return jsonify({
            "success": False,
            "error": "access_token is required"
        }), 400

    result = platform.set_chatgpt_token(access_token)
    return jsonify(result)


@unified_bp.route('/chatgpt/ask', methods=['POST'])
def ask_chatgpt():
    """
    Ask ChatGPT a question

    Request body:
    {
        "question": "Your question here"
    }
    """
    data = request.get_json()
    question = data.get('question')

    if not question:
        return jsonify({
            "success": False,
            "error": "question is required"
        }), 400

    result = platform.ask_chatgpt(question)
    return jsonify(result)


@unified_bp.route('/biorhythm/set-birth-date', methods=['POST'])
def set_birth_date():
    """
    Set user birth date for biorhythm calculations

    Request body:
    {
        "birth_date": "1990-01-15"  // YYYY-MM-DD format
    }
    """
    data = request.get_json()
    birth_date_str = data.get('birth_date')

    if not birth_date_str:
        return jsonify({
            "success": False,
            "error": "birth_date is required (YYYY-MM-DD format)"
        }), 400

    try:
        birth_date = datetime.strptime(birth_date_str, "%Y-%m-%d")
        result = platform.set_user_birth_date(birth_date)
        return jsonify(result)
    except ValueError:
        return jsonify({
            "success": False,
            "error": "Invalid date format. Use YYYY-MM-DD"
        }), 400


@unified_bp.route('/biorhythm/analyze', methods=['POST'])
def analyze_biorhythm():
    """
    Analyze biorhythm with optional AI interpretation

    Request body (all optional):
    {
        "birth_date": "1990-01-15",  // Optional, uses stored if not provided
        "ask_chatgpt": true           // Optional, default true
    }
    """
    data = request.get_json() or {}

    birth_date = None
    if data.get('birth_date'):
        try:
            birth_date = datetime.strptime(data['birth_date'], "%Y-%m-%d")
        except ValueError:
            return jsonify({
                "success": False,
                "error": "Invalid birth_date format. Use YYYY-MM-DD"
            }), 400

    ask_chatgpt = data.get('ask_chatgpt', True)

    result = platform.analyze_biorhythm_with_ai(
        birth_date=birth_date,
        ask_chatgpt=ask_chatgpt
    )
    return jsonify(result)


@unified_bp.route('/circadian/analyze', methods=['POST'])
def analyze_circadian():
    """
    Analyze circadian rhythm with optional AI recommendations

    Request body (all optional):
    {
        "sleep_schedule": {
            "bedtime": 23,      // 24-hour format
            "wake_time": 7
        },
        "ask_chatgpt": true
    }
    """
    data = request.get_json() or {}

    sleep_schedule = data.get('sleep_schedule')
    ask_chatgpt = data.get('ask_chatgpt', True)

    result = platform.analyze_circadian_rhythm_with_ai(
        sleep_schedule=sleep_schedule,
        ask_chatgpt=ask_chatgpt
    )
    return jsonify(result)


@unified_bp.route('/wellness/complete', methods=['POST'])
def complete_wellness_analysis():
    """
    Complete wellness analysis combining all systems

    Request body:
    {
        "birth_date": "1990-01-15",   // Required if not previously set
        "sleep_schedule": {            // Optional
            "bedtime": 23,
            "wake_time": 7
        },
        "sleep_data": [                // Optional historical sleep data
            {
                "date": "2025-01-20",
                "sleep_hours": 7.5,
                "quality": 0.8
            }
        ]
    }
    """
    data = request.get_json() or {}

    birth_date = None
    if data.get('birth_date'):
        try:
            birth_date = datetime.strptime(data['birth_date'], "%Y-%m-%d")
        except ValueError:
            return jsonify({
                "success": False,
                "error": "Invalid birth_date format. Use YYYY-MM-DD"
            }), 400

    sleep_schedule = data.get('sleep_schedule')
    sleep_data = data.get('sleep_data')

    result = platform.complete_wellness_analysis(
        birth_date=birth_date,
        sleep_schedule=sleep_schedule,
        sleep_data=sleep_data
    )
    return jsonify(result)


@unified_bp.route('/vrchat/send-parameter', methods=['POST'])
def vrchat_send_parameter():
    """
    Manually send parameter to VRChat avatar

    Request body:
    {
        "parameter_name": "MyParameter",
        "value": 0.75
    }
    """
    data = request.get_json()
    parameter_name = data.get('parameter_name')
    value = data.get('value')

    if not parameter_name:
        return jsonify({
            "success": False,
            "error": "parameter_name is required"
        }), 400

    if value is None:
        return jsonify({
            "success": False,
            "error": "value is required"
        }), 400

    try:
        value = float(value)
    except (ValueError, TypeError):
        return jsonify({
            "success": False,
            "error": "value must be a number"
        }), 400

    result = platform.update_vrchat_manually(parameter_name, value)
    return jsonify(result)


@unified_bp.route('/vrchat/send-chatbox', methods=['POST'])
def vrchat_send_chatbox():
    """
    Send message to VRChat chatbox

    Request body:
    {
        "message": "Hello from Python!",
        "send_immediately": true
    }
    """
    data = request.get_json()
    message = data.get('message')
    send_immediately = data.get('send_immediately', True)

    if not message:
        return jsonify({
            "success": False,
            "error": "message is required"
        }), 400

    success = platform.vrchat.send_chatbox_message(message, send_immediately)
    return jsonify({
        "success": success,
        "message": message
    })


@unified_bp.route('/status', methods=['GET'])
def get_status():
    """Get status of all integrated systems"""
    return jsonify(platform.get_status())


# Register blueprint function
def register_unified_routes(app):
    """Register unified API routes with Flask app"""
    app.register_blueprint(unified_bp)
    logger.info("✅ Unified API routes registered")
