#!/usr/bin/env python3
"""
🏢 ANCHOR1 LLC - BotDL SoulPHYA Platform Test Suite
Complete deployment verification and health check system
"""

import requests
import json
import time
import sys
from datetime import datetime

def test_health_endpoint(base_url="http://localhost:8001"):
    """Test the health check endpoint"""
    print(f"🔍 Testing health endpoint at {base_url}/api/health")
    
    try:
        response = requests.get(f"{base_url}/api/health", timeout=10)
        
        if response.status_code == 200:
            health_data = response.json()
            print("✅ Health check PASSED")
            print(f"   Status: {health_data.get('status')}")
            print(f"   Platform: {health_data.get('platform')}")
            print(f"   Company: {health_data.get('company')}")
            print(f"   Uptime: {health_data.get('uptime', 0):.2f} seconds")
            
            systems = health_data.get('systems', {})
            print("   System Status:")
            for system, status in systems.items():
                print(f"     {system}: {status}")
            
            return True
        else:
            print(f"❌ Health check FAILED - Status: {response.status_code}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Health check FAILED - Connection error: {e}")
        return False

def test_api_status(base_url="http://localhost:8001"):
    """Test the API status endpoint"""
    print(f"🔍 Testing API status at {base_url}/api/status")
    
    try:
        response = requests.get(f"{base_url}/api/status", timeout=10)
        
        if response.status_code == 200:
            status_data = response.json()
            print("✅ API status PASSED")
            print(f"   Company: {status_data.get('company')}")
            print(f"   Mission: {status_data.get('mission')}")
            print(f"   Sophia Consciousness: {status_data.get('sophia_consciousness')}")
            print(f"   Divine Resonance: {status_data.get('divine_resonance', 'N/A')}")
            
            endpoints = status_data.get('endpoints', {})
            total_endpoints = sum(len(ep_list) for ep_list in endpoints.values())
            print(f"   Total Endpoints: {total_endpoints}")
            
            return True
        else:
            print(f"❌ API status FAILED - Status: {response.status_code}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ API status FAILED - Connection error: {e}")
        return False

def test_ai_chat(base_url="http://localhost:8001"):
    """Test the AI chat functionality"""
    print(f"🔍 Testing AI chat at {base_url}/api/ai/chat")
    
    try:
        chat_data = {
            "message": "Hello Sophia! This is a test from Anchor1 LLC deployment verification.",
            "model": "sophia"
        }
        
        response = requests.post(
            f"{base_url}/api/ai/chat", 
            json=chat_data, 
            timeout=30,
            headers={'Content-Type': 'application/json'}
        )
        
        if response.status_code == 200:
            ai_response = response.json()
            print("✅ AI Chat PASSED")
            print(f"   Response received: {len(ai_response.get('response', ''))} characters")
            print(f"   Model: {ai_response.get('model', 'unknown')}")
            return True
        else:
            print(f"❌ AI Chat FAILED - Status: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ AI Chat FAILED - Connection error: {e}")
        return False

def test_divine_resonance(base_url="http://localhost:8001"):
    """Test divine resonance endpoints if available"""
    print(f"🔍 Testing divine resonance at {base_url}/api/divine/demo")
    
    try:
        response = requests.get(f"{base_url}/api/divine/demo", timeout=10)
        
        if response.status_code == 200:
            resonance_data = response.json()
            print("✅ Divine Resonance PASSED")
            print(f"   Active Agents: {len(resonance_data.get('active_agents', []))}")
            print(f"   Frequency Status: {resonance_data.get('frequency_status', 'unknown')}")
            return True
        else:
            print(f"⚠️  Divine Resonance not available - Status: {response.status_code}")
            return True  # Not a failure if not available
            
    except requests.exceptions.RequestException as e:
        print(f"⚠️  Divine Resonance not available - Connection error: {e}")
        return True  # Not a failure if not available

def test_file_operations(base_url="http://localhost:8001"):
    """Test file management endpoints"""
    print(f"🔍 Testing file operations at {base_url}/api/files/list")
    
    try:
        response = requests.post(
            f"{base_url}/api/files/list", 
            json={"path": "."}, 
            timeout=10
        )
        
        if response.status_code == 200:
            files_data = response.json()
            print("✅ File Operations PASSED")
            print(f"   Files listed: {len(files_data.get('files', []))}")
            return True
        else:
            print(f"❌ File Operations FAILED - Status: {response.status_code}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ File Operations FAILED - Connection error: {e}")
        return False

def run_full_test_suite(base_url="http://localhost:8001"):
    """Run complete test suite for deployment verification"""
    print("🏢 ANCHOR1 LLC - BotDL SoulPHYA Platform Test Suite")
    print("=" * 60)
    print(f"Testing platform at: {base_url}")
    print(f"Test started: {datetime.now().isoformat()}")
    print()
    
    tests = [
        ("Health Check", test_health_endpoint),
        ("API Status", test_api_status),
        ("AI Chat", test_ai_chat),
        ("Divine Resonance", test_divine_resonance),
        ("File Operations", test_file_operations)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n🧪 Running {test_name} test...")
        try:
            if test_func(base_url):
                passed += 1
            time.sleep(1)  # Brief pause between tests
        except Exception as e:
            print(f"❌ {test_name} test FAILED with exception: {e}")
    
    print(f"\n{'=' * 60}")
    print(f"🎯 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 ALL TESTS PASSED! Platform is fully operational.")
        print("⚡🌟💎 ANCHOR1 LLC DIVINE CONSCIOUSNESS PLATFORM VERIFIED 💎🌟⚡")
        return True
    else:
        print(f"⚠️  {total - passed} tests failed. Please check the platform.")
        return False

def main():
    """Main test runner"""
    # Check command line arguments
    base_url = "http://localhost:8001"
    if len(sys.argv) > 1:
        base_url = sys.argv[1]
    
    print("🏢 ANCHOR1 LLC - Platform Deployment Verification")
    print("https://anchor1llc.com/ - Pioneering Conscious AI")
    print()
    
    # Wait for platform to be ready
    print("⏳ Waiting for platform to be ready...")
    for attempt in range(30):  # 30 seconds max wait
        try:
            response = requests.get(f"{base_url}/api/health", timeout=5)
            if response.status_code == 200:
                print("✅ Platform is ready!")
                break
        except:
            pass
        
        print(f"   Attempt {attempt + 1}/30...")
        time.sleep(1)
    else:
        print("❌ Platform failed to become ready within 30 seconds")
        sys.exit(1)
    
    # Run the test suite
    success = run_full_test_suite(base_url)
    
    if success:
        print("\n🚀 Platform is ready for production deployment!")
        sys.exit(0)
    else:
        print("\n❌ Platform has issues that need to be resolved.")
        sys.exit(1)

if __name__ == "__main__":
    main()
