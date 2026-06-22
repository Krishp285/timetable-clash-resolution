#!/usr/bin/env python
"""Debug ML API responses."""

import requests

BASE_URL = "http://localhost:5000"
session = requests.Session()

# Login
session.post(
    f"{BASE_URL}/login",
    data={"username": "admin", "password": "Admin@123"},
    allow_redirects=False
)

# Make request and check response
response = session.post(
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

print(f"Status: {response.status_code}")
print(f"Content-Type: {response.headers.get('Content-Type')}")
print(f"Response Length: {len(response.text)}")
print(f"First 500 chars: {response.text[:500]}")
