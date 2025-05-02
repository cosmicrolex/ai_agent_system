from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import threading
import time
import os

app = Flask(__name__)
CORS(app)  # ✅ Apply CORS to ALL routes

# Global in-memory event log
event_log = []

AUTH_TOKEN = "mysecrettoken"

@app.route('/event', methods=['POST'])
def send_event():
    auth = request.headers.get("Authorization")
    if auth != AUTH_TOKEN:
        return jsonify({"error": "Unauthorized"}), 403

    data = request.get_json()
    sender = data.get("from")
    receiver = data.get("to")
    message = data.get("message")

    if not sender or not receiver or not message:
        return jsonify({"error": "Missing fields"}), 400

    event = {
        "from": sender,
        "to": receiver,
        "message": message,
        "timestamp": time.time()
    }
    event_log.append(event)
    return jsonify({"status": "Event received"}), 200

@app.route('/get_events/<receiver>', methods=['GET'])
def get_events(receiver):
    auth = request.headers.get("Authorization")
    if auth != AUTH_TOKEN:
        return jsonify({"error": "Unauthorized"}), 403

    relevant_events = [e for e in event_log if e['to'] == receiver]
    return jsonify(relevant_events)

@app.route('/logs/<filename>', methods=['GET'])
def get_log_file(filename):
    try:
        log_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../logs'))
        return send_from_directory(log_dir, filename)
    except Exception as e:
        return jsonify({"error": f"Failed to load log file: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(port=5000, debug=True)
