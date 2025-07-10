#!/usr/bin/env python3
import requests
import json
import time

# Test the API
headers = {'Authorization': 'Bearer UNAD-TEST-TOKEN'}
base_url = 'http://localhost:5001'

def test_get_stations():
    print("Testing GET /stations...")
    try:
        response = requests.get(f'{base_url}/stations', headers=headers, timeout=5)
        print(f'Status Code: {response.status_code}')
        print(f'Response: {response.text}')
        return response.status_code == 200
    except Exception as e:
        print(f'Error: {e}')
        return False

def test_get_station_details():
    print("\nTesting GET /stations/ST-1001...")
    try:
        response = requests.get(f'{base_url}/stations/ST-1001', headers=headers, timeout=5)
        print(f'Status Code: {response.status_code}')
        print(f'Response: {response.text}')
        return response.status_code == 200
    except Exception as e:
        print(f'Error: {e}')
        return False

def test_create_session():
    print("\nTesting POST /sessions...")
    # Try multiple times since availability is random
    for attempt in range(10):
        try:
            data = {
                "station_id": "ST-1001",
                "connector_id": "CON-001"
            }
            response = requests.post(f'{base_url}/sessions', headers=headers, json=data, timeout=5)
            print(f'Attempt {attempt + 1} - Status Code: {response.status_code}')
            print(f'Response: {response.text}')
            if response.status_code == 201:
                return response.json().get('session_id')
            elif response.status_code == 400:
                print("Connector not available, trying again...")
                time.sleep(0.5)
                continue
        except Exception as e:
            print(f'Error: {e}')
    return None

def test_start_session(session_id):
    print(f"\nTesting POST /sessions/{session_id}/start...")
    try:
        response = requests.post(f'{base_url}/sessions/{session_id}/start', headers=headers, timeout=5)
        print(f'Status Code: {response.status_code}')
        print(f'Response: {response.text}')
        return response.status_code == 200
    except Exception as e:
        print(f'Error: {e}')
        return False

def test_get_session_status(session_id):
    print(f"\nTesting GET /sessions/{session_id}...")
    try:
        response = requests.get(f'{base_url}/sessions/{session_id}', headers=headers, timeout=5)
        print(f'Status Code: {response.status_code}')
        print(f'Response: {response.text}')
        return response.status_code == 200
    except Exception as e:
        print(f'Error: {e}')
        return False

def test_stop_session(session_id):
    print(f"\nTesting POST /sessions/{session_id}/stop...")
    try:
        response = requests.post(f'{base_url}/sessions/{session_id}/stop', headers=headers, timeout=5)
        print(f'Status Code: {response.status_code}')
        print(f'Response: {response.text}')
        return response.status_code == 200
    except Exception as e:
        print(f'Error: {e}')
        return False

if __name__ == '__main__':
    print("Starting API tests...")
    
    # Test basic endpoints
    if not test_get_stations():
        print("Failed to get stations")
        exit(1)
    
    if not test_get_station_details():
        print("Failed to get station details")
        exit(1)
    
    # Test session flow
    session_id = test_create_session()
    if not session_id:
        print("Failed to create session")
        exit(1)
    
    if not test_start_session(session_id):
        print("Failed to start session")
        exit(1)
    
    if not test_get_session_status(session_id):
        print("Failed to get session status")
        exit(1)
    
    if not test_stop_session(session_id):
        print("Failed to stop session")
        exit(1)
    
    print("\nAll tests passed!")

