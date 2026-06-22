#!/usr/bin/env python
"""Test ML API endpoints with authentication."""

import requests
import json

BASE_URL = "http://localhost:5000"

# Create a session to maintain cookies
session = requests.Session()

print("📝 Logging in as admin...")
login_response = session.post(
    f"{BASE_URL}/login",
    data={
        "username": "admin",
        "password": "Admin@123"
    },
    allow_redirects=False
)
print(f"Login Status: {login_response.status_code}")

print("\n" + "="*60)
print("🤖 Testing ML API Endpoints")
print("="*60)

# Test 1: Clash Risk Prediction
print("\n✅ Test 1: Clash Risk Prediction")
try:
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
    if response.status_code == 200:
        result = response.json()
        print(f"Risk Score: {result.get('risk', {}).get('risk_score'):.2f}")
        print(f"Risk Level: {result.get('risk', {}).get('risk_level')}")
        print(f"Confidence: {result.get('risk', {}).get('confidence'):.2f}")
    else:
        print(f"Response: {response.text[:200]}")
except Exception as e:
    print(f"Error: {e}")

# Test 2: Slot Recommendations
print("\n✅ Test 2: Slot Recommendations")
try:
    response = session.get(
        f"{BASE_URL}/api/ml/slot-recommendations",
        params={
            "faculty_id": 1,
            "division_id": 6,
            "subject_id": 1,
            "preferred_day": "Monday"
        }
    )
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        result = response.json()
        recs = result.get('recommendations', [])
        print(f"Recommendations Found: {len(recs)}")
        for i, rec in enumerate(recs[:2], 1):
            print(f"  {i}. {rec.get('day')} at {rec.get('time_range')} (Risk: {rec.get('clash_risk'):.2f})")
    else:
        print(f"Response: {response.text[:200]}")
except Exception as e:
    print(f"Error: {e}")

# Test 3: Faculty Recommendations
print("\n✅ Test 3: Faculty Recommendations")
try:
    response = session.get(
        f"{BASE_URL}/api/ml/recommend-faculty",
        params={
            "subject_id": 1,
            "division_id": 6,
            "preferred_day": "Monday",
            "preferred_time_slot_id": 1
        }
    )
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        result = response.json()
        recs = result.get('recommendations', [])
        print(f"Recommendations Found: {len(recs)}")
        for i, rec in enumerate(recs[:2], 1):
            print(f"  {i}. {rec.get('faculty_name')} (Score: {rec.get('overall_score'):.2f})")
    else:
        print(f"Response: {response.text[:200]}")
except Exception as e:
    print(f"Error: {e}")

# Test 4: Clash Risk Summary
print("\n✅ Test 4: Clash Risk Summary")
try:
    response = session.get(
        f"{BASE_URL}/api/ml/clash-risk-summary",
        params={"division_id": 6}
    )
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        result = response.json()
        summary = result.get('summary', {})
        print(f"Average Risk Score: {summary.get('average_risk_score'):.2f}")
        print(f"Total Entries: {summary.get('total_entries')}")
        print(f"High Risk: {summary.get('high_risk_entries')}, Medium: {summary.get('medium_risk_entries')}, Low: {summary.get('low_risk_entries')}")
    else:
        print(f"Response: {response.text[:200]}")
except Exception as e:
    print(f"Error: {e}")

# Test 5: Evaluate Timetable Quality
print("\n✅ Test 5: Timetable Quality Evaluation")
try:
    response = session.post(
        f"{BASE_URL}/api/ml/evaluate-timetable",
        json={"division_id": 6}
    )
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        result = response.json()
        quality = result.get('quality', {})
        print(f"Quality Score: {quality.get('quality_score'):.2f}")
        print(f"Feasibility: {quality.get('feasibility')}")
        issues = quality.get('issues', [])
        if issues:
            print(f"Issues Found: {len(issues)}")
            for issue in issues[:2]:
                print(f"  - {issue}")
    else:
        print(f"Response: {response.text[:200]}")
except Exception as e:
    print(f"Error: {e}")

print("\n" + "="*60)
print("✅ ML API TESTING COMPLETE!")
print("="*60)
