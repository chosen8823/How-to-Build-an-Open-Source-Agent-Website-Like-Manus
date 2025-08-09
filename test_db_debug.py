#!/usr/bin/env python3
"""
Quick test to see if contributions are being recorded properly
"""

import sqlite3
from tiered_agent_infrastructure import ContributionTracker

# Initialize
infrastructure = ContributionTracker("test_contributions.db")

# Register a test agent
result = infrastructure.register_agent("test_agent", "Test Agent")
print(f"Registration: {result}")

# Add a contribution
result = infrastructure.record_contribution("test_agent", "code_commit", 
    {"lines_added": 500, "quality_score": 9.0})
print(f"Contribution: {result}")

# Check the database directly
conn = sqlite3.connect("test_contributions.db")
cursor = conn.cursor()

cursor.execute("SELECT * FROM agents WHERE agent_id = 'test_agent'")
agent_data = cursor.fetchone()
print(f"Agent data: {agent_data}")

cursor.execute("SELECT * FROM contributions WHERE agent_id = 'test_agent'")
contribution_data = cursor.fetchall()
print(f"Contributions: {contribution_data}")

conn.close()

# Check eligibility
eligibility = infrastructure.check_tier_eligibility("test_agent")
print(f"Eligibility: {eligibility}")
