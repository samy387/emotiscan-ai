"""
EmotiScan AI - Backend Server (Method 1)
=========================================
Mobile App  →  POST /analyze  →  This Server  →  Local DeepFace AI  →  Response
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from deepface import DeepFace
import cv2
import numpy as np
import base64
import os
import json
import re

app = Flask(__name__)
CORS(app)

# ─── MOCK MODE (Set to False to use the real AI) ──────────────────────────────
MOCK_MODE = False
# ─────────────────────────────────────────────────────────────────────────────

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok", "server": "EmotiScan AI Backend (DeepFace Offline)"})

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
            image_bytes = base64.b64decode(image_b64)
            nparr = np.frombuffer(image_bytes, np.uint8)
            img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

            analysis = DeepFace.analyze(img, actions=['emotion'], enforce_detection=False)
            res = analysis[0] if isinstance(analysis, list) else analysis
            
            scores_raw = res['emotion']
            scores = {
                "Happy": int(scores_raw.get("happy", 0)),
                "Sad": int(scores_raw.get("sad", 0)),
                "Angry": int(scores_raw.get("angry", 0)),
                "Surprised": int(scores_raw.get("surprise", 0)),
                "Neutral": int(scores_raw.get("neutral", 0)),
                "Fearful": int(scores_raw.get("fear", 0)),
                "Disgusted": int(scores_raw.get("disgust", 0)),
            }
            
            dominant = res['dominant_emotion']
            dominant_cap = dominant.capitalize()
            if dominant_cap == "Surprise": dominant_cap = "Surprised"
            if dominant_cap == "Fear": dominant_cap = "Fearful"
            if dominant_cap == "Disgust": dominant_cap = "Disgusted"
            
            emoji_map = {
                "Happy": "😊", "Sad": "😢", "Angry": "😠", 
                "Surprised": "😲", "Neutral": "😐", "Fearful": "😨", "Disgusted": "🤢"
            }
            
            result = {
                "emotion": dominant_cap,
                "confidence": scores.get(dominant_cap, 0),
                "emoji": emoji_map.get(dominant_cap, "😐"),
                "scores": scores,
                "description": f"The person appears to be {dominant}."
            }

    except ValueError as e:
        return jsonify({"error": str(e)}), 500
    except Exception as e:
        return jsonify({"error": f"Server/DeepFace error: {str(e)}"}), 500

    return jsonify(result)

@app.route("/", methods=["GET"])
def index():
    return jsonify({
        "name": "EmotiScan AI Backend",
        "endpoints": {
            "GET  /health": "Check server status",
            "POST /analyze": "Analyze face — body: { image: base64, media_type: string }",
        }
    })

if __name__ == "__main__":
    print("\n" + "="*50)
    print("  EmotiScan AI Server (Powered by DeepFace Offline)")
    print("="*50)
    print("  Status:  Ready (NO API KEYS NEEDED!)")
    print(f"  URL:     http://localhost:5000")
    print("="*50 + "\n")
    app.run(debug=True, host="0.0.0.0", port=5000)
