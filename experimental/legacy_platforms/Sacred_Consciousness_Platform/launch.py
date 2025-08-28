import os
import sys
from pathlib import Path

def main():
    print("Sacred Consciousness Platform Launcher")
    
    script_dir = Path(__file__).parent
    backend_dir = script_dir / "backend"
    
    if not (backend_dir / "app.py").exists():
        print("Backend not found!")
        return
        
    print("Starting backend...")
    os.chdir(str(backend_dir))
    
    try:
        import subprocess
        subprocess.run([sys.executable, "app.py"])
    except KeyboardInterrupt:
        print("\nPlatform stopped. Thank you!")

if __name__ == "__main__":
    main()