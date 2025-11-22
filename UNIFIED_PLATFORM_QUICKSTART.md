# 🌟 Unified AI Platform - Quick Start Guide

**ChatGPT Web + Hugging Face Biorhythm + VRChat OSC Integration**

---

## ✨ What This Platform Does

Your platform now integrates **three powerful systems** into one unified API:

1. **ChatGPT Web Session** - Interact with ChatGPT without API keys (uses your web session)
2. **Biorhythm & Circadian Analysis** - Neural pathways, biological cycles using Hugging Face models
3. **VRChat OSC Integration** - Real-time avatar visualization of your biorhythm data

---

## 🚀 Quick Setup (5 Minutes)

### Step 1: Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

**New dependencies added:**
- `selenium` - ChatGPT web automation
- `python-osc` - VRChat OSC communication
- `sktime` & `statsmodels` - Biorhythm time-series analysis

### Step 2: Get Your ChatGPT Access Token

**Option 1: Browser Console (Fastest)**
1. Go to https://chat.openai.com (logged in)
2. Press `F12` → Console tab
3. Paste this code:
```javascript
copy(document.cookie.split('; ').find(row => row.startsWith('__Secure-next-auth.session-token=')).split('=')[1])
```
4. Token is copied to clipboard!

**Option 2: Developer Tools**
1. Open ChatGPT → F12 → Application Tab
2. Cookies → https://chat.openai.com
3. Find `__Secure-next-auth.session-token`
4. Copy the Value

See [CHATGPT_INTEGRATION_GUIDE.md](CHATGPT_INTEGRATION_GUIDE.md) for detailed instructions.

### Step 3: Set Environment Variable

Create `.env` file in `backend/`:

```bash
CHATGPT_ACCESS_TOKEN=your_token_here
```

### Step 4: Enable VRChat OSC

In VRChat:
1. Quick Menu (R key) → Settings → OSC
2. Enable OSC (Port: 9000)

### Step 5: Start the Platform

```bash
python app.py
```

Platform starts on: `http://localhost:8001`

---

## 🎯 Quick Test

### Test 1: ChatGPT Integration

```bash
# Set your token
curl -X POST http://localhost:8001/api/unified/chatgpt/set-token \
  -H "Content-Type: application/json" \
  -d '{"access_token": "your_token_here"}'

# Ask ChatGPT a question
curl -X POST http://localhost:8001/api/unified/chatgpt/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "What are biorhythms and how do they affect daily performance?"}'
```

### Test 2: Biorhythm Analysis

```bash
curl -X POST http://localhost:8001/api/unified/biorhythm/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "birth_date": "1990-01-15",
    "ask_chatgpt": true
  }'
```

### Test 3: Complete Wellness Analysis with VRChat

```bash
curl -X POST http://localhost:8001/api/unified/wellness/complete \
  -H "Content-Type: application/json" \
  -d '{
    "birth_date": "1990-01-15",
    "sleep_schedule": {
      "bedtime": 23,
      "wake_time": 7
    },
    "sleep_data": [
      {"date": "2025-01-20", "sleep_hours": 7.5, "quality": 0.8},
      {"date": "2025-01-21", "sleep_hours": 6.0, "quality": 0.6},
      {"date": "2025-01-22", "sleep_hours": 8.0, "quality": 0.9}
    ]
  }'
```

This will:
- Calculate your biorhythm (physical, emotional, intellectual)
- Analyze circadian rhythm
- Get AI recommendations from ChatGPT
- Send data to your VRChat avatar (if connected)

---

## 🎮 VRChat Avatar Setup

### Required Avatar Parameters

Add these to your VRChat avatar in Unity:

**Float Parameters (0-1):**
```
Physical         - Physical biorhythm level
Emotional        - Emotional biorhythm level
Intellectual     - Intellectual biorhythm level
Composite        - Overall biorhythm composite
CircadianLevel   - Current circadian rhythm
EnergyLevel      - Current energy level
WellnessScore    - Overall wellness composite
```

**Int Parameter (0-4):**
```
NeuralState      - Brainwave state
  0 = Delta (deep sleep)
  1 = Theta (meditation)
  2 = Alpha (relaxed)
  3 = Beta (active/focused)
  4 = Gamma (peak awareness)
```

**Bool Parameter:**
```
BiorhythmActive  - System active indicator
```

### Avatar Animation Ideas

- **Aura Color**: Change based on `Composite` or `WellnessScore`
- **Eye Glow**: Intensity from `EnergyLevel`
- **Particle Effects**: Based on `NeuralState`
- **Material Emission**: Driven by `CircadianLevel`
- **Idle Animations**: Speed/type based on `Physical`

---

## 📊 API Endpoints Reference

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/api/unified/health` | GET | Health check |
| `/api/unified/status` | GET | Integration status |
| `/api/unified/chatgpt/set-token` | POST | Set ChatGPT token |
| `/api/unified/chatgpt/ask` | POST | Ask ChatGPT |
| `/api/unified/biorhythm/set-birth-date` | POST | Set birth date |
| `/api/unified/biorhythm/analyze` | POST | Analyze biorhythm |
| `/api/unified/circadian/analyze` | POST | Analyze circadian |
| `/api/unified/wellness/complete` | POST | Complete analysis |
| `/api/unified/vrchat/send-parameter` | POST | Manual VRChat param |
| `/api/unified/vrchat/send-chatbox` | POST | VRChat chatbox |

---

## 🔬 Understanding the Science

### Biorhythm Cycles

Your system calculates three biological cycles:

1. **Physical (23 days)** - Strength, coordination, well-being
2. **Emotional (28 days)** - Mood, creativity, perception
3. **Intellectual (33 days)** - Alertness, analytical ability, memory

Each cycle oscillates between high and low states, calculated from your birth date.

### Circadian Rhythm

24-hour biological clock that regulates:
- Sleep/wake cycles
- Hormone release
- Body temperature
- Cognitive performance

Peak alertness: ~10 AM - 2 PM
Lowest energy: ~2 AM - 4 AM

### Neural States (Brainwaves)

- **Delta (0.5-4 Hz)**: Deep sleep, healing
- **Theta (4-8 Hz)**: Deep meditation, dreams
- **Alpha (8-13 Hz)**: Relaxation, light meditation
- **Beta (13-30 Hz)**: Active thinking, focus
- **Gamma (30-100 Hz)**: Peak consciousness, insight

---

## 🎨 Example Use Cases

### 1. Daily Wellness Dashboard

```python
from integrations.unified_platform import get_unified_platform
from datetime import datetime

platform = get_unified_platform()

# Set your data
platform.set_chatgpt_token("your_token")
platform.set_user_birth_date(datetime(1990, 1, 15))

# Get daily analysis
result = platform.complete_wellness_analysis(
    sleep_schedule={"bedtime": 23, "wake_time": 7}
)

print(f"Today's Wellness: {result['biorhythm']['composite']:.1%}")
print(f"Energy Level: {result['circadian']['energy_level']:.1%}")
print(f"\nAI Recommendations:\n{result['ai_comprehensive_analysis']}")
```

### 2. VRChat Live Biorhythm Display

Your avatar will automatically update based on your real-time biorhythm data!

```bash
# This runs continuously and sends updates to VRChat
curl -X POST http://localhost:8001/api/unified/wellness/complete \
  -H "Content-Type: application/json" \
  -d '{"birth_date": "1990-01-15"}'
```

### 3. Sleep Optimization

```python
# Track sleep data and get AI recommendations
sleep_data = [
    {"date": "2025-01-20", "sleep_hours": 7.5, "quality": 0.8},
    {"date": "2025-01-21", "sleep_hours": 6.0, "quality": 0.6},
    {"date": "2025-01-22", "sleep_hours": 8.0, "quality": 0.9},
]

result = platform.complete_wellness_analysis(
    birth_date=datetime(1990, 1, 15),
    sleep_data=sleep_data
)

print(result['sleep_analysis'])
print(result['ai_comprehensive_analysis'])
```

### 4. Optimal Productivity Timing

```python
# Find your best times for different activities
biorhythm_analyzer = get_biorhythm_analyzer()
predictions = biorhythm_analyzer.predict_optimal_times(
    datetime(1990, 1, 15)
)

for day in predictions['predictions']:
    print(f"{day['date']}: {day['optimal_activity']}")
```

---

## 🔧 Troubleshooting

### ChatGPT Token Issues

**Problem**: 401 Unauthorized
**Solution**: Token expired - get a new one from ChatGPT web interface

**Problem**: Token not working
**Solution**:
- Ensure you're logged into ChatGPT in your browser
- Copy the entire token value
- Clear browser cookies and re-login

### VRChat OSC Not Working

**Problem**: Avatar not updating
**Solution**:
- Enable OSC in VRChat settings
- Verify port is 9000
- Check avatar has correct parameters defined
- Reset avatar in VRChat

**Problem**: Parameters not found
**Solution**:
- Avatar must have parameters in Unity
- Upload avatar again after adding parameters
- Parameter names are case-sensitive

### Biorhythm Analysis Issues

**Problem**: Birth date error
**Solution**:
- Use YYYY-MM-DD format
- Ensure date is in the past
- Validate date (no Feb 30, etc.)

---

## 🎓 Next Steps

1. ✅ **Customize Avatar**: Add visual effects driven by biorhythm parameters
2. ✅ **Build Dashboard**: Create frontend to visualize your wellness data
3. ✅ **Automate Updates**: Schedule periodic wellness checks
4. ✅ **Track Trends**: Store historical data to see patterns over time
5. ✅ **Share in VRChat**: Show friends your biorhythm-driven avatar effects

---

## 📚 Documentation

- [CHATGPT_INTEGRATION_GUIDE.md](CHATGPT_INTEGRATION_GUIDE.md) - Detailed ChatGPT setup
- [README.md](README.md) - Main platform documentation
- [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) - Production deployment

---

## 🌟 Key Features

- ✅ **No API Keys**: Uses ChatGPT web session (no OpenAI API costs)
- ✅ **Real-time**: Live updates to VRChat avatar
- ✅ **AI-Powered**: ChatGPT provides personalized recommendations
- ✅ **Scientific**: Based on biorhythm and circadian rhythm research
- ✅ **Extensible**: Easy to add more integrations
- ✅ **Open Source**: Fully customizable

---

## 💡 Advanced Tips

### Auto-Refresh Setup

Create a cron job or scheduled task to update hourly:

```bash
# Linux/Mac crontab
0 * * * * curl -X POST http://localhost:8001/api/unified/wellness/complete \
  -H "Content-Type: application/json" \
  -d '{"birth_date": "1990-01-15"}' > /dev/null 2>&1
```

### Custom VRChat World

Build a world that displays biorhythm data:
- Use VRChat Udon to receive OSC data
- Create visualizations (graphs, colors, effects)
- Share with friends for group wellness tracking

### Data Logging

Log your wellness data for trend analysis:

```python
import json
from datetime import datetime

result = platform.complete_wellness_analysis(...)

# Save to file
with open(f"wellness_{datetime.now().date()}.json", "w") as f:
    json.dump(result, f, indent=2)
```

---

**Happy Integrating! 🌟**

For questions or issues, see the main [README.md](README.md) or check the detailed [CHATGPT_INTEGRATION_GUIDE.md](CHATGPT_INTEGRATION_GUIDE.md).
