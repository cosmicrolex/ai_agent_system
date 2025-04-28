# communication/event_bus.py
from flask_cors import CORS
from flask import Flask, request, jsonify
import logging
import os

SECRET_TOKEN = "mysecrettoken"  # You can change this secret

# Ensure log directory exists
log_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../logs'))
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

log_file_path = os.path.join(log_dir, 'event_bus.log')

# Configure logging
logging.basicConfig(
    filename=log_file_path,
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

app = Flask(__name__)
CORS(app)

events_storage = []

@app.route('/event', methods=['POST'])
def receive_event():
    token = request.headers.get('Authorization')
    if token != SECRET_TOKEN:
        return jsonify({"error": "Unauthorized"}), 401

    data = request.get_json()
    agent_from = data.get('from')
    agent_to = data.get('to')
    message = data.get('message')

    events_storage.append({
        "from": agent_from,
        "to": agent_to,
        "message": message
    })

    logging.info(f"Received Event: From {agent_from} To {agent_to} Message: {message}")

    return jsonify({"status": "Message Received", "from": agent_from, "to": agent_to}), 200
@app.route('/get_events/<agent_name>', methods=['GET'])
def get_events(agent_name):
    token = request.headers.get('Authorization')
    if token != SECRET_TOKEN:
        return jsonify({"error": "Unauthorized"}), 401

    my_events = [e for e in events_storage if e["to"] == agent_name]
    for e in my_events:
        events_storage.remove(e)

    return jsonify(my_events), 200


if __name__ == "__main__":
    app.run(port=5000)
