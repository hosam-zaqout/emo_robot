"""
EMO Robot — Flask Token Server
Hosted on Render. Provides AssemblyAI temporary WebSocket tokens to ESP32.
"""

import os
import requests
from flask import Flask, jsonify

app = Flask(__name__)

ASSEMBLYAI_API_KEY = os.environ.get("ASSEMBLYAI_API_KEY")
AAI_TOKEN_URL      = "https://streaming.assemblyai.com/v3/token"
TOKEN_EXPIRES_IN   = 60  # seconds


@app.route("/token", methods=["GET"])
def get_token():
    """
    Called by ESP32 on boot.
    Fetches a short-lived AssemblyAI WebSocket token and returns it as JSON.
    """
    if not ASSEMBLYAI_API_KEY:
        return jsonify({"error": "ASSEMBLYAI_API_KEY environment variable not set"}), 500

    try:
        resp = requests.post(
            AAI_TOKEN_URL,
            params={"expires_in_seconds": TOKEN_EXPIRES_IN},
            headers={
                "Authorization": f"Bearer {ASSEMBLYAI_API_KEY}",
                "Content-Type": "application/json",
            },
            timeout=10,
        )
    except requests.exceptions.Timeout:
        return jsonify({"error": "AssemblyAI request timed out"}), 504
    except requests.exceptions.RequestException as exc:
        return jsonify({"error": f"Failed to reach AssemblyAI: {str(exc)}"}), 502

    if resp.status_code != 200:
        return jsonify({
            "error": "AssemblyAI returned an error",
            "status": resp.status_code,
            "detail": resp.text,
        }), resp.status_code

    data = resp.json()

    if "token" not in data:
        return jsonify({"error": "Unexpected response from AssemblyAI", "raw": data}), 500

    return jsonify({"token": data["token"]}), 200


@app.route("/health", methods=["GET"])
def health():
    """Simple health check for Render."""
    return jsonify({"status": "ok"}), 200


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
