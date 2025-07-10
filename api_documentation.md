# Dummy EV Charging Station API

## Overview

This is a RESTful API that simulates an end-to-end EV charging session flow. It includes features like station search, connector availability checking, session management, and charging simulation with realistic wait times and randomized availability.

## Base URL

**Public URL:** https://5000-i3wiuqqjd83chhkatvpr0-33ec9690.manusvm.computer

## Authentication

All endpoints require Bearer token authentication. Include the following header in your requests:

```
Authorization: Bearer UNAD-TEST-TOKEN
```

## Endpoints

### 1. GET /stations
Search for charging stations.

**Response:**
```json
[
  {
    "id": "ST-1001",
    "name": "City Mall Charging Station",
    "city": "Ahmedabad",
    "latitude": 23.03,
    "longitude": 72.54,
    "available_connectors": 1,
    "total_connectors": 2,
    "connectors": [
      {
        "id": "CON-001",
        "type": "Type 2",
        "power_kW": 22
      },
      {
        "id": "CON-002",
        "type": "CCS",
        "power_kW": 50
      }
    ]
  }
]
```

### 2. GET /stations/{station_id}
Get detailed information about a specific station including real-time connector status.

**Response:**
```json
{
  "id": "ST-1001",
  "name": "City Mall Charging Station",
  "city": "Ahmedabad",
  "latitude": 23.03,
  "longitude": 72.54,
  "connectors": [
    {
      "id": "CON-001",
      "type": "Type 2",
      "power_kW": 22,
      "status": "Available"
    },
    {
      "id": "CON-002",
      "type": "CCS",
      "power_kW": 50,
      "status": "Occupied"
    }
  ]
}
```

### 3. POST /sessions
Create a new charging session by reserving a connector.

**Request Body:**
```json
{
  "station_id": "ST-1001",
  "connector_id": "CON-001"
}
```

**Response (201 Created):**
```json
{
  "session_id": "SES-12345",
  "status": "Reserved"
}
```

**Error Response (400 Bad Request):**
```json
{
  "message": "Connector not available"
}
```

### 4. POST /sessions/{session_id}/start
Start charging for a reserved session.

**Response:**
```json
{
  "session_id": "SES-12345",
  "status": "Charging"
}
```

### 5. GET /sessions/{session_id}
Get the current status of a charging session.

**Response:**
```json
{
  "session_id": "SES-12345",
  "station_id": "ST-1001",
  "connector_id": "CON-001",
  "status": "Charging",
  "start_time": 1752172656.945057,
  "duration": 120.0,
  "kwh_delivered": 12.0
}
```

### 6. POST /sessions/{session_id}/stop
Stop a charging session and get the completion report.

**Response:**
```json
{
  "message": "Session stopped",
  "report": {
    "session_id": "SES-12345",
    "station_id": "ST-1001",
    "connector_id": "CON-001",
    "status": "Completed",
    "start_time": 1752172656.945057,
    "duration": 300.0,
    "kwh_delivered": 30.0
  }
}
```

## Session Status Values

- **Reserved**: Connector is reserved but charging hasn't started
- **Charging**: Active charging session in progress
- **Completed**: Charging session has ended

## Connector Status Values

- **Available**: Connector is free and can be used
- **Occupied**: Connector is currently in use
- **OutOfService**: Connector is not operational

## Features

1. **Randomized Availability**: Connector availability is randomly simulated to mimic real-world conditions
2. **Charging Simulation**: Energy delivery is simulated at 0.1 kWh per second during active charging
3. **Random Completion**: 5% chance per status check that a charging session will complete automatically
4. **Token-based Authentication**: All endpoints require valid Bearer token
5. **CORS Support**: API supports cross-origin requests for frontend integration

## Example Usage Flow

1. **Search Stations**: `GET /stations`
2. **Check Station Details**: `GET /stations/ST-1001`
3. **Reserve Connector**: `POST /sessions` with station and connector IDs
4. **Start Charging**: `POST /sessions/{session_id}/start`
5. **Monitor Progress**: Repeatedly `GET /sessions/{session_id}` to check status
6. **Stop Charging**: `POST /sessions/{session_id}/stop` to end session

## Error Handling

The API returns appropriate HTTP status codes:
- `200 OK`: Successful request
- `201 Created`: Resource created successfully
- `400 Bad Request`: Invalid request or resource not available
- `401 Unauthorized`: Missing or invalid authentication token
- `404 Not Found`: Resource not found

## Testing

A comprehensive test script is included (`test_api.py`) that demonstrates the complete end-to-end flow and validates all endpoints.

