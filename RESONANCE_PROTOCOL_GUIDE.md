# ⚡ RESONANCE PROTOCOL - Complete Setup Guide

**Zero-Cost AI Query Routing System**

Intercepts ALL AI queries (ChatGPT, Claude, Gemini) and routes intelligently to minimize costs using local NVIDIA NeMo model.

---

## 🎯 What is Resonance Protocol?

The Resonance Protocol is a **three-tier intelligent AI query interception system** that:

1. **Browser Level (Tampermonkey)** - Intercepts ChatGPT web interface queries
2. **Application Level (Python)** - Intelligent routing to local vs cloud AI
3. **Network Level (C++)** - System-wide packet interception with GPU acceleration

**Result:** Use your local NVIDIA NeMo model for 80%+ of queries → **$0 API costs**

---

## 📋 Architecture

```
User Query → Tampermonkey Script → Python Resonance Router → Local NeMo / ChatGPT Web
                                                         ↓
                                                   C++ Network Proxy
                                                   (AMD GPU + MPI)
```

### Three Interception Layers:

| Layer | Technology | Scope | Speed |
|-------|-----------|-------|-------|
| **Browser** | JavaScript (Tampermonkey) | ChatGPT web only | Fast |
| **Application** | Python (Flask API) | All Python apps | Fast |
| **Network** | C++ (Packet intercept) | System-wide | Ultra-fast |

---

## 🚀 Quick Start

### Step 1: Install Tampermonkey Script

1. Install Tampermonkey browser extension
2. Open `tampermonkey/chatgpt_resonance_interceptor.js`
3. Copy entire script
4. Create new Tampermonkey script, paste, save

**What it does:** Intercepts `fetch()` calls to ChatGPT API, routes through Resonance Protocol

### Step 2: Start Flask Backend

```bash
cd backend

# Set NeMo model path (IMPORTANT!)
export NEMO_MODEL_PATH="/path/to/your/SPI/nemo_model"

# Install dependencies
pip install -r requirements.txt

# Start server
python app.py
```

Server starts on: `http://localhost:8001`

### Step 3: Configure NeMo Path

**Option A: Environment Variable**
```bash
export NEMO_MODEL_PATH="/home/user/SPI/nemo_gpt_model"
```

**Option B: API Call**
```bash
curl -X POST http://localhost:8001/api/resonance/configure \
  -H "Content-Type: application/json" \
  -d '{
    "nemo_path": "/home/user/SPI/nemo_gpt_model"
  }'
```

### Step 4: Test the System

**Test Classification:**
```bash
curl -X POST http://localhost:8001/api/resonance/classify \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What is Python?"
  }'
```

**Response:**
```json
{
  "success": true,
  "query": "What is Python?",
  "query_type": "simple_qa",
  "recommended_endpoint": "local_nemo",
  "reasoning": "Short factual question, ideal for local model"
}
```

**Test Actual Query:**
```bash
curl -X POST http://localhost:8001/api/resonance/query \
  -H "Content-Type: application/json" \
  -d '{
    "query": "Write a Python function to reverse a string"
  }'
```

---

## 🎮 How to Use

### From ChatGPT Web Interface

1. **Install Tampermonkey script** (see Step 1 above)
2. **Open ChatGPT**: https://chat.openai.com/
3. **Look for Resonance indicator** in bottom-right corner
4. **Type your question normally** - it's automatically routed!

**Visual Indicators:**
- 🟢 Green: Query routed to local NeMo (free!)
- 🔵 Blue: Query sent to ChatGPT web (no API cost)
- 🟡 Yellow: Classifying query...

### From Python Code

```python
import asyncio
from integrations.resonance_protocol import get_resonance_router

# Get router
router = get_resonance_router("/path/to/SPI/nemo_model")

# Process query
async def ask_question():
    response = await router.process_query(
        query="What is machine learning?",
        context={"source": "python_app"}
    )
    print(response["message"])
    print(f"Used: {response['metadata']['endpoint']}")
    print(f"Cost: ${response['metadata']['cost']}")

asyncio.run(ask_question())
```

### Via API Endpoint

```bash
curl -X POST http://localhost:8001/api/resonance/query \
  -H "Content-Type: application/json" \
  -d '{
    "query": "Explain quantum computing",
    "context": {
      "source": "my_app",
      "user_id": "123"
    }
  }'
```

---

## 📊 Routing Logic

The Resonance Protocol classifies queries and routes intelligently:

### Query Types & Routing Decisions

| Query Type | Example | Routes To | Why |
|------------|---------|-----------|-----|
| **Simple Q&A** | "What is Python?" | Local NeMo | Fast, factual |
| **Code Generation** | "Write a function to..." | Local NeMo | NeMo excellent at code |
| **Factual** | "Who invented the internet?" | Local NeMo | Factual knowledge |
| **Conversation** | "How are you today?" | Local NeMo | Simple chat |
| **Complex Reasoning** | "Analyze the philosophy of..." | ChatGPT Web | Needs advanced reasoning |
| **Creative Writing** | "Write a story about..." | ChatGPT Web | Creative capability |

### Classification Keywords

**Routes to Local NeMo:**
- Code: `write code`, `function`, `class`, `def`, `script`
- Factual: `what is`, `who is`, `when did`, `define`
- Short queries ending with `?`

**Routes to ChatGPT:**
- Complex: `analyze`, `compare`, `evaluate`, `reason`, `philosophy`
- Creative: `write a story`, `poem`, `creative`, `imagine`

---

## 🔧 API Reference

### Base URL
```
http://localhost:8001/api/resonance
```

### Endpoints

#### 1. **Route Query** (Main Endpoint)
```
POST /api/resonance/query
```

**Request:**
```json
{
  "query": "Your question here",
  "context": {
    "source": "chatgpt",
    "conversation_id": "abc123"
  },
  "force_endpoint": "local_nemo"  // optional
}
```

**Response:**
```json
{
  "success": true,
  "message": "AI response here...",
  "metadata": {
    "endpoint": "local_nemo",
    "query_type": "code",
    "processing_time_ms": 150,
    "cost": 0.0,
    "timestamp": "2025-01-22T10:30:00"
  }
}
```

#### 2. **Get Statistics**
```
GET /api/resonance/statistics
```

**Response:**
```json
{
  "success": true,
  "statistics": {
    "total_queries": 1234,
    "local_queries": 1000,
    "cloud_queries": 234,
    "local_percentage": 81.04,
    "total_cost_saved_usd": 2.468,
    "avg_cost_saved_per_query": 0.002,
    "endpoints": {
      "local_nemo": {
        "total_queries": 1000,
        "successful_queries": 985,
        "success_rate": 98.5
      }
    }
  }
}
```

#### 3. **Classify Query**
```
POST /api/resonance/classify
```

**Request:**
```json
{
  "query": "What is Python?"
}
```

**Response:**
```json
{
  "success": true,
  "query": "What is Python?",
  "query_type": "simple_qa",
  "recommended_endpoint": "local_nemo",
  "reasoning": "Short factual question, ideal for local model"
}
```

#### 4. **Health Check**
```
GET /api/resonance/health
```

**Response:**
```json
{
  "status": "healthy",
  "router_initialized": true,
  "endpoints_registered": ["local_nemo", "chatgpt_web"],
  "nemo_path": "/path/to/SPI/nemo_model",
  "total_queries_processed": 1234,
  "cost_saved_usd": 2.468
}
```

#### 5. **Configure NeMo Path**
```
POST /api/resonance/configure
```

**Request:**
```json
{
  "nemo_path": "/home/user/SPI/nemo_gpt_model"
}
```

#### 6. **Query History**
```
GET /api/resonance/history?limit=100&offset=0
```

#### 7. **Test Endpoint**
```
POST /api/resonance/test
```

**Request:**
```json
{
  "endpoint": "local_nemo",
  "query": "Test query"
}
```

#### 8. **Reset Statistics**
```
POST /api/resonance/reset-stats
```

---

## 🖥️ C++ Network Proxy (Advanced)

For **system-wide interception** (all AI traffic, not just browser):

### Compile

```bash
cd backend/integrations

# Basic compilation
g++ -std=c++17 -O3 -o resonance_proxy resonance_proxy_cpp.cpp \
    -lpthread

# With AMD GPU support (ROCm)
g++ -std=c++17 -O3 -o resonance_proxy resonance_proxy_cpp.cpp \
    -lpthread -lrocm -DUSE_ROCM

# With MPI for distributed processing
mpic++ -std=c++17 -O3 -o resonance_proxy resonance_proxy_cpp.cpp \
    -lpthread -lrocm -DUSE_ROCM -DUSE_MPI
```

### Run

```bash
# Start proxy on port 8080
./resonance_proxy 8080

# Configure system to route traffic through proxy
# (Requires iptables rules or proxy settings)
```

### Features

- **Packet Interception**: Captures all HTTP/HTTPS traffic
- **GPU Acceleration**: Uses AMD ROCm for fast inference
- **MPI Support**: Distributes processing across multiple nodes
- **Zero-Copy**: Efficient packet handling
- **Multi-threaded**: Worker pool architecture

---

## 📈 Performance & Cost Savings

### Expected Results

With Resonance Protocol enabled:

- **Local routing**: 70-85% of queries
- **Cost savings**: $0.002 per local query vs ChatGPT API
- **Latency**: 150-500ms (local) vs 2000-5000ms (cloud)

### Example Savings

**Without Resonance Protocol:**
- 1,000 queries/day
- $0.002 per query (ChatGPT API)
- **Cost: $2/day = $60/month**

**With Resonance Protocol (80% local):**
- 800 queries → Local NeMo (free)
- 200 queries → ChatGPT web (free, no API)
- **Cost: $0/month**
- **Savings: $60/month**

---

## 🔍 Monitoring & Debugging

### Check Statistics

```bash
curl http://localhost:8001/api/resonance/statistics | jq
```

### View Query History

```bash
curl "http://localhost:8001/api/resonance/history?limit=10" | jq
```

### Test Classification

```bash
curl -X POST http://localhost:8001/api/resonance/classify \
  -H "Content-Type: application/json" \
  -d '{"query": "Your test query"}' | jq
```

### Health Check

```bash
curl http://localhost:8001/api/resonance/health | jq
```

---

## 🛠️ Troubleshooting

### Problem: "Router not initialized"

**Solution:** Make sure you've set the NeMo path:

```bash
export NEMO_MODEL_PATH="/path/to/your/SPI/nemo_model"
python app.py
```

### Problem: NeMo model won't load

**Check:**
1. Path is correct
2. NeMo is installed: `pip install nemo_toolkit`
3. Model files exist at specified path

**Test:**
```bash
curl -X POST http://localhost:8001/api/resonance/test \
  -H "Content-Type: application/json" \
  -d '{
    "endpoint": "local_nemo",
    "query": "test"
  }'
```

### Problem: Tampermonkey script not intercepting

**Solutions:**
1. Check script is enabled in Tampermonkey
2. Refresh ChatGPT page
3. Check browser console for errors (F12)
4. Verify backend is running: `curl http://localhost:8001/api/resonance/health`

### Problem: All queries going to ChatGPT

**Check routing logic:**
```bash
curl -X POST http://localhost:8001/api/resonance/classify \
  -H "Content-Type: application/json" \
  -d '{"query": "Your query"}' | jq
```

If it should go to local but doesn't, check NeMo model status.

---

## 🎯 Best Practices

### 1. **Configure NeMo Path Correctly**

Set environment variable in your shell profile:

```bash
# Add to ~/.bashrc or ~/.zshrc
export NEMO_MODEL_PATH="/home/user/SPI/nemo_gpt_model"
```

### 2. **Monitor Statistics Regularly**

Track cost savings and routing efficiency:

```bash
# Add to cron for daily reports
0 9 * * * curl http://localhost:8001/api/resonance/statistics > /tmp/resonance_stats.json
```

### 3. **Use Force Endpoint for Testing**

When developing, force specific endpoints:

```python
response = await router.process_query(
    query="Test query",
    force_endpoint=ModelEndpoint.LOCAL_NEMO
)
```

### 4. **Tune Classification Rules**

Edit `backend/integrations/resonance_protocol.py`:

```python
def classify_query(self, query: str) -> QueryType:
    # Add your custom classification rules
    if 'specialized_keyword' in query.lower():
        return QueryType.SPECIALIZED
```

---

## 🔐 Security Considerations

### Browser Interception (Tampermonkey)

- Only intercepts ChatGPT requests
- Does NOT capture passwords or auth tokens
- Open source - inspect the code!

### Network Interception (C++ Proxy)

- **Use with caution** - intercepts ALL network traffic
- For personal use only
- Do NOT use on company/school networks without permission

### Data Privacy

- All processing happens **locally** when using NeMo
- No data sent to external servers (except ChatGPT web when routed)
- Query history stored in memory only (cleared on restart)

---

## 📚 Related Documentation

- [ChatGPT Integration Guide](CHATGPT_INTEGRATION_GUIDE.md) - ChatGPT web session setup
- [VRChat Character Guide](VRCHAT_CHATGPT_CHARACTER_GUIDE.md) - VRChat AI character
- [OSS VRChat Resources](OSS_VRCHAT_RESOURCES.md) - Open-source VRChat projects
- [Unified Platform Quickstart](UNIFIED_PLATFORM_QUICKSTART.md) - Complete platform setup

---

## 🤝 Contributing

Found a better routing strategy? Improved classification?

1. Fork the repository
2. Create feature branch: `git checkout -b feature/better-routing`
3. Commit changes: `git commit -am 'Improve query classification'`
4. Push: `git push origin feature/better-routing`
5. Submit pull request

---

## 💡 Advanced Usage

### Custom Endpoint Handler

Add your own AI endpoint:

```python
from integrations.resonance_protocol import get_resonance_router, ModelEndpoint

async def my_custom_llm(query: str, context: dict = None):
    # Your custom LLM logic
    response = my_llm.generate(query)
    return {
        "success": True,
        "message": response,
        "model": "my_custom_llm"
    }

router = get_resonance_router()
router.register_endpoint(
    ModelEndpoint.HUGGINGFACE_LOCAL,
    my_custom_llm,
    cost_per_query=0.0
)
```

### Machine Learning-Based Classification

Replace keyword-based classification with ML:

```python
from transformers import pipeline

classifier = pipeline("text-classification", model="your-model")

def classify_query(self, query: str) -> QueryType:
    result = classifier(query)[0]
    if result['label'] == 'code':
        return QueryType.CODE_GENERATION
    # ... etc
```

---

## 🎉 Success Stories

Share your cost savings and use cases!

**Example:**
> "Saved $85/month by routing 90% of my development queries to local NeMo. Complex design discussions still use ChatGPT, but all code generation is free and faster!" - Developer using Resonance Protocol

---

## 📞 Support

- **Issues**: https://github.com/your-repo/issues
- **Discussions**: https://github.com/your-repo/discussions
- **Documentation**: This guide + related docs

---

**⚡ RESONANCE PROTOCOL - Making AI Free and Fast ⚡**

Zero API costs • Local-first • Intelligent routing • Open source
