#!/usr/bin/env python
"""Test ML API endpoints - Simple version."""

import requests
import json

BASE_URL = "http://localhost:5000"

print("Testing ML Clash Risk Prediction API...")
try:
    response = requests.post(
        f"{BASE_URL}/api/ml/predict-clash-risk",
        json={
            "faculty_id": 1,
            "division_id": 6,
            "subject_id": 1,
            "time_slot_id": 1,
            "day": "Monday",
            "room_number": "101"
        }
    )
    print(f"Status Code: {response.status_code}")
    print(f"Response Text: {response.text}")
    if response.status_code == 200:
        result = response.json()
        print(f"Response JSON: {json.dumps(result, indent=2)}")
except Exception as e:
    print(f"Error: {e}")

print("\n" + "="*60)
print("Testing Clash Risk Summary API...")
try:
    response = requests.get(
        f"{BASE_URL}/api/ml/clash-risk-summary",
        params={"division_id": 6}
    )
    print(f"Status Code: {response.status_code}")
    print(f"Response Text: {response.text}")
    if response.status_code == 200:
        result = response.json()
        print(f"Response JSON: {json.dumps(result, indent=2)}")
except Exception as e:
    print(f"Error: {e}")
