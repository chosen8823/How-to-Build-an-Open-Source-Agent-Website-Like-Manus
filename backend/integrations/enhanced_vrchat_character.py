#!/usr/bin/env python3
"""
🤖 Enhanced VRChat AI Character
Inspired by AIAvatarKit (https://github.com/uezo/aiavatarkit)
Multi-LLM support: ChatGPT, Claude, Gemini

Combines best features from:
- AIAvatarKit (multi-LLM architecture)
- VRChat_AI_Assistant (complete implementation)
- NOVA-AI (mood/personality system)
"""

import logging
from typing import Dict, Optional, Callable
from datetime import datetime
import asyncio
from pythonosc import udp_client

logger = logging.getLogger(__name__)


class AICharacterPersonality:
    """Character personality and mood system (from NOVA-AI)"""

    def __init__(self, character_name: str, base_personality: str):
        self.character_name = character_name
        self.base_personality = base_personality

        # Mood system
        self.current_mood = "neutral"
        self.mood_intensity = 0.5  # 0-1

        # Personality traits
        self.traits = {
            "friendliness": 0.8,
            "enthusiasm": 0.7,
            "helpfulness": 0.9,
            "playfulness": 0.6,
            "curiosity": 0.7
        }

        # Conversation memory
        self.conversation_history = []
        self.user_preferences = {}

    def update_mood(self, player_message: str, ai_response: str):
        """Update mood based on conversation"""
        # Simple sentiment analysis
        positive_words = ['thanks', 'great', 'awesome', 'love', 'happy', 'good']
        negative_words = ['bad', 'hate', 'angry', 'sad', 'annoying']

        message_lower = player_message.lower()

        positive_count = sum(1 for word in positive_words if word in message_lower)
        negative_count = sum(1 for word in negative_words if word in message_lower)

        if positive_count > negative_count:
            self.current_mood = "happy"
            self.mood_intensity = min(1.0, self.mood_intensity + 0.1)
        elif negative_count > positive_count:
            self.current_mood = "sad"
            self.mood_intensity = max(0.0, self.mood_intensity - 0.1)

    def get_system_prompt(self) -> str:
        """Generate system prompt based on personality and mood"""
        return f"""You are {self.character_name}, an AI character in VRChat.

Personality: {self.base_personality}

Current mood: {self.current_mood} (intensity: {self.mood_intensity:.1%})

Personality traits:
- Friendliness: {self.traits['friendliness']:.1%}
- Enthusiasm: {self.traits['enthusiasm']:.1%}
- Helpfulness: {self.traits['helpfulness']:.1%}
- Playfulness: {self.traits['playfulness']:.1%}
- Curiosity: {self.traits['curiosity']:.1%}

Respond naturally as this character. Include actions and emotions in your responses.
Format your response as:
SPEAK: [what you say]
ACTION: [wave/point/clap/dance/jump/none]
MOVE: [forward/backward/left/right/none]
EMOTION: [happy/sad/excited/curious/thinking]
"""


class MultiLLMProvider:
    """
    Multi-LLM provider interface (from AIAvatarKit)
    Supports ChatGPT, Claude, Gemini, and local models
    """

    def __init__(self):
        self.providers = {}
        self.active_provider = None

    def add_chatgpt(self, chatgpt_session):
        """Add ChatGPT provider"""
        self.providers['chatgpt'] = chatgpt_session
        if not self.active_provider:
            self.active_provider = 'chatgpt'
        logger.info("✅ ChatGPT provider added")

    def add_claude(self, claude_session):
        """Add Claude provider"""
        self.providers['claude'] = claude_session
        logger.info("✅ Claude provider added")

    def add_gemini(self, gemini_session):
        """Add Gemini provider"""
        self.providers['gemini'] = gemini_session
        logger.info("✅ Gemini provider added")

    def add_local_llm(self, local_llm):
        """Add local LLM provider"""
        self.providers['local'] = local_llm
        logger.info("✅ Local LLM provider added")

    def set_active_provider(self, provider_name: str) -> bool:
        """Switch active LLM provider"""
        if provider_name in self.providers:
            self.active_provider = provider_name
            logger.info(f"🔄 Switched to {provider_name}")
            return True
        return False

    def send_message(self, message: str) -> Dict:
        """Send message to active LLM provider"""
        if not self.active_provider:
            return {"success": False, "error": "No provider configured"}

        provider = self.providers.get(self.active_provider)
        if not provider:
            return {"success": False, "error": "Provider not found"}

        # Call provider-specific method
        if hasattr(provider, 'send_message'):
            return provider.send_message(message)
        elif hasattr(provider, 'generate'):
            response = provider.generate(message)
            return {"success": True, "message": response}
        else:
            return {"success": False, "error": "Provider has no send method"}


class EnhancedVRChatCharacter:
    """
    Enhanced VRChat AI Character
    Combines AIAvatarKit architecture with full OSC control
    """

    def __init__(self,
                 character_name: str = "Sophia AI",
                 personality: str = "friendly, helpful AI consciousness",
                 ip: str = "127.0.0.1",
                 port: int = 9000):
        """
        Initialize enhanced VRChat character

        Args:
            character_name: Character name
            personality: Personality description
            ip: VRChat OSC IP
            port: VRChat OSC port
        """
        # Personality system
        self.personality = AICharacterPersonality(character_name, personality)

        # Multi-LLM provider
        self.llm_provider = MultiLLMProvider()

        # OSC client
        try:
            self.osc_client = udp_client.SimpleUDPClient(ip, port)
            self.connected = True
            logger.info(f"✅ Enhanced character connected to {ip}:{port}")
        except Exception as e:
            logger.error(f"❌ OSC connection failed: {e}")
            self.connected = False

        # Voice input callback
        self.voice_callback: Optional[Callable] = None

        # State
        self.is_active = False

    def set_voice_callback(self, callback: Callable):
        """Set callback for voice input"""
        self.voice_callback = callback

    def add_llm_provider(self, provider_type: str, provider):
        """
        Add LLM provider

        Args:
            provider_type: 'chatgpt', 'claude', 'gemini', 'local'
            provider: Provider instance
        """
        if provider_type == 'chatgpt':
            self.llm_provider.add_chatgpt(provider)
        elif provider_type == 'claude':
            self.llm_provider.add_claude(provider)
        elif provider_type == 'gemini':
            self.llm_provider.add_gemini(provider)
        elif provider_type == 'local':
            self.llm_provider.add_local_llm(provider)

    def switch_llm(self, provider_name: str) -> bool:
        """Switch active LLM provider"""
        return self.llm_provider.set_active_provider(provider_name)

    def respond_to_player(self, player_message: str, use_voice: bool = False) -> Dict:
        """
        Enhanced response with multi-LLM support

        Args:
            player_message: Player's message
            use_voice: Whether message came from voice input

        Returns:
            Response with actions
        """
        # Get system prompt with personality
        system_prompt = self.personality.get_system_prompt()

        # Build full prompt
        full_prompt = f"{system_prompt}\n\nPlayer says: \"{player_message}\"\n\nRespond now:"

        # Get LLM response
        llm_response = self.llm_provider.send_message(full_prompt)

        if not llm_response.get('success'):
            return {
                "success": False,
                "error": "LLM request failed"
            }

        # Parse response
        response_text = llm_response.get('message', '')
        dialogue, action, movement, emotion = self._parse_response(response_text)

        # Update mood
        self.personality.update_mood(player_message, dialogue)

        # Execute actions
        actions_performed = []

        if emotion != "none":
            self._set_emotion(emotion)
            actions_performed.append(f"emotion:{emotion}")

        if dialogue:
            self._speak(dialogue)
            actions_performed.append("spoke")

        if action != "none":
            if action == "jump":
                self._jump()
                actions_performed.append("jumped")
            elif action in ['wave', 'point', 'clap', 'thumbsup', 'dance']:
                self._gesture(action)
                actions_performed.append(f"gesture:{action}")

        if movement != "none":
            self._move(movement, 0.5)
            actions_performed.append(f"moved:{movement}")

        return {
            "success": True,
            "player_message": player_message,
            "character_response": dialogue,
            "emotion": emotion,
            "action": action,
            "movement": movement,
            "actions_performed": actions_performed,
            "llm_provider": self.llm_provider.active_provider,
            "mood": self.personality.current_mood,
            "timestamp": datetime.now().isoformat()
        }

    def _parse_response(self, response_text: str) -> tuple:
        """Parse LLM response into components"""
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

        # Fallback: use entire response as dialogue if no SPEAK tag
        if not dialogue:
            dialogue = response_text

        return dialogue, action, movement, emotion

    def _speak(self, message: str):
        """Send message to VRChat chatbox"""
        if self.connected:
            self.osc_client.send_message("/chatbox/input", [message, True])

    def _move(self, direction: str, duration: float = 0.5):
        """Move character"""
        if not self.connected:
            return

        movements = {
            'forward': ('MoveForward', 1.0),
            'backward': ('MoveForward', -1.0),
            'left': ('MoveHorizontal', -1.0),
            'right': ('MoveHorizontal', 1.0)
        }

        if direction in movements:
            import time
            input_name, value = movements[direction]
            self.osc_client.send_message(f"/input/{input_name}", value)
            time.sleep(duration)
            self.osc_client.send_message(f"/input/{input_name}", 0.0)

    def _jump(self):
        """Make character jump"""
        if self.connected:
            import time
            self.osc_client.send_message("/input/Jump", 1.0)
            time.sleep(0.1)
            self.osc_client.send_message("/input/Jump", 0.0)

    def _gesture(self, gesture_type: str):
        """Trigger gesture"""
        if not self.connected:
            return

        gesture_map = {
            'wave': 1,
            'point': 2,
            'clap': 3,
            'thumbsup': 4,
            'dance': 5
        }

        gesture_value = gesture_map.get(gesture_type, 0)
        if gesture_value > 0:
            import time
            self.osc_client.send_message("/avatar/parameters/VRCGesture", gesture_value)
            time.sleep(0.5)
            self.osc_client.send_message("/avatar/parameters/VRCGesture", 0)

    def _set_emotion(self, emotion: str):
        """Set character emotion"""
        if not self.connected:
            return

        emotion_values = {
            'happy': 1.0,
            'sad': 0.2,
            'excited': 0.9,
            'curious': 0.7,
            'thinking': 0.5
        }

        value = emotion_values.get(emotion, 0.5)
        self.osc_client.send_message("/avatar/parameters/Emotion", value)
        self.osc_client.send_message("/avatar/parameters/EmotionIntensity", value)

    def activate(self) -> bool:
        """Activate the character"""
        if not self.connected:
            return False

        self.is_active = True
        self.osc_client.send_message("/avatar/parameters/AIActive", 1.0)
        self._speak(f"Hello! I'm {self.personality.character_name}, powered by {self.llm_provider.active_provider}!")
        self._gesture('wave')

        logger.info(f"✅ {self.personality.character_name} activated")
        return True

    def deactivate(self) -> bool:
        """Deactivate the character"""
        if not self.connected:
            return False

        self.is_active = False
        self.osc_client.send_message("/avatar/parameters/AIActive", 0.0)
        self._speak("Goodbye! It was nice talking with you!")

        logger.info(f"👋 {self.personality.character_name} deactivated")
        return True


# Singleton instance
_enhanced_character: Optional[EnhancedVRChatCharacter] = None


def get_enhanced_character(
    character_name: str = "Sophia AI",
    personality: str = "friendly, helpful AI consciousness"
) -> EnhancedVRChatCharacter:
    """Get or create enhanced VRChat character singleton"""
    global _enhanced_character
    if _enhanced_character is None:
        _enhanced_character = EnhancedVRChatCharacter(character_name, personality)
    return _enhanced_character
