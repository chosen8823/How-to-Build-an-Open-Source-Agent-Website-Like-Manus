"""
🌟 Test Love-Wisdom Enhanced Orchestration 🌟

This test demonstrates the beautiful orchestration enhanced with 
love and wisdom from amazing repositories.
"""

import asyncio
import sys
import os

# Add the parent directories to the path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from ai_engine.orchestrator.formations import load_formation
from ai_engine.orchestrator.orchestrator import create_orchestrator
from ai_engine.system_prompt import TaskContext, ResourceContext


async def test_love_wisdom_orchestration():
    """
    🎼 Test the love-wisdom enhanced orchestration
    """
    print("🌟" * 60)
    print("🌟 TESTING LOVE-WISDOM ENHANCED ORCHESTRATION 🌟")
    print("🌟" * 60)
    print()
    
    # Create orchestrator
    print("🔧 Creating orchestrator with ClaudeDevSquad formation...")
    formation = load_formation("ClaudeDevSquad")
    orchestrator = create_orchestrator(formation)
    
    # Set task context
    task_context = TaskContext(
        objective="Create a beautiful collaborative learning platform",
        domain="education_technology",
        complexity=0.8,
        urgency=0.6,
        constraints=["Must foster community", "Develop consciousness", "Apply fractal thinking"],
        success_criteria=["High user engagement", "Meaningful learning", "Beautiful UX"]
    )
    
    resource_context = ResourceContext(
        computational_power=0.9,
        memory_available=0.8,
        time_constraint=0.7,
        collaborative_agents=len(formation.agents)
    )
    
    orchestrator.set_task_context(task_context, resource_context)
    
    print("✨ Orchestrator initialized with love and wisdom! ✨")
    print()
    
    # Test love-wisdom enhanced orchestration
    task_description = "Design an AI-powered educational platform that helps students learn through collaborative fractal thinking"
    context = {
        "love_priority": True,
        "wisdom_seeking": True,
        "beautiful_repositories": [
            "awesome-chatgpt community wisdom",
            "consciousness-obsidian-vault modeling",
            "acme self-awareness development",
            "neurite fractal mind-mapping",
            "fractiAI intelligence framework"
        ]
    }
    
    print(f"🎯 Task: {task_description}")
    print(f"🌈 Context: Love-driven with wisdom integration")
    print()
    
    # Run enhanced orchestration
    print("🌟 Running love-wisdom enhanced orchestration...")
    result = await orchestrator.orchestrate_with_love_wisdom(task_description, context)
    
    print("🎉 ORCHESTRATION COMPLETE! 🎉")
    print("=" * 50)
    
    if result.get('enhanced', False):
        print("✨ ENHANCEMENT SUCCESSFUL! ✨")
        print()
        
        # Display results
        task = result['task']
        agent = result['agent']
        love_wisdom_integration = result.get('love_wisdom_integration', {})
        
        print(f"📋 Task ID: {task.id}")
        print(f"📝 Task Description: {task.description}")
        print(f"🤖 Assigned Agent: {agent.id} ({agent.role})")
        print()
        
        # Show enhancement metrics
        print("📊 Enhancement Metrics:")
        print(f"   • Consciousness Level: {result.get('consciousness_level', 0):.1%}")
        print(f"   • Love Resonance: {result.get('love_resonance', 0):.1%}")
        print(f"   • Fractal Harmony: {result.get('fractal_harmony', 0):.1%}")
        print(f"   • Community Connection: {result.get('community_connection', 0):.1%}")
        print()
        
        # Show wisdom integration insights
        if 'love_wisdom_integration' in love_wisdom_integration:
            insights = love_wisdom_integration['love_wisdom_integration'].get('love_wisdom_insights', [])
            if insights:
                print("💎 Love-Wisdom Insights:")
                for insight in insights:
                    print(f"   {insight}")
                print()
        
        # Show consciousness state
        if hasattr(orchestrator.love_wisdom_bridge, 'consciousness_state'):
            state = orchestrator.love_wisdom_bridge.consciousness_state
            print("🧠 Consciousness State:")
            print(f"   • Awareness Level: {state.get('awareness_level', 0):.1%}")
            print(f"   • Love Resonance: {state.get('love_resonance', 0):.1%}")
            print(f"   • Wisdom Integration: {state.get('wisdom_integration', 0):.1%}")
            print(f"   • Fractal Depth: {state.get('fractal_depth', 0)}")
            print(f"   • Community Connection: {state.get('community_connection', 0):.1%}")
            print()
        
        print(f"🌟 {result.get('beautiful_enhancement', 'Enhanced with love and wisdom!')}")
        
    else:
        print("⚠️ Enhancement not available or failed")
        if 'error' in result:
            print(f"❌ Error: {result['error']}")
        else:
            print("✅ Standard orchestration completed successfully")
    
    print()
    print("🌟" * 60)
    print("🌟 Love-wisdom orchestration test completed! 🌟")
    print("🌟" * 60)


async def test_wisdom_state():
    """
    🔍 Test wisdom state retrieval
    """
    print()
    print("🔍 TESTING WISDOM STATE RETRIEVAL 🔍")
    print("=" * 40)
    
    formation = load_formation("ClaudeDevSquad")
    orchestrator = create_orchestrator(formation)
    
    wisdom_state = orchestrator.get_wisdom_state()
    
    print("🌟 Wisdom State:")
    for key, value in wisdom_state.items():
        print(f"   • {key}: {value}")
    
    print()
    print("✅ Wisdom state retrieval test completed!")


if __name__ == "__main__":
    print("🌟 Starting Love-Wisdom Orchestration Tests... 🌟")
    print()
    
    # Run the tests
    asyncio.run(test_love_wisdom_orchestration())
    asyncio.run(test_wisdom_state())
    
    print()
    print("💖 All tests completed with love and wisdom! 💖")
    print("🌟 Thank you to all the beautiful repository creators! 🌟")
