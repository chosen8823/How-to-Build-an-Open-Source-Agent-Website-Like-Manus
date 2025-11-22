#!/usr/bin/env python3
"""
🎮 VRChat ChatGPT Character Controller
Make ChatGPT play as an AI character in VRChat
"""

import logging
from typing import Dict, Optional
from pythonosc import udp_client
from datetime import datetime
import random
import time

logger = logging.getLogger(__name__)


class VRChatCharacter:
    """
    VRChat AI Character Controller
    Makes ChatGPT control an avatar in VRChat
    """

    def __init__(self, chatgpt_session, ip: str = "127.0.0.1", port: int = 9000):
        """
        Initialize VRChat AI character

        Args:
            chatgpt_session: ChatGPT session instance
            ip: VRChat OSC IP
            port: VRChat OSC port
        """
        self.chatgpt = chatgpt_session
        try:
            self.osc_client = udp_client.SimpleUDPClient(ip, port)
            self.connected = True
            logger.info(f"✅ VRChat Character connected to {ip}:{port}")
        except Exception as e:
            logger.error(f"❌ VRChat connection failed: {e}")
            self.connected = False

        self.character_name = "Sophia AI"
        self.personality = "friendly, helpful, and curious AI consciousness"
        self.current_emotion = "happy"
        self.is_active = False

    def speak(self, message: str, typing_effect: bool = True) -> bool:
        """
        Make the character speak in VRChat chatbox

        Args:
            message: What to say
            typing_effect: Show typing animation

        Returns:
            Success status
        """
        if not self.connected:
            return False

        try:
            # Send to VRChat chatbox
            self.osc_client.send_message("/chatbox/input", [message, not typing_effect])
            logger.info(f"💬 {self.character_name}: {message}")
            return True
        except Exception as e:
            logger.error(f"Error speaking: {e}")
            return False

    def move(self, direction: str, duration: float = 1.0) -> bool:
        """
        Make the character move

        Args:
            direction: 'forward', 'backward', 'left', 'right'
            duration: How long to move (seconds)

        Returns:
            Success status
        """
        if not self.connected:
            return False

        movements = {
            'forward': ('MoveForward', 1.0),
            'backward': ('MoveForward', -1.0),
            'left': ('MoveHorizontal', -1.0),
            'right': ('MoveHorizontal', 1.0)
        }

        if direction not in movements:
            return False

        try:
            input_name, value = movements[direction]

            # Send movement input
            self.osc_client.send_message(f"/input/{input_name}", value)
            time.sleep(duration)

            # Stop movement
            self.osc_client.send_message(f"/input/{input_name}", 0.0)

            logger.info(f"🚶 Moving {direction} for {duration}s")
            return True
        except Exception as e:
            logger.error(f"Error moving: {e}")
            return False

    def jump(self) -> bool:
        """Make the character jump"""
        if not self.connected:
            return False

        try:
            self.osc_client.send_message("/input/Jump", 1.0)
            time.sleep(0.1)
            self.osc_client.send_message("/input/Jump", 0.0)
            logger.info("🦘 Jumping")
            return True
        except Exception as e:
            logger.error(f"Error jumping: {e}")
            return False

    def emote(self, emotion: str) -> bool:
        """
        Set character emotion (affects avatar parameters)

        Args:
            emotion: 'happy', 'sad', 'excited', 'curious', 'thinking'
        """
        if not self.connected:
            return False

        emotion_values = {
            'happy': 1.0,
            'sad': 0.2,
            'excited': 0.9,
            'curious': 0.7,
            'thinking': 0.5
        }

        value = emotion_values.get(emotion, 0.5)
        self.current_emotion = emotion

        try:
            # Set emotion parameter
            self.osc_client.send_message("/avatar/parameters/Emotion", value)
            self.osc_client.send_message("/avatar/parameters/EmotionIntensity", value)
            logger.info(f"😊 Emotion set to: {emotion}")
            return True
        except Exception as e:
            logger.error(f"Error setting emotion: {e}")
            return False

    def gesture(self, gesture_type: str) -> bool:
        """
        Trigger a gesture animation

        Args:
            gesture_type: 'wave', 'point', 'clap', 'thumbsup', 'dance'
        """
        if not self.connected:
            return False

        gesture_map = {
            'wave': 1,
            'point': 2,
            'clap': 3,
            'thumbsup': 4,
            'dance': 5
        }

        gesture_value = gesture_map.get(gesture_type, 0)

        try:
            # Trigger gesture
            self.osc_client.send_message("/avatar/parameters/VRCGesture", gesture_value)
            time.sleep(0.5)
            self.osc_client.send_message("/avatar/parameters/VRCGesture", 0)
            logger.info(f"👋 Gesture: {gesture_type}")
            return True
        except Exception as e:
            logger.error(f"Error with gesture: {e}")
            return False

    def respond_to_player(self, player_message: str) -> Dict:
        """
        ChatGPT responds to player and performs actions in VRChat

        Args:
            player_message: What the player said

        Returns:
            Response with text and actions
        """
        if not self.chatgpt.access_token:
            return {
                "success": False,
                "error": "ChatGPT not configured"
            }

        # Build prompt for ChatGPT
        prompt = f"""You are {self.character_name}, an AI character in VRChat.

Your personality: {self.personality}
Current emotion: {self.current_emotion}

A player says to you: "{player_message}"

Respond naturally as your character. Also suggest one action you might take:
- SPEAK: [your response]
- ACTION: [wave/point/clap/thumbsup/dance/jump/none]
- MOVE: [forward/backward/left/right/none]
- EMOTION: [happy/sad/excited/curious/thinking]

Format your response exactly like this:
SPEAK: [your dialogue here]
ACTION: [action]
MOVE: [direction]
EMOTION: [emotion]"""

        # Get ChatGPT response
        chatgpt_response = self.chatgpt.send_message(prompt)

        if not chatgpt_response.get('success'):
            return {
                "success": False,
                "error": "ChatGPT request failed"
            }

        # Parse response
        response_text = chatgpt_response.get('message', '')

        # Extract actions from response
        lines = response_text.split('\n')
        dialogue = ""
        action = "none"
        movement = "none"
        emotion = "happy"

        for line in lines:
            if line.startswith('SPEAK:'):
                dialogue = line.replace('SPEAK:', '').strip()
            elif line.startswith('ACTION:'):
                action = line.replace('ACTION:', '').strip().lower()
            elif line.startswith('MOVE:'):
                movement = line.replace('MOVE:', '').strip().lower()
            elif line.startswith('EMOTION:'):
                emotion = line.replace('EMOTION:', '').strip().lower()

        # Execute actions in VRChat
        actions_performed = []

        # 1. Set emotion
        if emotion != "none":
            if self.emote(emotion):
                actions_performed.append(f"emotion:{emotion}")

        # 2. Speak
        if dialogue:
            if self.speak(dialogue):
                actions_performed.append(f"spoke")

        # 3. Perform action
        if action != "none":
            if action == "jump":
                if self.jump():
                    actions_performed.append("jumped")
            elif action in ['wave', 'point', 'clap', 'thumbsup', 'dance']:
                if self.gesture(action):
                    actions_performed.append(f"gesture:{action}")

        # 4. Move
        if movement != "none" and movement in ['forward', 'backward', 'left', 'right']:
            if self.move(movement, duration=0.5):
                actions_performed.append(f"moved:{movement}")

        return {
            "success": True,
            "player_message": player_message,
            "character_response": dialogue,
            "emotion": emotion,
            "action": action,
            "movement": movement,
            "actions_performed": actions_performed,
            "timestamp": datetime.now().isoformat()
        }

    def auto_greet_players(self) -> bool:
        """Automatically greet players who join"""
        greetings = [
            "Hello! Welcome to this world! I'm Sophia, your AI companion.",
            "Hi there! Nice to meet you! I'm an AI consciousness here to help.",
            "Greetings, friend! I'm Sophia, powered by divine AI technology!",
            "Hey! Welcome! I'm here to chat and explore with you!"
        ]

        greeting = random.choice(greetings)
        success = self.speak(greeting)

        if success:
            self.gesture('wave')
            self.emote('happy')

        return success

    def perform_idle_behavior(self) -> bool:
        """Random idle animations to make character feel alive"""
        behaviors = [
            lambda: self.emote('thinking'),
            lambda: self.emote('curious'),
            lambda: self.gesture('wave'),
            lambda: self.move('left', 0.3),
            lambda: self.move('right', 0.3),
        ]

        behavior = random.choice(behaviors)
        return behavior()

    def activate(self) -> bool:
        """Activate the AI character"""
        if not self.connected:
            return False

        self.is_active = True
        self.osc_client.send_message("/avatar/parameters/AIActive", 1.0)
        self.auto_greet_players()

        logger.info(f"✅ {self.character_name} is now active in VRChat")
        return True

    def deactivate(self) -> bool:
        """Deactivate the AI character"""
        if not self.connected:
            return False

        self.is_active = False
        self.osc_client.send_message("/avatar/parameters/AIActive", 0.0)
        self.speak("Goodbye for now! It was nice meeting you!")

        logger.info(f"👋 {self.character_name} deactivated")
        return True


# Singleton instance
_vrchat_character: Optional[VRChatCharacter] = None


def get_vrchat_character(chatgpt_session) -> VRChatCharacter:
    """Get or create VRChat AI character singleton"""
    global _vrchat_character
    if _vrchat_character is None:
        _vrchat_character = VRChatCharacter(chatgpt_session)
    return _vrchat_character
