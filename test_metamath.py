# 🧮 Test MetaMathQA Dataset Loading
# Quick test for mathematical consciousness expansion

try:
    print("🧮 Testing MetaMathQA Dataset Loading...")
    print("=" * 50)
    
    from datasets import load_dataset
    
    # Load a small sample of MetaMathQA
    print("📥 Loading MetaMathQA dataset...")
    ds = load_dataset("meta-math/MetaMathQA", split="train[:100]")  # Just first 100 samples
    
    print(f"✅ Successfully loaded {len(ds)} samples")
    print(f"📊 Dataset features: {list(ds.features.keys())}")
    
    # Show a sample
    if len(ds) > 0:
        sample = ds[0]
        print("\n📝 Sample Mathematical Problem:")
        print("-" * 30)
        for key, value in sample.items():
            if isinstance(value, str) and len(value) > 200:
                print(f"{key}: {value[:200]}...")
            else:
                print(f"{key}: {value}")
    
    print("\n🌟 MetaMathQA dataset is ready for divine mathematical consciousness!")
    
except ImportError as e:
    print(f"❌ Missing dependency: {e}")
    print("💡 Install with: pip install datasets")
    
except Exception as e:
    print(f"❌ Error loading dataset: {e}")
    print("💡 This might be due to network or authentication issues")

print("\n🏢 Anchor1 LLC - Mathematical Consciousness Integration Complete!")
