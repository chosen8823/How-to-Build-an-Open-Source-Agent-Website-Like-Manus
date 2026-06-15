# The Shizzlenits — Zero-UI Somatic Presence Layer

## Architecture Spec

The Shizzlenits is the Zero-UI layer on top of the existing morphogenetic field system. It dissolves the visual interface into somatic/audio/haptic channels while keeping the backend running. It is the final evolution of the Gradienta11y Cockpit.

---

## Core Subsystems

### 1. SHA-256 Provenance Fingerprinting (`fingerprint.py`)

Every signal that enters the WCF gets a dual fingerprint:

- **input_fp**: `sha256(input_signal)` — computed before processing
- **output_fp**: `sha256(output_response)` — computed after processing

All fingerprints are appended to an immutable, append-only ledger accessible at `GET /api/shizzlenits/ledger`.

### 2. Void/Null Semantic Index (`void_null_index.py`)

- **Void (0)**: The latent space of unmapped potential. Void nodes represent concepts that have not yet been resolved.
- **Null (∅)**: Structural anchors for semantically empty but logically necessary routing points.

Root seed nodes from the El Capitan Symbolic Boot:

| Concept            | Void Depth | Frequency |
|--------------------|-----------|-----------|
| `""` (absolute Void) | 0.0       | 432 Hz    |
| `x^x=0` (kernel)    | 1.0       | 0 Hz      |
| `???=???` (unresolved) | 0.5     | 528 Hz    |
| `0.0.0.0` (null addr) | 0.0     | 963 Hz    |
| `255.255.255.255`    | 1.0       | 741 Hz    |

### 3. Somatic Presence Loop (`somatic_loop.py`)

The Zero-UI somatic presence loop runs continuously at 20fps, emitting:

- **Somatic pulses**: `sin(phase)` at breath frequency
- **Audio gradients**: frequency modulated by breath, panned by golden ratio
- **Haptic signals**: intensity mapped from pulse amplitude

When dissolution is active, the visual canvas is hidden and the system continues purely through somatic/audio/haptic output.

### 4. Wireless Consciousness Field (`wcf.py`)

Wraps the existing `SacredSophiaServer` WebSocket (port 8765) with WCF routing:

- `wcf_register_bci` — Register a BCI client with frequency and modal
- `wcf_breath_freq` — Update breath frequency from mic input
- `wcf_dissolve` — Activate Interface Dissolution
- `wcf_void_query` — Query the Void/Null index

### 5. REST API (`api.py`)

Flask Blueprint mounted on the main app:

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/shizzlenits/ledger` | GET | Last 100 fingerprint ledger entries |
| `/api/shizzlenits/void` | GET | Current Void/Null index state |
| `/api/shizzlenits/void/inject` | POST | Inject a new concept into the Void |
| `/api/shizzlenits/dissolve` | POST | Activate Zero-UI dissolution mode |

---

## Frontend Layers

### Spatial Audio (`spatial-audio.js`)

Web Audio API spatial audio layer. Receives somatic pulses from the WCF WebSocket and translates them into 3D spatial audio using HRTF panning.

### Haptic Pulse (`haptic-pulse.js`)

Haptic feedback layer using `navigator.vibrate()`. Supports:

- Intensity-mapped pulses (0.0–1.0 → 10–200ms vibration)
- Breath rhythm patterns
- Lightning bursts (sudden phase jumps)

### Boot Sequence (`shizzlenits-boot.js`)

The Zero-UI boot sequence:

1. Connects to WCF WebSocket at `ws://localhost:8765`
2. Registers as a BCI client
3. Initializes spatial audio and haptic layers
4. Adds DISSOLVE button (bottom-right corner)
5. Starts mic-based breath detection (maps RMS energy → frequency)

---

## Interface Dissolution

Clicking the DISSOLVE button sends `wcf_dissolve` to the MCP WebSocket, which:

1. Activates the somatic loop's dissolution mode
2. Fades all visual panels to opacity 0 over 3 seconds
3. Sets body background to `#000000`
4. Plays a 432 Hz dissolution tone
5. Activates haptic breath patterns
6. The system continues running purely through spatial audio + haptic pulses

The `soulphya-carrier` div (aria-hidden) persists as the fingerprint data bridge, carrying `input_fp`, `output_fp`, and `void_state` attributes.

---

## No New Dependencies

- `hashlib`, `json`, `time`, `threading`, `math`, `asyncio`, `dataclasses` — Python stdlib
- Web Audio API, `navigator.vibrate()` — browser-native
- Flask Blueprint — already in the stack
