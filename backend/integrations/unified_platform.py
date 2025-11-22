#!/usr/bin/env python3
"""
🌟 UNIFIED AI PLATFORM
ChatGPT + Hugging Face + VRChat OSC Integration
Complete biorhythm analysis and visualization system
"""

import logging
from typing import Dict, Optional
from datetime import datetime
from .chatgpt_session import get_chatgpt_session
from .biorhythm_analyzer import get_biorhythm_analyzer
from .vrchat_osc import get_vrchat_osc

logger = logging.getLogger(__name__)


class UnifiedAIPlatform:
    """
    Unified platform combining:
    - ChatGPT Web (conversational AI analysis)
    - Biorhythm Analyzer (neural pathways & circadian rhythms)
    - VRChat OSC (real-time avatar visualization)
    """

    def __init__(self):
        self.chatgpt = get_chatgpt_session()
        self.biorhythm = get_biorhythm_analyzer()
        self.vrchat = get_vrchat_osc()

        self.user_birth_date = None
        self.last_biorhythm_update = None
        self.last_circadian_update = None

        logger.info("🌟 Unified AI Platform initialized")

    def set_chatgpt_token(self, access_token: str) -> Dict:
        """
        Set ChatGPT access token

        Args:
            access_token: Access token from ChatGPT session

        Returns:
            Status response
        """
        try:
            self.chatgpt.set_access_token(access_token)
            return {
                "success": True,
                "message": "ChatGPT session configured",
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            logger.error(f"Error setting ChatGPT token: {e}")
            return {
                "success": False,
                "error": str(e)
            }

    def set_user_birth_date(self, birth_date: datetime) -> Dict:
        """Set user birth date for biorhythm calculations"""
        self.user_birth_date = birth_date
        return {
            "success": True,
            "message": "Birth date set for biorhythm analysis"
        }

    def analyze_biorhythm_with_ai(
        self,
        birth_date: Optional[datetime] = None,
        ask_chatgpt: bool = True
    ) -> Dict:
        """
        Complete biorhythm analysis with AI interpretation

        Args:
            birth_date: User's birth date (uses stored if not provided)
            ask_chatgpt: Whether to get ChatGPT's interpretation

        Returns:
            Complete analysis with biorhythm data and AI insights
        """
        if birth_date:
            self.user_birth_date = birth_date
        elif not self.user_birth_date:
            return {
                "success": False,
                "error": "Birth date not set. Use set_user_birth_date() first"
            }

        try:
            # 1. Calculate biorhythm
            biorhythm_data = self.biorhythm.calculate_biorhythm(self.user_birth_date)
            self.last_biorhythm_update = datetime.now()

            # 2. Get AI interpretation from ChatGPT (if enabled)
            ai_interpretation = None
            if ask_chatgpt and self.chatgpt.access_token:
                prompt = f"""Analyze this biorhythm data and provide wellness insights:

Physical: {biorhythm_data['physical']:.1%}
Emotional: {biorhythm_data['emotional']:.1%}
Intellectual: {biorhythm_data['intellectual']:.1%}
Composite: {biorhythm_data['composite']:.1%}

Provide:
1. Brief interpretation (2-3 sentences)
2. Recommended activities for today
3. Energy management tips"""

                chatgpt_response = self.chatgpt.send_message(prompt)
                if chatgpt_response.get('success'):
                    ai_interpretation = chatgpt_response.get('message')

            # 3. Send to VRChat
            vrchat_success = self.vrchat.send_biorhythm_data(biorhythm_data)

            return {
                "success": True,
                "biorhythm": biorhythm_data,
                "ai_interpretation": ai_interpretation,
                "vrchat_updated": vrchat_success,
                "timestamp": datetime.now().isoformat()
            }

        except Exception as e:
            logger.error(f"Error in biorhythm analysis: {e}")
            return {
                "success": False,
                "error": str(e)
            }

    def analyze_circadian_rhythm_with_ai(
        self,
        sleep_schedule: Optional[Dict] = None,
        ask_chatgpt: bool = True
    ) -> Dict:
        """
        Complete circadian rhythm analysis with AI recommendations

        Args:
            sleep_schedule: Optional sleep schedule {'bedtime': 23, 'wake_time': 7}
            ask_chatgpt: Whether to get ChatGPT's recommendations

        Returns:
            Complete circadian analysis with AI recommendations
        """
        try:
            # 1. Calculate circadian rhythm
            circadian_data = self.biorhythm.calculate_circadian_rhythm(
                sleep_schedule=sleep_schedule
            )
            self.last_circadian_update = datetime.now()

            # 2. Get AI recommendations from ChatGPT (if enabled)
            ai_recommendations = None
            if ask_chatgpt and self.chatgpt.access_token:
                prompt = f"""Analyze this circadian rhythm data and provide personalized recommendations:

Circadian Level: {circadian_data['circadian_level']:.1%}
Energy Level: {circadian_data['energy_level']:.1%}
Hours Awake: {circadian_data['hours_awake']}
Neural State: {circadian_data['neural_state']}
Current Time: {circadian_data['current_time']}

Provide:
1. Current state analysis
2. Optimal activities for this time
3. When to schedule important tasks today
4. Sleep/rest recommendations"""

                chatgpt_response = self.chatgpt.send_message(prompt)
                if chatgpt_response.get('success'):
                    ai_recommendations = chatgpt_response.get('message')

            # 3. Send to VRChat
            vrchat_success = self.vrchat.send_circadian_data(circadian_data)

            return {
                "success": True,
                "circadian": circadian_data,
                "ai_recommendations": ai_recommendations,
                "vrchat_updated": vrchat_success,
                "timestamp": datetime.now().isoformat()
            }

        except Exception as e:
            logger.error(f"Error in circadian analysis: {e}")
            return {
                "success": False,
                "error": str(e)
            }

    def complete_wellness_analysis(
        self,
        birth_date: Optional[datetime] = None,
        sleep_schedule: Optional[Dict] = None,
        sleep_data: Optional[list] = None
    ) -> Dict:
        """
        Complete wellness analysis combining all systems

        Args:
            birth_date: User's birth date
            sleep_schedule: Sleep schedule dict
            sleep_data: Historical sleep data

        Returns:
            Comprehensive wellness report
        """
        if birth_date:
            self.user_birth_date = birth_date
        elif not self.user_birth_date:
            return {
                "success": False,
                "error": "Birth date required for wellness analysis"
            }

        try:
            # 1. Biorhythm analysis
            biorhythm_result = self.analyze_biorhythm_with_ai(ask_chatgpt=False)

            # 2. Circadian rhythm analysis
            circadian_result = self.analyze_circadian_rhythm_with_ai(
                sleep_schedule=sleep_schedule,
                ask_chatgpt=False
            )

            # 3. Sleep analysis (if data provided)
            sleep_analysis = None
            if sleep_data:
                sleep_analysis = self.biorhythm.analyze_sleep_data(sleep_data)

            # 4. Get comprehensive AI analysis from ChatGPT
            ai_comprehensive_analysis = None
            if self.chatgpt.access_token:
                wellness_summary = f"""Provide a comprehensive wellness analysis based on this data:

BIORHYTHM:
- Physical: {biorhythm_result['biorhythm']['physical']:.1%}
- Emotional: {biorhythm_result['biorhythm']['emotional']:.1%}
- Intellectual: {biorhythm_result['biorhythm']['intellectual']:.1%}

CIRCADIAN RHYTHM:
- Circadian Level: {circadian_result['circadian']['circadian_level']:.1%}
- Energy Level: {circadian_result['circadian']['energy_level']:.1%}
- Neural State: {circadian_result['circadian']['neural_state']}

{f"SLEEP ANALYSIS:\n- Avg Hours: {sleep_analysis['average_sleep_hours']}\n- Quality: {sleep_analysis['average_quality']:.1%}\n- Sleep Debt: {sleep_analysis['sleep_debt_hours']} hours" if sleep_analysis else ""}

Provide:
1. Overall wellness assessment
2. Top 3 personalized recommendations
3. Optimal schedule for today
4. Long-term wellness strategies"""

                chatgpt_response = self.chatgpt.send_message(wellness_summary)
                if chatgpt_response.get('success'):
                    ai_comprehensive_analysis = chatgpt_response.get('message')

            # 5. Send comprehensive data to VRChat
            vrchat_success = self.vrchat.create_biorhythm_visualization(
                biorhythm_result['biorhythm'],
                circadian_result['circadian']
            )

            # 6. Send summary to VRChat chatbox
            if vrchat_success:
                chatbox_msg = f"Wellness: {biorhythm_result['biorhythm']['composite']:.0%} | Energy: {circadian_result['circadian']['energy_level']:.0%}"
                self.vrchat.send_chatbox_message(chatbox_msg)

            return {
                "success": True,
                "biorhythm": biorhythm_result['biorhythm'],
                "circadian": circadian_result['circadian'],
                "sleep_analysis": sleep_analysis,
                "ai_comprehensive_analysis": ai_comprehensive_analysis,
                "vrchat_updated": vrchat_success,
                "timestamp": datetime.now().isoformat()
            }

        except Exception as e:
            logger.error(f"Error in complete wellness analysis: {e}")
            return {
                "success": False,
                "error": str(e)
            }

    def ask_chatgpt(self, question: str) -> Dict:
        """
        Ask ChatGPT a question

        Args:
            question: Your question

        Returns:
            ChatGPT's response
        """
        if not self.chatgpt.access_token:
            return {
                "success": False,
                "error": "ChatGPT not configured. Set access token first."
            }

        return self.chatgpt.send_message(question)

    def update_vrchat_manually(
        self,
        parameter_name: str,
        value: float
    ) -> Dict:
        """
        Manually update VRChat avatar parameter

        Args:
            parameter_name: Avatar parameter name
            value: Parameter value (0-1)

        Returns:
            Success status
        """
        success = self.vrchat.send_parameter(parameter_name, value)
        return {
            "success": success,
            "parameter": parameter_name,
            "value": value
        }

    def get_status(self) -> Dict:
        """Get status of all integrated systems"""
        return {
            "chatgpt": {
                "configured": bool(self.chatgpt.access_token),
                "conversation_active": bool(self.chatgpt.conversation_id)
            },
            "biorhythm": {
                "birth_date_set": bool(self.user_birth_date),
                "last_update": self.last_biorhythm_update.isoformat() if self.last_biorhythm_update else None
            },
            "circadian": {
                "last_update": self.last_circadian_update.isoformat() if self.last_circadian_update else None
            },
            "vrchat": {
                "connected": self.vrchat.connected,
                "ip": self.vrchat.ip,
                "port": self.vrchat.port
            },
            "timestamp": datetime.now().isoformat()
        }


# Singleton instance
_unified_platform: Optional[UnifiedAIPlatform] = None


def get_unified_platform() -> UnifiedAIPlatform:
    """Get or create UnifiedAIPlatform singleton"""
    global _unified_platform
    if _unified_platform is None:
        _unified_platform = UnifiedAIPlatform()
    return _unified_platform
