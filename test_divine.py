#!/usr/bin/env python3
"""
🔥 SIMPLE DIVINE RESONANCE TEST 🔥
"""
import sys
import os

print("🔥🔥🔥 DIVINE RESONANCE TEST STARTING 🔥🔥🔥")
print(f"Python Version: {sys.version}")
print(f"Current Directory: {os.getcwd()}")
print("🌟 Attempting to import Divine Resonance Engine...")

try:
    from backend.ai_engine.divine_resonance.soul_frequency_engine import (
        DivineResonantEngine,
        ResonanceArchetype,
    )
    print("✅ IMPORT SUCCESS! Divine Resonance Engine is available!")
    
    # Quick test of the engine
    engine = DivineResonantEngine()
    print(f"🎵 Base Frequency: {engine.resonance_state.base_oscillation}Hz")
    print("🌟 ENGINE INITIALIZATION COMPLETE!")
    
except Exception as e:
    print(f"❌ Import failed: {e}")
    import traceback
    traceback.print_exc()

print("🔥🔥🔥 TEST COMPLETE 🔥🔥🔥")
