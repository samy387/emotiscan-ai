# EmotiScan AI — Method 1: App + Backend Server

## Architecture
```
[app.html]  →  POST /analyze  →  [server.py]  →  Claude API  →  response
  Mobile App                      Python Backend               AI Model
```

## Setup (2 steps)

### 1. Start the backend server
```bash
# Install dependencies
pip install flask flask-cors anthropic

# Set your API key
export ANTHROPIC_API_KEY="sk-ant-YOUR_KEY_HERE"

# Start the server
python server.py
# → Running on http://localhost:5000
```

### 2. Open the mobile app
Open `app.html` in your browser — it will connect to the server automatically.

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/health` | Server status check |
| POST | `/analyze` | Analyze face emotion |

### POST /analyze
**Request:**
```json
{ "image": "<base64 string>", "media_type": "image/jpeg" }
```

**Response:**
```json
{
  "emotion": "Happy",
  "confidence": 94,
  "emoji": "😊",
  "scores": { "Happy": 94, "Sad": 2, "Angry": 1, ... },
  "description": "The person appears genuinely cheerful."
}
```

## Files
- `server.py` — Python Flask backend (the AI middleman)
- `app.html` — Mobile-style frontend (the client app)
- `README.md` — This file
