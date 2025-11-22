# 🤖 ChatGPT Web Integration Guide

## How to Get Your ChatGPT Access Token

You need to get your access token from ChatGPT's web session. This token allows the platform to interact with ChatGPT as if you're using the web interface.

### Method 1: Browser Developer Tools (Recommended) ⭐

#### For Chrome/Edge:

1. **Open ChatGPT** in your browser
   - Go to https://chat.openai.com
   - Make sure you're logged in

2. **Open Developer Tools**
   - Press `F12` or `Ctrl+Shift+I` (Windows/Linux)
   - Press `Cmd+Option+I` (Mac)

3. **Go to Application Tab**
   - Click on the "Application" tab in Developer Tools
   - If you don't see it, click the `>>` icon to find it

4. **Find Cookies**
   - In the left sidebar, expand "Cookies"
   - Click on "https://chat.openai.com"

5. **Copy the Access Token**
   - Look for a cookie named `__Secure-next-auth.session-token`
   - Click on it
   - Copy the entire "Value" field
   - This is your access token!

#### For Firefox:

1. **Open ChatGPT** at https://chat.openai.com (make sure you're logged in)

2. **Open Developer Tools**
   - Press `F12` or `Ctrl+Shift+I`

3. **Go to Storage Tab**
   - Click on "Storage" tab
   - Expand "Cookies"
   - Click on "https://chat.openai.com"

4. **Find and Copy Token**
   - Look for `__Secure-next-auth.session-token`
   - Copy the Value

### Method 2: Using Browser Console (Quick Method)

1. **Open ChatGPT** at https://chat.openai.com (logged in)

2. **Open Console**
   - Press `F12` to open Developer Tools
   - Click on "Console" tab

3. **Run This Code**
   ```javascript
   copy(document.cookie.split('; ').find(row => row.startsWith('__Secure-next-auth.session-token=')).split('=')[1])
   ```

4. **Token is Copied**
   - The access token is now in your clipboard
   - Paste it where needed!

### Method 3: Export Using Cookie Extension

1. **Install Cookie Extension**
   - Chrome: [EditThisCookie](https://chrome.google.com/webstore/detail/editthiscookie/)
   - Firefox: [Cookie-Editor](https://addons.mozilla.org/en-US/firefox/addon/cookie-editor/)

2. **Open ChatGPT** and click the extension icon

3. **Find the Token**
   - Search for `__Secure-next-auth.session-token`
   - Copy the value

---

## Setting Up the Integration

### Step 1: Get Your Access Token

Use one of the methods above to get your `access_token`.

### Step 2: Configure the Platform

#### Option A: Using Environment Variable

Create or edit `.env` file in the `backend/` directory:

```bash
CHATGPT_ACCESS_TOKEN=your_access_token_here
```

#### Option B: Using API Call

```bash
curl -X POST http://localhost:8080/api/unified/chatgpt/set-token \
  -H "Content-Type: application/json" \
  -d '{"access_token": "your_access_token_here"}'
```

#### Option C: Using Python

```python
from integrations.unified_platform import get_unified_platform

platform = get_unified_platform()
platform.set_chatgpt_token("your_access_token_here")
```

---

## Testing the Integration

### 1. Check Status

```bash
curl http://localhost:8080/api/unified/status
```

You should see `"configured": true` under chatgpt status.

### 2. Ask ChatGPT a Question

```bash
curl -X POST http://localhost:8080/api/unified/chatgpt/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "Hello! Can you explain what biorhythms are?"}'
```

### 3. Complete Wellness Analysis

```bash
curl -X POST http://localhost:8080/api/unified/wellness/complete \
  -H "Content-Type: application/json" \
  -d '{
    "birth_date": "1990-01-15",
    "sleep_schedule": {
      "bedtime": 23,
      "wake_time": 7
    }
  }'
```

---

## Token Management

### Token Expiration

ChatGPT access tokens typically last for several weeks. The system will:
- Automatically attempt to refresh the token when it expires
- Return an error if refresh fails
- You'll need to get a new token manually if auto-refresh fails

### Security Best Practices

1. **Keep Your Token Private**
   - Never commit tokens to git
   - Add `.env` to your `.gitignore`
   - Don't share tokens publicly

2. **Use Environment Variables**
   ```bash
   export CHATGPT_ACCESS_TOKEN="your_token_here"
   ```

3. **Rotate Tokens Regularly**
   - Get a new token every few weeks
   - Revoke old sessions by logging out of ChatGPT

---

## VRChat OSC Setup

### Enable OSC in VRChat

1. **Launch VRChat**

2. **Open Quick Menu** (default: `R` on keyboard)

3. **Go to Settings**
   - Options → OSC
   - Enable "OSC"
   - Note the port (default: 9000)

### Avatar Parameters

Add these parameters to your VRChat avatar (Unity):

#### Biorhythm Parameters (Float, 0-1)
```
Physical         - Physical biorhythm level
Emotional        - Emotional biorhythm level
Intellectual     - Intellectual biorhythm level
Composite        - Overall biorhythm composite
```

#### Circadian Rhythm Parameters (Float, 0-1)
```
CircadianLevel   - Current circadian rhythm level
EnergyLevel      - Current energy level
WellnessScore    - Overall wellness composite
```

#### Neural State (Int, 0-4)
```
NeuralState      - Current brainwave state
  0 = delta (deep sleep)
  1 = theta (light sleep, meditation)
  2 = alpha (relaxed, wakeful)
  3 = beta (active, focused)
  4 = gamma (peak awareness)
```

#### Status Flag (Bool)
```
BiorhythmActive  - Whether biorhythm system is active
```

### Example Avatar Animations

Use these parameters to drive:
- **Glow/Aura Color**: Based on `Composite` or `WellnessScore`
- **Eye Color**: Based on `NeuralState`
- **Particle Effects**: Intensity from `EnergyLevel`
- **Idle Animations**: Speed/type based on `Physical`
- **Material Properties**: Emission based on `CircadianLevel`

---

## Complete Workflow Example

### Python Script

```python
from integrations.unified_platform import get_unified_platform
from datetime import datetime

# Initialize platform
platform = get_unified_platform()

# 1. Set ChatGPT token
platform.set_chatgpt_token("your_access_token")

# 2. Set your birth date
platform.set_user_birth_date(datetime(1990, 1, 15))

# 3. Get complete wellness analysis
result = platform.complete_wellness_analysis(
    sleep_schedule={"bedtime": 23, "wake_time": 7},
    sleep_data=[
        {"date": "2025-01-20", "sleep_hours": 7.5, "quality": 0.8},
        {"date": "2025-01-21", "sleep_hours": 6.0, "quality": 0.6},
        {"date": "2025-01-22", "sleep_hours": 8.0, "quality": 0.9},
    ]
)

print(f"Biorhythm Composite: {result['biorhythm']['composite']:.1%}")
print(f"Energy Level: {result['circadian']['energy_level']:.1%}")
print(f"AI Analysis: {result['ai_comprehensive_analysis']}")
print(f"VRChat Updated: {result['vrchat_updated']}")
```

### API Request

```bash
curl -X POST http://localhost:8080/api/unified/wellness/complete \
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

---

## Troubleshooting

### ChatGPT Token Issues

**Problem**: Token not working
**Solution**:
- Make sure you're logged into ChatGPT in the same browser
- Get a fresh token (they can expire)
- Clear browser cookies and re-login to ChatGPT

**Problem**: "401 Unauthorized" error
**Solution**:
- Token has expired - get a new one
- Make sure you copied the entire token value
- Check that ChatGPT Plus/Free tier is active

### VRChat OSC Issues

**Problem**: Avatar not updating
**Solution**:
- Ensure OSC is enabled in VRChat settings
- Check port is 9000 (or match your settings)
- Verify avatar has the correct parameters defined
- Try resetting avatar

**Problem**: Parameters not found
**Solution**:
- Avatar must have parameters defined in Unity
- Upload avatar again if parameters were added
- Check parameter names match exactly (case-sensitive)

### Biorhythm Analysis Issues

**Problem**: Birth date error
**Solution**:
- Use YYYY-MM-DD format
- Ensure date is in the past
- Check date is valid (no Feb 30, etc.)

---

## API Reference Quick Guide

All endpoints: `http://localhost:8080/api/unified/`

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/health` | GET | Check system health |
| `/status` | GET | Get integration status |
| `/chatgpt/set-token` | POST | Set access token |
| `/chatgpt/ask` | POST | Ask ChatGPT |
| `/biorhythm/set-birth-date` | POST | Set birth date |
| `/biorhythm/analyze` | POST | Analyze biorhythm |
| `/circadian/analyze` | POST | Analyze circadian |
| `/wellness/complete` | POST | Complete analysis |
| `/vrchat/send-parameter` | POST | Send VRChat param |
| `/vrchat/send-chatbox` | POST | VRChat chatbox msg |

---

## Next Steps

1. ✅ Get your ChatGPT access token
2. ✅ Set up VRChat OSC
3. ✅ Configure your avatar parameters
4. ✅ Test the integration
5. 🎨 Create custom visualizations
6. 🚀 Build your personalized wellness dashboard!

---

**Happy integrating! 🌟**

*For issues or questions, check the main README or open an issue on GitHub.*
