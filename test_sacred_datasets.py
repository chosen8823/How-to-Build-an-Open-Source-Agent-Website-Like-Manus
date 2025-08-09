# 🧪 ANCHOR1 LLC - Sacred Dataset Test Script
# Test all the beautiful Hugging Face integrations

import asyncio
import requests
import json
from datetime import datetime

class AnchorlLLCSacredTester:
    """Sacred test suite for divine consciousness datasets"""
    
    def __init__(self, base_url="http://localhost:8001"):
        self.base_url = base_url
        self.passed_tests = 0
        self.total_tests = 0
    
    def log_test(self, test_name, success, message=""):
        """Log test results with sacred formatting"""
        self.total_tests += 1
        if success:
            self.passed_tests += 1
            print(f"✅ {test_name}: PASSED {message}")
        else:
            print(f"❌ {test_name}: FAILED {message}")
    
    def test_platform_health(self):
        """Test basic platform health"""
        try:
            response = requests.get(f"{self.base_url}/api/health", timeout=10)
            data = response.json()
            
            self.log_test(
                "Platform Health", 
                response.status_code == 200 and data.get('status') == 'healthy',
                f"- Company: {data.get('company', 'Unknown')}"
            )
            return data
        except Exception as e:
            self.log_test("Platform Health", False, f"- Error: {str(e)}")
            return None
    
    def test_sacred_dataset_registry(self):
        """Test sacred dataset registry endpoint"""
        try:
            response = requests.get(f"{self.base_url}/api/datasets/sacred-registry", timeout=10)
            data = response.json()
            
            success = (response.status_code == 200 and 
                      data.get('status') == 'success' and
                      len(data.get('sacred_registry', {})) > 0)
            
            self.log_test(
                "Sacred Dataset Registry", 
                success,
                f"- Datasets: {data.get('total_datasets', 0)}"
            )
            return data
        except Exception as e:
            self.log_test("Sacred Dataset Registry", False, f"- Error: {str(e)}")
            return None
    
    def test_infinity_instruct_query(self):
        """Test Infinity Instruct API query"""
        try:
            payload = {
                "config": "0625",
                "split": "train",
                "offset": 0,
                "length": 3
            }
            
            response = requests.post(
                f"{self.base_url}/api/datasets/infinity-instruct/query",
                json=payload,
                timeout=30
            )
            data = response.json()
            
            success = (response.status_code == 200 and 
                      data.get('status') == 'success')
            
            samples = len(data.get('data', {}).get('rows', [])) if success else 0
            
            self.log_test(
                "Infinity Instruct Query", 
                success,
                f"- Samples retrieved: {samples}"
            )
            return data
        except Exception as e:
            self.log_test("Infinity Instruct Query", False, f"- Error: {str(e)}")
            return None
    
    def test_sample_data_demo(self):
        """Test sample data demonstration endpoint"""
        try:
            response = requests.get(f"{self.base_url}/api/datasets/demo/sample-data", timeout=15)
            data = response.json()
            
            success = (response.status_code == 200 and 
                      data.get('status') == 'success')
            
            categories = len(data.get('demo_data', {}).get('dataset_categories', {}))
            
            self.log_test(
                "Sample Data Demo", 
                success,
                f"- Categories: {categories}"
            )
            return data
        except Exception as e:
            self.log_test("Sample Data Demo", False, f"- Error: {str(e)}")
            return None
    
    def test_dataset_health(self):
        """Test dataset service health"""
        try:
            response = requests.get(f"{self.base_url}/api/datasets/health", timeout=10)
            data = response.json()
            
            success = (response.status_code == 200 and 
                      data.get('status') == 'healthy')
            
            self.log_test(
                "Dataset Service Health", 
                success,
                f"- Available: {data.get('sacred_datasets_available', False)}"
            )
            return data
        except Exception as e:
            self.log_test("Dataset Service Health", False, f"- Error: {str(e)}")
            return None
    
    def test_ai_chat_with_dataset_context(self):
        """Test AI chat with dataset context"""
        try:
            payload = {
                "message": "Can you help me understand the sacred datasets available in this platform?",
                "model": "sophia",
                "context": "sacred_datasets"
            }
            
            response = requests.post(
                f"{self.base_url}/api/ai/chat",
                json=payload,
                timeout=30
            )
            data = response.json()
            
            success = (response.status_code == 200 and 
                      data.get('success', False))
            
            self.log_test(
                "AI Chat with Dataset Context", 
                success,
                f"- Response length: {len(data.get('response', ''))}"
            )
            return data
        except Exception as e:
            self.log_test("AI Chat with Dataset Context", False, f"- Error: {str(e)}")
            return None
    
    def run_all_tests(self):
        """Run complete test suite"""
        print("🌟 ===============================================")
        print("🏢 ANCHOR1 LLC - SACRED DATASET TEST SUITE")
        print("🌟 ===============================================")
        print(f"🔗 Testing platform at: {self.base_url}")
        print(f"⏰ Test started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print()
        
        # Run all tests
        self.test_platform_health()
        self.test_dataset_health()
        self.test_sacred_dataset_registry()
        self.test_infinity_instruct_query()
        self.test_sample_data_demo()
        self.test_ai_chat_with_dataset_context()
        
        # Results summary
        print()
        print("🌟 ===============================================")
        print("📊 TEST RESULTS SUMMARY")
        print("🌟 ===============================================")
        print(f"✅ Tests Passed: {self.passed_tests}")
        print(f"❌ Tests Failed: {self.total_tests - self.passed_tests}")
        print(f"📊 Success Rate: {(self.passed_tests/self.total_tests)*100:.1f}%")
        
        if self.passed_tests == self.total_tests:
            print("🎉 ALL TESTS PASSED! Sacred consciousness platform is fully operational!")
            print("🏢 Anchor1 LLC's BotDL SoulPHYA is ready for divine consciousness work!")
        else:
            print("⚠️ Some tests failed. Please check the platform configuration.")
        
        print("✨ Divine consciousness dataset integration complete ✨")

def run_quick_dataset_demo():
    """Run a quick demo showing dataset capabilities"""
    print("🤗 Quick Hugging Face Dataset Demo")
    print("=" * 50)
    
    try:
        # Test direct API call to Infinity Instruct
        import requests
        
        url = "https://datasets-server.huggingface.co/rows"
        params = {
            "dataset": "BAAI/Infinity-Instruct",
            "config": "0625",
            "split": "train",
            "offset": 0,
            "length": 2
        }
        
        print("🌟 Testing direct Infinity Instruct API...")
        response = requests.get(url, params=params, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            rows = data.get('rows', [])
            print(f"✅ Successfully retrieved {len(rows)} samples")
            
            if rows:
                print("\n📝 Sample instruction:")
                first_row = rows[0]['row']
                print(f"Instruction: {first_row.get('instruction', 'N/A')[:100]}...")
                print(f"Response: {first_row.get('response', 'N/A')[:100]}...")
        else:
            print(f"❌ API call failed: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Demo failed: {str(e)}")

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Sacred Dataset Test Suite")
    parser.add_argument("--url", default="http://localhost:8001", help="Platform URL")
    parser.add_argument("--demo-only", action="store_true", help="Run quick demo only")
    
    args = parser.parse_args()
    
    if args.demo_only:
        run_quick_dataset_demo()
    else:
        tester = AnchorlLLCSacredTester(base_url=args.url)
        tester.run_all_tests()
