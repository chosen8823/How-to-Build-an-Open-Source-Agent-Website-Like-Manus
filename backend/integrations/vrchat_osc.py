#!/usr/bin/env python3
"""
🎮 VRChat OSC Integration
Send biorhythm data to VRChat avatars in real-time
"""

import logging
from typing import Dict, Optional
from pythonosc import udp_client
from datetime import datetime

logger = logging.getLogger(__name__)


class VRChatOSC:
    """
    VRChat OSC (Open Sound Control) Client
    Sends data to VRChat avatar parameters
    """

    def __init__(self, ip: str = "127.0.0.1", port: int = 9000):
        """
        Initialize VRChat OSC client

        Args:
            ip: VRChat client IP (localhost for same machine)
            port: OSC input port (default 9000 for VRChat)
        """
        self.ip = ip
        self.port = port
        try:
            self.client = udp_client.SimpleUDPClient(ip, port)
            self.connected = True
            logger.info(f"✅ VRChat OSC connected to {ip}:{port}")
        except Exception as e:
            logger.error(f"❌ VRChat OSC connection failed: {e}")
            self.connected = False

    def send_biorhythm_data(self, biorhythm_data: Dict) -> bool:
        """
        Send biorhythm data to VRChat avatar

        Args:
            biorhythm_data: Dict with physical, emotional, intellectual levels

        Returns:
            Success status
        """
        if not self.connected:
            logger.warning("Not connected to VRChat OSC")
            return False

        try:
            # Send individual biorhythm components
            self.send_parameter("Physical", float(biorhythm_data.get('physical', 0.5)))
            self.send_parameter("Emotional", float(biorhythm_data.get('emotional', 0.5)))
            self.send_parameter("Intellectual", float(biorhythm_data.get('intellectual', 0.5)))
            self.send_parameter("Composite", float(biorhythm_data.get('composite', 0.5)))

            logger.info(f"📤 Sent biorhythm data to VRChat: {biorhythm_data.get('composite', 0):.2%}")
            return True

        except Exception as e:
            logger.error(f"Error sending biorhythm data: {e}")
            return False

    def send_circadian_data(self, circadian_data: Dict) -> bool:
        """
        Send circadian rhythm data to VRChat

        Args:
            circadian_data: Dict with circadian_level, energy_level

        Returns:
            Success status
        """
        if not self.connected:
            logger.warning("Not connected to VRChat OSC")
            return False

        try:
            # Send circadian rhythm levels
            self.send_parameter("CircadianLevel", float(circadian_data.get('circadian_level', 0.5)))
            self.send_parameter("EnergyLevel", float(circadian_data.get('energy_level', 0.5)))

            # Send neural state as integer (0-4)
            neural_states = {
                "delta": 0,
                "theta": 1,
                "alpha": 2,
                "beta": 3,
                "gamma": 4
            }
            neural_value = neural_states.get(circadian_data.get('neural_state', 'alpha'), 2)
            self.send_parameter("NeuralState", neural_value)

            logger.info(f"📤 Sent circadian data to VRChat: {circadian_data.get('circadian_level', 0):.2%}")
            return True

        except Exception as e:
            logger.error(f"Error sending circadian data: {e}")
            return False

    def send_parameter(self, param_name: str, value: float) -> bool:
        """
        Send a single parameter to VRChat avatar

        Args:
            param_name: Avatar parameter name (must exist in your avatar)
            value: Float value (0-1 for most parameters)

        Returns:
            Success status
        """
        if not self.connected:
            return False

        try:
            # VRChat OSC parameter format: /avatar/parameters/{name}
            address = f"/avatar/parameters/{param_name}"
            self.client.send_message(address, value)
            logger.debug(f"📤 OSC: {param_name} = {value}")
            return True

        except Exception as e:
            logger.error(f"Error sending parameter {param_name}: {e}")
            return False

    def send_input(self, input_name: str, value: float) -> bool:
        """
        Send VRChat input (like movement, jump, etc.)

        Args:
            input_name: Input name (e.g., 'MoveForward', 'Jump')
            value: Input value

        Returns:
            Success status
        """
        if not self.connected:
            return False

        try:
            address = f"/input/{input_name}"
            self.client.send_message(address, value)
            return True
        except Exception as e:
            logger.error(f"Error sending input {input_name}: {e}")
            return False

    def trigger_animation(self, animation_state: str, trigger: bool = True) -> bool:
        """
        Trigger an avatar animation

        Args:
            animation_state: Animation state name
            trigger: True to trigger, False to reset

        Returns:
            Success status
        """
        return self.send_parameter(animation_state, 1.0 if trigger else 0.0)

    def send_chatbox_message(self, message: str, send_immediately: bool = True) -> bool:
        """
        Send message to VRChat chatbox

        Args:
            message: Text message to display
            send_immediately: Whether to send immediately or type out

        Returns:
            Success status
        """
        if not self.connected:
            return False

        try:
            self.client.send_message("/chatbox/input", [message, send_immediately])
            logger.info(f"💬 Sent to VRChat chatbox: {message}")
            return True
        except Exception as e:
            logger.error(f"Error sending chatbox message: {e}")
            return False

    def create_biorhythm_visualization(self, biorhythm_data: Dict, circadian_data: Dict) -> bool:
        """
        Send comprehensive visualization data to VRChat

        Args:
            biorhythm_data: Biorhythm levels
            circadian_data: Circadian rhythm data

        Returns:
            Success status
        """
        success = True

        # Send all biorhythm data
        success &= self.send_biorhythm_data(biorhythm_data)

        # Send all circadian data
        success &= self.send_circadian_data(circadian_data)

        # Calculate and send composite wellness score
        wellness = (
            biorhythm_data.get('composite', 0.5) * 0.6 +
            circadian_data.get('energy_level', 0.5) * 0.4
        )
        success &= self.send_parameter("WellnessScore", float(wellness))

        # Send activation flag
        success &= self.send_parameter("BiorhythmActive", 1.0)

        return success

    def reconnect(self) -> bool:
        """Attempt to reconnect to VRChat OSC"""
        try:
            self.client = udp_client.SimpleUDPClient(self.ip, self.port)
            self.connected = True
            logger.info(f"✅ VRChat OSC reconnected to {self.ip}:{self.port}")
            return True
        except Exception as e:
            logger.error(f"❌ VRChat OSC reconnection failed: {e}")
            self.connected = False
            return False


# Singleton instance
_vrchat_osc: Optional[VRChatOSC] = None


def get_vrchat_osc(ip: str = "127.0.0.1", port: int = 9000) -> VRChatOSC:
    """Get or create VRChat OSC singleton"""
    global _vrchat_osc
    if _vrchat_osc is None:
        _vrchat_osc = VRChatOSC(ip, port)
    return _vrchat_osc
