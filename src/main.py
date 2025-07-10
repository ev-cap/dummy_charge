from flask import Flask, jsonify, request
from flask_cors import CORS
import json
import random
import time

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Load dummy data
with open('stations.json') as f:
    stations_data = json.load(f)

# In-memory storage for session data (for simplicity)
sessions = {}

AUTH_TOKEN = "UNAD-TEST-TOKEN"

def authenticate():
    token = request.headers.get('Authorization')
    if not token or token != f'Bearer {AUTH_TOKEN}':
        return False
    return True

@app.before_request
def before_request():
    if request.endpoint not in ['static', 'authenticate_route'] and not authenticate():
        return jsonify({"message": "Unauthorized"}), 401

# Helper function to simulate connector availability
def get_connector_status():
    return random.choice(["Available", "Occupied", "OutOfService"])

# Helper function to find a station by ID
def find_station(station_id):
    for station in stations_data:
        if station['id'] == station_id:
            return station
    return None

# Helper function to find a connector within a station
def find_connector(station, connector_id):
    for connector in station['connectors']:
        if connector['id'] == connector_id:
            return connector
    return None

@app.route("/stations", methods=["GET"])
def get_stations():
    stations_with_status = []
    for station in stations_data:
        available_connectors = 0
        total_connectors = len(station["connectors"])
        for connector in station["connectors"]:
            if get_connector_status() == "Available":
                available_connectors += 1
        station_copy = station.copy()
        station_copy["available_connectors"] = available_connectors
        station_copy["total_connectors"] = total_connectors
        stations_with_status.append(station_copy)
    return jsonify(stations_with_status)

@app.route("/stations/<station_id>", methods=["GET"])
def get_station_details(station_id):
    station = find_station(station_id)
    if not station:
        return jsonify({"message": "Station not found"}), 404

    detailed_connectors = []
    for connector in station["connectors"]:
        connector_copy = connector.copy()
        connector_copy["status"] = get_connector_status()
        detailed_connectors.append(connector_copy)
    
    station_copy = station.copy()
    station_copy["connectors"] = detailed_connectors
    return jsonify(station_copy)

@app.route("/sessions", methods=["POST"])
def create_session():
    data = request.get_json()
    station_id = data.get("station_id")
    connector_id = data.get("connector_id")

    station = find_station(station_id)
    if not station:
        return jsonify({"message": "Station not found"}), 404

    connector = find_connector(station, connector_id)
    if not connector:
        return jsonify({"message": "Connector not found"}), 404

    # Simulate connector availability check
    if get_connector_status() != "Available":
        return jsonify({"message": "Connector not available"}), 400

    session_id = f"SES-{random.randint(10000, 99999)}"
    sessions[session_id] = {
        "station_id": station_id,
        "connector_id": connector_id,
        "status": "Reserved",
        "start_time": None,
        "kwh_delivered": 0,
        "duration": 0
    }
    return jsonify({"session_id": session_id, "status": "Reserved"}), 201

@app.route("/sessions/<session_id>/start", methods=["POST"])
def start_session(session_id):
    session = sessions.get(session_id)

    if not session:
        return jsonify({"message": "Session not found"}), 404

    if session["status"] != "Reserved":
        return jsonify({"message": "Session is not in a reserved state"}), 400

    session["status"] = "Charging"
    session["start_time"] = time.time()
    return jsonify({"session_id": session_id, "status": "Charging"})

@app.route("/sessions/<session_id>", methods=["GET"])
def get_session_status(session_id):
    session = sessions.get(session_id)

    if not session:
        return jsonify({"message": "Session not found"}), 404

    if session["status"] == "Charging":
        elapsed_time = time.time() - session["start_time"]
        # Simulate kWh delivered over time
        session["kwh_delivered"] = round(elapsed_time * 0.1, 2)  # 0.1 kWh per second
        session["duration"] = round(elapsed_time, 0)
        # Simulate random completion
        if random.random() < 0.05: # 5% chance to complete each poll
            session["status"] = "Completed"

    return jsonify(session)

@app.route("/sessions/<session_id>/stop", methods=["POST"])
def stop_session(session_id):
    session = sessions.get(session_id)

    if not session:
        return jsonify({"message": "Session not found"}), 404

    if session["status"] == "Completed":
        return jsonify({"message": "Session already completed", "report": session}), 200

    session["status"] = "Completed"
    if session["start_time"] is not None:
        session["duration"] = round(time.time() - session["start_time"], 0)
        session["kwh_delivered"] = round(session["duration"] * 0.1, 2)
    else:
        session["duration"] = 0
        session["kwh_delivered"] = 0

    return jsonify({"message": "Session stopped", "report": session})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)

