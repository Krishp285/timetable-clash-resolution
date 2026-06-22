#!/usr/bin/env python
"""Test ML API with proper session handling."""

import requests

BASE_URL = "http://localhost:5000"

# Create session with proper cookie handling
session = requests.Session()

print("📝 Logging in...")
# Follow redirects on login
response = session.post(
    f"{BASE_URL}/login",
    data={
        "username": "admin",
        "password": "Admin@123"
    },
    allow_redirects=True  # Follow redirect to dashboard
)
print(f"Login Response Status: {response.status_code}")
print(f"Final URL after login: {response.url}")

# Check if we're authenticated by checking if we can access admin page
admin_check = session.get(f"{BASE_URL}/admin/dashboard")
print(f"Admin Dashboard Access: {admin_check.status_code}")

if "Dashboard" in admin_check.text:
    print("✅ Successfully authenticated!\n")
else:
    print("❌ Authentication may have failed\n")

# Now test ML endpoints
print("=" * 60)
print("🤖 Testing ML API Endpoints")
print("=" * 60)

# Test 1: Clash Risk Prediction
print("\n✅ Test 1: Clash Risk Prediction")
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

if "application/json" in response.headers.get('Content-Type', ''):
    try:
        result = response.json()
        if result.get('success'):
            print(f"✅ SUCCESS!")
            risk = result.get('risk', {})
            print(f"   Risk Score: {risk.get('risk_score'):.2f}")
            print(f"   Risk Level: {risk.get('risk_level')}")
            print(f"   Confidence: {risk.get('confidence'):.2f}")
        else:
            print(f"Response: {result}")
    except Exception as e:
        print(f"JSON Parse Error: {e}")
        print(f"Response Preview: {response.text[:200]}")
else:
    print(f"❌ Not JSON response. First 300 chars:\n{response.text[:300]}")

print("\n" + "=" * 60)
print("Testing Complete")
print("=" * 60)
