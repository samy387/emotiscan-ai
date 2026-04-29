"""
EmotiScan AI - Backend Server (Method 1)
=========================================
Mobile App  →  POST /analyze  →  This Server  →  Claude API  →  Response
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import anthropic
import base64
import os
import json
import re

app = Flask(__name__)
CORS(app)

# ─── PUT YOUR API KEY HERE ────────────────────────────────────────────────────
API_KEY = "YOUR_API_KEY_HERE"
# ─────────────────────────────────────────────────────────────────────────────

# ─── MOCK MODE (Bypasses the "Credit balance too low" error) ──────────────────
# Set to False when you add credits to your Anthropic account
MOCK_MODE = True
# ─────────────────────────────────────────────────────────────────────────────

# It also works if you set the environment variable instead

def get_client():
    key = os.environ.get("ANTHROPIC_API_KEY") or API_KEY
    if not key or key == "YOUR_API_KEY_HERE":
        raise ValueError("API key not set. Edit server.py and paste your key into API_KEY.")
    return anthropic.Anthropic(api_key=key)


@app.route("/health", methods=["GET"])
def health():
    try:
        get_client()
        return jsonify({"status": "ok", "server": "EmotiScan AI Backend", "key": "loaded"})
    except ValueError as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.get_json()
    if not data or "image" not in data:
        return jsonify({"error": "No image provided. Send { image: base64string }"}), 400

    image_b64 = data["image"]
    media_type = data.get("media_type", "image/jpeg")

    try:
        base64.b64decode(image_b64)
    except Exception:
        return jsonify({"error": "Invalid base64 image data"}), 400

    try:
        if MOCK_MODE:
            import time
            time.sleep(1) # simulate network delay
            result = {
                "emotion": "Happy",
                "confidence": 98,
                "emoji": "😊",
                "scores": {
                    "Happy": 98, "Sad": 0, "Angry": 0,
                    "Surprised": 1, "Neutral": 1, "Fearful": 0, "Disgusted": 0
                },
                "description": "(MOCK MODE) The person appears to be smiling and happy! Add credits to your Anthropic account and set MOCK_MODE = False in server.py to use real AI."
            }
        else:
            client = get_client()
            response = client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=600,
                system="""You are a face emotion detection AI server.
Analyze the face in the image and return ONLY a JSON object (no markdown, no extra text).
Format exactly:
{
  "emotion": "<primary emotion label>",
  "confidence": <integer 0-100>,
  "emoji": "<single emoji representing the emotion>",
  "scores": {
    "Happy": <0-100>,
    "Sad": <0-100>,
    "Angry": <0-100>,
    "Surprised": <0-100>,
    "Neutral": <0-100>,
    "Fearful": <0-100>,
    "Disgusted": <0-100>
  },
  "description": "<one sentence about the detected expression>"
}
If no face is visible, set emotion to "No face detected" and all scores to 0.""",
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "image",
                                "source": {
                                    "type": "base64",
                                    "media_type": media_type,
                                    "data": image_b64,
                                },
                            },
                            {"type": "text", "text": "Analyze the emotion on this face."},
                        ],
                    }
                ],
            )

            raw = response.content[0].text
            raw = re.sub(r"```json|```", "", raw).strip()
            result = json.loads(raw)

    except ValueError as e:
        return jsonify({"error": str(e)}), 500
    except json.JSONDecodeError:
        return jsonify({"error": "AI returned unexpected format"}), 500
    except anthropic.APIStatusError as e:
        return jsonify({"error": f"Claude API error {e.status_code}: {e.message}"}), 502
    except Exception as e:
        return jsonify({"error": f"Server error: {str(e)}"}), 500

    return jsonify(result)


@app.route("/", methods=["GET"])
def index():
    return jsonify({
        "name": "EmotiScan AI Backend",
        "endpoints": {
            "GET  /health": "Check server + key status",
            "POST /analyze": "Analyze face — body: { image: base64, media_type: string }",
        }
    })


if __name__ == "__main__":
    print("\n" + "="*50)
    print("  EmotiScan AI Server")
    print("="*50)
    key = os.environ.get("ANTHROPIC_API_KEY") or API_KEY
    if key and key != "YOUR_API_KEY_HERE":
        print(f"  API key: {key[:16]}...")
        print("  Status:  Ready")
    else:
        print("  Status:  NO API KEY SET")
        print("  Fix:     Edit server.py, paste key into API_KEY = '...'")
    print(f"  URL:     http://localhost:5000")
    print("="*50 + "\n")
    app.run(debug=True, host="0.0.0.0", port=5000)
