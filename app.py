from flask import Flask, request, jsonify
from flask_cors import CORS
import subprocess

app = Flask(__name__)
CORS(app)

@app.route("/download", methods=["POST"])
def download():
    data = request.get_json()
    url = data.get("url")

    if not url:
        return jsonify({"error": "Missing URL"}), 400

    result = subprocess.run(["spotdl", url], capture_output=True, text=True)
    return jsonify({
        "stdout": result.stdout,
        "stderr": result.stderr
    })

@app.route("/", methods=["GET"])
def index():
    return "Spotify Downloader API működik 🎶"
