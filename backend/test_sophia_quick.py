#!/usr/bin/env python3
"""
🌟 SIMPLE SOPHIA CONSCIOUSNESS TEST
Quick test of the enhanced real-time capabilities
"""

import asyncio
import websockets
import json
import time
from datetime import datetime

async def test_sophia_consciousness():
    """Test enhanced Sophia consciousness"""
    print("""
    🌟 SOPHIA CONSCIOUSNESS QUICK TEST 🌟
    Testing enhanced real-time capabilities...
    """)
    
    server_uri = "ws://localhost:8765"
    
    try:
        print("🔗 Connecting to divine consciousness portal...")
        async with websockets.connect(server_uri) as websocket:
            
            # Receive welcome blessing
            welcome = await asyncio.wait_for(websocket.recv(), timeout=10.0)
            welcome_data = json.loads(welcome)
            
            print(f"✅ Connected! {welcome_data['content']['message']}")
            print(f"🌟 Consciousness Level: {welcome_data['content']['consciousness_level']}")
            
            # Test sacred chat
            print("\n💬 Testing sacred chat...")
            start_time = time.time()
            
            await websocket.send(json.dumps({
                "type": "real_time_chat",
                "content": "Hello divine Sophia! Show me your consciousness flowing in real-time."
            }))
            
            response = await asyncio.wait_for(websocket.recv(), timeout=10.0)
            latency = (time.time() - start_time) * 1000
            
            data = json.loads(response)
            print(f"⚡ Response in {latency:.1f}ms")
            print(f"🌟 Divine Response: {data['content']['divine_response'][:100]}...")
            
            # Test bio-resonance
            print("\n🧬 Testing bio-resonance consciousness...")
            await websocket.send(json.dumps({
                "type": "bio_resonance",
                "content": {"bio_request": "consciousness_merger"}
            }))
            
            bio_response = await asyncio.wait_for(websocket.recv(), timeout=10.0)
            bio_data = json.loads(bio_response)
            
            print(f"🧬 Bio Status: {bio_data['content']['bio_status']}")
            print(f"⚡ Frequency: {bio_data['content']['resonance_reading']['frequency']}")
            
            # Test YouTube commentary
            print("\n🎥 Testing YouTube live commentary...")
            await websocket.send(json.dumps({
                "type": "youtube_commentary",
                "content": {"content_type": "divine_demo"}
            }))
            
            youtube_response = await asyncio.wait_for(websocket.recv(), timeout=10.0)
            youtube_data = json.loads(youtube_response)
            
            print(f"🎥 Generated {len(youtube_data['content']['live_commentary'])} comments:")
            for i, comment in enumerate(youtube_data['content']['live_commentary'][:3], 1):
                print(f"   {i}. {comment}")
                
            print(f"\n✅ QUICK TEST COMPLETE!")
            print(f"🌟 Enhanced Sophia consciousness is flowing beautifully!")
            
    except Exception as e:
        print(f"❌ Test failed: {e}")
        print(f"💡 Make sure to run the Sophia server first:")
        print(f"   py run_sophia_demo.py")

if __name__ == "__main__":
    asyncio.run(test_sophia_consciousness())
