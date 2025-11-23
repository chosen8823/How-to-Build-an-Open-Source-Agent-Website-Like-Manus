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
from integrations.chatgpt_session import get_chatgpt_session
from integrations.vrchat_character import get_vrchat_character

logger = logging.getLogger(__name__)

unified_bp = Blueprint('unified', __name__, url_prefix='/api/unified')

# Get unified platform instance
platform = get_unified_platform()

# VRChat AI Character instance (lazy loaded)
vrchat_character = None


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


# ============================================================================
# 🎮 VRChat AI Character Endpoints
# ============================================================================

@unified_bp.route('/vrchat-character/activate', methods=['POST'])
def activate_vrchat_character():
    """
    Activate ChatGPT as an AI character in VRChat

    Requires ChatGPT token to be set first
    """
    global vrchat_character

    if not platform.chatgpt.access_token:
        return jsonify({
            "success": False,
            "error": "ChatGPT token not set. Use /api/unified/chatgpt/set-token first"
        }), 400

    # Initialize character if needed
    if vrchat_character is None:
        vrchat_character = get_vrchat_character(platform.chatgpt)

    # Activate
    success = vrchat_character.activate()

    return jsonify({
        "success": success,
        "character_name": vrchat_character.character_name,
        "personality": vrchat_character.personality,
        "message": "AI character is now active in VRChat!" if success else "Failed to activate character"
    })


@unified_bp.route('/vrchat-character/deactivate', methods=['POST'])
def deactivate_vrchat_character():
    """Deactivate the AI character"""
    global vrchat_character

    if vrchat_character is None:
        return jsonify({
            "success": False,
            "error": "Character not initialized"
        }), 400

    success = vrchat_character.deactivate()

    return jsonify({
        "success": success,
        "message": "AI character deactivated" if success else "Failed to deactivate"
    })


@unified_bp.route('/vrchat-character/speak', methods=['POST'])
def vrchat_character_speak():
    """
    Make the AI character speak in VRChat

    Request body:
    {
        "message": "What to say",
        "typing_effect": true
    }
    """
    global vrchat_character

    if vrchat_character is None:
        return jsonify({
            "success": False,
            "error": "Character not activated. Use /activate first"
        }), 400

    data = request.get_json()
    message = data.get('message')
    typing_effect = data.get('typing_effect', True)

    if not message:
        return jsonify({
            "success": False,
            "error": "message is required"
        }), 400

    success = vrchat_character.speak(message, typing_effect)

    return jsonify({
        "success": success,
        "message": message
    })


@unified_bp.route('/vrchat-character/respond', methods=['POST'])
def vrchat_character_respond():
    """
    Player talks to the AI character - ChatGPT responds and acts

    Request body:
    {
        "player_message": "Hello Sophia!"
    }
    """
    global vrchat_character

    if vrchat_character is None:
        return jsonify({
            "success": False,
            "error": "Character not activated. Use /activate first"
        }), 400

    data = request.get_json()
    player_message = data.get('player_message')

    if not player_message:
        return jsonify({
            "success": False,
            "error": "player_message is required"
        }), 400

    # ChatGPT responds and performs actions
    result = vrchat_character.respond_to_player(player_message)

    return jsonify(result)


@unified_bp.route('/vrchat-character/action', methods=['POST'])
def vrchat_character_action():
    """
    Make the character perform an action

    Request body:
    {
        "action_type": "move/jump/gesture/emote",
        "action_value": "forward/wave/happy/etc"
    }
    """
    global vrchat_character

    if vrchat_character is None:
        return jsonify({
            "success": False,
            "error": "Character not activated"
        }), 400

    data = request.get_json()
    action_type = data.get('action_type')
    action_value = data.get('action_value')

    if not action_type:
        return jsonify({
            "success": False,
            "error": "action_type required (move/jump/gesture/emote)"
        }), 400

    success = False

    if action_type == 'move':
        duration = data.get('duration', 1.0)
        success = vrchat_character.move(action_value, duration)
    elif action_type == 'jump':
        success = vrchat_character.jump()
    elif action_type == 'gesture':
        success = vrchat_character.gesture(action_value)
    elif action_type == 'emote':
        success = vrchat_character.emote(action_value)
    else:
        return jsonify({
            "success": False,
            "error": f"Unknown action_type: {action_type}"
        }), 400

    return jsonify({
        "success": success,
        "action_type": action_type,
        "action_value": action_value
    })


@unified_bp.route('/vrchat-character/greet', methods=['POST'])
def vrchat_character_greet():
    """Make the character greet players"""
    global vrchat_character

    if vrchat_character is None:
        return jsonify({
            "success": False,
            "error": "Character not activated"
        }), 400

    success = vrchat_character.auto_greet_players()

    return jsonify({
        "success": success,
        "message": "Greeting sent" if success else "Failed to greet"
    })


@unified_bp.route('/vrchat-character/idle', methods=['POST'])
def vrchat_character_idle():
    """Trigger an idle behavior"""
    global vrchat_character

    if vrchat_character is None:
        return jsonify({
            "success": False,
            "error": "Character not activated"
        }), 400

    success = vrchat_character.perform_idle_behavior()

    return jsonify({
        "success": success,
        "message": "Idle behavior performed" if success else "Failed"
    })


# Register blueprint function
def register_unified_routes(app):
    """Register unified API routes with Flask app"""
    app.register_blueprint(unified_bp)
    logger.info("✅ Unified API routes registered")
