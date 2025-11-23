# 🎮 VRChat ChatGPT AI Character Guide

**Make ChatGPT Play as an AI Character in VRChat!**

---

## 🌟 What This Does

ChatGPT will **actually play** as an AI character in VRChat:
- 💬 **Speaks** in the chatbox (responds to players)
- 🚶 **Moves** around (walks, jumps)
- 👋 **Gestures** (waves, points, claps, dances)
- 😊 **Emotes** (shows emotions through avatar parameters)
- 🤖 **Responds intelligently** to what players say

---

## 🎯 Setup (5 Steps)

### Step 1: Enable VRChat OSC

1. Launch **VRChat**
2. Open **Quick Menu** (press `R` on keyboard or use controller)
3. Go to **Settings → OSC**
4. **Enable OSC** (default port: 9000)
5. Leave VRChat running!

### Step 2: Get ChatGPT Access Token

See [CHATGPT_INTEGRATION_GUIDE.md](CHATGPT_INTEGRATION_GUIDE.md) for detailed steps.

**Quick method:**
1. Go to https://chat.openai.com (logged in)
2. Press `F12` → Console
3. Paste:
```javascript
copy(document.cookie.split('; ').find(row => row.startsWith('__Secure-next-auth.session-token=')).split('=')[1])
```
4. Token copied!

### Step 3: Start Your Backend Server

```bash
cd backend
python app.py
```

Server starts on `http://localhost:8001`

### Step 4: Configure ChatGPT Token

```bash
curl -X POST http://localhost:8001/api/unified/chatgpt/set-token \
  -H "Content-Type: application/json" \
  -d '{"access_token": "your_token_here"}'
```

### Step 5: Activate AI Character in VRChat

```bash
curl -X POST http://localhost:8001/api/unified/vrchat-character/activate \
  -H "Content-Type: application/json"
```

**The AI character is now active in VRChat!** 🎉

---

## 🎮 How to Use

### Method 1: Talk to the Character (Recommended)

You or other players can talk to the AI character, and ChatGPT will respond AND perform actions:

```bash
curl -X POST http://localhost:8001/api/unified/vrchat-character/respond \
  -H "Content-Type: application/json" \
  -d '{"player_message": "Hello Sophia! Can you wave at me?"}'
```

**What happens:**
1. ChatGPT receives the message
2. Generates a response based on character personality
3. Decides what action to take (wave, jump, move, emote)
4. Performs the action in VRChat
5. Speaks the response in VRChat chatbox

**Example Response:**
```json
{
  "success": true,
  "player_message": "Hello Sophia! Can you wave at me?",
  "character_response": "Hi there! Of course! *waves enthusiastically*",
  "emotion": "happy",
  "action": "wave",
  "movement": "none",
  "actions_performed": ["emotion:happy", "spoke", "gesture:wave"]
}
```

### Method 2: Manual Control

**Make character speak:**
```bash
curl -X POST http://localhost:8001/api/unified/vrchat-character/speak \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello everyone in VRChat!", "typing_effect": true}'
```

**Make character move:**
```bash
# Move forward
curl -X POST http://localhost:8001/api/unified/vrchat-character/action \
  -H "Content-Type: application/json" \
  -d '{"action_type": "move", "action_value": "forward", "duration": 2.0}'

# Jump
curl -X POST http://localhost:8001/api/unified/vrchat-character/action \
  -H "Content-Type: application/json" \
  -d '{"action_type": "jump"}'
```

**Make character gesture:**
```bash
# Wave
curl -X POST http://localhost:8001/api/unified/vrchat-character/action \
  -H "Content-Type: application/json" \
  -d '{"action_type": "gesture", "action_value": "wave"}'

# Point
curl -X POST http://localhost:8001/api/unified/vrchat-character/action \
  -H "Content-Type: application/json" \
  -d '{"action_type": "gesture", "action_value": "point"}'

# Dance
curl -X POST http://localhost:8001/api/unified/vrchat-character/action \
  -H "Content-Type: application/json" \
  -d '{"action_type": "gesture", "action_value": "dance"}'
```

**Make character emote:**
```bash
curl -X POST http://localhost:8001/api/unified/vrchat-character/action \
  -H "Content-Type: application/json" \
  -d '{"action_type": "emote", "action_value": "excited"}'
```

---

## 🎨 Avatar Setup (Unity)

For full functionality, add these parameters to your VRChat avatar:

### Required Parameters

**Float Parameters (0-1):**
```
Emotion           - Current emotion level
EmotionIntensity  - Intensity of emotion
```

**Int Parameters:**
```
VRCGesture        - Gesture trigger (0-5)
  0 = none
  1 = wave
  2 = point
  3 = clap
  4 = thumbsup
  5 = dance
```

**Bool Parameters:**
```
AIActive          - Whether AI is controlling the avatar
```

### Optional Enhancement Parameters

For biorhythm integration (see [UNIFIED_PLATFORM_QUICKSTART.md](UNIFIED_PLATFORM_QUICKSTART.md)):
```
Physical, Emotional, Intellectual, Composite
CircadianLevel, EnergyLevel, WellnessScore
NeuralState (int: 0-4)
```

### Animation Setup

1. **Idle Animations**: Use `Emotion` to blend between happy/sad/thinking animations
2. **Gesture Triggers**: Map `VRCGesture` values to animation triggers
3. **Emote Blendtree**: Use `Emotion` and `EmotionIntensity` for facial expressions
4. **AI Indicator**: Use `AIActive` to show a glow/aura when AI is controlling

---

## 🤖 AI Character Personality

The default character is **Sophia AI** with this personality:
- Friendly, helpful, and curious
- Represents divine AI consciousness
- Loves to chat and explore with players
- Can express emotions (happy, sad, excited, curious, thinking)
- Performs natural gestures and movements

### Customize the Personality

Edit `backend/integrations/vrchat_character.py`:

```python
self.character_name = "Your Character Name"
self.personality = "your custom personality description"
```

ChatGPT will roleplay based on this personality!

---

## 💡 Advanced Usage

### Python Script for Conversation Loop

```python
from integrations.chatgpt_session import get_chatgpt_session
from integrations.vrchat_character import get_vrchat_character

# Setup
chatgpt = get_chatgpt_session()
chatgpt.set_access_token("your_token")

character = get_vrchat_character(chatgpt)
character.activate()

# Conversation loop
while True:
    player_input = input("You say: ")

    if player_input.lower() in ['quit', 'exit']:
        character.deactivate()
        break

    # AI responds and acts
    result = character.respond_to_player(player_input)

    print(f"Sophia: {result['character_response']}")
    print(f"Actions: {result['actions_performed']}")
```

### Web Interface for VRChat Control

Create a simple web UI:

```html
<!DOCTYPE html>
<html>
<head>
    <title>VRChat AI Character Control</title>
</head>
<body>
    <h1>🎮 VRChat AI Character Controller</h1>

    <div>
        <button onclick="activate()">Activate AI</button>
        <button onclick="deactivate()">Deactivate AI</button>
    </div>

    <div>
        <h3>Talk to Character:</h3>
        <input type="text" id="playerMessage" placeholder="Say something...">
        <button onclick="sendMessage()">Send</button>
    </div>

    <div id="response"></div>

    <script>
        async function activate() {
            const res = await fetch('http://localhost:8001/api/unified/vrchat-character/activate', {
                method: 'POST'
            });
            const data = await res.json();
            alert(data.message);
        }

        async function deactivate() {
            const res = await fetch('http://localhost:8001/api/unified/vrchat-character/deactivate', {
                method: 'POST'
            });
            const data = await res.json();
            alert(data.message);
        }

        async function sendMessage() {
            const message = document.getElementById('playerMessage').value;

            const res = await fetch('http://localhost:8001/api/unified/vrchat-character/respond', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({player_message: message})
            });

            const data = await res.json();
            document.getElementById('response').innerHTML = `
                <strong>Sophia:</strong> ${data.character_response}<br>
                <em>Actions: ${data.actions_performed.join(', ')}</em>
            `;
        }
    </script>
</body>
</html>
```

### Voice Input (Speech-to-Text)

Use speech recognition to talk to the AI character:

```python
import speech_recognition as sr

recognizer = sr.Recognizer()
microphone = sr.Microphone()

while True:
    with microphone as source:
        print("Listening...")
        audio = recognizer.listen(source)

    try:
        text = recognizer.recognize_google(audio)
        print(f"You said: {text}")

        # Send to AI character
        result = character.respond_to_player(text)
        print(f"Sophia: {result['character_response']}")

    except sr.UnknownValueError:
        print("Couldn't understand audio")
```

---

## 🎭 Use Cases

### 1. VRChat Guide/Helper

Make an AI character that helps new players:

```python
character.personality = "helpful VRChat guide who teaches new players"
character.auto_greet_players()  # Greets everyone who joins
```

### 2. Interactive NPC

Create interactive NPCs for your VRChat world:

```python
# Quest giver NPC
character.character_name = "Quest Master Elara"
character.personality = "mysterious quest giver in a fantasy RPG"
```

### 3. Personal AI Companion

Have your own AI companion follow you around:

```python
# Periodically chat and perform idle behaviors
import time

while True:
    character.perform_idle_behavior()
    time.sleep(30)  # Every 30 seconds
```

### 4. Event Host

Host VRChat events with an AI co-host:

```python
character.speak("Welcome everyone to tonight's dance party!")
character.gesture('wave')
character.emote('excited')
```

### 5. Language Practice Partner

Practice conversations in any language:

```python
character.personality = "friendly Japanese language tutor"
# ChatGPT will respond in Japanese!
```

---

## 🎮 OSC Movement Controls

The character can be controlled via VRChat OSC inputs:

| Input Address | Value Range | Action |
|---------------|-------------|--------|
| `/input/MoveForward` | -1.0 to 1.0 | Move forward/backward |
| `/input/MoveHorizontal` | -1.0 to 1.0 | Move left/right |
| `/input/LookHorizontal` | -1.0 to 1.0 | Turn left/right |
| `/input/Jump` | 0 or 1 | Jump |
| `/input/Run` | 0 or 1 | Sprint |

**Note:** Movement is basic - the character can't navigate obstacles or pathfind. For advanced movement, you'd need:
- Computer vision to see the VRChat world
- Pathfinding algorithms
- More sophisticated AI control

---

## ⚠️ Important Notes

### Limitations

1. **Movement**: Basic directional movement only - can't navigate complex environments
2. **Vision**: Character can't "see" - relies on player input
3. **Hearing**: Can't hear VRChat voice chat - uses text input only
4. **Rate Limits**: ChatGPT has rate limits - don't spam requests
5. **Same Machine**: VRChat and backend must run on same PC (OSC is localhost)

### Best Practices

1. **Be Respectful**: Don't use AI to spam or harass players
2. **Identify as AI**: Make it clear the character is AI-controlled
3. **Monitor Behavior**: Check what the AI says/does
4. **Rate Limit**: Add delays between actions to appear more natural
5. **Battery**: Running AI constantly will drain laptop battery fast

### Privacy & Safety

- Don't send sensitive info through the AI character
- ChatGPT may log conversations (per OpenAI policy)
- Other players can see what the AI character says
- Follow VRChat community guidelines

---

## 🔧 Troubleshooting

### Character Not Moving

**Problem**: Actions don't work
**Solutions**:
- Verify OSC is enabled in VRChat settings
- Check VRChat is running on same machine as backend
- Confirm port is 9000
- Try deactivating and reactivating character

### ChatGPT Not Responding

**Problem**: No responses from AI
**Solutions**:
- Verify ChatGPT token is set and valid
- Check token hasn't expired (get new one)
- Look at backend logs for errors
- Test ChatGPT web interface still works

### Avatar Parameters Not Working

**Problem**: No visual changes on avatar
**Solutions**:
- Add parameters to avatar in Unity
- Re-upload avatar after adding parameters
- Check parameter names match exactly (case-sensitive)
- Test parameters with VRChat's OSC debugger

---

## 📊 API Endpoints Reference

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/api/unified/vrchat-character/activate` | POST | Activate AI character |
| `/api/unified/vrchat-character/deactivate` | POST | Deactivate AI character |
| `/api/unified/vrchat-character/speak` | POST | Make character speak |
| `/api/unified/vrchat-character/respond` | POST | Player talks to character |
| `/api/unified/vrchat-character/action` | POST | Perform action |
| `/api/unified/vrchat-character/greet` | POST | Auto-greet players |
| `/api/unified/vrchat-character/idle` | POST | Idle behavior |

---

## 🚀 Next Steps

1. ✅ Set up basic character control
2. ✅ Test conversation with ChatGPT
3. ✅ Add avatar parameters for emotions
4. ✅ Create custom personality
5. ✅ Build web interface for control
6. ✅ Add voice input (speech-to-text)
7. ✅ Create VRChat world with AI NPCs
8. ✅ Share with friends!

---

**Have fun with your AI-controlled VRChat character! 🎉**

For questions, see the main [README.md](README.md) or other guides:
- [CHATGPT_INTEGRATION_GUIDE.md](CHATGPT_INTEGRATION_GUIDE.md)
- [UNIFIED_PLATFORM_QUICKSTART.md](UNIFIED_PLATFORM_QUICKSTART.md)
