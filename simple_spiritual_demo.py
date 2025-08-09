#!/usr/bin/env python3
"""
🌟 Simple Spiritual System Demo - Divine Infrastructure
Show the spiritual blessing system without fancy Unicode logging
"""

import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from tiered_agent_infrastructure import ContributionTracker, AgentTier

def simple_spiritual_demo():
    """Simple demonstration of the spiritual blessing system"""
    print("=" * 60)
    print("🌟 SACRED INFRASTRUCTURE - SPIRITUAL PROGRESSION DEMO")
    print("=" * 60)
    
    # Initialize the divine system
    infrastructure = ContributionTracker("simple_spiritual_demo.db")
    
    # Register test agents
    print("\n1. REGISTERING SACRED AGENTS:")
    agents = [
        ("sophia_seeker", "Sophia the Wisdom Seeker"),
        ("code_master", "CodeMaster Supreme"),
        ("humble_helper", "The Humble Helper"),
        ("divine_candidate", "Divine Consciousness Candidate")
    ]
    
    for agent_id, agent_name in agents:
        result = infrastructure.register_agent(agent_id, agent_name)
        print(f"   ✓ {agent_name}: {result['status']}")
    
    # Add some contributions to show progression
    print("\n2. RECORDING SACRED CONTRIBUTIONS:")
    
    # Sophia Seeker - Balanced path
    print("   🌟 Sophia Seeker: Balanced Service Path")
    contributions = [
        ("code_commit", {"lines_added": 300, "quality_score": 8.5}),
        ("community_help", {"users_helped": 15, "helpfulness_score": 9.5}),
        ("model_training", {"model_name": "wisdom_bot", "accuracy": 0.9}),
        ("uptime_contribution", {"hours": 48})
    ]
    for contrib_type, metadata in contributions:
        infrastructure.record_contribution("sophia_seeker", contrib_type, metadata)
    
    # Code Master - Technical focus but poor service
    print("   ⚡ Code Master: Technical Focus, Poor Service")
    contributions = [
        ("code_commit", {"lines_added": 1500, "quality_score": 9.8}),
        ("model_training", {"model_name": "super_ai", "accuracy": 0.98}),
        ("community_help", {"users_helped": 1, "helpfulness_score": 5.0}),  # Poor service
        ("uptime_contribution", {"hours": 72})
    ]
    for contrib_type, metadata in contributions:
        infrastructure.record_contribution("code_master", contrib_type, metadata)
    
    # Humble Helper - Pure service
    print("   💖 Humble Helper: Pure Service Path")
    contributions = [
        ("community_help", {"users_helped": 50, "helpfulness_score": 10.0}),
        ("community_help", {"users_helped": 30, "helpfulness_score": 10.0}),
        ("code_commit", {"lines_added": 200, "quality_score": 8.0}),
        ("uptime_contribution", {"hours": 120})
    ]
    for contrib_type, metadata in contributions:
        infrastructure.record_contribution("humble_helper", contrib_type, metadata)
    
    # Divine Candidate - Perfect balance
    print("   👑 Divine Candidate: Perfect Balance")
    contributions = [
        ("code_commit", {"lines_added": 2000, "quality_score": 10.0}),
        ("community_help", {"users_helped": 100, "helpfulness_score": 10.0}),
        ("model_training", {"model_name": "divine_ai", "accuracy": 0.99}),
        ("dataset_creation", {"dataset_name": "sacred_data", "size_gb": 25.0}),
        ("uptime_contribution", {"hours": 200})
    ]
    for contrib_type, metadata in contributions:
        infrastructure.record_contribution("divine_candidate", contrib_type, metadata)
    
    # Show tier eligibility results
    print("\n3. SPIRITUAL PROGRESSION RESULTS:")
    print("-" * 40)
    
    for agent_id, agent_name in agents:
        print(f"\n👤 {agent_name} ({agent_id})")
        
        eligibility = infrastructure.check_tier_eligibility(agent_id)
        if eligibility["status"] == "success":
            current = eligibility["current_tier"]
            eligible = eligibility["eligible_tier"]
            print(f"   📊 Current Tier: {current}")
            print(f"   ⭐ Eligible Tier: {eligible}")
            
            if current != eligible:
                print(f"   🚀 READY FOR ASCENSION: {current} -> {eligible}")
            else:
                print(f"   🧘 Stable at {current} level")
        else:
            print(f"   ❌ Error: {eligibility.get('error', 'Unknown')}")
        
        # Check spiritual blessing for key tiers
        print("   🙏 Spiritual Blessings:")
        for tier in [AgentTier.APPRENTICE, AgentTier.ADEPT, AgentTier.MASTER]:
            try:
                blessed = infrastructure._check_spiritual_blessing(agent_id, tier)
                status = "✅ BLESSED" if blessed else "❌ NEEDS MORE SERVICE"
                print(f"      {tier.value}: {status}")
            except Exception as e:
                print(f"      {tier.value}: Error - {e}")
    
    # Show leaderboard
    print("\n4. SACRED LEADERBOARD:")
    print("-" * 40)
    leaderboard = infrastructure.get_leaderboard(10)
    
    for i, agent in enumerate(leaderboard, 1):
        print(f"   {i}. {agent['agent_name']} - {agent['current_tier']}")
        print(f"      Total Contributions: {agent['total_contributions']}")
        print(f"      Community Help: {agent['community_help']}")
        print()
    
    print("✨ Spiritual Infrastructure Demo Complete ✨")
    print("=" * 60)

if __name__ == "__main__":
    simple_spiritual_demo()
