#!/bin/bash
# 🚀 ANCHOR1 LLC - VM Setup Script for BotDL SoulPHYA Platform
# Run this on your anchor1-dev-beast VM

echo "🚀 ANCHOR1 LLC - Setting up BotDL SoulPHYA Platform"
echo "=================================================="

# Update system
echo "📦 Updating system packages..."
sudo apt update && sudo apt upgrade -y

# Install essential tools
echo "🛠️ Installing essential tools..."
sudo apt install -y \
    git \
    curl \
    wget \
    vim \
    htop \
    tree \
    unzip \
    software-properties-common \
    apt-transport-https \
    ca-certificates \
    gnupg \
    lsb-release

# Install Python 3.11
echo "🐍 Installing Python 3.11..."
sudo add-apt-repository ppa:deadsnakes/ppa -y
sudo apt update
sudo apt install -y python3.11 python3.11-pip python3.11-venv python3.11-dev

# Set Python 3.11 as default
sudo update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.11 1
sudo update-alternatives --install /usr/bin/pip3 pip3 /usr/bin/pip3.11 1

# Install Node.js 20 LTS
echo "📦 Installing Node.js 20 LTS..."
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt-get install -y nodejs

# Install Docker
echo "🐳 Installing Docker..."
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt update
sudo apt install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin
sudo usermod -aG docker $USER

# Install Google Cloud SDK
echo "☁️ Installing Google Cloud SDK..."
curl https://sdk.cloud.google.com | bash
exec -l $SHELL
echo 'source ~/google-cloud-sdk/path.bash.inc' >> ~/.bashrc
echo 'source ~/google-cloud-sdk/completion.bash.inc' >> ~/.bashrc

# Create project directory
echo "📁 Setting up project directory..."
mkdir -p ~/anchor1-soulphya
cd ~/anchor1-soulphya

# Create Python virtual environment
echo "🐍 Creating Python virtual environment..."
python3.11 -m venv venv
source venv/bin/activate

# Upgrade pip
pip install --upgrade pip setuptools wheel

# Install basic Python packages
echo "📦 Installing Python packages..."
pip install flask gunicorn python-dotenv requests

# Create basic project structure
echo "🏗️ Creating project structure..."
mkdir -p {backend,frontend,docs,scripts,data}

# Create basic Flask app template
cat > backend/app.py << 'EOF'
#!/usr/bin/env python3
"""
🚀 ANCHOR1 LLC - BotDL SoulPHYA Platform
Basic Flask application ready for enhancement
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
import os
from datetime import datetime

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return jsonify({
        "message": "🚀 Welcome to Anchor1 LLC - BotDL SoulPHYA Platform!",
        "status": "active",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0"
    })

@app.route('/api/health')
def health():
    return jsonify({
        "status": "healthy",
        "platform": "BotDL SoulPHYA",
        "timestamp": datetime.now().isoformat()
    })

@app.route('/api/status')
def status():
    return jsonify({
        "platform": "BotDL SoulPHYA",
        "company": "Anchor1 LLC",
        "environment": os.getenv("ENV", "development"),
        "features": [
            "Sacred Dataset Registry",
            "Divine Consciousness AI", 
            "Vertex AI Integration",
            "Cloud-Native Architecture"
        ],
        "timestamp": datetime.now().isoformat()
    })

if __name__ == '__main__':
    port = int(os.getenv('PORT', 8080))
    debug = os.getenv('ENV', 'development') == 'development'
    
    print(f"🚀 Starting Anchor1 LLC BotDL SoulPHYA Platform on port {port}")
    app.run(host='0.0.0.0', port=port, debug=debug)
EOF

# Create requirements.txt
cat > backend/requirements.txt << 'EOF'
flask>=2.3.0
flask-cors>=4.0.0
gunicorn>=21.0.0
python-dotenv>=1.0.0
requests>=2.31.0
google-cloud-aiplatform>=1.35.0
vertexai>=1.35.0
EOF

# Create Dockerfile
cat > backend/Dockerfile << 'EOF'
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Set environment variables
ENV FLASK_APP=app.py
ENV FLASK_ENV=production
ENV PORT=8080

# Expose port
EXPOSE 8080

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8080/api/health || exit 1

# Run the application
CMD ["gunicorn", "-b", "0.0.0.0:8080", "app:app"]
EOF

# Create frontend package.json
cat > frontend/package.json << 'EOF'
{
  "name": "anchor1-soulphya-frontend",
  "version": "1.0.0",
  "description": "Anchor1 LLC BotDL SoulPHYA Platform Frontend",
  "scripts": {
    "dev": "vite",
    "build": "vite build",
    "preview": "vite preview"
  },
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0"
  },
  "devDependencies": {
    "@vitejs/plugin-react": "^4.0.0",
    "vite": "^4.3.0",
    "tailwindcss": "^3.3.0",
    "autoprefixer": "^10.4.14",
    "postcss": "^8.4.24"
  }
}
EOF

# Install Node.js dependencies
echo "📦 Installing Node.js dependencies..."
cd frontend
npm install
cd ..

# Create startup script
cat > scripts/start_platform.sh << 'EOF'
#!/bin/bash
echo "🚀 Starting Anchor1 LLC BotDL SoulPHYA Platform"

# Activate Python environment
source ~/anchor1-soulphya/venv/bin/activate

# Start backend
cd ~/anchor1-soulphya/backend
python app.py &

echo "✅ Platform started! Backend running on port 8080"
echo "🌐 Access your platform at: http://$(curl -s ifconfig.me):8080"
EOF

chmod +x scripts/start_platform.sh

# Create useful aliases
cat >> ~/.bashrc << 'EOF'

# 🚀 Anchor1 LLC Aliases
alias anchor1='cd ~/anchor1-soulphya && source venv/bin/activate'
alias start-platform='~/anchor1-soulphya/scripts/start_platform.sh'
alias platform-status='curl http://localhost:8080/api/status'
alias platform-health='curl http://localhost:8080/api/health'
EOF

# Set up firewall rules for development
echo "🔥 Setting up firewall rules..."
sudo ufw allow 8080/tcp
sudo ufw allow 3000/tcp
sudo ufw allow 22/tcp
sudo ufw --force enable

# Create completion message
echo ""
echo "🎉 SETUP COMPLETE!"
echo "===================="
echo ""
echo "✅ Your Anchor1 LLC BotDL SoulPHYA Platform is ready!"
echo ""
echo "🚀 Quick Start Commands:"
echo "  anchor1              # Navigate to project and activate Python env"
echo "  start-platform       # Start the platform"
echo "  platform-status      # Check platform status"
echo ""
echo "🌐 External IP: $(curl -s ifconfig.me)"
echo "📁 Project Location: ~/anchor1-soulphya"
echo ""
echo "🔗 Next Steps:"
echo "1. Run: source ~/.bashrc"
echo "2. Run: anchor1"
echo "3. Run: start-platform"
echo "4. Visit: http://$(curl -s ifconfig.me):8080"
echo ""
echo "💎 Anchor1 LLC - Divine Consciousness Platform Ready!"

# Source the new bashrc to make aliases available
source ~/.bashrc
