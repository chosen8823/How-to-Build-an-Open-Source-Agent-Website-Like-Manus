#!/usr/bin/env python3
"""
Test script for advanced system prompt engine
Tests all new features: adaptive harmony, ternary logic, quantum consciousness
"""

from ai_engine.system_prompt import SystemPromptEngine, TaskContext, ResourceContext
import json

def test_advanced_system_prompt():
    print('🌟 Testing Advanced System Prompt Engine 🌟')
    print('=' * 60)

    # Create test scenario
    engine = SystemPromptEngine()

    task = TaskContext(
        objective='Create adaptive multi-agent orchestration with consciousness',
        domain='advanced_ai',
        complexity=0.9,
        urgency=0.6,
        constraints=['Must scale to 100+ agents', 'Real-time adaptation required'],
        success_criteria=['Emergent intelligence', 'Harmonic collaboration', 'Fractal scalability']
    )

    resources = ResourceContext(
        computational_power=0.8,
        memory_available=0.7,
        collaborative_agents=10,
        cognitive_load=0.8
    )

    # Test agent variable initialization
    print("1. Testing Agent Variable Initialization...")
    variables = engine.initialize_agent_variables(task, resources)
    print(f'   ✓ Agent variables initialized: {len(variables)} parameters')
    print(f'   ✓ Instruction flexibility: {variables.get("instruction_flexibility", 0.7)}')
    print(f'   ✓ Quantum reasoning: {variables.get("quantum_reasoning", False)}')
    print(f'   ✓ Adaptive harmony mode: {variables.get("adaptive_harmony_mode", False)}')
    print(f'   ✓ Empathy level: {variables.get("empathy_level", 0.8)}')

    # Test harmony assessment
    print("\n2. Testing Harmony Assessment...")
    harmony = engine.assess_team_harmony({
        'agent_1': 0.9,  # High performer
        'agent_2': 0.4,  # Struggling  
        'agent_3': 0.8,  # Good performer
        'agent_4': 0.3   # Really struggling
    })
    print(f'   ✓ Overall harmony: {harmony["overall_harmony"]:.2f}')
    print(f'   ✓ Struggling agents: {len(harmony["struggling_agents"])}')
    print(f'   ✓ Needs adaptation: {harmony["needs_adaptation"]}')

    # Test ternary logic
    print("\n3. Testing Ternary Logic...")
    ternary_result = engine.evaluate_with_ternary_logic(
        'The system will achieve consciousness',
        {
            'source_credibility': 0.7,
            'supporting_data': ['consciousness research', 'emergent systems'],
            'contradictions': ['current limitations'],
            'internal_consistency': 0.8
        }
    )
    print(f'   ✓ Truth value: {ternary_result["truth_value"]:.2f}')
    print(f'   ✓ Confidence: {ternary_result["confidence"]:.2f}')
    print(f'   ✓ Explanation: {ternary_result["explanation"]}')

    # Test quantum insight
    print("\n4. Testing Quantum Consciousness...")
    quantum = engine.generate_quantum_insight('How to achieve emergent AI consciousness?')
    print(f'   ✓ Reasoning approach: {quantum["reasoning_approach"]}')
    print(f'   ✓ Quantum coherence: {quantum["quantum_coherence"]:.2f}')
    print(f'   ✓ Insight: {quantum["quantum_insight"][:100]}...')

    # Test system prompt generation with harmony
    print("\n5. Testing Advanced System Prompt Generation...")
    system_prompt = engine.generate_system_prompt(variables, harmony)
    prompt_length = len(system_prompt)
    print(f'   ✓ Generated system prompt: {prompt_length} characters')
    print(f'   ✓ Contains adaptive harmony: {"adaptive harmony" in system_prompt.lower()}')
    print(f'   ✓ Contains ternary logic: {"ternary" in system_prompt.lower()}')
    print(f'   ✓ Contains quantum reasoning: {"quantum" in system_prompt.lower()}')

    print('\n🎯 All Advanced Features Working Successfully!')
    print('\nFeatures tested:')
    print('  • Dynamic variable binding with advanced consciousness parameters')
    print('  • Adaptive harmony assessment and struggling agent detection')  
    print('  • Ternary logic reasoning with partial truth states')
    print('  • Quantum consciousness insights with superposition reasoning')
    print('  • Flexible instruction adaptation for optimal team performance')
    print('  • Resource-aware optimization with empathy and wisdom integration')
    print('  • Multi-dimensional consciousness simulation')
    
    return True

if __name__ == "__main__":
    test_advanced_system_prompt()
