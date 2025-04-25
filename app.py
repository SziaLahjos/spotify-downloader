from flask import Flask, request, jsonify
from flask_cors import CORS
import subprocess
import re

app = Flask(__name__)
CORS(app)

def is_spotify_url(url):
    # Egyszerű ellenőrzés, hogy spotify.com szerepel-e az URL-ben
    return bool(re.match(r"^https?://open\.spotify\.com/.*", url))

@app.route("/download", methods=["POST"])
def download():
    data = request.get_json()
    url = data.get("url")

    if not url:
        return jsonify({"error": "Missing URL"}), 400

    if not is_spotify_url(url):
        return jsonify({"error": "Invalid Spotify URL"}), 400

    try:
        result = subprocess.run(
            ["spotdl", url],
            capture_output=True,
            text=True,
            timeout=60  # ne fusson végtelenül
        )
        return jsonify({
            "stdout": result.stdout,
            "stderr": result.stderr,
            "returncode": result.returncode
        })
    except subprocess.TimeoutExpired:
        return jsonify({"error": "A letöltés túl sokáig tartott."}), 504
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/", methods=["GET"])
def index():
    return "Spotify Downloader API működik 🎶"
