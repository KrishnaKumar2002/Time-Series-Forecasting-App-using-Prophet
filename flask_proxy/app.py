import os
from flask import Flask, jsonify, request
import requests

app = Flask(__name__)
backend_url = os.environ.get("FORECAST_API_URL", "http://localhost:8000/api/forecast")


@app.route("/api/forecast", methods=["POST"])
def proxy_forecast():
    if request.content_type and request.content_type.startswith("multipart/form-data"):
        files = {"file": request.files.get("file")} if request.files.get("file") else {}
        data = {k: v for k, v in request.form.items()}
        response = requests.post(backend_url, data=data, files=files, timeout=120)
    else:
        response = requests.post(backend_url, json=request.json, timeout=120)

    return jsonify(response.json()), response.status_code


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "proxy healthy", "backend_url": backend_url})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
