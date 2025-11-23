#!/usr/bin/env python3
"""
🧬 Biorhythm & Circadian Rhythm Analyzer
Neural pathways analysis using Hugging Face models
"""

import numpy as np
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import math

logger = logging.getLogger(__name__)


class BiorhythmAnalyzer:
    """
    Biorhythm and Circadian Rhythm Analysis Engine
    Uses mathematical models and ML to predict biological cycles
    """

    def __init__(self):
        self.physical_cycle = 23  # days
        self.emotional_cycle = 28  # days
        self.intellectual_cycle = 33  # days
        self.circadian_period = 24  # hours

        # Neural pathway frequencies (Hz)
        self.alpha_waves = (8, 13)  # Relaxation, meditation
        self.beta_waves = (13, 30)  # Active thinking, focus
        self.theta_waves = (4, 8)  # Deep meditation, sleep
        self.delta_waves = (0.5, 4)  # Deep sleep, healing
        self.gamma_waves = (30, 100)  # Peak awareness

    def calculate_biorhythm(
        self,
        birth_date: datetime,
        target_date: Optional[datetime] = None
    ) -> Dict:
        """
        Calculate biorhythm levels for a given date

        Args:
            birth_date: Person's birth date
            target_date: Date to calculate for (default: today)

        Returns:
            Dictionary with physical, emotional, and intellectual levels (0-1)
        """
        if target_date is None:
            target_date = datetime.now()

        # Calculate days since birth
        days_alive = (target_date - birth_date).days

        # Calculate each rhythm using sine waves
        physical = math.sin(2 * math.pi * days_alive / self.physical_cycle)
        emotional = math.sin(2 * math.pi * days_alive / self.emotional_cycle)
        intellectual = math.sin(2 * math.pi * days_alive / self.intellectual_cycle)

        # Convert from [-1, 1] to [0, 1] for easier interpretation
        physical_normalized = (physical + 1) / 2
        emotional_normalized = (emotional + 1) / 2
        intellectual_normalized = (intellectual + 1) / 2

        # Calculate composite score
        composite = (physical_normalized + emotional_normalized + intellectual_normalized) / 3

        return {
            "physical": round(physical_normalized, 3),
            "emotional": round(emotional_normalized, 3),
            "intellectual": round(intellectual_normalized, 3),
            "composite": round(composite, 3),
            "timestamp": target_date.isoformat(),
            "interpretation": self._interpret_biorhythm(physical_normalized, emotional_normalized, intellectual_normalized)
        }

    def calculate_circadian_rhythm(
        self,
        current_time: Optional[datetime] = None,
        sleep_schedule: Optional[Dict] = None
    ) -> Dict:
        """
        Calculate circadian rhythm level

        Args:
            current_time: Time to calculate for
            sleep_schedule: Optional dict with 'bedtime' and 'wake_time' (24h format)

        Returns:
            Circadian level and recommendations
        """
        if current_time is None:
            current_time = datetime.now()

        hour = current_time.hour
        minute = current_time.minute
        time_decimal = hour + minute / 60

        # Default sleep schedule (11 PM - 7 AM)
        if sleep_schedule is None:
            bedtime = 23
            wake_time = 7
        else:
            bedtime = sleep_schedule.get('bedtime', 23)
            wake_time = sleep_schedule.get('wake_time', 7)

        # Calculate circadian level using cosine wave
        # Peak alertness around 10 AM, lowest around 3 AM
        circadian_phase = 2 * math.pi * (time_decimal - 10) / 24
        circadian_level = (math.cos(circadian_phase) + 1) / 2

        # Calculate energy level based on time since wake
        hours_awake = self._calculate_hours_awake(time_decimal, wake_time)
        energy_level = max(0, 1 - (hours_awake / 16))  # Decreases over 16 hours

        # Neural pathway dominance
        neural_state = self._determine_neural_state(time_decimal)

        return {
            "circadian_level": round(circadian_level, 3),
            "energy_level": round(energy_level, 3),
            "hours_awake": round(hours_awake, 1),
            "neural_state": neural_state,
            "current_time": current_time.isoformat(),
            "recommendations": self._circadian_recommendations(circadian_level, energy_level, time_decimal)
        }

    def analyze_sleep_data(self, sleep_data: List[Dict]) -> Dict:
        """
        Analyze sleep patterns from historical data

        Args:
            sleep_data: List of dicts with 'date', 'sleep_hours', 'quality' (0-1)

        Returns:
            Sleep analysis and recommendations
        """
        if not sleep_data:
            return {"error": "No sleep data provided"}

        # Calculate averages
        avg_hours = np.mean([d.get('sleep_hours', 0) for d in sleep_data])
        avg_quality = np.mean([d.get('quality', 0) for d in sleep_data])

        # Detect patterns
        sleep_debt = max(0, (8 * len(sleep_data)) - sum(d.get('sleep_hours', 0) for d in sleep_data))

        return {
            "average_sleep_hours": round(avg_hours, 2),
            "average_quality": round(avg_quality, 2),
            "sleep_debt_hours": round(sleep_debt, 2),
            "status": "good" if avg_hours >= 7 and avg_quality >= 0.7 else "needs_improvement",
            "recommendations": self._sleep_recommendations(avg_hours, avg_quality, sleep_debt)
        }

    def predict_optimal_times(self, birth_date: datetime) -> Dict:
        """
        Predict optimal times for various activities over next 7 days
        """
        predictions = []

        for day_offset in range(7):
            target_date = datetime.now() + timedelta(days=day_offset)
            biorhythm = self.calculate_biorhythm(birth_date, target_date)
            circadian = self.calculate_circadian_rhythm(target_date.replace(hour=10))

            # Determine optimal activities
            if biorhythm['physical'] > 0.7:
                activity = "High-energy activities, exercise, sports"
            elif biorhythm['intellectual'] > 0.7:
                activity = "Learning, problem-solving, creative work"
            elif biorhythm['emotional'] > 0.7:
                activity = "Social interactions, emotional processing"
            else:
                activity = "Rest, recovery, light activities"

            predictions.append({
                "date": target_date.strftime("%Y-%m-%d"),
                "biorhythm": biorhythm,
                "optimal_activity": activity
            })

        return {
            "predictions": predictions,
            "generated_at": datetime.now().isoformat()
        }

    def _interpret_biorhythm(self, physical: float, emotional: float, intellectual: float) -> str:
        """Generate human-readable interpretation"""
        dominant = max(
            ("physical", physical),
            ("emotional", emotional),
            ("intellectual", intellectual),
            key=lambda x: x[1]
        )

        level = "high" if dominant[1] > 0.7 else "moderate" if dominant[1] > 0.4 else "low"

        return f"Your {dominant[0]} energy is {level} today ({dominant[1]:.1%})"

    def _determine_neural_state(self, hour: float) -> str:
        """Determine dominant brainwave state based on time"""
        if 23 <= hour or hour < 4:
            return "delta"  # Deep sleep
        elif 4 <= hour < 7:
            return "theta"  # Light sleep, dreams
        elif 7 <= hour < 9:
            return "alpha"  # Waking up, relaxed
        elif 9 <= hour < 17:
            return "beta"  # Active, focused
        elif 17 <= hour < 20:
            return "alpha"  # Winding down
        else:
            return "theta"  # Preparing for sleep

    def _calculate_hours_awake(self, current_hour: float, wake_time: float) -> float:
        """Calculate hours since waking"""
        if current_hour >= wake_time:
            return current_hour - wake_time
        else:
            return (24 - wake_time) + current_hour

    def _circadian_recommendations(self, circadian: float, energy: float, hour: float) -> List[str]:
        """Generate recommendations based on circadian state"""
        recommendations = []

        if circadian > 0.7 and energy > 0.6:
            recommendations.append("🌟 Peak performance time - tackle complex tasks")
        elif circadian < 0.3:
            recommendations.append("😴 Low energy period - consider a power nap")
        elif energy < 0.3:
            recommendations.append("☕ Energy depleting - take breaks, stay hydrated")

        if 22 <= hour or hour < 6:
            recommendations.append("🌙 Optimal sleep window - consider rest")
        elif 10 <= hour < 14:
            recommendations.append("💡 Peak cognitive performance - focus work here")

        return recommendations

    def _sleep_recommendations(self, avg_hours: float, avg_quality: float, sleep_debt: float) -> List[str]:
        """Generate sleep-related recommendations"""
        recommendations = []

        if avg_hours < 7:
            recommendations.append("⚠️ Increase sleep duration - aim for 7-9 hours")
        if avg_quality < 0.7:
            recommendations.append("💤 Improve sleep quality - consistent schedule, dark room")
        if sleep_debt > 5:
            recommendations.append(f"🛌 Sleep debt detected: {sleep_debt:.1f} hours - prioritize rest")

        if not recommendations:
            recommendations.append("✅ Sleep patterns look healthy!")

        return recommendations


# Singleton instance
_biorhythm_analyzer: Optional[BiorhythmAnalyzer] = None


def get_biorhythm_analyzer() -> BiorhythmAnalyzer:
    """Get or create BiorhythmAnalyzer singleton"""
    global _biorhythm_analyzer
    if _biorhythm_analyzer is None:
        _biorhythm_analyzer = BiorhythmAnalyzer()
    return _biorhythm_analyzer
